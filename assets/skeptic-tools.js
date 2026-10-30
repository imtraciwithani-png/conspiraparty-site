/* Shared skeptic-tools helpers */
(function () {
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  async function loadJSON(path) {
    const r = await fetch(path, { cache: 'no-store' });
    if (!r.ok) throw new Error('Failed to load ' + path);
    return r.json();
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ---- Document Vault ---- */
  async function initVault() {
    const root = $('#vault-app');
    if (!root) return;
    const data = await loadJSON('data/document-vault.json');
    const list = $('#vault-list');
    const q = $('#vault-q');
    const topic = $('#vault-topic');
    const count = $('#vault-count');
    const topics = new Set();
    data.docs.forEach(d => (d.topics || []).forEach(t => topics.add(t)));
    const topicLabels = {
      jfk: 'JFK', deepstate: 'Deep State', mkultra: 'MKUltra', nine11: '9/11',
      epstein: 'Epstein', uap: 'UAP', area51: 'Area 51', fed: 'Federal Reserve',
      rothschilds: 'Banking', bilderberg: 'Bilderberg / WEF'
    };
    [...topics].sort().forEach(t => {
      const o = document.createElement('option');
      o.value = t; o.textContent = topicLabels[t] || t;
      topic.appendChild(o);
    });

    function render() {
      const query = (q.value || '').trim().toLowerCase();
      const top = topic.value;
      const filtered = data.docs.filter(d => {
        if (top && !(d.topics || []).includes(top)) return false;
        if (!query) return true;
        const blob = [d.title, d.summary, d.agency, ...(d.tags || [])].join(' ').toLowerCase();
        return blob.includes(query);
      });
      count.textContent = filtered.length + ' of ' + data.docs.length + ' files';
      list.innerHTML = filtered.map(d => `
        <article class="sk-card" id="${esc(d.id)}">
          <span class="sk-kind">${esc(d.kind || 'Primary document')}</span>
          <h3>${esc(d.title)}</h3>
          <p class="sk-meta">${esc(d.agency || '')} · ${esc(d.date || '')}</p>
          <p>${esc(d.summary)}</p>
          <p class="sk-dig"><a href="${esc(d.url)}" target="_blank" rel="noopener">Open record ↗</a></p>
          <div class="sk-tags">${(d.tags || []).map(t => `<span class="sk-tag">${esc(t)}</span>`).join('')}</div>
        </article>`).join('') || '<p class="sk-empty">No matches. Try another word or clear filters.</p>';
    }
    q.addEventListener('input', render);
    topic.addEventListener('change', render);
    render();
  }

  /* ---- Timeline ---- */
  async function initTimeline() {
    const root = $('#timeline-app');
    if (!root) return;
    const data = await loadJSON('data/timelines.json');
    const pick = $('#timeline-topic');
    const stage = $('#timeline-stage');
    data.topics.forEach(t => {
      const o = document.createElement('option');
      o.value = t.id; o.textContent = t.label;
      pick.appendChild(o);
    });
    function render() {
      const t = data.topics.find(x => x.id === pick.value) || data.topics[0];
      if (!t) return;
      stage.innerHTML = `<h2 class="center" style="color:#fff;margin:8px 0 16px">${esc(t.label)}</h2>
        <div class="sk-timeline">${t.events.map(e => `
          <article class="sk-event">
            <p class="when">${esc(e.date)}</p>
            <p class="claimed"><strong>What was claimed:</strong> ${esc(e.claimed)}</p>
            <p class="surfaced"><strong>What surfaced later:</strong> ${esc(e.surfaced)}</p>
            <p class="sk-dig"><a href="${esc(e.record)}" target="_blank" rel="noopener">What's on the record ↗</a></p>
          </article>`).join('')}</div>`;
    }
    pick.addEventListener('change', render);
    if (data.topics[0]) pick.value = data.topics[0].id;
    render();
  }

  /* ---- Scoreboard ---- */
  async function initScoreboard() {
    const root = $('#scoreboard-app');
    if (!root) return;
    const data = await loadJSON('data/scoreboard.json');
    const called = $('#score-called');
    const open = $('#score-open');
    function card(item, kind) {
      return `<article class="sk-card">
        <span class="sk-kind">${kind}</span>
        <h3>${esc(item.title)}</h3>
        <p>${esc(item.blurb)}</p>
        ${item.when_called ? `<p class="sk-meta">Called: ${esc(item.when_called)} · On record: ${esc(item.when_record || '')}</p>` : ''}
        <p class="sk-dig"><a href="${esc(item.record_url)}" target="_blank" rel="noopener">${esc(item.record_label || 'Record link')} ↗</a></p>
        <div class="sk-tags">${(item.tags || []).map(t => `<span class="sk-tag">${esc(t)}</span>`).join('')}</div>
      </article>`;
    }
    called.innerHTML = (data.called_it || []).map(i => card(i, 'Called it')).join('');
    open.innerHTML = (data.still_open || []).map(i => card(i, 'Still open')).join('');
  }

  /* ---- Follow the money ---- */
  async function initMoney() {
    const root = $('#money-app');
    if (!root) return;
    const data = await loadJSON('data/follow-the-money.json');
    const pick = $('#money-topic');
    const stage = $('#money-stage');
    data.cards.forEach(c => {
      const o = document.createElement('option');
      o.value = c.id; o.textContent = c.topic;
      pick.appendChild(o);
    });
    function block(title, items) {
      if (!items || !items.length) return '';
      return `<h4>${esc(title)}</h4><ul>${items.map(i => `
        <li><strong>${esc(i.who)}</strong> — ${esc(i.detail)}
        <div class="sk-dig"><a href="${esc(i.url)}" target="_blank" rel="noopener">Record ↗</a></div></li>`).join('')}</ul>`;
    }
    function render() {
      const c = data.cards.find(x => x.id === pick.value) || data.cards[0];
      if (!c) return;
      stage.innerHTML = `<article class="sk-card sk-money">
        <h3>${esc(c.topic)}</h3>
        ${block('Who funded', c.funded)}
        ${block('Who profited', c.profited)}
        ${block('Who testified', c.testified)}
      </article>`;
    }
    pick.addEventListener('change', render);
    if (data.cards[0]) pick.value = data.cards[0].id;
    render();
  }

  /* ---- Reader leads ---- */
  async function initLeads() {
    const root = $('#leads-app');
    if (!root) return;
    try {
      const data = await loadJSON('data/reader-leads.json');
      if (!data.leads || !data.leads.length) {
        root.innerHTML = '<p class="sk-empty">No approved reader leads yet. Submit one above — Traci reviews before anything is posted.</p>';
        return;
      }
      root.innerHTML = data.leads.map(l => `<article class="sk-card"><h3>${esc(l.title)}</h3><p>${esc(l.blurb)}</p></article>`).join('');
    } catch (e) {
      root.innerHTML = '<p class="sk-empty">No approved reader leads yet.</p>';
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initVault().catch(console.error);
    initTimeline().catch(console.error);
    initScoreboard().catch(console.error);
    initMoney().catch(console.error);
    initLeads().catch(console.error);
  });
})();
