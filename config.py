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
MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 500 * 1024 * 1024))  # 500MB

# Klasorler
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')

# Poppler (pdf2image icin)
POPPLER_PATH = _find_poppler()


def _find_tesseract():
    """Tesseract binary yolunu otomatik bul."""
    import shutil as _shutil
    env_path = os.environ.get('TESSERACT_PATH')
    if env_path and os.path.isfile(env_path):
        return env_path
    # Sistem PATH'inde ara
    t = _shutil.which('tesseract')
    if t:
        return t
    # Windows varsayilan yollar
    for p in [r'C:\Program Files\Tesseract-OCR\tesseract.exe',
              r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe']:
        if os.path.isfile(p):
            return p
    return None


def _find_libreoffice():
    """LibreOffice binary yolunu otomatik bul."""
    import shutil as _shutil
    env_path = os.environ.get('LIBREOFFICE_PATH')
    if env_path and os.path.isfile(env_path):
        return env_path
    lo = _shutil.which('libreoffice') or _shutil.which('soffice')
    if lo:
        return lo
    for p in [r'C:\Program Files\LibreOffice\program\soffice.exe',
              r'C:\Program Files (x86)\LibreOffice\program\soffice.exe']:
        if os.path.isfile(p):
            return p
    return None


# Tesseract (OCR icin)
TESSERACT_PATH = _find_tesseract()

# LibreOffice (Office -> PDF icin)
LIBREOFFICE_PATH = _find_libreoffice()

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

# iframe gomme (varsayilan: herkese acik, kisitlamak icin domain listesi ver)
# Ornek: ALLOWED_FRAME_ORIGINS="https://forum.example.com https://mysite.com"
ALLOWED_FRAME_ORIGINS = os.environ.get('ALLOWED_FRAME_ORIGINS', '*')

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.environ.get('LOG_FILE', '')
