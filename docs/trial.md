# 実際のリポジトリで試す

配る部品は、架空の例でしか動かしていない（`docs/roadmap.md`）。実際のリポジトリに導入して、何が動き、何が動かなかったかを集める手順。

報告は、試用の報告の Issue（<https://github.com/hassaku63/ai-dev-methodologies/issues/11>）に、コメントで集める。このリポジトリは公開されているので、報告には導入先に固有の情報を入れない（ADR-0004）。

## 進め方

1. **導入先を選ぶ。** 次のどれかに当たるリポジトリ。1 回の試用で 1 つ。
   - AWS のインフラを調べて記録するリポジトリ（`core` と `aws-ops`）
   - Terraform か CDK のリポジトリ（`core` と `aws-iac`）
   - どちらでもないリポジトリ（`core` だけ）
2. **作業用のブランチを切る。** 導入の結果は、良ければ PR にし、悪ければブランチごと捨てる。
3. **読み取り専用の認証情報を用意する。** `aws-ops` と `aws-iac` では、エージェントが使う AWS の認証情報を、読み取りだけ（`aws-iac` は加えて state の読み取りまで）にする。フックは安全網で、防壁は認証情報の権限。
4. **plugin を入れる。** 導入先のリポジトリの最上位で、使う plugin だけを入れる。GitHub に SSH の鍵が無い環境では、先に `export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` を実行する。

   ```bash
   claude plugin marketplace add hassaku63/ai-dev-methodologies --scope project
   ```

   ```bash
   claude plugin install core@ai-dev-methodologies --scope project
   ```

   ```bash
   claude plugin install aws-ops@ai-dev-methodologies --scope project
   ```

   ```bash
   claude plugin install aws-iac@ai-dev-methodologies --scope project
   ```

5. **Claude Code のセッションで導入する。** 新しいセッションを始め、順に実行する。各スキルの問いには、所有者が答える。
   - `/core:adopt`
   - `/aws-ops:adopt` か `/aws-iac:adopt`（入れた plugin に合わせて）
6. **使ってみる。** 入れた plugin に合わせて、少なくとも 1 つ。
   - `/aws-ops:inventory`
   - `/aws-ops:findings`
   - `/aws-iac:plan`（コードを少し変えたブランチで）
   - `core` だけなら、`observation` の Issue を 1 つ作り、`/core:propose` で企画にする
7. **フックを確かめる。** `aws-ops` か `aws-iac` を入れたなら、エージェントに、止まるはずのコマンドを 1 つ実行するよう頼む（`aws-ops` は `aws ec2 stop-instances --instance-ids i-0000000000000000`、`aws-iac` は `terraform apply`）。止まったか、止まらずに実行されかけたかを見る。認証情報が読み取り専用なら、止まらなくても環境は変わらない。
8. **報告を作らせる。** 同じセッションで、下の「報告を作らせるプロンプト」を貼る。
9. **確かめて貼る。** 出てきた報告を所有者が読み、固有の情報が残っていないことを確かめてから、試用の報告の Issue にコメントで貼る。セッションに直接投稿させない。

## 報告を作らせるプロンプト

次の枠の中を、そのまま貼る。

````text
このセッションで、ai-dev-methodologies（hassaku63/ai-dev-methodologies）の plugin を試した。その結果を、公開のリポジトリの Issue に貼る報告にまとめてほしい。報告は私（所有者）が読んでから貼る。あなたは GitHub に投稿しない。

## 守ること

報告は公開される。次を報告に入れない。入れる必要があるときは、`<app-1>`、`<bucket-1>`、`<account>`、`<region>` のような置き換えにする。

- AWS のアカウント ID、ARN、リソースの名前と ID、IP アドレス、ホスト名、URL（ai-dev-methodologies と、AWS・Terraform・CDK の公開の文書のものを除く）
- 組織、チーム、人、顧客、プロダクトの名前。このリポジトリの名前と、パス（ai-dev-methodologies が置いたファイルのパスを除く）
- 業務の内容、Finding の中身、構成の中身、plan の中身。数は、範囲（「10 未満」「10〜50」「50 より多い」）で書く
- 秘密情報、認証情報、プロファイルの名前、環境変数の値
- エラーの文に上のものが入っていれば、その部分を置き換える

迷ったものは入れない。

## 報告の形

次の見出しで、Markdown で書く。分からないことは「分からない」と書く。推測には「推測」と書く。

### 環境
- Claude Code の版（`claude --version`）、OS の種類
- 入れた plugin と、ai-dev-methodologies のコミット（`.agents/methodology.lock` か、plugin のキャッシュのディレクトリの名前から分かる範囲で）
- 使った道具と、その版: aws CLI、Python、Terraform、tflint、Node、CDK のうち、使ったもの

### 導入先の種類
- 系統（運用・管理、IaC、アプリケーション、その組み合わせ）と、主な技術（Terraform、CDK、言語の名前）
- 規模の目安: ファイルの数、インフラのコードのルートの数、対象のリージョンの数（範囲で）
- 導入の前にあったもの: 指示書（AGENTS.md、CLAUDE.md など）、Makefile、CI、lint の設定の有無

### 実行したこと
実行したスキルとコマンドを、順に箇条書きで。スキルの手順のどこを飛ばしたか、どこで所有者に尋ねたか。

### 結果
スキルごとに、次の表で。

| スキル | 結果（動いた／一部動いた／動かなかった） | 起きたこと |
| --- | --- | --- |

続けて、次を箇条書きで。
- 落ちた検査、エラー、例外。文はそのまま（置き換えたうえで）引く
- スクリプトの出力が、実際の AWS や Terraform の出力の形と合わなかったところ（欠けた表、数えられなかったもの、読めなかったファイル）
- フックが止めたもの。止めるべきなのに止めなかったもの。止めなくてよいのに止めたもの
- `make check` の結果

### 手順と実際のずれ
スキルや雛形が前提にしていたが、このリポジトリでは成り立たなかったこと（ディレクトリの構成、ブランチの名前、ツールの有無、権限）。そのときにどうしたか。

### 使ってみて
- 記録（棚卸し、Finding のまとめ、plan の要約）は、次に何をするかを決めるのに役立ったか。役立たなかったなら、何が足りなかったか（中身は書かず、足りなかった種類だけ）
- 所有者が手で直した、または書き足したもの

### ai-dev-methodologies への提案
直すとよいと思うことを、重い順に。それぞれ、どのファイルかスキルか、何をどう変えるか。

## 出す前に

報告を出す前に、上の「守ること」の各項目について、報告の全文を見直す。見直したあと、報告を 1 つの Markdown のコードブロックにして出し、そのあとに「見直した項目」と「置き換えたものの数」を 1 行ずつ書く。
````

## 報告を受けたあと

このリポジトリの作業として行う。

1. 報告から、直すことを拾う。1 つの問題につき 1 つの `observation` の Issue にし、報告のコメントを `refs` で指す。
2. 報告に固有の情報が残っていたら、所有者に伝え、コメントを直してもらう。
3. `docs/roadmap.md` の「段階 3 と 4 の部品は、…まだ動かしていない」を、試したものに合わせて直す。
