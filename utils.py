"""
PDF Tools - Yardimci fonksiyonlar
"""
import os
from flask import jsonify


def api_success(data=None, **kwargs):
    """Standart basarili API yaniti"""
    response = {'success': True}
    if data:
        response.update(data)
    response.update(kwargs)
    return jsonify(response)


def api_error(message, status_code=400):
    """Standart hata API yaniti"""
    return jsonify({'success': False, 'error': message}), status_code


def safe_path(base_dir, filename):
    """
    Path traversal saldirilarini onler.
    Dosya yolunun base_dir icinde kaldigini dogrular.
    """
    # Normalize paths
    base = os.path.realpath(base_dir)
    filepath = os.path.realpath(os.path.join(base_dir, filename))

    # Yolun base icinde oldugundan emin ol
    if not filepath.startswith(base + os.sep) and filepath != base:
        return None

    return filepath


def format_size(size_bytes):
    """Dosya boyutunu okunabilir formata cevir"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
