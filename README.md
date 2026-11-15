# ai-dev-methodologies

個人や業務のコードベースやインフラ（主にAWS）を開発・運用・保守するにあたって、ある程度ばらつきがあるそれぞれのレポジトリに対して、そのレポジトリで扱う内容に合わせて選択的にAI活用の枠組みを導入できるようにする。

このレポジトリは、そのメタフレームワークとして必要な仕組みや、知識のインデックスを配置しておく場所である。

## 持つもの

- 導入先に配る部品（Claude Code の plugin、導入時にコピーするファイル、雛形）
- 部品を選ぶ・導入する・更新する仕組み
- 公開してよい一般的な知識の索引

配れる部品は次の plugin。進み具合は `docs/roadmap.md`。

| plugin | 対象 | 中身 |
| --- | --- | --- |
| `core` | すべての導入先 | 導入、Issue の流れ、実装とレビューのサブエージェント、文書の鮮度 |
| `aws-ops` | AWS のインフラを調べて記録するリポジトリ | エージェントの AWS の操作を読み取りに限るフック。Security Hub の Finding を、アプリケーションの単位でまとめる手順（`/aws-ops:findings`）。ネットワークとコンピュートの構成の棚卸し（`/aws-ops:inventory`） |
| `aws-iac` | Terraform や CDK で AWS のインフラを管理するリポジトリ | エージェントの操作を、変更の計画（plan、diff、synth）までに限るフック。変更の計画を、置き換えと削除が目立つ形でまとめる手順（`/aws-iac:plan`）。インフラのコードの検査 |

## 導入先での使い方

導入先のリポジトリで、マーケットプレイスを登録して `core` を入れる。

```bash
claude plugin marketplace add hassaku63/ai-dev-methodologies --scope project
```

```bash
claude plugin install core@ai-dev-methodologies --scope project
```

Claude Code のセッションで `/core:adopt` を実行すると、検査のスクリプトと雛形を置き、指示書と文書をそのリポジトリの内容で埋める。導入先が守る規約は `docs/contract.md`。

AWS のインフラを調べて記録するリポジトリでは、続けて `aws-ops` を入れ、`/aws-ops:adopt` を実行する。記録の置き場所（`ops/`）ができる。

```bash
claude plugin install aws-ops@ai-dev-methodologies --scope project
```

Terraform や CDK のリポジトリでは、`aws-iac` を入れ、`/aws-iac:adopt` を実行する。インフラのコードの検査が `make check` に入る。

```bash
claude plugin install aws-iac@ai-dev-methodologies --scope project
```

## 読む順

1. `docs/concept.md`: 何を解決するか、導入先の種類、配り方
2. `docs/roadmap.md`: 段階と現在地
3. `docs/contract.md`: 導入先が守る規約と、配るファイル
4. `docs/architecture/adr/README.md`: 決定の記録
5. `AGENTS.md`: このリポジトリで作業するときの規則

## 置かないもの

会社や組織に固有の規則・構成・識別子は置かない（ADR-0004）。このリポジトリは公開されている。
