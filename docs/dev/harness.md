# 開発ハーネスの一覧

`make check` と CI が行う検査の全リスト。**検査を足すときは必ずここに 1 行足す。** 長いあいだ何も捕まえず費用だけがある検査は、削除の候補にする。

CI の `required (make check)` は `make check` をそのまま呼ぶ。必須チェックはこの 1 つ。手元で走らせられない検査（ネットワークや比べる先が要るもの）は、理由と一緒にここに載せ、CI の同じジョブで走らせる。

## 文書

| 検査 | 防ぐもの | 個別実行 | 場所 |
| --- | --- | --- | --- |
| リンク・パス・索引・競合マーカー | 存在しないものを指す文書、索引にない文書、マージで残った `<<<<<<<` | `make docs-check` | `make check` |
| `AGENTS.md` / `CLAUDE.md` の行数予算（150） | 読まれない指示書 | `make docs-check` | `make check` |

## 配る部品

| 検査 | 防ぐもの | 個別実行 | 場所 |
| --- | --- | --- | --- |
| shellcheck（`scripts/*.sh` と、plugin が持つスクリプト、導入先にコピーするスクリプト） | 失敗を見ない `cd`、引用符のない展開など、シェルの典型的な誤り。導入先に誤りを配ること | `make shell-lint` | `make check` |
| 導入のテスト（`scripts/test-adopt.sh`。空のリポジトリに `core` を導入し、別のリポジトリに `core`、`aws-ops`、`aws-iac` を続けて導入する。インフラのコードの検査を、偽の道具に対して走らせる） | 導入した直後に `make check` が通らないこと。2 度目の実行で何かが変わること。手で変えたファイルや導入先が所有するファイルを上書きすること。`--dry-run` が書き込むこと。ある plugin の導入が、ほかの plugin の導入の記録を消すこと。`ops/raw/` がコミットに入ること。インフラのコードの検査が、段を飛ばすこと、道具の失敗や不在を見逃すこと、フックが止める操作を呼ぶこと | `make test-adopt` | `make check` |
| `aws-ops` のフックのテスト（`scripts/test-guard-aws.py`。コマンドの表に対して、通す・止める・尋ねるを確かめる。Python 3 が要る） | 読み取りでない AWS の操作を通すこと。秘密情報やデータを読む操作を通すこと。読み取りを止めて調査を妨げること | `make test-guard-aws` | `make check` |
| `aws-iac` のフックのテスト（`scripts/test-guard-iac.py`。コマンドの表に対して、通す・止める・尋ねるを確かめる。Python 3 が要る） | 反映（apply、deploy、destroy）と、state を触る操作を通すこと。計画（plan、diff、synth）を止めて作業を妨げること | `make test-guard-iac` | `make check` |
| Finding のまとめのテスト（`scripts/test-findings.sh`。架空の例の Finding から作った記録が、コミットした記録と一致する。Python 3 が要る） | まとめのスクリプトの振る舞いが、気づかずに変わること。対応が要らない Finding を数えること。誤った定義を受け付けること | `make test-findings` | `make check` |
| 構成の棚卸しのテスト（`scripts/test-inventory.sh`。架空の例の取得結果から作った記録が、コミットした記録と一致する。取得のスクリプトを、偽の `aws` に対して走らせる。Python 3 が要る） | 記録のスクリプトの振る舞いが、気づかずに変わること。取得のスクリプトが、読み取りでない操作を呼ぶこと。1 つの失敗で取得が止まること。取れなかった部分を記録が黙って欠くこと。種類を問わない発見が取れなかったのに、記録がそれを言わないこと | `make test-inventory` | `make check` |
| plan の要約のテスト（`scripts/test-plan.sh`。架空の例の plan から作った要約が、コミットした要約と一致する。Python 3 が要る） | 要約のスクリプトの振る舞いが、気づかずに変わること。属性の値（秘密情報を含みうる）が要約に載ること。データソースを変更として数えること | `make test-plan` | `make check` |
| マーケットプレイスと plugin の定義（`claude` の CLI が要るので `make check` には入れない） | 定義の書き間違いで、導入先が plugin を読み込めないこと | `make plugin-validate` | 手元（plugin の定義を変えたとき） |

## 変更の大きさ

| 検査 | 防ぐもの | 個別実行 | 場所 |
| --- | --- | --- | --- |
| PR の大きさの予算（足した行と消した行の和。バイナリと `scripts/pr-size-excludes.txt` のパスは数えない。600 行を超えると警告、1000 行を超えると失敗。比べる先が要るので `make check` には入れない） | 読みきれない大きさの PR | `make pr-size`（比べる先は `PR_BASE`、既定は `origin/main`） | CI（PR のときだけ） |

## 手順（機械化されていない）

| 手順 | 目的 | いつ |
| --- | --- | --- |
| `docs-sync` 自己点検 | 差分で言及が変わる文書の修正 | PR 前（`docs/dev/docs-hygiene.md`） |
| 自己レビュー | 人間のレビュー負荷の低減 | PR 前 |
