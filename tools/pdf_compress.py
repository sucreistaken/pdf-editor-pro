"""
PDF Compress Tool - Reduce PDF file size
Ghostscript tabanli sikistirma + pikepdf stream optimizasyonu.
Metin, vektor grafikleri ve gorseller tamamen korunur.
"""
import os
import logging
import shutil
import subprocess
import tempfile

logger = logging.getLogger(__name__)


def _compress_with_ghostscript(input_path, output_path, quality='medium'):
    """Ghostscript ile PDF sikistirma - en guvenilir yontem."""
    gs_settings = {
        'low': '/screen',       # 72 dpi - maksimum sikistirma
        'medium': '/ebook',     # 150 dpi - dengeli
        'high': '/printer',     # 300 dpi - yuksek kalite
    }
    setting = gs_settings.get(quality, '/ebook')

    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={setting}',
        '-dNOPAUSE',
        '-dBATCH',
        '-dQUIET',
        f'-sOutputFile={output_path}',
        input_path,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=300,
            text=True,
        )
        if result.returncode == 0:
            return True, f"Ghostscript ({setting}) başarılı"
        else:
            err = result.stderr[:200] if result.stderr else "bilinmeyen hata"
            logger.warning(f"Ghostscript hatası: {err}")
            return False, f"Ghostscript hatası: {err}"
    except FileNotFoundError:
        return False, "Ghostscript yüklü değil"
    except subprocess.TimeoutExpired:
        return False, "Ghostscript zaman aşımı (300s)"
    except Exception as e:
        logger.warning(f"Ghostscript hatası: {e}")
        return False, f"Ghostscript hatası: {e}"


def _compress_with_pikepdf(input_path, output_path):
    """pikepdf ile stream sikistirma (fallback yontem)."""
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
        return True, "pikepdf stream optimizasyonu başarılı"
    except Exception as e:
        logger.warning(f"pikepdf hatası: {e}")
        return False, f"pikepdf hatası: {e}"


def compress_pdf(input_path, output_path, quality='medium'):
    """
    PDF dosyasini sikistirir.
    1. Ghostscript ile tam sikistirma (gorsel + stream)
    2. Ghostscript yoksa/basarisizsa pikepdf ile stream optimizasyonu
    """
    try:
        original_size = os.path.getsize(input_path)
        log = [f"Orijinal boyut: {original_size} bayt, Kalite: {quality}"]

        # Yontem 1: Ghostscript
        gs_success, gs_msg = _compress_with_ghostscript(input_path, output_path, quality)
        log.append(f"Ghostscript: {gs_msg}")

        if gs_success:
            gs_size = os.path.getsize(output_path)
            log.append(f"Ghostscript sonuc: {gs_size} bayt")

            # pikepdf ile ek optimizasyon dene
            output_dir = os.path.dirname(output_path)
            pike_fd, pike_path = tempfile.mkstemp(suffix='.pdf', dir=output_dir)
            os.close(pike_fd)

            try:
                pike_success, pike_msg = _compress_with_pikepdf(output_path, pike_path)
                log.append(f"pikepdf: {pike_msg}")

                if pike_success:
                    pike_size = os.path.getsize(pike_path)
                    log.append(f"pikepdf sonuc: {pike_size} bayt")
                    if pike_size < gs_size:
                        shutil.move(pike_path, output_path)
                        log.append("pikepdf daha kucuk, kullaniliyor")
                    else:
                        log.append("Ghostscript daha kucuk, korunuyor")
            finally:
                if os.path.exists(pike_path):
                    os.remove(pike_path)
        else:
            # Fallback: sadece pikepdf
            log.append("Ghostscript kullanılamadı, pikepdf deneniyor...")
            pike_success, pike_msg = _compress_with_pikepdf(input_path, output_path)
            log.append(f"pikepdf: {pike_msg}")

            if not pike_success:
                return {
                    'success': False,
                    'error': 'Sıkıştırma başarısız',
                    'log': log,
                }

        compressed_size = os.path.getsize(output_path)

        # Sonuc buyukse orijinali kopyala
        if compressed_size >= original_size:
            shutil.copy2(input_path, output_path)
            compressed_size = original_size
            log.append("Sonuç büyük, orijinal korunuyor")

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

    except Exception as e:
        logger.error(f"compress_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
