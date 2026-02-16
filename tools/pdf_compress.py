"""
PDF Compress Tool - Reduce PDF file size
Hibrit yontem: Faz 1 (PyMuPDF gorsel sikistirma) + Faz 2 (pikepdf stream optimizasyonu).
Metin ve vektor grafikleri tamamen korunur.
"""
import os
import io
import logging
import shutil
import subprocess
import tempfile
import fitz  # PyMuPDF
from PIL import Image

logger = logging.getLogger(__name__)


def _phase1_image_compress(input_path, output_path, quality_settings):
    """Faz 1: JPEG gorselleri dusuk kalitede + opsiyonel boyut kucultme.

    Guvenli degisiklikler:
    - stream verisi (yeni JPEG bytes)
    - Length (yeni boyut)
    - Width/Height (sadece boyut kucultme yapildiysa)
    Filter, ColorSpace, DecodeParms, BitsPerComponent -> DOKUNULMAZ.
    """
    jpeg_quality = quality_settings['jpeg_quality']
    max_dim = quality_settings.get('max_dim')  # None ise boyut kucultme yok

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

                # Sadece JPEG gorselleri isle
                if ext != "jpeg":
                    log_entries.append(f"[S.{page_num+1}] xref={xref}: ATLA ({ext})")
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
                saving_pct = round((1 - new_size / orig_size) * 100, 1)

                if new_size < orig_size * 0.90:
                    doc.update_stream(xref, compressed_bytes)
                    doc.xref_set_key(xref, "Length", str(new_size))
                    if resized:
                        doc.xref_set_key(xref, "Width", str(new_w))
                        doc.xref_set_key(xref, "Height", str(new_h))
                    images_compressed += 1
                    dim_info = f" -> {new_w}x{new_h}" if resized else ""
                    log_entries.append(
                        f"[S.{page_num+1}] xref={xref}: OK {width}x{height}{dim_info} "
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


def _compress_with_ghostscript(input_path, output_path, gs_setting='/ebook'):
    """Ghostscript ile tam sikistirma (en agresif yontem)."""
    cmd = [
        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={gs_setting}',
        '-dNOPAUSE', '-dBATCH', '-dQUIET',
        f'-sOutputFile={output_path}', input_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=300, text=True)
        return result.returncode == 0
    except Exception:
        return False


def compress_pdf(input_path, output_path, quality='medium'):
    """
    PDF sikistirma - 4 kalite seviyesi:
    - high:    Sadece JPEG kalite dusurme (75), boyut ayni
    - medium:  JPEG kalite dusurme (50) + boyut kucultme (maks 1600px)
    - low:     JPEG kalite dusurme (30) + boyut kucultme (maks 1200px)
    - maximum: Ghostscript /ebook (en agresif, yavas)
    """
    try:
        quality_settings = {
            'high':    {'jpeg_quality': 75},
            'medium':  {'jpeg_quality': 50, 'max_dim': 1600},
            'low':     {'jpeg_quality': 30, 'max_dim': 1200},
        }

        original_size = os.path.getsize(input_path)
        log = [f"Orijinal: {original_size} bayt, Kalite: {quality}"]

        # Maximum: Ghostscript kullan
        if quality == 'maximum':
            log.append("Ghostscript /ebook kullaniliyor...")
            gs_success = _compress_with_ghostscript(input_path, output_path)
            if gs_success:
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
                    'images_compressed': 0,
                    'log': log,
                }
            else:
                log.append("Ghostscript basarisiz, standart yontem deneniyor...")
                quality = 'low'  # fallback

        settings = quality_settings.get(quality, quality_settings['medium'])

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
