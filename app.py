from flask import Flask, render_template, request, send_file, jsonify, Response, redirect, url_for, g, make_response
from flask_wtf.csrf import CSRFProtect
import os
from werkzeug.utils import secure_filename
import uuid
import cv2
import numpy as np
from pdf2image import convert_from_path
import img2pdf
import json
import time
import zipfile
import shutil
import threading
import logging
import hashlib

import fitz as fitz_mod
import base64

import config
from utils import api_success, api_error, safe_path, format_size
from i18n import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, get_translator, get_js_translations
from seo import get_tool_seo, get_site_seo, get_all_tool_slugs, TOOLS
from tiers import rate_limit

# Import our tools
from tools.pdf_merger import merge_pdfs
from tools.pdf_splitter import split_pdf_by_pages, extract_pages
from tools.pdf_encryptor import encrypt_pdf, decrypt_pdf
from tools.img_to_pdf import images_to_pdf
from tools.watermark import add_text_watermark, add_image_watermark
from tools.pdf_compress import compress_pdf
from tools.pdf_rotate import rotate_pdf
from tools.pdf_text_extract import extract_text
from tools.pdf_image_extract import extract_images
from tools.pdf_reorder import get_pdf_thumbnails, reorder_pdf_pages
from tools.pdf_repair import repair_pdf, analyze_pdf
from tools.pdf_to_image import pdf_to_images_zip
from tools.pdf_metadata import get_metadata, update_metadata, clear_metadata
from tools.pdf_numbering import add_page_numbers
from tools.pdf_crop import crop_pdf, auto_crop_pdf
from tools.pdf_compare import compare_pdfs
from tools.pdf_to_excel import pdf_to_excel
from tools.pdf_form_fill import get_form_fields, fill_form
from tools.pdf_to_word import pdf_to_word
from tools.pdf_to_pdfa import convert_to_pdfa

# Logging setup
from logging.handlers import RotatingFileHandler

def _setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = getattr(logging, config.LOG_LEVEL, logging.INFO)

    logging.basicConfig(level=log_level, format=log_format)

    if config.LOG_FILE:
        log_dir = os.path.dirname(config.LOG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            config.LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(log_level)
        logging.getLogger().addHandler(file_handler)

_setup_logging()
logger = logging.getLogger(__name__)

_app_start_time = time.time()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# CSRF korumasi
csrf = CSRFProtect(app)

# Gzip compression
try:
    from flask_compress import Compress
    Compress(app)
except ImportError:
    pass

UPLOAD_FOLDER = config.UPLOAD_FOLDER
OUTPUT_FOLDER = config.OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Progress tracking (thread-safe: single worker + multiple threads)
progress_data = {}
_progress_lock = threading.Lock()

# --- progress_data bellek temizleme (FAZ 1.7) ---
def cleanup_progress_data():
    """1 saatten eski progress kayitlarini temizle"""
    while True:
        time.sleep(600)  # 10 dakikada bir kontrol
        now = time.time()
        expired = [k for k, v in progress_data.items()
                   if now - v.get('created_at', now) > config.CLEANUP_MAX_AGE_HOURS * 3600]
        for k in expired:
            del progress_data[k]
        if expired:
            logger.info(f"Temizlendi: {len(expired)} eski progress kaydi silindi")

cleanup_thread = threading.Thread(target=cleanup_progress_data, daemon=True)
cleanup_thread.start()

# --- Otomatik dosya temizleme (FAZ 5.5) ---
def _get_active_file_paths():
    """Aktif job'larin kullandigi dosya yollarini dondur"""
    active_paths = set()
    for key, data in progress_data.items():
        for field in ('pdf_path', 'logo_path', 'output_path'):
            path = data.get(field)
            if path:
                active_paths.add(os.path.realpath(path))
    return active_paths


def cleanup_old_files():
    """outputs ve uploads klasorlerindeki eski dosyalari temizle"""
    while True:
        time.sleep(1800)  # 30 dakikada bir
        now = time.time()
        max_age = config.CLEANUP_MAX_AGE_HOURS * 3600
        active_paths = _get_active_file_paths()
        cleaned = 0
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            if not os.path.exists(folder):
                continue
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                try:
                    real_path = os.path.realpath(item_path)
                    if real_path in active_paths:
                        continue
                    mtime = os.path.getmtime(item_path)
                    if now - mtime > max_age:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                            cleaned += 1
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            cleaned += 1
                except Exception as e:
                    logger.warning(f"Cleanup error for {item}: {e}")
                    continue
        if cleaned:
            logger.info(f"Dosya temizleme: {cleaned} eski dosya/klasor silindi")

file_cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
file_cleanup_thread.start()

def allowed_file(filename, file_type):
    if file_type == 'pdf':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
    else:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


# ==================== SECURITY HEADERS ====================
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    if config.FLASK_ENV == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'"
    )

    return response


# ==================== REQUEST LOGGING ====================
@app.before_request
def log_request_start():
    g.request_start_time = time.time()

@app.after_request
def log_request_end(response):
    if hasattr(g, 'request_start_time'):
        duration_ms = (time.time() - g.request_start_time) * 1000
        if request.path.startswith('/api/'):
            logger.info(
                "API %s %s -> %s (%.0fms) [%s]",
                request.method, request.path, response.status_code,
                duration_ms, request.remote_addr
            )
    return response


# ==================== HEALTH CHECK ====================
@app.route('/health')
def health_check():
    uptime_seconds = int(time.time() - _app_start_time)
    try:
        disk = shutil.disk_usage(os.path.abspath('.'))
        disk_free_gb = round(disk.free / (1024**3), 2)
        disk_total_gb = round(disk.total / (1024**3), 2)
    except Exception:
        disk_free_gb = -1
        disk_total_gb = -1

    return jsonify({
        'status': 'ok',
        'uptime_seconds': uptime_seconds,
        'disk_free_gb': disk_free_gb,
        'disk_total_gb': disk_total_gb,
        'active_jobs': len(progress_data),
        'environment': config.FLASK_ENV,
    })


