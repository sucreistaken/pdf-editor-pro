"""
PDF Redact - Kalici karalama/sansur (PyMuPDF redaction API)
"""
import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def redact_areas(input_path, output_path, redactions):
    """
    Belirli alanlari kalici olarak karala.

    Args:
        input_path: Giris PDF yolu
        output_path: Cikti PDF yolu
        redactions: [{'page': 0, 'rect': [x0, y0, x1, y1]}, ...]

    Returns:
        dict: {success, message, redaction_count}
    """
    try:
        doc = fitz.open(input_path)
        redaction_count = 0

        for redaction in redactions:
            page_num = redaction.get('page', 0)
            rect_coords = redaction.get('rect', [])

            if page_num < 0 or page_num >= len(doc):
                continue
            if len(rect_coords) != 4:
                continue

            page = doc[page_num]
            rect = fitz.Rect(rect_coords)
            page.add_redact_annot(rect, fill=(0, 0, 0))
            redaction_count += 1

        # Tum redaction'lari uygula
        for page in doc:
            page.apply_redactions()

        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

        return {
            'success': True,
            'message': f'{redaction_count} alan karalandi',
            'redaction_count': redaction_count
        }

    except Exception as e:
        logger.error(f"Redact hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'Karalama islemi basarisiz'}


def redact_text(input_path, output_path, search_text):
    """
    Belirli metni tum sayfalarda ara ve karala.

    Args:
        input_path: Giris PDF yolu
        output_path: Cikti PDF yolu
        search_text: Karalanacak metin

    Returns:
        dict: {success, message, redaction_count}
    """
    try:
        if not search_text or not search_text.strip():
            return {'success': False, 'error': 'Aranacak metin gerekli'}

        doc = fitz.open(input_path)
        redaction_count = 0

        for page in doc:
            text_instances = page.search_for(search_text)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
                redaction_count += 1
            if text_instances:
                page.apply_redactions()

        if redaction_count == 0:
            doc.close()
            return {'success': False, 'error': 'Metin bulunamadi'}

        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

        return {
            'success': True,
            'message': f'{redaction_count} eslesme karalandi',
            'redaction_count': redaction_count
        }

    except Exception as e:
        logger.error(f"Redact text hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'Metin karalama islemi basarisiz'}
