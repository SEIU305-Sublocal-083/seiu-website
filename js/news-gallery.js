document.querySelectorAll('[data-news-gallery]').forEach(gallery => {
    const slides = [...gallery.querySelectorAll('[data-gallery-slide]')];
    const controls = gallery.querySelector('[data-gallery-controls]');
    const counter = gallery.querySelector('[data-gallery-counter]');
    if (slides.length < 2 || !controls || !counter) return;
    let current = 0;
    const show = index => {
        current = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => { slide.hidden = i !== current; });
        counter.textContent = `Photo ${current + 1} of ${slides.length}`;
    };
    gallery.querySelector('[data-gallery-previous]').addEventListener('click', () => show(current - 1));
    gallery.querySelector('[data-gallery-next]').addEventListener('click', () => show(current + 1));
    gallery.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        if (event.target.closest('a, input, textarea, select')) return;
        event.preventDefault();
        show(event.key === 'Home' ? 0 : event.key === 'End' ? slides.length - 1 : current + (event.key === 'ArrowRight' ? 1 : -1));
    });
    let touchStart;
    gallery.addEventListener('touchstart', event => {
        if (event.touches.length !== 1 || !event.target.closest('[data-gallery-slide] img')) { touchStart = null; return; }
        touchStart = {x: event.touches[0].clientX, y: event.touches[0].clientY};
    }, {passive: true});
    gallery.addEventListener('touchend', event => {
        if (!touchStart || !event.changedTouches.length) return;
        const dx = event.changedTouches[0].clientX - touchStart.x;
        const dy = event.changedTouches[0].clientY - touchStart.y;
        touchStart = null;
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
    }, {passive: true});
    gallery.addEventListener('touchcancel', () => { touchStart = null; }, {passive: true});
    gallery.classList.add('news-gallery-ready');
    controls.hidden = false;
    show(0);
});
