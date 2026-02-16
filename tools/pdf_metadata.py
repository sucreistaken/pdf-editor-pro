"""
PDF Metadata Editor - PDF meta bilgilerini goruntule, duzenle, temizle
"""
import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)


def get_metadata(input_path):
    """
    PDF dosyasinin tum metadata bilgilerini getir
    """
    doc = None
    try:
        doc = fitz.open(input_path)
        metadata = doc.metadata

        return {
            'success': True,
            'metadata': {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'keywords': metadata.get('keywords', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creationDate': metadata.get('creationDate', ''),
                'modDate': metadata.get('modDate', ''),
            },
            'page_count': len(doc),
            'file_size': os.path.getsize(input_path)
        }

    except Exception as e:
        logger.error(f"get_metadata error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()


def update_metadata(input_path, output_path, new_metadata):
    """
    PDF metadata bilgilerini guncelle

    Args:
        new_metadata: dict - {'title': '...', 'author': '...', ...}
    """
    doc = None
    try:
        doc = fitz.open(input_path)

        current = doc.metadata
        for key in ['title', 'author', 'subject', 'keywords', 'creator', 'producer']:
            if key in new_metadata:
                current[key] = new_metadata[key]

        doc.set_metadata(current)
        doc.save(output_path, garbage=4, deflate=True)

        return {
            'success': True,
            'message': 'Metadata başarıyla güncellendi'
        }

    except Exception as e:
        logger.error(f"update_metadata error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()


def clear_metadata(input_path, output_path):
    """
    Tum PDF metadata bilgilerini temizle (gizlilik icin)
    """
    doc = None
    try:
        doc = fitz.open(input_path)

        doc.set_metadata({
            'title': '',
            'author': '',
            'subject': '',
            'keywords': '',
            'creator': '',
            'producer': '',
        })

        doc.save(output_path, garbage=4, deflate=True, clean=True)

        return {
            'success': True,
            'message': 'Tüm metadata bilgileri temizlendi'
        }

    except Exception as e:
        logger.error(f"clear_metadata error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()