# ==================== I18N MIDDLEWARE ====================
@app.before_request
def set_language():
    """Dil algilama: URL prefix > cookie > Accept-Language > default"""
    # API ve download icin i18n gereksiz
    if request.path.startswith(('/api/', '/download', '/upload', '/process/', '/static/', '/health')):
        g.lang = DEFAULT_LANGUAGE
        return

    parts = request.path.strip('/').split('/', 1)
    if parts[0] in SUPPORTED_LANGUAGES:
        g.lang = parts[0]
    else:
        # Cookie'den veya Accept-Language'den dil al
        cookie_lang = request.cookies.get('lang')
        if cookie_lang in SUPPORTED_LANGUAGES:
            g.lang = cookie_lang
        else:
            accept = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
            g.lang = accept if accept else DEFAULT_LANGUAGE


_static_hash_cache = {}

def _static_hash(filename):
    """Statik dosya icin cache-busting hash uret"""
    if filename in _static_hash_cache:
        return _static_hash_cache[filename]
    filepath = os.path.join(app.static_folder, filename)
    try:
        with open(filepath, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()[:8]
    except Exception:
        h = ''
    _static_hash_cache[filename] = h
    return h


@app.context_processor
def inject_i18n():
    """Tum template'lere i18n degiskenleri enjekte et"""
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    return {
        '_': get_translator(lang),
        'lang': lang,
        'supported_languages': SUPPORTED_LANGUAGES,
        'site_seo': get_site_seo(lang),
        'site_url': config.SITE_URL,
        'site_name': config.SITE_NAME,
        'ga_measurement_id': config.GA_MEASUREMENT_ID,
        'js_translations': json.dumps(get_js_translations(lang)),
        'static_hash': _static_hash,
    }


def _detect_lang():
    """Accept-Language'den dil belirle (redirect icin)"""
    accept = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    cookie_lang = request.cookies.get('lang')
    if cookie_lang in SUPPORTED_LANGUAGES:
        return cookie_lang
    return accept if accept else DEFAULT_LANGUAGE


def _tool_render(tool_name, template):
    """Arac sayfasini SEO verileriyle render et"""
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    seo = get_tool_seo(tool_name, lang)
    return render_template(template, seo=seo, tool_name=tool_name)


# ==================== PDF PREVIEW API ====================
@app.route('/api/preview', methods=['POST'])
def api_preview():
    """PDF sayfasini base64 PNG olarak dondur (onizleme icin)"""
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    try:
        page_num = int(request.form.get('page', 0))
    except (ValueError, TypeError):
        page_num = 0
    try:
        width = int(request.form.get('width', 400))
    except (ValueError, TypeError):
        width = 400
    page_num = max(0, page_num)
    width = max(50, min(width, 2000))

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"preview_{job_id}_{pdf_file.filename}")
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(temp_path)

    try:
        doc = fitz_mod.open(temp_path)
        total_pages = len(doc)

        if page_num >= total_pages:
            page_num = 0

        page = doc[page_num]
        zoom = width / page.rect.width
        mat = fitz_mod.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img_data = pix.tobytes("png")
        b64 = base64.b64encode(img_data).decode('utf-8')

        result = {
            'success': True,
            'image': f'data:image/png;base64,{b64}',
            'total_pages': total_pages,
            'width': pix.width,
            'height': pix.height,
            'page_width': page.rect.width,
            'page_height': page.rect.height
        }

        doc.close()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Preview error: {e}", exc_info=True)
        return api_error('Önizleme oluşturulamadı')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ==================== SITEMAP + ROBOTS ====================
@app.route('/sitemap.xml')
def sitemap():
    """Dinamik sitemap (tum araclar x tum diller)"""
    pages = []
    base_url = config.SITE_URL.rstrip('/')

    # Ana sayfalar
    for lang in SUPPORTED_LANGUAGES:
        pages.append({
            'url': f'{base_url}/{lang}/',
            'changefreq': 'daily',
            'priority': '1.0'
        })

    # Arac sayfalari
    for slug in get_all_tool_slugs():
        for lang in SUPPORTED_LANGUAGES:
            pages.append({
                'url': f'{base_url}/{lang}/{slug}',
                'changefreq': 'weekly',
                'priority': '0.8'
            })

    # Blog sayfalari
    try:
        from blog import get_all_posts
        for lang in SUPPORTED_LANGUAGES:
            posts = get_all_posts(lang)
            pages.append({
                'url': f'{base_url}/{lang}/blog',
                'changefreq': 'weekly',
                'priority': '0.6'
            })
            for post in posts:
                pages.append({
                    'url': f'{base_url}/{lang}/blog/{post["slug"]}',
                    'changefreq': 'monthly',
                    'priority': '0.5'
                })
    except Exception:
        pass

    return render_template('sitemap.xml', pages=pages), 200, {'Content-Type': 'application/xml'}


@app.route('/robots.txt')
def robots():
    """robots.txt"""
    base_url = config.SITE_URL.rstrip('/')
    content = f"""User-agent: *
Allow: /

Disallow: /api/
Disallow: /download/
Disallow: /download-image/
Disallow: /upload
Disallow: /process/
Disallow: /uploads/
Disallow: /outputs/
Disallow: /static/

Sitemap: {base_url}/sitemap.xml
"""
    return content, 200, {'Content-Type': 'text/plain'}


# ==================== ROOT + REDIRECTS ====================
@app.route('/')
def root():
    """Kok URL: dil algila ve redirect"""
    lang = _detect_lang()
    return redirect(f'/{lang}/', code=302)


# Eski URL'lerden 301 redirect
TOOL_SLUGS = [
    'merge', 'split', 'encrypt', 'compress', 'watermark', 'rotate',
    'extract-text', 'extract-images', 'img-to-pdf', 'pdf-to-image',
    'html-to-pdf', 'reorder', 'repair', 'metadata', 'numbering',
    'crop', 'compare', 'pdf-to-excel', 'form-fill', 'pdf-to-word', 'pdf-to-pdfa',
]

@app.route('/logo-removal')
def logo_removal_redirect():
    """Logo removal: DOKUNULMADI, redirect yok, direkt render"""
    return render_template('logo_removal.html')

@app.route('/manual-selection')
def manual_selection_redirect():
    """Manual selection: DOKUNULMADI, direkt render"""
    return render_template('manual_selection.html')


def _old_route_redirect(tool_slug):
    """Eski URL'den yeni URL'ye 301 redirect"""
    lang = _detect_lang()
    return redirect(f'/{lang}/{tool_slug}', code=301)

