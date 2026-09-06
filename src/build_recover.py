# -*- coding: utf-8 -*-
"""判定データの復元ページ（docs/recover.html）"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
d = json.load(open(os.path.join(HERE, "posts.json")))
CUR = "matsumura-x-stock-v2"
# 過去に使ったキー（新しい順）
OLD = ["matsumura-x-stock-v1", "matsumura-x-review-v4", "matsumura-x-review-v3",
       "matsumura-x-review-v2", "matsumura-x-review-v1"]
N = len(d["posts"])

HTML = """<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>判定の復元</title>
<style>
:root{--bg:#F1F2F3;--sf:#fff;--tx:#15191D;--t2:#5C6771;--t3:#8B959E;--ln:#D9DDE1;
 --ok:#1E6B4F;--ng:#B8401F;--st:#2E3A44;
 --f:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
 --m:ui-monospace,SFMono-Regular,Menlo,monospace;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111519;--sf:#191F25;--tx:#E7EBEE;--t2:#9AA6B0;--t3:#6E7A85;--ln:#2B343C;--ok:#5FBF95;--ng:#E8734C;--st:#B7C3CD;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font-family:var(--f);font-size:16px;line-height:1.75}
.w{max-width:760px;margin:0 auto;padding:28px 16px 80px}
h1{font-size:24px;margin:0 0 8px}
.lead{color:var(--t2);font-size:14px;margin:0 0 24px}
.card{background:var(--sf);border:1px solid var(--ln);border-radius:2px;padding:16px 18px;margin:0 0 14px}
.card h2{font-size:16px;margin:0 0 6px}
.k{font-family:var(--m);font-size:12px;color:var(--t3)}
.cnt{font-family:var(--m);font-size:14px;margin:8px 0}
.cnt b{font-size:20px}
.ok{color:var(--ok)} .ng{color:var(--ng)}
button{font:inherit;font-size:14px;font-weight:600;min-height:46px;padding:0 16px;border-radius:3px;
 cursor:pointer;border:1px solid var(--ln);background:var(--sf);color:var(--tx);margin:6px 6px 0 0}
button.pri{background:var(--st);border-color:var(--st);color:var(--bg)}
.note{font-size:12.5px;color:var(--t2);line-height:1.8;margin:10px 0 0}
.warn{background:#FBEDE8;border-left:3px solid var(--ng);padding:12px 14px;font-size:13px;line-height:1.8;margin:12px 0 0}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .warn{background:#2A1B15}}
#log{font-family:var(--m);font-size:12.5px;white-space:pre-wrap;background:var(--sf);
 border:1px solid var(--ln);border-radius:2px;padding:14px;margin-top:16px;max-height:44vh;overflow:auto}
a{color:var(--tx)}
textarea{font:inherit;font-size:14px;font-family:var(--m);width:100%;height:150px;background:var(--sf);
 color:var(--tx);border:1px solid var(--ln);border-radius:3px;padding:10px}
</style></head><body>
<div class="w">
<h1>判定の復元</h1>
<p class="lead">このページは、ブラウザの中に残っている過去の判定データを探して、今のページに戻すためのものです。
何も消しません。見つかったものを表示して、選んだものだけ復元します。</p>

<div id="found"></div>

<div class="card">
  <h2>バックアップを取り出す</h2>
  <p class="note">今入っているデータを全部テキストにします。念のため、復元の前後どちらでもコピーして残しておいてください。</p>
  <button class="pri" id="dump">全データをテキストにする</button>
  <textarea id="out" placeholder="ここに出ます"></textarea>
</div>

<div id="log"></div>
<p class="note" style="margin-top:20px"><a href="./">← 添削ページに戻る</a></p>
</div>

<script>
var CUR = '%CUR%', OLD = %OLD%, N = %N%;
var log = document.getElementById('log');
function say(s){ log.textContent += s + '\\n'; }

function read(k){ try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch(e){ return null; } }
function stat(o){
  var ok=0,ng=0,memo=0,posted=0,max=0,min=1e9;
  for (var k in o){
    var m = /^post(\\d+)$/.exec(k); if(!m) continue;
    var n = +m[1]; if(n>max)max=n; if(n<min)min=n;
    var v = o[k]||{};
    if (v.posted) posted++;
    if (v.v==='ok') ok++; else if (v.v==='ng') ng++;
    if (v.m && v.m.trim()) memo++;
  }
  return {ok:ok,ng:ng,memo:memo,posted:posted,max:max,min:min===1e9?0:min};
}

/* 98本時代 → 302本時代の番号変換。朝#1-49はそのまま、夕#50-98は+102 */
function mapOld98(n){ return n <= 49 ? n : n + 102; }

var box = document.getElementById('found');
var all = [CUR].concat(OLD);
var hits = [];
say('■ 保存されているキーを全部調べます');
for (var i=0;i<localStorage.length;i++){
  var key = localStorage.key(i);
  say('  ' + key + '  (' + (localStorage.getItem(key)||'').length + '文字)');
}
say('');

all.forEach(function(k){
  var o = read(k); if(!o) return;
  var s = stat(o);
  if (s.ok+s.ng+s.memo+s.posted === 0) return;
  hits.push({key:k,obj:o,st:s});
});

if (!hits.length){
  box.innerHTML = '<div class="card"><h2>判定データが見つかりませんでした</h2>' +
    '<p class="note">このブラウザには、過去の判定が残っていないようです。' +
    '別のブラウザやシークレットウィンドウで開いていた場合は、そちらで開き直すと出てくることがあります。' +
    'ページ内の「全データをテキストにする」で中身を確認できます。</p></div>';
} else {
  hits.forEach(function(h, idx){
    var isCur = h.key === CUR;
    var needMap = h.st.max <= 98 && h.st.max > 0;
    var el = document.createElement('div');
    el.className = 'card';
    el.innerHTML =
      '<h2>' + (isCur ? '今のページのデータ' : '古い保存データ') + '</h2>' +
      '<div class="k">' + h.key + '</div>' +
      '<div class="cnt"><b class="ok">' + h.st.ok + '</b> OK ／ <b class="ng">' + h.st.ng + '</b> NG ／ ' +
        h.st.memo + ' コメント ／ ' + h.st.posted + ' 投稿済み</div>' +
      '<div class="k">番号の範囲 #' + h.st.min + ' 〜 #' + h.st.max + '</div>' +
      (needMap ? '<div class="warn">これは<b>98本だった頃</b>の番号に見えます。' +
        '今は302本なので、夕方の投稿は番号がずれています。<br>' +
        '「番号を変換して復元」を押すと、朝はそのまま、夕方は +102 して正しい位置に戻します。</div>' : '') +
      (isCur ? '' :
        '<button class="pri" data-i="' + idx + '" data-map="' + (needMap?1:0) + '">' +
          (needMap ? '番号を変換して復元' : 'このデータを復元') + '</button>' +
        (needMap ? '<button data-i="' + idx + '" data-map="0">変換せずそのまま復元</button>' : ''));
    box.appendChild(el);
  });
}

box.addEventListener('click', function(e){
  var b = e.target.closest('button'); if(!b) return;
  var h = hits[+b.dataset.i], doMap = b.dataset.map === '1';
  var cur = read(CUR) || {};
  var moved = 0, skipped = 0;
  for (var k in h.obj){
    var m = /^post(\\d+)$/.exec(k);
    if (!m){ if(!(k in cur)) cur[k] = h.obj[k]; continue; }
    var n = +m[1];
    var t = doMap ? mapOld98(n) : n;
    if (t < 1 || t > N){ skipped++; continue; }
    var tk = 'post' + t;
    var src = h.obj[k] || {};
    if (!src.v && !(src.m||'').trim() && !src.posted) continue;
    var dst = cur[tk] || {};
    if (dst.v || (dst.m||'').trim()){ skipped++; continue; }   // 今の判定は上書きしない
    cur[tk] = src; moved++;
  }
  localStorage.setItem(CUR, JSON.stringify(cur));
  say('■ 復元しました: ' + h.key + (doMap ? '（番号を変換）' : '') );
  say('  戻した数 ' + moved + ' ／ 飛ばした数 ' + skipped);
  say('  添削ページを開き直すと反映されます。');
  b.textContent = '復元しました';
  b.disabled = true;
});

document.getElementById('dump').addEventListener('click', function(){
  var o = {};
  for (var i=0;i<localStorage.length;i++){ var k = localStorage.key(i); o[k] = localStorage.getItem(k); }
  document.getElementById('out').value = JSON.stringify(o, null, 1);
});
</script>
</body></html>
"""
HTML = HTML.replace("%CUR%", CUR).replace("%OLD%", json.dumps(OLD)).replace("%N%", str(N))
open(os.path.join(DOCS, "recover.html"), "w").write(HTML)
print("recover.html", len(HTML), "bytes ／ 対象キー", [CUR] + OLD)
