# 出どころとの差（chord-rambler）

`core` の導入のスクリプトを `hassaku63/chord-rambler`（コミット `ad3f1b0` の手元の写し）に当てて、手書きの版と比べた結果。`core` が何を持ち、何を持たないかの現在の状態。

## コピーするファイル

| ファイル | 手書きの版との差 | 振る舞い |
| --- | --- | --- |
| `scripts/check-docs.sh` | 読むファイルを `find` ではなく git から取る。`docs/README.md`、`AGENTS.md`、`CLAUDE.md` が無いときに落ちない | chord-rambler の文書で同じ結果（通る）。壊したリンク、存在しないパス、索引にない文書を落とす |
| `scripts/check-pr-size.sh` | 数えないパスを、スクリプトの中ではなく `scripts/pr-size-excludes.txt` から読む | 同じパスを書くと、同じ行数を数える |
| `docs/dev/docs-hygiene.md` | ADR の番号への参照を外した。誤検知のときに直す先を `core` にした | — |
| `.github/ISSUE_TEMPLATE/observation.md` | 「画面、ブラウザ」を「環境、対象のリソース」にした | — |
| `docs/architecture/adr/0000-template.md` | 同じ（導入先では索引の ADR の雛形が違えば残す） | — |
| `.github/ISSUE_TEMPLATE/proposal.md`、`config.yml` | 同じ | — |

chord-rambler に導入すると、中身の違う 5 つは手で変えたものとして残る（ADR-0007）。`core` の版に置き換えるかどうかは、所有者が決める。

## 導入先が所有するファイル

chord-rambler にはすべてあるので、導入のスクリプトは触らない。雛形は、chord-rambler の版から次を外したもの。

| 外したもの | 理由 |
| --- | --- |
| プロダクトの説明、配置の表、音楽理論のガードレール | 導入先ごとに違う。「（導入先で書く: …）」にした |
| テストの書き方の表 | 技術スタックごとに違う |
| プラクティスの索引と標準の索引への参照（`AGENTS.md`、`ready` の Issue の「当たる索引の項目」、PR テンプレートの欄） | 索引は `core` にまだない（`docs/roadmap.md` の段階 5）。`implementer` と `reviewer` は、`AGENTS.md` が索引を挙げていれば引く |
| 助言役のモデルの使い方 | 各自の設定で、リポジトリに置かないもの |

## `core` にないもの

chord-rambler にあって、技術スタックに依らないが、`core` に入れていないもの。

| もの | 入れていない理由 |
| --- | --- |
| プラクティスの索引、標準の索引、その検査と月次の報告 | 段階 5 で作る |
| `make doctor` と `.tool-versions`（手元と CI の道具の版のずれ） | 道具の一覧が導入先ごとに違う。型だけを配る価値があるかは決めていない |
| `shell-lint`、`actions-lint` | 導入先がシェルやワークフローを持つかによる。このリポジトリ自身は `shell-lint` を持つ |

## 規約に足りなかったもの

比べて見つけ、直したもの。

- 導入した直後の `CLAUDE.md` が `.claude/settings.local.json` を指し、`.gitignore` が無いと文書の検査が落ちた。`.gitignore` の雛形を足した。
- ADR の雛形を、chord-rambler のものと同じにした。
