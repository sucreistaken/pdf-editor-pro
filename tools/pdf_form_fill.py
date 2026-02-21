"""
PDF Form Fill Tool - PDF form alanlarini tespit et ve doldur
"""
import re
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)


def get_form_fields(input_path):
    """
    PDF form alanlarini tespit et

    Args:
        input_path (str): Girdi PDF yolu

    Returns:
        dict: Alan listesi ve bilgileri
    """
    doc = None
    try:
        doc = fitz.open(input_path)
        fields = []

        for page_num, page in enumerate(doc):
            widgets = page.widgets()
            if widgets is None:
                continue
            for widget in widgets:
                field_info = {
                    'name': widget.field_name or f'field_{len(fields)}',
                    'type': _widget_type_name(widget.field_type),
                    'type_id': widget.field_type,
                    'value': widget.field_value or '',
                    'page': page_num + 1,
                    'rect': list(widget.rect),
                }

                # Checkbox/radio icin secenekleri al
                if widget.field_type in (2, 5):  # Btn (checkbox/radio)
                    field_info['is_checkbox'] = True
                    field_info['on_value'] = _get_checkbox_on_value(doc, widget)

                # Combobox/listbox icin secenekleri al
                if widget.field_type in (3, 4):  # Ch (choice)
                    try:
                        field_info['choices'] = widget.choice_values or []
                    except Exception:
                        field_info['choices'] = []

                fields.append(field_info)

        return {
            'success': True,
            'fields': fields,
            'field_count': len(fields),
            'page_count': len(doc)
        }

    except Exception as e:
        logger.error(f"get_form_fields error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()


def fill_form(input_path, output_path, field_data, flatten=True):
    """
    PDF form alanlarini doldur

    Args:
        input_path (str): Girdi PDF yolu
        output_path (str): Cikti PDF yolu
        field_data (dict): {alan_adi: deger} eslesmesi
        flatten (bool): Formu duzlestir (duzenlemeyi kapat)

    Returns:
        dict: Islem sonucu
    """
    doc = None
    try:
        doc = fitz.open(input_path)
        filled_count = 0

        for page in doc:
            widgets = page.widgets()
            if widgets is None:
                continue
            for widget in widgets:
                field_name = widget.field_name
                if field_name and field_name in field_data:
                    value = field_data[field_name]

                    if widget.field_type in (2, 5):  # Checkbox/radio
                        on_value = _get_checkbox_on_value(doc, widget)
                        is_checked = value in ('true', 'True', True, '1', 'Yes', on_value)
                        widget.field_value = on_value if is_checked else 'Off'
                    else:
                        widget.field_value = str(value)

                    widget.update()
                    filled_count += 1

        if flatten:
            for page in doc:
                # Widget annotation'larini topla
                annot = page.first_annot
                widget_annots = []
                while annot:
                    if annot.type[0] == 20:  # PDF_ANNOT_WIDGET
                        widget_annots.append(annot)
                    annot = annot.next
                # Widget'lari sil (gorunumleri sayfa iceriginde kalir)
                for wa in widget_annots:
                    try:
                        page.delete_annot(wa)
                    except Exception:
                        pass

        doc.save(output_path, garbage=4, deflate=True)

        return {
            'success': True,
            'message': f'{filled_count} alan dolduruldu',
            'filled_count': filled_count,
            'page_count': len(doc)
        }

    except Exception as e:
        logger.error(f"fill_form error: {e}", exc_info=True)
        return {'success': False, 'error': 'İşlem başarısız'}
    finally:
        if doc:
            doc.close()


def _get_checkbox_on_value(doc, widget):
    """Widget'in gercek on-state degerini tespit et (Yes, 1, Checked vs.)"""
    try:
        xref = widget.xref
        ap_text = doc.xref_get_key(xref, "AP/N")
        if ap_text and ap_text[0] == "dict":
            states = re.findall(r'/(\w+)', ap_text[1])
            for s in states:
                if s != 'Off':
                    return s
    except Exception:
        pass
    return 'Yes'


def _widget_type_name(type_id):
    """Widget type ID'sini isme cevir"""
    type_map = {
        1: 'text',
        2: 'checkbox',
        3: 'combobox',
        4: 'listbox',
        5: 'radiobutton',
        6: 'pushbutton',
        7: 'signature',
    }
    return type_map.get(type_id, 'unknown')