# Eski URL'ler icin 301 redirect'ler olustur
for _slug in TOOL_SLUGS:
    app.add_url_rule(
        f'/{_slug}',
        endpoint=f'redirect_{_slug.replace("-", "_")}',
        view_func=lambda s=_slug: _old_route_redirect(s)
    )


# ==================== LANDING PAGE ====================
@app.route('/<lang>/')
def index(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/', code=302)
    g.lang = lang
    seo = get_site_seo(lang)
    return render_template('index.html', seo=seo)


# ==================== TOOL PAGE ROUTES (i18n) ====================
@app.route('/<lang>/merge')
def merge_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/merge', code=302)
    g.lang = lang
    return _tool_render('merge', 'merge.html')

@app.route('/<lang>/split')
def split_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/split', code=302)
    g.lang = lang
    return _tool_render('split', 'split.html')

@app.route('/<lang>/encrypt')
def encrypt_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/encrypt', code=302)
    g.lang = lang
    return _tool_render('encrypt', 'encrypt.html')

@app.route('/<lang>/compress')
def compress_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/compress', code=302)
    g.lang = lang
    return _tool_render('compress', 'compress.html')

@app.route('/<lang>/watermark')
def watermark_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/watermark', code=302)
    g.lang = lang
    return _tool_render('watermark', 'watermark.html')

@app.route('/<lang>/rotate')
def rotate_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/rotate', code=302)
    g.lang = lang
    return _tool_render('rotate', 'rotate.html')

@app.route('/<lang>/extract-text')
def extract_text_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/extract-text', code=302)
    g.lang = lang
    return _tool_render('extract-text', 'extract_text.html')

@app.route('/<lang>/extract-images')
def extract_images_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/extract-images', code=302)
    g.lang = lang
    return _tool_render('extract-images', 'extract_images.html')

@app.route('/<lang>/img-to-pdf')
def img_to_pdf_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/img-to-pdf', code=302)
    g.lang = lang
    return _tool_render('img-to-pdf', 'img_to_pdf.html')

@app.route('/<lang>/pdf-to-image')
def pdf_to_image_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/pdf-to-image', code=302)
    g.lang = lang
    return _tool_render('pdf-to-image', 'pdf_to_image.html')

@app.route('/<lang>/html-to-pdf')
def html_to_pdf_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/html-to-pdf', code=302)
    g.lang = lang
    return _tool_render('html-to-pdf', 'html_to_pdf.html')

@app.route('/<lang>/reorder')
def reorder_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/reorder', code=302)
    g.lang = lang
    return _tool_render('reorder', 'reorder.html')

@app.route('/<lang>/repair')
def repair_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/repair', code=302)
    g.lang = lang
    return _tool_render('repair', 'repair.html')

@app.route('/<lang>/metadata')
def metadata_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/metadata', code=302)
    g.lang = lang
    return _tool_render('metadata', 'metadata.html')

@app.route('/<lang>/numbering')
def numbering_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/numbering', code=302)
    g.lang = lang
    return _tool_render('numbering', 'numbering.html')

@app.route('/<lang>/crop')
def crop_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/crop', code=302)
    g.lang = lang
    return _tool_render('crop', 'crop.html')

@app.route('/<lang>/compare')
def compare_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/compare', code=302)
    g.lang = lang
    return _tool_render('compare', 'compare.html')

@app.route('/<lang>/pdf-to-excel')
def pdf_to_excel_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/pdf-to-excel', code=302)
    g.lang = lang
    return _tool_render('pdf-to-excel', 'pdf_to_excel.html')

@app.route('/<lang>/form-fill')
def form_fill_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/form-fill', code=302)
    g.lang = lang
    return _tool_render('form-fill', 'form_fill.html')

@app.route('/<lang>/pdf-to-word')
def pdf_to_word_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/pdf-to-word', code=302)
    g.lang = lang
    return _tool_render('pdf-to-word', 'pdf_to_word.html')

@app.route('/<lang>/pdf-to-pdfa')
def pdf_to_pdfa_page(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/pdf-to-pdfa', code=302)
    g.lang = lang
    return _tool_render('pdf-to-pdfa', 'pdf_to_pdfa.html')


# ==================== BLOG ROUTES ====================
@app.route('/<lang>/blog')
def blog_index(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/blog', code=302)
    g.lang = lang
    try:
        from blog import get_all_posts
        posts = get_all_posts(lang)
    except Exception:
        posts = []
    return render_template('blog_index.html', posts=posts)


@app.route('/<lang>/blog/<slug>')
def blog_post(lang, slug):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f'/{DEFAULT_LANGUAGE}/blog/{slug}', code=302)
    g.lang = lang
    try:
        from blog import get_post
        post = get_post(slug, lang)
    except Exception:
        post = None
    if not post:
        return render_template('error.html', code=404, message='Yazi bulunamadi'), 404
    return render_template('blog_post.html', post=post)


# ==================== LOGO REMOVAL APIs (DOKUNULMADI) ====================
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'pdf_file' not in request.files or 'logo_file' not in request.files:
        return jsonify({'error': 'PDF ve logo dosyalari gerekli!'}), 400

    pdf_file = request.files['pdf_file']
    logo_file = request.files['logo_file']
    custom_filename = request.form.get('custom_filename', '').strip()

    if pdf_file.filename == '' or logo_file.filename == '':
        return jsonify({'error': 'Dosya secilmedi!'}), 400

    if not allowed_file(pdf_file.filename, 'pdf'):
        return jsonify({'error': 'Gecersiz PDF dosyasi!'}), 400

    if not allowed_file(logo_file.filename, 'logo'):
        return jsonify({'error': 'Gecersiz logo dosyasi!'}), 400

    job_id = str(uuid.uuid4())[:8]

    if custom_filename:
        if not custom_filename.endswith('.pdf'):
            custom_filename += '.pdf'
        output_filename = f"{job_id}_{secure_filename(custom_filename)}"
    else:
        output_filename = f"{job_id}_temiz.pdf"

    pdf_filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    logo_filename = secure_filename(f"{job_id}_{logo_file.filename}")

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    pdf_file.save(pdf_path)
    logo_file.save(logo_path)

    progress_data[job_id] = {
        'pdf_path': pdf_path,
        'logo_path': logo_path,
        'output_path': output_path,
        'output_filename': output_filename,
        'custom_name': custom_filename or 'temiz.pdf',
        'status': 'pending',
        'progress': 0,
        'logs': [],
        'total_pages': 0,
        'current_page': 0,
        'created_at': time.time()
    }

    return jsonify({
        'success': True,
        'job_id': job_id,
        'message': 'Dosyalar yüklendi, işlem başlatılıyor...'
    })

@app.route('/process/<job_id>')
def process_pdf(job_id):
    def generate():
        if job_id not in progress_data:
            yield f"data: {json.dumps({'error': 'Is bulunamadi'})}\n\n"
            return

        job = progress_data[job_id]
        pdf_path = job['pdf_path']
        logo_path = job['logo_path']
        output_path = job['output_path']

        poppler_yolu = config.POPPLER_PATH

        try:
            yield f"data: {json.dumps({'log': 'PDF dosyasi yukleniyor...', 'progress': 5})}\n\n"
            time.sleep(0.3)

            pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_yolu)
            total_pages = len(pages)
            job['total_pages'] = total_pages

            yield f"data: {json.dumps({'log': f'{total_pages} sayfa bulundu', 'progress': 10})}\n\n"

            yield f"data: {json.dumps({'log': 'Logo dosyasi analiz ediliyor...', 'progress': 15})}\n\n"
            time.sleep(0.2)

            logo_img = cv2.imread(logo_path, 0)
            if logo_img is None:
                yield f"data: {json.dumps({'error': 'Logo dosyasi okunamadi!'})}\n\n"
                return

            yield f"data: {json.dumps({'log': 'SIFT algoritması başlatılıyor...', 'progress': 20})}\n\n"
            sift = cv2.SIFT_create()
            kp1, des1 = sift.detectAndCompute(logo_img, None)

            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            cleaned_pages_bytes = []

            for i, page in enumerate(pages):
                page_num = i + 1
                base_progress = 20 + int((i / total_pages) * 70)

                yield f"data: {json.dumps({'log': f'Sayfa {page_num}/{total_pages} isleniyor...', 'progress': base_progress, 'current_page': page_num})}\n\n"

                img_bgr = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
                img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

                kp2, des2 = sift.detectAndCompute(img_blur, None)
                result_img = img_bgr.copy()

                if des2 is None or len(kp2) < 5:
                    yield f"data: {json.dumps({'log': f'   Sayfa {page_num}: Ozellik bulunamadi, atlandi'})}\n\n"
                    cleaned_pages_bytes.append(cv2.imencode('.jpg', result_img)[1].tobytes())
                    continue

                try:
                    matches = flann.knnMatch(des1, des2, k=2)
                    good_matches = []
                    for m, n in matches:
                        if m.distance < 0.75 * n.distance:
                            good_matches.append(m)

                    MIN_MATCH_COUNT = 7

                    if len(good_matches) >= MIN_MATCH_COUNT:
                        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                        if M is not None:
                            h, w = logo_img.shape
                            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                            dst = cv2.perspectiveTransform(pts, M)

                            mask_img = np.zeros(img_gray.shape, dtype=np.uint8)
                            cv2.fillPoly(mask_img, [np.int32(dst)], 255)

                            kernel = np.ones((7, 7), np.uint8)
                            mask_dilated = cv2.dilate(mask_img, kernel, iterations=1)

                            result_img = cv2.inpaint(result_img, mask_dilated, 5, cv2.INPAINT_TELEA)

                            rect = cv2.boundingRect(np.int32(dst))
                            x, y, w_box, h_box = rect

                            pad = 5
                            x1 = max(x - pad, 0)
                            y1 = max(y - pad, 0)
                            x2 = min(x + w_box + pad, result_img.shape[1])
                            y2 = min(y + h_box + pad, result_img.shape[0])

                            roi = result_img[y1:y2, x1:x2]
                            if roi.size > 0:
                                roi_blur = cv2.GaussianBlur(roi, (9, 9), 0)
                                result_img[y1:y2, x1:x2] = roi_blur

                            yield f"data: {json.dumps({'log': f'   Sayfa {page_num}: Logo temizlendi ({len(good_matches)} eslesme)'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'log': f'   Sayfa {page_num}: Homografi hesaplanamadi'})}\n\n"
                    else:
                        yield f"data: {json.dumps({'log': f'   Sayfa {page_num}: Eslesme yetersiz ({len(good_matches)})'})}\n\n"

                except Exception as e:
                    yield f"data: {json.dumps({'log': f'   Sayfa {page_num}: Hata - {str(e)}'})}\n\n"

                cleaned_pages_bytes.append(cv2.imencode('.jpg', result_img)[1].tobytes())

            yield f"data: {json.dumps({'log': 'Yeni PDF oluşturuluyor...', 'progress': 95})}\n\n"

            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(cleaned_pages_bytes))

            os.remove(pdf_path)
            os.remove(logo_path)

            yield f"data: {json.dumps({'log': 'İşlem tamamlandı!', 'progress': 100, 'complete': True, 'download_id': job['output_filename'], 'download_name': job['custom_name']})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': f'İşlem hatası: {str(e)}'})}\n\n"
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(logo_path):
                os.remove(logo_path)

    return Response(generate(), mimetype='text/event-stream')

