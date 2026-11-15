# 構成の棚卸し（2026-11-01）

AWS から読み取った構成を、そのまま表にしたもの。対象のリージョン: ap-northeast-1。

## ap-northeast-1

取得できなかったもの（権限かサービスの状態による。該当する表は欠けている）: `discovered-explorer`

### ネットワーク

| VPC | 名前 | CIDR | 既定 |
| --- | --- | --- | --- |
| `vpc-0a1b2c3d4e5f60001` | main | 10.0.0.0/16 | いいえ |
| `vpc-0a1b2c3d4e5f60002` | — | 172.31.0.0/16 | はい |

サブネット。「外向き」は、ルートテーブルが `0.0.0.0/0` をインターネットゲートウェイに向けているもの。

| サブネット | 名前 | VPC | AZ | CIDR | 外向き |
| --- | --- | --- | --- | --- | --- |
| `subnet-0aaa000000000001` | public-a | `vpc-0a1b2c3d4e5f60001` | ap-northeast-1a | 10.0.0.0/24 | はい |
| `subnet-0aaa000000000003` | private-a | `vpc-0a1b2c3d4e5f60001` | ap-northeast-1a | 10.0.10.0/24 | いいえ |
| `subnet-0aaa000000000002` | public-c | `vpc-0a1b2c3d4e5f60001` | ap-northeast-1c | 10.0.1.0/24 | はい |
| `subnet-0aaa000000000004` | private-c | `vpc-0a1b2c3d4e5f60001` | ap-northeast-1c | 10.0.11.0/24 | いいえ |

出入り口。

| 種類 | ID | VPC | 補足 |
| --- | --- | --- | --- |
| インターネットゲートウェイ | `igw-0ccc000000000001` | `vpc-0a1b2c3d4e5f60001` | — |
| NAT ゲートウェイ | `nat-0ddd000000000001` | `vpc-0a1b2c3d4e5f60001` | サブネット `subnet-0aaa000000000001` |
| VPC エンドポイント | `vpce-0eee000000000001` | `vpc-0a1b2c3d4e5f60001` | com.amazonaws.ap-northeast-1.s3（Gateway） |

### 外から届くもの

見直しの入り口になるもの。ここに載ることは、誤りを意味しない。意図したものかを所有者が確かめる。

インバウンドを `0.0.0.0/0` か `::/0` に開けているセキュリティグループの規則。

| セキュリティグループ | 名前 | VPC | ポート | 送信元 |
| --- | --- | --- | --- | --- |
| `sg-0aaa1111bbbb2222c` | order-alb | `vpc-0a1b2c3d4e5f60001` | tcp 443 | 0.0.0.0/0 |
| `sg-0aaa1111bbbb2222c` | order-alb | `vpc-0a1b2c3d4e5f60001` | tcp 80 | 0.0.0.0/0 |
| `sg-0ddd3333eeee4444f` | bastion | `vpc-0a1b2c3d4e5f60001` | tcp 22 | 0.0.0.0/0 |

パブリック IP を持つインスタンス、インターネット向けのロードバランサー、公開の設定のデータベース。

| 種類 | ID | アプリケーション | 補足 |
| --- | --- | --- | --- |
| インスタンス | `i-0123456789abcdef1` | — | 203.0.113.10、サブネット `subnet-0aaa000000000001` |
| ロードバランサー | order-alb | order-api | application、order-alb-1234567890.ap-northeast-1.elb.amazonaws.com |

### コンピュートとデータベース

インスタンス。

| インスタンス | 名前 | アプリケーション | 種類 | 状態 | サブネット | パブリック IP |
| --- | --- | --- | --- | --- | --- | --- |
| `i-0123456789abcdef1` | bastion | — | t3.micro | running | `subnet-0aaa000000000001` | 203.0.113.10 |
| `i-0123456789abcdef2` | report-worker | report-batch | m6i.large | stopped | `subnet-0aaa000000000003` | — |

ECS のサービス。

