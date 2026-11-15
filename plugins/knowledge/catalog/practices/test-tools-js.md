# JavaScript のテストの道具

Testing Library と Vitest の使い方の判断。テストの書き方の一般の判断は、テストの束にある。 項目の形は `plugins/knowledge/catalog/README.md`。

### 部品は、利用者が見つける手がかりで問い合わせる

| 欄 | 内容 |
| --- | --- |
| ID | `testing-library-queries` |
| 出どころ | Testing Library の文書「About Queries」の「Priority」。https://testing-library.com/docs/queries/about#priority |
| ソース | `testing-library/testing-library-docs:docs/queries/about.mdx@7c49d04` |
| 何を言っているか | テストは利用者の使い方に似せる。問い合わせは、誰でも使える手がかり（役割と名前、ラベル、プレースホルダー、文字、入力の値）、意味の属性（代替の文字、`title`）、テスト用の ID の順に選ぶ。役割と名前でほぼ何でも取れ、取れないなら UI が使いにくい印かもしれない。テスト用の ID は、利用者に見えないので、役割や文字で取れないときだけにする。 |
| 確からしさ | 公式の推奨（道具の作者の指針）。誤用: 取りにくい要素にテスト用の ID を付けて済ませ、UI が読み上げで使えないことに気づかない。 |
| 当たるべき場面 | 画面のテストを書く、レビューするとき。テストのために要素へ属性を足したくなったとき。 |
| 判断の問い | この問い合わせは、上の段の手がかりで書けないか。テスト用の ID を足すなら、役割や文字で取れない理由を言えるか。 |
| 対象 | `@testing-library/react@16` |
| 確認 | 2026-11-15 / 間隔 365 日 |

### Vitest のモックは、何が自動で戻るかを知って戻す

| 欄 | 内容 |
| --- | --- |
| ID | `vitest-mock-restore` |
| 出どころ | Vitest の文書「Mocking」、設定の「clearMocks」「restoreMocks」「unstubGlobals」、「Migrating to Vitest 5.0」。https://vitest.dev/guide/mocking 、https://vitest.dev/config/clearmocks 、https://vitest.dev/guide/migration |
| ソース | `vitest-dev/vitest:docs/guide/mocking.md@cab34bb`, `vitest-dev/vitest:docs/config/clearmocks.md@cab34bb`, `vitest-dev/vitest:docs/config/restoremocks.md@cab34bb`, `vitest-dev/vitest:docs/config/unstubglobals.md@cab34bb`, `vitest-dev/vitest:docs/guide/migration/index.md@cab34bb` |
| 何を言っているか | Vitest 5 から `clearMocks` の既定が有効になり、各テストの前にモックの呼び出しの記録が消える（実装は残る）。テストの外（セットアップのファイル、モジュールの最上位、`beforeAll`）で記録した呼び出しは、確かめる前に消える。`vi.stubGlobal` で替えた大域の値は、`unstubGlobals` を有効にするか `vi.unstubAllGlobals` を呼ぶまで戻らない。`vi.restoreAllMocks` が戻すのは `vi.spyOn` で作ったものだけ。自動で戻す設定は、並行のテストでは、ほかのテストが使っている最中の値も戻す。 |
| 確からしさ | 公式の文書。版で既定が変わった点を含む（5.0 の移行の手引き）。誤用: 古い版の記事に従い、各テストで記録を手で消す後片付けを重ねる。`restoreAllMocks` で `vi.fn` の実装も戻ると思い込む。 |
| 当たるべき場面 | `fetch` やブラウザの API を偽物に替えるテストを書くとき。テストの順序で結果が変わったとき。Vitest の設定の `test` を変えるとき。Vitest の大きな版を上げるとき。 |
| 判断の問い | このテストで替えた値は、次のテストの前に、どの仕組み（既定の設定、`afterEach`、自動の設定）で戻るか。テストの外で記録した呼び出しを、テストの中で確かめていないか。 |
| 対象 | `vitest@5` |
| 確認 | 2026-11-15 / 間隔 180 日 |
