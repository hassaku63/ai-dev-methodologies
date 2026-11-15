# chord-rambler と middy を、目録を使う形に移す

`hassaku63/chord-rambler` と `hassaku63/middy` は、プラクティスと業界標準（middy は HCI も）の索引を、それぞれのリポジトリに全欄で持っている。そのうちどこでも使える項目は、plugin `knowledge` の目録に移した（ADR-0011、hassaku63/ai-dev-methodologies#13）。両リポジトリを、目録と対応表を使う形に移す手順。

移す作業は、それぞれのリポジトリのセッションで行う。このリポジトリからは両リポジトリを変えない。

## 移したあとの形

| もの | 移す前 | 移したあと |
| --- | --- | --- |
| どこでも使える項目の本体（出どころ、要点、判断の問い、対象、確認） | リポジトリの `index.md` | plugin `knowledge` の目録 |
| そのリポジトリでの場面、立場、接点 | 同じ項目の欄 | リポジトリの対応表（`<導入先>/docs/knowledge/practices.md`、`<導入先>/docs/knowledge/standards.md`） |
| そのリポジトリにだけ当てはまる項目（音楽の知見など） | リポジトリの `index.md` | 対応表の「このリポジトリの項目」か、今の索引のまま（下の手順 5） |
| 項目の形と版の検査 | `<導入先>/scripts/check-practices.sh`、`<導入先>/scripts/check-standards.sh` | `<導入先>/scripts/check-knowledge.py`（`make knowledge-check`） |
| 出どころの鮮度の報告 | リポジトリの月次のワークフロー | 目録の項目は ai-dev-methodologies の月次の報告。リポジトリにだけある項目は、リポジトリに残す |

## 手順

それぞれのリポジトリで、作業用のブランチを切ってから行う。

1. **plugin を入れる。** リポジトリの最上位で実行する。

   ```bash
   claude plugin install knowledge@ai-dev-methodologies --scope project
   ```

   マーケットプレイスをまだ登録していなければ、先に登録する。

   ```bash
   claude plugin marketplace add hassaku63/ai-dev-methodologies --scope project
   ```

2. **新しいセッションで、下の「移すセッションに貼るプロンプト」を貼る。** `/knowledge:adopt` の手順に、移すための手順を足したもの。
3. **出てきた PR を読む。** 特に、対応表の「このリポジトリでの場面」と「このプロジェクトの立場」が、元の索引の欄から正しく移っているか。
4. **ADR を足す。** 元の索引の形を決めた ADR（chord-rambler の ADR-0007 と ADR-0015）を Superseded にする新しい ADR を、そのリポジトリに足す。何を目録に移し、何を残したかを書く。
5. **リポジトリにだけある項目の置き場所を決める。** 次のどちらか。
   - 対応表の「このリポジトリの項目」に移す。検査は形だけを見る（見直しの期限は見ない）。
   - 今の索引のまま残し、今の検査と月次の報告を、その項目だけに向ける。期限と出どころの移動を、引き続き機械で見られる。

   項目が多く、鮮度を機械で見たいなら後者を勧める。
6. **マージする。** 検査、CI、ADR を変える PR なので、所有者が見てマージする。

## 目録の項目と、元の索引の見出し

目録の項目の見出しは、元の索引の見出しと同じ。対応表には ID を書く。

