/**
 * PDFEdit - Ortak JavaScript
 */

// ==================== I18N Helper ====================
function __(key, params) {
    const strings = window.PDFEDIT_STRINGS || {};
    let text = strings[key] || key;
    if (params) {
        Object.keys(params).forEach(k => {
            text = text.replace('{' + k + '}', params[k]);
        });
    }
    return text;
}

// ==================== CSRF Token ====================
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// ==================== Analytics Event Tracking ====================
function trackToolUsage(toolName, action) {
    if (typeof gtag === 'function' && localStorage.getItem('pdfedit_consent') === 'accepted') {
        gtag('event', 'tool_usage', {
            'tool_name': toolName,
            'action': action,
            'event_category': 'PDF Tools'
        });
    }
}

// Dosya boyutu formatlama
function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + units[i];
}

// Drop zone kurulumu
function setupDropZone(dropZoneEl, fileInputEl, options = {}) {
    const accept = options.accept || '.pdf';
    const multiple = options.multiple || false;
    const onFiles = options.onFiles || (() => {});
    const maxSize = options.maxSize || 500 * 1024 * 1024; // 500MB

    dropZoneEl.addEventListener('click', () => fileInputEl.click());

    dropZoneEl.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZoneEl.classList.add('drag-over');
    });

    dropZoneEl.addEventListener('dragleave', () => {
        dropZoneEl.classList.remove('drag-over');
    });

    dropZoneEl.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZoneEl.classList.remove('drag-over');
        const files = filterFiles(e.dataTransfer.files, accept, maxSize);
        if (files.length > 0) onFiles(files);
    });

    fileInputEl.addEventListener('change', (e) => {
        const files = filterFiles(e.target.files, accept, maxSize);
        if (files.length > 0) onFiles(files);
        fileInputEl.value = '';
    });
}

function filterFiles(fileList, accept, maxSize) {
    const validExts = accept.split(',').map(e => e.trim().toLowerCase());
    const valid = [];
    for (let file of fileList) {
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        if (validExts.includes(ext) || validExts.includes('.' + file.type.split('/').pop())) {
            if (file.size > maxSize) {
                showToast(`${file.name} çok büyük! Maks: ${formatSize(maxSize)}`, 'error');
                continue;
            }
            valid.push(file);
        } else {
            showToast(`${file.name} geçersiz dosya türü`, 'error');
        }
    }
    return valid;
}

// PDF dogrulama
function validatePDF(file) {
    if (!file) return false;
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'pdf') {
        showToast('Lütfen bir PDF dosyası seçin', 'error');
        return false;
    }
    if (file.size > 500 * 1024 * 1024) {
        showToast('Dosya çok büyük! Maksimum: 500 MB', 'error');
        return false;
    }
    return true;
}

// Gorsel dogrulama
function validateImage(file) {
    if (!file) return false;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'].includes(ext)) {
        showToast('Geçersiz görsel formatı', 'error');
        return false;
    }
    if (file.size > 500 * 1024 * 1024) {
        showToast('Dosya çok büyük! Maksimum: 500 MB', 'error');
        return false;
    }
    return true;
}

// Toast bildirimi
function showToast(message, type = 'info', duration = 4000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Yukleme progress ile XHR
function uploadWithProgress(url, formData, options = {}) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader('X-CSRFToken', getCSRFToken());

        if (options.onProgress) {
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    options.onProgress(percent, e.loaded, e.total);
                }
            });
        }

        xhr.addEventListener('load', () => {
            try {
                const data = JSON.parse(xhr.responseText);
                resolve(data);
            } catch (e) {
                reject(new Error('Sunucu yanıtı ayrıştırılamadı'));
            }
        });

        xhr.addEventListener('error', () => reject(new Error('Bağlantı hatası')));
        xhr.addEventListener('timeout', () => reject(new Error('İstek zaman aşımına uğradı')));

        xhr.timeout = options.timeout || 300000; // 5 dakika
        xhr.send(formData);
    });
}

