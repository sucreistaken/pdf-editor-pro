"""
Watermark Tool - Add text or image watermarks to PDF
"""
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
import logging

logger = logging.getLogger(__name__)


def add_text_watermark(input_path, output_path, text, position='center',
                       opacity=0.3, font_size=50, color=(0, 0, 0),
                       rotation=0):
    """
    Add text watermark to all pages

    Args:
        input_path (str): Path to input PDF
        output_path (str): Path for watermarked PDF
        text (str): Watermark text
        position (str): 'center', 'top-right', 'bottom-left', etc.
        opacity (float): Transparency (0-1)
        font_size (int): Font size
        color (tuple): RGB color (0-1 range)
        rotation (int): Rotation angle in degrees
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        packets = []

        for page in reader.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            packet = io.BytesIO()
            packets.append(packet)

            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            can.setFillColorRGB(*color, alpha=opacity)
            can.setFont("Helvetica-Bold", font_size)

            text_width = can.stringWidth(text, "Helvetica-Bold", font_size)

            if position == 'center':
                x = (page_width - text_width) / 2
                y = page_height / 2
            elif position == 'top-center':
                x = (page_width - text_width) / 2
                y = page_height - 50
            elif position == 'top-right':
                x = page_width - text_width - 50
                y = page_height - 50
            elif position == 'bottom-left':
                x = 50
                y = 50
            elif position == 'bottom-right':
                x = page_width - text_width - 50
                y = 50
            else:  # top-left
                x = 50
                y = page_height - 50

            if rotation:
                can.saveState()
                can.translate(page_width / 2, page_height / 2)
                can.rotate(rotation)
                can.drawString(-text_width / 2, 0, text)
                can.restoreState()
            else:
                can.drawString(x, y, text)

            can.save()

            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            page.merge_page(watermark_pdf.pages[0])

            writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        for p in packets:
            p.close()

        return {
            'success': True,
            'message': f'{len(reader.pages)} sayfaya filigran eklendi'
        }

    except Exception as e:
        logger.error(f"add_text_watermark error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def add_image_watermark(input_path, output_path, image_path,
                        position='center', opacity=0.5, scale=0.2):
    """
    Add image watermark to all pages
    """
    try:
        if not os.path.exists(image_path):
            return {'success': False, 'error': 'Filigran görseli bulunamadı'}

        reader = PdfReader(input_path)
        writer = PdfWriter()
        packets = []

        for page in reader.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            packet = io.BytesIO()
            packets.append(packet)

            can = canvas.Canvas(packet, pagesize=(page_width, page_height))

            img = ImageReader(image_path)
            img_width, img_height = img.getSize()

            scaled_width = img_width * scale
            scaled_height = img_height * scale

            if position == 'center':
                x = (page_width - scaled_width) / 2
                y = (page_height - scaled_height) / 2
            elif position == 'top-center':
                x = (page_width - scaled_width) / 2
                y = page_height - scaled_height - 20
            elif position == 'top-right':
                x = page_width - scaled_width - 20
                y = page_height - scaled_height - 20
            elif position == 'bottom-left':
                x = 20
                y = 20
            elif position == 'bottom-right':
                x = page_width - scaled_width - 20
                y = 20
            else:  # top-left
                x = 20
                y = page_height - scaled_height - 20

            can.setFillAlpha(opacity)
            can.drawImage(img, x, y, width=scaled_width, height=scaled_height, mask='auto')
            can.save()

            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            page.merge_page(watermark_pdf.pages[0])

            writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        for p in packets:
            p.close()

        return {
            'success': True,
            'message': f'{len(reader.pages)} sayfaya görsel filigran eklendi'
        }

    except Exception as e:
        logger.error(f"add_image_watermark error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