| 見出し | ID | 目録の束 | 元の索引 |
| --- | --- | --- | --- |
| 段階ごとに、強いモデルを要所で使う | `advisor-at-decision-points` | `practices/agent-workflow.md` | chord-rambler の practices |
| 検査の結果を型で返し、境界で一度だけ行う | `parse-dont-validate` | `practices/general.md` | chord-rambler の practices |
| 不正な状態を表せない形にする | `illegal-states-unrepresentable` | `practices/general.md` | chord-rambler の practices |
| 純粋な計算を、副作用で挟む | `impureim-sandwich` | `practices/general.md` | chord-rambler の practices |
| 見込みの機能を作らない | `yagni` | `practices/general.md` | chord-rambler の practices |
| 誤った抽象は戻す | `wrong-abstraction` | `practices/general.md` | chord-rambler の practices |
| 単純な設計の 4 つの規則 | `beck-design-rules` | `practices/general.md` | chord-rambler の practices |
| 小さな変更にし、構造と振る舞いを分ける | `small-changes` | `practices/general.md` | chord-rambler の practices |
| レビューで見るもの | `what-to-look-for-in-review` | `practices/general.md` | chord-rambler の practices |
| エラーを包むかは API として決め、比べるときは木をたどる | `go-error-wrapping` | `practices/go.md` | chord-rambler の practices |
| テーブル駆動のテストを、名前つきのサブテストで回す | `go-table-driven-subtests` | `practices/go.md` | chord-rambler の practices |
| `log/slog` の属性は、書き方をそろえ、共通のものは `With` で付ける | `go-slog-attributes` | `practices/go.md` | chord-rambler の practices |
| インタフェースは使う側に、使われてから置く | `go-interfaces-at-consumer` | `practices/go.md` | chord-rambler の practices |
| ゲシュタルトの群化（近接・類同・共通領域・共通運命・連結） | `gestalt-grouping` | `practices/hci.md` | middy の hci |
| 分割注意と近接（説明は対象の隣に、同じ時間に） | `split-attention-contiguity` | `practices/hci.md` | middy の hci |
| 概観+詳細、ズーム、焦点+文脈 | `overview-detail-focus-context` | `practices/hci.md` | middy の hci |
| 記憶に頼らせない: 作業記憶の容量、外部記憶、認識 > 想起 | `recognition-over-recall` | `practices/hci.md` | middy の hci |
| 行長と読みやすさ | `line-length-readability` | `practices/hci.md` | middy の hci |
| 強調と手がかり: 前注意的特徴、シグナリング、同期ハイライトの限界 | `preattentive-signaling` | `practices/hci.md` | middy の hci |
| 画面幅のクラスと配置の切り替え | `window-size-classes` | `practices/hci.md` | middy の hci |
| 流れて消える情報: 一過性情報効果と WCAG 2.2.1 / 2.2.2 | `transient-information` | `practices/hci.md` | middy の hci |
| 分節化と学習者ペース（止められるだけでは足りない） | `segmenting-learner-pace` | `practices/hci.md` | middy の hci |
| 読みの速さと字幕の基準 | `reading-speed-captions` | `practices/hci.md` | middy の hci |
| 注意の捕捉と見落とし（出現・動き始め、変化の見落とし、選択的注意） | `attention-capture-change-blindness` | `practices/hci.md` | middy の hci |
| 動きと「動きを減らす」設定 | `motion-and-reduced-motion` | `practices/hci.md` | middy の hci |
| モードとモードエラー、準モード（quasimode） | `modes-and-quasimodes` | `practices/hci.md` | middy の hci |
| 実行の淵と評価の淵、7 段階の行為 | `gulfs-of-execution-evaluation` | `practices/hci.md` | middy の hci |
| 概念モデル、システムイメージ、自然な対応づけ、制約 | `conceptual-models-mapping` | `practices/hci.md` | middy の hci |
| 直接操作と委任（会話型 AI の UI、明示の壁、狭いスコープ） | `direct-manipulation-delegation` | `practices/hci.md` | middy の hci |
| ヒューリスティクス（Nielsen の 10 と、Shneiderman の黄金律の独自 2 点） | `usability-heuristics` | `practices/hci.md` | middy の hci |
| アフォーダンス（Gibson）とシグニファイア（Norman） | `affordances-signifiers` | `practices/hci.md` | middy の hci |
| フラット UI とクリック可能性の手がかり | `flat-ui-clickability` | `practices/hci.md` | middy の hci |
| Fitts の法則とタッチターゲットの大きさ・間隔 | `fitts-target-size` | `practices/hci.md` | middy の hci |
| オブジェクト指向 UI（OOUI / OOUX） | `object-oriented-ui` | `practices/hci.md` | middy の hci |
| 段階的開示 | `progressive-disclosure` | `practices/hci.md` | middy の hci |
| 選択過多（再現性に注意）と既定値の力 | `choice-overload-defaults` | `practices/hci.md` | middy の hci |
| 応答時間のしきい値（0.1 / 1 / 10 秒）と進捗表示の形 | `response-time-limits` | `practices/hci.md` | middy の hci |
| 認知負荷理論（内在・外在）と一貫性（関係のない情報は削る） | `cognitive-load-coherence` | `practices/hci.md` | middy の hci |
| 色だけに頼らない（WCAG 1.4.1） | `color-not-sole-means` | `practices/hci.md` | middy の hci |
| コントラスト: 文字（1.4.3）と文字以外（1.4.11）、WCAG 3 / APCA の位置づけ | `contrast-wcag` | `practices/hci.md` | middy の hci |
| 色覚多様性とカテゴリ色: Okabe–Ito の Color Universal Design | `color-universal-design` | `practices/hci.md` | middy の hci |
| 知覚的に均一な色空間でトークンを作る（CIELAB / Oklab / OKLCH） | `perceptual-color-spaces` | `practices/hci.md` | middy の hci |
| ダークモードとコントラスト極性 | `dark-mode-polarity` | `practices/hci.md` | middy の hci |
| WAI-ARIA Authoring Practices: ツールバー、リストボックス／グリッド、スライダー | `aria-authoring-practices` | `practices/hci.md` | middy の hci |
| ライブリージョンと状態メッセージ（うるさい読み上げの危険） | `live-regions-status` | `practices/hci.md` | middy の hci |
| 描画から導ける値とイベントの処理に、Effect を使わない | `react-you-might-not-need-an-effect` | `practices/react.md` | chord-rambler の practices |
| Effect での通信は、後片付けで古い応答を捨てる | `react-effect-fetch-cleanup` | `practices/react.md` | chord-rambler の practices |
| 状態は、重複させず、持つ部品を 1 つに決める | `react-state-single-owner` | `practices/react.md` | chord-rambler の practices |
| 部品は、利用者が見つける手がかりで問い合わせる | `testing-library-queries` | `practices/test-tools-js.md` | chord-rambler の practices |
| Vitest のモックは、何が自動で戻るかを知って戻す | `vitest-mock-restore` | `practices/test-tools-js.md` | chord-rambler の practices |
| テストに求める性質は釣り合いで決める | `test-desiderata` | `practices/testing.md` | chord-rambler の practices |
| 振る舞いを公開の入口から、状態で確かめる | `test-via-public-api` | `practices/testing.md` | chord-rambler の practices |
| テストは読んで正しいと分かるように書く | `test-clear-and-complete` | `practices/testing.md` | chord-rambler の practices |
| 依存は本物を優先し、代役は fake、stub、呼び出しの検証の順に選ぶ | `test-doubles-prefer-real` | `practices/testing.md` | chord-rambler の practices |
| テストの大きさを制約で決め、小さいものを既定にする | `test-size-small-first` | `practices/testing.md` | chord-rambler の practices |
| 事例をデータの表にする | `table-driven-tests` | `practices/testing.md` | chord-rambler の practices |
| 例ではなく性質で試す | `property-based-tests` | `practices/testing.md` | chord-rambler の practices |
| 状態を判別共用体で表し、`never` で網羅を確かめる | `ts-discriminated-unions` | `practices/typescript.md` | chord-rambler の practices |
| インデックスの読み出しと、省略した項目を、`undefined` と区別する | `ts-index-and-optional-undefined` | `practices/typescript.md` | chord-rambler の practices |
| Dockerfile（BuildKit の Dockerfile フロントエンドの構文） | `dockerfile-syntax` | `standards/containers.md` | chord-rambler の standards / middy の standards |
| Build checks（BuildKit の組み込みの検査） | `buildkit-build-checks` | `standards/containers.md` | chord-rambler の standards / middy の standards |
| Compose Specification | `compose-spec` | `standards/containers.md` | chord-rambler の standards / middy の standards |

