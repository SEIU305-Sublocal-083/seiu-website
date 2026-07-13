(function () {
    // Some static pages or content-management includes can accidentally load this
    // file twice. Keep page views and delegated click events single-fire.
    if (window.__local083AnalyticsLoaded) return;
    window.__local083AnalyticsLoaded = true;

    const POSTHOG_KEY = 'phc_777ihTsY1YRlyHhK42ADhcXGvS5rUFr5Zz8TfJvjOtf';
    const API_HOST = 'https://us.i.posthog.com';
    const debug = window.location.search.includes('ph_debug=1');

    const dnt = (navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack || '').toString().toLowerCase();
    const isDNT = dnt === '1' || dnt === 'yes';
    const isGPC = navigator.globalPrivacyControl === true;
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
        if (isDNT || isGPC) {
            alert('Your browser privacy signal keeps analytics disabled. Change that browser setting first if you want to opt in.');
            return;
        }
        localStorage.removeItem('ph_opt_out');
        if (window.posthog?.opt_in_capturing) {
            window.posthog.opt_in_capturing();
        }
        alert('Privacy updated: tracking enabled. Reloading to apply.');
        window.location.reload();
    };

    // Respect Do Not Track or manual opt-out
    if (isDNT || isGPC || isOptOut) {
        log('PostHog disabled', { isDNT, isGPC, isOptOut });
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
        autocapture: false,
        capture_pageview: false,
        capture_pageleave: false,
        disable_session_recording: true,
        person_profiles: 'never',
        persistence: 'localStorage'
    });

    if (debug && typeof posthog.debug === 'function') {
        posthog.debug();
    }

    const commonProps = () => {
        const parts = window.location.pathname.split('/').filter(Boolean);
        const site_section = parts[0] || 'home';
        return {
            // Search terms and email/action query parameters can be sensitive.
            // Analytics only needs the path-level location.
            page_url: `${window.location.origin}${window.location.pathname}`,
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

    window.phCapture('page_view');

    const parseMetadata = (raw) => {
        if (!raw) return {};
        try { return JSON.parse(raw); } catch (err) { log('metadata parse error', err); return {}; }
    };

    const textFor = (el) => (el?.dataset?.phLabel || el?.getAttribute?.('aria-label') || el?.textContent || '').trim();

    const parseUrl = (raw) => {
        try {
            return new URL(raw || '', window.location.href);
        } catch (error) {
            return null;
        }
    };

    const cleanTargetUrl = (raw) => {
        if (!raw || raw.startsWith('mailto:') || raw.startsWith('tel:')) return undefined;
        const parsed = parseUrl(raw);
        if (!parsed) return raw;
        parsed.search = '';
        parsed.hash = '';
        return parsed.origin === window.location.origin ? parsed.pathname : parsed.toString();
    };

    const fileNameFromUrl = (raw) => {
        const parsed = parseUrl(raw);
        const pathname = parsed ? parsed.pathname : raw;
        return (pathname || '').split('/').filter(Boolean).pop() || '';
    };

    const eventIdFromUrl = (raw) => fileNameFromUrl(raw).replace(/\.html$/i, '').toLowerCase();

    const isCatSignup = (raw) => /seiu503\.tfaforms\.net\/759/i.test(raw || '');
    const isMemberSignup = (raw) => /seiu503signup\.org/i.test(raw || '');
    const isTakeAction = (raw) => /www2\.seiu503\.org\/e\/171302\//i.test(raw || '');
    const isBargainingHub = (raw) => /\/2026-bargaining\/(?:index\.html)?$/i.test(parseUrl(raw)?.pathname || raw || '');
    const isStewardMailto = (raw) => /^mailto:083stewards@seiu503\.org/i.test(raw || '');
    const isEventDetails = (raw) => /^\/events\/.+\.html$/i.test(parseUrl(raw)?.pathname || raw || '');
    const mailtoRecipient = (raw) => {
        const match = /^mailto:([^?]+)/i.exec(raw || '');
        return match ? decodeURIComponent(match[1]) : '';
    };

    const normalizedEventName = (name, rawTarget) => {
        if (isMemberSignup(rawTarget)) return 'member_signup_click';
        if (isCatSignup(rawTarget)) return 'cat_signup_click';
        if (isTakeAction(rawTarget)) return 'take_action_click';
        if (isBargainingHub(rawTarget)) return 'bargaining_hub_click';
        if (isStewardMailto(rawTarget)) return 'steward_contact_click';
        if (name === 'event_click') return 'event_details_click';
        if (name === 'file_download') return 'file_download_click';
        if (name === 'cta_click' && isEventDetails(rawTarget)) return 'event_details_click';
        return name;
    };

    const clickProps = (eventName, rawTarget, label, metadata = {}, legacyEventName = null) => {
        const props = { label, target_url: cleanTargetUrl(rawTarget), ...metadata };
        if (legacyEventName && legacyEventName !== eventName) props.legacy_event_name = legacyEventName;

        if (eventName === 'member_signup_click') {
            props.signup_type = props.signup_type || 'member';
            props.signup_destination_domain = 'seiu503signup.org';
        }

        if (eventName === 'cat_signup_click') {
            props.signup_type = props.signup_type || 'cat';
            props.signup_destination_domain = 'seiu503.tfaforms.net';
        }

        if (eventName === 'take_action_click') {
            props.action_type = props.action_type || 'president_email';
            const recipient = mailtoRecipient(rawTarget);
            props.action_channel = recipient ? 'email' : 'web_form';
            props.action_destination_domain = recipient.split('@')[1] || 'www2.seiu503.org';
        }

        if (eventName === 'steward_contact_click') {
            props.label = props.label && props.label.includes('@') ? 'Steward email' : props.label;
            props.contact_role = 'steward';
            props.contact_channel = 'email';
            delete props.target_url;
        }

        if (eventName === 'file_download_click') {
            const fileName = fileNameFromUrl(rawTarget);
            props.file_name = fileName;
            props.file_type = (fileName.split('.').pop() || '').toLowerCase();
        }

        if (eventName === 'event_details_click') {
            props.event_id = props.event_id || eventIdFromUrl(rawTarget);
        }

        return props;
    };

    document.addEventListener('click', (event) => {
        const target = event.target.closest('a, button');
        if (!target) return;

        const href = target.getAttribute('href') || '';
        const url = target.href || href;

        if (target.dataset.phEvent) {
            const metadata = parseMetadata(target.dataset.phMetadata);
            const rawEventName = target.dataset.phEvent;
            const eventName = normalizedEventName(rawEventName, url || href);
            window.phCapture(eventName, clickProps(eventName, url || href, textFor(target), metadata, rawEventName));
            return;
        }

        const label = textFor(target);
        const isMailto = href.startsWith('mailto:');
        const isTel = href.startsWith('tel:');
        const isDownload = target.hasAttribute('download') || /\.(pdf|docx?|xlsx?|csv|zip|ics)$/i.test(href);
        const isExternal = /^https?:\/\//i.test(url) && (new URL(url)).hostname !== window.location.hostname;
        const isNav = !!target.closest('header') || !!target.closest('#mobile-menu');

        if (isNav) {
            window.phCapture('nav_click', { label, target_url: cleanTargetUrl(url || href) });
            return;
        }

        if (isMailto || isTel) {
            const eventName = normalizedEventName('contact_click', url || href);
            window.phCapture(eventName, clickProps(eventName, url || href, label, { channel: isMailto ? 'email' : 'phone' }, eventName === 'contact_click' ? null : 'contact_click'));
            return;
        }

        if (isDownload) {
            window.phCapture('file_download_click', clickProps('file_download_click', url || href, label));
            return;
        }

        if (isEventDetails(url || href)) {
            window.phCapture('event_details_click', clickProps('event_details_click', url || href, label));
            return;
        }

        if (isExternal) {
            const eventName = normalizedEventName('outbound_click', url || href);
            window.phCapture(eventName, clickProps(eventName, url || href, label, {}, eventName === 'outbound_click' ? null : 'outbound_click'));
            return;
        }
    });
})();
