"""
PDFEdit - SEO Metadata Registry
Tum araclarin SEO verilerini tek yerde tutar.
Sitemap, meta tags, structured data hepsi buradan beslenir.
"""

# Arac temel bilgileri
TOOLS = {
    'merge': {'slug': 'merge', 'icon': '&#128279;', 'category': 'edit', 'tier': 'free'},
    'split': {'slug': 'split', 'icon': '&#9986;', 'category': 'edit', 'tier': 'free'},
    'reorder': {'slug': 'reorder', 'icon': '&#128209;', 'category': 'edit', 'tier': 'limited_free'},
    'rotate': {'slug': 'rotate', 'icon': '&#128260;', 'category': 'edit', 'tier': 'free'},
    'compress': {'slug': 'compress', 'icon': '&#128230;', 'category': 'optimize', 'tier': 'free'},
    'encrypt': {'slug': 'encrypt', 'icon': '&#128274;', 'category': 'security', 'tier': 'limited_free'},
    'watermark': {'slug': 'watermark', 'icon': '&#128167;', 'category': 'security', 'tier': 'limited_free'},
    'metadata': {'slug': 'metadata', 'icon': '&#127991;', 'category': 'security', 'tier': 'limited_free'},
    'extract-text': {'slug': 'extract-text', 'icon': '&#128221;', 'category': 'extract', 'tier': 'free'},
    'extract-images': {'slug': 'extract-images', 'icon': '&#128444;', 'category': 'extract', 'tier': 'limited_free'},
    'img-to-pdf': {'slug': 'img-to-pdf', 'icon': '&#128444;', 'category': 'convert', 'tier': 'free'},
    'pdf-to-image': {'slug': 'pdf-to-image', 'icon': '&#128248;', 'category': 'convert', 'tier': 'limited_free'},
    'html-to-pdf': {'slug': 'html-to-pdf', 'icon': '&#127760;', 'category': 'convert', 'tier': 'premium'},
    'repair': {'slug': 'repair', 'icon': '&#128295;', 'category': 'optimize', 'tier': 'limited_free'},
    'numbering': {'slug': 'numbering', 'icon': '&#128290;', 'category': 'optimize', 'tier': 'limited_free'},
    'logo-removal': {'slug': 'logo-removal', 'icon': '&#127912;', 'category': 'ai', 'tier': 'free'},
    'crop': {'slug': 'crop', 'icon': '&#9986;', 'category': 'edit', 'tier': 'free'},
    'compare': {'slug': 'compare', 'icon': '&#128203;', 'category': 'edit', 'tier': 'limited_free'},
    'pdf-to-excel': {'slug': 'pdf-to-excel', 'icon': '&#128202;', 'category': 'convert', 'tier': 'limited_free'},
    'form-fill': {'slug': 'form-fill', 'icon': '&#128221;', 'category': 'edit', 'tier': 'limited_free'},
    'pdf-to-word': {'slug': 'pdf-to-word', 'icon': '&#128196;', 'category': 'convert', 'tier': 'limited_free'},
    'pdf-to-pdfa': {'slug': 'pdf-to-pdfa', 'icon': '&#128196;', 'category': 'convert', 'tier': 'limited_free'},
}

