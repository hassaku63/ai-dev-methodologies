# 知識の目録

開発のプラクティスと業界標準の、出どころに付く知見の目録。導入先のリポジトリは、このうち使う項目を、自分の対応表（`<導入先>/docs/knowledge/practices.md`、`<導入先>/docs/knowledge/standards.md`）で選び、そのリポジトリでの場面と立場を書く。決定は ADR-0011。

## 束

| 種類 | 束 | 中身 |
| --- | --- | --- |
| プラクティス | `practices/general.md` | 型と境界、抽象、変更の分け方とレビュー |
| プラクティス | `practices/testing.md` | テストを何で、どう書くか |
| プラクティス | `practices/agent-workflow.md` | エージェントとの作業の進め方 |
| プラクティス | `practices/go.md` | Go |
| プラクティス | `practices/typescript.md` | TypeScript |
| プラクティス | `practices/react.md` | React |
| プラクティス | `practices/test-tools-js.md` | JavaScript のテストの道具（Testing Library、Vitest） |
| 業界標準 | `standards/containers.md` | コンテナとビルド（Dockerfile、BuildKit の Build checks、Compose） |

## 載せるもの・載せないもの

載せるのは次の 4 種類。学習済みの一般的な知識で足りるものは載せない。

1. 版で変わるもの（技術の、今の版での推奨）
2. 流儀が割れるもの（並び立つ立場と出どころ）
3. やりがちな逆（知っていても起きる乱雑さの元）
4. レビューの観点（機械で検出できず、レビューで見るもの）

- 書かない: 出どころの文章の写し、例のコード、手順。出どころを開かずに書いた中身。特定のリポジトリの事情。
- 検討して載せなかった知見は、束の「外したもの」の節に、理由と一緒に 1 行残す。

## プラクティスの項目の形

`###` の見出しと、次の欄を持つ表。`make catalog-check` が形を検査する。

| 欄 | 書き方 |
| --- | --- |
| ID | 対応表から指す名前。`` `kebab-case` ``。目録の中で 1 つ。変えない |
| 出どころ | 著者と題、URL |
| ソース | Git で公開されていれば `` `owner/repo:path@コミット` ``（複数なら `, ` で区切る）。なければ「なし」 |
| 何を言っているか | 自分の言葉で 2〜4 行 |
| 確からしさ | 公式の推奨／広く共有された実務の知見／一流派の主張、とよくある誤用 |
| 当たるべき場面 | どの判断のときに引くか。特定のリポジトリの例を書かない |
| 判断の問い | 差分か設計を見て答えられる問い |
| 対象 | 関係する技術と、確かめた時点の版。導入先の検査が、そのリポジトリで使っている版と比べ、違えば落とす。名前は、依存のファイルでの名前（npm のパッケージ名、Go のモジュール、Terraform の provider は `hashicorp/aws` の形、道具は `node`、`go`、`python`、`terraform`）。`` `react@19` ``、`` `go@1.27` ``、`` `python@3.12` ``、`` `hashicorp/aws@5` `` のように。技術によらなければ「なし」 |
| 確認 | `YYYY-MM-DD / 間隔 N 日`。出どころを実際に開いた日と、見直しの間隔 |

## 業界標準の項目の形

| 欄 | 書き方 |
| --- | --- |
| ID | プラクティスと同じ |
| 発行元 | 標準を決めている組織やプロジェクト |
| 何を決めているか | 1〜2 行 |
| 一次情報 | URL と、入手の条件（登録の要否、有償か） |
| 状態 | 現行か、後継があるか。確かめた時点の版 |
| 当たるべき場面 | どの判断のときに引くか |
| 確認 | プラクティスと同じ |

仕様の本文や要約、例のコードは書かない。

## 項目を足す・直す

- 出どころを開いて書く。開けなかった出どころの項目は足さない。
- 項目を直したら、確認の日を開いた日にする。出どころを開かずに確認の日だけを変えない。
- 古くなった項目は、月次の報告が挙げる。確かめ直す手順は `docs/dev/knowledge-review.md`。
- ID は変えない。導入先の対応表が指している。項目を外すときは、束の「外したもの」に移し、ID を書いておく。

## 出どころ

次の束は、`hassaku63/chord-rambler` の索引から移した。プラクティスは `hassaku63/chord-rambler:.claude/skills/practices/index.md@76ea655`、業界標準は `hassaku63/chord-rambler:.claude/skills/standards/index.md@76ea655`。

- プラクティス: `practices/general.md`、`practices/testing.md`、`practices/agent-workflow.md`、`practices/go.md`、`practices/typescript.md`、`practices/react.md`、`practices/test-tools-js.md`
- 業界標準: `standards/containers.md`

移すときに、当たるべき場面と判断の問いから chord-rambler に固有の例を外し、ID を足した。業界標準の「chord-rambler との接点」は、導入先の対応表の「このリポジトリとの接点」に当たるので外した。出どころ・何を言っているか・確からしさ（標準では何を決めているか・状態）・確認は、chord-rambler が出どころを開いて書いたものをそのまま使っている。このリポジトリでは、出どころの中身を開き直していない（月次の報告が、出どころの URL が開けることと、記録したソースが変わっていないことを確かめる）。
