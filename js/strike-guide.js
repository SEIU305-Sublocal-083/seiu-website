(() => {
  const topics = [...document.querySelectorAll('.hub-topic')];
  if (!topics.length) return;

  const expand = document.querySelector('[data-expand-guides]');
  const syncExpand = () => {
    if (!expand) return;
    const allOpen = topics.every((topic) => topic.open);
    expand.textContent = allOpen ? 'Close all topics' : 'Open all topics';
    expand.setAttribute('aria-expanded', String(allOpen));
  };
  if (expand) {
    expand.hidden = false;
    expand.addEventListener('click', () => {
      const open = !topics.every((topic) => topic.open);
      topics.forEach((topic) => { topic.open = open; });
      syncExpand();
    });
    topics.forEach((topic) => topic.addEventListener('toggle', syncExpand));
  }

  // A link to a question, source or subsection must reveal its enclosing topic.
  function reveal(hash) {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    if (target.matches('details')) target.open = true;
    let parent = target.parentElement;
    while (parent) {
      if (parent.matches('details')) parent.open = true;
      parent = parent.parentElement;
    }
    syncExpand();
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const url = new URL(link.href, location.href);
    if (url.origin === location.origin && url.pathname === location.pathname && url.hash) reveal(url.hash);
  });
  window.addEventListener('hashchange', () => reveal(location.hash));
  reveal(location.hash);

  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('main details')].map((detail) => [detail, detail.open]);
    printState.forEach(([detail]) => { detail.open = true; });
  });
  window.addEventListener('afterprint', () => {
    printState.forEach(([detail, open]) => { detail.open = open; });
    printState = [];
    syncExpand();
  });
})();
