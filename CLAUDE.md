# PDF Edit - Proje Rehberi

## Genel Bakis
Flask tabanli bir PDF arac sitesi. Turkce arayuz. 23 farkli PDF araci mevcut.
Calisma portu: `localhost:5000` | Max upload: 100MB (config ile degistirilebilir)

## Teknoloji Yigini
- **Backend:** Flask 3.0, Python 3.12
- **PDF isleme:** PyPDF2, pikepdf, PyMuPDF (fitz), reportlab, pdf2image, img2pdf
- **Goruntu isleme:** OpenCV (SIFT algoritmasi), NumPy, Pillow
- **HTML → PDF:** WeasyPrint (dis binary gerektirmez)
- **Dis bagimlilik:** Poppler (pdf2image icin) - yol `config.py` veya `POPPLER_PATH` env var ile ayarlanir
- **Konfigrasyon:** python-dotenv ile `.env` dosyasi destegi

## Mimari
- **Template sistemi:** `base.html` + `common.css` + `common.js` ile Jinja2 kalitim
- **Ortak CSS:** `static/common.css` - tum stiller burada (logo_removal haric)
- **Ortak JS:** `static/common.js` - formatSize, setupDropZone, uploadWithProgress, showToast vs.
- **Konfigrasyon:** `config.py` - tum ayarlar environment variable ile override edilebilir
- **Yardimci fonksiyonlar:** `utils.py` - api_success, api_error, safe_path, format_size
- **Katman sistemi:** `tiers.py` - ucretsiz/limitli/premium arac katmanlari (odeme altyapisi icin hazir)

## Dizin Yapisi
```
pdfedit/
├── app.py                  # Ana Flask uygulamasi - tum route'lar burada (~1270 satir)
├── config.py               # Merkezi konfigrasyon (env var destekli)
├── utils.py                # API yardimci fonksiyonlari (api_success, api_error, safe_path)
├── tiers.py                # Arac katmanlari ve rate limiting (odeme altyapisi)
├── requirements.txt        # Python bagimliliklari
├── tools/                  # PDF arac modulleri
│   ├── __init__.py         # Tum modulleri listeler
│   ├── pdf_merger.py       # merge_pdfs()
│   ├── pdf_splitter.py     # split_pdf_by_pages(), extract_pages()
│   ├── pdf_encryptor.py    # encrypt_pdf(), decrypt_pdf()
│   ├── img_to_pdf.py       # images_to_pdf(), get_image_info()
│   ├── watermark.py        # add_text_watermark(), add_image_watermark()
│   ├── pdf_compress.py     # compress_pdf(), get_pdf_size_info()
│   ├── pdf_rotate.py       # rotate_pdf()
│   ├── pdf_text_extract.py # extract_text(), extract_text_by_page()
│   ├── pdf_image_extract.py# extract_images(), get_image_count()
│   ├── pdf_reorder.py      # get_pdf_thumbnails(), reorder_pdf_pages(), delete_pdf_pages()
│   ├── pdf_repair.py       # repair_pdf(), try_deep_recovery(), analyze_pdf()
│   ├── pdf_to_image.py     # pdf_to_images(), pdf_to_images_zip()
│   ├── html_to_pdf.py      # html_to_pdf_from_string(), html_to_pdf_from_url() [WeasyPrint]
│   ├── pdf_metadata.py     # get_metadata(), update_metadata(), clear_metadata()
│   └── pdf_numbering.py    # add_page_numbers()
├── templates/              # Jinja2 HTML sablonlari
│   ├── base.html           # Temel sablon (tum araclar bunu extend eder)
│   ├── error.html          # Hata sayfalari (404, 413, 500)
│   ├── index.html          # Ana sayfa - tum araclarin listesi
│   ├── logo_removal.html   # Logo silme (SSE ile canli progress) [DOKUNMA]
│   ├── manual_selection.html # Manuel bolge secimi ile silme [DOKUNMA]
│   ├── merge.html          # PDF birlestirme (surukle-siralama, ozel dosya adi)
│   ├── split.html          # PDF bolme (sayfa sayisi, ZIP indirme)
│   ├── encrypt.html        # Sifreleme/cozme (sifre gucu, izin ozeti)
│   ├── img_to_pdf.html     # Gorsel -> PDF (onizleme, boyut/yon secimi)
│   ├── watermark.html      # Filigran (metin/gorsel, donme, renk secici)
│   ├── compress.html       # Sikistirma (kalite secenekleri, istatistik)
│   ├── rotate.html         # Dondurme (sayfa secici, thumbnail onizleme)
│   ├── extract_text.html   # Metin cikarma (kelime sayisi, TXT indirme)
│   ├── extract_images.html # Gorsel cikarma (detay gosterimi, lightbox)
│   ├── reorder.html        # Sayfa siralama (drag-drop, ters cevir, tasi)
│   ├── repair.html         # PDF onarma (analiz + onarim, metadata gosterimi)
│   ├── pdf_to_image.html   # PDF -> Gorsel (format/DPI secimi)
│   ├── html_to_pdf.html    # HTML -> PDF (kod/URL tabli, sayfa secenekleri)
│   ├── metadata.html       # Metadata duzenleyici (goruntule/duzenle/temizle)
│   └── numbering.html      # Sayfa numaralandirma (konum, format, onizleme)
├── static/
│   ├── common.css          # Ortak stiller (tum araclar icin)
│   ├── common.js           # Ortak JavaScript (dropzone, toast, upload vs.)
│   ├── style.css           # Sadece logo_removal icin stiller
│   └── script.js           # Sadece logo_removal icin JS
├── uploads/                # Gecici yukleme dizini (daemon thread ile temizlenir)
└── outputs/                # Cikti dosyalari (daemon thread ile temizlenir)
```

