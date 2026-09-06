# -*- coding: utf-8 -*-
"""投稿スケジュール
   今日(2026-09-06)は昼12時台からスタート。翌日以降は 朝7時台／昼12時台／夕17時台 の1日3本。"""
from datetime import date, timedelta

TODAY = date(2026, 9, 6)
SEP_END = date(2026, 9, 30)
MIN = [0, 10, 20, 30, 40, 50]
HOUR = {"朝": 7, "昼": 12, "夕": 17}
ORDER = {"朝": 0, "昼": 1, "夕": 2}   # 同じ日の中での並び

def slots(n_days=200):
    """{'朝':[(date,h,m)...], '昼':[...], '夕':[...]}
       初日だけ朝が無い（もう過ぎているため）"""
    s = {"朝": [], "昼": [], "夕": []}
    for i in range(n_days):
        d0 = TODAY + timedelta(days=i)
        for k in ("朝", "昼", "夕"):
            if i == 0 and k == "朝":
                continue
            s[k].append((d0, HOUR[k], MIN[i % len(MIN)]))
    return s

def label(sl):
    d0, h, m = sl
    return f"{d0.month}/{d0.day} {h}:{m:02d}"

def sortkey(sl):
    d0, h, m = sl
    return (d0.toordinal(), h, m)

def in_sep(sl):
    return sl[0] <= SEP_END

def sep_capacity():
    s = slots()
    return {k: sum(1 for x in v if in_sep(x)) for k, v in s.items()}
