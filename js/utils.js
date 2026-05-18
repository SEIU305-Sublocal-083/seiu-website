window.Sentinel = window.Sentinel || {};

/**
 * Escapes HTML characters in a string to prevent XSS.
 * @param {string} unsafe The unsafe string.
 * @returns {string} The escaped string.
 */
window.Sentinel.escapeHTML = function (unsafe) {
    if (unsafe == null) return '';
    return String(unsafe)
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
};

/**
 * Sanitizes URLs to prevent javascript: or data: injection.
 * @param {string} url The unsafe URL.
 * @returns {string} The sanitized URL, or '#' if invalid.
 */
window.Sentinel.sanitizeUrl = function (url) {
    if (!url) return '#';
    const str = String(url).trim();
    const lower = str.toLowerCase();
    if (lower.startsWith('javascript:') || lower.startsWith('data:')) {
        return '#';
    }
    return str;
};
