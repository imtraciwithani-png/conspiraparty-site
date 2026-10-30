(function () {
  'use strict';
  function ready(fn) {
    if (window.__SRT && window.__SRT.ready) fn(window.__SRT);
    else document.addEventListener('srt-ready', function () { fn(window.__SRT); });
  }

  ready(function (SRT) {
    var MODE_KEY = 'srt-content-mode';
    var SPOOKY_KEY = 'srt-spooky-level';
    var KIDS_PROG = 'srt-kids-progress-v1';

    var family = null;
    var mode = 'kids';
    var spooky = 'mild';
    var kidsProg = {
      factReads: {},
      quizDone: {},
      gamesPlayed: {},
      investigator: false,
      certName: ''
    };
    var familyTab = 'facts';

    try {
      mode = localStorage.getItem(MODE_KEY) || 'kids';
      if (mode !== 'kids' && mode !== 'adult') mode = 'kids';
      spooky = localStorage.getItem(SPOOKY_KEY) || 'mild';
      if (spooky !== 'mild' && spooky !== 'spooky') spooky = 'mild';
      var kp = JSON.parse(localStorage.getItem(KIDS_PROG) || 'null');
      if (kp) kidsProg = Object.assign(kidsProg, kp);
    } catch (e) {}

    function saveKids() {
      try { localStorage.setItem(KIDS_PROG, JSON.stringify(kidsProg)); } catch (e) {}
    }
    function setMode(m) {
      mode = m;
      try { localStorage.setItem(MODE_KEY, m); } catch (e) {}
      document.body.classList.toggle('srt-adult-mode', m === 'adult');
      var kidsBtn = document.getElementById('srt-mode-kids');
      var adultBtn = document.getElementById('srt-mode-adult');
      if (kidsBtn) kidsBtn.setAttribute('aria-pressed', m === 'kids' ? 'true' : 'false');
      if (adultBtn) adultBtn.setAttribute('aria-pressed', m === 'adult' ? 'true' : 'false');
      var blurb = document.getElementById('srt-mode-blurb');
      if (blurb && family) {
        blurb.textContent = m === 'kids' ? family.modes.kids.blurb : family.modes.adult.blurb;
      }
      var wrap = document.getElementById('srt-spooky-wrap');
      if (wrap) wrap.hidden = m === 'adult';
      if (SRT.state.view === 'state') SRT.setView('state', { state: SRT.state.selected });
      if (SRT.state.view === 'family') renderFamily();
      if (SRT.state.view === 'home') {/* chrome only */}
      SRT.toast(m === 'adult' ? 'Adult mode — not for kids' : 'Kids mode — family-safe');
    }
    function setSpooky(level) {
      spooky = level;
      try { localStorage.setItem(SPOOKY_KEY, level); } catch (e) {}
      var mild = document.getElementById('srt-spooky-mild');
      var sp = document.getElementById('srt-spooky-spooky');
      if (mild) mild.setAttribute('aria-pressed', level === 'mild' ? 'true' : 'false');
      if (sp) sp.setAttribute('aria-pressed', level === 'spooky' ? 'true' : 'false');
      if (level === 'mild') {
        kidsProg.mildOn = true;
        saveKids();
      }
      if (SRT.state.view === 'state') SRT.setView('state', { state: SRT.state.selected });
      if (SRT.state.view === 'family') renderFamily();
    }

    function markFactRead(code) {
      if (!kidsProg.factReads[code]) {
        kidsProg.factReads[code] = true;
        saveKids();
      }
    }
    function factReadCount() { return Object.keys(kidsProg.factReads).length; }
    function quizDoneCount() { return Object.keys(kidsProg.quizDone).length; }
    function gamesPlayedCount() { return Object.keys(kidsProg.gamesPlayed).length; }

    function juniorBadges() {
      var list = (family && family.modes.kids.juniorBadges) || [];
      return list.map(function (b) {
        var earned = false;
        if (b.need === 'kids_fact_reads') earned = factReadCount() >= b.n;
        if (b.need === 'kids_quiz_done') earned = quizDoneCount() >= b.n;
        if (b.need === 'kids_games_played') earned = gamesPlayedCount() >= b.n;
        if (b.need === 'kids_investigator') earned = !!kidsProg.investigator;
        if (b.need === 'kids_mild_on') earned = !!kidsProg.mildOn || spooky === 'mild';
        if (b.need === 'kids_cert_ready') earned = certReady();
        return Object.assign({}, b, { earned: earned });
      });
    }
    function certReady() {
      return factReadCount() >= 3 && quizDoneCount() >= 1 && kidsProg.investigator;
    }

    function kidsCardHtml(code) {
      if (mode !== 'kids' || !family) return '';
      var card = family.modes.kids.states[code];
      if (!card) return '';
      markFactRead(code);
      var tone = card[spooky] || card.mild;
      return (
        '<section class="srt-section"><h2>Mystery Facts for Kids</h2>' +
        '<div class="srt-fact-card">' +
        '<p class="kicker">' + SRT.escapeHtml((spooky === 'spooky' ? 'Spooky' : 'Mild') + ' · ' + (card.theme || 'legend')) + '</p>' +
        '<h3>' + SRT.escapeHtml(card.place || code) + '</h3>' +
        '<p class="blk"><strong>The legend:</strong> ' + SRT.escapeHtml(tone.legend) + '</p>' +
        '<p class="blk"><strong>What’s real / checkable:</strong> ' + SRT.escapeHtml(tone.real) + '</p>' +
        '<p class="src">Source notes: ' + SRT.escapeHtml(card.source) + '</p>' +
        '</div></section>'
      );
    }

    function adultCardHtml(code) {
      if (mode !== 'adult' || !family) return '';
      var card = family.modes.adult.states[code];
      if (!card) return '';
      var src = (card.sources || []).map(SRT.escapeHtml).join(' · ');
      var html =
        '<section class="srt-section"><h2>Adult dossier</h2>' +
        '<div class="srt-adult-banner">Adult mode: political conspiracy culture & darker history may appear. Framed as <em>what believers say</em> vs <em>what’s documented</em> — not kid-safe.</div>' +
        '<div class="srt-adult-card">' +
        '<h3>' + SRT.escapeHtml(card.place) + '</h3>' +
        '<p class="lab">What believers say</p><p>' + SRT.escapeHtml(card.believers_say) + '</p>' +
        '<p class="lab">What’s documented</p><p>' + SRT.escapeHtml(card.documented) + '</p>' +
        '<p class="lab">Darker / adult context</p><p>' + SRT.escapeHtml(card.darker_context) + '</p>' +
        (src ? '<p class="lab">Sources / starting points</p><p>' + src + '</p>' : '') +
        '</div>';
      if (code === 'VA' || code === 'MD') {
        var b = family.modes.adult.beltway;
        html +=
          '<div class="srt-adult-card">' +
          '<h3>' + SRT.escapeHtml(b.title) + '</h3>' +
          '<p class="lab">What believers say</p><p>' + SRT.escapeHtml(b.believers_say) + '</p>' +
          '<p class="lab">What’s documented</p><p>' + SRT.escapeHtml(b.documented) + '</p>' +
          '<p class="lab">Darker / adult context</p><p>' + SRT.escapeHtml(b.darker_context) + '</p>' +
          '<p class="lab">Sources</p><p>' + (b.sources || []).map(SRT.escapeHtml).join(' · ') + '</p>' +
          '</div>';
      }
      html += '</section>';
      return html;
    }

    // Hook state page injection
    SRT.hooks = SRT.hooks || {};
    SRT.hooks.stateExtraHtml = function (code) {
      if (mode === 'kids') return kidsCardHtml(code);
      return adultCardHtml(code);
    };

    function renderFamily() {
      var root = document.getElementById('srt-family-root');
      var lede = document.getElementById('srt-family-lede');
      if (!root || !family) return;
      if (mode === 'adult') {
        if (lede) lede.textContent = 'Adult mode is on. Family HQ tools stay kid-focused—switch to Kids for quizzes, car games, and junior badges. Adult dossiers are on each state page.';
        root.innerHTML =
          '<div class="srt-adult-banner">Switch to <strong>Kids</strong> mode to use Family HQ. Adult dossiers (believers vs documented, including political conspiracy culture where relevant) appear on state pages only in Adult mode.</div>' +
          '<div class="srt-adult-card"><h3>' + SRT.escapeHtml(family.modes.adult.beltway.title) + '</h3>' +
          '<p class="lab">Preview (Adult only)</p><p>' + SRT.escapeHtml(family.modes.adult.beltway.documented) + '</p></div>' +
          '<button type="button" class="srt-btn" id="srt-switch-kids">Switch to Kids mode</button>';
        document.getElementById('srt-switch-kids').onclick = function () { setMode('kids'); renderFamily(); };
        return;
      }
      if (lede) lede.textContent = 'Mystery facts, Real-or-Legend quizzes, investigator skills, car games, junior badges, and a printable certificate.';
      var html = '<div class="srt-subtabs" id="srt-fam-tabs">';
      [['facts','Facts'],['quiz','Quiz'],['investigate','Investigate'],['games','Car games'],['junior','Junior badges'],['parents','Parents']].forEach(function (pair) {
        html += '<button type="button" data-ftab="' + pair[0] + '" aria-current="' + (familyTab === pair[0] ? 'true' : 'false') + '">' + pair[1] + '</button>';
      });
      html += '</div><div id="srt-fam-body"></div>';
      root.innerHTML = html;
      root.querySelectorAll('[data-ftab]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          familyTab = btn.getAttribute('data-ftab');
          renderFamily();
        });
      });
      var body = document.getElementById('srt-fam-body');
      if (familyTab === 'facts') body.innerHTML = renderFactsPicker();
      if (familyTab === 'quiz') body.innerHTML = renderQuiz();
      if (familyTab === 'investigate') body.innerHTML = renderInvestigate();
      if (familyTab === 'games') body.innerHTML = renderGames();
      if (familyTab === 'junior') body.innerHTML = renderJunior();
      if (familyTab === 'parents') body.innerHTML = renderParents();
      wireFamilyBody();
    }

    function renderFactsPicker() {
      var regions = SRT.state.meta.regions;
      var html = '<p class="srt-lede">Pick a state for a Mystery Facts card (uses your Mild/Spooky setting).</p>';
      html += '<label class="srt-mode-label" for="srt-fact-state">State</label>';
      html += '<select id="srt-fact-state" class="srt-search" style="margin-top:6px">';
      SRT.state.places.forEach(function (p) {
        html += '<option value="' + p.state + '">' + p.state + ' — ' + SRT.escapeHtml(p.short) + '</option>';
      });
      html += '</select><div id="srt-fact-out" style="margin-top:12px"></div>';
      return html;
    }
    function showFact(code) {
      var out = document.getElementById('srt-fact-out');
      if (!out) return;
      out.innerHTML = kidsCardHtml(code);
    }

    function renderQuiz() {
      var regions = SRT.state.meta.regions;
      var html = '<p class="srt-lede">Real or Legend? Pick a region. Answers teach, not shame.</p>';
      html += '<label class="srt-mode-label" for="srt-quiz-region">Region</label>';
      html += '<select id="srt-quiz-region" class="srt-search" style="margin-top:6px">';
      regions.forEach(function (r) {
        html += '<option value="' + r.slug + '">' + SRT.escapeHtml(r.name) + '</option>';
      });
      html += '</select><div id="srt-quiz-out" style="margin-top:12px"></div>';
      return html;
    }
    function showQuiz(slug) {
      var out = document.getElementById('srt-quiz-out');
      if (!out) return;
      var qs = family.modes.kids.quizzes[slug] || [];
      var html = '';
      qs.forEach(function (item, i) {
        html += '<div class="srt-quiz-q" data-qi="' + i + '" data-ans="' + item.answer + '">';
        html += '<p><strong>' + (i + 1) + '.</strong> ' + SRT.escapeHtml(item.prompt) + '</p>';
        html += '<div class="ans">';
        html += '<button type="button" class="srt-btn sm" data-pick="real">Real</button>';
        html += '<button type="button" class="srt-btn ghost sm" data-pick="legend">Legend</button>';
        html += '</div><p class="srt-quiz-explain" hidden></p></div>';
      });
      html += '<p class="srt-note" id="srt-quiz-score"></p>';
      out.innerHTML = html;
      var answered = 0, correct = 0;
      out.querySelectorAll('.srt-quiz-q').forEach(function (box) {
        var explain = box.querySelector('.srt-quiz-explain');
        var ans = box.getAttribute('data-ans');
        var idx = parseInt(box.getAttribute('data-qi'), 10);
        box.querySelectorAll('[data-pick]').forEach(function (btn) {
          btn.addEventListener('click', function () {
            if (box.getAttribute('data-locked')) return;
            box.setAttribute('data-locked', '1');
            var pick = btn.getAttribute('data-pick');
            var ok = pick === ans;
            box.classList.add(ok ? 'correct' : 'wrong');
            explain.hidden = false;
            explain.textContent = (ok ? 'Nice! ' : 'Not quite. ') + (family.modes.kids.quizzes[slug][idx].explain);
            answered++;
            if (ok) correct++;
            if (answered >= qs.length) {
              kidsProg.quizDone[slug] = true;
              saveKids();
              document.getElementById('srt-quiz-score').textContent =
                'Score: ' + correct + '/' + qs.length + ' · Region quiz saved for Junior badges.';
              SRT.toast('Quiz complete');
            }
          });
        });
      });
    }

    function renderInvestigate() {
      var inv = family.modes.kids.investigator;
      var html = '<h2 style="margin-top:0">' + SRT.escapeHtml(inv.title) + '</h2>';
      html += '<p class="srt-lede">' + SRT.escapeHtml(inv.lede) + '</p>';
      inv.steps.forEach(function (s, i) {
        html += '<div class="srt-fact-card"><p class="kicker">Step ' + (i + 1) + '</p><h3>' +
          SRT.escapeHtml(s.title) + '</h3><p class="blk">' + SRT.escapeHtml(s.body) + '</p></div>';
      });
      html += '<button type="button" class="srt-btn" id="srt-invest-done">' +
        (kidsProg.investigator ? 'Lesson complete ✓' : 'Mark lesson complete') + '</button>';
      return html;
    }

    function renderGames() {
      var html = '<p class="srt-lede">Backseat missions—no screens required once you start.</p>';
      family.modes.kids.carGames.forEach(function (g) {
        html += '<div class="srt-game"><strong>' + SRT.escapeHtml(g.title) +
          ' <span>· ages ' + SRT.escapeHtml(g.ages) + '</span></strong>' +
          '<p style="margin:6px 0 8px;font-size:.9rem">' + SRT.escapeHtml(g.how) + '</p>' +
          '<button type="button" class="srt-btn soft sm" data-game="' + g.id + '">' +
          (kidsProg.gamesPlayed[g.id] ? 'Played ✓' : 'We played this') + '</button></div>';
      });
      return html;
    }

    function renderJunior() {
      var html = '<p class="srt-lede">Junior agent badges unlock as you explore Family HQ.</p><div class="srt-badge-grid">';
      juniorBadges().forEach(function (b) {
        html += '<div class="srt-badge ' + (b.earned ? 'earned' : 'locked') + '"><div class="emoji">' + b.emoji +
          '</div><div><strong>' + SRT.escapeHtml(b.name) + '</strong><span>' + SRT.escapeHtml(b.desc) + '</span></div></div>';
      });
      html += '</div>';
      var cert = family.modes.kids.certificate;
      html += '<h2>Certificate</h2>';
      if (!certReady()) {
        html += '<p class="srt-note">Earn certificate when you: read 3 Mystery Fact cards, finish 1 regional quiz, and complete the Investigator lesson.</p>';
      }
      html += '<div class="srt-cert" id="srt-cert">';
      html += '<p class="kicker" style="color:var(--red)">Conspiraparty</p>';
      html += '<h3>' + SRT.escapeHtml(cert.title) + '</h3>';
      html += '<p>This certifies that</p>';
      html += '<div class="name" id="srt-cert-name">' + SRT.escapeHtml(kidsProg.certName || 'Junior Agent') + '</div>';
      html += '<p>' + SRT.escapeHtml(cert.body) + '</p>';
      html += '<p style="margin-top:14px;font-size:.8rem">' + SRT.escapeHtml(cert.signoff) + '</p></div>';
      html += '<div class="srt-actions"><input class="srt-search" id="srt-cert-input" placeholder="Agent name" value="' +
        SRT.escapeHtml(kidsProg.certName || '') + '" style="flex:1;min-width:140px">';
      html += '<button type="button" class="srt-btn sm" id="srt-cert-save">Save name</button>';
      html += '<button type="button" class="srt-btn ghost sm" id="srt-cert-print">Print / save PDF</button></div>';
      return html;
    }

    function renderParents() {
      var html = '<p class="srt-lede">Quick tips for grown-ups riding shotgun.</p><ul class="srt-check">';
      family.modes.kids.parentTips.forEach(function (tip) {
        html += '<li><label class="is-on" style="cursor:default"><span>' + SRT.escapeHtml(tip) + '</span></label></li>';
      });
      html += '</ul>';
      return html;
    }

    function wireFamilyBody() {
      var sel = document.getElementById('srt-fact-state');
      if (sel) {
        showFact(sel.value);
        sel.addEventListener('change', function () { showFact(sel.value); });
      }
      var qsel = document.getElementById('srt-quiz-region');
      if (qsel) {
        showQuiz(qsel.value);
        qsel.addEventListener('change', function () { showQuiz(qsel.value); });
      }
      var inv = document.getElementById('srt-invest-done');
      if (inv) {
        inv.addEventListener('click', function () {
          kidsProg.investigator = true;
          saveKids();
          inv.textContent = 'Lesson complete ✓';
          SRT.toast('Investigator lesson saved');
        });
      }
      document.querySelectorAll('[data-game]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          kidsProg.gamesPlayed[btn.getAttribute('data-game')] = true;
          saveKids();
          btn.textContent = 'Played ✓';
          SRT.toast('Car game logged');
        });
      });
      var save = document.getElementById('srt-cert-save');
      if (save) {
        save.addEventListener('click', function () {
          var v = (document.getElementById('srt-cert-input').value || '').trim() || 'Junior Agent';
          kidsProg.certName = v;
          saveKids();
          document.getElementById('srt-cert-name').textContent = v;
          SRT.toast('Name saved');
        });
      }
      var pr = document.getElementById('srt-cert-print');
      if (pr) {
        pr.addEventListener('click', function () {
          if (!certReady()) {
            SRT.toast('Keep exploring to unlock the certificate');
            return;
          }
          kidsProg.certReady = true;
          saveKids();
          var w = window.open('', '_blank');
          if (!w) { SRT.toast('Allow pop-ups to print'); return; }
          var cert = document.getElementById('srt-cert').innerHTML;
          w.document.write('<html><head><title>Junior Agent Certificate</title><style>body{font-family:Georgia,serif;padding:40px;background:#111;color:#f2efe8} .name{font-size:28px;border-bottom:1px solid #999;display:inline-block;min-width:50%;margin:12px 0} h3{font-size:32px}</style></head><body>' + cert + '<script>onload=function(){print()}<\/script></body></html>');
          w.document.close();
        });
      }
    }

    // Wire mode buttons
    document.getElementById('srt-mode-kids').addEventListener('click', function () { setMode('kids'); });
    document.getElementById('srt-mode-adult').addEventListener('click', function () {
      if (!confirm('Adult mode can include political conspiracy theories, Q-adjacent internet lore, and darker history. Keep Kids mode on if children can see this screen. Continue?')) return;
      setMode('adult');
    });
    document.getElementById('srt-spooky-mild').addEventListener('click', function () { setSpooky('mild'); });
    document.getElementById('srt-spooky-spooky').addEventListener('click', function () { setSpooky('spooky'); });

    SRT.hooks.renderFamily = renderFamily;

    function syncModeUi(quiet) {
      document.body.classList.toggle('srt-adult-mode', mode === 'adult');
      document.getElementById('srt-mode-kids').setAttribute('aria-pressed', mode === 'kids' ? 'true' : 'false');
      document.getElementById('srt-mode-adult').setAttribute('aria-pressed', mode === 'adult' ? 'true' : 'false');
      document.getElementById('srt-spooky-mild').setAttribute('aria-pressed', spooky === 'mild' ? 'true' : 'false');
      document.getElementById('srt-spooky-spooky').setAttribute('aria-pressed', spooky === 'spooky' ? 'true' : 'false');
      document.getElementById('srt-spooky-wrap').hidden = mode === 'adult';
      var blurb = document.getElementById('srt-mode-blurb');
      if (blurb && family) blurb.textContent = mode === 'kids' ? family.modes.kids.blurb : family.modes.adult.blurb;
      if (!quiet) SRT.toast(mode === 'adult' ? 'Adult mode — not for kids' : 'Kids mode — family-safe');
    }
    // Replace setMode body toast with syncModeUi
    fetch('data/family.json').then(function (r) { return r.json(); }).then(function (data) {
      family = data;
      syncModeUi(true);
    }).catch(function (err) { console.error('family.json', err); });

    // Patch setMode to use syncModeUi — redefine by wrapping buttons already bound
    // Buttons call setMode which already toasts; keep that for user clicks.
  });
})();
