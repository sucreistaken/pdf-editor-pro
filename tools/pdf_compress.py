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
    """Faz 1: Sadece JPEG gorselleri daha dusuk kalitede yeniden kodla.

    KURAL: Sadece stream verisi ve Length degisir. Baska HICBIR KEY degismez.
    Filter, ColorSpace, DecodeParms, Width, Height, BitsPerComponent -> DOKUNULMAZ.
    """
    jpeg_quality = quality_settings['jpeg_quality']

    doc = fitz.open(input_path)
    images_compressed = 0
    xrefs_done = set()
    log_entries = []

    for page_num, page in enumerate(doc):
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            smask = img_info[1]

            if xref in xrefs_done:
                continue
            xrefs_done.add(xref)

            if smask and smask != 0:
                log_entries.append(f"[S.{page_num+1}] xref={xref}: ATLA (seffaf)")
                continue

            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue

                img_bytes = base_image["image"]
                width = base_image["width"]
                height = base_image["height"]
                ext = base_image.get("ext", "?")

                # Sadece JPEG gorselleri isle - diger formatlara DOKUNMA
                if ext != "jpeg":
                    log_entries.append(f"[S.{page_num+1}] xref={xref}: ATLA ({ext}, JPEG degil)")
                    continue

                if width < 100 and height < 100:
                    continue

                if len(img_bytes) < 50000:
                    log_entries.append(f"[S.{page_num+1}] xref={xref}: ATLA (kucuk {len(img_bytes)}B)")
                    continue

                pil_img = Image.open(io.BytesIO(img_bytes))

                # PIL ile ayni modda yeniden kodla
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
                compressed_bytes = buf.getvalue()

                orig_size = len(img_bytes)
                new_size = len(compressed_bytes)
                saving_pct = round((1 - new_size / orig_size) * 100, 1)

                if new_size < orig_size * 0.90:
                    # SADECE stream ve Length degistir - BASKA HICBIR SEY DEGISMEZ
                    doc.update_stream(xref, compressed_bytes)
                    doc.xref_set_key(xref, "Length", str(new_size))
                    images_compressed += 1
                    log_entries.append(
                        f"[S.{page_num+1}] xref={xref}: OK {width}x{height} "
                        f"{pil_img.mode} {orig_size}B->{new_size}B (%{saving_pct})"
                    )
                else:
                    log_entries.append(
                        f"[S.{page_num+1}] xref={xref}: ATLA (az tasarruf %{saving_pct})"
                    )

            except Exception as e:
                log_entries.append(f"[S.{page_num+1}] xref={xref}: HATA {e}")
                continue

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    return images_compressed, log_entries


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
        logger.warning(f"pikepdf hatası: {e}")
        return False


def compress_pdf(input_path, output_path, quality='medium'):
    """
    PDF dosyasini sikistirir (hibrit yontem).
    Faz 1: JPEG gorselleri dusuk kalitede yeniden kodlar (hizli, PyMuPDF).
    Faz 2: Stream optimizasyonu (pikepdf).
    """
    try:
        quality_settings = {
            'low': {'jpeg_quality': 30},
            'medium': {'jpeg_quality': 50},
            'high': {'jpeg_quality': 75}
        }
        settings = quality_settings.get(quality, quality_settings['medium'])
        original_size = os.path.getsize(input_path)
        log = [f"Orijinal: {original_size} bayt, Kalite: {quality}"]

        output_dir = os.path.dirname(output_path)
        phase1_fd, phase1_path = tempfile.mkstemp(suffix='.pdf', dir=output_dir)
        os.close(phase1_fd)

        try:
            images_compressed, phase1_log = _phase1_image_compress(
                input_path, phase1_path, settings
            )
            log.extend(phase1_log)
            phase1_size = os.path.getsize(phase1_path)
            log.append(f"Faz1: {images_compressed} gorsel, {phase1_size} bayt")

            phase2_success = _phase2_stream_optimize(phase1_path, output_path)

            if phase2_success:
                phase2_size = os.path.getsize(output_path)
                log.append(f"Faz2: {phase2_size} bayt")
                if phase2_size >= phase1_size:
                    shutil.copy2(phase1_path, output_path)
                    log.append("Faz2 buyuttu, Faz1 kullaniliyor")
            else:
                shutil.copy2(phase1_path, output_path)
                log.append("Faz2 basarisiz, Faz1 kullaniliyor")
        finally:
            if os.path.exists(phase1_path):
                os.remove(phase1_path)

        compressed_size = os.path.getsize(output_path)

        if compressed_size >= original_size:
            shutil.copy2(input_path, output_path)
            compressed_size = original_size
            log.append("Sonuc buyuk, orijinal korunuyor")

        reduction = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
        log.append(f"Final: {compressed_size} bayt, %{round(reduction, 1)} azalma")

        return {
            'success': True,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'reduction_percent': round(max(reduction, 0), 1),
            'images_compressed': images_compressed,
            'log': log,
        }

    except Exception as e:
        logger.error(f"compress_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
