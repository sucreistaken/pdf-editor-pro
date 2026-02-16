"""
PDF Rotate Tool - Rotate PDF pages
"""
from PyPDF2 import PdfReader, PdfWriter
import logging

logger = logging.getLogger(__name__)


def rotate_pdf(input_path, output_path, rotation, pages='all'):
    """
    Rotate PDF pages
    
    Args:
        input_path (str): Path to input PDF
        output_path (str): Path for rotated PDF
        rotation (int): Rotation angle (90, 180, 270)
        pages (str or list): 'all' or list of page numbers
    
    Returns:
        dict: Result with success status
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        
        for i, page in enumerate(reader.pages):
            page_num = i + 1
            
            if pages == 'all' or page_num in pages:
                page.rotate(rotation)
            
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        rotated_count = total_pages if pages == 'all' else len(pages)
        
        return {
            'success': True,
            'message': f'{rotated_count} sayfa {rotation}° döndürüldü',
            'rotated_pages': rotated_count
        }
    
    except Exception as e:
        logger.error(f"rotate_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
