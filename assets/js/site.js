var VERIF = {'fr': 'lettres vérifiées sur le scan : erreur probable du chiffreur ; voir le caractère proposé dans la version lisible', 'en': 'letters checked on the scan: probably an encipherer\'s error; see the proposed character in the readable version', 'zh-Hant': '字母已對照掃描影像核實：可能是發報人加密時的錯誤；請參見可讀版本中建議的字', 'zh-Hans': '字母已对照扫描影像核实：可能是发报人加密时的错误；请参见可读版本中建议的字', 'ja': '文字は画像で確認済み：暗号化した者の誤りと思われる。読み下しの提案字を参照'};
// Wenmi — scripts communs : thème, grille G0, décodeur pas à pas.
(function () {
  'use strict';

  // ---------- thème clair / sombre ----------
  var root = document.documentElement;
  try { var saved = localStorage.getItem('wenmi-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.theme-toggle');
    if (!b) return;
    var dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('wenmi-theme', next); } catch (e) {}
  });

  // ---------- langue choisie : mémorisée pour la page d'accueil racine ----------
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('.lang-switch a[data-lang]');
    if (a) { try { localStorage.setItem('wenmi-lang', a.dataset.lang); } catch (e) {} }
  });

  // ---------- menu des langues : fermeture au clic extérieur ou par Échap ----------
  var langMenu = document.querySelector('.lang-switch details');
  if (langMenu) {
    document.addEventListener('click', function (ev) { if (langMenu.open && !langMenu.contains(ev.target)) langMenu.open = false; });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && langMenu.open) { langMenu.open = false; langMenu.querySelector('summary').focus(); }
    });
  }

  // ---------- hauteur réelle de l'en-tête : le sommaire flottant se cale dessous ----------
  var head = document.querySelector('.site-header');
  function headH() { if (head) root.style.setProperty('--head-h', head.offsetHeight + 'px'); }
  headH(); window.addEventListener('resize', headH);

  // ---------- grilles G0 (canal de Cen) et Y0 (canal du Yunnan) ----------
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  var GRIDS = {
    // G0 : 20 consonnes (alphabet inversé depuis h), deux par dizaine ; voyelles a e i o u en serpentin.
    G0: (function () {
      var C = 'hgfdcbzyxwvtsrqpnmlk', V = 'aeiou', T = {};
      for (var i = 0; i < C.length; i++) for (var j = 0; j < 5; j++)
        T[C[i] + V[j]] = 10 * Math.floor(i / 2) + (i % 2 === 0 ? j : 9 - j);
      return { cons: C, vow: V, table: T };
    })(),
    // Y0 : 17 consonnes (ordre alphabétique sans c, j, q) × 6 voyelles ; valeur = 6 × rang + rang de la voyelle (serpentin).
    Y0: (function () {
      var C = 'bdfghklmnprstvwxz', V = 'aeiouy', T = {};
      for (var i = 0; i < C.length; i++) {
        var ord = i % 2 === 0 ? 'yuoiea' : 'aeiouy';
        for (var r = 0; r < 6; r++) T[C[i] + ord[r]] = 6 * i + r;
      }
      return { cons: C, vow: V, table: T };
    })()
  };

  function renderGrid(el, key) {
    var g = GRIDS[key], h = '<div class="table-wrap"><table class="grid-g0" data-grid="' + key + '"><thead><tr><th>' + key + '</th>';
    for (var j = 0; j < g.vow.length; j++) h += '<th>' + g.vow[j] + '</th>';
    h += '</tr></thead><tbody>';
    for (var i = 0; i < g.cons.length; i++) {
      var c = g.cons[i];
      h += '<tr class="' + (i % 2 ? 'odd' : '') + '"><th>' + c + '</th>';
      for (var k = 0; k < g.vow.length; k++) {
        var v = g.table[c + g.vow[k]];
        h += '<td data-s="' + c + g.vow[k] + '">' + (v > 99 ? '—' : pad(v)) + '</td>';
      }
      h += '</tr>';
    }
    el.innerHTML = h + '</tbody></table></div>';
  }
  function highlight(scope, syl) {
    scope.querySelectorAll('.grid-g0 td.hit').forEach(function (td) { td.classList.remove('hit'); });
    (syl || []).forEach(function (s) {
      scope.querySelectorAll('.grid-g0 td[data-s="' + s + '"]').forEach(function (td) { td.classList.add('hit'); });
    });
  }
  document.querySelectorAll('[data-grid]').forEach(function (el) { if (el.tagName !== 'TABLE') renderGrid(el, el.getAttribute('data-grid')); });
  document.querySelectorAll('[data-g0-grid]').forEach(function (el) { renderGrid(el, 'G0'); });

  // ---------- décodeur ----------
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function mountDecoder(box) {
    var all = (window.WENMI_MESSAGES || []).map(function (m) { m.grid = m.grid || 'G0'; return m; })
      .concat(window.WENMI_MESSAGES_Y0 || []);
    if (!all.length) return;
    var I = (window.WENMI_I18N || {})[root.lang] || (window.WENMI_I18N || {}).fr;
    var byId = {}; all.forEach(function (m) { byId[m.id] = m; });
    var msgs = I.order.map(function (id) { return byId[id]; }).filter(Boolean);
    var sel = box.querySelector('select');
    var groups = {};
    msgs.forEach(function (m, idx) {
      if (!groups[m.grid]) {
        groups[m.grid] = document.createElement('optgroup');
        groups[m.grid].label = (I.channel || {})[m.grid] || m.grid;
        sel.appendChild(groups[m.grid]);
      }
      var o = document.createElement('option');
      o.value = idx; o.textContent = m.id + ' — ' + (I.date[m.id] || '');
      groups[m.grid].appendChild(o);
    });
    var gridBox = box.querySelector('.dec-grid'), shownGrid = null;
    var want = box.getAttribute('data-default');
    msgs.forEach(function (m, idx) { if (m.id === want) sel.value = idx; });
    var cipher = box.querySelector('.cipher'), toks = box.querySelector('.tokens'), meta = box.querySelector('.meta');
    var step = -1, timer = null;

    function draw() {
      var m = msgs[+sel.value];
      // flux de lettres, regroupé en mots de dix lettres comme sur le formulaire
      var letters = m.units.join(''), h = '';
      for (var p = 0; p < letters.length; p++) {
        if (p && p % 10 === 0) h += ' ';
        h += '<span data-i="' + Math.floor(p / 4) + '">' + letters[p] + '</span>';
      }
      cipher.innerHTML = h;
      var t = '';
      m.codes.forEach(function (code, i) {
        var d = m.doubt.indexOf(i) >= 0;
        t += '<button type="button" class="token' + (d ? ' doubt' : '') + '" data-i="' + i + '" title="' +
          (d ? I.doubt : code) + '">' +
          '<span class="u">' + m.units[2 * i] + '·' + m.units[2 * i + 1] + '</span>' +
          '<span class="c">' + code + '</span><span class="h" lang="zh-Hant">' + esc(m.chars[i]) + '</span></button>';
      });
      toks.innerHTML = t;
      meta.innerHTML = '<strong>' + esc(I.label) + '</strong> ' + esc(I.tr[m.id] || '');
      if (gridBox && shownGrid !== m.grid) { renderGrid(gridBox, m.grid); shownGrid = m.grid; }
      step = -1; highlight(box, []);
    }
    function focus(i) {
      var m = msgs[+sel.value];
      step = i;
      toks.querySelectorAll('.token').forEach(function (b) { b.classList.toggle('on', +b.dataset.i === i); });
      cipher.querySelectorAll('span').forEach(function (s) { s.classList.toggle('on', +s.dataset.i === i); });
      if (i >= 0) highlight(box, [m.units[2 * i], m.units[2 * i + 1]]);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; box.querySelector('[data-act=play]').textContent = I.play; } }
    sel.addEventListener('change', function () { stop(); draw(); });
    toks.addEventListener('click', function (ev) { var b = ev.target.closest('.token'); if (b) { stop(); focus(+b.dataset.i); } });
    box.querySelector('[data-act=play]').addEventListener('click', function () {
      if (timer) { stop(); return; }
      this.textContent = I.pause;
      timer = setInterval(function () {
        var n = msgs[+sel.value].codes.length;
        if (step + 1 >= n) { stop(); return; }
        focus(step + 1);
      }, 650);
    });
    box.querySelector('[data-act=play]').textContent = I.play;
    draw();
  }
  document.querySelectorAll('.decoder').forEach(mountDecoder);

  // ---------- page « Télégrammes » : corpus complet, statut de chaque code, pistes d'erreur ----------
  function mountCorpus(box) {
    var C = window.WENMI_CORPUS, I = (window.WENMI_I18N || {})[root.lang] || (window.WENMI_I18N || {}).fr;
    var Lel = document.getElementById('corpus-labels');
    if (!C || !Lel) return;
    var L = JSON.parse(Lel.textContent);
    var morse = function (m) { return m.replace(/\./g, '·').replace(/-/g, '−'); };
    var kindLabel = function (k) { return L.kind[k] || k; };
    var h = '<p class="corpus-stats">' + L.stats.replace('{codes}', C.stats.codes).replace('{douteux}', C.stats['douteux'])
      .replace('{conf}', C.stats['confirmé']).replace('{ill}', C.stats.illisible) + '</p>';
    h += '<nav class="corpus-toc">';
    ['G0', 'Y0'].forEach(function (g) {
      h += '<div><strong>' + esc((I.channel || {})[g] || g) + '</strong> ';
      C.messages.filter(function (m) { return m.grid === g; }).forEach(function (m) { h += '<a href="#t' + m.id + '">' + m.id + '</a> '; });
      h += '</div>';
    });
    h += '<div><strong>' + esc(L.y1917) + '</strong> <a href="#t1917">0509a · 0511</a></div>';
    var KX0 = window.WENMI_C1916_I18N, KI0 = KX0 ? (KX0[root.lang] || KX0.fr) : null;
    if (window.WENMI_C1916 && KI0) {
      h += '<div><strong>' + esc(KI0.toc) + '</strong> ' + window.WENMI_C1916.order.map(function (g) {
        var first = window.WENMI_C1916.messages.filter(function (m) { return m.grid === g; })[0];
        return first ? '<a href="#t' + first.id + '">' + esc(KI0.short[g] || g) + '</a>' : '';
      }).join(' · ') + '</div>';
    }
    h += '</nav>';
    function tg(m, I, X) {
      var h = '<section class="tg" id="t' + m.id + '"><h2>' + (m.label || m.id) + ' <small>' + esc(I.date[m.id] || '') + '</small></h2>';
      h += '<p class="tg-meta"><span>' + esc(m.route) + '</span> · <span>' + esc((I.channel || {})[m.grid] || m.grid) + '</span> · <a href="https://www.jacar.archives.go.jp/das/meta/' + m.record + '">JACAR ' + m.record + '</a></p>';
      if (m.fiche) {
        var fi = '../assets/img/fiches/', cap = (L.scan || '').replace('{rec}', m.record).replace('{img}', m.fiche.n || m.fiche.img);
        h += '<div class="tg-fiche"><a class="tg-scan" href="' + fi + 'scan-' + m.fiche.img + '-full.webp" title="' + esc(cap) + '">' +
          '<img src="' + fi + 'scan-' + m.fiche.img + '.webp" loading="lazy" alt="' + esc(cap) + '"></a>' +
          '<div class="tg-side"><img class="tg-map" src="' + fi + 'map-' + m.id + '.png" loading="lazy" alt="' + esc((L.route || '') + ' : ' + m.route) + '">' +
          '<p class="tg-keys"><span class="tg-label">' + esc(L.keys || '') + '</span> ' + m.fiche.keys.map(function (k) { return '<span lang="zh-Hant">' + esc(k) + '</span>'; }).join(' · ') + '</p>' +
          '<p class="tg-credit">' + esc(cap) + '</p></div></div>';
      }
      var groups = m.letters.match(/.{1,10}/g) || [];
      h += '<p class="tg-label">' + esc(X ? X.read : L.read) + '</p><p class="cipher mono">' + groups.join(' ') + '</p>';
      h += '<div class="tokens">';
      m.codes.forEach(function (code, i) {
        var st = m.status[i], cls = st === 'ok' ? '' : st === 'douteux' ? ' doubt' : st === 'illisible' ? ' illegible' : ' confirmed';
        var title = st.indexOf('confirmé') === 0 ? L.conf[st.split(':')[1]] : (L.status[st] || '');
        var fx = (m.fixed || {})[String(i)];
        if (fx && X) { cls += ' fixed'; title = X.fixed[fx.how].replace('{from}', fx.from || '') + (title ? ' · ' + title : ''); }
        if ((m.verified || []).indexOf(i) >= 0) title += ' · ' + (VERIF[document.documentElement.lang] || VERIF.fr);
        h += '<span class="token' + cls + '" title="' + esc(title) + '"><span class="u">' + m.letters.substr(4 * i, 2) + '·' + m.letters.substr(4 * i + 2, 2) +
          '</span><span class="c">' + code + '</span><span class="h" lang="zh-Hant">' + esc(m.chars[i]) + '</span></span>';
      });
      h += '</div>';
      // version lisible proposée
      var R = m.readable;
      if (R) {
        var byI = {}; R.props.forEach(function (p) { byI[p.i] = p; });
        var reasonTxt = function (p) { return p.reasons.map(function (r) { return L.reason[r] || r; }).join(', '); };
        var editTxt = function (p) {
          return p.letters + ' → ' + p.to_letters + ' (' + p.edits.map(function (e) {
            return e.from + '→' + e.to + ' : ' + kindLabel(e.kind) + (e.kind.indexOf('morse') >= 0 ? ' ' + morse(e.morse[0]) + '→' + morse(e.morse[1]) : '');
          }).join(' ; ') + ')';
        };
        h += '<p class="tg-label">' + esc(L.readable) + '</p><p class="readable" lang="zh-Hant">';
        R.toks.forEach(function (t) {
          var ch = t[0], i = t[1], prop = t[2];
          if (prop) { var p = byI[i]; h += '<span class="prop prop-' + p.level + '" title="' + esc(p.orig + ' → ' + p.ch + ' · ' + editTxt(p) + ' · ' + reasonTxt(p) + (p.image && L.image ? ' · ' + L.image[p.image] : '')) + '">' + esc(ch) + '</span>'; }
          else if (i !== null && (m.status[i] === 'douteux' || m.status[i] === 'illisible')) h += '<span class="unres" title="' + esc(L.unres) + '">' + esc(ch) + '</span>';
          else h += esc(ch);
        });
        h += '</p>';
        var fmt = function (x) { return (x > 0 ? '+' : '') + x.toLocaleString(root.lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
        h += '<p class="tg-score">' + esc(L.score).replace('{a}', fmt(R.score[0])).replace('{b}', fmt(R.score[1])) + '</p>';
        if (R.props.length) {
          h += '<details class="tg-props"><summary>' + esc(L.props.replace('{n}', R.props.length)) + '</summary><ul>';
          R.props.forEach(function (p) {
            h += '<li><b>' + (p.i + 1) + '.</b> <span lang="zh-Hant">' + esc(p.orig) + '</span> → <span lang="zh-Hant" class="prop prop-' + p.level + '">' + esc(p.ch) + '</span> <code>' + p.code + '</code> — <span class="lvl">' + esc(L.level[p.level]) + '</span> · ' +
              '<span class="mono">' + esc(editTxt(p)) + '</span> · ' + esc(reasonTxt(p)) +
              (p.image && L.image ? ' · <span class="img-state img-' + p.image + '">' + esc(L.image[p.image]) + '</span>' : '') + '</li>';
          });
          h += '</ul></details>';
        }
      }
      if (I.tr[m.id]) h += '<p class="meta"><strong>' + esc(I.label) + '</strong> ' + esc(I.tr[m.id]) + '</p>';
      var items = '';
      Object.keys(m.expected || {}).forEach(function (i) {
        var e = m.expected[i], idx = +i;
        items += '<li class="expected"><b>' + (idx + 1) + '.</b> <span lang="zh-Hant">' + esc(m.chars[idx]) + '</span> <code>' + m.codes[idx] + '</code> → <span lang="zh-Hant">' + esc(e.ch) + '</span> <code>' + e.code + '</code> — ' + esc(L.why[e.why]) + ' ';
        items += e.paths.length ? e.paths.map(function (p) {
          return '<span class="path">' + p.from + ' → ' + p.to + ' (' + esc(kindLabel(p.kind)) + (p.kind.indexOf('morse') >= 0 ? ' : ' + morse(p.morse[0]) + ' → ' + morse(p.morse[1]) : '') + ')</span>';
        }).join(' ') : esc(L.unreachable);
        items += '</li>';
      });
      m.status.forEach(function (st, idx) {
        if (st !== 'douteux' && st !== 'illisible') return;
        if (m.expected && m.expected[String(idx)]) return;
        var al = (m.alts || {})[String(idx)] || [];
        items += '<li><b>' + (idx + 1) + '.</b> <span class="mono">' + m.letters.substr(4 * idx, 4) + '</span> <span lang="zh-Hant">' + esc(m.chars[idx]) + '</span> <code>' + m.codes[idx] + '</code> → ';
        items += al.length ? al.map(function (a) {
          return '<span class="alt"><span lang="zh-Hant">' + esc(a.ch) + '</span> <code>' + a.code + '</code> <small>' + a.from + '→' + a.to + ', ' + esc(kindLabel(a.kind)) +
            (a.kind.indexOf('morse') >= 0 ? ' ' + morse(a.morse[0]) + '→' + morse(a.morse[1]) : '') + ', ' + (a.d > 0 ? '+' : '') + a.d.toLocaleString(root.lang, { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '</small></span>';
        }).join(' · ') : '<em>' + esc(L.none) + '</em>';
        items += '</li>';
      });
      if (items) h += '<details class="tg-doubts"' + (m.expected && Object.keys(m.expected).length ? ' open' : '') + '><summary>' + esc(L.doubts) + '</summary><ul>' + items + '</ul></details>';
      return h + '</section>';
    }
    C.messages.forEach(function (m) { h += tg(m, I, null); });
    h += '<section class="tg" id="t1917"><h2>' + esc(L.y1917) + '</h2>';
    var tpl1917 = document.getElementById('y1917-tpl');   // lecture, confusions et pistes (texte de la page, 5 langues)
    if (tpl1917) h += tpl1917.innerHTML;
    else C.undeciphered.forEach(function (u) {
      h += '<h3>' + u.id + ' <small>' + esc(u.route) + '</small></h3>';
      h += u.reading ? '<p class="tg-label">' + esc(L.read) + '</p><p class="cipher mono">' + esc(u.reading) + '</p><p>' + esc(L.notDecoded) + '</p>' : '<p>' + esc(L.pending) + '</p>';
    });
    h += '</section>';
    // télégrammes à condensateur de 1916 (corpus-c1916.js) : même gabarit, groupés par clé puis par date
    var K = window.WENMI_C1916, KX = window.WENMI_C1916_I18N;
    var KI = KX ? (KX[root.lang] || KX.fr) : null;
    if (K && KI) {
      var st = K.stats;
      h += '<section class="tg tg-group" id="c1916"><h2>' + esc(KI.title) + '</h2>' + KI.intro +
        '<p class="corpus-stats">' + esc(KI.stats.replace('{tels}', st.tels).replace('{codes}', st.codes).replace('{chg}', st.corr + st.sugg + st.new + (st.dx || 0)).replace('{dx}', st.dx || 0).replace('{corr}', st.corr)
          .replace('{sugg}', st.sugg).replace('{new}', st['new']).replace('{added}', st.added).replace('{conf}', st['confirmé']).replace('{douteux}', st.douteux)) + '</p><nav class="corpus-toc">';
      K.order.forEach(function (g) {
        h += '<div><strong>' + esc(KI.channel[g] || g) + '</strong> ';
        K.messages.filter(function (m) { return m.grid === g; }).forEach(function (m) { h += '<a href="#t' + m.id + '">' + m.label + '</a> '; });
        h += '</div>';
      });
      h += '</nav></section>';
      K.messages.forEach(function (m) { h += tg(m, KI, KI); });
    }
    // nouveaux déchiffrements de mai–juin 1916 (corpus-n1916.js)
    var N = window.WENMI_N1916, NX = window.WENMI_N1916_I18N;
    var NI = NX ? (NX[root.lang] || NX.fr) : null;
    if (N && NI) {
      var ns = N.stats;
      h += '<section class="tg tg-group" id="n1916"><h2>' + esc(NI.title) + '</h2>' + NI.intro +
        '<p class="corpus-stats">' + esc(NI.stats.replace('{tels}', ns.tels).replace('{codes}', ns.codes).replace('{conf}', ns['confirmé']).replace('{douteux}', ns.douteux)) +
        '</p><nav class="corpus-toc">';
      // sommaire groupé par canal (m.toc, sinon la clé) ; les intitulés viennent de NI.toc ou NI.channel
      var groups = NI.toc || NI.channel;
      Object.keys(groups).forEach(function (g) {
        var ms = N.messages.filter(function (m) { return (m.toc || m.grid) === g; });
        if (!ms.length) return;
        h += '<div><strong>' + esc(groups[g]) + '</strong> ';
        ms.forEach(function (m) { h += '<a href="#t' + m.id + '">' + m.label + '</a> '; });
        h += '</div>';
      });
      h += '</nav></section>';
      N.messages.forEach(function (m) { h += tg(m, NI, NI); });
    }
    box.innerHTML = h;
  }
  document.querySelectorAll('#corpus').forEach(mountCorpus);

  // ---------- sommaire flottant (pages longues) : colonne fixe sur grand écran, bouton + panneau sinon ----------
  function mountFloatingToc() {
    var main = document.querySelector('main');
    if (!main || document.querySelector('.hero')) return;           // pas sur l'accueil
    var heads = Array.prototype.slice.call(main.querySelectorAll('h2'));
    if (heads.length < 3) return;
    var T = { fr: 'Sommaire', en: 'Contents', 'zh-Hans': '目录', 'zh-Hant': '目錄', ja: '目次' };
    var title = T[root.lang] || T.fr, n = 0;
    var items = heads.map(function (h) {
      var target = h.id ? h : (h.parentElement && h.parentElement.id && h.parentElement.tagName === 'SECTION' ? h.parentElement : h);
      if (!target.id) target.id = 'sec-' + (++n);
      var label = h.cloneNode(true); label.querySelectorAll('small, sup, .star').forEach(function (x) { x.remove(); });
      var txt = label.textContent.replace(/\s+/g, ' ').trim(), small = h.querySelector('small');
      return { id: target.id, el: h, txt: txt, sub: small ? small.textContent.trim() : '' };
    });
    var wrap = document.createElement('div'); wrap.className = 'ftoc';
    var h = '<button class="ftoc-btn" type="button" aria-expanded="false" aria-controls="ftoc-panel">☰ ' + esc(title) + '</button>' +
      '<nav class="ftoc-panel" id="ftoc-panel" aria-label="' + esc(title) + '"><p class="ftoc-title">' + esc(title) + '</p><ul>';
    items.forEach(function (it) {
      h += '<li><a href="#' + it.id + '" data-id="' + it.id + '">' + esc(it.txt) + (it.sub ? ' <small>' + esc(it.sub) + '</small>' : '') + '</a></li>';
    });
    wrap.innerHTML = h + '</ul></nav>';
    document.body.appendChild(wrap);
    var btn = wrap.querySelector('.ftoc-btn'), links = wrap.querySelectorAll('a');
    function setOpen(o) { wrap.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    btn.addEventListener('click', function () { setOpen(!wrap.classList.contains('open')); });
    wrap.addEventListener('click', function (ev) { if (ev.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') setOpen(false); });
    document.addEventListener('click', function (ev) { if (!wrap.contains(ev.target)) setOpen(false); });
    // section en cours
    var current = null;
    function spy() {
      var y = window.scrollY + 120, cur = items[0];
      items.forEach(function (it) { if (it.el.getBoundingClientRect().top + window.scrollY <= y) cur = it; });
      if (cur !== current) {
        current = cur;
        links.forEach(function (a) { a.classList.toggle('on', a.dataset.id === cur.id); });
        var on = wrap.querySelector('a.on'), panel = wrap.querySelector('.ftoc-panel');
        if (on && panel.scrollHeight > panel.clientHeight) {
          var top = on.offsetTop - panel.clientHeight / 2;
          panel.scrollTop = Math.max(0, top);
        }
      }
    }
    window.addEventListener('scroll', spy, { passive: true }); spy();
    // les figures larges passent sous la colonne : on l'efface le temps qu'elles sont à l'écran
    var wide = Array.prototype.slice.call(document.querySelectorAll('figure.wide'));
    function hideOverWide() {
      var over = wide.some(function (f) { var r = f.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; });
      document.body.classList.toggle('ftoc-hide', over);
    }
    if (wide.length) { window.addEventListener('scroll', hideOverWide, { passive: true }); window.addEventListener('resize', hideOverWide); hideOverWide(); }
    // la colonne s'arrête au-dessus du pied de page : elle raccourcit, puis s'efface s'il ne reste plus de place
    var foot = document.querySelector('.site-footer'), panel = wrap.querySelector('.ftoc-panel');
    document.body.classList.add('has-ftoc');
    function fitFoot() {
      panel.style.maxHeight = '';
      var column = window.getComputedStyle(btn).display === 'none';
      if (!foot || !column) { document.body.classList.remove('ftoc-foot'); return; }
      var room = foot.getBoundingClientRect().top - panel.getBoundingClientRect().top - 24;
      if (room < panel.getBoundingClientRect().height) panel.style.maxHeight = Math.max(room, 0) + 'px';
      document.body.classList.toggle('ftoc-foot', room < 72);
    }
    window.addEventListener('scroll', fitFoot, { passive: true }); window.addEventListener('resize', fitFoot); fitFoot();
  }
  mountFloatingToc();
})();
