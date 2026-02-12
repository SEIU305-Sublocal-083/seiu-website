(function () {
    const POSTHOG_KEY = 'phc_777ihTsY1YRlyHhK42ADhcXGvS5rUFr5Zz8TfJvjOtf';
    const API_HOST = 'https://us.i.posthog.com';
    const debug = window.location.search.includes('ph_debug=1');

    const dnt = (navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack || '').toString().toLowerCase();
    const isDNT = dnt === '1' || dnt === 'yes';
    const isOptOut = localStorage.getItem('ph_opt_out') === '1';

    const log = (...args) => {
        if (debug) console.log('[PostHog]', ...args);
    };

    window.phOptOut = function () {
        localStorage.setItem('ph_opt_out', '1');
        if (window.posthog?.opt_out_capturing) {
            window.posthog.opt_out_capturing();
        }
        alert('Privacy updated: tracking disabled for this browser.');
    };

    window.phOptIn = function () {
        localStorage.removeItem('ph_opt_out');
        if (window.posthog?.opt_in_capturing) {
            window.posthog.opt_in_capturing();
        }
        alert('Privacy updated: tracking enabled. Reloading to apply.');
        window.location.reload();
    };

    // Respect Do Not Track or manual opt-out
    if (isDNT || isOptOut) {
        log('PostHog disabled', { isDNT, isOptOut });
        window.phCapture = () => {};
        return;
    }

    // PostHog loader snippet
    !function (t, e) {
        var o, n, p, r; e.__SV || (window.posthog = e, e._i = [], e.init = function (i, s, a) {
            function g(t, e) { var o = e.split('.'); 2 == o.length && (t = t[o[0]], e = o[1]), t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))) } }
            (p = t.createElement('script')).type = 'text/javascript', p.async = !0, p.src = s.api_host.replace('.i.posthog.com', '-assets.i.posthog.com') + '/static/array.js',
                (r = t.getElementsByTagName('script')[0]).parentNode.insertBefore(p, r); var u = e; for (void 0 !== a ? u = e[a] = [] : a = 'posthog', u.people = u.people || [], u.toString = function (t) { var e = 'posthog'; return 'posthog' !== a && (e += '.' + a), t || (e += ' (stub)'), e }, u.people.toString = function () { return u.toString(1) + '.people (stub)' }, o = 'init capture register register_once register_for_session unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group identify setPersonProperties setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroups onFeatureFlags addFeatureFlagsHandler onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep'.split(' '), n = 0; n < o.length; n++)g(u, o[n]); e._i.push([i, s, a]) }, e.__SV = 1)
    }(document, window.posthog || []);

    posthog.init(POSTHOG_KEY, {
        api_host: API_HOST,
        autocapture: true,
        capture_pageview: true,
        capture_pageleave: true,
        session_recording: {
            sampling_rate: 0.1,
            mask_all_inputs: true
        },
        disable_session_recording: false
    });

    if (debug && typeof posthog.debug === 'function') {
        posthog.debug();
    }

    const commonProps = () => {
        const parts = window.location.pathname.split('/').filter(Boolean);
        const site_section = parts[0] || 'home';
        return {
            page_url: window.location.href,
            page_title: document.title,
            site_section,
            environment: 'prod'
        };
    };

    window.phCapture = function (name, props = {}) {
        if (!window.posthog?.capture) return;
        const payload = { ...commonProps(), ...props };
        posthog.capture(name, payload);
        log('capture', name, payload);
    };

    const parseMetadata = (raw) => {
        if (!raw) return {};
        try { return JSON.parse(raw); } catch (err) { log('metadata parse error', err); return {}; }
    };

    const textFor = (el) => (el?.dataset?.phLabel || el?.getAttribute?.('aria-label') || el?.textContent || '').trim();

    document.addEventListener('click', (event) => {
        const target = event.target.closest('a, button');
        if (!target) return;

        const href = target.getAttribute('href') || '';
        const url = target.href || href;

        if (target.dataset.phEvent) {
            const metadata = parseMetadata(target.dataset.phMetadata);
            window.phCapture(target.dataset.phEvent, {
                label: textFor(target),
                target_url: url || href,
                ...metadata
            });
            return;
        }

        const label = textFor(target);
        const isMailto = href.startsWith('mailto:');
        const isTel = href.startsWith('tel:');
        const isDownload = target.hasAttribute('download') || /\.(pdf|docx?|xlsx?|csv|zip|ics)$/i.test(href);
        const isExternal = /^https?:\/\//i.test(url) && (new URL(url)).hostname !== window.location.hostname;
        const isNav = !!target.closest('header') || !!target.closest('#mobile-menu');

        if (isNav) {
            window.phCapture('nav_click', { label, target_url: url || href });
            return;
        }

        if (isMailto || isTel) {
            window.phCapture('contact_click', { channel: isMailto ? 'email' : 'phone', target: url || href });
            return;
        }

        if (isDownload) {
            window.phCapture('file_download', { label, target_url: url || href });
            return;
        }

        if (isExternal) {
            window.phCapture('outbound_click', { label, target_url: url });
            return;
        }
    });
})();