// Tab sistemi
function setupTabs(tabBtns, tabContents) {
    tabBtns.forEach((btn, i) => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            tabContents[i].classList.add('active');
        });
    });
}

// Sifre gucu gostergesi
function checkPasswordStrength(password) {
    let score = 0;
    if (password.length >= 6) score++;
    if (password.length >= 10) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    if (score <= 2) return { level: 'weak', text: 'Zayıf', color: '#ef4444' };
    if (score <= 3) return { level: 'medium', text: 'Orta', color: '#f59e0b' };
    return { level: 'strong', text: 'Güçlü', color: '#10b981' };
}

// ==================== PDF Onizleme ====================
async function loadPreview(file, previewContainer, options = {}) {
    const page = options.page || 0;
    const width = options.width || 400;
    const onLoad = options.onLoad || null;

    // Placeholder goster
    previewContainer.innerHTML = '<div class="skeleton" style="width:100%;height:300px;"></div>';

    const formData = new FormData();
    formData.append('pdf_file', file);
    formData.append('page', page);
    formData.append('width', width);

    try {
        const resp = await fetch('/api/preview', { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCSRFToken() } });
        const data = await resp.json();

        if (data.success) {
            const img = document.createElement('img');
            img.className = 'preview-page';
            img.alt = __('preview_page') + ' ' + (page + 1);
            img.onload = function() {
                if (onLoad) onLoad(data);
            };
            previewContainer.innerHTML = '';
            previewContainer.appendChild(img);
            img.src = data.image;
            return data;
        } else {
            previewContainer.innerHTML = '<div class="preview-placeholder"><p>' + __('preview_load_error') + '</p></div>';
            return null;
        }
    } catch (e) {
        previewContainer.innerHTML = '<div class="preview-placeholder"><p>' + __('preview_error') + '</p></div>';
        return null;
    }
}

// ==================== Inline Preview Helper ====================
async function showInlinePreview(file, container, options = {}) {
    container.style.display = 'block';
    // Store file reference and state on the container for navigation
    container._previewFile = file;
    container._previewPage = 0;
    container._previewTotalPages = 1;
    container._onPageChange = options.onPageChange || null;

    const data = await loadPreview(file, container, { width: 500 });
    if (data && data.total_pages) {
        container._previewTotalPages = data.total_pages;

        // Remove old nav/info if re-rendering
        const oldNav = container.querySelector('.inline-preview-nav');
        if (oldNav) oldNav.remove();
        const oldInfo = container.querySelector('.preview-page-info');
        if (oldInfo) oldInfo.remove();

        if (data.total_pages > 1) {
            // Page navigation bar
            const nav = document.createElement('div');
            nav.className = 'inline-preview-nav';
            nav.innerHTML = `
                <button class="ip-nav-btn ip-prev" disabled>&lsaquo;</button>
                <span class="ip-nav-info">1 / ${data.total_pages}</span>
                <button class="ip-nav-btn ip-next">&rsaquo;</button>
            `;
            container.appendChild(nav);

            const prevBtn = nav.querySelector('.ip-prev');
            const nextBtn = nav.querySelector('.ip-next');
            const info = nav.querySelector('.ip-nav-info');

            prevBtn.addEventListener('click', () => _inlinePreviewNav(container, -1));
            nextBtn.addEventListener('click', () => _inlinePreviewNav(container, 1));
        } else {
            // Single page: just show page count info
            const info = document.createElement('div');
            info.className = 'preview-page-info';
            info.textContent = '1 ' + (__('pages') || 'sayfa');
            container.appendChild(info);
        }
    }
    return data;
}