# Her arac icin SEO verileri (2 dil)
TOOL_SEO = {
    'merge': {
        'tr': {
            'title': 'PDF Birlestirme - Ucretsiz Online | PDFEdit',
            'description': 'Birden fazla PDF dosyasini tek dosyada birlestirin. Hizli, guvenli ve ucretsiz online PDF birlestirme araci.',
            'keywords': 'pdf birlestirme, pdf birlestir, ucretsiz pdf birlestirme, online pdf birlestiricisi, pdf dosyalari birlestir',
            'h1': 'PDF Birlestirme',
            'subtitle': 'Birden fazla PDF dosyasini tek bir dosyada birlestirin',
            'faq': [
                {'q': 'PDF dosyalarini nasil birlestirebilirim?', 'a': 'PDF dosyalarinizi surukleyip birakin veya dosya secerek yukleyin. Siralamayi ayarlayin ve "Birlestir" butonuna basin. Birlestirilmis PDF\'iniz aninda hazir olacaktir.'},
                {'q': 'Kac tane PDF birlestirilebilir?', 'a': 'Tek seferde istediginiz kadar PDF dosyasini birlestirebilirsiniz. Her dosya maksimum 100 MB olabilir.'},
                {'q': 'Birlestirme islemi guvenli mi?', 'a': 'Evet, dosyalariniz sunucumuzda islenir ve 1 saat icinde otomatik olarak silinir. Verileriniz ucuncu taraflarla paylasilmaz.'},
            ]
        },
        'en': {
            'title': 'Merge PDF - Free Online PDF Merger | PDFEdit',
            'description': 'Combine multiple PDF files into one document. Fast, secure, and free online PDF merger tool.',
            'keywords': 'merge pdf, combine pdf, free pdf merger, online pdf combiner, join pdf files',
            'h1': 'Merge PDF Files',
            'subtitle': 'Combine multiple PDF files into a single document',
            'faq': [
                {'q': 'How can I merge PDF files?', 'a': 'Drag and drop your PDF files or select them using the file picker. Arrange the order and click "Merge". Your combined PDF will be ready instantly.'},
                {'q': 'How many PDFs can I merge?', 'a': 'You can merge as many PDF files as you want in a single session. Each file can be up to 100 MB.'},
                {'q': 'Is the merge process secure?', 'a': 'Yes, your files are processed on our server and automatically deleted within 1 hour. Your data is never shared with third parties.'},
            ]
        }
    },
    'split': {
        'tr': {
            'title': 'PDF Bolme - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarini sayfalara veya araliklara gore bolun. Hizli ve ucretsiz online PDF bolme araci.',
            'keywords': 'pdf bolme, pdf bol, pdf sayfa ayirma, ucretsiz pdf bolme, online pdf bolme',
            'h1': 'PDF Bolme',
            'subtitle': 'PDF dosyalarini sayfalara veya araliklara gore bolun',
            'faq': [
                {'q': 'PDF dosyasini nasil bolebilirim?', 'a': 'PDF dosyanizi yukleyin, "Tum Sayfalari Ayir" veya "Sayfa Araligi" modunu secin ve "Bol" butonuna basin. Her sayfa ayri bir PDF olarak indirilir.'},
                {'q': 'Belirli sayfalari cikarabilir miyim?', 'a': 'Evet, sayfa araligi modunu secip "1-5, 8-10" gibi araliklar belirtebilirsiniz.'},
                {'q': 'Bolunmus dosyalari toplu indirebilir miyim?', 'a': 'Evet, tum bolunmus dosyalari tek bir ZIP dosyasi olarak indirebilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Split PDF - Free Online | PDFEdit',
            'description': 'Split PDF files by pages or page ranges. Fast and free online PDF splitter tool.',
            'keywords': 'split pdf, pdf splitter, separate pdf pages, free pdf split, extract pdf pages',
            'h1': 'Split PDF',
            'subtitle': 'Split PDF files by pages or page ranges',
            'faq': [
                {'q': 'How do I split a PDF file?', 'a': 'Upload your PDF, choose "Split All Pages" or "Page Range" mode, and click "Split". Each page will be available as a separate PDF.'},
                {'q': 'Can I extract specific pages?', 'a': 'Yes, select the page range mode and specify ranges like "1-5, 8-10".'},
                {'q': 'Can I download all split files at once?', 'a': 'Yes, you can download all split files as a single ZIP archive.'},
            ]
        }
    },
    'compress': {
        'tr': {
            'title': 'PDF Sikistirma - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosya boyutunu kucultun. Kalite secenekleriyle hizli ve ucretsiz online PDF sikistirma araci.',
            'keywords': 'pdf sikistirma, pdf kucultme, pdf boyut azaltma, ucretsiz pdf sikistirma, online pdf compress',
            'h1': 'PDF Sikistirma',
            'subtitle': 'PDF dosya boyutunu kucultun',
            'faq': [
                {'q': 'PDF dosyami nasil sikistirabilirim?', 'a': 'PDF dosyanizi yukleyin, kalite seviyesini secin (Yuksek, Orta veya Dusuk) ve "Sikistir" butonuna basin. Sikistirilmis dosya aninda hazir olacaktir.'},
                {'q': 'Sikistirma kaliteyi etkiler mi?', 'a': 'Yuksek kalite modu minimum kalite kaybiyla sikistirma yapar. Dusuk kalite modu daha fazla sikistirma saglar ancak gorsel kalitesi dusebilir.'},
                {'q': 'Ne kadar sikistirma yapilir?', 'a': 'Sikistirma orani dosyanin icerigine bagli olarak degisir. Tipik olarak %20-80 arasi boyut azaltma saglanir.'},
            ]
        },
        'en': {
            'title': 'Compress PDF - Free Online | PDFEdit',
            'description': 'Reduce PDF file size with quality options. Fast and free online PDF compression tool.',
            'keywords': 'compress pdf, reduce pdf size, pdf compressor, free pdf compression, shrink pdf',
            'h1': 'Compress PDF',
            'subtitle': 'Reduce your PDF file size',
            'faq': [
                {'q': 'How do I compress a PDF?', 'a': 'Upload your PDF, choose a quality level (High, Medium, or Low), and click "Compress". Your compressed file will be ready instantly.'},
                {'q': 'Does compression affect quality?', 'a': 'High quality mode compresses with minimal quality loss. Low quality mode provides more compression but visual quality may decrease.'},
                {'q': 'How much compression is achieved?', 'a': 'Compression ratio depends on the file content. Typically, 20-80% size reduction is achieved.'},
            ]
        }
    },
    'encrypt': {
        'tr': {
            'title': 'PDF Sifreleme - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarinizi sifre ile koruyun veya sifresini cozun. Guvenli ve ucretsiz online PDF sifreleme araci.',
            'keywords': 'pdf sifreleme, pdf sifrele, pdf sifre koyma, pdf sifre cozme, pdf koruma',
            'h1': 'PDF Sifreleme',
            'subtitle': 'PDF dosyalarinizi sifre ile koruyun veya sifresini cozun',
            'faq': [
                {'q': 'PDF dosyama nasil sifre koyabilirim?', 'a': 'PDF dosyanizi yukleyin, bir sifre belirleyin, izinleri ayarlayin ve "Sifrele" butonuna basin.'},
                {'q': 'Hangi izinleri ayarlayabilirim?', 'a': 'Yazdirma, kopyalama ve duzenleme izinlerini ayri ayri kontrol edebilirsiniz.'},
                {'q': 'Sifrelenmis PDF\'in sifresini cozebilir miyim?', 'a': 'Evet, mevcut sifreyi bilerek PDF\'in sifresini cozebilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Encrypt PDF - Free Online | PDFEdit',
            'description': 'Protect your PDF files with a password or decrypt them. Secure and free online PDF encryption tool.',
            'keywords': 'encrypt pdf, password protect pdf, pdf encryption, decrypt pdf, pdf security',
            'h1': 'Encrypt PDF',
            'subtitle': 'Protect your PDF files with a password or decrypt them',
            'faq': [
                {'q': 'How do I add a password to my PDF?', 'a': 'Upload your PDF, set a password, configure permissions, and click "Encrypt".'},
                {'q': 'What permissions can I set?', 'a': 'You can control printing, copying, and editing permissions separately.'},
                {'q': 'Can I decrypt an encrypted PDF?', 'a': 'Yes, you can decrypt a PDF if you know the existing password.'},
            ]
        }
    },
    'watermark': {
        'tr': {
            'title': 'PDF Filigran Ekleme - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalariniza metin veya gorsel filigran ekleyin. Konumlandirma ve seffaflik ayarlari ile ucretsiz filigran araci.',
            'keywords': 'pdf filigran, pdf watermark, pdf damga, metin filigran, gorsel filigran',
            'h1': 'PDF Filigran Ekleme',
            'subtitle': 'PDF dosyalariniza metin veya gorsel filigran ekleyin',
            'faq': [
                {'q': 'PDF\'e filigran nasil eklenir?', 'a': 'PDF dosyanizi yukleyin, metin veya gorsel filigran secin, konum ve seffaflik ayarlayin, "Filigran Ekle" butonuna basin.'},
                {'q': 'Filigranin konumunu ayarlayabilir miyim?', 'a': 'Evet, merkez, ust-sol, ust-sag, alt-sol ve alt-sag konumlarindan birini secebilirsiniz. Donme acisini da ayarlayabilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Add Watermark to PDF - Free Online | PDFEdit',
            'description': 'Add text or image watermarks to your PDF files. Free watermark tool with positioning and transparency options.',
            'keywords': 'pdf watermark, add watermark to pdf, text watermark, image watermark, pdf stamp',
            'h1': 'Add Watermark to PDF',
            'subtitle': 'Add text or image watermarks to your PDF files',
            'faq': [
                {'q': 'How do I add a watermark to a PDF?', 'a': 'Upload your PDF, choose text or image watermark, set position and transparency, and click "Add Watermark".'},
                {'q': 'Can I adjust the watermark position?', 'a': 'Yes, you can choose from center, top-left, top-right, bottom-left, and bottom-right positions. You can also set rotation angle.'},
            ]
        }
    },
    'rotate': {
        'tr': {
            'title': 'PDF Dondurme - Ucretsiz Online | PDFEdit',
            'description': 'PDF sayfalarini 90, 180 veya 270 derece dondurun. Hizli ve ucretsiz online PDF dondurme araci.',
            'keywords': 'pdf dondurme, pdf dondur, pdf sayfa dondurme, pdf aci, pdf cevir',
            'h1': 'PDF Dondurme',
            'subtitle': 'PDF sayfalarini 90, 180 veya 270 derece dondurun',
            'faq': [
                {'q': 'PDF sayfalarini nasil dondururum?', 'a': 'PDF dosyanizi yukleyin, dondurme acisini secin, tum sayfalari veya belirli sayfalari secin ve "Dondur" butonuna basin.'},
                {'q': 'Sadece belirli sayfalari dondurebilir miyim?', 'a': 'Evet, dondurulecek sayfa numaralarini virgul ile ayirarak belirtebilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Rotate PDF - Free Online | PDFEdit',
            'description': 'Rotate PDF pages by 90, 180, or 270 degrees. Fast and free online PDF rotation tool.',
            'keywords': 'rotate pdf, pdf rotation, turn pdf pages, pdf page rotation, flip pdf',
            'h1': 'Rotate PDF',
            'subtitle': 'Rotate PDF pages by 90, 180, or 270 degrees',
            'faq': [
                {'q': 'How do I rotate PDF pages?', 'a': 'Upload your PDF, choose rotation angle, select all pages or specific pages, and click "Rotate".'},
                {'q': 'Can I rotate specific pages only?', 'a': 'Yes, you can specify page numbers separated by commas.'},
            ]
        }
    },
    'extract-text': {
        'tr': {
            'title': 'PDF\'den Metin Cikarma - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarindan tum metni cikarin ve kopyalayin. Ucretsiz online PDF metin cikarma araci.',
            'keywords': 'pdf metin cikarma, pdf yazilari kopyalama, pdf text extract, pdf icerik cikarma',
            'h1': 'PDF Metin Cikarma',
            'subtitle': 'PDF dosyalarindan tum metni cikarin ve kopyalayin',
            'faq': [
                {'q': 'PDF\'den metin nasil cikarilir?', 'a': 'PDF dosyanizi yukleyin, metin otomatik olarak cikarilacaktir. Metni kopyalayabilir veya TXT dosyasi olarak indirebilirsiniz.'},
                {'q': 'Taranmis PDF\'lerden metin cikarilabilir mi?', 'a': 'Hayir, bu arac sadece metin katmani iceren PDF\'lerden metin cikarabilir. Taranmis belgeler icin OCR gerektiriyor.'},
            ]
        },
        'en': {
            'title': 'Extract Text from PDF - Free Online | PDFEdit',
            'description': 'Extract all text from PDF files. Free online PDF text extraction tool.',
            'keywords': 'extract text from pdf, pdf to text, copy text from pdf, pdf text extractor',
            'h1': 'Extract Text from PDF',
            'subtitle': 'Extract all text from your PDF files',
            'faq': [
                {'q': 'How do I extract text from a PDF?', 'a': 'Upload your PDF and the text will be extracted automatically. You can copy the text or download it as a TXT file.'},
                {'q': 'Can I extract text from scanned PDFs?', 'a': 'No, this tool only extracts text from PDFs with a text layer. Scanned documents require OCR.'},
            ]
        }
    },
    'extract-images': {
        'tr': {
            'title': 'PDF\'den Gorsel Cikarma - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarindan tum gorselleri cikarin ve indirin. Ucretsiz online PDF gorsel cikarma araci.',
            'keywords': 'pdf gorsel cikarma, pdf resim cikarma, pdf image extract, pdf fotograflari kaydetme',
            'h1': 'PDF Gorsel Cikarma',
            'subtitle': 'PDF dosyalarindan tum gorselleri cikarin ve indirin',
            'faq': [
                {'q': 'PDF\'den gorselleri nasil cikarabilirim?', 'a': 'PDF dosyanizi yukleyin, tum gorseller otomatik olarak cikarilacaktir. Gorselleri tek tek veya ZIP olarak toplu indirebilirsiniz.'},
                {'q': 'Gorseller hangi formatta cikarilir?', 'a': 'Gorseller orijinal formatlarinda (PNG, JPEG vs.) cikarilir.'},
            ]
        },
        'en': {
            'title': 'Extract Images from PDF - Free Online | PDFEdit',
            'description': 'Extract all images from PDF files. Free online PDF image extraction tool.',
            'keywords': 'extract images from pdf, pdf to images, save pdf images, pdf image extractor',
            'h1': 'Extract Images from PDF',
            'subtitle': 'Extract all images from your PDF files',
            'faq': [
                {'q': 'How do I extract images from a PDF?', 'a': 'Upload your PDF and all images will be extracted automatically. You can download images individually or as a ZIP.'},
                {'q': 'What format are the extracted images?', 'a': 'Images are extracted in their original format (PNG, JPEG, etc.).'},
            ]
        }
    },
    'img-to-pdf': {
        'tr': {
            'title': 'Gorsel\'den PDF\'e Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'JPG, PNG ve diger gorselleri PDF belgesine donusturun. Ucretsiz online gorsel PDF donusturme araci.',
            'keywords': 'gorsel pdf donusturme, jpg pdf, png pdf, resim pdf, foto pdf donustur',
            'h1': 'Gorsel\'den PDF\'e Donusturme',
            'subtitle': 'Gorselleri PDF belgesine donusturun',
            'faq': [
                {'q': 'Gorselleri PDF\'e nasil donusturebilirim?', 'a': 'Gorsel dosyalarinizi surukleyip birakin veya secin, siralamayi ayarlayin ve "Donustur" butonuna basin.'},
                {'q': 'Hangi gorsel formatlari desteklenir?', 'a': 'JPG, JPEG, PNG ve diger yaygin gorsel formatlari desteklenir.'},
            ]
        },
        'en': {
            'title': 'Image to PDF Converter - Free Online | PDFEdit',
            'description': 'Convert JPG, PNG and other images to PDF. Free online image to PDF converter.',
            'keywords': 'image to pdf, jpg to pdf, png to pdf, convert image to pdf, photo to pdf',
            'h1': 'Image to PDF Converter',
            'subtitle': 'Convert images to PDF documents',
            'faq': [
                {'q': 'How do I convert images to PDF?', 'a': 'Drag and drop your image files or select them, arrange the order, and click "Convert".'},
                {'q': 'What image formats are supported?', 'a': 'JPG, JPEG, PNG, and other common image formats are supported.'},
            ]
        }
    },
    'pdf-to-image': {
        'tr': {
            'title': 'PDF\'den Gorsel\'e Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'PDF sayfalarini PNG, JPG veya WebP formatinda gorsellere donusturun. DPI secenekleriyle ucretsiz online arac.',
            'keywords': 'pdf gorsel donusturme, pdf png, pdf jpg, pdf resim, pdf to image',
            'h1': 'PDF\'den Gorsel\'e Donusturme',
            'subtitle': 'PDF sayfalarini PNG, JPG veya WebP formatinda gorsellere donusturun',
            'faq': [
                {'q': 'PDF\'yi gorsele nasil donusturebilirim?', 'a': 'PDF dosyanizi yukleyin, gorsel formatini (PNG, JPG, WebP) ve DPI degerini secin, "Donustur" butonuna basin.'},
                {'q': 'DPI ne anlama gelir?', 'a': 'DPI (Dots Per Inch) gorsel cozunurlugunu belirler. Yuksek DPI daha net gorseller uretir ancak dosya boyutu artar.'},
            ]
        },
        'en': {
            'title': 'PDF to Image Converter - Free Online | PDFEdit',
            'description': 'Convert PDF pages to PNG, JPG, or WebP images. Free online tool with DPI options.',
            'keywords': 'pdf to image, pdf to png, pdf to jpg, convert pdf to image, pdf to picture',
            'h1': 'PDF to Image Converter',
            'subtitle': 'Convert PDF pages to PNG, JPG, or WebP images',
            'faq': [
                {'q': 'How do I convert PDF to images?', 'a': 'Upload your PDF, select image format (PNG, JPG, WebP) and DPI value, then click "Convert".'},
                {'q': 'What does DPI mean?', 'a': 'DPI (Dots Per Inch) determines image resolution. Higher DPI produces clearer images but increases file size.'},
            ]
        }
    },
    'html-to-pdf': {
        'tr': {
            'title': 'HTML\'den PDF\'e Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'HTML kodunu veya web sayfasi URL\'sini PDF belgesine donusturun. Sayfa boyutu ve kenar boslugu secenekleriyle ucretsiz arac.',
            'keywords': 'html pdf donusturme, web sayfa pdf, url pdf, html to pdf, web to pdf',
            'h1': 'HTML\'den PDF\'e Donusturme',
            'subtitle': 'HTML kodunu veya web sayfasi URL\'sini PDF belgesine donusturun',
            'faq': [
                {'q': 'HTML\'i PDF\'e nasil donusturebilirim?', 'a': 'HTML kodu girin veya bir URL yapistirin, sayfa boyutu ve kenar boslugu ayarlarini yapin, "Donustur" butonuna basin.'},
                {'q': 'Web sayfasi URL\'si donusturulebilir mi?', 'a': 'Evet, herhangi bir web sayfasi URL\'sini girerek PDF\'e donusturebilirsiniz.'},
            ]
        },
        'en': {
            'title': 'HTML to PDF Converter - Free Online | PDFEdit',
            'description': 'Convert HTML code or webpage URL to PDF. Free tool with page size and margin options.',
            'keywords': 'html to pdf, webpage to pdf, url to pdf, convert html, web page pdf',
            'h1': 'HTML to PDF Converter',
            'subtitle': 'Convert HTML code or webpage URL to PDF',
            'faq': [
                {'q': 'How do I convert HTML to PDF?', 'a': 'Enter HTML code or paste a URL, configure page size and margin settings, then click "Convert".'},
                {'q': 'Can I convert a webpage URL?', 'a': 'Yes, you can enter any webpage URL to convert it to PDF.'},
            ]
        }
    },
    'reorder': {
        'tr': {
            'title': 'PDF Sayfa Siralama - Ucretsiz Online | PDFEdit',
            'description': 'Surukle-birak ile PDF sayfalarini yeniden siralayin veya sayfa silin. Ucretsiz online PDF sayfa yonetim araci.',
            'keywords': 'pdf sayfa siralama, pdf sayfa duzenleme, pdf sirala, sayfa sil, pdf reorder',
            'h1': 'PDF Sayfa Siralama',
            'subtitle': 'Surukle-birak ile PDF sayfalarini yeniden siralayin veya sayfa silin',
            'faq': [
                {'q': 'PDF sayfalarini nasil yeniden siralayabilirim?', 'a': 'PDF dosyanizi yukleyin, sayfa onizlemelerini surukleyerek yeni siraya koyun ve "Kaydet" butonuna basin.'},
                {'q': 'Sayfalar silinebilir mi?', 'a': 'Evet, istemediginiz sayfalari secip silebilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Reorder PDF Pages - Free Online | PDFEdit',
            'description': 'Rearrange PDF pages with drag and drop or delete pages. Free online PDF page management tool.',
            'keywords': 'reorder pdf pages, rearrange pdf, sort pdf pages, delete pdf pages, pdf page order',
            'h1': 'Reorder PDF Pages',
            'subtitle': 'Rearrange PDF pages with drag and drop or delete pages',
            'faq': [
                {'q': 'How do I reorder PDF pages?', 'a': 'Upload your PDF, drag page thumbnails to rearrange, and click "Save".'},
                {'q': 'Can I delete pages?', 'a': 'Yes, you can select and delete unwanted pages.'},
            ]
        }
    },
    'repair': {
        'tr': {
            'title': 'PDF Onarma - Ucretsiz Online | PDFEdit',
            'description': 'Bozuk veya hasarli PDF dosyalarini onarin. Analiz ve kurtarma ozellikleriyle ucretsiz online PDF onarma araci.',
            'keywords': 'pdf onarma, bozuk pdf, pdf tamir, pdf kurtarma, pdf repair, hasarli pdf',
            'h1': 'PDF Onarma',
            'subtitle': 'Bozuk veya hasarli PDF dosyalarini onarin',
            'faq': [
                {'q': 'Bozuk bir PDF nasil onarilir?', 'a': 'PDF dosyanizi yukleyin, "Analiz Et" ile sorunlari goruntuleyin ve "Onar" butonuyla dosyayi kurtarin.'},
                {'q': 'Her bozuk PDF onarilabilir mi?', 'a': 'Cogu durumda basariyla onarim yapilir, ancak ciddi sekilde hasarli dosyalarin tamami kurtarilamayabilir.'},
            ]
        },
        'en': {
            'title': 'Repair PDF - Free Online | PDFEdit',
            'description': 'Repair corrupted or damaged PDF files. Free online PDF repair tool with analysis and recovery features.',
            'keywords': 'repair pdf, fix pdf, corrupted pdf, pdf recovery, broken pdf, damaged pdf',
            'h1': 'Repair PDF',
            'subtitle': 'Repair corrupted or damaged PDF files',
            'faq': [
                {'q': 'How do I repair a corrupted PDF?', 'a': 'Upload your PDF, click "Analyze" to see issues, and click "Repair" to fix the file.'},
                {'q': 'Can every corrupted PDF be repaired?', 'a': 'Most cases can be successfully repaired, but severely damaged files may not be fully recoverable.'},
            ]
        }
    },
    'metadata': {
        'tr': {
            'title': 'PDF Metadata Duzenleyici - Ucretsiz Online | PDFEdit',
            'description': 'PDF meta bilgilerini goruntuleyin, duzenleyin veya temizleyin. Gizlilik icin metadata kaldirma araci.',
            'keywords': 'pdf metadata, pdf bilgi, pdf yazar, pdf baslik, metadata duzenleme, metadata temizleme',
            'h1': 'PDF Metadata Duzenleyici',
            'subtitle': 'PDF meta bilgilerini goruntuleyin, duzenleyin veya temizleyin',
            'faq': [
                {'q': 'PDF metadata nedir?', 'a': 'PDF metadata dosya hakkindaki bilgileri (yazar, baslik, olusturma tarihi vs.) icerir. Bu bilgiler gizlilik acisindan onemli olabilir.'},
                {'q': 'Metadata neden temizlenmeli?', 'a': 'PDF paylasirken kisisel bilgilerinizin (yazar adi, bilgisayar adi vs.) gorunmesini onlemek icin metadata temizlenebilir.'},
            ]
        },
        'en': {
            'title': 'PDF Metadata Editor - Free Online | PDFEdit',
            'description': 'View, edit, or remove PDF metadata. Privacy-friendly metadata cleaning tool.',
            'keywords': 'pdf metadata, pdf properties, pdf info, metadata editor, remove pdf metadata',
            'h1': 'PDF Metadata Editor',
            'subtitle': 'View, edit, or remove PDF metadata',
            'faq': [
                {'q': 'What is PDF metadata?', 'a': 'PDF metadata contains information about the file (author, title, creation date, etc.). This information can be important for privacy.'},
                {'q': 'Why should I clean metadata?', 'a': 'To prevent your personal information (author name, computer name, etc.) from being visible when sharing PDFs.'},
            ]
        }
    },
    'numbering': {
        'tr': {
            'title': 'PDF Sayfa Numaralandirma - Ucretsiz Online | PDFEdit',
            'description': 'PDF sayfalarina ozellestirilmis numara ekleyin. Konum, format ve font secenekleriyle ucretsiz numaralandirma araci.',
            'keywords': 'pdf numaralandirma, pdf sayfa numarasi, pdf numara ekle, sayfa numaralandirma',
            'h1': 'PDF Sayfa Numaralandirma',
            'subtitle': 'PDF sayfalarina ozellestirilmis numara ekleyin',
            'faq': [
                {'q': 'PDF\'e sayfa numarasi nasil eklenir?', 'a': 'PDF dosyanizi yukleyin, numara konumunu, formatini ve font boyutunu secin, "Numarala" butonuna basin.'},
                {'q': 'Ilk sayfayi atlayabilir miyim?', 'a': 'Evet, "Ilk sayfayi atla" secenegini isaretleyerek kapak sayfasini numarasiz birakabilirsiniz.'},
            ]
        },
        'en': {
            'title': 'Add Page Numbers to PDF - Free Online | PDFEdit',
            'description': 'Add customizable page numbers to PDF files. Free numbering tool with position, format, and font options.',
            'keywords': 'pdf page numbers, add page numbers, pdf numbering, number pdf pages',
            'h1': 'Add Page Numbers to PDF',
            'subtitle': 'Add customizable page numbers to your PDF files',
            'faq': [
                {'q': 'How do I add page numbers to a PDF?', 'a': 'Upload your PDF, choose number position, format, and font size, then click "Number".'},
                {'q': 'Can I skip the first page?', 'a': 'Yes, check the "Skip first page" option to leave the cover page unnumbered.'},
            ]
        }
    },
    'logo-removal': {
        'tr': {
            'title': 'AI Logo Silme - Ucretsiz Online | PDFEdit',
            'description': 'Yapay zeka ile PDF dosyalarindan logo ve filigran kaldirin. SIFT algoritmasi ile otomatik tespit ve temizleme.',
            'keywords': 'logo silme, pdf logo kaldir, filigran kaldir, ai logo silme, pdf logo temizleme',
            'h1': 'AI Logo Silme',
            'subtitle': 'Yapay zeka ile PDF dosyalarindan logo ve filigran kaldirin',
            'faq': [
                {'q': 'Logo silme nasil calisir?', 'a': 'SIFT algoritmasi ile logonuz PDF\'deki her sayfada otomatik olarak tespit edilir ve temizlenir.'},
                {'q': 'Her tur logo silinebilir mi?', 'a': 'Cogu durumda basarili sonuc alinir, ancak cok kucuk veya dusuk kontrastli logolar tam tespit edilemeyebilir.'},
            ]
        },
        'en': {
            'title': 'AI Logo Removal - Free Online | PDFEdit',
            'description': 'Remove logos and watermarks from PDF files with AI. Automatic detection and cleaning with SIFT algorithm.',
            'keywords': 'remove logo from pdf, pdf logo removal, remove watermark, ai logo remover',
            'h1': 'AI Logo Removal',
            'subtitle': 'Remove logos and watermarks from PDF files with AI',
            'faq': [
                {'q': 'How does logo removal work?', 'a': 'The SIFT algorithm automatically detects your logo on each page of the PDF and removes it.'},
                {'q': 'Can every type of logo be removed?', 'a': 'Most cases produce successful results, but very small or low-contrast logos may not be fully detected.'},
            ]
        }
    },
    'crop': {
        'tr': {
            'title': 'PDF Kirpma - Ucretsiz Online | PDFEdit',
            'description': 'PDF sayfalarinin kenar bosluklarini kirpin veya beyaz kenarlari otomatik temizleyin. Ucretsiz online PDF kirpma araci.',
            'keywords': 'pdf kirpma, pdf kirp, pdf kenar bosluk, pdf crop, pdf margin, beyaz kenar kirpma',
            'h1': 'PDF Kirpma',
            'subtitle': 'PDF sayfalarinin kenar bosluklarini ayarlayin veya otomatik kirpin',
            'faq': [
                {'q': 'PDF nasil kirpilir?', 'a': 'PDF dosyanizi yukleyin, kenar bosluklarini ayarlayin veya otomatik kirpma secin ve "Kirp" butonuna basin.'},
                {'q': 'Otomatik kirpma ne yapar?', 'a': 'Sayfalardaki beyaz kenar bosluklarini otomatik tespit edip kaldirarak icerige gore kirpar.'},
                {'q': 'Kirpma geri alinabilir mi?', 'a': 'Kirpma islemi kalicidir, orijinal PDF\'iniz korunur ve yeni bir dosya olusturulur.'},
            ]
        },
        'en': {
            'title': 'Crop PDF - Free Online | PDFEdit',
            'description': 'Crop PDF page margins or auto-remove white borders. Free online PDF cropping tool.',
            'keywords': 'crop pdf, pdf crop, pdf margins, trim pdf, remove white borders, pdf trim',
            'h1': 'Crop PDF',
            'subtitle': 'Adjust page margins or auto-crop white borders',
            'faq': [
                {'q': 'How do I crop a PDF?', 'a': 'Upload your PDF, set margins or choose auto-crop, and click "Crop".'},
                {'q': 'What does auto-crop do?', 'a': 'It automatically detects and removes white border areas, cropping to the content.'},
                {'q': 'Is cropping reversible?', 'a': 'The cropping is permanent on the output file. Your original PDF is preserved.'},
            ]
        }
    },
    'compare': {
        'tr': {
            'title': 'PDF Karsilastirma - Ucretsiz Online | PDFEdit',
            'description': 'Iki PDF dosyasini sayfa sayfa karsilastirin. Gorsel farklar ve metin degisiklikleri ile detayli karsilastirma.',
            'keywords': 'pdf karsilastir, pdf farklari, pdf compare, pdf diff, iki pdf karsilastirma',
            'h1': 'PDF Karsilastirma',
            'subtitle': 'Iki PDF dosyasini sayfa sayfa karsilastirin',
            'faq': [
                {'q': 'PDF karsilastirma nasil calisir?', 'a': 'Iki PDF yukleyin, her sayfa gorsel ve metin olarak karsilastirilir. Farklar kirmizi ile vurgulanir.'},
                {'q': 'Farkli sayfa sayisindaki PDF\'ler karsilastirilabilir mi?', 'a': 'Evet, ortak sayfalar karsilastirilir ve fazla sayfalar ayrica belirtilir.'},
            ]
        },
        'en': {
            'title': 'Compare PDF - Free Online | PDFEdit',
            'description': 'Compare two PDF files page by page. Visual differences and text changes with detailed comparison.',
            'keywords': 'compare pdf, pdf diff, pdf comparison, difference between pdfs, pdf compare tool',
            'h1': 'Compare PDF Files',
            'subtitle': 'Compare two PDF files page by page',
            'faq': [
                {'q': 'How does PDF comparison work?', 'a': 'Upload two PDFs and each page is compared visually and by text. Differences are highlighted in red.'},
                {'q': 'Can I compare PDFs with different page counts?', 'a': 'Yes, common pages are compared and extra pages are noted separately.'},
            ]
        }
    },
    'pdf-to-excel': {
        'tr': {
            'title': 'PDF\'den Excel\'e Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'PDF tablolarini Excel (XLSX) dosyasina donusturun. Otomatik tablo tespiti ile ucretsiz online donusturme.',
            'keywords': 'pdf excel, pdf xlsx, pdf tablo cikarma, pdf to excel, pdf excel donusturme',
            'h1': 'PDF\'den Excel\'e Donusturme',
            'subtitle': 'PDF tablolarini Excel dosyasina donusturun',
            'faq': [
                {'q': 'PDF tablolari Excel\'e nasil aktarilir?', 'a': 'PDF dosyanizi yukleyin, tablolar otomatik tespit edilir ve XLSX dosyasi olarak indirebilirsiniz.'},
                {'q': 'Tablo olmayan PDF\'ler donusturulur mu?', 'a': 'Tablo bulunamazsa metin icerigi Excel\'e aktarilir.'},
            ]
        },
        'en': {
            'title': 'PDF to Excel Converter - Free Online | PDFEdit',
            'description': 'Convert PDF tables to Excel (XLSX) files. Free online converter with automatic table detection.',
            'keywords': 'pdf to excel, pdf to xlsx, extract tables from pdf, pdf table converter',
            'h1': 'PDF to Excel Converter',
            'subtitle': 'Convert PDF tables to Excel files',
            'faq': [
                {'q': 'How do I convert PDF tables to Excel?', 'a': 'Upload your PDF, tables are automatically detected and you can download the XLSX file.'},
                {'q': 'What if the PDF has no tables?', 'a': 'If no tables are found, text content is exported to Excel.'},
            ]
        }
    },
    'form-fill': {
        'tr': {
            'title': 'PDF Form Doldurma - Ucretsiz Online | PDFEdit',
            'description': 'PDF form alanlarini cevrimici doldurun. Otomatik alan tespiti ile ucretsiz online PDF form doldurma araci.',
            'keywords': 'pdf form doldurma, pdf form fill, pdf alan doldur, pdf formunu doldur, pdf doldurucu',
            'h1': 'PDF Form Doldurma',
            'subtitle': 'PDF form alanlarini cevrimici doldurun',
            'faq': [
                {'q': 'PDF formunu nasil doldurabilirim?', 'a': 'PDF formunuzu yukleyin, tum alanlar otomatik tespit edilir. Alanlari doldurun ve dosyayi indirin.'},
                {'q': 'Her tur form destekleniyor mu?', 'a': 'Metin alanlari, onay kutulari, acilir listeler ve radyo butonlari desteklenir.'},
            ]
        },
        'en': {
            'title': 'Fill PDF Forms - Free Online | PDFEdit',
            'description': 'Fill PDF form fields online. Free online PDF form filler with automatic field detection.',
            'keywords': 'fill pdf form, pdf form filler, pdf form fill online, complete pdf form',
            'h1': 'Fill PDF Forms',
            'subtitle': 'Fill PDF form fields online',
            'faq': [
                {'q': 'How do I fill a PDF form?', 'a': 'Upload your PDF form, all fields are auto-detected. Fill in the fields and download the completed file.'},
                {'q': 'What field types are supported?', 'a': 'Text fields, checkboxes, dropdown lists, and radio buttons are supported.'},
            ]
        }
    },
    'pdf-to-word': {
        'tr': {
            'title': 'PDF\'den Word\'e Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarini Word (DOCX) formatina donusturun. Yapi ve biclendirme korunarak ucretsiz online donusturme.',
            'keywords': 'pdf word, pdf docx, pdf to word, pdf word donusturme, pdf den word e',
            'h1': 'PDF\'den Word\'e Donusturme',
            'subtitle': 'PDF dosyalarini Word belgesine donusturun',
            'faq': [
                {'q': 'PDF nasil Word\'e donusturulur?', 'a': 'PDF dosyanizi yukleyin ve "Donustur" butonuna basin. DOCX dosyaniz aninda hazir olacaktir.'},
                {'q': 'Biclendirme korunur mu?', 'a': 'Metin, tablolar ve temel bicimler mumkun oldugunca korunur. Karmasik tasarimlar farklilik gosterebilir.'},
            ]
        },
        'en': {
            'title': 'PDF to Word Converter - Free Online | PDFEdit',
            'description': 'Convert PDF files to Word (DOCX) format. Free online conversion preserving layout and formatting.',
            'keywords': 'pdf to word, pdf to docx, convert pdf to word, pdf word converter',
            'h1': 'PDF to Word Converter',
            'subtitle': 'Convert PDF files to Word documents',
            'faq': [
                {'q': 'How do I convert PDF to Word?', 'a': 'Upload your PDF and click "Convert". Your DOCX file will be ready instantly.'},
                {'q': 'Is formatting preserved?', 'a': 'Text, tables, and basic formatting are preserved as much as possible. Complex layouts may differ.'},
            ]
        }
    },
    'pdf-to-pdfa': {
        'tr': {
            'title': 'PDF/A Donusturme - Ucretsiz Online | PDFEdit',
            'description': 'PDF dosyalarini arsivleme standardi PDF/A formatina donusturun. PDF/A-1b, 2b, 3b surum destegi.',
            'keywords': 'pdf/a, pdfa, pdf arsiv, pdf/a donusturme, pdf/a-1b, pdf/a-2b, pdf archival',
            'h1': 'PDF/A Donusturme',
            'subtitle': 'PDF dosyalarini arsivleme standardi PDF/A formatina donusturun',
            'faq': [
                {'q': 'PDF/A nedir?', 'a': 'PDF/A, uzun sureli dijital arsivleme icin ISO standardi formatdir. Belgelerinizin gelecekte de okunabilir kalmasini saglar.'},
                {'q': 'Hangi PDF/A surumleri destekleniyor?', 'a': 'PDF/A-1b, PDF/A-2b ve PDF/A-3b surumleri desteklenmektedir.'},
            ]
        },
        'en': {
            'title': 'PDF to PDF/A Converter - Free Online | PDFEdit',
            'description': 'Convert PDF files to archival PDF/A format. Support for PDF/A-1b, 2b, 3b versions.',
            'keywords': 'pdf/a, pdfa, pdf archival, pdf/a converter, pdf/a-1b, pdf/a-2b, long-term archival',
            'h1': 'PDF to PDF/A Converter',
            'subtitle': 'Convert PDF files to archival PDF/A format',
            'faq': [
                {'q': 'What is PDF/A?', 'a': 'PDF/A is an ISO standard format for long-term digital archiving. It ensures your documents remain readable in the future.'},
                {'q': 'Which PDF/A versions are supported?', 'a': 'PDF/A-1b, PDF/A-2b, and PDF/A-3b versions are supported.'},
            ]
        }
    },
}

# Site geneli SEO verileri
SITE_SEO = {
    'tr': {
        'site_name': 'PDFEdit - Ucretsiz Online PDF Araclari',
        'site_description': '23 ucretsiz online PDF araci. PDF birlestirme, bolme, sikistirma, sifreleme, filigran, dondurme ve daha fazlasi. Hizli, guvenli ve gizlilik odakli.',
        'site_keywords': 'pdf araclari, ucretsiz pdf, online pdf, pdf islem, pdf edit, pdf duzenleyici',
        'hero_title': 'Ucretsiz Online PDF Araclari',
        'hero_subtitle': '23 profesyonel PDF araci. Hizli, guvenli ve tamamen ucretsiz.',
        'how_it_works': [
            {'icon': '&#128228;', 'title': 'Yukle', 'desc': 'PDF dosyanizi surukleyin veya secin'},
            {'icon': '&#9881;', 'title': 'Isle', 'desc': 'Araci secin ve ayarlari yapin'},
            {'icon': '&#128229;', 'title': 'Indir', 'desc': 'Islenmis dosyanizi aninda indirin'},
        ],
        'trust_items': [
            {'icon': '&#128274;', 'text': 'Dosyalariniz 1 saat icinde otomatik silinir'},
            {'icon': '&#128737;', 'text': 'Verileriniz ucuncu taraflarla paylasilmaz'},
            {'icon': '&#9889;', 'text': 'Tum islemler sunucuda gerceklesir'},
        ],
    },
    'en': {
        'site_name': 'PDFEdit - Free Online PDF Tools',
        'site_description': '23 free online PDF tools. Merge, split, compress, encrypt, watermark, rotate PDFs and more. Fast, secure, and privacy-focused.',
        'site_keywords': 'pdf tools, free pdf, online pdf, pdf processing, pdf edit, pdf editor',
        'hero_title': 'Free Online PDF Tools',
        'hero_subtitle': '23 professional PDF tools. Fast, secure, and completely free.',
        'how_it_works': [
            {'icon': '&#128228;', 'title': 'Upload', 'desc': 'Drag and drop or select your PDF file'},
            {'icon': '&#9881;', 'title': 'Process', 'desc': 'Choose a tool and configure settings'},
            {'icon': '&#128229;', 'title': 'Download', 'desc': 'Download your processed file instantly'},
        ],
        'trust_items': [
            {'icon': '&#128274;', 'text': 'Your files are automatically deleted within 1 hour'},
            {'icon': '&#128737;', 'text': 'Your data is never shared with third parties'},
            {'icon': '&#9889;', 'text': 'All processing happens on our server'},
        ],
    }
}


def get_tool_seo(tool_name, lang='tr'):
    """Aracin SEO verilerini dondur"""
    tool_data = TOOL_SEO.get(tool_name, {})
    return tool_data.get(lang, tool_data.get('tr', {}))


def get_site_seo(lang='tr'):
    """Site geneli SEO verilerini dondur"""
    return SITE_SEO.get(lang, SITE_SEO['tr'])


def get_all_tool_slugs():
    """Sitemap icin tum arac slug'larini dondur"""
    return [t['slug'] for t in TOOLS.values()]
