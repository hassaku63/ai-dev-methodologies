# AWS CDK

AWS CDK（v2）のコードの判断。反映（`cdk deploy`）は人間が行う前提で、設計、計画（`cdk diff`、`cdk synth`）、レビューのときに引く。項目の形は `plugins/knowledge/catalog/README.md`。

### データを持つリソースの論理 ID を変えない

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-stable-logical-ids` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Don't change the logical ID of stateful resources」「Separate your application into multiple stacks as dictated by deployment requirements」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| ソース | なし |
| 何を言っているか | リソースの論理 ID が変わると、次の反映でそのリソースは新しいものに置き換わる。データベースや S3 のバケット、VPC のような、データや長く使う基盤を持つものでは、まず望まない。論理 ID は構成の木の中の位置と名前から決まるので、コードの整理（コンストラクトの名前の変更、移動）で変わりうる。データを持つリソースの論理 ID が変わらないことを確かめる単体テストを書く。データを持つリソースは、移動や名前の変更が起きやすいコンストラクトの中に入れず、別のスタックに分けて終了保護をかけることを考える。 |
| 確からしさ | 公式の推奨。誤用: コンストラクトの名前を整えるリファクタリングを、`cdk diff` の置き換えを見ずに出す。 |
| 当たるべき場面 | コンストラクトの名前の変更、移動、切り出しの差分を書く、レビューするとき。`cdk diff` に、データを持つリソースの置き換え（`replace`）が出たとき。スタックの分け方を決めるとき。 |
| 判断の問い | この差分で、データを持つリソースの論理 ID は変わっていないか（`cdk diff` に置き換えが出ていないか）。論理 ID が変わらないことを、テストで確かめているか。データを持つリソースは、名前の変わりやすいコンストラクトの中にないか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### コンストラクトとスタックは、環境変数ではなくプロパティで設定する

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-props-not-env-vars` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Configure with properties and methods, not environment variables」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| ソース | なし |
| 何を言っているか | コンストラクトやスタックの中で環境変数を読むのは、よくある誤り。どちらもプロパティのオブジェクトを受け取り、コードの中ですべてを設定できるようにする。環境変数を読むと、コードを動かす機械への依存が生まれ、追跡すべき設定が増える。環境変数を読むのは、アプリの最上位に限り、主に開発の環境で動かすための情報に使う。 |
| 確からしさ | 公式の推奨。誤用: スタックの中で `process.env` を読み、手元と CI で違うテンプレートができる。 |
| 当たるべき場面 | コンストラクトやスタックに、設定の値（環境の名前、アカウント、サイズ）を渡す形を決めるとき。 |
| 判断の問い | コンストラクトやスタックの中で、環境変数を読んでいないか。同じコミットから、どの機械でも同じテンプレートができるか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 合成を決定的にする: 判断は合成のときに行い、外への問い合わせは cdk.context.json に留める

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-deterministic-synthesis` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Make decisions at synthesis time」「Commit cdk.context.json to avoid non-deterministic behavior」「Model all production stages in code」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| ソース | なし |
| 何を言っているか | 同じ環境に対しては、いつ反映しても同じ結果になるようにする。CloudFormation の条件やパラメータで反映のときに分岐せず、プログラムの言語の `if` で合成のときに決める。合成の中で AWS の SDK などで問い合わせると、値が変わったときに構成が変わる（AZ の数が増えてサブネットが作り直しになる、最新の AMI でインスタンスが置き換わる）。`.fromLookup()` の結果は `cdk.context.json` に記録されるので、コミットする。合成で AWS を変えてはいけない（読み取りでも安全とは限らない）。本番を含むすべての段階を、別々のスタックとしてコードに書く。 |
| 確からしさ | 公式の推奨。文脈の提供者が無い値は、別のスクリプトで取ってファイルに書き、合成はそのファイルを読む（スクリプトは値を更新したいときだけ走らせる）。誤用: `cdk.context.json` を `.gitignore` に入れる。合成のたびに最新の AMI や AZ の一覧を取る。 |
| 当たるべき場面 | 環境ごとの違い（アカウント、リージョン、サイズ）の持ち方を決めるとき。`fromLookup` や SDK の呼び出しを、スタックのコードに足すとき。`cdk.context.json` の差分をレビューするとき。 |
| 判断の問い | 同じコミットから、いつ合成しても同じテンプレートができるか。合成の中で、記録されない問い合わせをしていないか。CloudFormation の条件やパラメータでの分岐を、コードの分岐にできないか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 物理的な名前を付けず、生成された名前を渡す

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-generated-names` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Use generated resource names, not physical names」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| ソース | なし |
| 何を言っているか | テーブルやバケットに名前を固定すると、同じアカウントに 2 度反映できない。さらに、作るときにしか決められない属性（DynamoDB のテーブルのキーの構成など）を変えると、新しいリソースへの置き換えになるが、同じ名前のものは古いものがあるうちは作れない。名前はできるだけ付けず、CDK に生成させる。名前が要る所には、`table.tableName` のような参照で渡す。同じアプリのスタックの間は参照を渡し、別のアプリからは `fromArn()` などで参照する。 |
| 確からしさ | 公式の推奨。誤用: 見分けやすさのために、すべてのリソースに物理的な名前を付ける。 |
| 当たるべき場面 | リソースの名前のプロパティ（`bucketName`、`tableName` など）を書くとき。アプリケーションに、リソースの名前を渡す方法を決めるとき。 |
| 判断の問い | この物理的な名前は、本当に固定が要るか（外から名前で参照される、など）。固定したとき、置き換えの要る変更ができなくなるのを受け入れているか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 削除の方針とログの保持期間を、リソースごとに決める

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-removal-and-retention` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Define removal policies and log retention」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| ソース | なし |
| 何を言っているか | CDK は、データを失わないよう、既定ですべてを残す方針を取る。データを持つリソース（バケット、テーブル）の既定の削除の方針は、スタックから外しても削除せず、スタックから切り離す（孤立させる）。ログの既定は、永遠に保持する。本番のリソースごとに方針を考えて指定し、Aspects で方針を確かめる。 |
| 確からしさ | 公式の推奨。本番の環境では、この既定のために要らないデータが大量に残り、その分の費用がかかりうる、とページは書く。誤用: 開発の都合で `DESTROY` を既定にし、本番にもそのまま適用する。 |
| 当たるべき場面 | データを持つリソースとロググループを足すとき。スタックからリソースを外す差分をレビューするとき。 |
| 判断の問い | このリソースの削除の方針は、本番でも同じでよいか。スタックから外したとき、リソースは消えるか、残るか（残るなら、誰が後片付けをするか）。ログの保持期間は決めてあるか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 細かい検証のテストとスナップショットのテストを、役割で使い分ける

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-fine-grained-vs-snapshot-tests` |
| 出どころ | AWS「Test AWS CDK applications」。https://docs.aws.amazon.com/cdk/v2/guide/testing.html |
| ソース | なし |
| 何を言っているか | 細かい検証（`Template.fromStack` で「このリソースはこの属性をこの値で持つ」を確かめる）は、退行を見つけ、テストを先に書く開発にも使える。スナップショットのテストは、保存した基準のテンプレートと比べ、リファクタリングで振る舞いが同じことを確かめられる。ただし CDK の版を上げるだけでもテンプレートは変わるので、スナップショットだけに頼って正しさを確かめることはできない。 |
| 確からしさ | 公式の推奨。誤用: スナップショットの差分を、読まずに基準として受け入れる。細かい検証で、テンプレートの全体を写して確かめる（実質はスナップショットになる）。 |
| 当たるべき場面 | CDK のコードにテストを足すとき。CDK の版を上げて、スナップショットのテストが落ちたとき。 |
| 判断の問い | 守りたい性質（暗号化、公開しない、論理 ID）は、細かい検証で確かめているか。スナップショットの差分を受け入れる前に、何が変わったかを読んだか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 規則の強制は、自前のラッパーではなく組織の仕組みと検査で行う