async function _inlinePreviewNav(container, direction) {
    const page = container._previewPage + direction;
    const total = container._previewTotalPages;
    if (page < 0 || page >= total) return;

    container._previewPage = page;
    const nav = container.querySelector('.inline-preview-nav');
    if (!nav) return;

    const prevBtn = nav.querySelector('.ip-prev');
    const nextBtn = nav.querySelector('.ip-next');
    const info = nav.querySelector('.ip-nav-info');

    prevBtn.disabled = true;
    nextBtn.disabled = true;
    info.textContent = (page + 1) + ' / ' + total;

    await loadPreview(container._previewFile, container, { width: 500, page: page });

    // Re-append nav (loadPreview clears container)
    container.appendChild(nav);
    prevBtn.disabled = page === 0;
    nextBtn.disabled = page >= total - 1;
    info.textContent = (page + 1) + ' / ' + total;

    if (container._onPageChange) {
        container._onPageChange(page, total);
    }
}

// ==================== Filigran Onizleme ====================
function updateWatermarkPreview(container, text, options = {}) {
    const pos = options.position || 'center';
    const fontSize = options.fontSize || 50;
    const rotation = options.rotation || 0;
    const color = options.color || '#808080';
    const opacity = options.opacity || 0.3;

    let overlay = container.querySelector('.preview-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'preview-overlay';
        container.appendChild(overlay);
    }

    let wm = overlay.querySelector('.preview-watermark');
    if (!wm) {
        wm = document.createElement('div');
        wm.className = 'preview-watermark';
        overlay.appendChild(wm);
    }

    wm.textContent = text || '';

    // Onizlemedeki font boyutu olcekleme (gercek PDF boyutu icin yaklasik)
    const scaledFontSize = Math.max(8, fontSize * 0.35);
    wm.style.fontSize = scaledFontSize + 'px';
    wm.style.color = color;
    wm.style.opacity = opacity;
    wm.style.transform = `rotate(${rotation}deg)`;

    // Pozisyon
    const posMap = {
        'center':       { top: '50%', left: '50%', transform: `translate(-50%,-50%) rotate(${rotation}deg)` },
        'top-left':     { top: '8%', left: '8%', transform: `rotate(${rotation}deg)` },
        'top-right':    { top: '8%', right: '8%', left: 'auto', transform: `rotate(${rotation}deg)` },
        'bottom-left':  { bottom: '8%', top: 'auto', left: '8%', transform: `rotate(${rotation}deg)` },
        'bottom-right': { bottom: '8%', top: 'auto', right: '8%', left: 'auto', transform: `rotate(${rotation}deg)` },
    };

    // Reset
    Object.assign(wm.style, { top: '', left: '', right: '', bottom: '' });
    const posStyle = posMap[pos] || posMap['center'];
    Object.assign(wm.style, posStyle);
}

// ==================== Gorsel Filigran Onizleme ====================
function updateImageWatermarkPreview(container, imageSrc, options = {}) {
    const pos = options.position || 'center';
    const opacity = options.opacity || 0.5;

    let overlay = container.querySelector('.preview-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'preview-overlay';
        container.appendChild(overlay);
    }

    let wmImg = overlay.querySelector('.preview-watermark-img');
    if (!wmImg) {
        wmImg = document.createElement('img');
        wmImg.className = 'preview-watermark-img';
        overlay.appendChild(wmImg);
    }

    wmImg.src = imageSrc;
    wmImg.style.opacity = opacity;
    wmImg.style.maxWidth = '40%';
    wmImg.style.maxHeight = '40%';

    // Reset position styles
    Object.assign(wmImg.style, { top: '', left: '', right: '', bottom: '', transform: '' });

    const posMap = {
        'center':       { top: '50%', left: '50%', transform: 'translate(-50%,-50%)' },
        'top-left':     { top: '8%', left: '8%' },
        'top-right':    { top: '8%', right: '8%', left: 'auto' },
        'bottom-left':  { bottom: '8%', top: 'auto', left: '8%' },
        'bottom-right': { bottom: '8%', top: 'auto', right: '8%', left: 'auto' },
    };

    const posStyle = posMap[pos] || posMap['center'];
    Object.assign(wmImg.style, posStyle);
}

