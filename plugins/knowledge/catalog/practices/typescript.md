# TypeScript

TypeScript の型の書き方の判断。 項目の形は `plugins/knowledge/catalog/README.md`。

### 状態を判別共用体で表し、`never` で網羅を確かめる

| 欄 | 内容 |
| --- | --- |
| ID | `ts-discriminated-unions` |
| 出どころ | TypeScript Handbook「Narrowing」の「Discriminated unions」「The never type」「Exhaustiveness checking」。https://www.typescriptlang.org/docs/handbook/2/narrowing.html |
| ソース | `microsoft/TypeScript-Website:packages/documentation/copy/en/handbook-v2/Narrowing.md@4ec663a` |
| 何を言っているか | 共用体のすべての型が、リテラルの型の共通の項目を持つと、その項目で絞り込める。省略できる項目を 1 つの型に並べるより、種別ごとの型の共用体にした方が、型の検査が正しく働く。`switch` の `default` で値を `never` の変数に入れると、種別を足して扱い忘れたときに型の誤りになる。 |
| 確からしさ | 公式の推奨。誤用: 判別の項目を持たない共用体を作り、`in` や型の断定で分岐する。`default` で何もせず返し、種別の追加に気づけなくする。 |
| 当たるべき場面 | API の応答、画面の状態（読み込み中・成功・失敗など）、種別を持つデータの型を書くとき。種別を足す差分をレビューするとき。一般の束の「不正な状態を表せない形にする」の TypeScript での書き方。 |
| 判断の問い | 種別によってある・ないが決まる項目を、省略できる項目として 1 つの型に並べていないか。種別ごとの分岐は、種別を足したときに型の誤りになるか。 |
| 対象 | `typescript@5` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### インデックスの読み出しと、省略した項目を、`undefined` と区別する

| 欄 | 内容 |
| --- | --- |
| ID | `ts-index-and-optional-undefined` |
| 出どころ | TSConfig Reference「noUncheckedIndexedAccess」「exactOptionalPropertyTypes」。https://www.typescriptlang.org/tsconfig/#noUncheckedIndexedAccess 、https://www.typescriptlang.org/tsconfig/#exactOptionalPropertyTypes |
| ソース | `microsoft/TypeScript-Website:packages/tsconfig-reference/copy/en/options/noUncheckedIndexedAccess.md@4ec663a`, `microsoft/TypeScript-Website:packages/tsconfig-reference/copy/en/options/exactOptionalPropertyTypes.md@4ec663a` |
| 何を言っているか | `noUncheckedIndexedAccess` は、インデックスシグネチャで読んだ、宣言していない項目の型に `undefined` を足す。`exactOptionalPropertyTypes` は、`?` の付いた項目に `undefined` を入れることを許さない。項目に `undefined` が入っていることと、項目がないことは違う（`in` の結果が変わる）ためで、「ない」は項目を置かないことで表す。 |
| 確からしさ | 公式の文書（設定の意味の説明）。誤用: 足された `undefined` を、確かめずに断定で消す。「ない」を表すために `undefined` を代入し、型を `undefined` との共用体に広げて検査を黙らせる。 |
| 当たるべき場面 | 配列や辞書から値を読む処理を書くとき。省略できる項目を持つ型（API の応答、設定）を書くとき。`?` の項目に `undefined` を入れようとして型の誤りが出たとき。 |
| 判断の問い | 読み出しの `undefined` を、絞り込みで扱っているか（断定で消していないか）。省略できる項目を「ない」にするとき、項目を置かない形で書いているか。 |
| 対象 | `typescript@5` |
| 確認 | 2026-11-15 / 間隔 180 日 |
