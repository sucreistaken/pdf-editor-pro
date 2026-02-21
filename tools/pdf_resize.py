"""
PDF Resize - Sayfa boyutu degistirme (PyMuPDF)
"""
import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

# Standart sayfa boyutlari (points: 1 inch = 72 points)
PAGE_SIZES = {
    'a4': (595.28, 841.89),
    'letter': (612, 792),
    'a3': (841.89, 1190.55),
    'a5': (419.53, 595.28),
    'legal': (612, 1008),
}


def resize_pdf(input_path, output_path, target_size, mode='fit'):
    """
    PDF sayfa boyutunu degistir.

    Args:
        input_path: Giris PDF yolu
        output_path: Cikti PDF yolu
        target_size: 'a4', 'letter', 'a3', 'a5', 'legal' veya [width, height] (pt)
        mode: 'fit' (icerigi olcekle), 'crop' (kes), 'expand' (bosluk ekle)

    Returns:
        dict: {success, message, page_count, original_size, new_size}
    """
    try:
        # Hedef boyutu belirle
        if isinstance(target_size, str):
            target_size_lower = target_size.lower()
            if target_size_lower not in PAGE_SIZES:
                return {'success': False, 'error': f'Gecersiz boyut: {target_size}'}
            target_w, target_h = PAGE_SIZES[target_size_lower]
        elif isinstance(target_size, (list, tuple)) and len(target_size) == 2:
            target_w, target_h = float(target_size[0]), float(target_size[1])
        else:
            return {'success': False, 'error': 'Gecersiz hedef boyut'}

        src_doc = fitz.open(input_path)
        page_count = len(src_doc)

        if page_count == 0:
            src_doc.close()
            return {'success': False, 'error': 'PDF bos'}

        # Orijinal boyut bilgisi (ilk sayfa)
        first_page = src_doc[0]
        orig_w = first_page.rect.width
        orig_h = first_page.rect.height
        original_size = f'{orig_w:.0f}x{orig_h:.0f} pt'
        new_size = f'{target_w:.0f}x{target_h:.0f} pt'

        # Yeni PDF olustur
        new_doc = fitz.open()

        for i in range(page_count):
            src_page = src_doc[i]
            src_rect = src_page.rect
            sw, sh = src_rect.width, src_rect.height

            # Yeni sayfa olustur
            new_page = new_doc.new_page(width=target_w, height=target_h)

            if mode == 'fit':
                # Icerigi hedef boyuta sigdir (aspect ratio koru)
                scale_x = target_w / sw
                scale_y = target_h / sh
                scale = min(scale_x, scale_y)

                new_w = sw * scale
                new_h = sh * scale
                # Ortala
                x_offset = (target_w - new_w) / 2
                y_offset = (target_h - new_h) / 2

                dest_rect = fitz.Rect(x_offset, y_offset, x_offset + new_w, y_offset + new_h)
                new_page.show_pdf_page(dest_rect, src_doc, i)

            elif mode == 'crop':
                # Ortadan kes
                # Kaynak sayfanin hangi kismini gosterecegimizi hesapla
                clip_w = min(sw, target_w)
                clip_h = min(sh, target_h)
                clip_x = (sw - clip_w) / 2
                clip_y = (sh - clip_h) / 2
                clip_rect = fitz.Rect(clip_x, clip_y, clip_x + clip_w, clip_y + clip_h)

                dest_x = (target_w - clip_w) / 2
                dest_y = (target_h - clip_h) / 2
                dest_rect = fitz.Rect(dest_x, dest_y, dest_x + clip_w, dest_y + clip_h)

                new_page.show_pdf_page(dest_rect, src_doc, i, clip=clip_rect)

            elif mode == 'expand':
                # Orijinal boyutu koru, etrafina bosluk ekle veya kes
                dest_x = (target_w - sw) / 2
                dest_y = (target_h - sh) / 2
                dest_rect = fitz.Rect(dest_x, dest_y, dest_x + sw, dest_y + sh)
                new_page.show_pdf_page(dest_rect, src_doc, i)

            else:
                # Varsayilan: fit
                scale_x = target_w / sw
                scale_y = target_h / sh
                scale = min(scale_x, scale_y)
                new_w = sw * scale
                new_h = sh * scale
                x_offset = (target_w - new_w) / 2
                y_offset = (target_h - new_h) / 2
                dest_rect = fitz.Rect(x_offset, y_offset, x_offset + new_w, y_offset + new_h)
                new_page.show_pdf_page(dest_rect, src_doc, i)

        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        src_doc.close()

        # Boyut isimlerini bul
        size_name = target_size.upper() if isinstance(target_size, str) else 'Ozel'

        return {
            'success': True,
            'message': f'{page_count} sayfa {size_name} boyutuna donusturuldu',
            'page_count': page_count,
            'original_size': original_size,
            'new_size': new_size
        }

    except Exception as e:
        logger.error(f"Resize hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'Boyut degistirme islemi basarisiz'}
