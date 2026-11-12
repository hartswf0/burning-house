/* burning-house · Editorial Web Reader interactive controls (reader.js) */
(function () {
  var root = document.documentElement;

  function applyPlate(p, persist) {
    if (!['paper', 'notebook', 'ochre', 'night'].includes(p)) p = 'paper';
    root.setAttribute('data-plate', p);
    document.querySelectorAll('[data-set-plate]').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-set-plate') === p);
    });
    if (persist) {
      try {
        localStorage.setItem('bh_doc_plate', p);
        if (p === 'paper' || p === 'ochre') {
          localStorage.setItem('bh_plate', p);
        }
      } catch (e) {}
    }
  }

  function applySize(s, persist) {
    if (!['sm', 'md', 'lg'].includes(s)) s = 'md';
    root.setAttribute('data-size', s);
    document.querySelectorAll('[data-set-size]').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-set-size') === s);
    });
    if (persist) {
      try { localStorage.setItem('bh_doc_size', s); } catch (e) {}
    }
  }

  function applyWidth(w, persist) {
    if (!['book', 'wide'].includes(w)) w = 'book';
    root.setAttribute('data-width', w);
    document.querySelectorAll('[data-set-width]').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-set-width') === w);
    });
    if (persist) {
      try { localStorage.setItem('bh_doc_width', w); } catch (e) {}
    }
  }

  // Hydrate initial preferences
  try {
    var qp = new URLSearchParams(location.search).get('plate');
    var savedPlate = qp || localStorage.getItem('bh_doc_plate') || localStorage.getItem('bh_plate') || root.getAttribute('data-plate') || 'paper';
    applyPlate(savedPlate, false);
    applySize(localStorage.getItem('bh_doc_size') || 'md', false);
    applyWidth(localStorage.getItem('bh_doc_width') || 'book', false);
  } catch (e) {}

  document.addEventListener('click', function (ev) {
    var pBtn = ev.target.closest('[data-set-plate]');
    if (pBtn) { applyPlate(pBtn.getAttribute('data-set-plate'), true); return; }

    var sBtn = ev.target.closest('[data-set-size]');
    if (sBtn) { applySize(sBtn.getAttribute('data-set-size'), true); return; }

    var wBtn = ev.target.closest('[data-set-width]');
    if (wBtn) { applyWidth(wBtn.getAttribute('data-set-width'), true); return; }

    var mobBtn = ev.target.closest('#mobTocBtn');
    var rail = document.getElementById('readerRail');
    if (mobBtn && rail) {
      rail.classList.toggle('open');
      return;
    }
    if (rail && rail.classList.contains('open') && ev.target.closest('.toc-item a')) {
      rail.classList.remove('open');
    }

    var copyBtn = ev.target.closest('[data-copy-code]');
    if (copyBtn) {
      var wrap = copyBtn.closest('.md-code-wrap, .z-bib');
      var pre = wrap ? wrap.querySelector('pre') : null;
      if (pre && navigator.clipboard) {
        navigator.clipboard.writeText(pre.innerText).then(function () {
          var orig = copyBtn.textContent;
          copyBtn.textContent = 'Copied';
          setTimeout(function () { copyBtn.textContent = orig; }, 1300);
        });
      }
      return;
    }

    var linkBtn = ev.target.closest('[data-copy-url]');
    if (linkBtn && navigator.clipboard) {
      var targetHash = linkBtn.getAttribute('data-copy-url');
      var u = targetHash ? (location.origin + location.pathname + '#' + targetHash) : location.href;
      navigator.clipboard.writeText(u).then(function () {
        var orig = linkBtn.textContent;
        linkBtn.textContent = 'Copied link';
        setTimeout(function () { linkBtn.textContent = orig; }, 1300);
      });
      return;
    }

    var xmlTab = ev.target.closest('[data-xml-view]');
    if (xmlTab) {
      var mode = xmlTab.getAttribute('data-xml-view');
      document.querySelectorAll('[data-xml-view]').forEach(function (b) {
        b.classList.toggle('active', b === xmlTab);
      });
      var structPane = document.getElementById('xmlStructuredPane');
      var rawPane = document.getElementById('xmlRawPane');
      if (structPane && rawPane) {
        structPane.hidden = (mode !== 'structured');
        rawPane.hidden = (mode !== 'raw');
      }
    }
  });

  // Reading progress bar + Scroll-spy TOC
  var prog = document.getElementById('readProgress');
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc-item a[href^="#"]'));
  var targets = tocLinks.map(function (a) {
    var id = decodeURIComponent(a.getAttribute('href').slice(1));
    return document.getElementById(id);
  }).filter(Boolean);

  function onScroll() {
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    if (prog) {
      var pct = docH > 0 ? Math.min(100, Math.max(0, (window.scrollY / docH) * 100)) : 0;
      prog.style.width = pct.toFixed(1) + '%';
    }
    if (!targets.length) return;
    var y = window.scrollY + 120;
    var currentId = targets[0].id;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].offsetTop <= y) currentId = targets[i].id;
      else break;
    }
    tocLinks.forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === '#' + currentId);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Sidebar TOC live filter
  var tocFilter = document.getElementById('tocFilter');
  if (tocFilter) {
    tocFilter.addEventListener('input', function () {
      var q = tocFilter.value.trim().toLowerCase();
      document.querySelectorAll('.toc-item').forEach(function (li) {
        var txt = li.textContent.toLowerCase();
        li.style.display = (!q || txt.indexOf(q) !== -1) ? '' : 'none';
      });
    });
  }

  // Zettelkasten live full-text & platform filter
  var zSearch = document.getElementById('zettelSearch');
  var zCount = document.getElementById('zettelCount');
  var zCards = Array.prototype.slice.call(document.querySelectorAll('.zettel-card'));
  var activePlat = '';

  function filterZettels() {
    if (!zCards.length) return;
    var q = zSearch ? zSearch.value.trim().toLowerCase() : '';
    var shown = 0;
    zCards.forEach(function (c) {
      var plat = (c.getAttribute('data-platform') || '').toLowerCase();
      var matchPlat = !activePlat || plat.indexOf(activePlat) !== -1;
      var matchQ = !q || c.textContent.toLowerCase().indexOf(q) !== -1;
      var ok = matchPlat && matchQ;
      c.hidden = !ok;
      if (ok) shown++;
    });
    if (zCount) zCount.textContent = shown + ' / ' + zCards.length + ' cards';
  }

  if (zSearch) zSearch.addEventListener('input', filterZettels);
  document.querySelectorAll('[data-plat-filter]').forEach(function (chip) {
    chip.addEventListener('click', function () {
      var p = chip.getAttribute('data-plat-filter').toLowerCase();
      activePlat = (activePlat === p) ? '' : p;
      document.querySelectorAll('[data-plat-filter]').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-plat-filter').toLowerCase() === activePlat && activePlat !== '');
      });
      filterZettels();
    });
  });

  // Clicking an unresolved conceptual [[wiki-link]] filters Zettels by that concept if on a Zettel page
  document.querySelectorAll('[data-wiki-query]').forEach(function (w) {
    w.addEventListener('click', function (ev) {
      if (zSearch) {
        ev.preventDefault();
        zSearch.value = w.getAttribute('data-wiki-query');
        filterZettels();
        zSearch.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  // Reading Room filter (docs/index.html)
  var roomSearch = document.getElementById('roomSearch');
  if (roomSearch) {
    roomSearch.addEventListener('input', function () {
      var q = roomSearch.value.trim().toLowerCase();
      document.querySelectorAll('.room-card').forEach(function (card) {
        card.style.display = (!q || card.textContent.toLowerCase().indexOf(q) !== -1) ? '' : 'none';
      });
    });
  }
})();
