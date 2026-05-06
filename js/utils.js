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