| クラスター | サービス | アプリケーション | 起動の種類 | 希望数 | 実行数 |
| --- | --- | --- | --- | --- | --- |
| prod | order-api | order-api | FARGATE | 2 | 2 |

Lambda の関数。

| 関数 | アプリケーション | ランタイム | メモリ | VPC |
| --- | --- | --- | --- | --- |
| report-export | report-batch | python3.12 | 256 | — |
| report-nightly | report-batch | python3.9 | 512 | `vpc-0a1b2c3d4e5f60001` |
| slack-notify | — | nodejs20.x | 128 | — |

ロードバランサー。

| 名前 | アプリケーション | 種類 | 向き | VPC |
| --- | --- | --- | --- | --- |
| order-alb | order-api | application | インターネット向け | `vpc-0a1b2c3d4e5f60001` |

データベース（RDS）。

| 識別子 | アプリケーション | エンジン | クラス | マルチ AZ | 公開の設定 |
| --- | --- | --- | --- | --- | --- |
| order-db | order-api | postgres 16.4 | db.t4g.medium | いいえ | いいえ |

### すべての種類

種類を問わずに見つけたリソースの数。出どころ: AWS Config、タグ付けの API。取れなかった出どころ: Resource Explorer。
出どころには漏れがある（AWS Config は記録の対象の種類だけ、タグ付けの API はタグを持つか持ったことのあるものだけ、Resource Explorer は索引のあるリージョンで 1000 件まで）。ここに無いことは、無いことの証明にならない。

| 種類 | 数 | 詳しい表 | 出どころ |
| --- | --- | --- | --- |
| `dynamodb:table` | 1 | なし | AWS Config |
| `ec2:instance` | 2 | あり | AWS Config、タグ付けの API |
| `ec2:security-group` | 1 | あり | AWS Config |
| `ec2:volume` | 3 | なし | AWS Config |
| `ecr:repository` | 1 | なし | AWS Config |
| `events:rule` | 1 | なし | タグ付けの API |
| `lambda:function` | 1 | あり | AWS Config |
| `logs:log-group` | 1 | なし | タグ付けの API |
| `rds:db` | 1 | あり | AWS Config |
| `s3` | 2 | なし | AWS Config、タグ付けの API |
| `secretsmanager:secret` | 1 | なし | タグ付けの API |
| `sns` | 1 | なし | AWS Config |
| `sqs` | 1 | なし | AWS Config |

詳しい表が無い種類のリソース。必要なものは、個別に読み取って調べる。

`dynamodb:table`（1 件）

- `arn:aws:dynamodb:ap-northeast-1:111122223333:table/report-state`

`ec2:volume`（3 件）

- `arn:aws:ec2:ap-northeast-1:111122223333:volume/vol-0123456789abcdef1`
- `arn:aws:ec2:ap-northeast-1:111122223333:volume/vol-0123456789abcdef2` アプリケーション: report-batch
- `arn:aws:ec2:ap-northeast-1:111122223333:volume/vol-0123456789abcdef3`

`ecr:repository`（1 件）

- `arn:aws:ecr:ap-northeast-1:111122223333:repository/order-api` アプリケーション: order-api

`events:rule`（1 件）

- `arn:aws:events:ap-northeast-1:111122223333:rule/report-nightly-schedule` アプリケーション: report-batch

`logs:log-group`（1 件）

- `arn:aws:logs:ap-northeast-1:111122223333:log-group:/ecs/order-api` アプリケーション: order-api

`s3`（2 件）

- `arn:aws:s3:::example-old-uploads` タグ: Owner=unknown
- `arn:aws:s3:::example-report-output` アプリケーション: report-batch

`secretsmanager:secret`（1 件）

- `arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:legacy-api-key-AbCdEf` タグ: CreatedBy=unknown

`sns`（1 件）

- `arn:aws:sns:ap-northeast-1:111122223333:alert-notify`

`sqs`（1 件）

- `arn:aws:sqs:ap-northeast-1:111122223333:order-events` アプリケーション: order-api
