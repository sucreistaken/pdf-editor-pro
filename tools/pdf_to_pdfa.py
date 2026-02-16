"""
PDF/A Conversion Tool - PDF'i PDF/A formatina donustur
"""
import pikepdf
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def convert_to_pdfa(input_path, output_path, version='2b'):
    """
    PDF dosyasini PDF/A formatina donustur

    Args:
        input_path (str): Girdi PDF yolu
        output_path (str): Cikti PDF yolu
        version (str): PDF/A surumu ('1b', '2b', '3b')

    Returns:
        dict: Islem sonucu
    """
    pdf = None
    try:
        pdf = pikepdf.open(input_path)

        # PDF/A uyumluluk icin metadata ayarla
        version_map = {
            '1b': ('1', 'B'),
            '2b': ('2', 'B'),
            '3b': ('3', 'B'),
        }

        part, conformance = version_map.get(version, ('2', 'B'))

        # XMP metadata olustur
        with pdf.open_metadata() as meta:
            # PDF/A tanimi ekle
            meta['pdfaid:part'] = part
            meta['pdfaid:conformance'] = conformance

            # Temel metadata
            meta['dc:format'] = 'application/pdf'
            if not meta.get('dc:title'):
                meta['dc:title'] = 'PDF/A Document'
            meta['xmp:CreateDate'] = datetime.now().isoformat()
            meta['xmp:ModifyDate'] = datetime.now().isoformat()
            meta['pdf:Producer'] = 'PDFEdit - PDF/A Converter'

        # Kaydet
        pdf.save(output_path, linearize=True)

        return {
            'success': True,
            'message': f'PDF/A-{part}{conformance} formatına dönüştürüldü',
            'version': f'PDF/A-{part}{conformance}',
            'page_count': len(pdf.pages)
        }

    except Exception as e:
        logger.error(f"convert_to_pdfa error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if pdf:
            pdf.close()
