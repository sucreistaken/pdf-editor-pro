"""
PDF to Word Tool - PDF'i Word belgesine donustur
"""
from pdf2docx import Converter
import logging

logger = logging.getLogger(__name__)


def pdf_to_word(input_path, output_path):
    """
    PDF dosyasini DOCX formatina donustur

    Args:
        input_path (str): Girdi PDF yolu
        output_path (str): Cikti DOCX yolu

    Returns:
        dict: Islem sonucu
    """
    cv = None
    try:
        cv = Converter(input_path)
        cv.convert(output_path)
        page_count = len(cv.pages) if hasattr(cv, 'pages') else 0

        return {
            'success': True,
            'message': f'PDF başarıyla Word\'e dönüştürüldü',
            'page_count': page_count
        }

    except Exception as e:
        logger.error(f"pdf_to_word error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if cv:
            try:
                cv.close()
            except Exception:
                pass
