---
name: findings
description: Security Hub の Finding を取得し、稼働しているアプリケーションの単位でまとめた記録を作る。対応が要るものを、アプリケーションごと・項目ごとに並べ、所有者がアクションを決めやすくする。AWS は読み取るだけ。
disable-model-invocation: true
---

# findings

Security Hub の Finding を、アプリケーションの単位でまとめる。目的は、所有者が「どのアプリケーションの、何から手を付けるか」を決められること。エージェントは読み取りと記録だけを行い、環境を変えない。

まとめるのはスクリプト（このスキルのディレクトリの `group_findings.py`）。同じ入力からは同じ記録ができる。

## 前提

| もの | 場所 | 誰が書くか |
| --- | --- | --- |
| アプリケーションの単位の定義 | `ops/apps.json` | 所有者。エージェントは案を示す |
| 取得したままの Finding | `ops/raw/findings/<日付>.json`（コミットしない） | エージェント |
| まとめた記録 | `ops/findings/<日付>.md` | スクリプト |

`ops/apps.json` の書式と当て方は、この plugin の `lib/apps.py` の冒頭の説明にある。リソースは、定義の並び順で最初に当たったアプリケーションに入る。範囲の広い当て方（アカウント）は後ろに置く。

## 手順

1. **誰として読むかを確かめる。** `aws sts get-caller-identity` の結果（アカウントとロール）を所有者に示す。読み取り専用の認証情報でなければ、止めて所有者に伝える。
2. **どこから取るかを決める。** Security Hub の集約リージョンがあればそこから、なければ対象のリージョンごとに取る。分からなければ所有者に尋ねる。
3. **取得する。** 対応が要るものに絞って取る。出力は `ops/raw/findings/<日付>.json` に置く。先に、`ops/raw/` がコミットから外れていることを `git check-ignore ops/raw/findings/x` で確かめる（`ops/raw/.gitignore` が外す）。外れていなければ、止めて所有者に伝える。
   ```bash
   mkdir -p ops/raw/findings ops/findings
   ```
   ```bash
   aws securityhub get-findings --region <region> --output json \
     --filters '{"RecordState":[{"Value":"ACTIVE","Comparison":"EQUALS"}],"WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"},{"Value":"NOTIFIED","Comparison":"EQUALS"}]}' \
     > ops/raw/findings/<日付>.json
   ```
4. **まとめる。**
   ```bash
   python3 <このスキルのディレクトリ>/group_findings.py --apps ops/apps.json --date <日付> \
     --out ops/findings/<日付>.md ops/raw/findings/<日付>.json
   ```
   `ops/apps.json` が無ければ、`{"apps": []}` で一度走らせる。すべてが「どのアプリケーションにも当たらない」に入る。
5. **定義の案を示す。** 「どのアプリケーションにも当たらない」のリソースを、タグ・名前・種類で見て、どのアプリケーションに入りそうか、新しい単位が要りそうかを所有者に示す。`ops/apps.json` を直すのは、所有者が決めてから。直したら 4 をやり直す。
6. **読み解きを足す。** 記録そのものは書き換えない。会話で、次を短く伝える。
   - アプリケーションごとに、先に手を付けるとよい項目（重大度が高く、リソースが多いもの）と、その理由。
   - 同じ原因で直りそうな項目のまとまり（同じ設定、同じ雛形から作られたリソース）。
   - 事実として確かめたことと、推測を分ける。推測には、確かめ方を書く。
7. **アクションにする。** 所有者が対応すると決めた項目を、`observation` か `proposal` の Issue にする案を示す。Issue を作るのは、所有者が確かめてから。

## 守ること

- AWS を変える操作をしない。抑制、ワークフローの状態の更新、設定の修正は、所有者への提案として書く。
- Finding の中身（アカウント ID、リソースの名前）を、このリポジトリの外に送らない。Issue や PR に書く前に、そのリポジトリが非公開であることを確かめる。
- 件数や重大度を、記録と違う数で伝えない。数は記録から引く。