// ==================== Numara Onizleme ====================
function updateNumberPreview(container, options = {}) {
    const pos = options.position || 'bottom-center';
    const format = options.format || '{n}';
    const fontSize = options.fontSize || 12;
    const number = options.number || 1;
    const total = options.total || 10;

    let overlay = container.querySelector('.preview-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'preview-overlay';
        container.appendChild(overlay);
    }

    let numEl = overlay.querySelector('.preview-number');
    if (!numEl) {
        numEl = document.createElement('div');
        numEl.className = 'preview-number';
        overlay.appendChild(numEl);
    }

    const text = format.replace('{n}', number).replace('{total}', total);
    numEl.textContent = text;

    const scaledFontSize = Math.max(8, fontSize * 0.9);
    numEl.style.fontSize = scaledFontSize + 'px';
    numEl.style.color = 'rgba(0,0,0,0.8)';

    // Reset
    Object.assign(numEl.style, { top: '', left: '', right: '', bottom: '', transform: '' });

    const posMap = {
        'top-left':      { top: '5%', left: '8%' },
        'top-center':    { top: '5%', left: '50%', transform: 'translateX(-50%)' },
        'top-right':     { top: '5%', right: '8%', left: 'auto' },
        'bottom-left':   { bottom: '5%', top: 'auto', left: '8%' },
        'bottom-center': { bottom: '5%', top: 'auto', left: '50%', transform: 'translateX(-50%)' },
        'bottom-right':  { bottom: '5%', top: 'auto', right: '8%', left: 'auto' },
    };

    const posStyle = posMap[pos] || posMap['bottom-center'];
    Object.assign(numEl.style, posStyle);
}

// ==================== Adim Gostergesi ====================
function initSteps(containerEl) {
    const steps = containerEl.querySelectorAll('.step');
    const lines = containerEl.querySelectorAll('.step-line');

    return {
        setStep(n) {
            steps.forEach((step, i) => {
                step.classList.remove('active', 'completed');
                if (i < n) step.classList.add('completed');
                else if (i === n) step.classList.add('active');
            });
            lines.forEach((line, i) => {
                line.classList.toggle('completed', i < n);
            });
        }
    };
}

