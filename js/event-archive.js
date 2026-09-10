/* Shared selection and rendering for the Events page's recent archive. */
(function (root) {
    'use strict';

    const validDate = (value) => {
        if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
        const date = new Date(`${value}T12:00:00Z`);
        return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
    };
    const eventEndDay = (event) => {
        const end = typeof event.schema_end_date === 'string' ? event.schema_end_date.slice(0, 10) : '';
        return validDate(end) && end > event.date ? end : event.date;
    };
    const pacificDate = (now = new Date()) => {
        const parts = new Intl.DateTimeFormat('en-US', {
            timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit'
        }).formatToParts(now);
        const part = (type) => parts.find((item) => item.type === type).value;
        return `${part('year')}-${part('month')}-${part('day')}`;
    };
    const selectPastEvents = (events, today = pacificDate(), limit = 3) => {
        const seen = new Set();
        return events.filter((event) => event && validDate(event.date)
            && typeof event.title === 'string' && event.title.trim()
            && typeof event.url === 'string' && /^\/events\/[A-Za-z0-9._-]+\.html$/.test(event.url)
            && eventEndDay(event) < today)
            .sort((a, b) => {
                const left = `${eventEndDay(a)}|${a.date}|${a.url}`;
                const right = `${eventEndDay(b)}|${b.date}|${b.url}`;
                return left < right ? 1 : left > right ? -1 : 0;
            })
            .filter((event) => {
                if (seen.has(event.url)) return false;
                seen.add(event.url);
                return true;
            }).slice(0, limit);
    };
    const escapeHtml = (value = '') => String(value).replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
    const theme = (type = '') => {
        if (/rally|strike vote/i.test(type)) return ['past-rally', '✊'];
        if (/social|community/i.test(type)) return ['past-community', '♥'];
        if (/cat/i.test(type)) return ['past-meeting', '⚡'];
        if (/meeting/i.test(type)) return ['past-meeting', '◎'];
        return ['past-meeting', '•'];
    };
    const formatter = new Intl.DateTimeFormat('en-US', {
        timeZone: 'UTC', month: 'short', day: 'numeric', year: 'numeric'
    });
    const renderPastEvents = (events, today = pacificDate()) => {
        const past = selectPastEvents(events, today);
        if (!past.length) return '<p class="past-empty">No past events are listed yet.</p>';
        return past.map((event) => {
            const [color, icon] = theme(event.type);
            const date = formatter.format(new Date(`${event.date}T12:00:00Z`));
            const details = [event.time, event.location_detail].filter(Boolean).join(' · ');
            return `<a class="past-item ${color}" href="${escapeHtml(event.url)}">
                <div class="past-item-top"><span class="past-icon" aria-hidden="true">${icon}</span><time datetime="${event.date}">${escapeHtml(date)} · ${escapeHtml(event.type || 'Event')}</time></div>
                <h3>${escapeHtml(event.title)}</h3>
                <p>${escapeHtml(details)}</p>
                <span class="arrow" aria-hidden="true">→</span>
            </a>`;
        }).join('\n');
    };
    const api = { pacificDate, selectPastEvents, renderPastEvents };
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
    else root.Local083EventArchive = api;
})(typeof window !== 'undefined' ? window : globalThis);
