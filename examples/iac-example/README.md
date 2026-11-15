# 架空の例: IaC のリポジトリ

`aws-iac` の部品を確かめるための、架空の例。リソース、アカウント ID（AWS の文書で使われる例の番号）、plan は、すべて作りもので、実在の環境のものではない（ADR-0004）。

| ファイル | 中身 |
| --- | --- |
| `examples/iac-example/fixtures/plan.json` | `terraform show -json` の出力の形をした plan。置き換え、削除、変更、作成、変更なし、データソース、コードの外での変更を含む。秘密情報に見立てた値を含む |
| `examples/iac-example/plan-summary.md` | 上から作った要約。`make test-plan` が、スクリプトの出力と一致することと、値が載っていないことを確かめる |

要約を作り直す:

```bash
python3 plugins/aws-iac/skills/plan/summarize_plan.py --out examples/iac-example/plan-summary.md \
  examples/iac-example/fixtures/plan.json
```
