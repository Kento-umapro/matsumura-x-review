(function () {
  var KEY = 'matsumura-x-stock-v2';
  var N = __N__;
  var SLOTS = __SLOTS__, SEPCAP = __SEPCAP__, SEPTOTAL = __SEPTOTAL__;
  var S = {};
  try { S = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { S = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
  function st(k) { return S[k] || {}; }

  var cards = {};
  document.querySelectorAll('.post').forEach(function (el) {
    cards[el.dataset.k] = { el: el, slot: el.dataset.slot, no: +el.dataset.no };
  });

  /* 承認順に投稿枠を割り当てる。夕は当日17時、朝は翌日7時から */
  function queue(slot) {
    return Object.keys(cards)
      .filter(function (k) { var s = st(k); return s.v === 'ok' && !s.posted && cards[k].slot === slot; })
      .sort(function (a, b) { return (st(a).t || 0) - (st(b).t || 0); });
  }
  function plan() {
    var out = {};
    ['朝', '夕'].forEach(function (slot) {
      queue(slot).forEach(function (k, i) {
        var lab = SLOTS[slot][i];
        if (!lab) return;
        var day = (slot === '夕') ? i : i + 1;
        var hour = (slot === '夕') ? 17 : 7;
        out[k] = { label: lab, order: day * 100 + hour, sep: i < SEPCAP[slot] };
      });
    });
    return out;
  }

  function paintCard(k, pl) {
    var c = cards[k], s = st(k), el = c.el;
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
    el.querySelector('.memo').classList.toggle('show', s.v === 'ng' || !!s.m);
    var rank = el.querySelector('.rank');
    if (rank) {
      if (s.posted) { rank.textContent = '投稿済み'; rank.className = 'rank done'; rank.hidden = false; }
      else if (s.v === 'ok' && pl[k]) {
        rank.textContent = pl[k].label + ' に投稿' + (pl[k].sep ? '' : '（10月）');
        rank.className = 'rank' + (pl[k].sep ? '' : ' over');
        rank.hidden = false;
      } else if (s.v === 'ng') { rank.textContent = '投稿しません'; rank.className = 'rank ng'; rank.hidden = false; }
      else rank.hidden = true;
    }
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

  document.querySelectorAll('.ans').forEach(function (t) {
    t.value = S[t.dataset.k] || '';
    t.addEventListener('input', function () { S[t.dataset.k] = t.value; save(); });
  });

  var view = 'todo';
  function counts() {
    var c = { todo: 0, ok: 0, ng: 0, done: 0 };
    Object.keys(cards).forEach(function (k) {
      var s = st(k);
      if (s.posted) c.done++; else if (s.v === 'ok') c.ok++;
      else if (s.v === 'ng') c.ng++; else c.todo++;
    });
    return c;
  }
  function inView(k) {
    var s = st(k);
    if (view === 'todo') return !s.v && !s.posted;
    if (view === 'ok') return s.v === 'ok' && !s.posted;
    if (view === 'ng') return s.v === 'ng';
    if (view === 'done') return !!s.posted;
    return true;
  }
  function repaint() {
    var c = counts(), pl = plan();
    ['todo', 'ok', 'ng', 'done'].forEach(function (v) {
      var el = document.getElementById('c-' + v); if (el) el.textContent = c[v];
    });
    var sep = 0;
    Object.keys(pl).forEach(function (k) { if (pl[k].sep) sep++; });
    ['sepDone', 'sepDone2'].forEach(function (id) {
      var el = document.getElementById(id); if (el) el.textContent = sep;
    });
    var note = document.getElementById('stockNote');
    if (note) note.textContent = sep >= SEPTOTAL
      ? '9月末まで全部埋まりました'
      : 'あと ' + (SEPTOTAL - sep) + ' 本OKを出すと9月が埋まります';
    var pgf = document.getElementById('pgf');
    if (pgf) pgf.style.width = (sep / SEPTOTAL * 100) + '%';
    document.getElementById('pgt').textContent = '未確認 ' + c.todo + ' 件 / 全' + N + '本';

    var list = document.querySelector('.posts');
    Object.keys(cards).forEach(function (k) { cards[k].el.hidden = !inView(k); paintCard(k, pl); });
    var keys = Object.keys(cards);
    if (view === 'ok') {
      keys.filter(function (k) { return pl[k]; })
          .sort(function (a, b) { return pl[a].order - pl[b].order; })
          .forEach(function (k) { list.appendChild(cards[k].el); });
    } else {
      keys.sort(function (a, b) { return cards[a].no - cards[b].no; })
          .forEach(function (k) { list.appendChild(cards[k].el); });
    }
    document.getElementById('empty').hidden = (c[view] || 0) > 0;
  }
  document.querySelectorAll('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('on'); });
      t.classList.add('on'); view = t.dataset.v; repaint();
      window.scrollTo({ top: document.getElementById('posts').offsetTop - 60, behavior: 'smooth' });
    });
  });
  repaint();

  var dlg = document.getElementById('dlg'), out = document.getElementById('outText');
  function pad(n) { return n < 10 ? '00' + n : (n < 100 ? '0' + n : '' + n); }
  function num(k) { return '#' + pad(cards[k].no); }
  function build() {
    var c = counts(), pl = plan();
    var L = ['【一問一喝 添削結果】', '', '■ 表示名', '__NAME__', ''];
    var sep = 0; Object.keys(pl).forEach(function (k) { if (pl[k].sep) sep++; });
    L.push('■ 9月の埋まり具合');
    L.push(sep + ' / ' + SEPTOTAL + ' 本');
    L.push('未確認 ' + c.todo + ' / OK ' + c.ok + ' / NG ' + c.ng + ' / 投稿済み ' + c.done, '');
    var okq = Object.keys(pl).sort(function (a, b) { return pl[a].order - pl[b].order; });
    L.push('■ 投稿スケジュール ' + okq.length + '本');
    L.push(okq.length ? okq.map(function (k) { return pl[k].label + '　' + num(k); }).join('\n') : 'なし');
    L.push('');
    var ng = Object.keys(cards).filter(function (k) { return st(k).v === 'ng'; })
      .sort(function (a, b) { return cards[a].no - cards[b].no; });
    L.push('■ NG ' + ng.length + '本');
    L.push(ng.length ? ng.map(function (k) {
      return num(k) + (st(k).m ? ' → ' + st(k).m : ' → （理由なし）');
    }).join('\n') : 'なし');
    L.push('');
    var todo = Object.keys(cards).filter(function (k) { return !st(k).v && !st(k).posted; })
      .sort(function (a, b) { return cards[a].no - cards[b].no; });
    L.push('■ 未確認 ' + todo.length + '本');
    L.push(todo.length ? todo.map(num).join(' ') : 'なし');
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
