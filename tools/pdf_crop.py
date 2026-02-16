"""
PDF Crop Tool - PDF sayfalarini kirp
"""
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)


def crop_pdf(input_path, output_path, margins):
    """
    PDF sayfalarini verilen kenar bosluklarina gore kirp

    Args:
        input_path (str): Girdi PDF yolu
        output_path (str): Cikti PDF yolu
        margins (dict): {'top': px, 'bottom': px, 'left': px, 'right': px}

    Returns:
        dict: Islem sonucu
    """
    doc = None
    try:
        doc = fitz.open(input_path)
        top = float(margins.get('top', 0))
        bottom = float(margins.get('bottom', 0))
        left = float(margins.get('left', 0))
        right = float(margins.get('right', 0))

        for page in doc:
            rect = page.rect
            new_rect = fitz.Rect(
                rect.x0 + left,
                rect.y0 + top,
                rect.x1 - right,
                rect.y1 - bottom
            )
            if new_rect.width <= 0 or new_rect.height <= 0:
                return {'success': False, 'error': 'Kenar boşluklar sayfa boyutundan büyük!'}
            page.set_cropbox(new_rect)

        doc.save(output_path, garbage=4, deflate=True)

        return {
            'success': True,
            'message': f'{len(doc)} sayfa kırpıldı',
            'page_count': len(doc)
        }

    except Exception as e:
        logger.error(f"crop_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()


def auto_crop_pdf(input_path, output_path):
    """
    PDF sayfalarindaki beyaz kenarlari otomatik kirp

    Returns:
        dict: Islem sonucu
    """
    doc = None
    try:
        doc = fitz.open(input_path)
        cropped_count = 0

        for page in doc:
            # Sayfayi render et ve icerik sinirlari bul
            blocks = page.get_text("dict")["blocks"]
            if not blocks:
                continue

            min_x, min_y = page.rect.width, page.rect.height
            max_x, max_y = 0, 0

            for block in blocks:
                bbox = block.get("bbox", (0, 0, 0, 0))
                min_x = min(min_x, bbox[0])
                min_y = min(min_y, bbox[1])
                max_x = max(max_x, bbox[2])
                max_y = max(max_y, bbox[3])

            # Gorsel bloklari da kontrol et
            images = page.get_images(full=True)
            for img in images:
                try:
                    rects = page.get_image_rects(img[0])
                    for r in rects:
                        min_x = min(min_x, r.x0)
                        min_y = min(min_y, r.y0)
                        max_x = max(max_x, r.x1)
                        max_y = max(max_y, r.y1)
                except Exception:
                    pass

            if max_x > min_x and max_y > min_y:
                # 10px padding birak
                padding = 10
                new_rect = fitz.Rect(
                    max(0, min_x - padding),
                    max(0, min_y - padding),
                    min(page.rect.width, max_x + padding),
                    min(page.rect.height, max_y + padding)
                )
                page.set_cropbox(new_rect)
                cropped_count += 1

        doc.save(output_path, garbage=4, deflate=True)

        return {
            'success': True,
            'message': f'{cropped_count} sayfa otomatik kırpıldı',
            'page_count': len(doc),
            'cropped_count': cropped_count
        }

    except Exception as e:
        logger.error(f"auto_crop_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()
