"""
PDF Image Extractor - Extract images from PDF
"""
import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)


def extract_images(input_path, output_folder):
    """
    Extract all images from PDF
    
    Args:
        input_path (str): Path to input PDF
        output_folder (str): Folder to save extracted images
    
    Returns:
        dict: Result with extracted image info
    """
    try:
        doc = fitz.open(input_path)
        os.makedirs(output_folder, exist_ok=True)
        
        extracted_images = []
        image_count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_count += 1
                    filename = f"image_{page_num + 1}_{img_index + 1}.{image_ext}"
                    filepath = os.path.join(output_folder, filename)
                    
                    with open(filepath, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    extracted_images.append({
                        'filename': filename,
                        'page': page_num + 1,
                        'size': len(image_bytes)
                    })
                except Exception:
                    continue
        
        doc.close()
        
        return {
            'success': True,
            'images': extracted_images,
            'count': len(extracted_images),
            'message': f'{len(extracted_images)} görsel çıkarıldı'
        }
    
    except Exception as e:
        logger.error(f"extract_images error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def get_image_count(input_path):
    """
    Get count of images in PDF without extracting
    """
    try:
        doc = fitz.open(input_path)
        count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            count += len(page.get_images(full=True))
        
        doc.close()
        return {'success': True, 'count': count}
    
    except Exception as e:
        logger.error(f"get_image_count error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
