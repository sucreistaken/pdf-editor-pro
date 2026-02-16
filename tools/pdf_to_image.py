"""
PDF to Image - PDF sayfalarini resme donustur
"""
from pdf2image import convert_from_path
import os
import zipfile
import io
import logging

logger = logging.getLogger(__name__)

try:
    from config import POPPLER_PATH
except ImportError:
    POPPLER_PATH = os.environ.get('POPPLER_PATH', r'C:\Program Files\poppler-25.12.0\Library\bin')

MAX_PAGES = 200


def pdf_to_images(pdf_path, output_folder, format='png', dpi=200):
    """
    PDF sayfalarini resme donusturur

    Returns:
        dict: Islem sonucu ve dosya listesi
    """
    try:
        pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH,
                                  last_page=MAX_PAGES)

        if not pages:
            return {'success': False, 'error': 'PDF sayfaları okunamadı'}

        os.makedirs(output_folder, exist_ok=True)

        image_files = []
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        for i, page in enumerate(pages):
            filename = f"{base_name}_sayfa_{i+1}.{format}"
            filepath = os.path.join(output_folder, filename)

            if format.lower() in ('jpg', 'jpeg'):
                page.save(filepath, 'JPEG', quality=95)
            elif format.lower() == 'webp':
                page.save(filepath, 'WEBP', quality=95)
            else:
                page.save(filepath, 'PNG')

            image_files.append(filename)
            page.close()

        return {
            'success': True,
            'total_pages': len(pages),
            'files': image_files,
            'format': format.upper()
        }

    except Exception as e:
        logger.error(f"pdf_to_images error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def pdf_to_images_zip(pdf_path, format='png', dpi=200):
    """
    PDF sayfalarini resme donusturup ZIP olarak dondurur

    Returns:
        dict: {'success': True, 'data': bytes, 'page_count': int} veya hata
    """
    try:
        pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH,
                                  last_page=MAX_PAGES)

        if not pages:
            return {'success': False, 'error': 'PDF sayfaları okunamadı'}

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for i, page in enumerate(pages):
                img_buffer = io.BytesIO()

                if format.lower() in ['jpg', 'jpeg']:
                    page.save(img_buffer, 'JPEG', quality=95)
                    ext = 'jpg'
                elif format.lower() == 'webp':
                    page.save(img_buffer, 'WEBP', quality=95)
                    ext = 'webp'
                else:
                    page.save(img_buffer, 'PNG')
                    ext = 'png'

                filename = f"{base_name}_sayfa_{i+1}.{ext}"
                zf.writestr(filename, img_buffer.getvalue())
                page.close()

        zip_buffer.seek(0)
        return {
            'success': True,
            'data': zip_buffer.getvalue(),
            'page_count': len(pages)
        }

    except Exception as e:
        logger.error(f"pdf_to_images_zip error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız', 'page_count': 0}
