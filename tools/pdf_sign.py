"""
PDF Sign - PDF'e imza ekleme (PyMuPDF overlay)
"""
import os
import logging
import fitz  # PyMuPDF
import base64
import io

logger = logging.getLogger(__name__)


def add_signature(input_path, output_path, image_path=None, image_data=None,
                  page_num='all', x=100, y=100, width=200, height=80):
    """
    PDF'e imza gorseli ekle.

    Args:
        input_path: Giris PDF yolu
        output_path: Cikti PDF yolu
        image_path: Imza gorsel dosya yolu (image_data yoksa)
        image_data: Base64 encoded imza verisi (data:image/png;base64,...)
        page_num: Sayfa numarasi (0-indexed) veya 'all'
        x: Sol ust kose X koordinati (pt)
        y: Sol ust kose Y koordinati (pt)
        width: Imza genisligi (pt)
        height: Imza yuksekligi (pt)

    Returns:
        dict: {success, message, page_count}
    """
    try:
        # Imza gorselini oku
        if image_data:
            # Base64 data URL'den gorsel oku
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]
            img_bytes = base64.b64decode(image_data)
        elif image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
        else:
            return {'success': False, 'error': 'Imza gorseli gerekli'}

        doc = fitz.open(input_path)
        page_count = len(doc)

        if page_count == 0:
            doc.close()
            return {'success': False, 'error': 'PDF bos'}

        # Koordinatlari float'a cevir
        x = float(x)
        y = float(y)
        width = float(width)
        height = float(height)

        # Imzalanacak sayfalari belirle
        if page_num == 'all':
            pages_to_sign = list(range(page_count))
        else:
            page_idx = int(page_num)
            if page_idx < 0 or page_idx >= page_count:
                doc.close()
                return {'success': False, 'error': 'Gecersiz sayfa numarasi'}
            pages_to_sign = [page_idx]

        # Her sayfaya imza ekle
        for idx in pages_to_sign:
            page = doc[idx]
            rect = fitz.Rect(x, y, x + width, y + height)
            page.insert_image(rect, stream=img_bytes)

        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

        signed_count = len(pages_to_sign)
        return {
            'success': True,
            'message': f'{signed_count} sayfaya imza eklendi',
            'page_count': signed_count
        }

    except Exception as e:
        logger.error(f"Sign hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'Imza ekleme islemi basarisiz'}