## Route - API Eslesmesi
| Route | API Endpoint(leri) | Tool Modulu |
|-------|-------------------|-------------|
| `/` | - | index.html |
| `/logo-removal` | `POST /upload`, `SSE /process/<job_id>` | app.py icinde (OpenCV SIFT) |
| `/manual-selection` | `POST /api/manual-upload` | app.py icinde |
| `/merge` | `POST /api/merge` | pdf_merger.py |
| `/split` | `POST /api/split` | pdf_splitter.py |
| `/encrypt` | `POST /api/encrypt`, `POST /api/decrypt` | pdf_encryptor.py |
| `/img-to-pdf` | `POST /api/img-to-pdf` | img_to_pdf.py |
| `/watermark` | `POST /api/watermark/text`, `POST /api/watermark/image` | watermark.py |
| `/compress` | `POST /api/compress` | pdf_compress.py |
| `/rotate` | `POST /api/rotate`, `POST /api/rotate-thumbnails` | pdf_rotate.py |
| `/extract-text` | `POST /api/extract-text` | pdf_text_extract.py |
| `/extract-images` | `POST /api/extract-images` | pdf_image_extract.py |
| `/reorder` | `POST /api/reorder-upload`, `POST /api/reorder-pages`, `POST /api/pdf-thumbnails` | pdf_reorder.py |
| `/repair` | `POST /api/pdf-analyze`, `POST /api/pdf-repair` | pdf_repair.py |
| `/pdf-to-image` | `POST /api/pdf-to-image` | pdf_to_image.py |
| `/html-to-pdf` | `POST /api/html-to-pdf` | html_to_pdf.py |
| `/metadata` | `POST /api/metadata`, `POST /api/metadata/update`, `POST /api/metadata/clear` | pdf_metadata.py |
| `/numbering` | `POST /api/numbering` | pdf_numbering.py |
| `/download/<filename>` | GET | Dosya indirme |
| `/download/<job_id>/<filename>` | GET | Split dosyasi indirme |
| `/download-image/<job_id>/<filename>` | GET | Cikarilan gorsel indirme |

