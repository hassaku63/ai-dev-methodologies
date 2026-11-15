# 文書の索引

`docs/` の文書はすべてここに載せる（`make docs-check` が漏れを落とす）。書き方の規則は [dev/docs-hygiene.md](dev/docs-hygiene.md)。

## 何を作るか

- [concept.md](concept.md) — 何を解決するか、導入先の種類、配り方、出どころ
- [roadmap.md](roadmap.md) — 段階、現在地、あとで検討すること
- [comparison-chord-rambler.md](comparison-chord-rambler.md) — 出どころ（chord-rambler）の手書きの版と `core` の差
- [trial.md](trial.md) — 実際のリポジトリで試す手順と、導入先のセッションに報告を作らせるプロンプト
- [contract.md](contract.md) — 導入先が守る規約（パス、コマンド、ラベル）と、配るファイルの一覧

## 設計

- [architecture/adr/README.md](architecture/adr/README.md) — 設計判断の記録（ADR）の索引

## 開発

- [dev/workflow.md](dev/workflow.md) — Issue と PR で回す開発ループ、完了の定義
- [dev/docs-hygiene.md](dev/docs-hygiene.md) — 文書の鮮度を保つ規則と自己点検
- [dev/harness.md](dev/harness.md) — `make check` と CI が行う検査の一覧
