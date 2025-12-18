"""
PDF Repair Tool
- Repair corrupted PDF files
- Recover pages from damaged PDFs
- Fix common PDF issues
"""
import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)


def repair_pdf(input_path, output_path):
    """
    Attempt to repair a corrupted PDF file.
    try/finally ile kaynak sizintisi onlenir.
    """
    issues_found = []
    issues_fixed = []
    doc = None
    new_doc = None

    try:
        doc = fitz.open(input_path)

        if doc.is_encrypted:
            issues_found.append("Şifreli PDF")

        if doc.needs_pass:
            return {
                'success': False,
                'error': 'PDF şifre korumalı. Önce şifreyi kaldırın.',
                'issues_found': issues_found
            }

        page_count = len(doc)
        if page_count == 0:
            issues_found.append("Sayfa bulunamadı")
            return {
                'success': False,
                'error': 'PDF dosyasında sayfa bulunamadı.',
                'issues_found': issues_found
            }

        new_doc = fitz.open()
        recovered_pages = 0
        failed_pages = []

        for i in range(page_count):
            try:
                new_doc.insert_pdf(doc, from_page=i, to_page=i)
                recovered_pages += 1
            except Exception:
                failed_pages.append(i + 1)
                issues_found.append(f"Sayfa {i+1} hasarlı")

        if recovered_pages > 0:
            new_doc.set_metadata({
                'title': 'Onarılmış PDF',
                'creator': 'PDF Tools - Onarım Aracı',
                'producer': 'PyMuPDF'
            })

            new_doc.save(
                output_path,
                garbage=4,
                deflate=True,
                clean=True
            )

            issues_fixed.append("PDF yeniden oluşturuldu")
            issues_fixed.append("Gereksiz veriler temizlendi")
            issues_fixed.append("Dosya optimize edildi")

            original_size = os.path.getsize(input_path)
            repaired_size = os.path.getsize(output_path)

            return {
                'success': True,
                'pages_recovered': recovered_pages,
                'pages_failed': len(failed_pages),
                'failed_pages': failed_pages,
                'issues_found': issues_found,
                'issues_fixed': issues_fixed,
                'original_size': original_size,
                'repaired_size': repaired_size,
                'size_reduction': round((1 - repaired_size/original_size) * 100, 1) if original_size > 0 else 0
            }
        else:
            return {
                'success': False,
                'error': 'Hiçbir sayfa kurtarılamadı.',
                'issues_found': issues_found
            }

    except fitz.FileDataError:
        return try_deep_recovery(input_path, output_path)

    except Exception as e:
        logger.error(f"repair_pdf error: {e}", exc_info=True)
        return {
            'success': False,
            'error': 'Onarim hatasi',
            'issues_found': issues_found
        }

    finally:
        if new_doc:
            new_doc.close()
        if doc:
            doc.close()


def try_deep_recovery(input_path, output_path):
    """Deep recovery for severely corrupted PDFs"""
    issues_found = ["Ciddi bozulma tespit edildi"]
    issues_fixed = []
    doc = None
    new_doc = None

    try:
        with open(input_path, 'rb') as f:
            pdf_bytes = f.read()

        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            if len(doc) > 0:
                new_doc = fitz.open()
                recovered = 0

                for i in range(len(doc)):
                    try:
                        new_doc.insert_pdf(doc, from_page=i, to_page=i)
                        recovered += 1
                    except Exception:
                        pass

                if recovered > 0:
                    new_doc.save(output_path, garbage=4, deflate=True, clean=True)
                    issues_fixed.append("Derin kurtarma başarılı")
                    issues_fixed.append(f"{recovered} sayfa kurtarıldı")

                    original_size = os.path.getsize(input_path)
                    repaired_size = os.path.getsize(output_path)

                    return {
                        'success': True,
                        'pages_recovered': recovered,
                        'pages_failed': len(doc) - recovered,
                        'issues_found': issues_found,
                        'issues_fixed': issues_fixed,
                        'original_size': original_size,
                        'repaired_size': repaired_size,
                        'deep_recovery': True
                    }
        except Exception:
            pass
        finally:
            if new_doc:
                new_doc.close()
            if doc:
                doc.close()

        return {
            'success': False,
            'error': 'PDF çok hasarlı, kurtarılamadı.',
            'issues_found': issues_found
        }

    except Exception as e:
        logger.error(f"try_deep_recovery error: {e}", exc_info=True)
        return {
            'success': False,
            'error': 'Derin kurtarma hatasi',
            'issues_found': issues_found
        }


def analyze_pdf(pdf_path):
    """Analyze a PDF file for issues without repairing"""
    issues = []
    warnings = []
    info = {}
    doc = None

    try:
        doc = fitz.open(pdf_path)

        info['page_count'] = len(doc)
        info['is_encrypted'] = doc.is_encrypted
        info['needs_pass'] = doc.needs_pass

        metadata = doc.metadata
        info['title'] = metadata.get('title', '')
        info['author'] = metadata.get('author', '')
        info['creator'] = metadata.get('creator', '')
        info['producer'] = metadata.get('producer', '')
        info['creation_date'] = metadata.get('creationDate', '')
        info['mod_date'] = metadata.get('modDate', '')

        if doc.is_encrypted:
            warnings.append("PDF şifreli")

        if info['page_count'] == 0:
            issues.append("Sayfa yok")

        for i in range(len(doc)):
            try:
                page = doc[i]
                _ = page.get_text()
            except Exception:
                issues.append(f"Sayfa {i+1} hasarlı olabilir")

        info['file_size'] = os.path.getsize(pdf_path)

        return {
            'success': True,
            'info': info,
            'issues': issues,
            'warnings': warnings,
            'needs_repair': len(issues) > 0,
            'health': 'good' if len(issues) == 0 else ('warning' if len(issues) < 3 else 'bad')
        }

    except fitz.FileDataError:
        return {
            'success': True,
            'issues': ["PDF dosyası ciddi şekilde bozuk"],
            'warnings': [],
            'needs_repair': True,
            'health': 'critical',
            'info': {'file_size': os.path.getsize(pdf_path)}
        }

    except Exception as e:
        logger.error(f"analyze_pdf error: {e}", exc_info=True)
        return {
            'success': False,
            'error': 'Islem basarisiz'
        }

    finally:
        if doc:
            doc.close()
