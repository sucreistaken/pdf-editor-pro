"""
Office to PDF - Word/Excel/PowerPoint -> PDF donusumu (LibreOffice headless)
"""
import os
import subprocess
import logging
import shutil

logger = logging.getLogger(__name__)

# Desteklenen dosya uzantilari
SUPPORTED_EXTENSIONS = {
    '.docx', '.doc', '.xlsx', '.xls',
    '.pptx', '.ppt', '.odt', '.ods', '.odp'
}

FILE_TYPE_NAMES = {
    '.docx': 'Word', '.doc': 'Word',
    '.xlsx': 'Excel', '.xls': 'Excel',
    '.pptx': 'PowerPoint', '.ppt': 'PowerPoint',
    '.odt': 'Writer', '.ods': 'Calc', '.odp': 'Impress',
}


def _find_libreoffice():
    """LibreOffice binary yolunu bul"""
    try:
        import config
        if hasattr(config, 'LIBREOFFICE_PATH') and config.LIBREOFFICE_PATH:
            return config.LIBREOFFICE_PATH
    except Exception:
        pass

    # Sistem PATH'inde ara
    lo_path = shutil.which('libreoffice') or shutil.which('soffice')
    if lo_path:
        return lo_path

    # Windows varsayilan yollar
    windows_paths = [
        r'C:\Program Files\LibreOffice\program\soffice.exe',
        r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
    ]
    for p in windows_paths:
        if os.path.isfile(p):
            return p

    return None


def office_to_pdf(input_path, output_path):
    """
    Office dosyasini PDF'e donustur.

    Args:
        input_path: Giris dosya yolu (.docx, .xlsx, .pptx vs.)
        output_path: Cikti PDF yolu

    Returns:
        dict: {success, message, file_type}
    """
    try:
        # Uzanti kontrolu
        ext = os.path.splitext(input_path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return {
                'success': False,
                'error': f'Desteklenmeyen dosya formati: {ext}'
            }

        file_type = FILE_TYPE_NAMES.get(ext, 'Office')

        # LibreOffice yolunu bul
        lo_path = _find_libreoffice()
        if not lo_path:
            return {
                'success': False,
                'error': 'LibreOffice bulunamadi. Lutfen yukleyin.'
            }

        # Cikti klasoru
        output_dir = os.path.dirname(output_path)
        if not output_dir:
            output_dir = '.'

        # LibreOffice ile donustur
        cmd = [
            lo_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            logger.error(f"LibreOffice hatasi: {result.stderr}")
            return {'success': False, 'error': 'Donusturme islemi basarisiz'}

        # LibreOffice cikti dosyasini bul ve yeniden adlandir
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        lo_output = os.path.join(output_dir, base_name + '.pdf')

        if not os.path.exists(lo_output):
            return {'success': False, 'error': 'Cikti dosyasi olusturulamadi'}

        # Hedef yola tasi
        if lo_output != output_path:
            shutil.move(lo_output, output_path)

        # Sayfa sayisini al
        page_count = 0
        try:
            import fitz
            doc = fitz.open(output_path)
            page_count = len(doc)
            doc.close()
        except Exception:
            pass

        return {
            'success': True,
            'message': f'{file_type} dosyasi PDF\'e donusturuldu',
            'file_type': file_type,
            'page_count': page_count
        }

    except subprocess.TimeoutExpired:
        logger.error("LibreOffice timeout")
        return {'success': False, 'error': 'Donusturme suresi doldu (zaman asimi)'}
    except Exception as e:
        logger.error(f"Office to PDF hatasi: {e}", exc_info=True)
        return {'success': False, 'error': 'Donusturme islemi basarisiz'}
