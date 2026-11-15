# Terraform

Terraform のコードと state の扱いの判断。反映（`terraform apply`）は人間が行う前提で、計画とレビューのときに引く。項目の形は `plugins/knowledge/catalog/README.md`。

### 名前や構造を変えるときは、moved ブロックで住所を移す

| 欄 | 内容 |
| --- | --- |
| ID | `tf-moved-blocks` |
| 出どころ | HashiCorp「Refactor modules」。https://developer.hashicorp.com/terraform/language/modules/develop/refactoring |
| ソース | なし |
| 何を言っているか | リソースやモジュールの名前を変える、モジュールに入れる、`count` と `for_each` を切り替えると、Terraform はそれを「古い住所のものを壊し、新しい住所に作る」と解釈する。`moved` ブロックで古い住所と新しい住所を書くと、壊さずに state の住所だけを移す。v1.1 から使える。それより前は `terraform state mv` を使う。`moved` ブロックを消すことは、そのモジュールを使う側にとって壊れる変更になる。 |
| 確からしさ | 公式の推奨。種類（type）をまたいだ移動は、provider が対応している場合に限られる。誤用: 名前を変えて plan に出た削除と作成を、そのまま反映する。`moved` を書いたあと、すぐ消す（まだ移していない環境やモジュールの利用者で、壊して作り直しになる）。 |
| 当たるべき場面 | リソースやモジュールの名前を変える、モジュールに切り出す・まとめる、`count` と `for_each` を切り替える差分を書く、レビューするとき。plan に、意図していない削除と作成の組が出たとき。 |
| 判断の問い | この差分の plan で、置き換え・削除と作成の組になっているリソースは、住所が変わっただけではないか。`moved` ブロックで、壊さずに移せないか。消そうとしている `moved` ブロックは、すべての環境と利用者で移し終えたか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### state と plan のファイルには秘密情報が入る。sensitive は表示を隠すだけ

| 欄 | 内容 |
| --- | --- |
| ID | `tf-state-holds-secrets` |
| 出どころ | HashiCorp「Manage sensitive data in your configuration」。https://developer.hashicorp.com/terraform/language/manage-sensitive-data |
| ソース | なし |
| 何を言っているか | 設定に書いた秘密情報や、リソースの属性（初期のパスワード、トークン）は、state と plan のファイルにそのまま入る。手元の state は平文。`sensitive` は CLI の出力と画面で値を伏せるだけで、state には残る。state にも plan にも残さないには、ephemeral の値を使う（変数と子モジュールの出力の `ephemeral` と `ephemeral` ブロックは v1.10、管理するリソースの write-only の引数は v1.11 から。使えるものは provider ごとに違う）。state は、暗号化できるリモートの置き場所に置き、Git に入れない。 |
| 確からしさ | 公式の推奨。リモートの state の暗号化の方法は、バックエンドごとに違う。誤用: `sensitive = true` を付けたので、state に秘密情報が残らないと考える。plan のファイルを、レビューのために PR や Issue に貼る。 |
| 当たるべき場面 | 秘密情報（パスワード、鍵、トークン）を Terraform に渡す設計を決めるとき。plan や state を、人やエージェントに見せる・共有するとき。state の置き場所と権限を決めるとき。 |
| 判断の問い | この値は、state か plan のファイルに残るか。残るなら、ephemeral の値か write-only の引数（あるいは、秘密情報の置き場所のサービスから実行時に読む形）にできないか。plan や state の中身を、会話・PR・Issue に写していないか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### count はほぼ同じものの数に、for_each は値の違うものの集まりに使う

| 欄 | 内容 |
| --- | --- |
| ID | `tf-count-vs-for-each` |
| 出どころ | HashiCorp「count」。https://developer.hashicorp.com/terraform/language/meta-arguments/count 。HashiCorp「Style guide」の「Use count and for_each sparingly」。https://developer.hashicorp.com/terraform/language/style |
| ソース | なし |
| 何を言っているか | `count` は、ほぼ同じインスタンスを数で作るときに使う。インスタンスごとに整数の番号から導けない値が要るなら `for_each` を使う。`count` のインスタンスは 0 から始まる番号で区別され、`for_each` のインスタンスはキーで区別される。スタイルガイドは、どちらも使いすぎないよう勧め、効果が明らかでないときはコメントを付けるとする。 |
| 確からしさ | 公式の推奨。番号で区別されるので、`count` で並べたものの途中を消すと、後ろのものの番号がずれ、置き換えの plan になりうる（番号とインスタンスの対応から導いたもので、ページにこの例は無い）。誤用: 名前の一覧を `count` と `count.index` で回す。 |
| 当たるべき場面 | 同じ種類のリソースを複数作る差分を書く、レビューするとき。一覧から 1 つを足す・消す差分の plan に、置き換えが並んだとき。 |
| 判断の問い | インスタンスは、番号で区別して困らないほど同じか。一覧の途中を足し引きしたとき、ほかのインスタンスの住所が変わらないか（変わるなら `for_each` とキーにし、`moved` で移す）。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 依存のロックファイルをコミットし、上げるときはレビューする