| 欄 | 内容 |
| --- | --- |
| ID | `cdk-compliance-guardrails` |
| 出どころ | AWS「Best practices for developing and deploying cloud infrastructure with the AWS CDK」の「Constructs aren't enough for compliance」「Let the AWS CDK manage roles and security groups」。https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html 。cdklabs「cdk-nag」の README。https://github.com/cdklabs/cdk-nag |
| ソース | `cdklabs/cdk-nag:README.md@5dbf92f` |
| 何を言っているか | 暗号化や IAM の方針を強制するために L2 のコンストラクトを包む自前のコンストラクトを作っても、開発者はそれを使わずに済ませられ、Construct Hub などの外のコンストラクトも使えなくなる。強制は、サービスコントロールポリシーや権限の境界で組織の水準で行い、反映の前の検査（Aspects、CloudFormation Guard）で確かめる。権限は、`grants` のメソッド（`bucket.grants.read(fn)` など）に、最小の範囲で作らせる。cdk-nag は、規則の束（AWS Solutions など）でアプリを検査し、違反を見送るときは対象のコンストラクトと理由を書く。 |
| 確からしさ | 公式の推奨（AWS）と、AWS のプロジェクトの道具の文書（cdk-nag）。誤用: 違反を見送る理由を書かずに抑制する。セキュリティの担当が作ったロールだけを使わせ、コードを複雑にする。 |
| 当たるべき場面 | セキュリティの規則（暗号化、公開しない、最小の権限）を、CDK のコードに持ち込む方法を決めるとき。cdk-nag などの検査を足す、違反を見送るとき。IAM のポリシーを手で書きたくなったとき。 |
| 判断の問い | この規則は、コードのラッパーではなく、組織の仕組みか反映の前の検査で強制できないか。見送った違反には、対象と理由が書いてあるか。手で書いた IAM のポリシーは、`grants` のメソッドで置き換えられないか。 |
| 対象 | `aws-cdk-lib@2` |
| 確認 | 2026-11-15 / 間隔 180 日 |
