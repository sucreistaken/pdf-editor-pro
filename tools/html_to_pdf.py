"""
HTML to PDF - Playwright (headless Chromium) ile HTML'i PDF'e donustur
GTK/WeasyPrint bagimliligi yok.
"""
import os
import logging

logger = logging.getLogger(__name__)


def _wrap_html(html_content):
    """
    Eksik HTML yapisini tamamla: DOCTYPE, charset, varsayilan font ekle.
    Tam HTML belgesi gonderilmisse dokunma.
    """
    stripped = html_content.strip().lower()
    if stripped.startswith('<!doctype') or stripped.startswith('<html'):
        # Tam belge ama charset eksik olabilir - head icine ekle
        if '<meta charset' not in html_content.lower() and '<meta http-equiv' not in html_content.lower():
            # <head> varsa icine ekle
            if '<head>' in html_content.lower():
                idx = html_content.lower().index('<head>') + len('<head>')
                html_content = html_content[:idx] + '\n<meta charset="UTF-8">' + html_content[idx:]
            elif '<head ' in html_content.lower():
                # <head ...> formatinda
                idx = html_content.lower().index('<head ')
                close = html_content.index('>', idx) + 1
                html_content = html_content[:close] + '\n<meta charset="UTF-8">' + html_content[close:]
        return html_content

    # Parcali HTML - tam belgeye sar
    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    padding: 20px;
    max-width: 100%;
}}
img {{ max-width: 100%; height: auto; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f5f5f5; }}
</style>
</head>
<body>
{html_content}
</body>
</html>'''


def html_to_pdf_from_string(html_content, output_path, options=None):
    """
    HTML kodundan PDF olustur

    Args:
        html_content: HTML string
        output_path: Cikti PDF yolu
        options: {'page_size': 'A4', 'margin': '10', 'orientation': 'portrait'}
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            'success': False,
            'error': 'Playwright yüklü değil. Lütfen "pip install playwright && playwright install chromium" komutunu çalıştırın.'
        }

    pdf_options = _build_pdf_options(options)
    wrapped_html = _wrap_html(html_content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1280, 'height': 900})
            page.set_content(wrapped_html, wait_until='networkidle', timeout=30000)
            page.pdf(path=output_path, **pdf_options)
            browser.close()

        file_size = os.path.getsize(output_path)
        return {
            'success': True,
            'file_size': file_size,
            'message': 'HTML başarıyla PDF\'e dönüştürüldü'
        }
    except Exception as e:
        logger.error(f"html_to_pdf_from_string error: {e}", exc_info=True)
        return {'success': False, 'error': 'HTML dönüştürme başarısız oldu'}


def html_to_pdf_from_url(url, output_path, options=None):
    """
    URL'den PDF olustur

    Args:
        url: Web sayfasi URL'si
        output_path: Cikti PDF yolu
        options: {'page_size': 'A4', 'margin': '10', 'orientation': 'portrait'}
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            'success': False,
            'error': 'Playwright yüklü değil. Lütfen "pip install playwright && playwright install chromium" komutunu çalıştırın.'
        }

    # URL dogrulama
    if not (url.startswith('http://') or url.startswith('https://')):
        return {'success': False, 'error': 'Geçersiz URL formatı'}

    pdf_options = _build_pdf_options(options)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1280, 'height': 900})
            page.goto(url, wait_until='networkidle', timeout=30000)
            # Dinamik icerik icin ekstra bekleme
            page.wait_for_timeout(1500)
            page.pdf(path=output_path, **pdf_options)
            browser.close()

        file_size = os.path.getsize(output_path)
        return {
            'success': True,
            'file_size': file_size,
            'message': 'URL başarıyla PDF\'e dönüştürüldü'
        }
    except Exception as e:
        error_msg = str(e)
        if 'Timeout' in error_msg or 'timeout' in error_msg:
            logger.warning(f"html_to_pdf_from_url timeout: {url}")
            return {'success': False, 'error': 'Sayfa yüklenirken zaman aşımı (30 saniye). URL\'yi kontrol edin.'}
        if 'net::ERR_NAME_NOT_RESOLVED' in error_msg:
            return {'success': False, 'error': 'Alan adı bulunamadı. URL\'yi kontrol edin.'}
        if 'net::ERR_CONNECTION_REFUSED' in error_msg:
            return {'success': False, 'error': 'Bağlantı reddedildi. Site erişilebilir değil.'}
        logger.error(f"html_to_pdf_from_url error: {e}", exc_info=True)
        return {'success': False, 'error': 'URL dönüştürme başarısız oldu'}


def _build_pdf_options(options):
    """Playwright page.pdf() icin opsiyon dict'i olustur"""
    pdf_opts = {
        'print_background': True,
    }

    if not options:
        pdf_opts['format'] = 'A4'
        pdf_opts['margin'] = {'top': '10mm', 'right': '10mm', 'bottom': '10mm', 'left': '10mm'}
        return pdf_opts

    page_size = options.get('page_size', 'A4')
    margin = options.get('margin', '10')
    orientation = options.get('orientation', 'portrait')

    pdf_opts['format'] = page_size
    pdf_opts['landscape'] = (orientation == 'landscape')
    pdf_opts['margin'] = {
        'top': f'{margin}mm',
        'right': f'{margin}mm',
        'bottom': f'{margin}mm',
        'left': f'{margin}mm',
    }

    return pdf_opts
