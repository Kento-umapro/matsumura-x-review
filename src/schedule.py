# -*- coding: utf-8 -*-
"""投稿スケジュール

朝・昼・夕で別々に管理するのをやめた（2026-09-07 西村さん指示）。
枠は時系列に一本つなぎ、**OKを押した順に頭から詰めていく**だけ。
何本目が朝で何本目が夕か、を人が考える必要はない。
"""
from datetime import date, timedelta

BASE = date(2026, 9, 6)      # 分パターン（:00 :10 :20…）の起点。動かさない
START = date(2026, 9, 8)     # ここから先が未予約。9/7までは公開済み
SEP_END = date(2026, 9, 30)
MIN = [0, 10, 20, 30, 40, 50]
HOUR = {"朝": 7, "昼": 12, "夕": 17}
SLOT_ORDER = ["朝", "昼", "夕"]


def flat(n_days=200):
    """[(date, '朝'|'昼'|'夕', hour, minute), ...] を時系列で返す。"""
    out = []
    for i in range(n_days):
        d0 = START + timedelta(days=i)
        m = MIN[(d0 - BASE).days % len(MIN)]
        for k in SLOT_ORDER:
            out.append((d0, k, HOUR[k], m))
    return out


def label(sl):
    d0, k, h, m = sl
    return f"{d0.month}/{d0.day} {h}:{m:02d}"


def sortkey(sl):
    d0, k, h, m = sl
    return (d0.toordinal(), h, m)


def in_sep(sl):
    return sl[0] <= SEP_END


def sep_capacity():
    """9月末までに埋められる枠の数。"""
    return sum(1 for x in flat() if in_sep(x))
