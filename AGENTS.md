# AGENTS.md — 開発ガイド

ai-dev-methodologies で作業する人間と AI コーディングエージェントの共通の正典。ツール固有の補足は `CLAUDE.md` に置き、規則の本体はここだけに書く。

## 1. このリポジトリは何か

複数のリポジトリに AI 活用の枠組みを選んで導入するためのメタフレームワーク。Claude Code の plugin と、導入先にコピーするファイルと雛形を持つ。詳細は `docs/concept.md`、段階と現在地は `docs/roadmap.md`。

このリポジトリ自身にも `core` を導入してあり、導入先と同じ規約（`docs/contract.md`）で作業する。

## 2. 作業の進め方

1. 着手の前に `docs/roadmap.md` で現在の段階を確かめる。段階を飛ばさない。
2. 作業は GitHub の Issue から始める。`ready` ラベルの Issue を、`docs/dev/workflow.md` の「次の Issue の選び方」の規則で 1 つ選ぶ。所有者が会話で直接指示した作業は、指示に従う。思いついたことや見つけた問題は `observation` の Issue にする。
3. 何をするかが決まっていないものは、`proposal` の Issue で選択肢と推奨を書き、所有者の判断を待つ。所有者にしか決められないこと（範囲、優先、公開してよいか）を、決めずに質問する。
4. 新しく発明する前に、出どころのリポジトリ（`docs/concept.md` の「出どころ」）に動いている実装がないかを見る。あれば、それを一般化する。
5. `make check` を通す。通らないものは完成ではない。
6. 設計判断をしたら `docs/architecture/adr/` に 1 枚足す。影響する文書を同じ PR で直す（`docs/dev/docs-hygiene.md`）。
7. 1 PR = 1 Issue。PR テンプレートを埋め、スコープ外にしたことを書く。

詳細は `docs/dev/workflow.md`。

## 3. ガードレール

- **会社や組織に固有の情報を置かない。** 規則、構成、アカウント ID、ホスト名、社内の文書への参照、実在の Finding を含めない。例が要るときは架空のものを作り、架空であることを書く（ADR-0004）。
- **秘密情報を扱わない。** `.env` を読まない・コミットしない。鍵をコードや文書に書かない。
- **配る部品に、特定の導入先を前提にした内容を書かない。** 導入先ごとに違うものは、導入先が所有する雛形に出す（ADR-0003）。
- **手順が導入先に前提を足すときは、同じ PR で `docs/contract.md` に足す**（ADR-0008）。
- **本番環境を変える操作を、エージェントに許す部品を作らない**（ADR-0005）。
- **スコープを広げない。** 今の段階に要らない部品は作らない。
- **検査を消す・スキップする・無効化して通す** ことで緑にしない。根本原因を直す。
- **`main` に直接 push しない。** `git push --force` をしない。
- **エージェントが開いた未マージの PR が 3 本になったら止まる。** 所有者にマージか方針の判断を仰ぐ。
- **自分でマージしてよいのは、`docs/dev/workflow.md` の「マージ」の条件を満たす PR だけ。** 迷ったら所有者の OK を待つ。
- **検査を足したら `docs/dev/harness.md` に 1 行足す。** `make check` にない検査を CI だけに置かない。

## 4. 配置とコマンド

| 場所 | 役割 | 守ること |
| --- | --- | --- |
| `.claude-plugin/marketplace.json` | マーケットプレイスの定義 | plugin を足したらここに載せる。`version` は書かない（導入先がコミットを追う） |
| `plugins/core/skills/`、`plugins/core/agents/` | plugin で配る手順 | 導入先の規約（`docs/contract.md`）にあるパスとコマンドだけを前提にする |
| `plugins/core/skills/adopt/adopt.sh` | 導入先にファイルを置くスクリプト。ほかの plugin の `skills/adopt/adopt.sh` は、これへのシンボリックリンク | 振る舞いを変えたら `scripts/test-adopt.sh` に確かめを足す |
| `plugins/core/skills/adopt/assets/managed/` | 導入先にそのままコピーするファイル | 導入先ごとに変えたくなるものを置かない |
| `plugins/core/skills/adopt/assets/owned/` | 導入先が所有するファイルの雛形（末尾が `.tmpl`） | 導入先で埋める箇所は「（導入先で書く: …）」と書く |
| `plugins/aws-ops/hooks/` | 運用・管理のリポジトリ向けのフック。AWS の操作を読み取りに限る（ADR-0009） | 通す操作を足したら `scripts/test-guard-aws.py` に行を足す。迷う操作は通さない |
| `plugins/aws-ops/skills/adopt/assets/` | `aws-ops` の導入で置くファイル（`ops/` の置き場所） | `core` の `assets/` と同じ |
| `plugins/aws-ops/skills/findings/` | Finding を、アプリケーションの単位でまとめる手順とスクリプト | 同じ入力から同じ記録を作る（時刻やネットワークを読まない）。出力を変えたら、架空の例の記録を作り直す |
| `plugins/aws-ops/skills/inventory/` | 構成を取得するスクリプトと、棚卸しの記録を作るスクリプト | 取得は読み取りの操作だけにする（テストがフックの判定で確かめる）。同じ取得結果から同じ記録を作る |
| `plugins/aws-ops/lib/apps.py` | アプリケーションの単位の定義の読み方と、リソースの当て方。Finding と棚卸しが共に使う | 当て方を変えたら、架空の例の記録を両方作り直す |
| `examples/ops-example/` | 部品を確かめるための、架空の運用・管理のリポジトリ | 実在の環境の値を入れない |
| `docs/contract.md` | 導入先が守る規約 | 手順の前提と食い違わせない |
| `docs/architecture/adr/` | 決定の記録 | 索引に載せる |
| `scripts/`、`docs/dev/docs-hygiene.md`、`.github/ISSUE_TEMPLATE/` | このリポジトリ自身に導入した `core` のコピー | 直接は変えない。`assets/managed/` の方を変えて、導入し直す |

```bash
make check            # すべての検査（CI は同じターゲットを呼ぶ）
make docs-check       # 文書の検査だけ
make test-adopt       # 空のリポジトリに core を導入して確かめる
make test-guard-aws   # aws-ops のフックを、コマンドの表で確かめる
make test-findings    # Finding のまとめを、架空の例で確かめる
make test-inventory   # 構成の棚卸しを、架空の例と偽の aws で確かめる
make plugin-validate  # マーケットプレイスと plugin の定義（claude の CLI が要る）
bash plugins/core/skills/adopt/adopt.sh .   # このリポジトリに core を導入し直す
```

## 5. コミットと PR

- Conventional Commits（`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`, `ci:`）。
- コミットメッセージ・コード・コメントにモデル名や生成ツールの宣伝を書かない。
- 文書は日本語で書く。スクリプトのコメントと、検査やエラーの出力は英語で書く。スクリプトが作る記録（所有者が読む文書）は日本語で書く。

## 6. 文書の鮮度

- 文書は **現在の状態だけ** を書く。経緯は git log と ADR に、検討の過程は Issue に残す。
- 事実は 1 箇所にだけ書き、他は参照する。
- `make docs-check` が、リンク切れ・存在しないパス・索引漏れを落とす。

## 7. 迷ったら

1. 出どころのリポジトリで動いている形に近い方を選ぶ。
2. 小さい方を選ぶ。
3. それでも決まらなければ、着手せずに質問する。
