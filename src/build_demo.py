# -*- coding: utf-8 -*-
"""Xタイムライン風デモ（docs/demo.html）を posts.json から生成"""
import os, json, html
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
d = json.load(open(os.path.join(HERE, "posts.json")))
P, PIN, BIO, CHOSEN = d["posts"], d["pin"], d["bio"], d["chosen"]
e = lambda s: html.escape(s, quote=True)

# 朝7時台／夕17時台で日付を振り、時系列に並べ替え
mins = [0, 20, 40, 10, 30, 50, 5, 25, 45, 15, 35, 55]
start = date(2026, 8, 21)
cnt = {"朝": 0, "夕": 0}
for p in P:
    i = cnt[p["slot"]]; cnt[p["slot"]] += 1
    dt = start + timedelta(days=i)
    hh = 7 if p["slot"] == "朝" else 17
    mm = mins[i % len(mins)]
    p["_dt"] = (dt, hh, mm)
    p["_label"] = f"{dt.month}月{dt.day}日"
    p["_time"] = f"{hh}:{mm:02d}"
P = sorted(P, key=lambda p: p["_dt"])

NAME = CHOSEN.split("/")[0]          # 松村僚
TAG  = CHOSEN.split("/", 1)[1] if "/" in CHOSEN else ""

def tweet(p, pinned=False, body=None):
    b = e(body if body is not None else p["body"]).replace("\n", "<br>")
    pin_row = ('<div class="pinrow">'
               '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5C7 3.12 8.12 2 9.5 2h5C15.88 2 17 3.12 17 4.5v5.26L20.12 16H13v5l-1 2-1-2v-5H3.88L7 9.76V4.5z"/></svg>'
               '固定されたポスト</div>') if pinned else ''
    when = '' if pinned else f'<span class="dot">·</span><span class="tm">{p["_label"]}</span>'
    return f"""<article class="tw">
{pin_row}
<div class="row">
  <div class="av">松</div>
  <div class="col">
    <div class="hd"><span class="nm">{e(NAME)}/{e(TAG)}</span>
      <svg class="vf" viewBox="0 0 22 22" aria-label="認証済み"><path d="M20.4 11c0-1-.6-1.9-1.5-2.3.3-1 .1-2-.6-2.7-.7-.7-1.7-.9-2.7-.6C15.2 4.5 14.3 4 13.3 4h-.6c-1 0-1.9.5-2.3 1.4-1-.3-2-.1-2.7.6-.7.7-.9 1.7-.6 2.7-.9.4-1.5 1.3-1.5 2.3v.6c0 1 .6 1.9 1.5 2.3-.3 1-.1 2 .6 2.7.7.7 1.7.9 2.7.6.4.9 1.3 1.5 2.3 1.5h.6c1 0 1.9-.6 2.3-1.5 1 .3 2 .1 2.7-.6.7-.7.9-1.7.6-2.7.9-.4 1.5-1.3 1.5-2.3V11zm-9.6 3.9L7.6 11.7l1.3-1.3 1.9 1.9 4.3-4.3 1.3 1.3-5.6 5.6z"/></svg>
      <span class="hd2">@Umapro_ryo</span>{when}</div>
    <div class="bd">{b}</div>
    <div class="acts">
      <span><svg viewBox="0 0 24 24"><path d="M1.75 12a10.25 10.25 0 1 1 5.2 8.92l-4.2 1.06 1.08-4.13A10.2 10.2 0 0 1 1.75 12z"/></svg>12</span>
      <span><svg viewBox="0 0 24 24"><path d="M4.5 3.9h11.2l-2.3-2.3L14.8.2l4.7 4.7-4.7 4.7-1.4-1.4 2.3-2.3H4.5v3H2.5v-5zm15 16.2H8.3l2.3 2.3-1.4 1.4-4.7-4.7 4.7-4.7 1.4 1.4-2.3 2.3h11.2v-3h2v5z"/></svg>8</span>
      <span class="lk"><svg viewBox="0 0 24 24"><path d="M12 21.6l-1.4-1.3C5.4 15.6 2 12.5 2 8.8 2 6 4.2 3.8 7 3.8c1.6 0 3.1.7 4 1.9.9-1.2 2.4-1.9 4-1.9 2.8 0 5 2.2 5 5 0 3.7-3.4 6.8-8.6 11.5L12 21.6z"/></svg>96</span>
      <span><svg viewBox="0 0 24 24"><path d="M12 2.6l5.7 5.7-1.4 1.4L13 6.4V16h-2V6.4L7.7 9.7 6.3 8.3 12 2.6zM4 18v2h16v-2h2v4H2v-4h2z"/></svg></span>
    </div>
  </div>
</div>
</article>"""

