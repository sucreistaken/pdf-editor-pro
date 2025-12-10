"""
PDF Splitter Tool - Split PDF by pages or ranges
"""
from PyPDF2 import PdfReader, PdfWriter
import os
import logging

logger = logging.getLogger(__name__)


def split_pdf_by_pages(input_path, output_folder, page_ranges=None):
    """
    Split PDF into separate files based on page ranges

    Args:
        input_path (str): Path to input PDF
        output_folder (str): Folder to save split PDFs
        page_ranges (list): List of tuples (start, end) or None for all pages separately

    Returns:
        dict: Result with success status and output files
    """
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []

        if page_ranges is None:
            # Split every page
            for page_num in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])

                output_filename = f"sayfa_{page_num + 1}.pdf"
                output_path = os.path.join(output_folder, output_filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                output_files.append(output_filename)
        else:
            # Split by ranges - girdi dogrulama
            for idx, (start, end) in enumerate(page_ranges):
                if start < 1:
                    return {'success': False, 'error': f'Başlangıç sayfası 1\'den küçük olamaz (girdi: {start})'}
                if end < start:
                    return {'success': False, 'error': f'Bitiş sayfası ({end}) başlangıçtan ({start}) küçük olamaz'}
                if start > total_pages:
                    return {'success': False, 'error': f'Başlangıç sayfası ({start}) toplam sayfa sayısından ({total_pages}) büyük'}

                writer = PdfWriter()
                actual_end = min(end, total_pages)

                for page_num in range(start - 1, actual_end):
                    writer.add_page(reader.pages[page_num])

                output_filename = f"sayfa_{start}-{actual_end}.pdf"
                output_path = os.path.join(output_folder, output_filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                output_files.append(output_filename)

        return {
            'success': True,
            'message': f'{len(output_files)} dosyaya bölündü',
            'files': output_files,
            'total_pages': total_pages
        }

    except Exception as e:
        logger.error(f"split_pdf_by_pages error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}


def extract_pages(input_path, output_path, page_numbers):
    """
    Extract specific pages from a PDF

    Args:
        input_path (str): Path to input PDF
        output_path (str): Path for output PDF
        page_numbers (list): List of page numbers to extract (1-indexed)

    Returns:
        dict: Result with success status
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page_num in page_numbers:
            if 1 <= page_num <= len(reader.pages):
                writer.add_page(reader.pages[page_num - 1])

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {
            'success': True,
            'message': f'{len(page_numbers)} sayfa çıkarıldı'
        }

    except Exception as e:
        logger.error(f"extract_pages error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}
