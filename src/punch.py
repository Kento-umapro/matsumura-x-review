# -*- coding: utf-8 -*-
"""BOSSの口ぐせ（！！ ／ ？？ ／ w）を本文に入れる。松村さん本人の書き癖。
   1本あたり最大2箇所まで。機械的に見えないよう、本文と通し番号で当たりを散らす。"""
import re

ASSERT = re.compile(r'(や|やん|ねん|あかん|しろ|せえ|せえへん|探せ|捨てろ|やめろ|いらん|動かせ|'
                    r'なれ|持て|出せ|やれ|行け|見ろ|上げろ|勝つ|強い|決まる|終わる|残る|変わる|'
                    r'一緒や|同じや|それだけや|そこや)」$')
ASK    = re.compile(r'(か|やろ|んか|へんか|あるか|できるか|してるか|言えるか|思うか|なるか)」$')
LIGHT  = ('たぶん', 'せやろな', 'せやな', 'ふーん', '余計', '早いな', '知ってる', '読め',
          'もう行ってる', '俺が一番', 'せやねん', '好きにせえ', '無理や', '切れへん',
          '聞くんじゃ', 'そういうとこ', '言うたな', '乗るやろ', '歌詞やな', '厳しい',
          '痛いところ', '身も蓋もない', 'まあな', '合うてる', 'ちゃう', 'ないな', 'そらそうや',
          '覚えてへん', 'もろた', 'つくな', 'ええ話', '知っとる', 'あるわ', '数えてへん')
HAHA   = ('でした', 'ました', 'ですね', 'ですか', 'んですが', 'ないです', 'すみません')

def punch(body, seed):
    lines = body.split('\n')
    boss = [i for i, l in enumerate(lines) if l.startswith('BOSS「')]
    hide = [i for i, l in enumerate(lines) if l.startswith('秘書「')]
    used = 0

    # 1) BOSSの問いかけ → ？？
    cand = [i for i in boss if ASK.search(lines[i])]
    if cand:
        i = cand[(seed // 2) % len(cand)]
        if (seed + i) % 4 != 3:
            lines[i] = lines[i][:-1] + '？？」'
            used += 1

    # 2) BOSSの断言 → ！！（最後のBOSS行を優先）
    if used < 2:
        for i in reversed(boss):
            if i in cand and used: continue
            if ASSERT.search(lines[i]) and (seed + i) % 5 != 4:
                lines[i] = lines[i][:-1] + '！！」'
                used += 1
                break

    # 3) 軽口 → w
    if seed % 3 != 2:
        hit = None
        for i in boss:
            if any(k in lines[i] for k in LIGHT) and len(lines[i]) <= 26:
                hit = i; break
        if hit is None and hide and seed % 6 in (0, 4):
            last = hide[-1]
            if len(lines[last]) <= 20 and any(lines[last].endswith(h + '」') for h in HAHA):
                hit = last
        if hit is not None and '！！' not in lines[hit] and '？？' not in lines[hit]:
            lines[hit] = lines[hit][:-1] + 'w」'
    return '\n'.join(lines)
