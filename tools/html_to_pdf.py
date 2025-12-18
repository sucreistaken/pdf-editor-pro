"""
HTML to PDF - Playwright (headless Chromium) ile HTML'i PDF'e donustur
GTK/WeasyPrint bagimliligi yok.
"""
import os
import tempfile
import logging

logger = logging.getLogger(__name__)


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

        pdf_options = _build_pdf_options(options)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html_content, wait_until='networkidle')
            page.pdf(path=output_path, **pdf_options)
            browser.close()

        file_size = os.path.getsize(output_path)
        return {
            'success': True,
            'file_size': file_size,
            'message': 'HTML başarıyla PDF\'e dönüştürüldü'
        }

    except ImportError:
        return {
            'success': False,
            'error': 'Playwright yüklü değil. Lütfen "pip install playwright && playwright install chromium" komutunu çalıştırın.'
        }
    except Exception as e:
        logger.error(f"html_to_pdf_from_string error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}


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

        pdf_options = _build_pdf_options(options)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.pdf(path=output_path, **pdf_options)
            browser.close()

        file_size = os.path.getsize(output_path)
        return {
            'success': True,
            'file_size': file_size,
            'message': 'URL başarıyla PDF\'e dönüştürüldü'
        }

    except ImportError:
        return {
            'success': False,
            'error': 'Playwright yüklü değil. Lütfen "pip install playwright && playwright install chromium" komutunu çalıştırın.'
        }
    except Exception as e:
        logger.error(f"html_to_pdf_from_url error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}


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
