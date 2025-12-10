"""
Image to PDF Tool - Convert images to PDF format
"""
import img2pdf
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)


def images_to_pdf(image_paths, output_path, page_size=None):
    """
    Convert one or more images to a PDF
    
    Args:
        image_paths (list): List of image file paths
        output_path (str): Path for output PDF
        page_size (tuple): Optional (width, height) in points
    
    Returns:
        dict: Result with success status
    """
    try:
        # Validate all images exist
        for img_path in image_paths:
            if not os.path.exists(img_path):
                return {'success': False, 'error': f'Image not found: {img_path}'}
        
        # Convert to PDF
        with open(output_path, "wb") as f:
            if page_size:
                # Custom page size
                layout = img2pdf.get_layout_fun(page_size)
                f.write(img2pdf.convert(image_paths, layout_fun=layout))
            else:
                # Auto size
                f.write(img2pdf.convert(image_paths))
        
        return {
            'success': True,
            'message': f'Converted {len(image_paths)} images to PDF',
            'pages': len(image_paths)
        }
    
    except Exception as e:
        logger.error(f"images_to_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}


def get_image_info(image_path):
    """
    Get image dimensions and format
    
    Args:
        image_path (str): Path to image file
    
    Returns:
        dict: Image information or error
    """
    try:
        with Image.open(image_path) as img:
            return {
                'success': True,
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode
            }
    except Exception as e:
        logger.error(f"get_image_info error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}
