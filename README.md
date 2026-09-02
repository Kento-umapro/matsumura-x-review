# 一問一喝｜秘書とBOSS

うまプロ COO 松村僚（[@Umapro_ryo](https://x.com/Umapro_ryo)）のX運用ページ。

- 添削・ストック（表示名や確認事項のセクションは廃止。投稿の添削とストックのみ）: https://kento-umapro.github.io/matsumura-x-review/
- **Xデモ（実物に近い見え方）: https://kento-umapro.github.io/matsumura-x-review/demo.html**
- **参考にしたアカウント**: [@phads_kouhou](https://www.instagram.com/phads_kouhou)（勝手に！さのなおし広報部）/ [@sanonaoshi.everydaylife](https://www.instagram.com/sanonaoshi.everydaylife)
- **コンセプト**: 本人非公認。側近が「勝手に」広報部を名乗って発信する。人物観察コンテンツ
- **シリーズ**: 質問編35 / 証言編19 / 分析編20 / 目撃編12 / 図鑑編12
- **投稿設計**: 1日2本。朝7時台＝気合いが入る系、夕方17時台＝振り返り系。朝49／夕49＝49日分

## 運用フロー

1. 松村さんが各投稿に **OK / NG** をつける
2. **OK** → 投稿ストックへ。押した順に朝／夕それぞれのキューに並ぶ
3. **NG** → ゴミ箱へ。投稿されず、消えずに残る
4. 実際に投稿したら「投稿した」を押す → 投稿済みへ移動、キューが繰り上がる
5. 週1本ぐらいのペースで新しい文章を追加 → 添削 → OKストックを積み増す

朝と夕が1本ずつ揃って「1日分」。上部に残り日数が出る。

## 構成（すべてこのリポジトリ内で完結）

```
src/posts.json   本文・表示名案・bio・固定ポスト・確認事項の正本
src/build.py     → docs/index.html を生成
src/page.css
src/page.js
```

追加のしかた: `src/posts.json` の `posts` 配列の **末尾に追記**（並び順を変えると端末に保存済みの判定がズレる）→ `python3 src/build.py` → commit & push。

判定は端末のlocalStorage（キー `matsumura-x-stock-v1`）に保存。

一次資料: 松村メッセージ vol.1〜415（本文＋コメント欄）。松村さんの発言は全て実在の言葉。

## ビルド

```
python3 src/gen_posts.py   # 本文を生成（src/gen_posts.py が本文の正）
python3 src/build.py       # docs/index.html（添削・ストック）
python3 src/build_demo.py  # docs/demo.html（Xデモ）
```
