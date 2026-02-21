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
        'nav_tools': 'Araçlar',
        'nav_blog': 'Blog',
        'all_tools_ready': 'Tüm araçlar hazır',
        'search_placeholder': 'Araç ara... (birleştir, sıkıştır, filigran...)',
        'search_no_results': 'Aradığınız araç bulunamadı',
        'footer_tagline': 'Hız ve güvenilirlik için tasarlandı',
        'trust_auto_delete': 'Dosyalarınız 1 saat içinde otomatik silinir',
        'trust_no_share': 'Verileriniz üçüncü taraflarla paylaşılmaz',
        'trust_server_side': 'Tüm işlemler sunucuda gerçekleşir',
        'try_also': 'Bunları da deneyin:',

        # Cookie consent
        'cookie_message': 'Bu site deneyiminizi iyileştirmek için çerez kullanır.',
        'cookie_accept': 'Kabul Et',
        'cookie_reject': 'Reddet',
        'cookie_learn_more': 'Daha Fazla Bilgi',

        # Ortak UI
        'upload_file': 'PDF dosyasını seçin veya sürükleyin',
        'upload_drag': 'veya tıklayarak seçin',
        'upload_limit': 'Maksimum 100 MB',
        'upload_limit_multi': 'Maksimum 100 MB / dosya - Birden fazla dosya seçebilirsiniz',
        'download': 'İndir',
        'download_zip': 'Tümünü ZIP Olarak İndir',
        'download_all': 'Tümünü İndir',
        'processing': 'İşleniyor...',
        'uploading': 'Yükleniyor...',
        'uploading_pct': 'Yükleniyor... {pct}%',
        'error': 'Hata',
        'error_generic': 'Bir hata oluştu',
        'error_file_required': 'PDF dosyası gerekli!',
        'error_file_too_large': 'Dosya çok büyük! Maksimum: {size}',
        'error_invalid_file': 'Geçersiz dosya türü',
        'success': 'Başarılı',
        'cancel': 'İptal',
        'save': 'Kaydet',
        'reset': 'Sıfırla',
        'close': 'Kapat',
        'back': 'Geri',
        'next': 'İleri',
        'loading': 'Yükleniyor...',
        'ready': 'Hazır',
        'remove': 'Kaldır',
        'total': 'Toplam',
        'files_selected': '{count} dosya seçildi',
        'page': 'Sayfa',
        'pages': 'Sayfa',
        'of': '/',

        # Step labels
        'step_upload': 'Yükle',
        'step_configure': 'Ayarla',
        'step_download': 'İndir',
        'step_process': 'İşle',

        # Merge
        'merge_title': 'PDF Birleştirme',
        'merge_subtitle': 'Birden fazla PDF dosyasını tek bir dosyada birleştirin',
        'merge_btn': 'Birleştir',
        'merge_btn_loading': 'Birleştiriliyor...',
        'merge_complete': 'Birleştirme Tamamlandı!',
        'merge_success_msg': '{count} dosya başarıyla birleştirildi.',
        'merge_min_files': 'En az 2 PDF dosyası gerekli!',
        'merge_drag_files': 'PDF dosyalarını sürükleyin',
        'merge_reorder_hint': 'Sıralamayı değiştirmek için dosyaları sürükleyip bırakın',
        'merge_output_name': 'Çıktı Dosya Adı (isteğe bağlı)',
        'step_sort': 'Sırala',

        # Split
        'split_title': 'PDF Bölme',
        'split_subtitle': 'PDF dosyalarını sayfalara veya aralıklara göre bölün',
        'split_btn': 'Böl',
        'split_btn_loading': 'Bölünüyor...',
        'split_complete': 'Bölme Tamamlandı!',
        'split_files_created': '{count} dosya oluşturuldu',
        'split_mode': 'Bölme Modu',
        'split_all': 'Tüm Sayfaları Ayır',
        'split_range': 'Sayfa Aralığı',
        'split_range_label': 'Sayfa Aralığı',
        'split_range_hint': 'Örnek: 1-5, 8-10',
        'split_prefix': 'Dosya Adı Öneki (isteğe bağlı)',
        'step_split': 'Böl',

        # Encrypt
        'encrypt_title': 'PDF Şifreleme',
        'encrypt_subtitle': 'PDF dosyalarınızı şifre ile koruyun veya şifresini çözün',
        'encrypt_btn': 'Şifrele',
        'encrypt_btn_loading': 'Şifreleniyor...',
        'decrypt_btn': 'Şifre Çöz',
        'decrypt_btn_loading': 'Çözülüyor...',
        'encrypt_complete': 'Şifreleme Tamamlandı!',
        'decrypt_complete': 'Şifre Çözme Tamamlandı!',
        'encrypt_password': 'Şifre',
        'encrypt_password_required': 'Şifre gerekli!',
        'encrypt_allow_print': 'Yazdırma İzni',
        'encrypt_allow_copy': 'Kopyalama İzni',
        'encrypt_allow_modify': 'Düzenleme İzni',
        'password_weak': 'Zayıf',
        'password_medium': 'Orta',
        'password_strong': 'Güçlü',
        'tab_encrypt': 'Şifrele',
        'tab_decrypt': 'Şifre Çöz',

        # Compress
        'compress_title': 'PDF Sıkıştırma',
        'compress_subtitle': 'PDF dosya boyutunu küçültün',
        'compress_btn': 'Sıkıştır',
        'compress_btn_loading': 'Sıkıştırılıyor...',
        'compress_complete': 'Sıkıştırma Tamamlandı!',
        'compress_quality': 'Sıkıştırma Kalitesi',
        'compress_high': 'Yüksek Kalite',
        'compress_high_desc': 'Az sıkıştırma, en iyi görsel kalitesi',
        'compress_medium': 'Orta Kalite',
        'compress_medium_desc': 'Dengeli sıkıştırma, iyi sonuç',
        'compress_low': 'Düşük Kalite',
        'compress_low_desc': 'Maksimum sıkıştırma, en küçük boyut',
        'compress_original': 'Orijinal Boyut',
        'compress_new': 'Yeni Boyut',
        'compress_already_optimized': 'Dosya zaten optimize edilmiş görünüyor. Sıkıştırma oranı düşük.',
        'compress_images': 'Sıkıştırılan Görsel',
        'step_compress': 'Sıkıştır',

        # Watermark
        'watermark_title': 'PDF Filigran Ekleme',
        'watermark_subtitle': 'PDF dosyalarınıza metin veya görsel filigran ekleyin',
        'watermark_btn': 'Filigran Ekle',
        'watermark_btn_loading': 'Ekleniyor...',
        'watermark_complete': 'Filigran Eklendi!',
        'watermark_text': 'Filigran Metni',
        'watermark_position': 'Konum',
        'watermark_opacity': 'Şeffaflık',
        'watermark_font_size': 'Font Boyutu',
        'watermark_rotation': 'Döndürme Açısı',
        'watermark_color': 'Renk',
        'tab_text_watermark': 'Metin Filigran',
        'tab_image_watermark': 'Görsel Filigran',
        'pos_center': 'Merkez',
        'pos_top_left': 'Üst Sol',
        'pos_top_center': 'Üst Orta',
        'pos_top_right': 'Üst Sağ',
        'pos_bottom_left': 'Alt Sol',
        'pos_bottom_right': 'Alt Sağ',
        'watermark_scale': 'Boyut',

        # Rotate
        'rotate_title': 'PDF Döndürme',
        'rotate_subtitle': 'PDF sayfalarını 90, 180 veya 270 derece döndürün',
        'rotate_btn': 'Döndür',
        'rotate_btn_loading': 'Döndürülüyor...',
        'rotate_complete': 'Döndürme Tamamlandı!',
        'rotate_angle': 'Döndürme Açısı',
        'rotate_pages': 'Sayfalar',
        'rotate_all': 'Tüm Sayfalar',
        'rotate_specific': 'Belirli Sayfalar',
        'step_rotate': 'Döndür',

        # Extract Text
        'extract_text_title': 'PDF Metin Çıkarma',
        'extract_text_subtitle': "PDF'den tüm metni çıkarın ve kopyalayın",
        'extract_text_btn': 'Metni Çıkar',
        'extract_text_btn_loading': 'Çıkarılıyor...',
        'extract_text_complete': 'Metin Çıkarıldı!',
        'extract_text_copy': 'Kopyala',
        'extract_text_download': 'TXT Olarak İndir',
        'extract_text_chars': 'Karakter',
        'extract_text_words': 'Kelime',

        # Extract Images
        'extract_images_title': 'PDF Görsel Çıkarma',
        'extract_images_subtitle': "PDF'deki tüm görselleri çıkarın ve indirin",
        'extract_images_btn': 'Görselleri Çıkar',
        'extract_images_btn_loading': 'Çıkarılıyor...',
        'extract_images_complete': 'Görseller Çıkarıldı!',
        'extract_images_count': '{count} görsel bulundu',
        'extract_images_no_images': 'Görsel bulunamadı',

        # Image to PDF
        'img_to_pdf_title': "Görsel'den PDF'e Dönüştürme",
        'img_to_pdf_subtitle': 'Görselleri PDF belgesine dönüştürün',
        'img_to_pdf_btn': 'Dönüştür',
        'img_to_pdf_btn_loading': 'Dönüştürülüyor...',
        'img_to_pdf_complete': 'Dönüştürme Tamamlandı!',
        'img_to_pdf_drag': 'Görsel dosyalarını sürükleyin',

        # PDF to Image
        'pdf_to_image_title': "PDF'den Görsel'e Dönüştürme",
        'pdf_to_image_subtitle': "PDF sayfalarını PNG, JPG veya WebP'ye dönüştürün",
        'pdf_to_image_btn': 'Dönüştür',
        'pdf_to_image_btn_loading': 'Dönüştürülüyor...',
        'pdf_to_image_complete': 'Dönüştürme Tamamlandı!',
        'pdf_to_image_format': 'Görsel Formatı',
        'pdf_to_image_dpi': 'Çözünürlük (DPI)',

        # HTML to PDF
        'html_to_pdf_title': "HTML'den PDF'e Dönüştürme",
        'html_to_pdf_subtitle': "HTML kodunu veya web sayfasını PDF'e dönüştürün",
        'html_to_pdf_btn': 'Dönüştür',
        'html_to_pdf_btn_loading': 'Dönüştürülüyor...',
        'html_to_pdf_complete': 'Dönüştürme Tamamlandı!',
        'html_to_pdf_source': 'Kaynak',
        'html_to_pdf_html_code': 'HTML Kodu',
        'html_to_pdf_url': 'Web Sayfası URL',
        'html_to_pdf_page_size': 'Sayfa Boyutu',
        'html_to_pdf_margin': 'Kenar Boşluğu (mm)',
        'html_to_pdf_orientation': 'Yönlendirme',
        'html_to_pdf_portrait': 'Dikey',
        'html_to_pdf_landscape': 'Yatay',
        'html_to_pdf_output_name': 'Çıktı Dosya Adı',
        'tab_html': 'HTML Kodu',
        'tab_url': 'URL',

        # Reorder
        'reorder_title': 'PDF Sayfa Sıralama',
        'reorder_subtitle': 'Sürükle-bırak ile PDF sayfalarını yeniden sıralayın',
        'reorder_btn': 'Kaydet',
        'reorder_btn_loading': 'Kaydediliyor...',
        'reorder_complete': 'Sıralama Kaydedildi!',

        # Repair
        'repair_title': 'PDF Onarma',
        'repair_subtitle': 'Bozuk veya hasarlı PDF dosyalarını onarın',
        'repair_analyze': 'Analiz Et',
        'repair_btn': 'Onar',
        'repair_btn_loading': 'Onarılıyor...',
        'repair_complete': 'Onarım Tamamlandı!',

        # Metadata
        'metadata_title': 'PDF Metadata Düzenleyici',
        'metadata_subtitle': 'PDF meta bilgilerini görüntüleyin, düzenleyin veya temizleyin',
        'metadata_btn_update': 'Güncelle',
        'metadata_btn_clear': 'Tüm Metadata\'yı Temizle',
        'metadata_complete': 'Metadata Güncellendi!',

        # Numbering
        'numbering_title': 'PDF Sayfa Numaralandırma',
        'numbering_subtitle': 'PDF sayfalarına özelleştirilmiş numara ekleyin',
        'numbering_btn': 'Numarala',
        'numbering_btn_loading': 'Numaralandırılıyor...',
        'numbering_complete': 'Numaralandırma Tamamlandı!',
        'numbering_position': 'Numara Konumu',
        'numbering_format': 'Format',
        'numbering_start': 'Başlangıç Numarası',
        'numbering_skip_first': 'İlk sayfayı atla',
        'numbering_font_size': 'Font Boyutu',

        # Logo Removal
        'logo_removal_title': 'AI Logo Silme',
        'logo_removal_subtitle': 'Yapay zeka ile PDF\'lerden logo ve filigran kaldırma',

        # Crop
        'crop_title': 'PDF Kırpma',
        'crop_subtitle': 'PDF sayfalarının kenar boşluklarını ayarlayın veya otomatik kırpın',
        'crop_btn': 'Kırp',
        'crop_btn_loading': 'Kırpılıyor...',
        'crop_complete': 'Kırpma Tamamlandı!',
        'crop_mode_manual': 'Manuel Kırpma',
        'crop_mode_auto': 'Otomatik Kırpma',
        'crop_top': 'Üst',
        'crop_bottom': 'Alt',
        'crop_left': 'Sol',
        'crop_right': 'Sağ',
        'crop_margin_px': 'piksel',
        'crop_auto_desc': 'Beyaz kenarları otomatik tespit edip kırpar',
        'step_crop': 'Kırp',

        # Compare
        'compare_title': 'PDF Karşılaştırma',
        'compare_subtitle': 'İki PDF dosyasını sayfa sayfa karşılaştırın',
        'compare_btn': 'Karşılaştır',
        'compare_btn_loading': 'Karşılaştırılıyor...',
        'compare_complete': 'Karşılaştırma Tamamlandı!',
        'compare_file1': 'Birinci PDF',
        'compare_file2': 'İkinci PDF',
        'compare_identical': 'Aynı',
        'compare_different': 'Farklı',
        'compare_only_first': 'Sadece 1. dosyada',
        'compare_only_second': 'Sadece 2. dosyada',
        'compare_pages_diff': '{count} sayfada fark bulundu',
        'compare_no_diff': 'İki dosya arasında fark bulunamadı',
        'compare_visual_diff': 'Görsel Fark',
        'compare_text_diff': 'Metin Farkları',

        # PDF to Excel
        'pdf_to_excel_title': 'PDF\'den Excel\'e Dönüştürme',
        'pdf_to_excel_subtitle': 'PDF tablolarını Excel dosyasına dönüştürün',
        'pdf_to_excel_btn': 'Dönüştür',
        'pdf_to_excel_btn_loading': 'Dönüştürülüyor...',
        'pdf_to_excel_complete': 'Dönüştürme Tamamlandı!',
        'pdf_to_excel_tables': 'Bulunan Tablo',
        'pdf_to_excel_rows': 'Toplam Satır',

        # Form Fill
        'form_fill_title': 'PDF Form Doldurma',
        'form_fill_subtitle': 'PDF form alanlarını çevrimiçi doldurun',
        'form_fill_btn': 'Formu İndir',
        'form_fill_btn_loading': 'Hazırlanıyor...',
        'form_fill_complete': 'Form Dolduruldu!',
        'form_fill_detect': 'Alanları Tespit Et',
        'form_fill_detecting': 'Tespit ediliyor...',
        'form_fill_fields_found': '{count} form alanı bulundu',
        'form_fill_no_fields': 'Form alanı bulunamadı',
        'form_fill_field_name': 'Alan Adı',
        'form_fill_field_type': 'Tür',
        'form_fill_field_value': 'Değer',

        # PDF to Word
        'pdf_to_word_title': 'PDF\'den Word\'e Dönüştürme',
        'pdf_to_word_subtitle': 'PDF dosyalarını Word belgesine dönüştürün',
        'pdf_to_word_btn': 'Dönüştür',
        'pdf_to_word_btn_loading': 'Dönüştürülüyor...',
        'pdf_to_word_complete': 'Dönüştürme Tamamlandı!',

        # PDF/A
        'pdf_to_pdfa_title': 'PDF/A Dönüştürme',
        'pdf_to_pdfa_subtitle': 'PDF dosyalarını arşivleme standardı PDF/A formatına dönüştürün',
        'pdf_to_pdfa_btn': 'Dönüştür',
        'pdf_to_pdfa_btn_loading': 'Dönüştürülüyor...',
        'pdf_to_pdfa_complete': 'Dönüştürme Tamamlandı!',
        'pdf_to_pdfa_version': 'PDF/A Sürümü',

        # OCR
        'ocr_title': 'PDF OCR - Metin Tanıma',
        'ocr_subtitle': 'Taranmış PDF dosyalarından metin çıkarın (OCR)',
        'ocr_btn': 'OCR Başlat',
        'ocr_btn_loading': 'OCR işleniyor...',
        'ocr_complete': 'OCR Tamamlandı!',
        'ocr_language': 'OCR Dili',
        'ocr_lang_tr': 'Türkçe',
        'ocr_lang_en': 'İngilizce',
        'ocr_lang_both': 'Türkçe + İngilizce',
        'ocr_no_text': 'Metin bulunamadı',

        # Sign
        'sign_title': 'PDF İmzalama',
        'sign_subtitle': 'PDF dosyalarınıza el yazısı imza ekleyin',
        'sign_btn': 'İmzala',
        'sign_btn_loading': 'İmzalanıyor...',
        'sign_complete': 'İmzalama Tamamlandı!',
        'sign_tab_draw': 'Çiz',
        'sign_tab_upload': 'Görsel Yükle',
        'sign_step_create': 'İmza Oluştur',
        'sign_pen_size': 'Kalınlık',
        'sign_pen_color': 'Renk',
        'sign_upload_image': 'İmza görselini seçin veya sürükleyin',
        'sign_page': 'Sayfa',
        'sign_all_pages': 'Tüm Sayfalar',
        'sign_position': 'İmza Konumu',
        'sign_width': 'Genişlik',
        'sign_height': 'Yükseklik',
        'sign_no_signature': 'İmza gorseli gerekli!',

        # Redact
        'redact_title': 'PDF Karalama (Redact)',
        'redact_subtitle': 'PDF içeriğini kalıcı olarak karalayın ve sansürleyin',
        'redact_btn': 'Karala',
        'redact_btn_loading': 'Karalanıyor...',
        'redact_complete': 'Karalama Tamamlandı!',
        'redact_tab_text': 'Metin Ara',
        'redact_tab_area': 'Alan Seç',
        'redact_search_placeholder': 'Karalanacak metni girin...',
        'redact_text_required': 'Aranacak metin gerekli!',
        'redact_no_areas': 'En az bir alan seçin!',
        'redact_areas_selected': 'alan seçildi',

        # Resize
        'resize_title': 'PDF Sayfa Boyutu Değiştirme',
        'resize_subtitle': 'PDF sayfalarını A4, Letter, A3 gibi standart boyutlara dönüştürün',
        'resize_btn': 'Boyutlandır',
        'resize_btn_loading': 'Boyutlandırılıyor...',
        'resize_complete': 'Boyutlandırma Tamamlandı!',
        'resize_target_size': 'Hedef Boyut',
        'resize_mode': 'Mod',
        'resize_mode_fit': 'Sığdır',
        'resize_mode_fit_desc': 'İçeriği orantılı ölçekle',
        'resize_mode_crop': 'Kes',
        'resize_mode_crop_desc': 'Taşan kısımları kes',
        'resize_mode_expand': 'Genişlet',
        'resize_mode_expand_desc': 'Boşluk ekle',

        # Office to PDF
        'office_to_pdf_title': 'Office\'den PDF\'e Dönüştürme',
        'office_to_pdf_subtitle': 'Word, Excel ve PowerPoint dosyalarını PDF\'e dönüştürün',
        'office_to_pdf_btn': 'Dönüştür',
        'office_to_pdf_btn_loading': 'Dönüştürülüyor...',
        'office_to_pdf_complete': 'Dönüştürme Tamamlandı!',
        'office_to_pdf_drag': 'Office dosyasını seçin veya sürükleyin',

        # Blog
        'blog_title': 'Blog',
        'blog_read_more': 'Devamını Oku',
        'blog_back': 'Blog\'a Dön',
        'blog_related_tool': 'İlgili Araç',
        'blog_published': 'Yayınlanma',
        'blog_no_posts': 'Henüz yazı yok.',
        'blog_min_read': 'dk okuma',

        # Error pages
        'error_404': 'Sayfa bulunamadı',
        'error_413': 'Dosya çok büyük!',
        'error_500': 'Sunucu hatası oluştu',
        'error_go_home': 'Ana Sayfaya Dön',

        # Categories
        'cat_edit': 'Düzenle',
        'cat_edit_desc': 'PDF sayfalarını birleştirin, bölün, sıralayın',
        'cat_convert': 'Dönüştür',
        'cat_convert_desc': 'Dosya formatlarını dönüştürün',
        'cat_security': 'Güvenlik',
        'cat_security_desc': "PDF'lerinizi koruyun ve metadatayı yönetin",
        'cat_extract': 'Çıkar',
        'cat_extract_desc': 'PDF içinden metin ve görselleri çıkartın',
        'cat_optimize': 'Optimize',
        'cat_optimize_desc': "PDF'lerinizi iyileştirin ve onarım",
        'cat_ai': 'AI Araçlar',
        'cat_ai_desc': 'Yapay zeka destekli araçlar',

        # Tool tags
        'tag_popular': 'Popüler',
        'tag_fast': 'Hızlı',
        'tag_edit': 'Düzenle',
        'tag_easy': 'Kolay',
        'tag_convert': 'Dönüştür',
        'tag_new': 'Yeni',
        'tag_secure': 'Güvenli',
        'tag_pro': 'Pro',
        'tag_privacy': 'Gizlilik',
        'tag_extract': 'Çıkarma',
        'tag_export': 'Dışa Aktar',
        'tag_optimize': 'Optimize',
        'tag_recovery': 'Kurtarma',
        'tag_ai': 'AI Destekli',

        # How it works
        'how_it_works': 'Nasıl Çalışır?',
        'how_step_1': 'Yükle',
        'how_step_1_desc': 'PDF dosyanızı sürükleyin veya seçin',
        'how_step_2': 'İşle',
        'how_step_2_desc': 'Aracı seçin ve ayarları yapın',
        'how_step_3': 'İndir',
        'how_step_3_desc': 'İşlenmiş dosyanızı anında indirin',

        # Preview
        'preview': 'Önizleme',
        'preview_page': 'Sayfa',
        'preview_load_error': 'Önizleme yüklenemedi',
        'preview_error': 'Önizleme hatası',
        'preview_page_info': '{count} sayfa',
        'prev_page': 'Önceki',
        'next_page': 'Sonraki',
        'page_info': 'Sayfa 1/1',

        # FAQ
        'faq_title': 'Sıkça Sorulan Sorular',
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
        'pos_top_center': 'Top Center',
        'pos_top_right': 'Top Right',
        'pos_bottom_left': 'Bottom Left',
        'pos_bottom_right': 'Bottom Right',
        'watermark_scale': 'Size',

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

        # OCR
        'ocr_title': 'PDF OCR - Text Recognition',
        'ocr_subtitle': 'Extract text from scanned PDF files using OCR',
        'ocr_btn': 'Start OCR',
        'ocr_btn_loading': 'Processing OCR...',
        'ocr_complete': 'OCR Complete!',
        'ocr_language': 'OCR Language',
        'ocr_lang_tr': 'Turkish',
        'ocr_lang_en': 'English',
        'ocr_lang_both': 'Turkish + English',
        'ocr_no_text': 'No text found',

        # Sign
        'sign_title': 'Sign PDF',
        'sign_subtitle': 'Add handwritten signatures to your PDF files',
        'sign_btn': 'Sign',
        'sign_btn_loading': 'Signing...',
        'sign_complete': 'Signing Complete!',
        'sign_tab_draw': 'Draw',
        'sign_tab_upload': 'Upload Image',
        'sign_step_create': 'Create Signature',
        'sign_pen_size': 'Thickness',
        'sign_pen_color': 'Color',
        'sign_upload_image': 'Select or drag a signature image',
        'sign_page': 'Page',
        'sign_all_pages': 'All Pages',
        'sign_position': 'Signature Position',
        'sign_width': 'Width',
        'sign_height': 'Height',
        'sign_no_signature': 'Signature image is required!',

        # Redact
        'redact_title': 'PDF Redact',
        'redact_subtitle': 'Permanently redact and censor PDF content',
        'redact_btn': 'Redact',
        'redact_btn_loading': 'Redacting...',
        'redact_complete': 'Redaction Complete!',
        'redact_tab_text': 'Search Text',
        'redact_tab_area': 'Select Area',
        'redact_search_placeholder': 'Enter text to redact...',
        'redact_text_required': 'Search text is required!',
        'redact_no_areas': 'Select at least one area!',
        'redact_areas_selected': 'areas selected',

        # Resize
        'resize_title': 'Resize PDF Pages',
        'resize_subtitle': 'Convert PDF pages to standard sizes like A4, Letter, A3',
        'resize_btn': 'Resize',
        'resize_btn_loading': 'Resizing...',
        'resize_complete': 'Resize Complete!',
        'resize_target_size': 'Target Size',
        'resize_mode': 'Mode',
        'resize_mode_fit': 'Fit',
        'resize_mode_fit_desc': 'Scale content proportionally',
        'resize_mode_crop': 'Crop',
        'resize_mode_crop_desc': 'Trim overflowing parts',
        'resize_mode_expand': 'Expand',
        'resize_mode_expand_desc': 'Add whitespace',

        # Office to PDF
        'office_to_pdf_title': 'Office to PDF Converter',
        'office_to_pdf_subtitle': 'Convert Word, Excel and PowerPoint files to PDF',
        'office_to_pdf_btn': 'Convert',
        'office_to_pdf_btn_loading': 'Converting...',
        'office_to_pdf_complete': 'Conversion Complete!',
        'office_to_pdf_drag': 'Select or drag an Office file',

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
        'prev_page': 'Previous',
        'next_page': 'Next',
        'page_info': 'Page 1/1',

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
        'ocr_', 'sign_', 'redact_', 'resize_', 'office_to_pdf_',
    ]
    result = {}
    for key, val in translations.items():
        for prefix in js_keys:
            if key.startswith(prefix) or key == prefix.rstrip('_'):
                result[key] = val
                break
    return result
