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
    """Faz 1: PyMuPDF ile gomulu gorsel sikistirma.

    ONEMLI: Gorsel boyutlari (Width/Height) ASLA degistirilmez.
    Sadece JPEG kalitesi dusurulur. Boyut degistirmek sayfa transformation
    matrix'ini bozar ve bos sayfalara neden olur.
    """
    jpeg_quality = quality_settings['jpeg_quality']

    doc = fitz.open(input_path)
    images_compressed = 0
    xrefs_done = set()

    for page in doc:
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            smask = img_info[1]  # SMask xref (transparency)

            if xref in xrefs_done:
                continue
            xrefs_done.add(xref)

            # Transparency/SMask iceren gorselleri atla - JPEG desteklemez
            if smask and smask != 0:
                continue

            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue

                img_bytes = base_image["image"]
                width = base_image["width"]
                height = base_image["height"]

                # Cok kucuk gorselleri atla (ikon, logo vs.)
                if width < 100 and height < 100:
                    continue

                # Zaten JPEG ve kucukse atla
                if base_image.get("ext") == "jpeg" and len(img_bytes) < 50000:
                    continue

                pil_img = Image.open(io.BytesIO(img_bytes))

                # Alfa kanalli gorselleri atla (JPEG desteklemez)
                if pil_img.mode in ('RGBA', 'PA', 'LA', 'P'):
                    # P mode palette'li olabilir, alfa icerip icermedigini bilemeyiz
                    continue

                # Renk modu donusumu
                if pil_img.mode == 'CMYK':
                    pil_img = pil_img.convert('RGB')
                    is_gray = False
                elif pil_img.mode == 'L':
                    is_gray = True
                elif pil_img.mode != 'RGB':
                    pil_img = pil_img.convert('RGB')
                    is_gray = False
                else:
                    is_gray = False

                # JPEG olarak yeniden sikistir (BOYUT DEGISTIRMEDEN)
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
                compressed_bytes = buf.getvalue()

                # Sadece %10'dan fazla kuculduyse degistir (guvenli esik)
                if len(compressed_bytes) < len(img_bytes) * 0.90:
                    doc.update_stream(xref, compressed_bytes)
                    doc.xref_set_key(xref, "Filter", "/DCTDecode")
                    doc.xref_set_key(xref, "DecodeParms", "null")
                    doc.xref_set_key(xref, "ColorSpace",
                                     "/DeviceGray" if is_gray else "/DeviceRGB")
                    doc.xref_set_key(xref, "BitsPerComponent", "8")
                    doc.xref_set_key(xref, "Length", str(len(compressed_bytes)))
                    # Width ve Height DEGISTIRILMEZ - orijinal degerler korunur
                    images_compressed += 1

            except Exception as e:
                logger.warning(f"Görsel sıkıştırma hatası (xref={xref}): {e}")
                continue

    doc.save(output_path, garbage=4, deflate=True, clean=True)
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
        logger.warning(f"pikepdf stream optimizasyonu başarısız: {e}")
        return False


def compress_pdf(input_path, output_path, quality='medium'):
    """
    PDF dosyasini sikistirir (hibrit yontem).
    Faz 1: Gomulu gorselleri JPEG olarak yeniden sikistirir (PyMuPDF).
    Faz 2: Stream'leri sikistirir, kullanilmayan nesneleri temizler (pikepdf).
    Metin ve vektor icerik tamamen korunur.
    """
    try:
        quality_settings = {
            'low': {'max_dim': 800, 'jpeg_quality': 30},
            'medium': {'max_dim': 1200, 'jpeg_quality': 50},
            'high': {'max_dim': 1600, 'jpeg_quality': 75}
        }
        settings = quality_settings.get(quality, quality_settings['medium'])
        original_size = os.path.getsize(input_path)

        # Faz 1: Gorsel sikistirma (gecici dosyaya yaz)
        output_dir = os.path.dirname(output_path)
        phase1_fd, phase1_path = tempfile.mkstemp(suffix='.pdf', dir=output_dir)
        os.close(phase1_fd)

        try:
            images_compressed = _phase1_image_compress(input_path, phase1_path, settings)
            phase1_size = os.path.getsize(phase1_path)

            # Faz 2: Stream optimizasyonu
            phase2_success = _phase2_stream_optimize(phase1_path, output_path)

            if phase2_success:
                phase2_size = os.path.getsize(output_path)
                # Faz 2 buyuttuyse Faz 1 sonucunu kullan
                if phase2_size >= phase1_size:
                    shutil.copy2(phase1_path, output_path)
            else:
                # pikepdf basarisiz: Faz 1 sonucunu kullan
                shutil.copy2(phase1_path, output_path)
        finally:
            # Gecici Faz 1 dosyasini temizle
            if os.path.exists(phase1_path):
                os.remove(phase1_path)

        compressed_size = os.path.getsize(output_path)

        # Sonuc buyukse orijinali kopyala
        if compressed_size >= original_size:
            shutil.copy2(input_path, output_path)
            compressed_size = original_size

        reduction = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0

        return {
            'success': True,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'reduction_percent': round(max(reduction, 0), 1),
            'images_compressed': images_compressed
        }

    except Exception as e:
        logger.error(f"compress_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
