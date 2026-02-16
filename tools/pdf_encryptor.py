"""
PDF Encryption Tool - Add/remove password protection
"""
from PyPDF2 import PdfReader, PdfWriter
import pikepdf
import logging

logger = logging.getLogger(__name__)


def encrypt_pdf(input_path, output_path, password, owner_password=None, permissions=None):
    """
    Encrypt a PDF with password protection
    
    Args:
        input_path (str): Path to input PDF
        output_path (str): Path for encrypted PDF
        password (str): User password
        owner_password (str): Owner password (optional)
        permissions (dict): Permission flags (optional)
    
    Returns:
        dict: Result with success status
    """
    try:
        with pikepdf.open(input_path) as pdf:
            perm_extract = permissions.get('extract', False) if permissions else False
            perm_modify = permissions.get('modify', False) if permissions else False
            perm_print = permissions.get('print', True) if permissions else True

            encryption_settings = pikepdf.Encryption(
                user=password,
                owner=owner_password or password,
                allow=pikepdf.Permissions(
                    accessibility=True,
                    extract=perm_extract,
                    modify_annotation=perm_modify,
                    modify_assembly=perm_modify,
                    modify_form=perm_modify,
                    modify_other=perm_modify,
                    print_lowres=perm_print,
                    print_highres=perm_print
                )
            )
            pdf.save(output_path, encryption=encryption_settings)
        
        return {
            'success': True,
            'message': 'PDF encrypted successfully'
        }
    
    except Exception as e:
        logger.error(f"encrypt_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}


def decrypt_pdf(input_path, output_path, password):
    """
    Remove password protection from PDF
    
    Args:
        input_path (str): Path to encrypted PDF
        output_path (str): Path for decrypted PDF
        password (str): PDF password
    
    Returns:
        dict: Result with success status
    """
    try:
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(output_path)
        
        return {
            'success': True,
            'message': 'PDF decrypted successfully'
        }
    
    except pikepdf.PasswordError:
        return {'success': False, 'error': 'Incorrect password'}
    except Exception as e:
        logger.error(f"decrypt_pdf error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