# ==================== MANUAL SELECTION ====================
@app.route('/api/manual-upload', methods=['POST'])
def api_manual_upload():
    """Upload PDF for manual selection mode - keeps file for processing"""
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"manual_{job_id}_{pdf_file.filename}")
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(pdf_path)

    return jsonify({
        'success': True,
        'pdf_path': pdf_path,
        'job_id': job_id
    })

# ==================== PDF MERGE API ====================
@app.route('/api/merge', methods=['POST'])
def api_merge():
    if 'pdf_files' not in request.files:
        return api_error('PDF dosyalari gerekli!')

    files = request.files.getlist('pdf_files')
    if len(files) < 2:
        return api_error('En az 2 PDF dosyasi gerekli!')

    custom_name = request.form.get('custom_name', '').strip()
    file_order = request.form.get('file_order', '')

    job_id = str(uuid.uuid4())[:8]
    pdf_paths = []
    file_map = {}

    for i, file in enumerate(files):
        if file and allowed_file(file.filename, 'pdf'):
            filename = secure_filename(f"{job_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            pdf_paths.append(filepath)
            file_map[i] = filepath

    if file_order:
        try:
            order = [int(x) for x in file_order.split(',')]
            pdf_paths = [file_map[i] for i in order if i in file_map]
        except (ValueError, KeyError):
            pass

    if custom_name:
        if not custom_name.endswith('.pdf'):
            custom_name += '.pdf'
        dl_name = custom_name
    else:
        dl_name = 'birlestirilmis.pdf'

    output_filename = f"{job_id}_{secure_filename(dl_name)}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = merge_pdfs(pdf_paths, output_path)

    for path in file_map.values():
        if os.path.exists(path):
            os.remove(path)

    if result['success']:
        return api_success(
            download_url=f'/download/{output_filename}?name={dl_name}',
            filename=dl_name
        )
    else:
        return jsonify(result), 400

# ==================== PDF SPLIT API ====================
@app.route('/api/split', methods=['POST'])
def api_split():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    mode = request.form.get('mode', 'all')
    ranges = request.form.get('ranges', '')

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_folder = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
    os.makedirs(output_folder, exist_ok=True)

    try:
        if mode == 'range' and ranges:
            page_ranges = []
            for r in ranges.split(','):
                r = r.strip()
                if '-' in r:
                    start, end = map(int, r.split('-'))
                    page_ranges.append((start, end))
            result = split_pdf_by_pages(input_path, output_folder, page_ranges)
        else:
            result = split_pdf_by_pages(input_path, output_folder, None)

        if result['success']:
            files = [{'name': f, 'url': f'/download/{job_id}/{f}'} for f in result['files']]
            zip_url = None
            if len(files) > 1:
                zip_filename = f"{job_id}_split.zip"
                zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
                with zipfile.ZipFile(zip_path, 'w') as zf:
                    for f_info in result['files']:
                        fpath = os.path.join(output_folder, f_info)
                        if os.path.exists(fpath):
                            zf.write(fpath, f_info)
                zip_url = f'/download/{zip_filename}?name=bolunmus.zip'

            return api_success(
                files=files,
                total_pages=result.get('total_pages', len(files)),
                zip_url=zip_url
            )
        else:
            return jsonify(result), 400
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

@app.route('/download/<job_id>/<filename>')
def download_split_file(job_id, filename):
    sub_folder = safe_path(app.config['OUTPUT_FOLDER'], job_id)
    if not sub_folder:
        return api_error('Gecersiz dosya yolu!', 403)
    file_path = safe_path(sub_folder, filename)
    if not file_path:
        return api_error('Gecersiz dosya yolu!', 403)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return api_error('Dosya bulunamadi!', 404)

# ==================== PDF ENCRYPT API ====================
@app.route('/api/encrypt', methods=['POST'])
@rate_limit('encrypt')
def api_encrypt():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    password = request.form.get('password', '')
    allow_print = request.form.get('allow_print', 'true') == 'true'
    allow_copy = request.form.get('allow_copy', 'false') == 'true'
    allow_modify = request.form.get('allow_modify', 'false') == 'true'

    if not password:
        return api_error('Sifre gerekli!')

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_sifreli.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    permissions = {'print': allow_print, 'extract': allow_copy, 'modify': allow_modify}
    result = encrypt_pdf(input_path, output_path, password, permissions=permissions)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(
            download_url=f'/download/{output_filename}?name=sifreli.pdf',
            filename='sifreli.pdf'
        )
    else:
        return api_error(result.get('error', 'Şifreleme hatası'))

@app.route('/api/decrypt', methods=['POST'])
@rate_limit('encrypt')
def api_decrypt():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    password = request.form.get('password', '')

    if not password:
        return api_error('Sifre gerekli!')

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_sifresiz.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = decrypt_pdf(input_path, output_path, password)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(
            download_url=f'/download/{output_filename}?name=sifresiz.pdf',
            filename='sifresiz.pdf'
        )
    else:
        return api_error(result.get('error', 'Şifre çözme hatası'))

# ==================== IMAGE TO PDF API ====================
@app.route('/api/img-to-pdf', methods=['POST'])
def api_img_to_pdf():
    if 'image_files' not in request.files:
        return jsonify({'success': False, 'error': 'Gorsel dosyalari gerekli!'}), 400

    files = request.files.getlist('image_files')
    if len(files) == 0:
        return jsonify({'success': False, 'error': 'En az 1 gorsel dosyasi gerekli!'}), 400

    job_id = str(uuid.uuid4())[:8]
    image_paths = []

    for file in files:
        if file:
            filename = secure_filename(f"{job_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_paths.append(filepath)

    output_filename = f"{job_id}_gorsellerden.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = images_to_pdf(image_paths, output_path)

    for path in image_paths:
        if os.path.exists(path):
            os.remove(path)

    if result['success']:
        return jsonify({
            'success': True,
            'download_url': f'/download/{output_filename}?name=gorsellerden.pdf',
            'filename': 'gorsellerden.pdf',
            'pages': result.get('pages', len(image_paths))
        })
    else:
        return jsonify(result), 400

# ==================== WATERMARK API ====================
@app.route('/api/watermark/text', methods=['POST'])
@rate_limit('watermark')
def api_watermark_text():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    text = request.form.get('text', '')
    position = request.form.get('position', 'center')
    opacity = float(request.form.get('opacity', 0.3))
    font_size = int(request.form.get('font_size', 50))
    rotation = int(request.form.get('rotation', 0))
    color = request.form.get('color', '#808080')

    if not text:
        return api_error('Filigran metni gerekli!')

    try:
        hex_color = color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    except (ValueError, IndexError):
        rgb = (0.5, 0.5, 0.5)

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_watermarked.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = add_text_watermark(
        input_path, output_path, text,
        position=position, opacity=opacity,
        font_size=font_size, color=rgb, rotation=rotation
    )

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(download_url=f'/download/{output_filename}?name=filigranli.pdf')
    else:
        return jsonify(result), 400

@app.route('/api/watermark/image', methods=['POST'])
@rate_limit('watermark')
def api_watermark_image():
    if 'pdf_file' not in request.files or 'image_file' not in request.files:
        return api_error('PDF ve gorsel dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    image_file = request.files['image_file']
    position = request.form.get('position', 'center')
    opacity = float(request.form.get('opacity', 0.5))

    job_id = str(uuid.uuid4())[:8]
    pdf_filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    img_filename = secure_filename(f"{job_id}_{image_file.filename}")

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

    pdf_file.save(input_path)
    image_file.save(image_path)

    output_filename = f"{job_id}_watermarked.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = add_image_watermark(input_path, output_path, image_path, position=position, opacity=opacity)

    if os.path.exists(input_path):
        os.remove(input_path)
    if os.path.exists(image_path):
        os.remove(image_path)

    if result['success']:
        return api_success(download_url=f'/download/{output_filename}?name=filigranli.pdf')
    else:
        return jsonify(result), 400

# ==================== PDF COMPRESS API ====================
@app.route('/api/compress', methods=['POST'])
def api_compress():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']
    quality = request.form.get('quality', 'medium')

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_compressed.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = compress_pdf(input_path, output_path, quality)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(
            original_size=format_size(result['original_size']),
            compressed_size=format_size(result['compressed_size']),
            reduction=result['reduction_percent'],
            images_compressed=result.get('images_compressed', 0),
            download_url=f'/download/{output_filename}?name=compressed.pdf'
        )
    else:
        return jsonify(result), 400

# ==================== PDF ROTATE API ====================
@app.route('/api/rotate', methods=['POST'])
def api_rotate():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    rotation = int(request.form.get('rotation', 90))
    pages_str = request.form.get('pages', 'all')

    if pages_str == 'all':
        pages = 'all'
    else:
        try:
            pages = [int(p.strip()) for p in pages_str.split(',')]
        except ValueError:
            pages = 'all'

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_rotated.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = rotate_pdf(input_path, output_path, rotation, pages=pages)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(
            message=result['message'],
            download_url=f'/download/{output_filename}?name=dondurulmus.pdf'
        )
    else:
        return jsonify(result), 400

@app.route('/api/rotate-thumbnails', methods=['POST'])
def api_rotate_thumbnails():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    from tools.pdf_reorder import get_pdf_thumbnails
    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"rotate_{job_id}_{pdf_file.filename}")
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(temp_path)

    result = get_pdf_thumbnails(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return jsonify(result)

# ==================== EXTRACT TEXT API ====================
@app.route('/api/extract-text', methods=['POST'])
def api_extract_text():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    result = extract_text(input_path)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return jsonify({
            'success': True,
            'text': result['text'],
            'page_count': result['page_count'],
            'char_count': result['char_count']
        })
    else:
        return jsonify(result), 400

# ==================== EXTRACT IMAGES API ====================
@app.route('/api/extract-images', methods=['POST'])
@rate_limit('extract_images')
def api_extract_images():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_folder = os.path.join(app.config['OUTPUT_FOLDER'], f"images_{job_id}")

    result = extract_images(input_path, output_folder)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        zip_filename = f"{job_id}_images.zip"
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)

        if result['count'] > 0:
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for img in result['images']:
                    img_path = os.path.join(output_folder, img['filename'])
                    if os.path.exists(img_path):
                        zipf.write(img_path, img['filename'])

        images_with_urls = [{
            'filename': img['filename'],
            'page': img['page'],
            'url': f'/download-image/{job_id}/{img["filename"]}'
        } for img in result['images']]

        return jsonify({
            'success': True,
            'images': images_with_urls,
            'count': result['count'],
            'zip_url': f'/download/{zip_filename}?name=images.zip'
        })
    else:
        return jsonify(result), 400

@app.route('/download-image/<job_id>/<filename>')
def download_image(job_id, filename):
    img_folder = safe_path(app.config['OUTPUT_FOLDER'], f"images_{job_id}")
    if not img_folder:
        return api_error('Gecersiz dosya yolu!', 403)
    file_path = safe_path(img_folder, filename)
    if not file_path:
        return api_error('Gecersiz dosya yolu!', 403)
    if os.path.exists(file_path):
        return send_file(file_path)
    return api_error('Dosya bulunamadi!', 404)

# ==================== PAGE REORDER API ====================
@app.route('/api/pdf-thumbnails', methods=['POST'])
def api_pdf_thumbnails():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"thumb_{job_id}_{pdf_file.filename}")
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(temp_path)

    result = get_pdf_thumbnails(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return jsonify(result)

@app.route('/api/reorder-upload', methods=['POST'])
def api_reorder_upload():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"reorder_{job_id}_{pdf_file.filename}")
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(pdf_path)

    progress_data[f"reorder_{job_id}"] = {
        'pdf_path': pdf_path,
        'created_at': time.time()
    }

    return api_success(job_id=job_id)

@app.route('/api/reorder-pages', methods=['POST'])
@rate_limit('reorder')
def api_reorder_pages():
    data = request.get_json()

    if not data or 'job_id' not in data or 'new_order' not in data:
        return api_error('job_id ve new_order gerekli!')

    reorder_key = f"reorder_{data['job_id']}"
    if reorder_key not in progress_data:
        return api_error('Oturum bulunamadi! Lutfen PDF\'i tekrar yukleyin.')

    pdf_path = progress_data[reorder_key]['pdf_path']
    new_order = data['new_order']

    if not os.path.exists(pdf_path):
        return api_error('PDF dosyasi bulunamadi!')

    job_id = str(uuid.uuid4())[:8]
    output_filename = f"{job_id}_reordered.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = reorder_pdf_pages(pdf_path, output_path, new_order)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    del progress_data[reorder_key]

    if result['success']:
        result['download_url'] = f'/download/{output_filename}?name=sirali.pdf'

    return jsonify(result)

# ==================== PDF REPAIR API ====================
@app.route('/api/pdf-analyze', methods=['POST'])
def api_pdf_analyze():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"analyze_{job_id}_{pdf_file.filename}")
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(temp_path)

    result = analyze_pdf(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return jsonify(result)

@app.route('/api/pdf-repair', methods=['POST'])
@rate_limit('repair')
def api_pdf_repair():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'error': 'PDF dosyasi gerekli!'}), 400

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"repair_{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_repaired.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = repair_pdf(input_path, output_path)

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        result['download_url'] = f'/download/{output_filename}?name=onarilmis.pdf'

    return jsonify(result)