tl = "\n".join(tweet(p) for p in P)
pin_tweet = tweet(P[0], pinned=True, body=PIN)

HTML = f"""<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#000000">
<title>一問一喝｜Xデモ</title>
<style>
:root {{
  --bg:#fff; --tx:#0f1419; --sub:#536471; --ln:#eff3f4; --bl:#1d9bf0;
  --hd:rgba(255,255,255,.85); --hov:#f7f9f9; --ban:#cfd9de;
  --f:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic",Meiryo,sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#000; --tx:#e7e9ea; --sub:#71767b; --ln:#2f3336; --bl:#1d9bf0;
  --hd:rgba(0,0,0,.75); --hov:#080808; --ban:#333639;
}} }}
:root[data-theme="dark"] {{
  --bg:#000; --tx:#e7e9ea; --sub:#71767b; --ln:#2f3336; --bl:#1d9bf0;
  --hd:rgba(0,0,0,.75); --hov:#080808; --ban:#333639;
}}
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
body{{margin:0;background:var(--bg);color:var(--tx);font-family:var(--f);
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}}
.note{{background:#ffe8b3;color:#4a3200;font-size:12.5px;padding:9px 16px;text-align:center;
  line-height:1.7;border-bottom:1px solid #e5cf95}}
.note a{{color:#4a3200;font-weight:700}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) .note{{background:#3b2f12;color:#f3dfae;border-color:#5a4a1e}}
 :root:not([data-theme="light"]) .note a{{color:#f3dfae}}}}
.wrap{{max-width:600px;margin:0 auto;border-left:1px solid var(--ln);border-right:1px solid var(--ln);min-height:100vh}}
.top{{position:sticky;top:0;z-index:9;background:var(--hd);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--ln);padding:9px 16px;display:flex;align-items:center;gap:18px}}
.top .bk{{font-size:20px;color:var(--tx);line-height:1}}
.top b{{font-size:17px;display:block}}
.top s{{display:block;font-size:12.5px;color:var(--sub);text-decoration:none}}
.banner{{height:132px;background:linear-gradient(120deg,var(--ban),#8a949c)}}
.pf{{padding:0 16px 12px;position:relative}}
.avbig{{width:88px;height:88px;border-radius:50%;background:#1a1d1f;color:#fff;border:4px solid var(--bg);
  margin-top:-46px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:700}}
.btns{{position:absolute;right:16px;top:12px;display:flex;gap:8px}}
.btn{{border:1px solid var(--ln);border-radius:999px;padding:7px 16px;font-weight:700;font-size:14px}}
.btn.pri{{background:var(--tx);color:var(--bg);border-color:var(--tx)}}
h1{{font-size:20px;margin:10px 0 0;display:flex;align-items:center;gap:4px;flex-wrap:wrap}}
.at{{color:var(--sub);font-size:15px;margin:0 0 12px}}
.bio{{white-space:pre-wrap;margin:0 0 12px;font-size:15px}}
.meta{{color:var(--sub);font-size:14px;margin-bottom:10px}}
.fol{{display:flex;gap:18px;font-size:14px}}
.fol b{{color:var(--tx)}} .fol span{{color:var(--sub)}}
.tabs{{display:flex;border-bottom:1px solid var(--ln);margin-top:14px}}
.tabs div{{flex:1;text-align:center;padding:14px 0;color:var(--sub);font-weight:600;font-size:14.5px}}
.tabs div.on{{color:var(--tx);position:relative}}
.tabs div.on::after{{content:"";position:absolute;left:50%;transform:translateX(-50%);bottom:0;
  width:56px;height:4px;background:var(--bl);border-radius:2px}}
.tw{{border-bottom:1px solid var(--ln);padding:12px 16px}}
.tw:hover{{background:var(--hov)}}
.pinrow{{display:flex;align-items:center;gap:8px;color:var(--sub);font-size:13px;font-weight:700;
  margin:0 0 4px;padding-left:44px}}
.pinrow svg{{width:16px;height:16px;fill:var(--sub)}}
.row{{display:flex;gap:12px}}
.av{{width:40px;height:40px;border-radius:50%;background:#1a1d1f;color:#fff;flex:0 0 40px;
  display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700}}
.col{{flex:1;min-width:0}}
.hd{{display:flex;align-items:center;gap:4px;flex-wrap:wrap;font-size:15px;line-height:1.3}}
.nm{{font-weight:700}}
.vf{{width:17px;height:17px;fill:var(--bl);flex:0 0 17px}}
.hd2,.tm{{color:var(--sub);font-weight:400}}
.dot{{color:var(--sub)}}
.bd{{margin-top:3px;white-space:pre-wrap;word-break:break-word;font-size:15.5px;line-height:1.62}}
.acts{{display:flex;justify-content:space-between;max-width:340px;margin-top:12px;color:var(--sub);font-size:13px}}
.acts span{{display:flex;align-items:center;gap:6px}}
.acts svg{{width:18px;height:18px;fill:var(--sub)}}
.acts .lk svg{{fill:#f91880}} .acts .lk{{color:#f91880}}
.end{{text-align:center;color:var(--sub);font-size:13px;padding:28px 16px 60px}}
</style>
</head><body>
<div class="note">
これは <b>Xでどう見えるかのデモ</b>です。実際のアカウントではありません。<br>
アイコンとヘッダー画像は仮です。数字も仮の表示です。<br>
<a href="./">← 添削ページに戻る</a>
</div>
<div class="wrap">
  <div class="top"><span class="bk">←</span><div><b>{e(NAME)}/{e(TAG)}</b><s>{len(P)}件のポスト</s></div></div>
  <div class="banner"></div>
  <div class="pf">
    <div class="btns"><span class="btn">･･･</span><span class="btn pri">フォロー</span></div>
    <div class="avbig">松</div>
    <h1>{e(NAME)}/{e(TAG)}
      <svg class="vf" viewBox="0 0 22 22"><path d="M20.4 11c0-1-.6-1.9-1.5-2.3.3-1 .1-2-.6-2.7-.7-.7-1.7-.9-2.7-.6C15.2 4.5 14.3 4 13.3 4h-.6c-1 0-1.9.5-2.3 1.4-1-.3-2-.1-2.7.6-.7.7-.9 1.7-.6 2.7-.9.4-1.5 1.3-1.5 2.3v.6c0 1 .6 1.9 1.5 2.3-.3 1-.1 2 .6 2.7.7.7 1.7.9 2.7.6.4.9 1.3 1.5 2.3 1.5h.6c1 0 1.9-.6 2.3-1.5 1 .3 2 .1 2.7-.6.7-.7.9-1.7.6-2.7.9-.4 1.5-1.3 1.5-2.3V11zm-9.6 3.9L7.6 11.7l1.3-1.3 1.9 1.9 4.3-4.3 1.3 1.3-5.6 5.6z"/></svg>
    </h1>
    <p class="at">@Umapro_ryo</p>
    <p class="bio">{e(BIO)}</p>
    <p class="meta">東京 中央区 月島　･　2015年3月からXを利用しています</p>
    <div class="fol"><div><b>189</b> <span>フォロー中</span></div><div><b>293</b> <span>フォロワー</span></div></div>
  </div>
  <div class="tabs"><div class="on">ポスト</div><div>返信</div><div>ハイライト</div><div>メディア</div></div>
  {pin_tweet}
  {tl}
  <p class="end">ここまで {len(P)}件（{len(P)//2}日分）</p>
</div>
</body></html>
"""
open(os.path.join(DOCS, "demo.html"), "w").write(HTML)
print("demo.html", len(HTML), "bytes ／", len(P), "件")
