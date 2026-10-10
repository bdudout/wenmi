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

  // ---------- grille G0 ----------
  var ORDER = 'hgfdcbzyxwvtsrqpnmlk', VOW = 'aeiou';
  var G0 = {};
  for (var i = 0; i < ORDER.length; i++) {
    for (var j = 0; j < 5; j++) {
      G0[ORDER[i] + VOW[j]] = 10 * Math.floor(i / 2) + (i % 2 === 0 ? j : 9 - j);
    }
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function renderGrid(el) {
    var h = '<div class="table-wrap"><table class="grid-g0"><thead><tr><th></th>';
    for (var j = 0; j < 5; j++) h += '<th>' + VOW[j] + '</th>';
    h += '<th>dizaine</th></tr></thead><tbody>';
    for (var i = 0; i < ORDER.length; i++) {
      var c = ORDER[i];
      h += '<tr class="' + (i % 2 ? 'odd' : '') + '"><th>' + c + '</th>';
      for (var k = 0; k < 5; k++) h += '<td data-s="' + c + VOW[k] + '">' + pad(G0[c + VOW[k]]) + '</td>';
      h += '<td class="mono">' + Math.floor(i / 2) + '·</td></tr>';
    }
    el.innerHTML = h + '</tbody></table></div>';
  }
  function highlight(syl) {
    document.querySelectorAll('.grid-g0 td.hit').forEach(function (td) { td.classList.remove('hit'); });
    (syl || []).forEach(function (s) {
      document.querySelectorAll('.grid-g0 td[data-s="' + s + '"]').forEach(function (td) { td.classList.add('hit'); });
    });
  }
  document.querySelectorAll('[data-g0-grid]').forEach(renderGrid);

  // ---------- décodeur ----------
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function mountDecoder(box) {
    var all = window.WENMI_MESSAGES || [];
    if (!all.length) return;
    var I = (window.WENMI_I18N || {})[root.lang] || (window.WENMI_I18N || {}).fr;
    var byId = {}; all.forEach(function (m) { byId[m.id] = m; });
    var msgs = I.order.map(function (id) { return byId[id]; }).filter(Boolean);
    var sel = box.querySelector('select');
    msgs.forEach(function (m, idx) {
      var o = document.createElement('option');
      o.value = idx; o.textContent = m.id + ' — ' + (I.date[m.id] || '');
      sel.appendChild(o);
    });
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
      step = -1; highlight([]);
    }
    function focus(i) {
      var m = msgs[+sel.value];
      step = i;
      toks.querySelectorAll('.token').forEach(function (b) { b.classList.toggle('on', +b.dataset.i === i); });
      cipher.querySelectorAll('span').forEach(function (s) { s.classList.toggle('on', +s.dataset.i === i); });
      if (i >= 0) highlight([m.units[2 * i], m.units[2 * i + 1]]);
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
})();
