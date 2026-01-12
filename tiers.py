"""
PDF Tools - Arac Katmanlari ve Kullanim Sinirlamalari
Odeme altyapisi hazirlik modulu.
"""
import time
from functools import wraps
from flask import request, jsonify

# Arac katmanlari
TIERS = {
    'free': {
        'tools': [
            'merge', 'split', 'rotate', 'compress',
            'img_to_pdf', 'extract_text', 'crop'
        ],
        'daily_limit': None,  # Sinirsiz
        'max_file_size': 50 * 1024 * 1024,  # 50MB
    },
    'limited_free': {
        'tools': [
            'encrypt', 'watermark', 'extract_images', 'repair',
            'pdf_to_image', 'reorder', 'numbering', 'metadata',
            'compare', 'pdf_to_excel', 'form_fill', 'pdf_to_word', 'pdf_to_pdfa'
        ],
        'daily_limit': 10,
        'max_file_size': 100 * 1024 * 1024,  # 100MB
    },
    'premium': {
        'tools': [
            'html_to_pdf', 'batch_processing', 'ocr',
            'digital_signature', 'api_access'
        ],
        'daily_limit': None,
        'max_file_size': 500 * 1024 * 1024,  # 500MB
    }
}

# Tum araclarin tier eslesmesi
TOOL_TIER_MAP = {}
for tier_name, tier_data in TIERS.items():
    for tool in tier_data['tools']:
        TOOL_TIER_MAP[tool] = tier_name


def get_tool_tier(tool_name):
    """Aracin hangi katmanda oldugunu dondur"""
    return TOOL_TIER_MAP.get(tool_name, 'free')


def is_premium(tool_name):
    """Arac premium mi?"""
    return get_tool_tier(tool_name) == 'premium'


def is_limited(tool_name):
    """Arac gunluk sinirli mi?"""
    return get_tool_tier(tool_name) == 'limited_free'


# IP bazli kullanim takibi (bellek icinde, uretim icin veritabani gerekir)
_usage_store = {}


def track_usage(tool_name, ip_address):
    """Kullanimi kaydet ve siniri kontrol et"""
    tier = get_tool_tier(tool_name)

    if tier == 'free':
        return {'allowed': True}

    tier_data = TIERS.get(tier, {})
    daily_limit = tier_data.get('daily_limit')

    if daily_limit is None:
        return {'allowed': True}

    today = time.strftime('%Y-%m-%d')
    key = f"{ip_address}:{tool_name}:{today}"

    current = _usage_store.get(key, 0)

    if current >= daily_limit:
        return {
            'allowed': False,
            'remaining': 0,
            'limit': daily_limit,
            'message': f'Günlük kullanım limitine ulaştınız ({daily_limit}/{daily_limit}). Yarın tekrar deneyin.'
        }

    _usage_store[key] = current + 1

    return {
        'allowed': True,
        'remaining': daily_limit - current - 1,
        'limit': daily_limit
    }


def _get_client_ip():
    """Get real client IP, supporting reverse proxy X-Forwarded-For header."""
    forwarded = request.headers.get('X-Forwarded-For', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.remote_addr or '127.0.0.1'


def rate_limit(tool_name):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip = _get_client_ip()
            usage = track_usage(tool_name, ip)

            if not usage['allowed']:
                return jsonify({
                    'success': False,
                    'error': usage['message'],
                    'rate_limited': True
                }), 429

            response = f(*args, **kwargs)
            return response
        return wrapper
    return decorator


# Veritabani semasi (dokumantas yon icin)
DB_SCHEMA = """
-- Kullanici tablosu
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    tier TEXT DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Kullanim log tablosu
CREATE TABLE IF NOT EXISTS usage_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    ip_address TEXT,
    tool_name TEXT NOT NULL,
    file_size INTEGER,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Gunluk kullanim ozeti
CREATE TABLE IF NOT EXISTS daily_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    date TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    UNIQUE(ip_address, tool_name, date)
);
"""
