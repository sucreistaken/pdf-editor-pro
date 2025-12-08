"""
PDF Tools - Configuration
Environment variable ile konfigure edilebilir ayarlar.
"""
import os
import sys
import secrets
import glob as _glob
import logging

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Environment (development / production)
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')


def _find_poppler():
    """Poppler binary yolunu otomatik bul. Oncelik: env var > Program Files tarama > None"""
    env_path = os.environ.get('POPPLER_PATH')
    if env_path and os.path.isdir(env_path):
        return env_path

    # Program Files altinda poppler* klasorlerini tara
    for program_dir in [r'C:\Program Files', r'C:\Program Files (x86)']:
        if not os.path.isdir(program_dir):
            continue
        for candidate in sorted(_glob.glob(os.path.join(program_dir, 'poppler*')), reverse=True):
            # Library\bin veya bin altini kontrol et
            for sub in [os.path.join(candidate, 'Library', 'bin'), os.path.join(candidate, 'bin')]:
                if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, 'pdftoppm.exe')):
                    return sub
    # Bulunamazsa None dondur (pdf2image PATH'ten dener)
    return None


# Flask
_secret_key_env = os.environ.get('SECRET_KEY', '')
if not _secret_key_env and FLASK_ENV == 'production':
    logging.getLogger(__name__).critical(
        "SECRET_KEY environment variable is not set! "
        "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    )
    sys.exit(1)
SECRET_KEY = _secret_key_env or 'dev-only-insecure-key-' + secrets.token_hex(8)
MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB

# Klasorler
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')

# Poppler (pdf2image icin)
POPPLER_PATH = _find_poppler()

# Dosya temizleme
CLEANUP_MAX_AGE_HOURS = int(os.environ.get('CLEANUP_MAX_AGE_HOURS', 1))

# Rate limiting
RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 30))

# Site / SEO
SITE_NAME = os.environ.get('SITE_NAME', 'PDFEdit')
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')
DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'tr')

# Analytics
GA_MEASUREMENT_ID = os.environ.get('GA_MEASUREMENT_ID', '')

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.environ.get('LOG_FILE', '')
