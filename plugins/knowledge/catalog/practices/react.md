# React

React の部品と hook の判断。画面の設計の判断は、HCI の束にある。 項目の形は `plugins/knowledge/catalog/README.md`。

### 描画から導ける値とイベントの処理に、Effect を使わない

| 欄 | 内容 |
| --- | --- |
| ID | `react-you-might-not-need-an-effect` |
| 出どころ | React の文書「You Might Not Need an Effect」。https://react.dev/learn/you-might-not-need-an-effect |
| ソース | `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md@46a54e0` |
| 何を言っているか | Effect は外の仕組みと同期するためのもの。props や状態から計算できる値は、描画の中で計算する（重ければ `useMemo`）。props が変わったら全体を初期化したいなら `key` を変える。利用者の操作で起きる処理はイベントの処理に書き、表示されたことが理由で動く処理だけを Effect に置く。複数の部品の状態を同期したくなったら、状態を持ち上げる。 |
| 確からしさ | 公式の推奨。React Compiler を使えば手書きの `useMemo` が要らない場合が多い、とも書く。誤用: 状態を別の状態に写す Effect を書き、描画が 1 回余計に走る。Effect の連鎖で計算を進める。 |
| 当たるべき場面 | 部品か hook に `useEffect` を足す差分を書く、レビューするとき。状態や props から導く値の置き場所を決めるとき。 |
| 判断の問い | この Effect は、どの外の仕組み（通信、タイマー、保存、ブラウザの API）と同期しているか。答えられないなら、描画の中の計算かイベントの処理にできないか。状態から計算できる値を、別の状態として持っていないか。 |
| 対象 | `react@19` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### Effect での通信は、後片付けで古い応答を捨てる

| 欄 | 内容 |
| --- | --- |
| ID | `react-effect-fetch-cleanup` |
| 出どころ | React の文書「Synchronizing with Effects」の「Fetching data」。https://react.dev/learn/synchronizing-with-effects 。同「You Might Not Need an Effect」の「Fetching data」。https://react.dev/learn/you-might-not-need-an-effect |
| ソース | `reactjs/react.dev:src/content/learn/synchronizing-with-effects.md@46a54e0`, `reactjs/react.dev:src/content/learn/you-might-not-need-an-effect.md@46a54e0` |
| 何を言っているか | 依存の値が変わるたびに通信すると、応答の順序は保証されず、古い応答が新しい結果を上書きする。Effect の後片付けで、通信を取り消すか結果を無視する。開発の Strict Mode は部品を 2 回取り付けるので通信が 2 回見えるが、後片付けがあれば結果は変わらない。Effect での通信には、キャッシュがない、親から子へ順に待つ、などの弱点がある。フレームワークの仕組みかキャッシュのライブラリを勧め、自前で続けるなら専用の hook に閉じ込めると後で替えやすい、と書く。 |
| 確からしさ | 公式の推奨。Effect での通信を続けてもよいと明記している。誤用: 2 回の通信を止めるために ref で 1 回だけ走らせる（文書が名指しで避けるよう書いている）。後片付けのない通信の Effect。 |
| 当たるべき場面 | 画面から API を呼ぶ hook を書く、レビューするとき。入力に追随して結果を取り直す画面を作るとき。通信のライブラリ（依存）を足すか検討するとき。 |
| 判断の問い | この Effect は、依存の値が速く変わったとき、最後の応答だけを反映するか。後片付けで取り消すか無視しているか。同じ通信を複数の部品が別々にしていないか。 |
| 対象 | `react@19` |
| 確認 | 2026-11-15 / 間隔 180 日 |

### 状態は、重複させず、持つ部品を 1 つに決める

| 欄 | 内容 |
| --- | --- |
| ID | `react-state-single-owner` |
| 出どころ | React の文書「Choosing the State Structure」。https://react.dev/learn/choosing-the-state-structure 。同「Sharing State Between Components」。https://react.dev/learn/sharing-state-between-components |
| ソース | `reactjs/react.dev:src/content/learn/choosing-the-state-structure.md@46a54e0`, `reactjs/react.dev:src/content/learn/sharing-state-between-components.md@46a54e0` |
| 何を言っているか | いつも一緒に変わる状態は 1 つにまとめる。あり得ない組み合わせを作らない。計算できる値や重複した値を状態に持たない。props を状態に写さない（更新を止めたいときを除く）。選択はものそのものではなく ID か位置で持つ。深い入れ子は平らにする。2 つの部品をそろえたいときは、状態を共通の親に移し、props とイベントの処理を下に渡す。状態ごとに、持つ部品を 1 つに決める。 |
| 確からしさ | 公式の推奨。作りながら状態を上げ下げするのは普通のことだ、とも書く。誤用: すべての状態を最上位に集める（各状態の持ち主を 1 つに決めることは、1 か所に集めることではない）。 |
| 当たるべき場面 | 画面の状態の形と置き場所を決めるとき。2 つの機能の部品が同じ値を見たくなったとき。 |
| 判断の問い | この状態は、ほかの状態か props から計算できないか。同じものを 2 か所に持っていないか。選んだものを、ものそのものの写しで持っていないか。 |
| 対象 | `react@19` |
| 確認 | 2026-11-15 / 間隔 365 日 |
