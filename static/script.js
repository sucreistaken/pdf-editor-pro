// PDF Logo Temizleyici - JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const pdfDropZone = document.getElementById('pdfDropZone');
    const logoDropZone = document.getElementById('logoDropZone');
    const pdfInput = document.getElementById('pdfInput');
    const logoInput = document.getElementById('logoInput');
    const pdfFileName = document.getElementById('pdfFileName');
    const logoFileName = document.getElementById('logoFileName');
    const logoPreview = document.getElementById('logoPreview');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const customFilename = document.getElementById('customFilename');

    // Sections
    const uploadSection = document.getElementById('uploadSection');
    const progressSection = document.getElementById('progressSection');
    const successSection = document.getElementById('successSection');
    const errorSection = document.getElementById('errorSection');

    // Progress elements
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const pageCounter = document.getElementById('pageCounter');
    const logContent = document.getElementById('logContent');

    // Result elements
    const downloadBtn = document.getElementById('downloadBtn');
    const downloadFileName = document.getElementById('downloadFileName');
    const errorMessage = document.getElementById('errorMessage');

    let pdfFile = null;
    let logoFile = null;

    // Drop Zone Handlers
    pdfDropZone.addEventListener('click', () => pdfInput.click());
    logoDropZone.addEventListener('click', () => logoInput.click());

    pdfInput.addEventListener('change', (e) => handleFile(e.target.files[0], 'pdf'));
    logoInput.addEventListener('change', (e) => handleFile(e.target.files[0], 'logo'));

    [pdfDropZone, logoDropZone].forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });

        zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            const type = zone.id === 'pdfDropZone' ? 'pdf' : 'logo';
            handleFile(file, type);
        });
    });

    function handleFile(file, type) {
        if (!file) return;

        if (type === 'pdf') {
            if (!file.name.toLowerCase().endsWith('.pdf')) {
                showToast('Lütfen bir PDF dosyası seçin!', 'error');
                return;
            }
            pdfFile = file;
            pdfFileName.textContent = file.name;
            pdfDropZone.classList.add('has-file');

            // Dosya adı önerisi
            if (!customFilename.value) {
                const baseName = file.name.replace('.pdf', '').replace('.PDF', '');
                customFilename.value = baseName + '_temiz';
            }
        } else {
            const ext = file.name.split('.').pop().toLowerCase();
            if (!['png', 'jpg', 'jpeg'].includes(ext)) {
                showToast('Lütfen PNG, JPG veya JPEG formatında logo seçin!', 'error');
                return;
            }
            logoFile = file;
            logoFileName.textContent = file.name;
            logoDropZone.classList.add('has-file');

            const reader = new FileReader();
            reader.onload = (e) => {
                logoPreview.innerHTML = `<img src="${e.target.result}" alt="Logo">`;
            };
            reader.readAsDataURL(file);
        }

        updateSubmitButton();
    }

    function updateSubmitButton() {
        submitBtn.disabled = !(pdfFile && logoFile);
    }

    // Form Submit
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!pdfFile || !logoFile) return;

        const formData = new FormData();
        formData.append('pdf_file', pdfFile);
        formData.append('logo_file', logoFile);
        formData.append('custom_filename', customFilename.value || 'temiz');

        // Show progress section
        showSection('progress');
        resetProgress();

        try {
            // Step 1: Upload files
            const csrfMeta = document.querySelector('meta[name="csrf-token"]');
            const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrfToken }
            });

            const uploadResult = await uploadResponse.json();

            if (!uploadResponse.ok || !uploadResult.success) {
                throw new Error(uploadResult.error || 'Yükleme hatası');
            }

            // Step 2: Start processing with SSE
            const eventSource = new EventSource(`/process/${uploadResult.job_id}`);

            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.error) {
                    eventSource.close();
                    showError(data.error);
                    return;
                }

                if (data.log) {
                    addLog(data.log);
                }

                if (data.progress !== undefined) {
                    updateProgress(data.progress);
                }

                if (data.current_page) {
                    pageCounter.innerHTML = `<span>Sayfa ${data.current_page} işleniyor...</span>`;
                }

                if (data.complete) {
                    eventSource.close();

                    // Build download URL with custom name
                    const downloadName = data.download_name || 'temiz.pdf';
                    downloadBtn.href = `/download/${data.download_id}?name=${encodeURIComponent(downloadName)}`;
                    downloadFileName.textContent = downloadName.endsWith('.pdf') ? downloadName : downloadName + '.pdf';

                    setTimeout(() => showSection('success'), 500);
                }
            };

            eventSource.onerror = () => {
                eventSource.close();
                showError('Bağlantı hatası oluştu');
            };

        } catch (error) {
            showError(error.message);
        }
    });

    function showSection(section) {
        uploadSection.classList.add('hidden');
        progressSection.classList.add('hidden');
        successSection.classList.add('hidden');
        errorSection.classList.add('hidden');

        switch (section) {
            case 'upload': uploadSection.classList.remove('hidden'); break;
            case 'progress': progressSection.classList.remove('hidden'); break;
            case 'success': successSection.classList.remove('hidden'); break;
            case 'error': errorSection.classList.remove('hidden'); break;
        }
    }

    function resetProgress() {
        progressBar.style.width = '0%';
        progressPercent.textContent = '0%';
        pageCounter.innerHTML = '<span>Hazırlanıyor...</span>';
        logContent.innerHTML = '';
    }

    function updateProgress(percent) {
        progressBar.style.width = percent + '%';
        progressPercent.textContent = percent + '%';
    }

    function addLog(message) {
        const line = document.createElement('div');
        line.className = 'log-line';
        line.textContent = message;
        logContent.appendChild(line);
        logContent.scrollTop = logContent.scrollHeight;
    }

    function showError(message) {
        errorMessage.textContent = message;
        showSection('error');
    }

    // Global reset function
    window.resetAll = function () {
        pdfFile = null;
        logoFile = null;
        pdfFileName.textContent = 'Dosya seçilmedi';
        logoFileName.textContent = 'Dosya seçilmedi';
        logoPreview.innerHTML = '';
        pdfDropZone.classList.remove('has-file');
        logoDropZone.classList.remove('has-file');
        pdfInput.value = '';
        logoInput.value = '';
        customFilename.value = '';
        submitBtn.disabled = true;
        showSection('upload');
    };

    // Toast
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            padding: 14px 28px;
            background: ${type === 'error' ? '#ef4444' : '#667eea'};
            color: white;
            border-radius: 8px;
            font-weight: 500;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: toastIn 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes toastIn {
            from { opacity: 0; transform: translate(-50%, 20px); }
            to { opacity: 1; transform: translate(-50%, 0); }
        }
        @keyframes toastOut {
            from { opacity: 1; transform: translate(-50%, 0); }
            to { opacity: 0; transform: translate(-50%, 20px); }
        }
    `;
    document.head.appendChild(style);
});
