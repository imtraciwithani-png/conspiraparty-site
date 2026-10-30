(function () {
  'use strict';
  var dataUrl = 'data/rabbit-hole-map.json?v=labels';
  var stage = document.getElementById('rh-stage');
  var panel = document.getElementById('rh-panel');
  var list = document.getElementById('rh-list');
  if (!stage || !panel) return;

  var state = {
    data: null,
    mode: 'both', // bunk | debunk | both
    active: null,
    news: null,
    scale: 1,
    tx: 0,
    ty: 0,
    dragging: false,
    lastX: 0,
    lastY: 0,
    pointers: new Map(),
    pinchStartDist: 0,
    pinchStartScale: 1
  };

  var gWorld = null;

  function fetchData() {
    var newsUrl = 'data/rhmap-news.json?v=news1';
    var mapP = fetch(dataUrl, { credentials: 'same-origin' }).then(function (r) { return r.json(); });
    var newsP = fetch(newsUrl, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
    return Promise.all([mapP, newsP])
      .then(function (pair) {
        var d = pair[0];
        state.data = d;
        state.news = pair[1];
        if (state.news && state.news.topics) {
          window.__RH_BREAKING = state.news.topics;
        }
        buildMap();
        buildList();
        bindToolbar();
        var hash = (location.hash || '').replace(/^#/, '');
        if (hash && d.content[hash]) selectNode(hash, false);
      })
      .catch(function (e) {
        stage.innerHTML = '<text x="20" y="40" fill="#fff">Could not load map data.</text>';
        console.error(e);
      });
  }

  function nodeById(id) {
    return state.data.nodes.find(function (n) { return n.id === id; });
  }

  function neighbors(id) {
    var set = {};
    state.data.edges.forEach(function (e) {
      if (e.a === id) set[e.b] = 1;
      if (e.b === id) set[e.a] = 1;
    });
    return Object.keys(set);
  }

  function buildMap() {
    var NS = 'http://www.w3.org/2000/svg';
    while (stage.firstChild) stage.removeChild(stage.firstChild);
    var vb = '0 0 1000 640';
    stage.setAttribute('viewBox', vb);
    stage.setAttribute('role', 'img');
    stage.setAttribute('aria-label', 'Corkboard rabbit hole map. Drag to pan, pinch or scroll to zoom, tap a node to dig.');

    gWorld = document.createElementNS(NS, 'g');
    gWorld.setAttribute('id', 'rh-world');
    stage.appendChild(gWorld);

    // cork tint rect
    var bg = document.createElementNS(NS, 'rect');
    bg.setAttribute('x', 0); bg.setAttribute('y', 0);
    bg.setAttribute('width', 1000); bg.setAttribute('height', 640);
    bg.setAttribute('fill', '#6b4330');
    gWorld.appendChild(bg);

    // edges
    state.data.edges.forEach(function (e, i) {
      var a = nodeById(e.a), b = nodeById(e.b);
      if (!a || !b) return;
      var line = document.createElementNS(NS, 'line');
      line.setAttribute('class', 'rh-edge');
      line.setAttribute('data-a', e.a);
      line.setAttribute('data-b', e.b);
      line.setAttribute('x1', a.x); line.setAttribute('y1', a.y);
      line.setAttribute('x2', b.x); line.setAttribute('y2', b.y);
      // slight wobble via quadratic approximation: use path
      var mx = (a.x + b.x) / 2 + ((i % 2) ? 12 : -12);
      var my = (a.y + b.y) / 2 + ((i % 3) ? 10 : -10);
      var path = document.createElementNS(NS, 'path');
      path.setAttribute('class', 'rh-edge');
      path.setAttribute('data-a', e.a);
      path.setAttribute('data-b', e.b);
      path.setAttribute('d', 'M' + a.x + ' ' + a.y + ' Q' + mx + ' ' + my + ' ' + b.x + ' ' + b.y);
      gWorld.appendChild(path);
    });

    // nodes — pin + always-visible cream paper tag
    state.data.nodes.forEach(function (n) {
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', 'rh-node');
      g.setAttribute('data-id', n.id);
      g.setAttribute('tabindex', '0');
      g.setAttribute('role', 'button');
      g.setAttribute('aria-label', n.label);
      var c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', n.x); c.setAttribute('cy', n.y);
      c.setAttribute('r', 18);
      // red pushpin head
      var pin = document.createElementNS(NS, 'circle');
      pin.setAttribute('class', 'rh-pin');
      pin.setAttribute('cx', n.x); pin.setAttribute('cy', n.y);
      pin.setAttribute('r', 6);

      var tagLabel = n.short || n.label;
      var lines = wrapLabel(tagLabel, 14);
      var longest = lines.reduce(function (m, s) { return Math.max(m, s.length); }, 0);
      var tw = Math.max(72, Math.min(210, longest * 11 + 28));
      var lineH = 18;
      var th = 14 + lines.length * lineH;
      var tagX = clamp(n.x - tw / 2, 4, 996 - tw);
      var tagY = n.y + 22;
      if (tagY + th > 636) tagY = Math.max(4, n.y - th - 22);

      var shadow = document.createElementNS(NS, 'rect');
      shadow.setAttribute('class', 'rh-tag-shadow');
      shadow.setAttribute('x', tagX + 3); shadow.setAttribute('y', tagY + 3);
      shadow.setAttribute('width', tw); shadow.setAttribute('height', th);
      shadow.setAttribute('rx', 3);

      var tag = document.createElementNS(NS, 'rect');
      tag.setAttribute('class', 'rh-tag');
      tag.setAttribute('x', tagX); tag.setAttribute('y', tagY);
      tag.setAttribute('width', tw); tag.setAttribute('height', th);
      tag.setAttribute('rx', 3);

      var t = document.createElementNS(NS, 'text');
      t.setAttribute('class', 'rh-tag-text');
      t.setAttribute('x', tagX + tw / 2);
      t.setAttribute('y', tagY + 12 + lineH * 0.72);
      t.setAttribute('text-anchor', 'middle');
      lines.forEach(function (line, i) {
        var tsp = document.createElementNS(NS, 'tspan');
        tsp.setAttribute('x', tagX + tw / 2);
        tsp.setAttribute('dy', i === 0 ? 0 : lineH);
        tsp.textContent = line;
        t.appendChild(tsp);
      });

      g.appendChild(shadow); g.appendChild(tag); g.appendChild(c); g.appendChild(pin); g.appendChild(t);
      g.addEventListener('click', function (ev) {
        ev.stopPropagation();
        selectNode(n.id, true);
      });
      g.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          selectNode(n.id, true);
        }
      });
      gWorld.appendChild(g);
    });

    applyTransform();
    bindPanZoom();
  }

  function applyTransform() {
    if (!gWorld) return;
    gWorld.setAttribute('transform', 'translate(' + state.tx + ',' + state.ty + ') scale(' + state.scale + ')');
  }

  function bindPanZoom() {
    stage.addEventListener('pointerdown', function (e) {
      if (e.target.closest && e.target.closest('.rh-node')) return;
      stage.setPointerCapture(e.pointerId);
      state.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (state.pointers.size === 1) {
        state.dragging = true;
        state.lastX = e.clientX; state.lastY = e.clientY;
      } else if (state.pointers.size === 2) {
        var pts = Array.from(state.pointers.values());
        state.pinchStartDist = dist(pts[0], pts[1]);
        state.pinchStartScale = state.scale;
      }
    });
    stage.addEventListener('pointermove', function (e) {
      if (!state.pointers.has(e.pointerId)) return;
      state.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (state.pointers.size === 2) {
        var pts = Array.from(state.pointers.values());
        var d = dist(pts[0], pts[1]);
        if (state.pinchStartDist > 0) {
          var next = state.pinchStartScale * (d / state.pinchStartDist);
          state.scale = clamp(next, 0.55, 2.8);
          applyTransform();
        }
      } else if (state.dragging && state.pointers.size === 1) {
        var dx = e.clientX - state.lastX;
        var dy = e.clientY - state.lastY;
        state.lastX = e.clientX; state.lastY = e.clientY;
        // convert screen delta roughly into svg units
        var rect = stage.getBoundingClientRect();
        state.tx += dx * (1000 / rect.width);
        state.ty += dy * (640 / rect.height);
        applyTransform();
      }
    });
    function endPtr(e) {
      state.pointers.delete(e.pointerId);
      if (state.pointers.size < 2) state.pinchStartDist = 0;
      if (state.pointers.size === 0) state.dragging = false;
    }
    stage.addEventListener('pointerup', endPtr);
    stage.addEventListener('pointercancel', endPtr);
    stage.addEventListener('wheel', function (e) {
      e.preventDefault();
      var factor = e.deltaY > 0 ? 0.92 : 1.08;
      state.scale = clamp(state.scale * factor, 0.55, 2.8);
      applyTransform();
    }, { passive: false });
  }

  function dist(a, b) {
    var dx = a.x - b.x, dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  function wrapLabel(label, maxChars) {
    if (!label || label.length <= maxChars) return [label];
    var parts = label.split(' ');
    if (parts.length === 1) {
      return [label.slice(0, maxChars), label.slice(maxChars)];
    }
    var mid = Math.ceil(parts.length / 2);
    return [parts.slice(0, mid).join(' '), parts.slice(mid).join(' ')];
  }


  function highlight(id) {
    var neigh = neighbors(id);
    stage.querySelectorAll('.rh-node').forEach(function (g) {
      var nid = g.getAttribute('data-id');
      g.classList.remove('is-hot', 'is-dim');
      if (nid === id) g.classList.add('is-hot');
      else if (neigh.indexOf(nid) === -1) g.classList.add('is-dim');
      else g.classList.add('is-hot');
    });
    stage.querySelectorAll('.rh-edge').forEach(function (el) {
      var a = el.getAttribute('data-a'), b = el.getAttribute('data-b');
      el.classList.remove('is-hot', 'is-dim');
      if (a === id || b === id) el.classList.add('is-hot');
      else el.classList.add('is-dim');
    });
  }

  function clearHighlight() {
    stage.querySelectorAll('.rh-node, .rh-edge').forEach(function (el) {
      el.classList.remove('is-hot', 'is-dim');
    });
  }

  function selectNode(id, pushHash) {
    if (!state.data.content[id]) return;
    state.active = id;
    highlight(id);
    renderPanel(id);
    if (pushHash) {
      try { history.replaceState(null, '', '#' + id); } catch (e) {}
    }
    panel.hidden = false;
    panel.focus && panel.focus();
    setTimeout(function () {
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
  }

  function kindBadge(k) {
    return '<span class="kind">' + escapeHtml(k) + '</span>';
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  function renderPanel(id) {
    var c = state.data.content[id];
    var n = nodeById(id);
    var mode = state.mode;
    var html = '';
    html += '<button type="button" class="btn sm" id="rh-close" style="float:right">Close</button>';
    html += '<h2>' + escapeHtml(n.label) + '</h2>';
    html += '<p class="rh-hook">' + escapeHtml(c.hook) + '</p>';

    if (id === 'rothschilds') {
      html += '<p class="rh-antisem"><strong>Read this first:</strong> Banking and central-bank power are fair game to question. Tropes that treat Jewish people as a secret controlling group are an old hate script (including the forged <em>Protocols of the Elders of Zion</em>). This node stays about institutions and the history of the theory — never about an ethnicity or religion.</p>';
    }

    // paths
    html += '<h3>Paths from here</h3><div class="rh-paths">';
    (c.paths || []).forEach(function (p) {
      html += '<div class="rh-path"><strong>' + escapeHtml(p.title) + '</strong>';
      html += '<span>' + escapeHtml(p.blurb) + '</span>';
      if (p.to) html += ' <a href="#' + escapeHtml(p.to) + '" data-jump="' + escapeHtml(p.to) + '">→ ' + escapeHtml((nodeById(p.to) || {}).label || p.to) + '</a>';
      html += '</div>';
    });
    html += '</div>';

    // Bunk / Debunk
    if (mode === 'bunk' || mode === 'both') {
      html += '<div class="rh-side" data-side="bunk"><p class="rh-side-label">Bunk — the case believers make</p><p>' + escapeHtml(c.bunk) + '</p>';
      html += '<p><strong>What believers say:</strong> ' + escapeHtml(c.believers) + '</p></div>';
    }
    if (mode === 'debunk' || mode === 'both') {
      html += '<div class="rh-side" data-side="debunk"><p class="rh-side-label">Debunk — the skeptic case</p><p>' + escapeHtml(c.debunk) + '</p></div>';
    }

    html += '<h3>What\'s on the record</h3><p>' + escapeHtml(c.on_record) + '</p>';

    html += '<h3>Unanswered questions</h3><ul>';
    (c.unanswered || []).forEach(function (q) { html += '<li>' + escapeHtml(q) + '</li>'; });
    html += '</ul>';

    // Breaking (multi-source feed from data/rhmap-news.json)
    var newsMeta = (state.news && state.news.generated_at_display) || state.data.weird_news_updated || '';
    html += '<div class="rh-break"><p class="rh-break-meta">Breaking · multi-source · updated ' + escapeHtml(newsMeta) + '</p>';
    var breaking = [];
    if (state.news && state.news.topics && state.news.topics[id]) breaking = state.news.topics[id];
    else if (window.__RH_BREAKING && window.__RH_BREAKING[id]) breaking = window.__RH_BREAKING[id];
    if (breaking.length) {
      breaking.forEach(function (it) {
        var kind = it.kind || '';
        html += '<div class="rh-break-item">';
        if (kind) html += '<span class="rh-kind rh-kind-' + escapeHtml(kind.toLowerCase()) + '">' + escapeHtml(kind) + '</span>';
        html += '<a href="' + escapeHtml(it.url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(it.title) + '</a>';
        html += '<div class="rh-break-meta-line">' + escapeHtml(it.published_display || '') + (it.source ? ' · ' + escapeHtml(it.source) : '') + '</div>';
        html += '</div>';
      });
    } else {
      html += '<a href="weird-news.html">No fresh match for this node yet — browse Weird News</a>';
    }
    html += '</div>';

    html += '<h3>Talk about it</h3><ul>';
    (c.talk || []).forEach(function (q) { html += '<li>' + escapeHtml(q) + '</li>'; });
    html += '</ul>';

    html += '<h3>Connect the dots</h3><p>';
    (c.connect || []).forEach(function (cid) {
      var nn = nodeById(cid);
      if (!nn) return;
      html += '<a class="btn sm" href="#' + cid + '" data-jump="' + cid + '">' + escapeHtml(nn.label) + '</a> ';
    });
    html += '</p>';

    html += '<h3>Primary documents</h3><ul class="rh-dig">';
    (c.primary || []).forEach(function (l) {
      html += '<li>' + kindBadge(l.kind) + '<a href="' + escapeHtml(l.url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(l.title) + '</a></li>';
    });
    html += '</ul>';

    html += '<h3>Dig in yourself</h3><ul class="rh-dig">';
    (c.dig || []).forEach(function (l) {
      var href = l.url;
      var target = href.indexOf('http') === 0 ? ' target="_blank" rel="noopener noreferrer"' : '';
      html += '<li>' + kindBadge(l.kind) + '<a href="' + escapeHtml(href) + '"' + target + '>' + escapeHtml(l.title) + '</a></li>';
    });
    html += '</ul>';

    // Dig deeper: books (affiliate) + weird tours (Viator placeholder)
    if (c.books && c.books.length) {
      html += '<div class="rh-aff">';
      html += '<p class="rh-aff-label">Dig deeper: books</p>';
      html += '<ul class="rh-aff-list">';
      c.books.forEach(function (b) {
        html += '<li><a href="' + escapeHtml(b.url) + '" target="_blank" rel="noopener sponsored">' + escapeHtml(b.title) + '</a></li>';
      });
      html += '</ul>';
      html += '<p class="rh-aff-note">As an Amazon Associate, Conspiraparty earns from qualifying purchases.</p>';
      html += '</div>';
    }
    if (c.tour && c.tour.url) {
      html += '<div class="rh-aff rh-aff-tour">';
      html += '<p class="rh-aff-label">Book a weird tour</p>';
      html += '<p class="rh-aff-tour-line"><a href="' + escapeHtml(c.tour.url) + '" target="_blank" rel="noopener sponsored">' + escapeHtml(c.tour.label || 'Browse tours') + '</a></p>';
      html += '<p class="rh-aff-note">Tour links may earn a commission. Viator affiliate ID pending signup.</p>';
      html += '</div>';
    }

    if (c.site && c.site.length) {
      html += '<h3>On this site</h3><p>';
      c.site.forEach(function (s) {
        html += '<a class="btn sm" href="' + escapeHtml(s[1]) + '">' + escapeHtml(s[0]) + '</a> ';
      });
      html += '</p>';
    }

    if (c.hint) {
      html += '<p class="rh-hint-soft">' + escapeHtml(c.hint) + '</p>';
    }

    panel.innerHTML = html;
    panel.querySelector('#rh-close').addEventListener('click', function () {
      panel.hidden = true;
      clearHighlight();
      state.active = null;
    });
    panel.querySelectorAll('[data-jump]').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        selectNode(a.getAttribute('data-jump'), true);
      });
    });
  }

  function buildList() {
    if (!list) return;
    list.innerHTML = '';
    state.data.nodes
      .slice()
      .sort(function (a, b) { return a.label.localeCompare(b.label); })
      .forEach(function (n) {
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = n.label;
        b.addEventListener('click', function () { selectNode(n.id, true); });
        list.appendChild(b);
      });
  }

  function bindToolbar() {
    document.querySelectorAll('[data-rh-mode]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        state.mode = btn.getAttribute('data-rh-mode');
        document.querySelectorAll('[data-rh-mode]').forEach(function (b) {
          b.classList.toggle('is-on', b === btn);
        });
        if (state.active) renderPanel(state.active);
      });
    });
    var both = document.querySelector('[data-rh-mode="both"]');
    if (both) both.classList.add('is-on');
    var reset = document.getElementById('rh-reset');
    if (reset) reset.addEventListener('click', function () {
      state.scale = 1; state.tx = 0; state.ty = 0; applyTransform();
    });
  }

  // Embed breaking news from inline script if present
  window.__RH_BREAKING = window.__RH_BREAKING || {};

  fetchData();
})();