# ==================== DOWNLOAD ====================
@app.route('/download/<filename>')
def download_file(filename):
    file_path = safe_path(app.config['OUTPUT_FOLDER'], filename)
    if not file_path:
        return api_error('Gecersiz dosya yolu!', 403)

    custom_name = request.args.get('name', 'dosya.pdf')

    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name=custom_name
        )
    return api_error('Dosya bulunamadi!', 404)

# ==================== PDF TO IMAGE API ====================
@app.route('/api/pdf-to-image', methods=['POST'])
@rate_limit('pdf_to_image')
def api_pdf_to_image():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    format_type = request.form.get('format', 'png').lower()
    dpi = int(request.form.get('dpi', 200))

    if format_type not in ['png', 'jpg', 'jpeg', 'webp']:
        format_type = 'png'

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    try:
        result = pdf_to_images_zip(input_path, format=format_type, dpi=dpi)

        if result['success']:
            zip_filename = f"{job_id}_images.zip"
            zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)

            with open(zip_path, 'wb') as f:
                f.write(result['data'])

            return api_success(
                page_count=result['page_count'],
                format=format_type.upper(),
                download_url=f'/download/{zip_filename}?name=pdf_images.zip'
            )
        else:
            return api_error(result.get('error', 'Dönüştürme hatası'))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

