FROM python:3.12-slim

# System dependencies for PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium browser + dependencies
RUN playwright install --with-deps chromium

# Copy application
COPY . .

# Create required directories
RUN mkdir -p uploads outputs logs

# Environment
ENV FLASK_ENV=production
ENV PORT=5000
ENV POPPLER_PATH=""
ENV LOG_FILE=logs/pdfedit.log

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run with Gunicorn (Linux) - single worker with threads for in-memory state
CMD ["gunicorn", "-w", "1", "--threads", "4", "-b", "0.0.0.0:5000", "--timeout", "300", "--access-logfile", "-", "wsgi:app"]
