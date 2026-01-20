"""
PDFEdit - Hafif Ceviri Sistemi
Flask-Babel yerine ozel hafif sistem (~200 UI string, 2 dil).
"""

SUPPORTED_LANGUAGES = ['tr', 'en']
DEFAULT_LANGUAGE = 'tr'

TRANSLATIONS = {
    'tr': {
        # Genel
        'nav_home': 'Ana Sayfa',
        'nav_tools': 'Araclar',
        'nav_blog': 'Blog',
        'all_tools_ready': 'Tum araclar hazir',
        'search_placeholder': 'Arac ara... (birlestir, sikistir, filigran...)',
        'search_no_results': 'Aradiginiz arac bulunamadi',
        'footer_tagline': 'Hiz ve guvenilirlik icin tasarlandi',
        'trust_auto_delete': 'Dosyalariniz 1 saat icinde otomatik silinir',
        'trust_no_share': 'Verileriniz ucuncu taraflarla paylasilmaz',
        'trust_server_side': 'Tum islemler sunucuda gerceklesir',
        'try_also': 'Bunlari da deneyin:',

        # Cookie consent
        'cookie_message': 'Bu site deneyiminizi iyilestirmek icin cerez kullanir.',
        'cookie_accept': 'Kabul Et',
        'cookie_reject': 'Reddet',
        'cookie_learn_more': 'Daha Fazla Bilgi',

        # Ortak UI
        'upload_file': 'PDF dosyasini secin veya surukleyin',
        'upload_drag': 'veya tiklayarak secin',
        'upload_limit': 'Maksimum 100 MB',
        'upload_limit_multi': 'Maksimum 100 MB / dosya - Birden fazla dosya secebilirsiniz',
        'download': 'Indir',
        'download_zip': 'Tumunu ZIP Olarak Indir',
        'download_all': 'Tumunu Indir',
        'processing': 'Isleniyor...',
        'uploading': 'Yukleniyor...',
        'uploading_pct': 'Yukleniyor... {pct}%',
        'error': 'Hata',
        'error_generic': 'Bir hata olustu',
        'error_file_required': 'PDF dosyasi gerekli!',
        'error_file_too_large': 'Dosya cok buyuk! Maksimum: {size}',
        'error_invalid_file': 'Gecersiz dosya turu',
        'success': 'Basarili',
        'cancel': 'Iptal',
        'save': 'Kaydet',
        'reset': 'Sifirla',
        'close': 'Kapat',
        'back': 'Geri',
        'next': 'Ileri',
        'loading': 'Yukleniyor...',
        'ready': 'Hazir',
        'remove': 'Kaldir',
        'total': 'Toplam',
        'files_selected': '{count} dosya secildi',
        'page': 'Sayfa',
        'pages': 'Sayfa',
        'of': '/',

        # Step labels
        'step_upload': 'Yukle',
        'step_configure': 'Ayarla',
        'step_download': 'Indir',
        'step_process': 'Isle',

        # Merge
        'merge_title': 'PDF Birlestirme',
        'merge_subtitle': 'Birden fazla PDF dosyasini tek bir dosyada birlestirin',
        'merge_btn': 'Birlestir',
        'merge_btn_loading': 'Birlestiriliyor...',
        'merge_complete': 'Birlestirme Tamamlandi!',
        'merge_success_msg': '{count} dosya basariyla birlestirildi.',
        'merge_min_files': 'En az 2 PDF dosyasi gerekli!',
        'merge_drag_files': 'PDF dosyalarini surukleyin',
        'merge_reorder_hint': 'Siralamayi degistirmek icin dosyalari surukleyip birakin',
        'merge_output_name': 'Cikti Dosya Adi (istege bagli)',
        'step_sort': 'Sirala',

        # Split
        'split_title': 'PDF Bolme',
        'split_subtitle': 'PDF dosyalarini sayfalara veya araliklara gore bolun',
        'split_btn': 'Bol',
        'split_btn_loading': 'Bolunuyor...',
        'split_complete': 'Bolme Tamamlandi!',
        'split_files_created': '{count} dosya olusturuldu',
        'split_mode': 'Bolme Modu',
        'split_all': 'Tum Sayfalari Ayir',
        'split_range': 'Sayfa Araligi',
        'split_range_label': 'Sayfa Araligi',
        'split_range_hint': 'Ornek: 1-5, 8-10',
        'split_prefix': 'Dosya Adi Oneki (istege bagli)',
        'step_split': 'Bol',

        # Encrypt
        'encrypt_title': 'PDF Sifreleme',
        'encrypt_subtitle': 'PDF dosyalarinizi sifre ile koruyun veya sifresini cozun',
        'encrypt_btn': 'Sifrele',
        'encrypt_btn_loading': 'Sifreleniyor...',
        'decrypt_btn': 'Sifre Coz',
        'decrypt_btn_loading': 'Cozuluyor...',
        'encrypt_complete': 'Sifreleme Tamamlandi!',
        'decrypt_complete': 'Sifre Cozme Tamamlandi!',
        'encrypt_password': 'Sifre',
        'encrypt_password_required': 'Sifre gerekli!',
        'encrypt_allow_print': 'Yazdirma Izni',
        'encrypt_allow_copy': 'Kopyalama Izni',
        'encrypt_allow_modify': 'Duzenleme Izni',
        'password_weak': 'Zayif',
        'password_medium': 'Orta',
        'password_strong': 'Guclu',
        'tab_encrypt': 'Sifrele',
        'tab_decrypt': 'Sifre Coz',

        # Compress
        'compress_title': 'PDF Sikistirma',
        'compress_subtitle': 'PDF dosya boyutunu kucultun',
        'compress_btn': 'Sikistir',
        'compress_btn_loading': 'Sikistiriliyor...',
        'compress_complete': 'Sikistirma Tamamlandi!',
        'compress_quality': 'Sikistirma Kalitesi',
        'compress_high': 'Yuksek Kalite',
        'compress_high_desc': 'Az sikistirma, en iyi gorsel kalitesi',
        'compress_medium': 'Orta Kalite',
        'compress_medium_desc': 'Dengeli sikistirma, iyi sonuc',
        'compress_low': 'Dusuk Kalite',
        'compress_low_desc': 'Maksimum sikistirma, en kucuk boyut',
        'compress_original': 'Orijinal Boyut',
        'compress_new': 'Yeni Boyut',
        'compress_already_optimized': 'Dosya zaten optimize edilmis gorunuyor. Sikistirma orani dusuk.',
        'compress_images': 'Sikistirilan Gorsel',
        'step_compress': 'Sikistir',

        # Watermark
        'watermark_title': 'PDF Filigran Ekleme',
        'watermark_subtitle': 'PDF dosyalariniza metin veya gorsel filigran ekleyin',
        'watermark_btn': 'Filigran Ekle',
        'watermark_btn_loading': 'Ekleniyor...',
        'watermark_complete': 'Filigran Eklendi!',
        'watermark_text': 'Filigran Metni',
        'watermark_position': 'Konum',
        'watermark_opacity': 'Seffaflik',
        'watermark_font_size': 'Font Boyutu',
        'watermark_rotation': 'Dondurme Acisi',
        'watermark_color': 'Renk',
        'tab_text_watermark': 'Metin Filigran',
        'tab_image_watermark': 'Gorsel Filigran',
        'pos_center': 'Merkez',
        'pos_top_left': 'Ust Sol',
        'pos_top_right': 'Ust Sag',
        'pos_bottom_left': 'Alt Sol',
        'pos_bottom_right': 'Alt Sag',

        # Rotate
        'rotate_title': 'PDF Dondurme',
        'rotate_subtitle': 'PDF sayfalarini 90, 180 veya 270 derece dondurun',
        'rotate_btn': 'Dondur',
        'rotate_btn_loading': 'Donduruluyor...',
        'rotate_complete': 'Dondurme Tamamlandi!',
        'rotate_angle': 'Dondurme Acisi',
        'rotate_pages': 'Sayfalar',
        'rotate_all': 'Tum Sayfalar',
        'rotate_specific': 'Belirli Sayfalar',
        'step_rotate': 'Dondur',

        # Extract Text
        'extract_text_title': 'PDF Metin Cikarma',
        'extract_text_subtitle': "PDF'den tum metni cikarin ve kopyalayin",
        'extract_text_btn': 'Metni Cikar',
        'extract_text_btn_loading': 'Cikariliyor...',
        'extract_text_complete': 'Metin Cikarildi!',
        'extract_text_copy': 'Kopyala',
        'extract_text_download': 'TXT Olarak Indir',
        'extract_text_chars': 'Karakter',
        'extract_text_words': 'Kelime',

        # Extract Images
        'extract_images_title': 'PDF Gorsel Cikarma',
        'extract_images_subtitle': "PDF'deki tum gorselleri cikarin ve indirin",
        'extract_images_btn': 'Gorselleri Cikar',
        'extract_images_btn_loading': 'Cikariliyor...',
        'extract_images_complete': 'Gorseller Cikarildi!',
        'extract_images_count': '{count} gorsel bulundu',
        'extract_images_no_images': 'Gorsel bulunamadi',

        # Image to PDF
        'img_to_pdf_title': "Gorsel'den PDF'e Donusturme",
        'img_to_pdf_subtitle': 'Gorselleri PDF belgesine donusturun',
        'img_to_pdf_btn': 'Donustur',
        'img_to_pdf_btn_loading': 'Donusturuluyor...',
        'img_to_pdf_complete': 'Donusturme Tamamlandi!',
        'img_to_pdf_drag': 'Gorsel dosyalarini surukleyin',

        # PDF to Image
        'pdf_to_image_title': "PDF'den Gorsel'e Donusturme",
        'pdf_to_image_subtitle': "PDF sayfalarini PNG, JPG veya WebP'ye donusturun",
        'pdf_to_image_btn': 'Donustur',
        'pdf_to_image_btn_loading': 'Donusturuluyor...',
        'pdf_to_image_complete': 'Donusturme Tamamlandi!',
        'pdf_to_image_format': 'Gorsel Formati',
        'pdf_to_image_dpi': 'Cozunurluk (DPI)',

        # HTML to PDF
        'html_to_pdf_title': "HTML'den PDF'e Donusturme",
        'html_to_pdf_subtitle': "HTML kodunu veya web sayfasini PDF'e donusturun",
        'html_to_pdf_btn': 'Donustur',
        'html_to_pdf_btn_loading': 'Donusturuluyor...',
        'html_to_pdf_complete': 'Donusturme Tamamlandi!',
        'html_to_pdf_source': 'Kaynak',
        'html_to_pdf_html_code': 'HTML Kodu',
        'html_to_pdf_url': 'Web Sayfasi URL',
        'html_to_pdf_page_size': 'Sayfa Boyutu',
        'html_to_pdf_margin': 'Kenar Boslugu (mm)',
        'html_to_pdf_orientation': 'Yonlendirme',
        'html_to_pdf_portrait': 'Dikey',
        'html_to_pdf_landscape': 'Yatay',
        'html_to_pdf_output_name': 'Cikti Dosya Adi',
        'tab_html': 'HTML Kodu',
        'tab_url': 'URL',

        # Reorder
        'reorder_title': 'PDF Sayfa Siralama',
        'reorder_subtitle': 'Surukle-birak ile PDF sayfalarini yeniden siralayin',
        'reorder_btn': 'Kaydet',
        'reorder_btn_loading': 'Kaydediliyor...',
        'reorder_complete': 'Siralama Kaydedildi!',

        # Repair
        'repair_title': 'PDF Onarma',
        'repair_subtitle': 'Bozuk veya hasarli PDF dosyalarini onarin',
        'repair_analyze': 'Analiz Et',
        'repair_btn': 'Onar',
        'repair_btn_loading': 'Onariliyor...',
        'repair_complete': 'Onarim Tamamlandi!',

        # Metadata
        'metadata_title': 'PDF Metadata Duzenleyici',
        'metadata_subtitle': 'PDF meta bilgilerini goruntuleyin, duzenleyin veya temizleyin',
        'metadata_btn_update': 'Guncelle',
        'metadata_btn_clear': 'Tum Metadata\'yi Temizle',
        'metadata_complete': 'Metadata Guncellendi!',

        # Numbering
        'numbering_title': 'PDF Sayfa Numaralandirma',
        'numbering_subtitle': 'PDF sayfalarina ozellestirilmis numara ekleyin',
        'numbering_btn': 'Numarala',
        'numbering_btn_loading': 'Numaralandiriliyor...',
        'numbering_complete': 'Numaralandirma Tamamlandi!',
        'numbering_position': 'Numara Konumu',
        'numbering_format': 'Format',
        'numbering_start': 'Baslangic Numarasi',
        'numbering_skip_first': 'Ilk sayfayi atla',
        'numbering_font_size': 'Font Boyutu',

        # Logo Removal
        'logo_removal_title': 'AI Logo Silme',
        'logo_removal_subtitle': 'Yapay zeka ile PDF\'lerden logo ve filigran kaldirma',

        # Crop
        'crop_title': 'PDF Kirpma',
        'crop_subtitle': 'PDF sayfalarinin kenar bosluklarini ayarlayin veya otomatik kirpin',
        'crop_btn': 'Kirp',
        'crop_btn_loading': 'Kirpiliyor...',
        'crop_complete': 'Kirpma Tamamlandi!',
        'crop_mode_manual': 'Manuel Kirpma',
        'crop_mode_auto': 'Otomatik Kirpma',
        'crop_top': 'Ust',
        'crop_bottom': 'Alt',
        'crop_left': 'Sol',
        'crop_right': 'Sag',
        'crop_margin_px': 'piksel',
        'crop_auto_desc': 'Beyaz kenarlari otomatik tespit edip kirpar',
        'step_crop': 'Kirp',

        # Compare
        'compare_title': 'PDF Karsilastirma',
        'compare_subtitle': 'Iki PDF dosyasini sayfa sayfa karsilastirin',
        'compare_btn': 'Karsilastir',
        'compare_btn_loading': 'Karsilastiriliyor...',
        'compare_complete': 'Karsilastirma Tamamlandi!',
        'compare_file1': 'Birinci PDF',
        'compare_file2': 'Ikinci PDF',
        'compare_identical': 'Ayni',
        'compare_different': 'Farkli',
        'compare_only_first': 'Sadece 1. dosyada',
        'compare_only_second': 'Sadece 2. dosyada',
        'compare_pages_diff': '{count} sayfada fark bulundu',
        'compare_no_diff': 'Iki dosya arasinda fark bulunamadi',
        'compare_visual_diff': 'Gorsel Fark',
        'compare_text_diff': 'Metin Farklari',

        # PDF to Excel
        'pdf_to_excel_title': 'PDF\'den Excel\'e Donusturme',
        'pdf_to_excel_subtitle': 'PDF tablolarini Excel dosyasina donusturun',
        'pdf_to_excel_btn': 'Donustur',
        'pdf_to_excel_btn_loading': 'Donusturuluyor...',
        'pdf_to_excel_complete': 'Donusturme Tamamlandi!',
        'pdf_to_excel_tables': 'Bulunan Tablo',
        'pdf_to_excel_rows': 'Toplam Satir',

        # Form Fill
        'form_fill_title': 'PDF Form Doldurma',
        'form_fill_subtitle': 'PDF form alanlarini cevrimici doldurun',
        'form_fill_btn': 'Formu Indir',
        'form_fill_btn_loading': 'Hazirlaniyor...',
        'form_fill_complete': 'Form Dolduruldu!',
        'form_fill_detect': 'Alanlari Tespit Et',
        'form_fill_detecting': 'Tespit ediliyor...',
        'form_fill_fields_found': '{count} form alani bulundu',
        'form_fill_no_fields': 'Form alani bulunamadi',
        'form_fill_field_name': 'Alan Adi',
        'form_fill_field_type': 'Tur',
        'form_fill_field_value': 'Deger',

        # PDF to Word
        'pdf_to_word_title': 'PDF\'den Word\'e Donusturme',
        'pdf_to_word_subtitle': 'PDF dosyalarini Word belgesine donusturun',
        'pdf_to_word_btn': 'Donustur',
        'pdf_to_word_btn_loading': 'Donusturuluyor...',
        'pdf_to_word_complete': 'Donusturme Tamamlandi!',

        # PDF/A
        'pdf_to_pdfa_title': 'PDF/A Donusturme',
        'pdf_to_pdfa_subtitle': 'PDF dosyalarini arsivleme standardi PDF/A formatina donusturun',
        'pdf_to_pdfa_btn': 'Donustur',
        'pdf_to_pdfa_btn_loading': 'Donusturuluyor...',
        'pdf_to_pdfa_complete': 'Donusturme Tamamlandi!',
        'pdf_to_pdfa_version': 'PDF/A Surumu',

        # Blog
        'blog_title': 'Blog',
        'blog_read_more': 'Devamini Oku',
        'blog_back': 'Blog\'a Don',
        'blog_related_tool': 'Ilgili Arac',
        'blog_published': 'Yayinlanma',
        'blog_no_posts': 'Henuz yazi yok.',
        'blog_min_read': 'dk okuma',

        # Error pages
        'error_404': 'Sayfa bulunamadi',
        'error_413': 'Dosya cok buyuk!',
        'error_500': 'Sunucu hatasi olustu',
        'error_go_home': 'Ana Sayfaya Don',

        # Categories
        'cat_edit': 'Duzenle',
        'cat_edit_desc': 'PDF sayfalarini birlestirin, bolun, siralayin',
        'cat_convert': 'Donustur',
        'cat_convert_desc': 'Dosya formatlarini donusturun',
        'cat_security': 'Guvenlik',
        'cat_security_desc': "PDF'lerinizi koruyun ve metadatayi yonetin",
        'cat_extract': 'Cikar',
        'cat_extract_desc': 'PDF icinden metin ve gorselleri cikartin',
        'cat_optimize': 'Optimize',
        'cat_optimize_desc': "PDF'lerinizi iyilestirin ve onarim",
        'cat_ai': 'AI Araclar',
        'cat_ai_desc': 'Yapay zeka destekli araclar',

        # Tool tags
        'tag_popular': 'Populer',
        'tag_fast': 'Hizli',
        'tag_edit': 'Duzenle',
        'tag_easy': 'Kolay',
        'tag_convert': 'Donustur',
        'tag_new': 'Yeni',
        'tag_secure': 'Guvenli',
        'tag_pro': 'Pro',
        'tag_privacy': 'Gizlilik',
        'tag_extract': 'Cikarma',
        'tag_export': 'Disa Aktar',
        'tag_optimize': 'Optimize',
        'tag_recovery': 'Kurtarma',
        'tag_ai': 'AI Destekli',

        # How it works
        'how_it_works': 'Nasil Calisir?',
        'how_step_1': 'Yukle',
        'how_step_1_desc': 'PDF dosyanizi surukleyin veya secin',
        'how_step_2': 'Isle',
        'how_step_2_desc': 'Araci secin ve ayarlari yapin',
        'how_step_3': 'Indir',
        'how_step_3_desc': 'Islenmis dosyanizi aninda indirin',

        # Preview
        'preview': 'Onizleme',
        'preview_page': 'Sayfa',
        'preview_load_error': 'Onizleme yuklenemedi',
        'preview_error': 'Onizleme hatasi',
        'preview_page_info': '{count} sayfa',

        # FAQ
        'faq_title': 'Sikca Sorulan Sorular',
    },
    'en': {
        # General
        'nav_home': 'Home',
        'nav_tools': 'Tools',
        'nav_blog': 'Blog',
        'all_tools_ready': 'All tools ready',
        'search_placeholder': 'Search tools... (merge, compress, watermark...)',
        'search_no_results': 'No tools found',
        'footer_tagline': 'Designed for speed and reliability',
        'trust_auto_delete': 'Your files are automatically deleted within 1 hour',
        'trust_no_share': 'Your data is never shared with third parties',
        'trust_server_side': 'All processing happens on our server',
        'try_also': 'Try these too:',

        # Cookie consent
        'cookie_message': 'This site uses cookies to improve your experience.',
        'cookie_accept': 'Accept',
        'cookie_reject': 'Reject',
        'cookie_learn_more': 'Learn More',

        # Common UI
        'upload_file': 'Select or drag a PDF file',
        'upload_drag': 'or click to select',
        'upload_limit': 'Maximum 100 MB',
        'upload_limit_multi': 'Maximum 100 MB per file - You can select multiple files',
        'download': 'Download',
        'download_zip': 'Download All as ZIP',
        'download_all': 'Download All',
        'processing': 'Processing...',
        'uploading': 'Uploading...',
        'uploading_pct': 'Uploading... {pct}%',
        'error': 'Error',
        'error_generic': 'An error occurred',
        'error_file_required': 'PDF file is required!',
        'error_file_too_large': 'File too large! Maximum: {size}',
        'error_invalid_file': 'Invalid file type',
        'success': 'Success',
        'cancel': 'Cancel',
        'save': 'Save',
        'reset': 'Reset',
        'close': 'Close',
        'back': 'Back',
        'next': 'Next',
        'loading': 'Loading...',
        'ready': 'Ready',
        'remove': 'Remove',
        'total': 'Total',
        'files_selected': '{count} files selected',
        'page': 'Page',
        'pages': 'Pages',
        'of': '/',

        # Step labels
        'step_upload': 'Upload',
        'step_configure': 'Configure',
        'step_download': 'Download',
        'step_process': 'Process',

        # Merge
        'merge_title': 'Merge PDF',
        'merge_subtitle': 'Combine multiple PDF files into a single document',
        'merge_btn': 'Merge',
        'merge_btn_loading': 'Merging...',
        'merge_complete': 'Merge Complete!',
        'merge_success_msg': '{count} files successfully merged.',
        'merge_min_files': 'At least 2 PDF files required!',
        'merge_drag_files': 'Drag PDF files here',
        'merge_reorder_hint': 'Drag and drop files to change order',
        'merge_output_name': 'Output Filename (optional)',
        'step_sort': 'Sort',

        # Split
        'split_title': 'Split PDF',
        'split_subtitle': 'Split PDF files by pages or page ranges',
        'split_btn': 'Split',
        'split_btn_loading': 'Splitting...',
        'split_complete': 'Split Complete!',
        'split_files_created': '{count} files created',
        'split_mode': 'Split Mode',
        'split_all': 'Split All Pages',
        'split_range': 'Page Range',
        'split_range_label': 'Page Range',
        'split_range_hint': 'Example: 1-5, 8-10',
        'split_prefix': 'Filename Prefix (optional)',
        'step_split': 'Split',

        # Encrypt
        'encrypt_title': 'Encrypt PDF',
        'encrypt_subtitle': 'Protect your PDF files with a password or decrypt them',
        'encrypt_btn': 'Encrypt',
        'encrypt_btn_loading': 'Encrypting...',
        'decrypt_btn': 'Decrypt',
        'decrypt_btn_loading': 'Decrypting...',
        'encrypt_complete': 'Encryption Complete!',
        'decrypt_complete': 'Decryption Complete!',
        'encrypt_password': 'Password',
        'encrypt_password_required': 'Password is required!',
        'encrypt_allow_print': 'Allow Print',
        'encrypt_allow_copy': 'Allow Copy',
        'encrypt_allow_modify': 'Allow Modify',
        'password_weak': 'Weak',
        'password_medium': 'Medium',
        'password_strong': 'Strong',
        'tab_encrypt': 'Encrypt',
        'tab_decrypt': 'Decrypt',

        # Compress
        'compress_title': 'Compress PDF',
        'compress_subtitle': 'Reduce your PDF file size',
        'compress_btn': 'Compress',
        'compress_btn_loading': 'Compressing...',
        'compress_complete': 'Compression Complete!',
        'compress_quality': 'Compression Quality',
        'compress_high': 'High Quality',
        'compress_high_desc': 'Less compression, best visual quality',
        'compress_medium': 'Medium Quality',
        'compress_medium_desc': 'Balanced compression, good results',
        'compress_low': 'Low Quality',
        'compress_low_desc': 'Maximum compression, smallest size',
        'compress_original': 'Original Size',
        'compress_new': 'New Size',
        'compress_already_optimized': 'File appears already optimized. Compression ratio is low.',
        'compress_images': 'Compressed Images',
        'step_compress': 'Compress',

        # Watermark
        'watermark_title': 'Add Watermark to PDF',
        'watermark_subtitle': 'Add text or image watermarks to your PDF files',
        'watermark_btn': 'Add Watermark',
        'watermark_btn_loading': 'Adding...',
        'watermark_complete': 'Watermark Added!',
        'watermark_text': 'Watermark Text',
        'watermark_position': 'Position',
        'watermark_opacity': 'Opacity',
        'watermark_font_size': 'Font Size',
        'watermark_rotation': 'Rotation Angle',
        'watermark_color': 'Color',
        'tab_text_watermark': 'Text Watermark',
        'tab_image_watermark': 'Image Watermark',
        'pos_center': 'Center',
        'pos_top_left': 'Top Left',
        'pos_top_right': 'Top Right',
        'pos_bottom_left': 'Bottom Left',
        'pos_bottom_right': 'Bottom Right',

        # Rotate
        'rotate_title': 'Rotate PDF',
        'rotate_subtitle': 'Rotate PDF pages by 90, 180, or 270 degrees',
        'rotate_btn': 'Rotate',
        'rotate_btn_loading': 'Rotating...',
        'rotate_complete': 'Rotation Complete!',
        'rotate_angle': 'Rotation Angle',
        'rotate_pages': 'Pages',
        'rotate_all': 'All Pages',
        'rotate_specific': 'Specific Pages',
        'step_rotate': 'Rotate',

        # Extract Text
        'extract_text_title': 'Extract Text from PDF',
        'extract_text_subtitle': 'Extract all text from your PDF files',
        'extract_text_btn': 'Extract Text',
        'extract_text_btn_loading': 'Extracting...',
        'extract_text_complete': 'Text Extracted!',
        'extract_text_copy': 'Copy',
        'extract_text_download': 'Download as TXT',
        'extract_text_chars': 'Characters',
        'extract_text_words': 'Words',

        # Extract Images
        'extract_images_title': 'Extract Images from PDF',
        'extract_images_subtitle': 'Extract and download all images from PDF files',
        'extract_images_btn': 'Extract Images',
        'extract_images_btn_loading': 'Extracting...',
        'extract_images_complete': 'Images Extracted!',
        'extract_images_count': '{count} images found',
        'extract_images_no_images': 'No images found',

        # Image to PDF
        'img_to_pdf_title': 'Image to PDF Converter',
        'img_to_pdf_subtitle': 'Convert images to PDF documents',
        'img_to_pdf_btn': 'Convert',
        'img_to_pdf_btn_loading': 'Converting...',
        'img_to_pdf_complete': 'Conversion Complete!',
        'img_to_pdf_drag': 'Drag image files here',

        # PDF to Image
        'pdf_to_image_title': 'PDF to Image Converter',
        'pdf_to_image_subtitle': 'Convert PDF pages to PNG, JPG, or WebP images',
        'pdf_to_image_btn': 'Convert',
        'pdf_to_image_btn_loading': 'Converting...',
        'pdf_to_image_complete': 'Conversion Complete!',
        'pdf_to_image_format': 'Image Format',
        'pdf_to_image_dpi': 'Resolution (DPI)',

        # HTML to PDF
        'html_to_pdf_title': 'HTML to PDF Converter',
        'html_to_pdf_subtitle': 'Convert HTML code or webpage URL to PDF',
        'html_to_pdf_btn': 'Convert',
        'html_to_pdf_btn_loading': 'Converting...',
        'html_to_pdf_complete': 'Conversion Complete!',
        'html_to_pdf_source': 'Source',
        'html_to_pdf_html_code': 'HTML Code',
        'html_to_pdf_url': 'Webpage URL',
        'html_to_pdf_page_size': 'Page Size',
        'html_to_pdf_margin': 'Margin (mm)',
        'html_to_pdf_orientation': 'Orientation',
        'html_to_pdf_portrait': 'Portrait',
        'html_to_pdf_landscape': 'Landscape',
        'html_to_pdf_output_name': 'Output Filename',
        'tab_html': 'HTML Code',
        'tab_url': 'URL',

        # Reorder
        'reorder_title': 'Reorder PDF Pages',
        'reorder_subtitle': 'Rearrange PDF pages with drag and drop',
        'reorder_btn': 'Save',
        'reorder_btn_loading': 'Saving...',
        'reorder_complete': 'Pages Reordered!',

        # Repair
        'repair_title': 'Repair PDF',
        'repair_subtitle': 'Repair corrupted or damaged PDF files',
        'repair_analyze': 'Analyze',
        'repair_btn': 'Repair',
        'repair_btn_loading': 'Repairing...',
        'repair_complete': 'Repair Complete!',

        # Metadata
        'metadata_title': 'PDF Metadata Editor',
        'metadata_subtitle': 'View, edit, or remove PDF metadata',
        'metadata_btn_update': 'Update',
        'metadata_btn_clear': 'Clear All Metadata',
        'metadata_complete': 'Metadata Updated!',

        # Numbering
        'numbering_title': 'Add Page Numbers to PDF',
        'numbering_subtitle': 'Add customizable page numbers to your PDF files',
        'numbering_btn': 'Number Pages',
        'numbering_btn_loading': 'Numbering...',
        'numbering_complete': 'Numbering Complete!',
        'numbering_position': 'Number Position',
        'numbering_format': 'Format',
        'numbering_start': 'Start Number',
        'numbering_skip_first': 'Skip first page',
        'numbering_font_size': 'Font Size',

        # Logo Removal
        'logo_removal_title': 'AI Logo Removal',
        'logo_removal_subtitle': 'Remove logos and watermarks from PDF files with AI',

        # Crop
        'crop_title': 'Crop PDF',
        'crop_subtitle': 'Adjust page margins or auto-crop white borders',
        'crop_btn': 'Crop',
        'crop_btn_loading': 'Cropping...',
        'crop_complete': 'Cropping Complete!',
        'crop_mode_manual': 'Manual Crop',
        'crop_mode_auto': 'Auto Crop',
        'crop_top': 'Top',
        'crop_bottom': 'Bottom',
        'crop_left': 'Left',
        'crop_right': 'Right',
        'crop_margin_px': 'pixels',
        'crop_auto_desc': 'Automatically detect and remove white borders',
        'step_crop': 'Crop',

        # Compare
        'compare_title': 'Compare PDF',
        'compare_subtitle': 'Compare two PDF files page by page',
        'compare_btn': 'Compare',
        'compare_btn_loading': 'Comparing...',
        'compare_complete': 'Comparison Complete!',
        'compare_file1': 'First PDF',
        'compare_file2': 'Second PDF',
        'compare_identical': 'Identical',
        'compare_different': 'Different',
        'compare_only_first': 'Only in file 1',
        'compare_only_second': 'Only in file 2',
        'compare_pages_diff': '{count} pages with differences found',
        'compare_no_diff': 'No differences found between the two files',
        'compare_visual_diff': 'Visual Difference',
        'compare_text_diff': 'Text Differences',

        # PDF to Excel
        'pdf_to_excel_title': 'PDF to Excel Converter',
        'pdf_to_excel_subtitle': 'Convert PDF tables to Excel files',
        'pdf_to_excel_btn': 'Convert',
        'pdf_to_excel_btn_loading': 'Converting...',
        'pdf_to_excel_complete': 'Conversion Complete!',
        'pdf_to_excel_tables': 'Tables Found',
        'pdf_to_excel_rows': 'Total Rows',

        # Form Fill
        'form_fill_title': 'Fill PDF Forms',
        'form_fill_subtitle': 'Fill PDF form fields online',
        'form_fill_btn': 'Download Form',
        'form_fill_btn_loading': 'Preparing...',
        'form_fill_complete': 'Form Filled!',
        'form_fill_detect': 'Detect Fields',
        'form_fill_detecting': 'Detecting...',
        'form_fill_fields_found': '{count} form fields found',
        'form_fill_no_fields': 'No form fields found',
        'form_fill_field_name': 'Field Name',
        'form_fill_field_type': 'Type',
        'form_fill_field_value': 'Value',

        # PDF to Word
        'pdf_to_word_title': 'PDF to Word Converter',
        'pdf_to_word_subtitle': 'Convert PDF files to Word documents',
        'pdf_to_word_btn': 'Convert',
        'pdf_to_word_btn_loading': 'Converting...',
        'pdf_to_word_complete': 'Conversion Complete!',

        # PDF/A
        'pdf_to_pdfa_title': 'PDF to PDF/A Converter',
        'pdf_to_pdfa_subtitle': 'Convert PDF files to archival PDF/A format',
        'pdf_to_pdfa_btn': 'Convert',
        'pdf_to_pdfa_btn_loading': 'Converting...',
        'pdf_to_pdfa_complete': 'Conversion Complete!',
        'pdf_to_pdfa_version': 'PDF/A Version',

        # Blog
        'blog_title': 'Blog',
        'blog_read_more': 'Read More',
        'blog_back': 'Back to Blog',
        'blog_related_tool': 'Related Tool',
        'blog_published': 'Published',
        'blog_no_posts': 'No posts yet.',
        'blog_min_read': 'min read',

        # Error pages
        'error_404': 'Page not found',
        'error_413': 'File too large!',
        'error_500': 'Server error occurred',
        'error_go_home': 'Go to Home Page',

        # Categories
        'cat_edit': 'Edit',
        'cat_edit_desc': 'Merge, split, and organize PDF pages',
        'cat_convert': 'Convert',
        'cat_convert_desc': 'Convert between file formats',
        'cat_security': 'Security',
        'cat_security_desc': 'Protect your PDFs and manage metadata',
        'cat_extract': 'Extract',
        'cat_extract_desc': 'Extract text and images from PDFs',
        'cat_optimize': 'Optimize',
        'cat_optimize_desc': 'Improve and repair your PDFs',
        'cat_ai': 'AI Tools',
        'cat_ai_desc': 'AI-powered tools',

        # Tool tags
        'tag_popular': 'Popular',
        'tag_fast': 'Fast',
        'tag_edit': 'Edit',
        'tag_easy': 'Easy',
        'tag_convert': 'Convert',
        'tag_new': 'New',
        'tag_secure': 'Secure',
        'tag_pro': 'Pro',
        'tag_privacy': 'Privacy',
        'tag_extract': 'Extract',
        'tag_export': 'Export',
        'tag_optimize': 'Optimize',
        'tag_recovery': 'Recovery',
        'tag_ai': 'AI Powered',

        # How it works
        'how_it_works': 'How It Works',
        'how_step_1': 'Upload',
        'how_step_1_desc': 'Drag and drop or select your PDF file',
        'how_step_2': 'Process',
        'how_step_2_desc': 'Choose a tool and configure settings',
        'how_step_3': 'Download',
        'how_step_3_desc': 'Download your processed file instantly',

        # Preview
        'preview': 'Preview',
        'preview_page': 'Page',
        'preview_load_error': 'Preview could not be loaded',
        'preview_error': 'Preview error',
        'preview_page_info': '{count} pages',

        # FAQ
        'faq_title': 'Frequently Asked Questions',
    }
}


def get_translator(lang):
    """Sablon icin ceviri fonksiyonu dondurur"""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])

    def translate(key, **kwargs):
        text = translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, IndexError):
                return text
        return text

    return translate


def get_js_translations(lang):
    """JS tarafinda kullanilacak cevirileri dondurur (sadece gerekli olanlar)"""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])
    # JS'de kullanilacak anahtar onekleri
    js_keys = [
        'upload', 'download', 'processing', 'uploading', 'error', 'success',
        'cancel', 'loading', 'remove', 'total', 'files_selected',
        'page', 'pages', 'of', 'try_also', 'ready',
        'merge_', 'split_', 'compress_', 'encrypt_', 'decrypt_',
        'watermark_', 'rotate_', 'extract_', 'img_to_pdf_',
        'pdf_to_image_', 'html_to_pdf_', 'reorder_', 'repair_',
        'metadata_', 'numbering_', 'password_',
        'crop_', 'compare_', 'pdf_to_excel_', 'form_fill_',
        'pdf_to_word_', 'pdf_to_pdfa_', 'preview_',
    ]
    result = {}
    for key, val in translations.items():
        for prefix in js_keys:
            if key.startswith(prefix) or key == prefix.rstrip('_'):
                result[key] = val
                break
    return result
