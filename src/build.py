# -*- coding: utf-8 -*-
"""勝手に！松村僚広報部 — 投稿ストックページを src/posts.json から生成"""
import os, json, html
from datetime import date, timedelta
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
d = json.load(open(os.path.join(HERE, "posts.json")))
P, PIN, BIO = d["posts"], d["pin"], d["bio"]
NAMES, CHECKS, CHOSEN = d["names"], d["checks"], d["chosen"]
e = lambda s: html.escape(s, quote=True)

import sys; sys.path.insert(0, HERE)
import schedule as SC
SLOTS = SC.slots()
SEPCAP = SC.sep_capacity()
SEPTOTAL = sum(SEPCAP.values())
cnt = {"朝": 0, "夕": 0}
for p in P:
    i = cnt[p["slot"]]; cnt[p["slot"]] += 1
    p["when"] = SC.label(SLOTS[p["slot"]][i])
    p["len"] = len(p["body"].replace("\n", ""))
SLOTS_JS = json.dumps({k: [SC.label(x) for x in v] for k, v in SLOTS.items()}, ensure_ascii=False)
SEPCAP_JS = json.dumps(SEPCAP, ensure_ascii=False)

SERC = Counter(p["series"] for p in P)
L = [p["len"] for p in P]

def card(p):
    i, slot, pn = p["no"], p["slot"], p["pillar"][0]
    t = [f'<span class="chip slot s{"A" if slot=="朝" else "P"}">{slot}{"7時台" if slot=="朝" else "17時台"}</span>',
         f'<span class="chip pillar p{pn}">{e(p["series"])}</span>',
         f'<span class="chip src">{e(p["src"])}</span>']
    if p.get("redo"): t.append(f'<span class="chip redo">再提案 #{p["redo"]:03d}</span>')
    if p.get("cta"): t.append('<span class="chip cta">CTA</span>')
    judge = (f'<div class="judge" data-k="post{i}">'
             '<button class="jb ok" data-v="ok" type="button">OK</button>'
             '<button class="jb ng" data-v="ng" type="button">NG</button>'
             '<button class="jb done" type="button" hidden>投稿した</button>'
             '<textarea class="memo" rows="2" placeholder="ここに直したいところを書くと、書き直して再提案します。空のままならボツ扱いです"></textarea></div>')
    return (f'<article class="post" data-k="post{i}" data-no="{i}" data-slot="{slot}" '
            f'data-series="{e(p["series"])}" id="p{i}">'
            f'<div class="phead"><span class="no">{i:02d}</span><div class="tags">{"".join(t)}</div>'
            f'<span class="stats"><b>{p["len"]}</b>字</span><span class="rank" hidden></span></div>'
            f'<div class="ptext">{e(p["body"])}</div>{judge}</article>')

cards = "\n".join(card(p) for p in P)
tabs = ('<button class="tab on" data-v="todo" type="button">未確認<i id="c-todo">0</i></button>'
        '<button class="tab tab-ok" data-v="ok" type="button">OK<i id="c-ok">0</i></button>'
        '<button class="tab tab-redo" data-v="redo" type="button">再提案<i id="c-redo">0</i></button>'
        '<button class="tab tab-ng" data-v="bin" type="button">ボツ<i id="c-bin">0</i></button>'
        '<button class="tab" data-v="done" type="button">投稿済み<i id="c-done">0</i></button>')
serchips = " ".join(f'<span class="serchip">{e(k)} {v}</span>' for k, v in SERC.most_common())

css = open(os.path.join(HERE, "page.css")).read()
js = (open(os.path.join(HERE, "page.js")).read()
      .replace("__SLOTS__", SLOTS_JS).replace("__SEPCAP__", SEPCAP_JS).replace("__SEPTOTAL__", str(SEPTOTAL)).replace("__N__", str(len(P))).replace("__QN__", str(len(CHECKS))).replace("__NAME__", CHOSEN))

