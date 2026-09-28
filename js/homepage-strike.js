/* The campaign status is editorial; the clock only measures its confirmed start. */
(() => {
    const units = ['days', 'hours', 'minutes', 'seconds'];

    function clockState(clock, now) {
        const start = Date.parse(clock?.startsAt);
        if (clock?.status !== 'confirmed' || !Number.isFinite(start)) return { phase: 'update' };
        const active = now >= start;
        const seconds = active ? Math.floor((now - start) / 1000) : Math.ceil((start - now) / 1000);
        return {
            phase: active ? 'active' : 'countdown',
            hour: active ? Math.floor(seconds / 3600) + 1 : null,
            values: [Math.floor(seconds / 86400), Math.floor(seconds % 86400 / 3600), Math.floor(seconds % 3600 / 60), seconds % 60],
        };
    }

    if (typeof module !== 'undefined' && module.exports) module.exports = { clockState };
    if (typeof document === 'undefined') return;
    const timer = document.querySelector('[data-home-strike-clock]');
    const configElement = document.getElementById('homepage-strike-config');
    if (!timer || !configElement) return;
    let config;
    try { config = JSON.parse(configElement.textContent); } catch { return; }
    let lastPhase;
    const announcer = document.createElement('p');
    announcer.className = 'sr-only';
    announcer.setAttribute('role', 'status');
    timer.append(announcer);
    const setText = (selector, value) => {
        const element = document.querySelector(selector);
        if (element && element.textContent !== value) element.textContent = value;
    };

    function render() {
        if (!config?.clock) return;
        const clock = config.clock;
        const state = clockState(clock, Date.now());
        const active = state.phase === 'active';
        const updated = state.phase === 'update';
        timer.hidden = false;
        timer.dataset.state = state.phase;
        const heading = updated ? 'Strike status updated' : active ? `Hour ${state.hour.toLocaleString('en-US')} on strike` : 'Strike starts in';
        const headline = updated ? (clock.resolutionHeadline || 'STRIKE UPDATE') : active ? clock.activeHeadline : config.headline;
        const summary = updated ? (clock.resolutionMessage || 'Read our union’s latest instructions before reporting to work or a picket line.') : config.summary;
        setText('[data-action-headline]', headline);
        setText('[data-action-summary]', summary);
        if (updated) setText('[data-action-eyebrow]', 'Latest union update');
        setText('[data-home-clock-heading]', heading);
        setText('[data-home-clock-status]', updated ? 'Latest union update' : active ? 'OSU classified workers are on strike' : 'The strike begins at 6 a.m.');
        setText('[data-home-clock-message]', updated ? summary : active ? clock.activeMessage : 'Management: settle a fair contract.');
        setText('[data-home-clock-date-label]', active ? 'Since:' : 'Strike start:');
        const time = timer.querySelector('time');
        time.dateTime = clock.startsAt;
        time.textContent = clock.startLabel;
        const digits = timer.querySelector('[role="timer"]');
        digits.hidden = updated;
        document.querySelectorAll('[data-strike-mobilization]').forEach(element => { element.hidden = updated; });
        if (/^\/(?!\/)/.test(clock.updateUrl || '')) {
            document.querySelector('[data-strike-update-link]').setAttribute('href', clock.updateUrl);
        }
        if (!updated) {
            units.forEach((unit, index) => setText(`[data-home-clock-unit="${unit}"]`, String(state.values[index]).padStart(2, '0')));
            digits.setAttribute('aria-label', state.values.map((value, index) => `${value} ${units[index]}`).join(', ') + (active ? ' on strike' : ' until the strike starts'));
        }
        // Announce the change of phase once, never every tick.
        if (lastPhase && lastPhase !== state.phase) announcer.textContent = `${headline} ${heading}.`;
        lastPhase = state.phase;
    }

    document.addEventListener('local083:homepage-action', event => {
        const action = event.detail;
        if (!action?.strikeClock) {
            config = null;
            timer.hidden = true;
            document.querySelectorAll('[data-strike-mobilization]').forEach(element => { element.hidden = false; });
            return;
        }
        config = { clock: action.strikeClock, headline: action.headline, summary: action.summary };
        render();
    });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) render(); });
    render();
    setInterval(() => { if (!document.hidden) render(); }, 1000);
})();
