/* A brief purple-and-gold celebration; the page remains usable underneath. */
(() => {
    const button = document.querySelector('[data-victory-confetti]');
    if (!button) return;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const colors = ['#4c1d95', '#7c3aed', '#a855f7', '#facc15', '#eab308', '#fde047'];
    let canvas, context, frame, previousTime, lastBurst = -Infinity;
    let particles = [];
    let width = 0, height = 0;

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        if (!canvas) return;
        const ratio = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(width * ratio);
        canvas.height = Math.round(height * ratio);
        context.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function stop() {
        cancelAnimationFrame(frame);
        frame = null;
        previousTime = null;
        particles = [];
        canvas?.remove();
        canvas = null;
        context = null;
    }

    function draw(time) {
        const dt = Math.min((time - (previousTime ?? time)) / 1000, 0.04);
        previousTime = time;
        context.clearRect(0, 0, width, height);
        particles = particles.filter(p => p.age < p.life && p.y < height + 30);
        for (const p of particles) {
            p.age += dt;
            p.vy += p.gravity * dt;
            p.x += (p.vx + Math.sin(p.age * 4 + p.phase) * 28) * dt;
            p.y += p.vy * dt;
            p.rotation += p.spin * dt;
            context.save();
            context.translate(p.x, p.y);
            context.rotate(p.rotation);
            context.globalAlpha = Math.min(1, Math.max(0, (p.life - p.age) / 0.65));
            context.fillStyle = p.color;
            context.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
            context.restore();
        }
        if (particles.length) frame = requestAnimationFrame(draw);
        else stop();
    }

    function celebrate(rain = false) {
        if (reducedMotion.matches || document.hidden) return;
        const now = performance.now();
        if (now - lastBurst < 800) return;
        lastBurst = now;
        if (!canvas) {
            canvas = document.createElement('canvas');
            canvas.className = 'home-victory-confetti';
            canvas.setAttribute('aria-hidden', 'true');
            context = canvas.getContext('2d');
            if (!context) { canvas = null; return; }
            document.body.append(canvas);
            resize();
        }
        const rect = button.getBoundingClientRect();
        const count = rain ? (width < 600 ? 90 : 155) : 65;
        for (let i = 0; i < count; i++) {
            particles.push({
                x: rain ? Math.random() * width : rect.left + rect.width / 2,
                y: rain ? -30 - Math.random() * height * 0.65 : rect.top + rect.height / 2,
                vx: (Math.random() - 0.5) * (rain ? 90 : 620),
                vy: rain ? 180 + Math.random() * 160 : -150 - Math.random() * 320,
                gravity: rain ? 65 : 420,
                age: 0, life: rain ? 4.6 : 2.8,
                rotation: Math.random() * Math.PI, spin: (Math.random() - 0.5) * 12,
                phase: Math.random() * Math.PI * 2, size: 7 + Math.random() * 7,
                color: colors[Math.floor(Math.random() * colors.length)],
            });
        }
        particles = particles.slice(-220);
        if (!frame) frame = requestAnimationFrame(draw);
    }

    button.addEventListener('pointerenter', event => {
        if (event.pointerType !== 'touch') celebrate();
    });
    button.addEventListener('click', () => celebrate());
    window.addEventListener('resize', resize, { passive: true });
    window.addEventListener('pagehide', stop);
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) stop(); });
    if (document.readyState === 'complete') celebrate(true);
    else window.addEventListener('load', () => celebrate(true), { once: true });
})();