# ==================== HTML TO PDF API ====================
@app.route('/api/html-to-pdf', methods=['POST'])
def api_html_to_pdf():
    from tools.html_to_pdf import html_to_pdf_from_string, html_to_pdf_from_url

    source_type = request.form.get('source_type', 'html')
    custom_name = request.form.get('custom_name', 'dönüştürülmüş').strip() or 'dönüştürülmüş'
    page_size = request.form.get('page_size', 'A4')
    margin = request.form.get('margin', '10')
    orientation = request.form.get('orientation', 'portrait')

    job_id = str(uuid.uuid4())[:8]

    if not custom_name.endswith('.pdf'):
        custom_name += '.pdf'

    output_filename = f"{job_id}_{secure_filename(custom_name)}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    options = {
        'page_size': page_size,
        'margin': margin,
        'orientation': orientation
    }

    try:
        if source_type == 'url':
            url = request.form.get('url', '')
            if not url:
                return api_error('URL gerekli!')
            if not url.startswith('http'):
                url = 'https://' + url
            result = html_to_pdf_from_url(url, output_path, options)
        else:
            html_content = request.form.get('html_content', '')
            if not html_content:
                return api_error('HTML icerigi gerekli!')
            result = html_to_pdf_from_string(html_content, output_path, options)

        if result['success']:
            return api_success(
                file_size=format_size(result['file_size']),
                download_url=f'/download/{output_filename}?name={custom_name}'
            )
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"HTML to PDF error: {e}", exc_info=True)
        return api_error('HTML dönüştürme hatası')

