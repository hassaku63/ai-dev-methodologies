# 導入先が守る規約

`core` の plugin の手順（スキル、サブエージェント）は、導入先のリポジトリに決まったパスとコマンドがあることを前提にする。その前提の一覧。決定は ADR-0008。

導入はスキル `adopt` で行う（`plugins/core/skills/adopt/SKILL.md`）。

## パスとコマンド

| 規約 | 中身 | 前提にする手順 |
| --- | --- | --- |
| `AGENTS.md` | 規則の正典。150 行まで | すべて |
| `CLAUDE.md` | `@AGENTS.md` と、Claude Code に固有の補足 | すべて |
| `make check` | すべての検査を呼ぶ 1 つのコマンド。CI も同じものを呼ぶ | `implementer`、完了の定義 |
| `make docs-check` | 文書の検査（`scripts/check-docs.sh`） | `docs-sync` |
| `docs/README.md` | `docs/` の文書の索引。Markdown のリンクで載せる | `docs-check` |
| `docs/dev/workflow.md` | 作業の進め方。次の見出しを持つ: 「Issue の使い方」「`ready` の Issue に書くこと」「次の Issue の選び方と、止まる条件」「1 スライスの進め方」「マージ」 | `next-issue`、`grill`、`propose`、`implementer` |
| `docs/dev/harness.md` | 検査の一覧 | `propose`、検査を足すとき |
| `docs/dev/docs-hygiene.md` | 文書の書き方と、自己点検の手順 | `docs-sync`、`reviewer` |
| `docs/architecture/adr/` | ADR。索引は `README.md`、雛形は `0000-template.md` | `propose`、`implementer` |
| `.github/ISSUE_TEMPLATE/proposal.md` | 企画の Issue の形 | `propose` |
| `.agents/methodology.lock` | コピーしたファイルの、導入したときのハッシュ。1 行に、ハッシュ、パス、plugin の名前を持つ | `adopt`（どの plugin のものも） |

## GitHub

| 規約 | 中身 |
| --- | --- |
| ラベル | `observation`、`proposal`、`needs-decision`、`ready`、`priority:high` |
| エージェントのブランチ | 名前が `claude/` で始まる。未マージの PR の数え方に使う |
| 必須のチェック | CI の `required (make check)` の 1 つ |

## `aws-ops` を使う導入先

`core` の規約に加えて、次を前提にする。

| 規約 | 中身 | 前提にする手順 |
| --- | --- | --- |
| `ops/apps.json` | アプリケーションの単位の定義。導入先の所有者が書く。書式は `plugins/aws-ops/lib/apps.py` の冒頭 | `findings`、`inventory` |
| `ops/findings/<日付>.md` | Finding をまとめた記録。スクリプトが作る | `findings` |
| `ops/inventory.md` | 構成の棚卸しの記録。スクリプトが作り、毎回上書きする | `inventory` |
| `ops/inventory-notes.md` | 棚卸しの記録に詳しい表が無い種類のリソースについての補足。エージェントが書き、毎回書き直す | `inventory` |
| `ops/raw/` | AWS から取得したままの出力。中の `.gitignore` が、コミットから外す | `findings`、`inventory` |
| `ops/README.md` | 対象のアカウントとリージョン、読み取り専用の認証情報の用意の仕方。導入先の所有者が書く | `findings`、`inventory` |
| 読み取り専用の認証情報 | エージェントが使う AWS の認証情報は、読み取り専用にする（ADR-0009） | すべて |
| `python3` | フックとスクリプトが使う | すべて |
| `aws` の CLI | 取得に使う | `findings`、`inventory` |

記録にはアカウント ID やリソースの名前が入る。`aws-ops` を使う導入先は、非公開のリポジトリにする。

導入はスキル `adopt`（`plugins/aws-ops/skills/adopt/SKILL.md`）で行う。`core` を先に導入しておく。

## 配るファイル

種類の分け方は ADR-0003。ファイルの実体は、plugin ごとの `skills/adopt/assets/` にある（`plugins/core/skills/adopt/assets/`、`plugins/aws-ops/skills/adopt/assets/`）。導入のスクリプトは `core` のものを、ほかの plugin がシンボリックリンクで使う。

| 種類 | 場所 | 導入のとき | 新しい版に合わせるとき |
| --- | --- | --- | --- |
| コピーするもの | `assets/managed/` | そのまま置き、ハッシュをロックに記録する | 導入先で変えていなければ置き換える。変えてあれば残して報告する（ADR-0007） |
| 導入先が所有するもの | `assets/owned/`（名前の末尾が `.tmpl`） | 無いときだけ、雛形から作る。あれば触らない | 触らない |

雛形の「（導入先で書く: …）」は、導入の手順が、導入先を読んで埋める。

## 導入先に置かないもの

スキルとサブエージェントは plugin として届き、導入先にはコピーしない。導入先の `.claude/settings.json` が、マーケットプレイスと、有効にする plugin を指す。
