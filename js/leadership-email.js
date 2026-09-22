/* Select an editable email draft. The visitor reviews and sends it in their mail app. */
(() => {
  'use strict';

  const STORAGE_KEY = 'local083.leadershipDrafts.v1';

  function shuffle(values, random = Math.random) {
    const result = [...values];
    for (let i = result.length - 1; i > 0; i -= 1) {
      const j = Math.floor(random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  function nextDraft(drafts, previous, random = Math.random) {
    const ids = drafts.map(draft => draft.id);
    const valid = previous && Array.isArray(previous.remaining)
      && previous.remaining.every(id => ids.includes(id))
      && new Set(previous.remaining).size === previous.remaining.length;
    let remaining = valid ? [...previous.remaining] : [];
    if (!remaining.length) {
      remaining = shuffle(ids, random);
      // Avoid an immediate repeat when starting the next cycle.
      if (remaining.length > 1 && remaining[0] === previous?.last) {
        [remaining[0], remaining[1]] = [remaining[1], remaining[0]];
      }
    }
    const id = remaining.shift();
    return {
      draft: drafts.find(draft => draft.id === id),
      state: { remaining, last: id },
    };
  }

  function emailUrl(to, draft) {
    const body = draft.body.replace(/\r?\n/g, '\r\n');
    return `mailto:${to.join(',')}?subject=${encodeURIComponent(draft.subject)}&body=${encodeURIComponent(body)}`;
  }

  // Export pure selection/encoding helpers for the focused contract checks.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { nextDraft, emailUrl };
    return;
  }

  const links = [...document.querySelectorAll('[data-leadership-email]')];
  if (!links.length) return;
  let data = null;
  let inMemoryState = null;
  let storageAvailable = true;

  fetch('/data/leadership-email-drafts.json')
    .then(response => {
      if (!response.ok) throw new Error('Drafts unavailable');
      return response.json();
    })
    .then(result => {
      const valid = Array.isArray(result.drafts) && result.drafts.length === 30
        && new Set(result.drafts.map(draft => draft.id)).size === 30
        && result.drafts.every(draft => typeof draft.id === 'string'
          && typeof draft.subject === 'string' && typeof draft.body === 'string')
        && Array.isArray(result.to) && result.to.length === 2
        && result.to[0] === 'pres.office@oregonstate.edu'
        && result.to[1] === 'trustees@oregonstate.edu';
      if (valid) data = result;
    })
    .catch(() => { /* The HTML contains a complete working mailto fallback. */ });

  links.forEach(link => {
    link.addEventListener('click', () => {
      if (!data) return;
      let previous = inMemoryState;
      if (storageAvailable) {
        try {
          const stored = localStorage.getItem(STORAGE_KEY);
          if (stored) previous = JSON.parse(stored);
        } catch {
          storageAvailable = false;
        }
      }
      const selected = nextDraft(data.drafts, previous);
      inMemoryState = selected.state;
      if (storageAvailable) {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(selected.state));
        } catch {
          storageAvailable = false;
        }
      }
      // Update synchronously within the user click so the browser opens its mail handler.
      link.href = emailUrl(data.to, selected.draft);
    });
  });
})();
