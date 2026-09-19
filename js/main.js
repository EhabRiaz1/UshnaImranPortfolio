/* Ushna Imran — portfolio interactions */
(() => {
  'use strict';
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- social grid: 3.5 rows collapsed, animated expand ----------- */
  const grid = $('#socialGrid'), wrap = $('#socialWrap'), toggle = $('#socialToggle');
  if (grid && toggle) {
    const VISIBLE_ROWS = 3.5;

    // Measured arithmetically: touching inline height to read scrollHeight makes
    // the browser coalesce the change and skip the transition entirely.
    const metrics = () => {
      const cs   = getComputedStyle(grid);
      const cols = cs.gridTemplateColumns.split(' ').filter(Boolean).length || 1;
      const gap  = parseFloat(cs.rowGap) || 0;
      const itemH = grid.firstElementChild.getBoundingClientRect().height;
      const rows  = Math.ceil(grid.children.length / cols);
      return {
        full:      Math.round(rows * itemH + (rows - 1) * gap),
        collapsed: Math.round(VISIBLE_ROWS * itemH + Math.ceil(VISIBLE_ROWS - 1) * gap),
      };
    };

    const measure = () => {
      if (!grid.firstElementChild) return;
      const { full, collapsed } = metrics();
      const shown = Math.min(collapsed, full);
      grid.style.setProperty('--collapsed', shown + 'px');
      grid.style.setProperty('--full', full + 'px');
      toggle.hidden = full <= shown + 4;
    };

    let animating = false, guard = 0;
    const setOpen = (open) => {
      if (animating) return;
      animating = true;
      clearTimeout(guard);
      guard = setTimeout(() => { animating = false; }, 1400);  // never latch shut

      grid.style.setProperty('--full', metrics().full + 'px');
      grid.classList.toggle('is-open', open);
      wrap.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      $('[data-label]', toggle).textContent = open
        ? 'Show less'
        : `View all ${grid.children.length}`;

      const done = () => { animating = false; clearTimeout(guard); grid.removeEventListener('transitionend', done); };
      reduced ? done() : grid.addEventListener('transitionend', done);

      if (!open) {
        const top = wrap.getBoundingClientRect().top + scrollY - 140;
        scrollTo({ top, behavior: reduced ? 'auto' : 'smooth' });
      }
    };

    toggle.addEventListener('click', () =>
      setOpen(toggle.getAttribute('aria-expanded') !== 'true'));

    measure();
    addEventListener('resize', debounce(measure, 150));
    $$('img', grid).forEach(img => img.complete ||
      img.addEventListener('load', debounce(measure, 80), { once: true }));
  }

  /* ---------- case-study modal ------------------------------------------- */
  const modal = $('#modal'), panel = $('#modalPanel'),
        body  = $('#modalBody'), titleEl = $('#modalTitle');
  let cases = {}, lastFocus = null, closing = false;

  const syncTiles = () => {
    // A tile only behaves as a link once its case study has been rendered.
    $$('[data-case]').forEach(btn => {
      const ready = Array.isArray(cases[btn.dataset.case]) && cases[btn.dataset.case].length;
      btn.classList.toggle('tile--link', !!ready);
      btn.classList.toggle('tile--static', !ready);
      btn.disabled = !ready;
    });
  };

  fetch('js/cases.json')
    .then(r => r.ok ? r.json() : {})
    .then(j => { cases = j; syncTiles(); })
    .catch(syncTiles);

  const openCase = (slug, label) => {
    const slices = cases[slug];
    if (!slices || !slices.length) return;         // nothing rendered for it yet
    lastFocus = document.activeElement;
    titleEl.textContent = label;
    body.innerHTML = slices.map((src, i) =>
      `<img src="${src}" alt="${label} — part ${i + 1} of ${slices.length}"` +
      `${i > 1 ? ' loading="lazy"' : ''}>`).join('');
    modal.hidden = false;
    requestAnimationFrame(() => {
      modal.classList.add('is-open');
      document.body.classList.add('is-locked');
      panel.scrollTop = 0;
      closing = false;
      $('.modal__close', modal).focus();
    });
  };

  const closeCase = () => {
    if (closing || modal.hidden) return;
    closing = true;
    modal.classList.remove('is-open');
    document.body.classList.remove('is-locked');
    const done = () => {
      modal.hidden = true;
      body.innerHTML = '';
      modal.removeEventListener('transitionend', done);
      if (lastFocus) lastFocus.focus();
    };
    reduced ? done() : modal.addEventListener('transitionend', done);
  };

  $$('[data-case]').forEach(btn => btn.addEventListener('click', () =>
    openCase(btn.dataset.case, $('.tile__label', btn).textContent.trim())));

  $$('[data-close]', modal).forEach(el => el.addEventListener('click', closeCase));
  addEventListener('keydown', e => { if (e.key === 'Escape') closeCase(); });

  // scrolling past the end of the case study dismisses it
  panel.addEventListener('scroll', () => {
    if (closing) return;
    const scrollable = panel.scrollHeight - panel.clientHeight;
    if (scrollable < 120) return;                   // too short to "scroll past"
    if (panel.scrollTop >= scrollable - 8) closeCase();
  }, { passive: true });

  /* ---------- videos ------------------------------------------------------ */
  const play = v => { const p = v.play(); if (p) p.catch(() => {}); };

  $$('[data-hover-video]').forEach(box => {
    const v = $('video', box);
    if (!v) return;
    const on  = () => { v.preload = 'auto'; box.classList.add('is-playing'); play(v); };
    const off = () => { box.classList.remove('is-playing'); v.pause(); };
    box.addEventListener('mouseenter', on);
    box.addEventListener('mouseleave', off);
    box.addEventListener('focusin', on);
    box.addEventListener('focusout', off);
    // touch: tap toggles
    box.addEventListener('click', () =>
      box.classList.contains('is-playing') ? off() : on());
  });

  const autoplay = $$('[data-autoplay-video]');
  if (autoplay.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(({ target, isIntersecting }) => {
        const v = $('video', target);
        if (!v) return;
        if (isIntersecting) { v.preload = 'auto'; target.classList.add('is-playing'); play(v); }
        else { target.classList.remove('is-playing'); v.pause(); }
      });
    }, { threshold: 0.35 });
    autoplay.forEach(el => io.observe(el));
  }

  /* ---------- hero jump-link underline follows the visible section -------- */
  const jumps = $$('[data-jump]');
  if (jumps.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        jumps.forEach(a => a.classList.toggle('is-active', a.dataset.jump === e.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['branding', 'uiux', 'social', 'animation']
      .map(id => document.getElementById(id)).filter(Boolean).forEach(s => io.observe(s));
  }

  /* ---------- assets that failed to render leave a blank slot, not a glyph -- */
  $$('.covers__row img').forEach(img => {
    const flag = () => { img.dataset.missing = '1'; };
    img.addEventListener('error', flag);
    if (img.complete && img.naturalWidth === 0) flag();
  });

  function debounce(fn, ms) {
    let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  }
})();
