# 架空の例: 運用・管理のリポジトリ

`aws-ops` の部品を確かめるための、架空の例。アカウント ID（AWS の文書で使われる例の番号）、リソース、Finding は、すべて作りもので、実在の環境のものではない（ADR-0004）。

| ファイル | 中身 |
| --- | --- |
| `examples/ops-example/ops/apps.json` | アプリケーションの単位の定義。タグ、名前の接頭辞、ARN のパターン、アカウントでの当て方を 1 つずつ含む |
| `examples/ops-example/fixtures/findings.json` | `aws securityhub get-findings` の出力の形をした Finding。対応が要らないもの（抑制済み、準拠、アーカイブ済み）を含む |
| `examples/ops-example/ops/findings/2026-11-01.md` | 上の 2 つから作った、まとめの記録。`make test-findings` が、スクリプトの出力と一致することを確かめる |
| `examples/ops-example/fixtures/inventory/` | `collect.sh` が取得する形をした、1 リージョンの構成 |
| `examples/ops-example/ops/inventory.md` | 上から作った、棚卸しの記録。`make test-inventory` が、スクリプトの出力と一致することを確かめる |

導入先では、取得したままの出力は `ops/raw/` に置いてコミットしない。この例では、確かめるために `fixtures/` に置いている。

記録を作り直す:

```bash
python3 plugins/aws-ops/skills/findings/group_findings.py --apps examples/ops-example/ops/apps.json \
  --date 2026-11-01 --out examples/ops-example/ops/findings/2026-11-01.md \
  examples/ops-example/fixtures/findings.json
```

```bash
python3 plugins/aws-ops/skills/inventory/summarize_inventory.py --raw examples/ops-example/fixtures/inventory \
  --apps examples/ops-example/ops/apps.json --account 111122223333 --date 2026-11-01 \
  --out examples/ops-example/ops/inventory.md
```
