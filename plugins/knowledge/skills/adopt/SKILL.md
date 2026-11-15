---
name: adopt
description: ai-dev-methodologies の knowledge を、今のリポジトリに導入する。リポジトリの技術から目録の束を選び、プラクティスと業界標準の対応表（docs/knowledge/）を作り、その検査を make check に入れる。core を導入済みのリポジトリで使う。
disable-model-invocation: true
---

# adopt（knowledge）

リポジトリに、プラクティスと業界標準の対応表を置く。先に `core` を導入しておく（`AGENTS.md` と `make check` があること）。無ければ、`core` のスキル `adopt` を先に行う。

ファイルを置くのはスクリプト（このスキルのディレクトリの `adopt.sh`）、目録の項目を表の行にするのもスクリプト（`list_items.py`）。

## 手順

1. **調べる。** リポジトリの技術を把握する。言語、フレームワーク、テストの道具、コンテナ、IaC。依存のファイル（`package.json`、`go.mod`、`pyproject.toml`、`requirements*.txt`、`.terraform.lock.hcl`、`cdk.json`、`Dockerfile`）と、すでにある索引や規約の文書も読む。
2. **束を選ぶ。** 目録の束の一覧を出す。
   ```bash
   python3 <このスキルのディレクトリ>/list_items.py practices
   ```
   ```bash
   python3 <このスキルのディレクトリ>/list_items.py standards
   ```
   技術によらない束（一般、テスト、エージェントとの作業の進め方）は入れる。技術の束は、1 で見つけた技術に当たるものだけを選ぶ。選んだ束と理由を所有者に示す。リポジトリの技術に当たる束が目録に無ければ、それも示す（ai-dev-methodologies の `observation` の Issue にする案）。
3. **置かれるものを見せる。** `bash <このスキルのディレクトリ>/adopt.sh --dry-run <リポジトリの最上位>` を走らせ、結果を所有者に示す。
4. **置く。** 作業用のブランチで、`--dry-run` を外して走らせる。
5. **対応表を埋める。** 選んだ束の行を出し、置かれた `practices.md` と `standards.md`（`./docs/knowledge/` の下）の「使う項目」の表に貼る。
   ```bash
   python3 <このスキルのディレクトリ>/list_items.py practices <束> [<束> ...]
   ```
   ```bash
   python3 <このスキルのディレクトリ>/list_items.py standards <束> [<束> ...]
   ```
   - 「このリポジトリでの場面」は、リポジトリを読んで具体的に書けるものだけ書く。書けなければ「—」のまま。
   - 「このプロジェクトの立場」は、`AGENTS.md`、ADR、検査で決まっているものだけ、そこを指す。決まっていなければ「未定」。立場を推測で決めない。
   - 項目は 40 個まで。超えるなら、当たりそうにない項目を「外したもの」に移す案を所有者に示す。
   - 標準の対応表に使う項目が無ければ、表を空のまま残す。
6. **検査をつなぐ。**
   - `Makefile` に `knowledge-check` のターゲット（置かれた `check-knowledge.py` を `python3` で呼ぶ）を足し、`check` から呼ぶ。
   - `docs/dev/harness.md` に、検査の行を足す。
   - `docs/README.md` に、対応表の 2 つの文書を載せる。
   - CI に Python 3 が無ければ、導入を足す。
7. **plugin を有効にする。** `.claude/settings.json` の `enabledPlugins` に `knowledge@ai-dev-methodologies` を足す。
8. **引くきっかけを書く。** `AGENTS.md` のガードレールに、次を足す。
   - 設計・実装・レビューで機械で検出できない判断をするときは、スキル `practices` で対応表と目録を引き、当たった項目の ID を PR に書く。
   - ファイル形式・記法・プロトコル・設定ファイルの書き方を決めるときは、スキル `standards` で一次情報に当たる。
   PR テンプレートに「当たった索引の項目」の欄が無ければ、足す。
9. **すでにある索引を扱う。** リポジトリにすでにプラクティスや標準の索引があれば、消さない。目録にある項目と重なるものと、このリポジトリにだけあるものを分けて所有者に示し、どう移すかを決めてもらう。
10. **確かめる。** `make check` を通す。
11. **報告する。** 選んだ束、対応表の項目の数、「このプロジェクトの立場」が決まっていた項目、所有者が決めること、を一覧にする。

## 新しい版に合わせる

コピーするファイルの結果（`same`、`updated`、`edited`、`kept`）の読み方と、`kept` のときの手順は、`core` のスキル `adopt` の「新しい版に合わせる」と同じ。

目録の項目が増えたときは、手順 3 から行う。`./.agents/knowledge-ids.txt` が新しくなり、増えた項目を対応表に足せるようになる。足すかどうかは、所有者に示す。

## 守ること

- 対応表の「このプロジェクトの立場」を、推測で決めない。
- 目録の項目を、導入先で書き換えない。直すべきなら、ai-dev-methodologies の `observation` の Issue にする案を示す。