# ==================== PDF METADATA API ====================
@app.route('/api/metadata', methods=['POST'])
def api_metadata_get():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"meta_{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    result = get_metadata(input_path)

    if result['success']:
        progress_data[f"meta_{job_id}"] = {
            'pdf_path': input_path,
            'created_at': time.time()
        }
        result['job_id'] = job_id
    else:
        if os.path.exists(input_path):
            os.remove(input_path)

    return jsonify(result)

@app.route('/api/metadata/update', methods=['POST'])
@rate_limit('metadata')
def api_metadata_update():
    data = request.get_json()
    if not data or 'job_id' not in data or 'metadata' not in data:
        return api_error('job_id ve metadata gerekli!')

    meta_key = f"meta_{data['job_id']}"
    if meta_key not in progress_data:
        return api_error('Oturum bulunamadi!')

    input_path = progress_data[meta_key]['pdf_path']
    if not os.path.exists(input_path):
        return api_error('PDF dosyasi bulunamadi!')

    job_id = str(uuid.uuid4())[:8]
    output_filename = f"{job_id}_metadata.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = update_metadata(input_path, output_path, data['metadata'])

    if os.path.exists(input_path):
        os.remove(input_path)
    del progress_data[meta_key]

    if result['success']:
        result['download_url'] = f'/download/{output_filename}?name=metadata_duzenlenmis.pdf'

    return jsonify(result)

@app.route('/api/metadata/clear', methods=['POST'])
@rate_limit('metadata')
def api_metadata_clear():
    data = request.get_json()
    if not data or 'job_id' not in data:
        return api_error('job_id gerekli!')

    meta_key = f"meta_{data['job_id']}"
    if meta_key not in progress_data:
        return api_error('Oturum bulunamadi!')

    input_path = progress_data[meta_key]['pdf_path']
    if not os.path.exists(input_path):
        return api_error('PDF dosyasi bulunamadi!')

    job_id = str(uuid.uuid4())[:8]
    output_filename = f"{job_id}_cleared.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = clear_metadata(input_path, output_path)

    if os.path.exists(input_path):
        os.remove(input_path)
    del progress_data[meta_key]

    if result['success']:
        result['download_url'] = f'/download/{output_filename}?name=metadata_temiz.pdf'

    return jsonify(result)

# ==================== NUMBERING API ====================
@app.route('/api/numbering', methods=['POST'])
@rate_limit('numbering')
def api_numbering():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    position = request.form.get('position', 'bottom-center')
    format_str = request.form.get('format', '{n}')
    start_page = int(request.form.get('start_page', 1))
    skip_first = request.form.get('skip_first', 'false') == 'true'
    font_size = int(request.form.get('font_size', 12))

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_numarali.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = add_page_numbers(
        input_path, output_path,
        position=position, format_str=format_str,
        start_number=start_page, skip_first=skip_first,
        font_size=font_size
    )

    if os.path.exists(input_path):
        os.remove(input_path)

    if result['success']:
        return api_success(
            download_url=f'/download/{output_filename}?name=numarali.pdf',
            page_count=result.get('page_count', 0)
        )
    else:
        return jsonify(result), 400