| 欄 | 内容 |
| --- | --- |
| ID | `tf-dependency-lock` |
| 出どころ | HashiCorp「Dependency Lock File (.terraform.lock.hcl)」。https://developer.hashicorp.com/terraform/language/files/dependency-lock 。HashiCorp「Style guide」の「.gitignore」と「Version pinning」。https://developer.hashicorp.com/terraform/language/style |
| ソース | なし |
| 何を言っているか | `.terraform.lock.hcl` は、選ばれた provider の版とチェックサムを記録する（v0.14 から）。`terraform init` が作り、更新する。リポジトリにコミットし、依存の変更をコードと同じくレビューで話せるようにする。版の制約の範囲で上げるのは `terraform init -upgrade` で、ロックファイルの変更を読んでからコミットする。モジュールの版はロックファイルに記録されないので、版の制約で固定する。コミットしないもの: state のファイル、`.terraform` のディレクトリ、`-out` で作った plan のファイル、秘密情報を含む `.tfvars`。 |
| 確からしさ | 公式の推奨。チェックサムは、手元と CI で別の OS を使うと足りないことがある（`terraform providers lock` で複数の環境の分を記録する）。誤用: ロックファイルを `.gitignore` に入れる。provider の制約を書かず、ロックファイルだけに頼る。 |
| 当たるべき場面 | provider やモジュールの版を足す・上げる差分を書く、レビューするとき。`.gitignore` を決めるとき。CI で `terraform init` がチェックサムの食い違いで落ちたとき。 |
| 判断の問い | ロックファイルはコミットされているか。この差分のロックファイルの変更は、意図した provider の版の変更だけか。モジュールの呼び出しは、版を固定しているか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### lifecycle の守りには抜け穴がある

| 欄 | 内容 |
| --- | --- |
| ID | `tf-lifecycle-cautions` |
| 出どころ | HashiCorp「lifecycle」。https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle |
| ソース | なし |
| 何を言っているか | `prevent_destroy` は、そのリソースを壊す plan を拒む。ただし規則は state に記録されないので、リソースのブロックそのものを設定から消すと、反映で実際に壊れる。`create_before_destroy` は、名前が一意でなければならない種類などでは、新旧が同時に存在できず使えない。依存するリソースにも引き継がれる。`ignore_changes` は、作ったあとに変わりうる値を参照するときや、Terraform の外の仕組みと 1 つのものを管理を分け合うときに使う。 |
| 確からしさ | 公式の推奨。`prevent_destroy` は控えめに使うよう書かれている（変えられない設定の変更や、`terraform destroy` が効かなくなる）。誤用: `prevent_destroy` があるので、ブロックを消す差分も安全だと考える。plan の差分を消すために `ignore_changes` を足し、実際の構成とコードのずれを隠す。 |
| 当たるべき場面 | データを持つリソース（データベース、バケット、ボリューム）を守る設計を決めるとき。リソースのブロックを消す差分をレビューするとき。plan に出続ける差分を、`ignore_changes` で止めたくなったとき。 |
| 判断の問い | この差分は、`prevent_destroy` の付いたリソースのブロックを消していないか。`ignore_changes` で無視する属性は、誰が（どの仕組みが）変えるのか言えるか。言えないなら、無視ではなく、コードを実際に合わせるべきではないか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### terraform test は、既定で実際のインフラを作る

| 欄 | 内容 |
| --- | --- |
| ID | `tf-test-creates-infrastructure` |
| 出どころ | HashiCorp「Tests」。https://developer.hashicorp.com/terraform/language/tests |
| ソース | なし |
| 何を言っているか | `terraform test` は v1.6 から使える。`run` ブロックは、既定で `command = apply` として、実際のインフラを作って確かめる（結合テストに当たる）。`command = plan` にすると、新しいインフラを作らずに、計算や条件を確かめる（単体テストに当たる）。v1.7 からは、provider の返す値を偽物にできる（mock）。 |
| 確からしさ | 公式の文書。誤用: 単体テストのつもりで `command` を書かずに走らせ、実際のアカウントにリソースを作る。テストを、本番に届く認証情報で走らせる。 |
| 当たるべき場面 | Terraform のコードにテストを足すとき。CI やエージェントに `terraform test` を走らせるか決めるとき。 |
| 判断の問い | この `run` ブロックは、`command = plan` か mock で足りないか。`apply` で走るなら、どのアカウントに何を作り、誰が後片付けを確かめるか。エージェントに任せる範囲（計画まで）の中で走らせてよいテストか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 既存のリソースは、import ブロックでコードとして取り込む

| 欄 | 内容 |
| --- | --- |
| ID | `tf-import-blocks` |
| 出どころ | HashiCorp「Import resources overview」。https://developer.hashicorp.com/terraform/language/import |
| ソース | なし |
| 何を言っているか | 既存のリソースを管理に入れるときは、`import` ブロックに、取り込むリソースの ID と state の住所を書き、同じ住所のリソースのブロックを用意して、反映で取り込む。リソースのブロックは、`import` ブロックだけを書いて `terraform plan` の `-generate-config-out` で作らせることもできる。多くを取り込むときは、問い合わせを HCL で書いて見つける方法もある。 |
| 確からしさ | 公式の文書。推測（ページには書かれていない）: `import` ブロックは、取り込みをコードとして PR でレビューでき、plan で何が起きるかを先に見られる。`terraform import` のコマンドは、レビューを経ずに state だけを変える。生成された設定は、そのまま使わずに読み直す必要がある。誤用: エージェントや手元で `terraform import` を直接走らせ、state だけを先に変える。 |
| 当たるべき場面 | 手で作られたリソースを、Terraform の管理に入れるとき。構成の棚卸しで、どのコードにも無いリソースが見つかったとき。 |
| 判断の問い | この取り込みは、`import` ブロックとして PR でレビューできる形か。plan で、取り込み以外の変更（属性の差による更新や置き換え）が一緒に出ていないか。 |
| 対象 | `terraform@1` |
| 確認 | 2026-11-15 / 間隔 180 日 |

## 外したもの

| 知見 | 外した理由 |
| --- | --- |
| ファイルの分け方（`main.tf`、`variables.tf` など）と、名前の付け方（Style guide） | 書式と配置の慣習で、`terraform fmt` とレビューの慣れで足りる。学習済みの一般的な知識で足りる |
