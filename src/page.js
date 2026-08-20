(function () {
  var KEY = 'matsumura-x-stock-v1';
  var N = __N__, QN = __QN__;
  var S = {};
  try { S = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { S = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
  function st(k) { return S[k] || {}; }

  var cards = {};   // key -> {el, slot, no}
  document.querySelectorAll('.post').forEach(function (el) {
    cards[el.dataset.k] = { el: el, slot: el.dataset.slot, no: +el.dataset.no };
  });

  /* ---- 判定 ---- */
  function paintCard(k) {
    var c = cards[k]; if (!c) return;
    var s = st(k), el = c.el;
    el.classList.toggle('j-ok', s.v === 'ok' && !s.posted);
    el.classList.toggle('j-ng', s.v === 'ng');
    el.classList.toggle('j-done', !!s.posted);
    el.querySelectorAll('.jb').forEach(function (b) {
      if (b.dataset.v) b.classList.toggle('on', b.dataset.v === s.v);
    });
    var done = el.querySelector('.jb.done');
    if (done) {
      done.hidden = !(s.v === 'ok');
      done.classList.toggle('on', !!s.posted);
      done.textContent = s.posted ? '投稿済み' : '投稿した';
    }
    var memo = el.querySelector('.memo');
    memo.classList.toggle('show', s.v === 'ng' || !!s.m);
    var rank = el.querySelector('.rank');
    if (rank) {
      if (s.v === 'ok' && !s.posted) {
        var q = queue(c.slot), i = q.indexOf(k);
        rank.textContent = c.slot + 'ストック ' + (i + 1) + '番目';
        rank.hidden = false;
      } else if (s.posted) { rank.textContent = '投稿済み'; rank.hidden = false; }
      else rank.hidden = true;
    }
  }
  function queue(slot) {
    return Object.keys(cards)
      .filter(function (k) { var s = st(k); return s.v === 'ok' && !s.posted && cards[k].slot === slot; })
      .sort(function (a, b) { return (st(a).t || 0) - (st(b).t || 0); });
  }

  document.querySelectorAll('.judge').forEach(function (j) {
    var k = j.dataset.k, memo = j.querySelector('.memo');
    j.querySelectorAll('.jb').forEach(function (b) {
      b.addEventListener('click', function () {
        var s = S[k] = S[k] || {};
        if (b.dataset.v) {
          s.v = (s.v === b.dataset.v) ? null : b.dataset.v;
          if (s.v === 'ok' && !s.t) s.t = Date.now();
          if (s.v !== 'ok') s.posted = 0;
        } else { s.posted = s.posted ? 0 : 1; }
        save(); repaint();
      });
    });
    memo.value = st(k).m || '';
    memo.addEventListener('input', function () { (S[k] = S[k] || {}).m = memo.value; save(); });
  });

  var ncards = document.querySelectorAll('.ncard');
  function paintNames() {
    ncards.forEach(function (c) { c.classList.toggle('chosen', S._name === c.dataset.name); });
  }
  ncards.forEach(function (c) {
    c.querySelector('.pick').addEventListener('click', function () {
      S._name = (S._name === c.dataset.name) ? null : c.dataset.name;
      save(); paintNames();
    });
  });
  paintNames();

  document.querySelectorAll('.ans').forEach(function (t) {
    t.value = S[t.dataset.k] || '';
    t.addEventListener('input', function () { S[t.dataset.k] = t.value; save(); });
  });

  /* ---- 集計とタブ ---- */
  var view = 'todo';
  function counts() {
    var c = { todo: 0, ok朝: 0, ok夕: 0, ng: 0, done: 0 };
    Object.keys(cards).forEach(function (k) {
      var s = st(k);
      if (s.posted) c.done++;
      else if (s.v === 'ok') c['ok' + cards[k].slot]++;
      else if (s.v === 'ng') c.ng++;
      else c.todo++;
    });
    return c;
  }
  function inView(k) {
    var s = st(k), slot = cards[k].slot;
    if (view === 'todo') return !s.v && !s.posted;
    if (view === 'ok朝') return s.v === 'ok' && !s.posted && slot === '朝';
    if (view === 'ok夕') return s.v === 'ok' && !s.posted && slot === '夕';
    if (view === 'ng') return s.v === 'ng';
    if (view === 'done') return !!s.posted;
    return true;
  }
  function repaint() {
    var c = counts();
    ['todo', 'ok朝', 'ok夕', 'ng', 'done'].forEach(function (v) {
      var el = document.getElementById('c-' + v); if (el) el.textContent = c[v];
    });
    var days = Math.min(c['ok朝'], c['ok夕']);
    ['stockDays','stockDays2'].forEach(function (id) {
      var el = document.getElementById(id); if (el) el.textContent = days;
    });
    document.getElementById('stockNote').textContent =
      days === 0 ? '朝と夕が揃うと1日分になります' : (days < 3 ? 'そろそろ補充どきです' : '余裕があります');
    var pgf = document.getElementById('pgf');
    pgf.style.width = ((N - c.todo) / N * 100) + '%';
    document.getElementById('pgt').textContent = '未確認 ' + c.todo + ' 件 / 全' + N + '本';

    var qA = queue('朝'), qP = queue('夕');
    var list = document.querySelector('.posts');
    var order = (view === 'ok朝') ? qA : (view === 'ok夕') ? qP : null;
    Object.keys(cards).forEach(function (k) { cards[k].el.hidden = !inView(k); paintCard(k); });
    if (order) order.forEach(function (k) { list.appendChild(cards[k].el); });
    else Object.keys(cards).sort(function (a, b) { return cards[a].no - cards[b].no; })
      .forEach(function (k) { list.appendChild(cards[k].el); });
    document.getElementById('empty').hidden = order ? order.length > 0 : (c[view] || 0) > 0;
  }
  document.querySelectorAll('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('on'); });
      t.classList.add('on'); view = t.dataset.v; repaint();
      window.scrollTo({ top: document.getElementById('posts').offsetTop - 60, behavior: 'smooth' });
    });
  });
  repaint();

  /* ---- 書き出し ---- */
  var dlg = document.getElementById('dlg'), out = document.getElementById('outText');
  function num(k) { return '#' + ('0' + cards[k].no).slice(-2); }
  function build() {
    var c = counts(), L = ['【勝手に！松村僚広報部 添削結果】', '', '■ 表示名', (S._name || '（未選択）'), ''];
    L.push('■ ストック状況');
    L.push('朝 ' + c['ok朝'] + '本 / 夕 ' + c['ok夕'] + '本 → ' + Math.min(c['ok朝'], c['ok夕']) + '日分');
    L.push('未確認 ' + c.todo + '本 / ゴミ箱 ' + c.ng + '本 / 投稿済み ' + c.done + '本', '');
    ['朝', '夕'].push;
    ['朝', '夕'].forEach(function (slot) {
      var q = queue(slot);
      L.push('■ 投稿キュー（' + slot + '）' + q.length + '本');
      L.push(q.length ? q.map(function (k, i) { return (i + 1) + '. ' + num(k); }).join('  ') : 'なし');
      L.push('');
    });
    var ng = Object.keys(cards).filter(function (k) { return st(k).v === 'ng'; })
      .sort(function (a, b) { return cards[a].no - cards[b].no; });
    var sers = {};
    Object.keys(cards).forEach(function (k) {
      var s = st(k); if (s.v !== 'ok' || s.posted) return;
      var se = cards[k].el.dataset.series; sers[se] = (sers[se] || 0) + 1;
    });
    var sk = Object.keys(sers);
    if (sk.length) { L.push('■ ストックの内訳'); L.push(sk.map(function (x) { return x + ' ' + sers[x] + '本'; }).join(' / ')); L.push(''); }
    L.push('■ ゴミ箱 ' + ng.length + '本');
    L.push(ng.length ? ng.map(function (k) {
      return num(k) + (st(k).m ? ' → ' + st(k).m : ' → （理由なし）');
    }).join('\n') : 'なし');
    L.push('');
    var todo = Object.keys(cards).filter(function (k) { return !st(k).v && !st(k).posted; })
      .sort(function (a, b) { return cards[a].no - cards[b].no; });
    L.push('■ 未確認 ' + todo.length + '本');
    L.push(todo.length ? todo.map(num).join(' ') : 'なし');
    L.push('');
    L.push('■ 確認の記録');
    var qs = document.querySelectorAll('.cq');
    for (var i = 1; i <= QN; i++) {
      var lb = qs[i - 1] ? qs[i - 1].querySelector('b').textContent : ('質問' + i);
      L.push(i + '. ' + lb + ': ' + (S['q' + i] || '（未回答）'));
    }
    return L.join('\n');
  }
  document.getElementById('exportBtn').addEventListener('click', function () {
    out.value = build();
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    out.scrollTop = 0;
  });
  document.getElementById('closeBtn').addEventListener('click', function () {
    if (dlg.close) dlg.close(); else dlg.removeAttribute('open');
  });
  document.getElementById('copyBtn').addEventListener('click', function () {
    var btn = this;
    function ok() { btn.textContent = 'コピーしました'; setTimeout(function () { btn.textContent = 'コピーする'; }, 1800); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(out.value).then(ok, function () {
        out.removeAttribute('readonly'); out.select(); document.execCommand('copy');
        out.setAttribute('readonly', ''); ok();
      });
    } else {
      out.removeAttribute('readonly'); out.select(); document.execCommand('copy');
      out.setAttribute('readonly', ''); ok();
    }
  });
})();
