"""
PDF Compress Tool - Reduce PDF file size
Hibrit yontem: Faz 1 (PyMuPDF gorsel sikistirma) + Faz 2 (pikepdf stream optimizasyonu).
Metin ve vektor grafikleri tamamen korunur.
"""
import os
import io
import logging
import shutil
import tempfile
import fitz  # PyMuPDF
from PIL import Image

logger = logging.getLogger(__name__)


def _phase1_image_compress(input_path, output_path, quality_settings):
    """Faz 1: JPEG gorselleri dusuk kalitede + opsiyonel boyut kucultme."""
    jpeg_quality = quality_settings['jpeg_quality']
    max_dim = quality_settings.get('max_dim')

    doc = fitz.open(input_path)
    images_compressed = 0
    xrefs_done = set()

    for page in doc:
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            smask = img_info[1]

            if xref in xrefs_done:
                continue
            xrefs_done.add(xref)

            if smask and smask != 0:
                continue

            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue

                img_bytes = base_image["image"]
                width = base_image["width"]
                height = base_image["height"]
                ext = base_image.get("ext", "?")

                # Sadece JPEG gorselleri isle
                if ext != "jpeg":
                    continue

                if width < 100 and height < 100:
                    continue

                if len(img_bytes) < 50000:
                    continue

                pil_img = Image.open(io.BytesIO(img_bytes))

                # Boyut kucultme (sadece max_dim varsa)
                resized = False
                if max_dim and (width > max_dim or height > max_dim):
                    pil_img.thumbnail((max_dim, max_dim), Image.LANCZOS)
                    resized = True

                new_w, new_h = pil_img.size

                # Ayni modda yeniden kodla
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
                compressed_bytes = buf.getvalue()

                orig_size = len(img_bytes)
                new_size = len(compressed_bytes)

                if new_size < orig_size * 0.90:
                    doc.update_stream(xref, compressed_bytes)
                    doc.xref_set_key(xref, "Length", str(new_size))
                    if resized:
                        doc.xref_set_key(xref, "Width", str(new_w))
                        doc.xref_set_key(xref, "Height", str(new_h))
                    images_compressed += 1

            except Exception as e:
                logger.warning(f"Gorsel sikistirma hatasi (xref={xref}): {e}")
                continue

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    return images_compressed


def _phase2_stream_optimize(input_path, output_path):
    """Faz 2: pikepdf ile stream sikistirma ve kullanilmayan nesne temizligi."""
    try:
        import pikepdf
        pdf = pikepdf.open(input_path)
        pdf.save(
            output_path,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            recompress_flate=True,
        )
        pdf.close()
        return True
    except Exception as e:
        logger.warning(f"pikepdf hatasi: {e}")
        return False


def compress_pdf(input_path, output_path, quality='medium'):
    """
    PDF sikistirma - 3 kalite seviyesi:
    - high:   JPEG kalite 75, boyut ayni
    - medium: JPEG kalite 50, maks 1600px
    - low:    JPEG kalite 30, maks 1200px
    """
    try:
        quality_settings = {
            'high':   {'jpeg_quality': 75},
            'medium': {'jpeg_quality': 50, 'max_dim': 1600},
            'low':    {'jpeg_quality': 30, 'max_dim': 1200},
        }

        original_size = os.path.getsize(input_path)
        settings = quality_settings.get(quality, quality_settings['medium'])

        output_dir = os.path.dirname(output_path)
        phase1_fd, phase1_path = tempfile.mkstemp(suffix='.pdf', dir=output_dir)
        os.close(phase1_fd)

        try:
            images_compressed = _phase1_image_compress(
                input_path, phase1_path, settings
            )
            phase1_size = os.path.getsize(phase1_path)

            phase2_success = _phase2_stream_optimize(phase1_path, output_path)

            if phase2_success:
                phase2_size = os.path.getsize(output_path)
                if phase2_size >= phase1_size:
                    shutil.copy2(phase1_path, output_path)
            else:
                shutil.copy2(phase1_path, output_path)
        finally:
            if os.path.exists(phase1_path):
                os.remove(phase1_path)

        compressed_size = os.path.getsize(output_path)

        if compressed_size >= original_size:
            shutil.copy2(input_path, output_path)
            compressed_size = original_size

        reduction = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0

        return {
            'success': True,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'reduction_percent': round(max(reduction, 0), 1),
            'images_compressed': images_compressed,
        }

    except Exception as e:
        logger.error(f"compress_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
