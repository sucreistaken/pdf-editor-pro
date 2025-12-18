"""
PDF Page Numbering - Sayfa numaralandirma araci
"""
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import logging

logger = logging.getLogger(__name__)


def add_page_numbers(input_path, output_path, position='bottom-center',
                     format_str='{n}', start_number=1, skip_first=False,
                     font_size=12, color=(0.3, 0.3, 0.3)):
    """
    PDF sayfalarina numara ekle

    Args:
        input_path: Girdi PDF yolu
        output_path: Cikti PDF yolu
        position: Konum ('bottom-center', 'bottom-right', 'bottom-left',
                         'top-center', 'top-right', 'top-left')
        format_str: Format ({n} = numara, {total} = toplam)
        start_number: Baslangic numarasi
        skip_first: Ilk sayfayi atla
        font_size: Yazi boyutu
        color: RGB renk (0-1 aralik)
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        packets = []

        for i, page in enumerate(reader.pages):
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            if skip_first and i == 0:
                writer.add_page(page)
                continue

            if skip_first:
                page_num = start_number + i - 1
            else:
                page_num = start_number + i

            text = format_str.replace('{n}', str(page_num)).replace('{total}', str(total_pages))

            packet = io.BytesIO()
            packets.append(packet)

            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            can.setFillColorRGB(*color)
            can.setFont("Helvetica", font_size)

            text_width = can.stringWidth(text, "Helvetica", font_size)
            margin = 40

            if 'center' in position:
                x = (page_width - text_width) / 2
            elif 'right' in position:
                x = page_width - text_width - margin
            else:
                x = margin

            if 'top' in position:
                y = page_height - margin - font_size
            else:
                y = margin

            can.drawString(x, y, text)
            can.save()

            packet.seek(0)
            overlay = PdfReader(packet)
            page.merge_page(overlay.pages[0])

            writer.add_page(page)

        with open(output_path, 'wb') as f:
            writer.write(f)

        for p in packets:
            p.close()

        return {
            'success': True,
            'page_count': total_pages,
            'message': f'{total_pages} sayfaya numara eklendi'
        }

    except Exception as e:
        logger.error(f"add_page_numbers error: {e}", exc_info=True)
        return {'success': False, 'error': 'Islem basarisiz'}
