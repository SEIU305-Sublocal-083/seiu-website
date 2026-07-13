/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.html', './js/**/*.js'],
  theme: {
    extend: {
      colors: {
        'brand-purple-dark': 'var(--brand-purple-dark)',
        'brand-purple': 'var(--brand-purple)',
        'brand-purple-light': 'var(--brand-purple-light)',
        'brand-dark': 'var(--brand-dark)',
        'brand-light': 'var(--brand-light)',
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'border-color': 'var(--border-color)'
      }
    }
  },
  plugins: []
};
