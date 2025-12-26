/**
 * PDF Edit - Cookie Consent & Google Analytics 4
 * GDPR/KVKK uyumlu: Kullanici onay vermeden hicbir analitik kodu yuklenmez.
 */

(function () {
    'use strict';

    var CONSENT_KEY = 'pdfedit_consent';
    var CONSENT_ACCEPTED = 'accepted';
    var CONSENT_REJECTED = 'rejected';

    // --- Cookie Consent Management ---

    /**
     * Returns the current consent status from localStorage.
     * @returns {string|null} 'accepted', 'rejected', or null if not yet recorded.
     */
    function getConsentStatus() {
        try {
            return localStorage.getItem(CONSENT_KEY);
        } catch (e) {
            return null;
        }
    }

    /**
     * Shows the cookie consent banner.
     */
    function showBanner() {
        var banner = document.getElementById('cookieConsent');
        if (banner) {
            banner.style.display = '';
            banner.removeAttribute('hidden');
        }
    }

    /**
     * Hides the cookie consent banner.
     */
    function hideBanner() {
        var banner = document.getElementById('cookieConsent');
        if (banner) {
            banner.style.display = 'none';
        }
    }

    /**
     * Called when user accepts cookies.
     * Stores consent, hides banner, and loads GA4.
     */
    function acceptConsent() {
        try {
            localStorage.setItem(CONSENT_KEY, CONSENT_ACCEPTED);
        } catch (e) {
            // localStorage unavailable, proceed without persisting
        }
        hideBanner();

        var measurementId = window.PDFEDIT_GA_ID || '';
        if (measurementId) {
            loadGA4(measurementId);
        }
    }

    /**
     * Called when user rejects cookies.
     * Stores rejection, hides banner. GA4 is NOT loaded.
     */
    function rejectConsent() {
        try {
            localStorage.setItem(CONSENT_KEY, CONSENT_REJECTED);
        } catch (e) {
            // localStorage unavailable, proceed without persisting
        }
        hideBanner();
    }

    /**
     * Initializes consent flow.
     * - If consent not yet recorded: show banner.
     * - If already accepted: load GA4 silently.
     * - If rejected: do nothing.
     */
    function initConsent() {
        var status = getConsentStatus();

        if (status === CONSENT_ACCEPTED) {
            hideBanner();
            var measurementId = window.PDFEDIT_GA_ID || '';
            if (measurementId) {
                loadGA4(measurementId);
            }
        } else if (status === CONSENT_REJECTED) {
            hideBanner();
        } else {
            // No consent recorded yet - show banner
            showBanner();
        }
    }

    // --- Google Analytics 4 Dynamic Loading ---

    var ga4Loaded = false;

    /**
     * Dynamically loads the GA4 gtag.js script and configures it.
     * Only loads if consent is given AND measurementId is not empty.
     * @param {string} measurementId - The GA4 measurement ID (e.g. 'G-XXXXXXXXXX').
     */
    function loadGA4(measurementId) {
        if (ga4Loaded) {
            return;
        }
        if (getConsentStatus() !== CONSENT_ACCEPTED) {
            return;
        }
        if (!measurementId) {
            return;
        }

        // Initialize the dataLayer and gtag function before the script loads
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () {
            window.dataLayer.push(arguments);
        };
        window.gtag('js', new Date());
        window.gtag('config', measurementId);

        // Create and insert the gtag.js script tag
        var script = document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
        var firstScript = document.getElementsByTagName('script')[0];
        if (firstScript && firstScript.parentNode) {
            firstScript.parentNode.insertBefore(script, firstScript);
        } else {
            document.head.appendChild(script);
        }

        ga4Loaded = true;
    }

    // --- Tool Usage Tracking ---

    /**
     * Sends a tool usage event to GA4.
     * Only tracks if consent has been given and GA4 is loaded.
     * @param {string} toolName - The name of the tool (e.g. 'merge', 'split', 'compress').
     * @param {string} action - The action performed: 'upload', 'process', or 'download'.
     */
    function trackToolUsage(toolName, action) {
        if (getConsentStatus() !== CONSENT_ACCEPTED) {
            return;
        }
        if (typeof window.gtag !== 'function') {
            return;
        }

        window.gtag('event', 'tool_usage', {
            tool_name: toolName,
            tool_action: action
        });
    }

    // --- Initialization ---

    document.addEventListener('DOMContentLoaded', function () {
        initConsent();
    });

    // --- Public API ---

    window.PDFEditAnalytics = {
        acceptConsent: acceptConsent,
        rejectConsent: rejectConsent,
        initConsent: initConsent,
        trackToolUsage: trackToolUsage,
        getConsentStatus: getConsentStatus
    };

})();