// ==================== Ilgili Araclar ====================
const RELATED_TOOLS = {
    'merge':          [{ icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔢', name: 'Numaralandirma', url: '/numbering' }, { icon: '💧', name: 'Filigran', url: '/watermark' }],
    'split':          [{ icon: '🔗', name: 'Birlestirme', url: '/merge' }, { icon: '📑', name: 'Sayfa Siralama', url: '/reorder' }, { icon: '📝', name: 'Metin Cikarma', url: '/extract-text' }],
    'encrypt':        [{ icon: '💧', name: 'Filigran', url: '/watermark' }, { icon: '🏷️', name: 'Metadata', url: '/metadata' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'img-to-pdf':     [{ icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '💧', name: 'Filigran', url: '/watermark' }, { icon: '🔗', name: 'Birlestirme', url: '/merge' }],
    'watermark':      [{ icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔒', name: 'Sifreleme', url: '/encrypt' }, { icon: '🔢', name: 'Numaralandirma', url: '/numbering' }],
    'compress':       [{ icon: '🔗', name: 'Birlestirme', url: '/merge' }, { icon: '💧', name: 'Filigran', url: '/watermark' }, { icon: '🔢', name: 'Numaralandirma', url: '/numbering' }],
    'rotate':         [{ icon: '📑', name: 'Sayfa Siralama', url: '/reorder' }, { icon: '✂️', name: 'Bolme', url: '/split' }, { icon: '📸', name: 'PDF > Gorsel', url: '/pdf-to-image' }],
    'extract-text':   [{ icon: '🖼️', name: 'Gorsel Cikarma', url: '/extract-images' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔗', name: 'Birlestirme', url: '/merge' }],
    'extract-images': [{ icon: '📝', name: 'Metin Cikarma', url: '/extract-text' }, { icon: '📸', name: 'PDF > Gorsel', url: '/pdf-to-image' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'reorder':        [{ icon: '🔄', name: 'Dondurme', url: '/rotate' }, { icon: '✂️', name: 'Bolme', url: '/split' }, { icon: '🔗', name: 'Birlestirme', url: '/merge' }],
    'repair':         [{ icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🏷️', name: 'Metadata', url: '/metadata' }, { icon: '🔗', name: 'Birlestirme', url: '/merge' }],
    'pdf-to-image':   [{ icon: '🖼️', name: 'Gorsel > PDF', url: '/img-to-pdf' }, { icon: '📝', name: 'Metin Cikarma', url: '/extract-text' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'html-to-pdf':    [{ icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '💧', name: 'Filigran', url: '/watermark' }, { icon: '🏷️', name: 'Metadata', url: '/metadata' }],
    'metadata':       [{ icon: '🔒', name: 'Sifreleme', url: '/encrypt' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔧', name: 'Onarma', url: '/repair' }],
    'numbering':      [{ icon: '💧', name: 'Filigran', url: '/watermark' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔗', name: 'Birlestirme', url: '/merge' }],
    'crop':           [{ icon: '🔄', name: 'Dondurme', url: '/rotate' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '✂️', name: 'Bolme', url: '/split' }],
    'compare':        [{ icon: '🔗', name: 'Birlestirme', url: '/merge' }, { icon: '🏷️', name: 'Metadata', url: '/metadata' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'pdf-to-excel':   [{ icon: '📝', name: 'Metin Cikarma', url: '/extract-text' }, { icon: '📄', name: 'PDF > Word', url: '/pdf-to-word' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'form-fill':      [{ icon: '🏷️', name: 'Metadata', url: '/metadata' }, { icon: '🔒', name: 'Sifreleme', url: '/encrypt' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'pdf-to-word':    [{ icon: '📊', name: 'PDF > Excel', url: '/pdf-to-excel' }, { icon: '📝', name: 'Metin Cikarma', url: '/extract-text' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }],
    'pdf-to-pdfa':    [{ icon: '🏷️', name: 'Metadata', url: '/metadata' }, { icon: '📦', name: 'Sikistirma', url: '/compress' }, { icon: '🔒', name: 'Sifreleme', url: '/encrypt' }],
};

function showRelatedTools(container, currentTool) {
    const tools = RELATED_TOOLS[currentTool];
    if (!tools || !container) return;

    const lang = window.PDFEDIT_LANG || 'tr';
    const title = __('try_also');

    container.innerHTML = `
        <div class="related-tools">
            <div class="related-tools-title">${title}</div>
            <div class="related-tools-list">
                ${tools.map(t => `<a href="/${lang}${t.url}" class="related-tool-link">${t.icon} ${t.name}</a>`).join('')}
            </div>
        </div>
    `;
}

// Surukle birak siralama
function enableDragSort(container, itemSelector, onReorder) {
    let dragItem = null;
    let dragIndex = -1;

    container.addEventListener('dragstart', (e) => {
        dragItem = e.target.closest(itemSelector);
        if (!dragItem) return;
        dragIndex = [...container.querySelectorAll(itemSelector)].indexOf(dragItem);
        dragItem.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
    });

    container.addEventListener('dragover', (e) => {
        e.preventDefault();
        const target = e.target.closest(itemSelector);
        if (!target || target === dragItem) return;

        const items = [...container.querySelectorAll(itemSelector)];
        const targetIndex = items.indexOf(target);

        if (targetIndex > dragIndex) {
            target.parentNode.insertBefore(dragItem, target.nextSibling);
        } else {
            target.parentNode.insertBefore(dragItem, target);
        }
    });

    container.addEventListener('dragend', () => {
        if (dragItem) {
            dragItem.style.opacity = '1';
            dragItem = null;
            if (onReorder) onReorder();
        }
    });
}
