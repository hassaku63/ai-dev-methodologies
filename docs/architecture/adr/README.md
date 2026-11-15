# ADR の索引

決定の記録。1 つの決定に 1 枚。書き方は [0000-template.md](0000-template.md)。決定を変えるときは、新しい ADR を足し、古い方の状態を Superseded にする。

| 番号 | 決定 |
| --- | --- |
| [0001](0001-record-architecture-decisions.md) | 決定を ADR に記録する |
| [0002](0002-personal-marketplace.md) | このリポジトリを個人用のマーケットプレイスにする |
| [0003](0003-three-kinds-of-deliverables.md) | 配るものを 3 種類に分ける |
| [0004](0004-no-organisation-specific-content.md) | 会社や組織に固有の情報を置かない |
| [0005](0005-autonomy-levels.md) | 任せる範囲を段階で選び、本番への反映は人間が行う |
| [0006](0006-claude-code-first-agents-md-canon.md) | Claude Code を既定にし、規則の正典は `AGENTS.md` に置く |
| [0007](0007-managed-files-update-by-hash.md) | コピーしたファイルは、ハッシュで手直しを見分けて更新する |
| [0008](0008-contract-and-self-adoption.md) | 導入先が守る規約を 1 つの文書に持ち、このリポジトリ自身にも導入する |
| [0009](0009-aws-read-only-guard.md) | 運用・管理のリポジトリでは、フックで AWS の操作を読み取りに限る |
