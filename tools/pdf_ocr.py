"""
PDF OCR - Taranmis PDF'lerden metin cikarma (Tesseract OCR)
"""
import os
import logging
import fitz  # PyMuPDF
from PIL import Image
import io

logger = logging.getLogger(__name__)


def ocr_pdf(input_path, output_path, language='tur+eng'):
    """
    PDF sayfalarini OCR ile tarayip metin cikar.

    Args:
        input_path: Giris PDF yolu
        output_path: Cikti TXT dosya yolu
        language: Tesseract dil kodu ('tur', 'eng', 'tur+eng')

    Returns:
        dict: {success, text, page_count, char_count, word_count}
    """
    try:
        import pytesseract
    except ImportError:
        return {'success': False, 'error': 'pytesseract yuklu degil'}

    # Tesseract yolu (config.py'den)
    try:
        import config
        if hasattr(config, 'TESSERACT_PATH') and config.TESSERACT_PATH:
            pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
    except Exception:
        pass

    try:
        doc = fitz.open(input_path)
        page_count = len(doc)

        if page_count == 0:
            doc.close()
            return {'success': False, 'error': 'PDF bos'}

        # Max sayfa limiti
        MAX_PAGES = 100
        if page_count > MAX_PAGES:
            doc.close()
            return {'success': False, 'error': f'Maksimum {MAX_PAGES} sayfa desteklenir'}

        all_text = []
        full_text_parts = []

        for i in range(page_count):
            page = doc[i]
            # Sayfayi goruntuye cevir (300 DPI)
            zoom = 300 / 72  # 72 DPI -> 300 DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Pixmap'i PIL Image'e cevir
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))

            # OCR uygula
            try:
                page_text = pytesseract.image_to_string(img, lang=language)
            except Exception as e:
                logger.warning(f"OCR sayfa {i+1} hatasi: {e}")
                page_text = ''

            page_text = page_text.strip()
            all_text.append(page_text)
            full_text_parts.append(f'--- Sayfa {i+1} ---\n{page_text}')

        doc.close()

        full_text = '\n\n'.join(full_text_parts)

        # TXT dosyasina yaz
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        # Istatistikler
        char_count = len(full_text)
        word_count = len(full_text.split()) if full_text.strip() else 0

        return {
            'success': True,
            'text': full_text,
            'page_count': page_count,
            'char_count': char_count,
            'word_count': word_count
        }

    except Exception as e:
        logger.error(f"OCR hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'OCR islemi basarisiz'}