middy の HCI の索引のうち、次の 3 項目は目録に無い（middy で出どころを開けていなかったため。`plugins/knowledge/catalog/practices/hci.md` の「外したもの」）。middy に残す。

- Hick–Hyman の法則と、その誤用
- 望ましい困難と「学習と成績の乖離」
- 熟達の逆転効果（初心者に効く支援が、経験者には邪魔になる）

## 移すセッションに貼るプロンプト

次の枠の中を、そのまま貼る。

````text
このリポジトリのプラクティスと業界標準の索引（あれば HCI の索引も）を、ai-dev-methodologies の plugin knowledge の目録と、このリポジトリの対応表を使う形に移したい。手順は ai-dev-methodologies の docs/migration-to-catalog.md にある（https://github.com/hassaku63/ai-dev-methodologies/blob/main/docs/migration-to-catalog.md ）。読めなければ、私に内容を尋ねて。

次の順で進めて。作業用のブランチで行い、PR は開くかどうかを私に確かめてから開く。

1. スキル /knowledge:adopt の手順で、対応表と検査を置く。ただし、使う項目は手順 2 の対応で決めるので、束の行をまとめて貼らない。
2. 今の索引（.claude/skills/ の practices、standards、hci の index.md）の項目を 1 つずつ見て、次の 3 つに分ける。分けた結果を表にして、私に見せる。
   - 目録にある（見出しが、docs/migration-to-catalog.md の表にある）: 対応表の「使う項目」に ID を書く。元の項目の「当たるべき場面」のうち、このリポジトリに固有の部分を「このリポジトリでの場面」に、「このプロジェクトの立場」をそのまま「このプロジェクトの立場」に移す。業界標準は、元の「（リポジトリ名）との接点」を「このリポジトリとの接点」に移す。HCI は、「適切・不適切な例」と「（リポジトリ名）との接点」を、短くして「このリポジトリでの場面」に移す。
   - 目録に無く、このリポジトリにだけ当てはまる: docs/migration-to-catalog.md の手順 5 のどちらにするか、私に尋ねる。
   - 目録に無いが、どこでも使えそうな知見: ai-dev-methodologies の目録に足す提案として、項目名と出どころを一覧にする。このリポジトリでは、今の索引に残す。
3. 元の索引から、目録に移した項目を消す。「外したもの」の節は残す。
4. 消した項目だけを見ていた検査や手順（scripts/check-practices.sh、scripts/check-standards.sh、月次の鮮度の報告、docs/dev/knowledge-review.md、AGENTS.md と PR テンプレートの索引への言及）を、残る項目と対応表に合わせて直す。検査を弱めて通さない。残る項目が無くなった検査は、消す案を私に示す。
5. 元の索引の形を決めた ADR を Superseded にする ADR の下書きを書く。
6. make check を通す。
7. 次を報告する: 移した項目の数、残した項目の数、目録に足す提案、直した検査と手順、私が決めること。

守ること:
- 「このプロジェクトの立場」を推測で書き換えない。元の欄をそのまま移す。
- 目録の項目の中身を、このリポジトリで書き換えない。直すべきなら、ai-dev-methodologies への提案として書く。
- 元の索引の項目を、対応表に移す前に消さない。

