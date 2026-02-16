"""
PDF Compare Tool - Iki PDF dosyasini karsilastir
"""
import fitz  # PyMuPDF
from PIL import Image, ImageChops
import numpy as np
import io
import base64
import difflib
import logging

logger = logging.getLogger(__name__)

MAX_COMPARE_PAGES = 50


def compare_pdfs(path1, path2):
    """
    Iki PDF dosyasini sayfa sayfa karsilastir (gorsel + metin)

    Args:
        path1 (str): Birinci PDF yolu
        path2 (str): Ikinci PDF yolu

    Returns:
        dict: Karsilastirma sonuclari
    """
    doc1 = None
    doc2 = None
    try:
        doc1 = fitz.open(path1)
        doc2 = fitz.open(path2)

        pages1 = len(doc1)
        pages2 = len(doc2)
        max_pages = max(pages1, pages2)

        if max_pages > MAX_COMPARE_PAGES:
            return {
                'success': False,
                'error': f'Karşılaştırma en fazla {MAX_COMPARE_PAGES} sayfa destekler. '
                         f'PDF dosyalarınız {max_pages} sayfa içeriyor.'
            }

        results = []
        total_diffs = 0

        for i in range(max_pages):
            page_result = {'page': i + 1, 'has_diff': False}

            if i >= pages1:
                page_result['status'] = 'only_in_second'
                page_result['has_diff'] = True
                total_diffs += 1
                results.append(page_result)
                continue

            if i >= pages2:
                page_result['status'] = 'only_in_first'
                page_result['has_diff'] = True
                total_diffs += 1
                results.append(page_result)
                continue

            # Gorsel karsilastirma
            page1 = doc1[i]
            page2 = doc2[i]

            zoom = 1.0
            mat = fitz.Matrix(zoom, zoom)
            pix1 = page1.get_pixmap(matrix=mat)
            pix2 = page2.get_pixmap(matrix=mat)

            img1 = Image.open(io.BytesIO(pix1.tobytes("png")))
            img2 = Image.open(io.BytesIO(pix2.tobytes("png")))

            # Boyutlari esitle
            max_w = max(img1.width, img2.width)
            max_h = max(img1.height, img2.height)

            canvas1 = Image.new('RGB', (max_w, max_h), (255, 255, 255))
            canvas1.paste(img1, (0, 0))
            canvas2 = Image.new('RGB', (max_w, max_h), (255, 255, 255))
            canvas2.paste(img2, (0, 0))

            # Fark gorseli
            diff_img = ImageChops.difference(canvas1, canvas2)

            # Fark var mi kontrol et
            bbox = diff_img.getbbox()
            if bbox:
                page_result['has_diff'] = True
                total_diffs += 1

                # Fark gorselini kirmizi vurgulu yap (numpy ile hizli)
                arr1 = np.array(canvas1)
                arr_diff = np.array(diff_img)
                mask = np.any(arr_diff > 10, axis=2)
                arr1[mask] = [255, 0, 0]
                diff_highlight = Image.fromarray(arr1)

                # Base64 gorsel
                buf = io.BytesIO()
                diff_highlight.save(buf, format='PNG', optimize=True)
                page_result['diff_image'] = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

            # Metin karsilastirma
            text1 = page1.get_text()
            text2 = page2.get_text()

            if text1 != text2:
                page_result['has_diff'] = True
                lines1 = text1.splitlines()
                lines2 = text2.splitlines()
                diff_lines = list(difflib.unified_diff(lines1, lines2, lineterm='', n=2))
                if diff_lines:
                    page_result['text_diff'] = '\n'.join(diff_lines[:50])

            page_result['status'] = 'different' if page_result['has_diff'] else 'identical'
            results.append(page_result)

        return {
            'success': True,
            'pages_file1': pages1,
            'pages_file2': pages2,
            'total_pages_compared': max_pages,
            'pages_with_differences': total_diffs,
            'results': results
        }

    except Exception as e:
        logger.error(f"compare_pdfs error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc1:
            doc1.close()
        if doc2:
            doc2.close()
