(function () {
    const DATA_URL = '/data/current-action.json?v=2026-07-09-email-encoding-hotfix';

    const safeText = (value) => String(value || '');

    const isVisible = (action, now = new Date()) => {
        const visibility = action && action.visibility;
        if (!visibility) return true;
        const starts = visibility.from ? new Date(visibility.from) : null;
        const ends = visibility.until ? new Date(visibility.until) : null;
        if (starts && now < starts) return false;
        if (ends && now > ends) return false;
        return true;
    };

    const getAction = (payload, slotName) => {
        const slug = payload?.slots?.[slotName] || payload?.defaultAction;
        const action = slug && payload?.actions ? payload.actions[slug] : null;
        if (action && isVisible(action)) return action;

        const visibleAction = Object.values(payload?.actions || {}).find(item => isVisible(item));
        return visibleAction || payload?.fallback || null;
    };

    const setText = (selector, value) => {
        const element = document.querySelector(selector);
        if (element && value) element.textContent = value;
    };

    const setImage = (selector, image) => {
        const element = document.querySelector(selector);
        if (!element || !image?.src) return;
        element.setAttribute('src', image.src);
        if (image.alt) element.setAttribute('alt', image.alt);
    };

    const applyAnalytics = (element, cta) => {
        const analytics = cta.analytics || {};
        if (analytics.event) element.dataset.phEvent = analytics.event;
        if (analytics.label) element.dataset.phLabel = analytics.label;
        if (analytics.metadata) element.dataset.phMetadata = JSON.stringify(analytics.metadata);
    };

    const randomIndex = (count) => {
        if (count <= 1) return 0;
        if (window.crypto?.getRandomValues) {
            const value = new Uint32Array(1);
            window.crypto.getRandomValues(value);
            return value[0] % count;
        }
        return Math.floor(Math.random() * count);
    };

    const mailtoFor = (emailAction, subject) => {
        const recipient = safeText(emailAction?.recipient);
        if (!recipient) return '#';
        const params = [];
        if (subject) params.push(`subject=${encodeURIComponent(subject)}`);
        if (emailAction?.body) params.push(`body=${encodeURIComponent(emailAction.body)}`);
        return `mailto:${recipient}?${params.join('&')}`;
    };

    const configureEmailActions = (payload) => {
        document.querySelectorAll('[data-email-action]').forEach(element => {
            const emailAction = payload?.emailActions?.[element.dataset.emailAction];
            const subjects = emailAction?.subjects || [];
            if (!emailAction?.recipient || !subjects.length) return;

            const subjectIndex = randomIndex(subjects.length);
            element.setAttribute('href', mailtoFor(emailAction, subjects[subjectIndex]));
            element.removeAttribute('target');
            element.removeAttribute('rel');
            element.dataset.emailSubjectVariant = String(subjectIndex + 1);

            if (element.dataset.phMetadata) {
                try {
                    const metadata = JSON.parse(element.dataset.phMetadata);
                    element.dataset.phMetadata = JSON.stringify({
                        ...metadata,
                        email_subject_variant: subjectIndex + 1
                    });
                } catch (error) {
                    // Leave malformed analytics metadata untouched.
                }
            }
        });
    };

    const setCta = (selector, cta) => {
        document.querySelectorAll(selector).forEach(element => {
            if (!cta) {
                element.classList.add('hidden');
                return;
            }

            element.classList.remove('hidden');
            element.textContent = safeText(cta.label);
            element.setAttribute('href', safeText(cta.href || '#'));
            applyAnalytics(element, cta);

            if (cta.emailAction) {
                element.dataset.emailAction = safeText(cta.emailAction);
            } else {
                delete element.dataset.emailAction;
                delete element.dataset.emailSubjectVariant;
            }

            if (/^https?:\/\//i.test(cta.href || '')) {
                element.setAttribute('target', '_blank');
                element.setAttribute('rel', 'noopener noreferrer');
            } else {
                element.removeAttribute('target');
                element.removeAttribute('rel');
            }
        });
    };

    const renderDetails = (selector, details) => {
        const container = document.querySelector(selector);
        if (!container || !Array.isArray(details)) return;

        container.replaceChildren();
        details.forEach(detail => {
            const item = document.createElement('div');
            item.className = 'rounded-lg border border-border-color bg-brand-light p-4';

            const term = document.createElement('dt');
            term.className = 'text-sm font-bold uppercase tracking-wide text-brand-purple';
            term.textContent = safeText(detail.label);

            const description = document.createElement('dd');
            description.className = 'mt-1 text-text-primary font-semibold';
            description.textContent = safeText(detail.value);

            item.append(term, description);
            container.appendChild(item);
        });
    };

    const ctaById = (action, id) => {
        return (action?.ctas || []).find(cta => cta.id === id) || null;
    };

    const renderHomepage = (action) => {
        if (!document.querySelector('[data-current-action-home]')) return;
        setText('[data-action-eyebrow]', action.eyebrow);
        setText('[data-action-headline]', action.headline);
        setText('[data-action-summary]', action.summary);
        setImage('[data-action-image]', action.image);
        renderDetails('[data-action-details]', action.details);

        setText('[data-action-promo-eyebrow]', action.promoEyebrow);
        setText('[data-action-promo-headline]', action.promoHeadline);
        setText('[data-action-promo-body]', action.promoBody);

        setCta('[data-action-primary]', ctaById(action, 'primary'));
        setCta('[data-action-secondary]', ctaById(action, 'secondary'));
        setCta('[data-action-tertiary]', ctaById(action, 'tertiary'));
    };

    const renderActionPage = (action) => {
        if (!document.querySelector('[data-current-action-page]')) return;
        setText('[data-action-page-eyebrow]', action.eyebrow);
        setText('[data-action-page-headline]', action.actionPage?.headline || action.headline);
        setText('[data-action-page-body]', action.actionPage?.body || action.summary);
        setText('[data-action-page-next-step]', action.actionPage?.nextStep);
        setImage('[data-action-page-image]', action.image);
        renderDetails('[data-action-page-details]', action.details);

        setCta('[data-action-page-primary]', ctaById(action, 'primary'));
        setCta('[data-action-page-secondary]', ctaById(action, 'secondary'));
        setCta('[data-action-page-tertiary]', ctaById(action, 'tertiary'));
    };

    const slugFromQuery = () => {
        try {
            return new URLSearchParams(window.location.search).get('slug');
        } catch (error) {
            return null;
        }
    };

    const chooseActionForPage = (payload) => {
        const requestedSlug = slugFromQuery();
        if (requestedSlug && payload?.actions?.[requestedSlug]) return payload.actions[requestedSlug];
        return getAction(payload, 'actionPageDefault');
    };

    const load = async () => {
        try {
            const response = await fetch(DATA_URL, { cache: 'no-store' });
            if (!response.ok) throw new Error('Current action payload unavailable');
            const payload = await response.json();
            renderHomepage(getAction(payload, 'homepageHero'));
            renderActionPage(chooseActionForPage(payload));
            configureEmailActions(payload);
        } catch (error) {
            if (window.location.search.includes('action_debug=1')) {
                console.warn('[current-action]', error);
            }
        }
    };

    document.addEventListener('DOMContentLoaded', load);
})();