# ==================== PDF CROP API ====================
@app.route('/api/crop', methods=['POST'])
def api_crop():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    mode = request.form.get('mode', 'manual')

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_cropped.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        if mode == 'auto':
            result = auto_crop_pdf(input_path, output_path)
        else:
            margins = {
                'top': float(request.form.get('top', 0)),
                'bottom': float(request.form.get('bottom', 0)),
                'left': float(request.form.get('left', 0)),
                'right': float(request.form.get('right', 0)),
            }
            result = crop_pdf(input_path, output_path, margins)

        if result['success']:
            return api_success(
                download_url=f'/download/{output_filename}?name=kirpilmis.pdf',
                filename='kirpilmis.pdf',
                page_count=result.get('page_count', 0)
            )
        else:
            return api_error(result.get('error', 'Kırpma hatası'))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

# ==================== PDF COMPARE API ====================
@app.route('/api/compare', methods=['POST'])
@rate_limit('compare')
def api_compare():
    if 'pdf_file_1' not in request.files or 'pdf_file_2' not in request.files:
        return api_error('Iki PDF dosyasi gerekli!')

    pdf_file_1 = request.files['pdf_file_1']
    pdf_file_2 = request.files['pdf_file_2']

    job_id = str(uuid.uuid4())[:8]
    filename1 = secure_filename(f"{job_id}_1_{pdf_file_1.filename}")
    filename2 = secure_filename(f"{job_id}_2_{pdf_file_2.filename}")
    path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    pdf_file_1.save(path1)
    pdf_file_2.save(path2)

    try:
        result = compare_pdfs(path1, path2)
        return jsonify(result)
    finally:
        if os.path.exists(path1):
            os.remove(path1)
        if os.path.exists(path2):
            os.remove(path2)

# ==================== PDF TO EXCEL API ====================
@app.route('/api/pdf-to-excel', methods=['POST'])
@rate_limit('pdf_to_excel')
def api_pdf_to_excel():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    base_name = os.path.splitext(pdf_file.filename)[0]
    output_filename = f"{job_id}_{secure_filename(base_name)}.xlsx"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        result = pdf_to_excel(input_path, output_path)

        if result['success']:
            dl_name = f"{base_name}.xlsx"
            return api_success(
                download_url=f'/download/{output_filename}?name={dl_name}',
                filename=dl_name,
                tables_found=result.get('tables_found', 0),
                total_rows=result.get('total_rows', 0)
            )
        else:
            return api_error(result.get('error', 'Dönüştürme hatası'))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

# ==================== PDF FORM FILL API ====================
@app.route('/api/form-fields', methods=['POST'])
def api_form_fields():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"form_{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    result = get_form_fields(input_path)

    if result['success']:
        progress_data[f"form_{job_id}"] = {
            'pdf_path': input_path,
            'created_at': time.time()
        }
        result['job_id'] = job_id
    else:
        if os.path.exists(input_path):
            os.remove(input_path)

    return jsonify(result)

@app.route('/api/form-fill', methods=['POST'])
@rate_limit('form_fill')
def api_form_fill():
    data = request.get_json()
    if not data or 'job_id' not in data or 'fields' not in data:
        return api_error('job_id ve fields gerekli!')

    form_key = f"form_{data['job_id']}"
    if form_key not in progress_data:
        return api_error('Oturum bulunamadi! Lutfen PDF\'i tekrar yukleyin.')

    input_path = progress_data[form_key]['pdf_path']
    if not os.path.exists(input_path):
        return api_error('PDF dosyasi bulunamadi!')

    job_id = str(uuid.uuid4())[:8]
    output_filename = f"{job_id}_filled.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    result = fill_form(input_path, output_path, data['fields'])

    if os.path.exists(input_path):
        os.remove(input_path)
    del progress_data[form_key]

    if result['success']:
        result['download_url'] = f'/download/{output_filename}?name=doldurulmus.pdf'

    return jsonify(result)

# ==================== PDF TO WORD API ====================
@app.route('/api/pdf-to-word', methods=['POST'])
@rate_limit('pdf_to_word')
def api_pdf_to_word():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    base_name = os.path.splitext(pdf_file.filename)[0]
    output_filename = f"{job_id}_{secure_filename(base_name)}.docx"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        result = pdf_to_word(input_path, output_path)

        if result['success']:
            dl_name = f"{base_name}.docx"
            return api_success(
                download_url=f'/download/{output_filename}?name={dl_name}',
                filename=dl_name,
                page_count=result.get('page_count', 0)
            )
        else:
            return api_error(result.get('error', 'Dönüştürme hatası'))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

# ==================== PDF/A CONVERSION API ====================
@app.route('/api/pdf-to-pdfa', methods=['POST'])
@rate_limit('pdf_to_pdfa')
def api_pdf_to_pdfa():
    if 'pdf_file' not in request.files:
        return api_error('PDF dosyasi gerekli!')

    pdf_file = request.files['pdf_file']
    version = request.form.get('version', '2b')

    if version not in ('1b', '2b', '3b'):
        version = '2b'

    job_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{job_id}_{pdf_file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    output_filename = f"{job_id}_pdfa.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        result = convert_to_pdfa(input_path, output_path, version=version)

        if result['success']:
            return api_success(
                download_url=f'/download/{output_filename}?name=pdfa.pdf',
                filename='pdfa.pdf',
                version=result.get('version', ''),
                page_count=result.get('page_count', 0)
            )
        else:
            return api_error(result.get('error', 'Dönüştürme hatası'))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

# ==================== HATA SAYFALARI ====================
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return api_error('Sayfa bulunamadi', 404)
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    _ = get_translator(lang)
    return render_template('error.html', code=404, message=_('error_404')), 404

@app.errorhandler(413)
def too_large(e):
    if request.path.startswith('/api/'):
        return api_error(f'Dosya cok buyuk! Maksimum: {format_size(config.MAX_CONTENT_LENGTH)}', 413)
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    _ = get_translator(lang)
    msg = _('error_413') + f' (Max: {format_size(config.MAX_CONTENT_LENGTH)})'
    return render_template('error.html', code=413, message=msg), 413

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 hatası: {e}")
    if request.path.startswith('/api/'):
        return api_error('Sunucu hatası', 500)
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    _ = get_translator(lang)
    return render_template('error.html', code=500, message=_('error_500')), 500


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host='0.0.0.0', port=port)
