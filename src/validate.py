# -*- coding: utf-8 -*-
"""本文の自動チェック。ビルド時に必ず通す。"""
import re, unicodedata
NG = {'絵文字': r'[\U0001F300-\U0001FAFF]', 'ハッシュタグ': '#', '三点リーダー': '…', 'やなく': 'やなく'}
OKLATIN = set('BOSSQCPLDERVisonaudUMACHAGIVEwxTNKF%0123456789./:')

def check(no, body):
    err = []
    for k, r in NG.items():
        if re.search(r, body): err.append(k)
    for ch in body:
        nm = unicodedata.name(ch, '')
        if 'CYRILLIC' in nm or 'GREEK' in nm or 'HANGUL' in nm:
            err.append(f'非日本語文字 {ch!r}')

    return err

def check_all(posts):
    bad = []
    for p in posts:
        e = check(p['no'], p['body'])
        if e: bad.append((p['no'], sorted(set(e))))
    return bad
