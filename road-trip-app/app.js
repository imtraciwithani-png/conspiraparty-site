(function () {
  'use strict';

  var STORAGE_KEY = 'srt-progress-v1';
  var LAST_STATE_KEY = 'srt-last-state';

  /* Geographic chip layout (11 cols). empty = spacer */
  var MAP_ROWS = [
    ['', '', '', '', '', '', '', '', '', 'ME', ''],
    ['', '', '', '', '', '', '', '', 'VT', 'NH', ''],
    ['WA', 'ID', 'MT', 'ND', 'MN', 'WI', '', 'MI', 'NY', 'MA', ''],
    ['OR', 'NV', 'WY', 'SD', 'IA', 'IL', 'IN', 'OH', 'PA', 'NJ', 'CT'],
    ['CA', 'UT', 'CO', 'NE', 'MO', 'KY', 'WV', 'VA', 'MD', 'DE', 'RI'],
    ['', 'AZ', 'NM', 'KS', 'AR', 'TN', 'NC', 'SC', '', '', ''],
    ['', '', '', 'OK', 'LA', 'MS', 'AL', 'GA', '', '', ''],
    ['AK', 'HI', '', 'TX', '', '', '', 'FL', '', '', '']
  ];

  var state = {
    places: [],
    byState: {},
    meta: null,
    progress: { checks: {}, spots: {} }, // checks[ST][i]=true, spots[ST][i]=true
    view: 'home',
    selected: null,
    nearOrder: null, // array of state codes when user picks a focus state for near-me fallback
    toastTimer: null
  };
  var hooks = window.__SRT && window.__SRT.hooks ? window.__SRT.hooks : {};

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function loadProgress() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var parsed = JSON.parse(raw);
      if (parsed && typeof parsed === 'object') {
        state.progress.checks = parsed.checks || {};
        state.progress.spots = parsed.spots || {};
      }
    } catch (e) { /* ignore corrupt */ }
  }

  function saveProgress() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progress));
    } catch (e) { /* quota */ }
  }

  function toast(msg) {
    var el = $('#srt-toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2200);
  }

  function scoring() {
    return (state.meta && state.meta.scoring) || { checklist: 5, spot: 10 };
  }

  function stateStats(code) {
    var p = state.byState[code];
    if (!p) return { checked: 0, total: 0, points: 0, pct: 0, done: false };
    var sc = scoring();
    var c = state.progress.checks[code] || {};
    var s = state.progress.spots[code] || {};
    var checked = 0, points = 0;
    var total = p.checklist.length + p.spots.length;
    p.checklist.forEach(function (_, i) {
      if (c[i]) { checked++; points += sc.checklist; }
    });
    p.spots.forEach(function (_, i) {
      if (s[i]) { checked++; points += sc.spot; }
    });
    var pct = total ? Math.round((checked / total) * 100) : 0;
    return { checked: checked, total: total, points: points, pct: pct, done: checked === total && total > 0 };
  }

  function totalPoints() {
    return state.places.reduce(function (sum, p) { return sum + stateStats(p.state).points; }, 0);
  }

  function statesTouched() {
    return state.places.filter(function (p) { return stateStats(p.state).checked > 0; }).length;
  }

  function statesDone() {
    return state.places.filter(function (p) { return stateStats(p.state).done; }).length;
  }

  function currentRank() {
    var pts = totalPoints();
    var ranks = (state.meta && state.meta.ranks) || [];
    var cur = ranks[0] || { id: 'recruit', name: 'Recruit', min: 0 };
    var next = null;
    for (var i = 0; i < ranks.length; i++) {
      if (pts >= ranks[i].min) cur = ranks[i];
      else { next = ranks[i]; break; }
    }
    var progress = 1;
    if (next) {
      var span = next.min - cur.min;
      progress = span ? Math.min(1, (pts - cur.min) / span) : 1;
    }
    return { current: cur, next: next, points: pts, progress: progress };
  }

  function regionProgress(slug) {
    var region = state.meta.regions.find(function (r) { return r.slug === slug; });
    if (!region) return { done: 0, total: 0, complete: false };
    var done = 0;
    region.states.forEach(function (st) {
      if (stateStats(st).done) done++;
    });
    return { done: done, total: region.states.length, complete: done === region.states.length };
  }

  function badges() {
    var pts = totalPoints();
    var touched = statesTouched();
    var done = statesDone();
    var checks = 0;
    state.places.forEach(function (p) {
      var c = state.progress.checks[p.state] || {};
      Object.keys(c).forEach(function (k) { if (c[k]) checks++; });
      var s = state.progress.spots[p.state] || {};
      Object.keys(s).forEach(function (k) { if (s[k]) checks++; });
    });
    var list = [
      { id: 'first', emoji: '👀', name: 'First Sighting', desc: 'Check off anything', earned: checks >= 1 },
      { id: 'ten', emoji: '📝', name: 'Field Notes', desc: '10 sightings logged', earned: checks >= 10 },
      { id: 'fifty', emoji: '🔦', name: 'Night Shift', desc: '50 sightings logged', earned: checks >= 50 },
      { id: 'hundred', emoji: '📁', name: 'Thick File', desc: '100 sightings logged', earned: checks >= 100 },
      { id: 'five-states', emoji: '🗺️', name: 'Five-State Circuit', desc: 'Touch 5 states', earned: touched >= 5 },
      { id: 'half', emoji: '⭐', name: 'Halfway Weird', desc: 'Finish 25 state missions', earned: done >= 25 },
      { id: 'all50', emoji: '🏆', name: '50-State Clearance', desc: 'Finish every state', earned: done >= 50 },
      { id: 'points-100', emoji: '🎖️', name: '100 Points', desc: 'Earn 100 agent points', earned: pts >= 100 },
      { id: 'points-500', emoji: '🛰️', name: '500 Points', desc: 'Earn 500 agent points', earned: pts >= 500 }
    ];
    state.meta.regions.forEach(function (r) {
      var rp = regionProgress(r.slug);
      list.push({
        id: 'region-' + r.slug,
        emoji: '📍',
        name: r.name + ' Agent',
        desc: 'Complete every state in ' + r.name,
        earned: rp.complete
      });
    });
    return list;
  }

  function setView(name, opts) {
    state.view = name;
    if (opts && opts.state) state.selected = opts.state;
    $all('.srt-panel').forEach(function (p) {
      p.classList.toggle('is-active', p.getAttribute('data-panel') === name);
    });
    $all('.srt-nav button').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-nav') === name ? 'page' : 'false');
    });
    if (name === 'home') renderHome();
    if (name === 'state') renderState();
    if (name === 'family') { if (hooks.renderFamily) hooks.renderFamily(); }
    if (name === 'badges') renderBadges();
    if (name === 'report') renderReport();
    if (name === 'shop') renderShop();
    window.scrollTo(0, 0);
  }

  function updateChrome() {
    var rank = currentRank();
    var ptsEl = $('#srt-points');
    var rankEl = $('#srt-rank');
    var doneEl = $('#srt-done');
    if (ptsEl) ptsEl.textContent = String(rank.points);
    if (rankEl) rankEl.textContent = rank.current.name;
    if (doneEl) doneEl.textContent = statesDone() + '/50';
  }

  function renderMap(container) {
    container.innerHTML = '';
    MAP_ROWS.forEach(function (row) {
      row.forEach(function (code) {
        var btn = document.createElement('button');
        btn.type = 'button';
        if (!code) {
          btn.className = 'empty';
          btn.tabIndex = -1;
          btn.setAttribute('aria-hidden', 'true');
        } else {
          var st = stateStats(code);
          btn.textContent = code;
          btn.title = (state.byState[code] && state.byState[code].state_name) || code;
          btn.setAttribute('aria-label', btn.title);
          if (st.done) btn.classList.add('done');
          else if (st.checked > 0) btn.classList.add('has-progress');
          if (state.selected === code) btn.setAttribute('aria-pressed', 'true');
          btn.addEventListener('click', function () {
            try { localStorage.setItem(LAST_STATE_KEY, code); } catch (e) {}
            setView('state', { state: code });
          });
        }
        container.appendChild(btn);
      });
    });
  }

  function renderHome() {
    updateChrome();
    var map = $('#srt-map');
    if (map) renderMap(map);

    var q = ($('#srt-search') && $('#srt-search').value || '').trim().toLowerCase();
    var list = $('#srt-state-list');
    if (!list) return;
    list.innerHTML = '';

    var places = state.places.slice();
    if (state.nearOrder) {
      var order = {};
      state.nearOrder.forEach(function (c, i) { order[c] = i; });
      places.sort(function (a, b) {
        return (order[a.state] != null ? order[a.state] : 999) - (order[b.state] != null ? order[b.state] : 999);
      });
    }

    places.forEach(function (p) {
      var hay = (p.state + ' ' + p.state_name + ' ' + p.short + ' ' + p.title).toLowerCase();
      if (q && hay.indexOf(q) === -1) return;
      var st = stateStats(p.state);
      var li = document.createElement('li');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.innerHTML =
        '<span class="abbr' + (st.done ? ' done' : '') + '">' + p.state + '</span>' +
        '<span class="meta"><strong>' + escapeHtml(p.short) + '</strong><span>' + escapeHtml(p.state_name) + '</span></span>' +
        '<span class="pct">' + st.pct + '%</span>';
      btn.addEventListener('click', function () {
        try { localStorage.setItem(LAST_STATE_KEY, p.state); } catch (e) {}
        setView('state', { state: p.state });
      });
      li.appendChild(btn);
      list.appendChild(li);
    });

    var nearNote = $('#srt-near-note');
    if (nearNote) {
      if (state.nearOrder) {
        nearNote.hidden = false;
        nearNote.textContent = 'Sorted by focus state (no verified GPS coordinates in the book source — Near Me uses the state you pick).';
      } else {
        nearNote.hidden = true;
      }
    }
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  function renderState() {
    updateChrome();
    var code = state.selected;
    var p = state.byState[code];
    var root = $('#srt-state-root');
    if (!p || !root) {
      setView('home');
      return;
    }
    var st = stateStats(code);
    var sc = scoring();
    var html = '';
    html += '<button type="button" class="srt-back" id="srt-back">← All states</button>';
    html += '<h1>' + escapeHtml(p.short) + ' <span class="r">' + escapeHtml(p.state) + '</span></h1>';
    html += '<p class="srt-tagline">' + escapeHtml(p.tagline) + '</p>';
    html += '<p class="srt-pill" style="margin:0 0 12px">' + st.checked + '/' + st.total + ' logged · ' + st.points + ' pts</p>';
    if (p.warning) {
      html += '<div class="srt-warn"><strong>Stay legal:</strong> ' + escapeHtml(p.warning) + '</div>';
    }

    html += '<section class="srt-section"><h2>Suspicious spots</h2><ul class="srt-check" id="srt-spots">';
    p.spots.forEach(function (spot, i) {
      var on = !!(state.progress.spots[code] && state.progress.spots[code][i]);
      html += '<li><label class="' + (on ? 'is-on' : '') + '">' +
        '<input type="checkbox" data-kind="spot" data-i="' + i + '"' + (on ? ' checked' : '') + '>' +
        '<span><span class="spot-name">' + escapeHtml(spot.name) + '</span>' +
        (spot.note ? '<span class="spot-note">' + escapeHtml(spot.note) + '</span>' : '') +
        '</span><span class="srt-pts">+' + sc.spot + '</span></label></li>';
    });
    html += '</ul></section>';

    html += '<section class="srt-section"><h2>Things that are weird</h2><ul class="srt-check" id="srt-checks">';
    p.checklist.forEach(function (item, i) {
      var on = !!(state.progress.checks[code] && state.progress.checks[code][i]);
      html += '<li><label class="' + (on ? 'is-on' : '') + '">' +
        '<input type="checkbox" data-kind="check" data-i="' + i + '"' + (on ? ' checked' : '') + '>' +
        '<span>' + escapeHtml(item) + '</span><span class="srt-pts">+' + sc.checklist + '</span></label></li>';
    });
    html += '</ul></section>';

    if (hooks.stateExtraHtml) html = hooks.stateExtraHtml(code) + html;

    root.innerHTML = html;
    $('#srt-back').addEventListener('click', function () { setView('home'); });
    $all('input[type=checkbox]', root).forEach(function (input) {
      input.addEventListener('change', function () {
        var kind = input.getAttribute('data-kind');
        var i = parseInt(input.getAttribute('data-i'), 10);
        if (kind === 'spot') {
          state.progress.spots[code] = state.progress.spots[code] || {};
          if (input.checked) state.progress.spots[code][i] = true;
          else delete state.progress.spots[code][i];
        } else {
          state.progress.checks[code] = state.progress.checks[code] || {};
          if (input.checked) state.progress.checks[code][i] = true;
          else delete state.progress.checks[code][i];
        }
        saveProgress();
        input.closest('label').classList.toggle('is-on', input.checked);
        updateChrome();
        var fresh = stateStats(code);
        var pill = root.querySelector('.srt-pill');
        if (pill) pill.textContent = fresh.checked + '/' + fresh.total + ' logged · ' + fresh.points + ' pts';
        if (input.checked) toast('Logged · +' + (kind === 'spot' ? sc.spot : sc.checklist) + ' pts');
      });
    });
  }

  function renderBadges() {
    updateChrome();
    var rank = currentRank();
    var card = $('#srt-rank-card');
    if (card) {
      var nextLine = rank.next
        ? (rank.next.min - rank.points) + ' pts to ' + rank.next.name
        : 'Top clearance unlocked';
      card.innerHTML =
        '<p class="rank-name">' + escapeHtml(rank.current.name) + '</p>' +
        '<p class="rank-sub">' + rank.points + ' agent points · ' + nextLine + '</p>' +
        '<div class="srt-bar"><span style="width:' + Math.round(rank.progress * 100) + '%"></span></div>';
    }
    var grid = $('#srt-badge-grid');
    if (!grid) return;
    grid.innerHTML = '';
    badges().forEach(function (b) {
      var el = document.createElement('div');
      el.className = 'srt-badge ' + (b.earned ? 'earned' : 'locked');
      el.innerHTML = '<div class="emoji">' + b.emoji + '</div><div><strong>' + escapeHtml(b.name) + '</strong><span>' + escapeHtml(b.desc) + '</span></div>';
      grid.appendChild(el);
    });
  }

  function buildReportText() {
    var rank = currentRank();
    var earned = badges().filter(function (b) { return b.earned; });
    var lines = [
      'CLASSIFIED // SUSPICIOUS ROAD TRIP REPORT',
      'Agent rank: ' + rank.current.name,
      'Points: ' + rank.points,
      'States touched: ' + statesTouched() + '/50',
      'Missions complete: ' + statesDone() + '/50',
      'Badges: ' + (earned.length ? earned.map(function (b) { return b.name; }).join(', ') : 'none yet'),
      '',
      'Top files:'
    ];
    var top = state.places
      .map(function (p) { return { p: p, st: stateStats(p.state) }; })
      .filter(function (x) { return x.st.checked > 0; })
      .sort(function (a, b) { return b.st.points - a.st.points; })
      .slice(0, 5);
    if (!top.length) lines.push('(No sightings logged yet.)');
    top.forEach(function (x) {
      lines.push('• ' + x.p.state + ' ' + x.p.short + ' — ' + x.st.checked + '/' + x.st.total + ' (' + x.st.points + ' pts)');
    });
    lines.push('');
    lines.push('Track weird with The Suspicious Road Trip Guide → conspiraparty.com/road-trip-app/');
    return lines.join('\n');
  }

  function renderReport() {
    updateChrome();
    var card = $('#srt-report-card');
    var text = buildReportText();
    if (card) {
      card.innerHTML =
        '<div class="stamp">Field Report</div>' +
        '<h3>Suspicious Road Trip</h3>' +
        '<pre style="margin:0;white-space:pre-wrap;font:inherit">' + escapeHtml(text) + '</pre>';
    }
    var box = $('#srt-share-box');
    if (box) {
      var shareUrl = location.href.split('#')[0];
      box.setAttribute('data-share-url', shareUrl);
      box.setAttribute('data-share-text', text.slice(0, 240));
    }
    // draw canvas image for download
    drawReportImage(text);
  }

  function drawReportImage(text) {
    var canvas = $('#srt-report-canvas');
    var dl = $('#srt-download-report');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var w = 780, h = 1100;
    canvas.width = w; canvas.height = h;
    ctx.fillStyle = '#0b0b0b';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#e11d26';
    ctx.lineWidth = 4;
    ctx.strokeRect(24, 24, w - 48, h - 48);
    ctx.fillStyle = '#e11d26';
    ctx.font = '700 28px Anton, Impact, sans-serif';
    ctx.fillText('SUSPICIOUS ROAD TRIP', 48, 80);
    ctx.fillStyle = '#f2efe8';
    ctx.font = '18px "Courier New", monospace';
    var y = 120;
    text.split('\n').forEach(function (line) {
      var words = line;
      // simple wrap
      while (words.length > 62) {
        ctx.fillText(words.slice(0, 62), 48, y);
        words = words.slice(62);
        y += 26;
      }
      ctx.fillText(words, 48, y);
      y += 26;
    });
    ctx.fillStyle = '#b8b2a6';
    ctx.font = '14px system-ui,sans-serif';
    ctx.fillText('conspiraparty.com', 48, h - 48);
    if (dl) {
      dl.href = canvas.toDataURL('image/png');
      dl.download = 'suspicious-road-trip-report.png';
    }
  }

  function renderShop() {
    updateChrome();
    var root = $('#srt-shop-list');
    if (!root || !state.meta) return;
    var html = '';
    var book = state.meta.book;
    html += '<a class="srt-soon" href="#" aria-disabled="true" id="srt-book-link">' +
      '<strong>' + escapeHtml(book.title) + ' <span class="badge-soon">Coming soon</span></strong>' +
      '<span>' + escapeHtml(book.amazon_label) + ' · ' + escapeHtml(book.price_hint || '') + '</span></a>';
    (state.meta.etsy.packs || []).forEach(function (pack) {
      html += '<a href="' + escapeHtml(pack.url) + '" target="_blank" rel="noopener sponsored">' +
        '<strong>' + escapeHtml(pack.name) + '</strong>' +
        '<span>Printable pack on Etsy · listing ' + pack.id + '</span></a>';
    });
    root.innerHTML = html;
    var bookLink = $('#srt-book-link');
    if (bookLink) {
      bookLink.addEventListener('click', function (e) {
        e.preventDefault();
        toast('Amazon link coming soon — book not live yet');
      });
    }
  }

  function nearMe() {
    /* Book places.json has no verified lat/lon for spots.
       Per product rule: do not invent coordinates. Sort by state picked. */
    var last = null;
    try { last = localStorage.getItem(LAST_STATE_KEY); } catch (e) {}
    if (!last || !state.byState[last]) {
      toast('Pick a state first — book spots have no verified GPS.');
      setView('home');
      return;
    }
    // Put focus state first, then A–Z for the rest (no invented distances).
    var rest = state.places.map(function (p) { return p.state; })
      .filter(function (c) { return c !== last; })
      .sort();
    state.nearOrder = [last].concat(rest);
    toast('Near Me: sorted from ' + last + ' (no spot GPS in book source).');
    setView('home');
    var search = $('#srt-search');
    if (search) search.value = '';
  }

  function wireNav() {
    $all('.srt-nav button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setView(btn.getAttribute('data-nav'));
      });
    });
    var near = $('#srt-near-btn');
    if (near) near.addEventListener('click', nearMe);
    var search = $('#srt-search');
    if (search) search.addEventListener('input', function () { renderHome(); });
    var copyBtn = $('#srt-copy-report');
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var text = buildReportText();
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { toast('Report copied'); });
        } else {
          window.prompt('Copy report', text);
        }
      });
    }
    var reset = $('#srt-reset');
    if (reset) {
      reset.addEventListener('click', function () {
        if (!confirm('Clear all road-trip progress on this device?')) return;
        state.progress = { checks: {}, spots: {} };
        saveProgress();
        state.nearOrder = null;
        toast('Progress cleared');
        setView('home');
      });
    }
  }

  function boot() {
    loadProgress();
    Promise.all([
      fetch('data/places.json').then(function (r) { return r.json(); }),
      fetch('data/meta.json').then(function (r) { return r.json(); })
    ]).then(function (pair) {
      state.places = pair[0];
      state.meta = pair[1];
      // Adjust ranks for realistic pacing vs max ~5605 pts
      state.meta.ranks = [
        { id: 'recruit', name: 'Recruit', min: 0 },
        { id: 'field-agent', name: 'Field Agent', min: 50 },
        { id: 'senior-agent', name: 'Senior Agent', min: 150 },
        { id: 'regional-director', name: 'Regional Director', min: 400 },
        { id: 'deputy-chief', name: 'Deputy Chief', min: 1000 },
        { id: 'chief-of-weird', name: 'Chief of Weird', min: 2500 }
      ];
      state.byState = {};
      state.places.forEach(function (p) { state.byState[p.state] = p; });
      wireNav();
      window.__SRT = {
        state: state,
        setView: setView,
        escapeHtml: escapeHtml,
        toast: toast,
        get hooks() { return hooks; },
        set hooks(v) { if (v) hooks = v; },
        ready: true
      };
      document.dispatchEvent(new CustomEvent('srt-ready'));
      setView('home');
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').catch(function () {});
      }
    }).catch(function (err) {
      console.error(err);
      var main = $('#srt-app');
      if (main) main.innerHTML = '<p style="padding:24px">Could not load road-trip data. Try a refresh.</p>';
    });
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
