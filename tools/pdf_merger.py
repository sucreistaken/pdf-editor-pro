"""
PDF Merger Tool - Combines multiple PDF files into one
"""
from PyPDF2 import PdfMerger
import os
import logging

logger = logging.getLogger(__name__)


def merge_pdfs(pdf_paths, output_path):
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        pdf_paths (list): List of paths to PDF files to merge
        output_path (str): Path where merged PDF will be saved
    
    Returns:
        dict: Result with success status and message
    """
    try:
        merger = PdfMerger()
        
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                return {'success': False, 'error': f'File not found: {pdf_path}'}
            merger.append(pdf_path)
        
        merger.write(output_path)
        merger.close()
        
        return {'success': True, 'message': f'Successfully merged {len(pdf_paths)} PDFs'}
    
    except Exception as e:
        logger.error(f"merge_pdfs error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}
