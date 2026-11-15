# 0010. IaC のリポジトリでは、フックで操作を計画までに限る

- 日付: 2026-11-15
- 状態: Accepted

## 文脈

Terraform や CDK のリポジトリでは、エージェントにコードの変更と、変更の計画（`terraform plan`、`cdk diff`）までを任せたい（ADR-0005 の L2）。反映（`terraform apply`、`cdk deploy`）は人間が行う。

反映のほかにも、エージェントに任せると危うい操作がある。state を書き換える操作（`state rm`、`import`、`force-unlock`）は、インフラを変えずに、Terraform の認識だけを壊す。`terraform test` は、実際のリソースを作る。`terraform output` や `state show`、`state pull` は、秘密情報の値を表示しうる。

運用・管理のリポジトリのフック（ADR-0009）と同じく、権限の設定の前方一致では、`-chdir=` のようなオプションを前に置いた呼び出しを書ききれない。

## 決定

1. plugin `aws-iac` が、Bash の実行の前に走るフックを持つ。`terraform`、`tofu`、`terragrunt`、`cdk`、`aws` の呼び出しをすべて見る。
2. **通すものを並べる。** インフラも、リモートの state も変えないサブコマンドだけを通す（`init`、`fmt`、`validate`、`plan`、`show`、`synth`、`diff` など）。それ以外は止める。
3. **秘密情報を表示しうるものは、所有者に尋ねる。** `terraform output`、`state show`、`console`。`state pull` は止める。
4. `aws` の呼び出しには、運用・管理のリポジトリと同じ規則（読み取りだけ）を当てる。フックの実体を共有する。
5. フックは安全網で、防壁ではない。スクリプトや `Makefile` のターゲットの中（`make apply`、`npm run deploy`）は見えない。防壁は、エージェントが使う認証情報の権限に置く。plan に要るのは読み取りの権限と、state の読み取りまで。
6. 開発環境に限った反映（L3）を許す部品は、まだ作らない。環境の見分け方を決めてから足す。

## 検討した選択肢

- **反映のサブコマンドだけを止める**（`apply`、`destroy`、`deploy`）: 一覧が短い。`import`、`state rm`、`test`、`watch` のような、反映と呼ばれないが変える操作が通る。
- **`terraform` と `cdk` をすべて所有者の確認にする**: 確実。plan と検証は作業のたびに何度も走らせるので、確認が多すぎる。

## 結果

- `terraform init` は通る。手元の `.terraform` を作り、バックエンドに接続する。state の移行を伴うオプションは止める。
- 一覧にないサブコマンド（新しい版で足されたもの）は止まる。要るものは一覧に足す。
- フックは Python 3 を要する。
- 再検討の条件: 止まった計画の操作の報告が続くとき。フックをすり抜けた反映があったとき。L3 を作るとき。
