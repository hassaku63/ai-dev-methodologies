# plan の要約

作成 1、変更 2、置き換え 1、削除 2（変更なし 2）。

属性の値は載せない（plan には秘密情報が入りうる）。値は、手元の plan で確かめる。

## 注意して見るもの

置き換えと削除。「データを持つ」は、作り直すと中身や識別子が失われる種類。

| 操作 | リソース | データを持つ | 理由 |
| --- | --- | --- | --- |
| 置き換え | `aws_db_instance.order` | **はい** | この属性は、作り直さないと変えられない。原因の属性: `storage_encrypted` |
| 削除 | `aws_security_group_rule.bastion_ssh` | いいえ | コードから定義が消えた |
| 削除 | `aws_sqs_queue.legacy_events` | **はい** | コードから定義が消えた |

## すべての変更

| 操作 | リソース | 変わる属性 |
| --- | --- | --- |
| 置き換え | `aws_db_instance.order` | `password`、`storage_encrypted` |
| 削除 | `aws_security_group_rule.bastion_ssh` | — |
| 削除 | `aws_sqs_queue.legacy_events` | — |
| 変更 | `aws_ecs_service.order_api` | `desired_count` |
| 変更 | `aws_lambda_function.report_nightly` | `runtime`、`source_code_hash` |
| 作成 | `aws_cloudwatch_metric_alarm.order_5xx` | — |

## コードの外で変わっていたもの

前回の反映のあとに、Terraform の外で変わっていたリソース。この plan は、それを踏まえている。

- `aws_ecs_service.order_api`

## 出力の変更

- `alarm_arn`