## Guvenlik Onlemleri
- **Path traversal koruması:** `safe_path()` ile tum download endpoint'lerinde
- **Reorder guvenlik:** pdf_path istemciye gonderilmez, job_id ile progress_data'dan alinir
- **Metadata guvenlik:** Ayni pattern - job_id ile oturum yonetimi
- **Dosya dogrulama:** `allowed_file()` ile dosya uzantisi kontrolu
- **Dosya temizleme:** Daemon thread eski dosyalari otomatik siler (varsayilan 1 saat)
- **Progress temizleme:** Daemon thread eski progress kayitlarini temizler
- **HTTP Guvenlik Header'lari:** CSP, X-Frame-Options, X-Content-Type-Options, HSTS (production), Referrer-Policy
- **Hata mesaji guvenlik:** API hatalari generic mesaj dondurur, detay sadece log'da
- **Rate limiting:** limited_free tier araclari icin IP bazli gunluk limit (X-Forwarded-For destekli)
- **SECRET_KEY:** Production'da .env'den zorunlu, development'ta rastgele uretilir

## Production Deployment
```bash
# Development
python app.py                    # FLASK_DEBUG=true ile

# Production (Windows - Waitress)
python wsgi.py                   # veya: waitress-serve --port=5000 wsgi:app

# Production (Linux - Gunicorn)
gunicorn -w 1 --threads 4 -b 0.0.0.0:5000 wsgi:app

# Docker
docker-compose up -d
```

### Deployment Dosyalari
- `wsgi.py` - WSGI entry point (Gunicorn/Waitress)
- `Dockerfile` - Docker image (Python 3.12 + Poppler + WeasyPrint)
- `docker-compose.yml` - App + Nginx
- `nginx.conf` - Reverse proxy, SSL, statik dosya serve
- `.env.example` - Tum environment variable'lar
- `.dockerignore` - Docker build optimizasyonu

## Konfigrasyon (config.py / .env)
```
SECRET_KEY          - Flask secret key
MAX_CONTENT_LENGTH  - Max upload boyutu (varsayilan 100MB)
UPLOAD_FOLDER       - Yukleme klasoru (varsayilan 'uploads')
OUTPUT_FOLDER       - Cikti klasoru (varsayilan 'outputs')
POPPLER_PATH        - Poppler binary yolu
CLEANUP_MAX_AGE_HOURS - Dosya temizleme suresi (varsayilan 1 saat)
RATE_LIMIT_PER_MINUTE - Rate limit (varsayilan 30)
```

## Tasarim Sistemi
- **Tema:** Koyu arka plan, glassmorphism kartlar, gradient butonlar
- **Ortak stiller:** `static/common.css` - CSS degiskenleri, responsive, animasyonlar
- **Renkler:** Her aracin kendi gradient rengi var. Basari: #10b981, Hata: #ef4444
- **Animasyonlar:** fadeInUp, fadeInDown, hover translateY(-3px), shimmer progress bar
- **Responsive:** 3 sutun -> 2 sutun -> 1 sutun grid
- **Toast bildirimleri:** `showToast()` ile basari/hata/uyari
- **Template kalitim:** Tum araclar `base.html`'i extend eder (logo_removal ve index haric)

## Bilinen Sorunlar / TODO
1. **CSRF koruması:** Henuz yok
2. **pdf_compress.py:** PDF'i goruntulere cevirip geri PDF yapiyor - vektor/metin bilgisi kayboluyor
3. **manual_selection.html:** Template henuz base.html'e migrate edilmedi
4. **tiers.py:** Olusturuldu ama app.py route'larina entegre edilmedi (odeme sistemi eklenince aktif edilecek)
5. **WeasyPrint:** Windows'ta kurulumu zor olabilir, GTK gerektiriyor

## Katman Sistemi (tiers.py)
- **Ucretsiz:** merge, split, rotate, compress, img_to_pdf, extract_text (sinirsiz)
- **Limitli ucretsiz:** encrypt, watermark, extract_images, repair, pdf_to_image, reorder, numbering, metadata (gunluk 10)
- **Premium:** html_to_pdf, batch_processing, ocr, digital_signature, api_access

## Yeni Arac Ekleme Sablonu
1. `tools/` altina yeni modul ekle (fonksiyon return format: `{'success': True/False, ...}`)
2. `tools/__init__.py`'ye modul adini ekle
3. `app.py`'ye import, route ve API endpoint ekle
4. `templates/` altina HTML template ekle (`{% extends 'base.html' %}` kullan)
5. `index.html`'e arac karti ekle
6. `tiers.py`'de uygun katmana ekle

## Calistirma
```bash
pip install -r requirements.txt
python app.py
# http://localhost:5000
```
