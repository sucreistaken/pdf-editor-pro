"""
PDF Page Reorder Tool
- Get page thumbnails
- Reorder pages based on new sequence
"""
import fitz  # PyMuPDF
import base64
import os
import logging

logger = logging.getLogger(__name__)


def get_pdf_thumbnails(pdf_path, max_width=150):
    """
    Generate thumbnails for all pages in a PDF
    
    Args:
        pdf_path: Path to PDF file
        max_width: Maximum width for thumbnails
    
    Returns:
        dict with list of base64 encoded thumbnails
    """
    try:
        doc = fitz.open(pdf_path)
        thumbnails = []
        
        for i, page in enumerate(doc):
            # Calculate zoom to fit max_width
            zoom = max_width / page.rect.width
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to base64
            img_bytes = pix.tobytes("png")
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            thumbnails.append({
                'page': i + 1,
                'image': f'data:image/png;base64,{img_base64}',
                'width': pix.width,
                'height': pix.height
            })
        
        result = {
            'success': True,
            'thumbnails': thumbnails,
            'total_pages': len(doc)
        }
        
        doc.close()
        return result
    
    except Exception as e:
        logger.error(f"get_pdf_thumbnails error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def reorder_pdf_pages(pdf_path, output_path, new_order):
    """
    Reorder PDF pages based on new sequence

    Args:
        pdf_path: Path to input PDF
        output_path: Path for output PDF
        new_order: List of page numbers in new order (1-indexed)

    Returns:
        dict with result
    """
    try:
        doc = fitz.open(pdf_path)

        # Convert to 0-indexed and validate
        select_order = [p - 1 for p in new_order if 0 <= p - 1 < len(doc)]

        # select() reorders pages in-place, preserving all resources
        doc.select(select_order)
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

        return {
            'success': True,
            'pages_reordered': len(select_order),
            'output_path': output_path
        }

    except Exception as e:
        logger.error(f"reorder_pdf_pages error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def delete_pdf_pages(pdf_path, output_path, pages_to_delete):
    """
    Delete specific pages from PDF
    
    Args:
        pdf_path: Path to input PDF
        output_path: Path for output PDF
        pages_to_delete: List of page numbers to delete (1-indexed)
    
    Returns:
        dict with result
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Get 0-indexed pages to keep
        pages_to_keep = [i for i in range(total_pages) if (i + 1) not in pages_to_delete]

        if len(pages_to_keep) == 0:
            doc.close()
            return {'success': False, 'error': 'En az bir sayfa kalmalı!'}

        # select() preserves all original resources
        doc.select(pages_to_keep)
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

        return {
            'success': True,
            'pages_deleted': len(pages_to_delete),
            'pages_remaining': len(pages_to_keep),
            'output_path': output_path
        }

    except Exception as e:
        logger.error(f"delete_pdf_pages error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
