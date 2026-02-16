"""
PDF to Excel Tool - PDF tablolarini Excel'e donustur
"""
import pdfplumber
from openpyxl import Workbook
import logging

logger = logging.getLogger(__name__)


def pdf_to_excel(input_path, output_path):
    """
    PDF icerisindeki tablolari Excel dosyasina donustur

    Args:
        input_path (str): Girdi PDF yolu
        output_path (str): Cikti XLSX yolu

    Returns:
        dict: Islem sonucu
    """
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sayfa 1"

        total_tables = 0
        total_rows = 0
        current_row = 1

        with pdfplumber.open(input_path) as pdf:
            for page_idx, page in enumerate(pdf.pages):
                tables = page.extract_tables()

                if not tables:
                    # Tablo yoksa metni cikar
                    text = page.extract_text()
                    if text:
                        if page_idx > 0:
                            # Yeni sayfa icin sheet ekle
                            ws = wb.create_sheet(title=f"Sayfa {page_idx + 1}")
                            current_row = 1
                        for line in text.split('\n'):
                            ws.cell(row=current_row, column=1, value=line.strip())
                            current_row += 1
                            total_rows += 1
                    continue

                for table_idx, table in enumerate(tables):
                    total_tables += 1

                    if page_idx > 0 or table_idx > 0:
                        sheet_name = f"Sayfa {page_idx + 1}"
                        if table_idx > 0:
                            sheet_name += f" - Tablo {table_idx + 1}"
                        ws = wb.create_sheet(title=sheet_name[:31])
                        current_row = 1

                    for row in table:
                        if row is None:
                            continue
                        for col_idx, cell in enumerate(row):
                            value = cell if cell else ''
                            # Sayi donusumu dene
                            try:
                                if '.' in str(value) or ',' in str(value):
                                    value = float(str(value).replace(',', '.'))
                                else:
                                    value = int(value)
                            except (ValueError, TypeError):
                                pass
                            ws.cell(row=current_row, column=col_idx + 1, value=value)
                        current_row += 1
                        total_rows += 1

        # Ilk default bos sheet'i kaldir (varsa)
        if 'Sheet' in wb.sheetnames and len(wb.sheetnames) > 1:
            del wb['Sheet']

        wb.save(output_path)

        return {
            'success': True,
            'message': f'{total_tables} tablo, {total_rows} satır çıkarıldı',
            'tables_found': total_tables,
            'total_rows': total_rows,
            'page_count': len(wb.sheetnames)
        }

    except Exception as e:
        logger.error(f"pdf_to_excel error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
