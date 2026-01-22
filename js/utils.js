/**
 * Utility functions for SEIU Local 503 Website
 */

// Global namespace for utilities
window.Sentinel = window.Sentinel || {};

/**
 * Escapes HTML characters in a string to prevent XSS.
 * @param {string} str - The string to escape.
 * @returns {string} The escaped string.
 */
window.Sentinel.escapeHTML = function(str) {
    if (!str) return '';
    return String(str).replace(/[&<>'"]/g,
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag]));
};
