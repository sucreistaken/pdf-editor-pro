#!/bin/bash
# ===========================================
# PDF Edit - GCP VM Deployment Script
# ===========================================
# Usage: Run on a fresh Ubuntu 22.04 VM
#   curl -fsSL raw.githubusercontent.com/sucreistaken/pdf-editor-pro/main/deploy.sh | bash
# ===========================================

set -e

REPO_URL="https://github.com/sucreistaken/pdf-editor-pro.git"
APP_DIR="$HOME/pdf-editor-pro"

echo "=========================================="
echo " PDF Edit - Deployment Baslatiliyor"
echo "=========================================="

# 1. Sistem guncelleme
echo "[1/6] Sistem guncelleniyor..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Docker kurulumu
echo "[2/6] Docker kuruluyor..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker "$USER"
    echo "  Docker kuruldu."
else
    echo "  Docker zaten kurulu."
fi

# 3. Docker Compose kurulumu (plugin)
echo "[3/6] Docker Compose kontrol ediliyor..."
if ! docker compose version &> /dev/null; then
    sudo apt-get install -y docker-compose-plugin
    echo "  Docker Compose plugin kuruldu."
else
    echo "  Docker Compose zaten kurulu."
fi

# 4. Repo clone
echo "[4/6] Repo klonlaniyor..."
if [ -d "$APP_DIR" ]; then
    echo "  Dizin mevcut, guncelleniyor..."
    cd "$APP_DIR"
    git pull
else
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# 5. Certs klasoru olustur
echo "[5/6] Sertifika klasoru hazirlaniyor..."
mkdir -p certs
if [ ! -f certs/origin.pem ] || [ ! -f certs/origin-key.pem ]; then
    echo ""
    echo "  !! ONEMLI: Cloudflare Origin Certificate gerekli !!"
    echo "  Asagidaki dosyalari olusturun:"
    echo "    nano $APP_DIR/certs/origin.pem       (Certificate PEM)"
    echo "    nano $APP_DIR/certs/origin-key.pem   (Private Key PEM)"
    echo ""
    echo "  Cloudflare Dashboard -> SSL/TLS -> Origin Server -> Create Certificate"
    echo ""
fi

# 6. .env dosyasi olustur
echo "[6/6] .env dosyasi hazirlaniyor..."
if [ ! -f .env ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    cat > .env << EOF
SECRET_KEY=${SECRET_KEY}
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
CLEANUP_MAX_AGE_HOURS=1
RATE_LIMIT_PER_MINUTE=30
SITE_URL=https://pdf.kadiray.com
LOG_LEVEL=INFO
LOG_FILE=logs/pdfedit.log
EOF
    echo "  .env olusturuldu (SECRET_KEY otomatik uretildi)."
else
    echo "  .env zaten mevcut, atlanıyor."
fi

echo ""
echo "=========================================="
echo " Kurulum Tamamlandi!"
echo "=========================================="
echo ""
echo " Sonraki adimlar:"
echo "   1. Cloudflare origin cert/key dosyalarini kopyalayin:"
echo "      nano $APP_DIR/certs/origin.pem"
echo "      nano $APP_DIR/certs/origin-key.pem"
echo ""
echo "   2. Uygulamayi baslatin:"
echo "      cd $APP_DIR"
echo "      docker compose up -d --build"
echo ""
echo "   3. Kontrol:"
echo "      docker compose ps"
echo "      curl -k https://localhost"
echo ""
echo "   4. https://pdf.kadiray.com adresini test edin"
echo "=========================================="