HTML = f"""<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#15191D">
<title>一問一喝｜秘書とBOSS</title>
<style>{css}</style>
</head><body>

<div class="bar">
  <div class="pg"><span class="pgt" id="pgt">未確認 {len(P)} 件</span>
  <div class="pgb"><div class="pgf" id="pgf"></div></div></div>
  <div class="stock"><b id="sepDone">0</b><span>/{SEPTOTAL} 9月分</span></div>
  <button id="exportBtn" type="button">結果を送る</button>
</div>

<div class="wrap">
<header class="top">
  <p class="eyebrow">@Umapro_ryo ／ コンセプト第3案</p>
  <h1>秘書とBOSSの一問一喝</h1>
  <p class="lede">秘書が質問して、BOSSが一言で斬って、秘書が受ける。それだけの一問一答です。<br>
  トーンは<b>面白おかしく、時々まじめに</b>。<b>BOSSのセリフは、すべて松村メッセージ415本の中に実在する言葉です。</b>
  {serchips}<br><br>
  <b>投稿は今日 9/2 の夕方17時台から。翌日以降は朝7時台と夕方17時台の1日2本です。</b>
  9月末まで埋めるには <b>{SEPTOTAL}本</b>（朝{SEPCAP["朝"]}・夕{SEPCAP["夕"]}）必要で、ここには<b>{len(P)}本</b>あります。<br><br>
  <b>OKを押した順に、投稿する日時が自動で決まります。</b><br>
  <b>NGにコメントを書くと「再提案」に回ります。</b>そのコメントを見てこちらで書き直し、新しい案として戻します。
  コメントを書かなければ、そのままボツです。<br>
  判定はこの端末に自動保存されるので、途中でやめて後から続けられます。</p>
  <a class="demolink" href="./demo.html">
    <span class="dl1">Xでどう見えるかのデモを見る</span>
    <span class="dl2">プロフィールとタイムラインを実物に近い形で再現しています</span>
  </a>
  <div class="facts">
    <div class="fact"><b>{len(P)}</b><span>ストック</span></div>
    <div class="fact"><b>{len(P)//2}</b><span>日分</span></div>
    <div class="fact"><b>{SEPTOTAL}</b><span>9月に必要</span></div>
    <div class="fact"><b>{sum(L)//len(L)}</b><span>平均字数</span></div>
  </div>
</header>

<section id="posts">
  <h2>投稿の添削とストック</h2>
  <p class="sub"><b>OK</b>を押すと投稿が確定し、<b>押した順に投稿日時が割り振られます</b>。カードの右上に「9/5 7:30 に投稿」と出ます。<br>
  <b>NG</b>を押すと投稿されません。<b>そこにコメントを書けば「再提案」タブに入り、こちらで書き直して戻します。</b>
  コメントなしなら「ボツ」タブに残ります。どちらも消えません。<br>
  投稿は今日 9/2 の夕方から。翌日以降は朝7時台と夕方17時台の1日2本です。<br>
  実際に投稿したら「投稿した」を押すと、投稿済みに移ります。</p>
  <div class="stockbar">
    <div><b id="sepDone2">0</b> / {SEPTOTAL} 本</div>
    <span id="stockNote">あと {SEPTOTAL} 本OKを出すと9月が埋まります</span>
  </div>
  <div class="filters">{tabs}</div>
  <div class="posts">{cards}</div>
  <p class="empty" id="empty" hidden>ここは今、空です。</p>
</section>

<footer>
  {e(d.get('batch','第1弾 2026-08-17'))}／一次資料 <code>松村メッセージ vol.1〜415</code>（本文とコメント欄）<br>
  参考: <code>@phads_kouhou</code> / <code>@sanonaoshi.everydaylife</code><br>
  判定はこの端末に自動保存されます。NGにしたものも消えません。<br>
  このページは検索に出ません。URLを知っている人だけが見られます。
</footer>
</div>

<dialog id="dlg">
  <div class="dh">添削結果</div>
  <div class="db"><textarea id="outText" readonly></textarea></div>
  <div class="df">
    <button class="pri" id="copyBtn" type="button">コピーする</button>
    <button id="closeBtn" type="button">閉じる</button>
  </div>
</dialog>

<script>{js}</script>
</body></html>
"""
os.makedirs(DOCS, exist_ok=True)
open(os.path.join(DOCS, "index.html"), "w").write(HTML)
open(os.path.join(DOCS, ".nojekyll"), "w").write("")
print(f"written {len(HTML)} bytes ／ {len(P)}本 ／ 朝{cnt['朝']}/夕{cnt['夕']} ／ 平均{sum(L)//len(L)}字")
