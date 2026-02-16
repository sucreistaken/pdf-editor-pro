"""
PDF Text Extractor - Extract text from PDF
"""
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)


def extract_text(input_path, output_path=None):
    """
    Extract all text from PDF
    
    Args:
        input_path (str): Path to input PDF
        output_path (str): Optional path to save text file
    
    Returns:
        dict: Result with extracted text
    """
    try:
        doc = fitz.open(input_path)
        full_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text.strip():
                full_text.append(f"--- Sayfa {page_num + 1} ---\n{text}")
        
        doc.close()
        
        combined_text = "\n\n".join(full_text)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(combined_text)
        
        return {
            'success': True,
            'text': combined_text,
            'page_count': len(full_text),
            'char_count': len(combined_text)
        }
    
    except Exception as e:
        logger.error(f"extract_text error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def extract_text_by_page(input_path, page_number):
    """
    Extract text from a specific page
    
    Args:
        input_path (str): Path to input PDF
        page_number (int): Page number (1-indexed)
    
    Returns:
        dict: Result with page text
    """
    try:
        doc = fitz.open(input_path)
        
        if page_number < 1 or page_number > len(doc):
            return {'success': False, 'error': 'Geçersiz sayfa numarası'}
        
        page = doc[page_number - 1]
        text = page.get_text("text")
        doc.close()
        
        return {
            'success': True,
            'text': text,
            'page': page_number
        }
    
    except Exception as e:
        logger.error(f"extract_text_by_page error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
