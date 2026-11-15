# ロードマップ

進め方の原則: 動いているリポジトリから抽出する。実際の導入先（または架空の例）で確かめながら、小さく広げる。

## 段階

| 段階 | やること | 終わりの条件 | 状態 |
| --- | --- | --- | --- |
| 0. 土台 | 目的、決定、作業の規則を文書にする | 文書だけで文脈を取り戻せる | 済み |
| 1. 規約と core | 導入先が守る規約（`docs/contract.md`）を定義する。`core` の plugin（導入、Issue の流れ、実装とレビューのサブエージェント、文書の鮮度）とマーケットプレイスの定義を作る | 空のリポジトリに導入して、検査が通る状態になる（`make test-adopt`） | 済み |
| 2. 逆輸入で確かめる | `hassaku63/chord-rambler` に導入し直した場合を、手書きの版と比べる（`docs/comparison-chord-rambler.md`） | 差を説明できる。規約の不足を直してある | 済み |
| 3a. 運用・管理: 読み取りに限る | plugin `aws-ops` と、読み取りでない AWS の操作を止めるフック（ADR-0009） | コマンドの表で、通す・止める・尋ねるを確かめてある（`make test-guard-aws`） | 済み |
| 3b. 運用・管理: Finding のまとめ | Security Hub の Finding を、稼働しているアプリケーションの単位でまとめる手順とスクリプト。アプリケーションの単位の定義の書式。架空の例（`examples/ops-example/README.md`） | 架空の例で、アプリケーションごとのまとめができる（`make test-findings`） | 済み |
| 3c. 運用・管理: 導入 | `aws-ops` の導入の手順と、置き場所（`ops/`）の雛形。導入の記録を、複数の plugin で共有する | 空のリポジトリに `core` と `aws-ops` を続けて導入して、検査が通る（`make test-adopt`） | 済み |
| 3d. 運用・管理: 構成の棚卸し | ネットワークとコンピュートの構成を取得して記録する手順とスクリプト。架空の例（`examples/ops-example/README.md`） | 架空の例で、棚卸しの記録ができる（`make test-inventory`） | 済み |
| 4a. IaC: 計画までに限る | plugin `aws-iac` と、反映と state の操作を止めるフック（ADR-0010） | コマンドの表で、通す・止める・尋ねるを確かめてある（`make test-guard-iac`） | 済み |
| 4b. IaC: plan の要約 | `terraform plan` の結果を、置き換えと削除が目立つ形で要約する手順とスクリプト。架空の例（`examples/iac-example/README.md`） | 架空の例で、要約ができる（`make test-plan`） | 済み |
| 4c. IaC: 導入と検査 | `aws-iac` の導入の手順。Terraform と CDK の検査（書式、初期化と検証、lint、synth）を `make check` に入れるスクリプト。`cdk diff` の読み方 | 空のリポジトリに導入して、偽の道具に対して検査が段をすべて走らせる（`make test-adopt`） | 済み |
| 5a. 知識: 目録の形と、最初の束 | plugin `knowledge`。目録の項目の形と検査、使い方のスキル。一般、テスト、エージェントとの作業の進め方の束（`hassaku63/chord-rambler` から移す）（ADR-0011） | 目録の形の検査が通る（`make catalog-check`） | 済み |
| 5b. 知識: 対応表と導入 | 導入のときに、技術から束を選び、対応表の雛形を作る。対応表の形と、目録にない ID を落とす検査を配る | 空のリポジトリに導入して、対応表の検査が通り、よくある誤りを落とす（`make test-adopt`） | 済み |
| 5c. 知識: 依存の版の検査 | 目録の項目の対象の版と、導入先の依存（`package.json`、`go.mod`、`pyproject.toml`、`.terraform.lock.hcl`）の食い違いを落とす | 架空の例で、食い違いが落ちる | 未着手 |
| 5d. 知識: 鮮度の報告 | このリポジトリで、目録の見直しの期限、リンク切れ、ソースの変更を月次に報告するジョブ | 報告のスクリプトが、架空の期限切れを挙げる | 未着手 |
| 5e. 知識: 技術の束 | TypeScript、React、テストの道具、Go、Dockerfile（chord-rambler から移す）。Terraform、CDK、Python、Vue（新しく書く）。HCI（含めるかは所有者の判断待ち、#13） | 束ごとに、目録の形の検査が通る | 未着手 |
| 5f. 更新と、ほかの道具 | 手で変えたコピーの差分を示す手順の確かめ。Cursor と Codex 向けの出力 | 2 つ以上の導入先に更新を届けられる | 未着手 |

段階 3 と 4 は、会社のリポジトリを使えないので、架空の例を作って確かめる。実地での確認は所有者が行う。段階 3 と 4 の部品は、実際の AWS の環境、実際の Terraform と CDK、実際の Claude Code のセッションでは、まだ動かしていない。試し方は `docs/trial.md`。

## あとで検討すること

- 「あとで検討すること」を `observation` の Issue に移し、この節をなくす（`docs/dev/docs-hygiene.md` の規約）。
- `make doctor` と `.tool-versions`、`actions-lint` を `core` で配るか（`docs/comparison-chord-rambler.md` の「`core` にないもの」）。
- 役割の分担（指示書をファイルで渡す、実装に関わっていない目で確かめる、修正の回数に上限を置く）を、運用・管理の調査にどう当てるか。
- エージェントの失敗を、検査 → フックと権限 → `AGENTS.md` の順で固定先を選ぶ手順を、スキルにするか。
- 開発環境に限った反映（ADR-0005 の L3）を許す部品。環境の見分け方が要る。
