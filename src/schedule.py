# -*- coding: utf-8 -*-
"""投稿スケジュール：今日(2026-09-02)の夕方から開始、翌日以降は朝7時台＋夕17時台の1日2本"""
from datetime import date, timedelta

TODAY = date(2026, 9, 2)
SEP_END = date(2026, 9, 30)
MIN = [0, 10, 20, 30, 40, 50]

def slots(n_days=200):
    """{'朝':[(date,h,m)...], '夕':[...]} 夕は今日から、朝は明日から"""
    s = {"朝": [], "夕": []}
    for i in range(n_days):
        d0 = TODAY + timedelta(days=i)
        if i >= 1:
            s["朝"].append((d0, 7, MIN[i % len(MIN)]))
        s["夕"].append((d0, 17, MIN[i % len(MIN)]))
    return s

def label(sl):
    d0, h, m = sl
    return f"{d0.month}/{d0.day} {h}:{m:02d}"

def in_sep(sl):
    return sl[0] <= SEP_END

def sep_capacity():
    s = slots()
    return {k: sum(1 for x in v if in_sep(x)) for k, v in s.items()}
