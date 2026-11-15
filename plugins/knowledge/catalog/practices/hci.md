# HCI: 画面と操作の設計

画面を持つアプリケーション（Web、モバイル）の、画面・操作・フィードバック・配置・色を決めるときの知見。HCI、認知心理学、インタラクションデザイン、アクセシビリティ。項目の形は `plugins/knowledge/catalog/README.md`。

数値（秒、文字数、px、比）を根拠に使うときは、その項目の出どころを開いてから使う。確からしさに「再現性に議論」「実務の経験則」とあるものは、数値ではなく向き（大きいほど／短いほど）だけを使う。

## 何を同時に見せるか（群化・近接・全体と部分）

### ゲシュタルトの群化（近接・類同・共通領域・共通運命・連結）

| 欄 | 内容 |
| --- | --- |
| ID | `gestalt-grouping` |
| 出どころ | Wertheimer (1923) 原典。総説: Wagemans, J. et al. (2012) A century of Gestalt psychology in visual perception: I. *Psychological Bulletin* 138(6). https://doi.org/10.1037/a0029333 。共通領域の原典: Palmer, S. E. (1992) *Cognitive Psychology* 24。解説: NN/g の Proximity https://www.nngroup.com/articles/gestalt-proximity/ 、Similarity https://www.nngroup.com/articles/gestalt-similarity/ 、Common Region https://www.nngroup.com/articles/common-region/ |
| ソース | なし |
| 何を言っているか | 近い・似ている・同じ枠の中にある・同じ向きに動く・線でつながった要素は、ひとまとまりとして知覚される。原理どうしが競合するとき、近接と共通領域は類同（色・形）より強いことが多く、類同は離れた要素を結べる点で粘り強い。余白・枠・色は「どれが何に属するか」を言葉なしで伝える手段で、使いすぎると枠だらけで構造が消える |
| 確からしさ | 100 年分の実験で原理の存在は安定（Wagemans らの総説）。「どの原理が勝つか」は刺激次第で、定量予測は限定的。NN/g は近接・共通領域が類同を上回る、と実務の観察で言う。 確かめた範囲（middy での確認）: NN/g の 3 記事。Wagemans 2012 と Palmer 1992 の原論文は未確認・網の方針外 |
| 当たるべき場面 | 画面の要素を「どれが何に属するか」目で分からせたいとき。余白・枠・色で群を作るとき。連動して動く要素を決めるとき（共通運命）。 |
| 判断の問い | 見た目の近さ・枠・動きが、意味の所属（どの対象の説明か、どの群に属するか）と一致しているか。意図しない群化（主操作が従属操作と同じ間隔・重さで並ぶ）が起きていないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 分割注意と近接（説明は対象の隣に、同じ時間に）

| 欄 | 内容 |
| --- | --- |
| ID | `split-attention-contiguity` |
| 出どころ | Chandler, P. & Sweller, J. (1992) The split-attention effect as a factor in the design of instruction. *British Journal of Educational Psychology* 62。Ginns, P. (2006) Integrating information: A meta-analysis of the spatial contiguity and temporal contiguity effects. *Learning and Instruction* 16. https://doi.org/10.1016/j.learninstruc.2006.10.001 。Mayer, R. E. (2021) *Multimedia Learning* 3rd ed., Cambridge UP。実務の観察: Nielsen, J. (2012) Tunnel Vision and Selective Attention, NN/g https://www.nngroup.com/articles/tunnel-vision-and-selective-attention/ |
| ソース | なし |
| 何を言っているか | 互いに参照しないと理解できない情報（図と説明、対象とその理由）が離れた場所・離れた時刻にあると、探して結びつける負荷がかかり学習が落ちる。近づける（統合する）と、内容が複雑なときほど改善が大きい。NN/g は実験でなく観察から同じ結論に至る: ユーザーは今見ている領域の外をほとんど見ないので、関係するものは隣に置く |
| 確からしさ | メタ分析が複数あり、効果の向きは安定。大きさは材料の複雑さと学習者の知識で変わる。「同じ時間に」は「同じ時間に消える」を含まない点に注意（→ 2 節「流れて消える情報」）。 確かめた範囲（middy での確認）: NN/g の記事。Ginns 2006、Chandler & Sweller 1992、Mayer の本は未確認・網の方針外 |
| 当たるべき場面 | 説明やラベルをどこに置くか決めるとき。横並びと縦積みで、対象と説明の距離が変わるとき。狭い画面で説明が画面の外に出るとき。 |
| 判断の問い | 対象と説明の間に、視線の移動か、スクロールか、時間差があるか。それは内容の理解に必要な往復か。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 概観+詳細、ズーム、焦点+文脈

| 欄 | 内容 |
| --- | --- |
| ID | `overview-detail-focus-context` |
| 出どころ | Cockburn, A., Karlson, A. & Bederson, B. B. (2008) A Review of Overview+Detail, Zooming, and Focus+Context Interfaces. *ACM Computing Surveys* 41(1). DOI 10.1145/1456650.1456652。著者公開 PDF: https://www.microsoft.com/en-us/research/wp-content/uploads/2008/01/cockburn-ComputingSurveys09.pdf 。Shneiderman (1996) The Eyes Have It（概観が先、ズームと絞り込み、詳細は求めに応じて）。Furnas (1986) Generalized Fisheye Views, *CHI '86* |
| ソース | なし |
| 何を言っているか | 全体と部分を同時に扱う手法は 4 つ: 概観+詳細（空間で分ける）、ズーム（時間で分ける）、焦点+文脈（1 つの表示に埋め込む）、手がかり（強調・抑制）。レビューの結論: 概観+詳細は文書理解の課題で最も強く好まれるが、2 つの表示を頭の中で結びつける注意の分割がコストで、動的な作業では不利になりうる。ズームはアニメーションなしだと迷う。歪みを使う焦点+文脈は空間判断とクリック精度を損ねる。詳細の変化は概観に即時に反映し、概観を触っても詳細は動かないのが慣例 |
| 確からしさ | 多数の実験の系統的レビュー。「どれが最良か」は課題次第で、一般的な指針は出せないと著者ら自身が明言。 確かめた範囲（middy での確認）: Cockburn らの全文。Shneiderman 1996 と Furnas 1986 は未確認・IEEE/ACM と著者ページが開けず |
| 当たるべき場面 | 長い一覧や時系列、大きな図の見せ方を決めるとき。全体（文脈）と今の部分（焦点）を並べるか切り替えるか決めるとき。縮小図と拡大を足すとき。 |
| 判断の問い | 焦点と文脈を同時に見せる必要がある作業か、切り替えでよいか。2 つの表示を見比べるコスト（視線の往復）は、作業の速さに間に合うか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 記憶に頼らせない: 作業記憶の容量、外部記憶、認識 > 想起

| 欄 | 内容 |
| --- | --- |
| ID | `recognition-over-recall` |
| 出どころ | Miller, G. A. (1956) The magical number seven, plus or minus two. *Psychological Review* 63。Cowan, N. (2001) The magical number 4 in short-term memory. *Behavioral and Brain Sciences* 24(1). https://doi.org/10.1017/S0140525X01003922 。Baddeley & Hitch (1974) の作業記憶。Nielsen, J. (2009) Short-Term Memory and Web Usability https://www.nngroup.com/articles/short-term-memory-and-web-usability/ 。Budiu, R. (2018) Working Memory and External Memory https://www.nngroup.com/articles/working-memory-external-memory/ 。Budiu, R. (2024) Memory Recognition and Recall in User Interfaces https://www.nngroup.com/articles/recognition-and-recall/ 。W3C WAI (2021) Making Content Usable for People with Cognitive and Learning Disabilities https://www.w3.org/TR/coga-usable/ |
| ソース | なし |
| 何を言っているか | 見えなくなった情報を頭の中で保持できる量は小さく、数秒〜20 秒ほどで薄れる。容量の数字は資料で違う（NN/g は「約 7 チャンク」、W3C COGA は平均 7・障害があれば 1〜3、Cowan はリハーサルを封じると 3〜5）が、設計への含意は同じ: 保持させず、画面に出しておく（外部記憶）。候補が見えていれば選べるが、手がかりなしに思い出すのは難しい（認識 > 想起）。NN/g は「メニューは 7 個まで」を誤解だと明記している。画面に並ぶものは見えているので記憶の容量は直接は当たらない |
| 確からしさ | 容量の存在と個人差（年齢・教育で大きく違う）は安定。正確な数とその原因（減衰か干渉か）は論争。**よくある誤用:** 7±2 や 4 を「項目数の上限」に使う。当たるのは、見えなくなった情報を保持させる場面だけ。 確かめた範囲（middy での確認）: NN/g の 3 記事と W3C COGA。Miller 1956、Cowan 2001 の原論文は未確認・網の方針外 |
| 当たるべき場面 | ユーザーに「覚えておいて、あとで照合する」ことを求めていないかの点検（流れていった前の表示と今のを比べる、記法を覚えて入力する）。空の画面の入力例。長い一覧で途中が流れる懸念。 |
| 判断の問い | この画面で、ユーザーが見えないものを何個保持しなければ目的を果たせないか。それを画面に出しておけば保持は不要になるか。この操作は見えているものを選ぶ形か、記法や前の状態を思い出す形か。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 行長と読みやすさ

| 欄 | 内容 |
| --- | --- |
| ID | `line-length-readability` |
| 出どころ | W3C WCAG 2.2 SC 1.4.8 Visual Presentation (AAA) と Understanding https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html 。Dyson, M. C. & Haselgrove, M. (2001) The influence of reading speed and line length on the effectiveness of reading from screen. *IJHCS* 54(4). https://doi.org/10.1006/ijhc.2001.0458 。Dyson (2004) *Behaviour & IT* 23(6)（総説） |
| ソース | なし |
| 何を言っているか | WCAG 1.4.8 は、1 行を 80 字以内（CJK は 40 字以内）にできる仕組み、両端揃えにしない、行間 1.5 倍以上、200% 拡大で横スクロールなし、を挙げる。Understanding は、行が長いと次の行の頭に戻りにくい読者がいること、CJK の 1 字は欧文の約 2 字幅に当たることを根拠に書く。Dyson らの画面実験では 55 字（英数）前後で理解の成績が最良で、55〜100 字で読む速さに差がなかったとされる（原論文は未確認） |
| 確からしさ | WCAG は規範（AAA。値は上限であり最適値ではない）。画面の行長の実験は 2000 年前後のものが中心で数は多くなく、日本語（分かち書きなし）での直接の実験は見つけていない。「100 字が最速」という通俗的な要約は支持が弱い。 確かめた範囲（middy での確認）: WCAG 2.2 Understanding 1.4.8。Dyson らの原論文は未確認・網の方針外 |
| 当たるべき場面 | 文を出す列の幅を決めるとき。文が縦に細長くなっていないかの点検。 |
| 判断の問い | 1 行の文字数は、文を「列」ではなく「文」として読める長さか（日本語で上限 40 字の目安。短すぎても行替えが増える）。200% に拡大しても横スクロールが出ないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 強調と手がかり: 前注意的特徴、シグナリング、同期ハイライトの限界

| 欄 | 内容 |
| --- | --- |
| ID | `preattentive-signaling` |
| 出どころ | Treisman, A. & Gelade, G. (1980) A feature-integration theory of attention. *Cognitive Psychology* 12。Healey, C. G. & Enns, J. T. (2012) Attention and visual memory in visualization and computer graphics. *IEEE TVCG* 18(7)。解説: Laubheimer, P. (2017) Dashboards: Making Charts and Graphs Easier to Understand, NN/g https://www.nngroup.com/articles/dashboards-preattentive/ 。Richter, J., Scheiter, K. & Eitel, A. (2016) Signaling text-picture relations in multimedia learning: A comprehensive meta-analysis. *Educational Research Review* 17. https://doi.org/10.1016/j.edurev.2015.12.003 。Gerbier, E., Bailly, G. & Bosse, M.-L. (2018) Audio–visual synchronization in reading while listening to texts. *Computer Speech & Language* 47 |
| ソース | なし |
| 何を言っているか | 色・明度・向き・大きさ・長さ・2 次元の位置・動きなど少数の特徴は、周囲と 1 つだけ違えば一瞬で浮き上がる（前注意的）。組み合わせ（赤くて丸い）はそうならず探索になる。NN/g は、長さと位置は量に、色と形はカテゴリに向くとし、色覚多様性のため色は「2 番目の手がかり」にせよと言う。図と文の対応を色・矢印・同時の強調で示すと（シグナリング）、自力で対応づけできない初心者ほど理解が上がる（メタ分析、小〜中の効果）。ただし読み上げに同期して語を光らせる実験では、視線は誘導されたが学習は増えなかった |
| 確からしさ | 前注意的特徴は実験の積み重ねがある（理論の細部は修正されたが「単一特徴なら速い」は安定）。シグナリングは複数のメタ分析で向きが一致。「同期ハイライトで読める・分かる」は根拠がなく、視線の誘導にとどまる。 確かめた範囲（middy での確認）: NN/g の記事。Treisman & Gelade、Healey & Enns、Richter ら、Gerbier らの原論文は未確認・網の方針外 |
| 当たるべき場面 | 今の位置や選んでいるものを、文を読まずに一瞬で見つけさせたいとき。強調に使う特徴を 1 つに絞るか決めるとき。複数の場所に出る同じものを結ぶ方法を決めるとき。同期したハイライトに効果を期待するとき。 |
| 判断の問い | 強調は、1 つの特徴（明度か枠か動き）で、周囲のどれとも違うか。分類の色と競合していないか。同じものは、どの場所でも同じ色・同じ形で結ばれているか。同期したハイライトに期待しているのは「どこか」を示すこと（根拠あり）か、「内容が頭に入る」こと（根拠なし）か。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 画面幅のクラスと配置の切り替え

| 欄 | 内容 |
| --- | --- |
| ID | `window-size-classes` |
| 出どころ | Apple *Human Interface Guidelines* "Layout"（compact / regular の size class）https://developer.apple.com/design/human-interface-guidelines/layout 。Material Design 3 "Window size classes"（compact / medium / expanded / large / extra-large） |
| ソース | なし |
| 何を言っているか | 配置の分岐は「スマホか PC か」ではなく「使える幅（と高さ）がどれだけか」で決める。幅が変わっても、できることは変えない（配置だけ変える）。安全領域と余白を尊重し、文字サイズの拡大でも崩れないようにする |
| 確からしさ | プラットフォームの実務指針。Apple は、使える空間によってできることは変えず、画面に見せる量は変えてよい（広い画面でタブバーからサイドバーに替える、など）と書く。 確かめた範囲（middy での確認）: Apple HIG。Material 3 は JS 描画で本文が取れず未確認）。2026-11-10 に Android Developers の window size classes と "Support different display sizes" を確認。どちらも Material 3 の境目に対応し、物理的な端末の値で配置を決めない、部品は与えられた幅を使う、と明記している（https://developer.android.com/develop/ui/compose/layouts/adaptive/support-different-display-sizes  |
| 当たるべき場面 | 広い画面の列構成と、狭い画面の縦積みを切り替える幅を決めるとき。画面の大きさごとのテストの幅を決めるとき。 |
| 判断の問い | 分岐の条件は幅（と高さ）か（端末の種類ではないか）。幅が狭いときに、できることが失われていないか。文字を大きくしたら崩れないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 時間で変わる情報（自動で出る・消える）

### 流れて消える情報: 一過性情報効果と WCAG 2.2.1 / 2.2.2

| 欄 | 内容 |
| --- | --- |
| ID | `transient-information` |
| 出どころ | Leahy, W. & Sweller, J. (2011) Cognitive load theory, modality of presentation and the transient information effect. *Applied Cognitive Psychology* 25(6)。Wong, A., Leahy, W., Marcus, N. & Sweller, J. (2012) *Learning and Instruction* 22。W3C WCAG 2.2 SC 2.2.1 Timing Adjustable (A) https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html 、SC 2.2.2 Pause, Stop, Hide (A) https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html 。Nielsen, J. (2013) Auto-Forwarding Carousels and Accordions Annoy Users and Reduce Visibility, NN/g https://www.nngroup.com/articles/auto-forwarding/ |
| ソース | なし |
| 何を言っているか | 出て消える情報（音声、アニメーション、自動で切り替わる文）は作業記憶で保持し続けねばならず、留まる情報より負荷が高い。短ければ差は出ないが、長くなると留まる文字の方が良くなる。分節して短くすると害は減る。WCAG はこれを規範にしている: 読む速さを超えて進む・更新される内容は「時間制限」であり（2.2.1）、自動で始まり他の内容と並行して 5 秒を超えて動くもの、自動更新されるものには、一時停止・停止・非表示か更新頻度の制御が要る（2.2.2。活動に必須なら例外）。同期字幕やカルーセルは、操作で戻れる限り 2.2.1 の対象外。5 秒で消えるトーストは、同じ情報が別の場所で得られるなら可。NN/g の観察: 5 秒ごとに切り替わる箱は「読む時間がなかった」と言われ、大きく出ていても見つけてもらえない |
| 確からしさ | 一過性情報効果は 2010 年代に複数の実験で反復（原論文は未確認）。「どこから長いか」の境界は材料次第で、一般化された秒数はない。WCAG は規範（A）。 確かめた範囲（middy での確認）: WCAG 2.2 Understanding 2.2.1 と 2.2.2、NN/g の記事。Leahy & Sweller 2011、Wong ら 2012 は未確認・網の方針外 |
| 当たるべき場面 | 表示を自動で切り替える設計（数秒ごとに変わる文、スライド、ティッカー）。文を短くするか、留めるか（固定・一覧）、分節するかの判断。トーストや通知の表示時間。 |
| 判断の問い | この情報はユーザーが読み終える前に消えるか。消えるなら、あとで戻れる場所に同じ情報が留まっているか。短いもの（見出し）と長いもの（理由）で、流すものと留めるものを分けているか。自動で切り替わる領域に、止める・頻度を変える手段があるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 分節化と学習者ペース（止められるだけでは足りない）

| 欄 | 内容 |
| --- | --- |
| ID | `segmenting-learner-pace` |
| 出どころ | Mayer, R. E. & Chandler, P. (2001) When learning is just a click away. *Journal of Educational Psychology* 93(2)。Rey, G. D. et al. (2019) A meta-analysis of the segmenting effect. *Educational Psychology Review* 31. https://doi.org/10.1007/s10648-018-9456-4 。Tabbers, H. K., Martens, R. L. & van Merriënboer, J. J. G. (2004) *British Journal of Educational Psychology* 74。関連: W3C Media Accessibility User Requirements（拡張字幕: ユーザーが読む速さを決め、追いつくために再生を止められること）https://www.w3.org/TR/media-accessibility-reqs/ 。Schade, A. (2014) Video Usability, NN/g https://www.nngroup.com/articles/video-usability/ |
| ソース | なし |
| 何を言っているか | 連続して流れる説明を、学習者が「次へ」で進める分節にすると、保持と転移が上がる（メタ分析で小〜中の効果）。ただしシステムが決めた間隔で止める分節と、学習者が止める分節は別物で、初心者は「いつ止めるべきか」を知らないため、止められるだけでは利益が小さいという報告がある。学習者が自分のペースで進める条件では「音声の方が文字より良い」という様相効果が消える・逆転する。W3C の MAUR は、拡張字幕の要件として、読む速さをユーザーが決め、追いつくために再生を一時停止できることを挙げる。NN/g も映像は「制御できること」「逐次にしか読めない欠点を補う代替」を条件にする |
| 確からしさ | 分節化の効果はメタ分析で支持（原論文は未確認）。学習者ペースの境界条件（初心者は止めどころを知らない）は 2020 年前後の研究で議論中。MAUR は W3C のノート（規範ではない）。 確かめた範囲（middy での確認）: W3C MAUR、NN/g Video Usability。Mayer & Chandler、Rey ら、Tabbers らの原論文は未確認・網の方針外 |
| 当たるべき場面 | 動画・音声・アニメーションなど、時間で進む内容と説明を同期させる設計。何をユーザーのペースにするかを決めるとき。 |
| 判断の問い | ユーザーは読みたいときに「読むためのペース」を自分で取れるか（止める、戻る、1 つずつ進める）。止める操作は、内容を見聞きしながらでも届く大きさ・位置か。初めての人に、止めて読んでよいことが伝わるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 読みの速さと字幕の基準

| 欄 | 内容 |
| --- | --- |
| ID | `reading-speed-captions` |
| 出どころ | Nielsen, J. (2008) How Little Do Users Read?, NN/g https://www.nngroup.com/articles/how-little-do-users-read/ （英語の読む速さの前提 200 wpm、高リテラシーで 250 wpm）。豊倉省子・山田優 (2017) 字幕翻訳における文字数制限の妥当性についての検証〜1秒4文字は妥当か？〜. *通訳翻訳研究への招待* 18。Netflix "Japanese Timed Text Style Guide"。BBC Subtitle Guidelines https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/ 。Trauzettel-Klosinski & Dietz (2012) IReST, *IOVS* 53(9) |
| ソース | なし |
| 何を言っているか | 英語の読みは実務で 200〜250 語/分が前提に置かれる（NN/g）。日本語の黙読は平均 600 字/分前後（約 10 字/秒）で個人差が 3 倍以上あると紹介されるが、原資料は未取得。映像の字幕は絵も見ながら読むので、ずっと遅い基準が使われる: 日本の字幕の慣習は 1 秒 4 文字で、豊倉・山田の視線計測では 4 字と 6 字に差がなく 8 字/秒で負荷が上がったとされる。Netflix の日本語ガイドは 4 字/秒（日本語音声の字幕は 7 字/秒）、英語の放送字幕は 160〜180 語/分（いずれも未確認） |
| 確からしさ | 字幕の数値は業界の規範で、科学的な裏づけは限定的。黙読速度は個人差が非常に大きく、平均で設計すると半分の人に速すぎる。**この項目の日本語の数値は、この session では一次情報を開けていない。数値を根拠に使う前に開くこと。** 向きだけは確か: 音を聴きながら絵も見る状況では、黙読の速さではなく字幕の基準に近い。 確かめた範囲（middy での確認）: NN/g の記事のみ。豊倉・山田、Netflix、BBC、IReST、日本語黙読の原資料は未確認・網の方針外 |
| 当たるべき場面 | 時間で切り替わる文の文字数の上限、文が留まる最短時間、1 行の文字数を決めるとき。 |
| 判断の問い | この文は、表示されている秒数 × 読みの速さ（字幕の基準の目安）に収まるか。収まらない文は、流さずに留める設計になっているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 注意の捕捉と見落とし（出現・動き始め、変化の見落とし、選択的注意）

| 欄 | 内容 |
| --- | --- |
| ID | `attention-capture-change-blindness` |
| 出どころ | Yantis, S. & Jonides, J. (1984) Abrupt visual onsets and selective attention. *JEP: HPP* 10(5)。Abrams & Christ (2003) Motion onset captures attention. *Psychological Science* 14。Rensink, O'Regan & Clark (1997) To see or not to see. *Psychological Science* 8。Simons & Chabris (1999) Gorillas in our midst. *Perception* 28。解説: Harley, A. (2014) Animation for Attention and Comprehension, NN/g https://www.nngroup.com/articles/animation-usability/ 。Budiu, R. (2018) Change Blindness in UX https://www.nngroup.com/articles/change-blindness-definition/ 。Nielsen, J. (2012) Tunnel Vision and Selective Attention https://www.nngroup.com/articles/tunnel-vision-and-selective-attention/ |
| ソース | なし |
| 何を言っているか | 周辺視野の動き、とくに新しく現れるものと位置が変わるものは、意図と関係なく注意を引く（スライドインはフェードインより強く引く）。逆に、視線が外れた瞬間（瞬き、サッカード、再描画）に起きた変化や、注意を向けていない領域の変化は、大きくても気づかれない。操作に応じて 1 か所が変わると、ユーザーはそこを見るので、同時に別の場所で起きた変化は見落とされる。「見ている = 気づいている」ではない。因果を感じさせる動きは操作から 0.1 秒以内に始める |
| 確からしさ | 出現・動き始めの捕捉、変化の見落とし、非注意性盲目はいずれも実験の積み重ねが厚い（再現性の議論がある心理学の中では安定した部類。原論文は未確認）。NN/g の観察とも一致。 確かめた範囲（middy での確認）: NN/g の 3 記事。Yantis & Jonides、Abrams & Christ、Rensink ら、Simons & Chabris の原論文は未確認・網の方針外 |
| 当たるべき場面 | 何かを動かす・切り替える・出現させるとき。通知やトーストを出すとき。ユーザーが別のもの（音、別の領域）に注意を向けている間に、画面の一部を変えるとき。「出しておけば読むだろう」と考えたくなったとき。 |
| 判断の問い | 注意を向けてほしい場所以外で、出現や動き始めが起きていないか。ほかに集中しているユーザーがこの変化に気づく根拠はあるか。気づかなくても困らない（あとで戻れる）か。操作に応じて現れるものは、操作した場所の近くに出るか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 動きと「動きを減らす」設定

| 欄 | 内容 |
| --- | --- |
| ID | `motion-and-reduced-motion` |
| 出どころ | WCAG 2.2 SC 2.3.3 Animation from Interactions (AAA) https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html 、SC 2.2.2 Pause, Stop, Hide (A)。*Media Queries Level 5* `prefers-reduced-motion` https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion 。MDN https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion 。Apple HIG "Motion" |
| ソース | なし |
| 何を言っているか | 操作をきっかけに起きる必須でない動き（視差、ズーム演出）は切れるようにする。自動で 5 秒以上動き続けるものは止められるようにする。前庭障害の人には吐き気・頭痛を起こしうる。OS の「動きを減らす」設定は `prefers-reduced-motion: reduce` で読める。再生位置の移動のような、情報そのものである動きは「必須」に当たる |
| 確からしさ | 規範（WCAG）と仕様（CSS。主要ブラウザで実装済み）。 確かめた範囲（middy での確認）: WCAG 2.2、MQ5、MDN、Apple HIG |
| 当たるべき場面 | 強調の移動、画面の遷移、切り替えの演出のアニメーションを足すとき。遷移のアニメーションで負荷を減らす設計（概観+詳細）と両立させるとき。 |
| 判断の問い | この動きは情報か、演出か。演出なら `prefers-reduced-motion` で止められるか。自動で動き続けるものは止められるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 状態とモード

### モードとモードエラー、準モード（quasimode）

| 欄 | 内容 |
| --- | --- |
| ID | `modes-and-quasimodes` |
| 出どころ | Sellen, A., Kurtenbach, G. & Buxton, W. (1992) The prevention of mode errors through sensory feedback. *Human-Computer Interaction* 7(2). 著者公開版: https://billbuxton.com/ModeErrors.html 。Raskin, J. (2000) *The Humane Interface*（モードの定義、quasimode）。Laubheimer, P. (2019) Modes in User Interfaces, NN/g https://www.nngroup.com/articles/modes/ |
| ソース | なし |
| 何を言っているか | モード = 同じ入力が状態によって違う結果になること。モードエラーは、状態を取り違えて、別の状態なら正しい操作をしてしまうスリップ。Sellen らの実験では、画面全体の色を変える視覚フィードバックも効いたが、ペダルを踏み続けて保つ「ユーザー自身が維持するモード」の方がエラーも負荷も減った。Raskin は「注意の焦点に状態があるか」でモードを定義し、押している間だけ有効な準モードを勧める。NN/g は、モードを使うなら表示を 2 つ以上重ねて示し、取り返しのつかない場面では使うなと言う。「同じデータの別の見え方」はモードではない |
| 確からしさ | モードエラーの存在とフィードバックでの低減は実験で支持。「すべてのモードをなくす」は理念で、選択状態や文脈もモードの一種。 確かめた範囲（middy での確認）: Sellen らの全文、NN/g。Raskin は未確認・書籍 |
| 当たるべき場面 | 同じ操作の意味が、状態で変わるとき（追従と固定、編集と閲覧）。トグル（固定／解除、再生／停止）を足すとき。 |
| 判断の問い | 今どちらの状態かは、注意をほかに向けているユーザーにも見えるか。取り違えたとき、結果は取り返せるか。押している間だけ有効（準モード）にできないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 実行の淵と評価の淵、7 段階の行為

| 欄 | 内容 |
| --- | --- |
| ID | `gulfs-of-execution-evaluation` |
| 出どころ | Hutchins, E. L., Hollan, J. D. & Norman, D. A. (1985) Direct Manipulation Interfaces. *Human-Computer Interaction* 1(4). DOI 10.1207/s15327051hci0104_2。Norman, D. A. (2013) *The Design of Everyday Things, Revised* 第 2 章。解説: Whitenton, K. (2018) The Two UX Gulfs, NN/g https://www.nngroup.com/articles/two-ux-gulfs-evaluation-execution/ |
| ソース | なし |
| 何を言っているか | 人は「目標 → 意図 → 計画 → 実行 → 知覚 → 解釈 → 評価」を繰り返す。目標から操作へ渡る側の隔たりが実行の淵、画面の状態から「目標に対してどうなったか」を読み取る側が評価の淵。評価の淵は「見えている」だけでは埋まらず「意味が解釈できる」必要がある。評価が外れると、その後の実行も外れる |
| 確からしさ | 広く使われる枠組み。実験で検証された法則ではなく、失敗の原因を分解する道具。 確かめた範囲（middy での確認）: NN/g の解説と DOET の目次。Hutchins ら 1985 の本文は未確認・網の方針外 |
| 当たるべき場面 | 操作のあとに何が起きたかが伝わっているかの点検。状態（実行中、固定中、設定を変えたあと）の表示。新しい操作の前に「ユーザーはどの状態を見て判断するか」を書くとき。 |
| 判断の問い | この操作の結果を、ユーザーはどこを見て、どう解釈するか。今の状態は見えて、かつ意味が分かるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 概念モデル、システムイメージ、自然な対応づけ、制約

| 欄 | 内容 |
| --- | --- |
| ID | `conceptual-models-mapping` |
| 出どころ | Norman, D. A. (2013) *The Design of Everyday Things, Revised and Expanded*, Basic Books。第 1 章（概念モデル／システムイメージ）、第 3 章（自然な対応づけ）、第 4 章（4 種の制約、強制機能）。目次: https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/ 。Nielsen のヒューリスティクス 2「現実世界との一致」 |
| ソース | なし |
| 何を言っているか | 設計者の頭の中のモデルは直接ユーザーに届かない。ユーザーは「システムイメージ」（画面・文書・振る舞いから見えるもの全部）から自分のモデルを組み立てる。操作子と結果の空間的な対応（自然な対応づけ）と、できることを絞る制約は、説明なしでモデルを伝える手段。対応づけの一部（左右と上下、色の意味）は文化で変わる |
| 確からしさ | 枠組み。実務での合意は厚いが、個々の対応づけの効果は文脈で測る。 確かめた範囲（middy での確認）: 目次のみ。本文は未確認・書籍 |
| 当たるべき場面 | 新しい概念を足すとき、画面でどう見えるかを決めるとき。概念どうしの関係が画面から読めるかの点検。 |
| 判断の問い | 画面と振る舞いだけから、ユーザーは概念どうしの関係を正しく組み立てられるか。操作子の並びは、それが効く対象の並びと対応しているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 直接操作と委任（会話型 AI の UI、明示の壁、狭いスコープ）

| 欄 | 内容 |
| --- | --- |
| ID | `direct-manipulation-delegation` |
| 出どころ | Shneiderman, B. (1983) Direct Manipulation: A Step Beyond Programming Languages. *IEEE Computer* 16(8)。Shneiderman, B. & Maes, P. (1997) Direct manipulation vs. interface agents. *ACM Interactions* 4(6)（著者公開 PDF は cs.umd.edu）。Nielsen, J. (2023, 2025 更新) The Articulation Barrier, UX Tigers https://www.uxtigers.com/post/ai-articulation-barrier 。Moran, K. (2025) Scope in Generative AI Features, NN/g https://www.nngroup.com/articles/scope-ai-features/ 。Mugunthan, T. (2024) Response Outlining with Generative-AI Chatbots, NN/g |
| ソース | なし |
| 何を言っているか | 直接操作は、対象を常に表示し、対象への操作で動かし、小刻みで取り消し可能にし、結果をすぐ見せる型。予測可能性と制御感が利点で、対象が見えない・多すぎる作業では委任（エージェント）が向く。散文で意図を書かせる UI は書く力を要求し多くの人に重い（Nielsen の推論）。狭いスコープの AI 機能は目的が見えやすく、短い入力で済み、出力の形が予測できるので構造化した UI にでき、採用がよかった（NN/g の定性調査）。推奨は GUI で選べる要素を足したハイブリッド |
| 確からしさ | 直接操作は概念の枠組みで、多数の事例と実験で支持されるが「常に優れる」わけではない。会話型 AI の知見は意見記事と少人数の定性調査で、方向は一致、実験の積み重ねは薄い。 確かめた範囲（middy での確認）: UX Tigers、NN/g の 2 記事。Shneiderman 1983 と 1997 は未確認・IEEE と cs.umd.edu の TLS 検証失敗 |
| 当たるべき場面 | AI に言葉で頼む操作と、画面で直接いじる操作の切り分け。入力例・言い直しの支援を決めるとき。 |
| 判断の問い | この操作の結果はユーザーが予見できるか（直接操作向き）、何が出てくるか自体を相談したいのか（会話向き）。ユーザーが「どう言えばいいか」を知らないとき、画面は手がかり（入力例、押せる選択肢）を出しているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### ヒューリスティクス（Nielsen の 10 と、Shneiderman の黄金律の独自 2 点）

| 欄 | 内容 |
| --- | --- |
| ID | `usability-heuristics` |
| 出どころ | Nielsen, J. (1994, 2020 更新・2024 再確認) 10 Usability Heuristics for User Interface Design, NN/g https://www.nngroup.com/articles/ten-usability-heuristics/ 。元は Nielsen & Molich (1990) と 249 件の問題の因子分析（Nielsen 1994）。Shneiderman ほか *Designing the User Interface* 第 6 版（2016）の 8 つの黄金律（著者の一覧 https://www.cs.umd.edu/~ben/goldenrules.html ） |
| ソース | なし |
| 何を言っているか | 状態の可視化、現実との一致、制御と自由（取り消し・脱出）、一貫性と標準、エラーの予防（スリップとミステイクを分ける）、記憶より認識、柔軟性と効率、美的で最小限、エラーの認識と回復、ヘルプ。ヒューリスティクスは見つけた問題を分類する言葉で、満たせば使いやすいという十分条件ではない。黄金律で独自なのは「作業のまとまりに区切りと完了感を与える」「ユーザーが始めて、システムが応じる」 |
| 確からしさ | 1994 年版は因子分析に基づく。黄金律は実務の経験則。**よくある誤用:** チェックリストとして使い、満たしたら終わりにする。 確かめた範囲（middy での確認）: NN/g。黄金律は cs.umd.edu の TLS 検証失敗で未確認・項目名は複数の二次資料で一致 |
| 当たるべき場面 | 設計の原則にない観点の点検: 制御と自由（解除、取り消し、削除）、一貫性と標準、エラーの予防（スリップとミステイクで対策が違う）、エラーメッセージ（何が起きたか・次にすること）、流れの区切りと完了感。 |
| 判断の問い | 間違えたとき 1 手で戻れるか。この間違いはスリップ（注意 → 制約と既定値）か、ミステイク（モデル → 説明と確認）か。この流れのどこで「終わった」と分かるか。システムが勝手に状態を変えていないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 操作の対象と手がかり

### アフォーダンス（Gibson）とシグニファイア（Norman）

| 欄 | 内容 |
| --- | --- |
| ID | `affordances-signifiers` |
| 出どころ | Gibson, J. J. (1979) *The Ecological Approach to Visual Perception*。Norman, D. A. (2008) Signifiers, not affordances. *ACM Interactions* 15(6). 著者公開版: https://jnd.org/signifiers-not-affordances/ 。Norman (2013) DOET 第 1 章 |
| ソース | なし |
| 何を言っているか | Gibson のアフォーダンスは環境と行為者の関係で、知覚されるかどうかと無関係に存在する。Norman は 1988 年に「知覚されたアフォーダンス」の意味で設計に持ち込んだが誤用が広がり、2008 年に「設計者が与えるべきは、何ができるかを示す手がかり = シグニファイア」と言い直した |
| 確からしさ | 概念の枠組みで、実験による検証ではない。**よくある誤用:** 「ボタンにアフォーダンスを付ける」。問題になるのはアフォーダンスの有無ではなく、見えるか（シグニファイア）。 確かめた範囲（middy での確認）: Norman 2008 の著者公開版と DOET の目次。Gibson 1979 は未確認・書籍 |
| 当たるべき場面 | 要素が操作できることをどう示すか決めるとき。押せるもの・押せないものの見分け。新しい操作を足すとき。 |
| 判断の問い | 初見の人が、これを押せる・動かせると気づく手がかりは何か。押せないものが押せそうに見えていないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### フラット UI とクリック可能性の手がかり

| 欄 | 内容 |
| --- | --- |
| ID | `flat-ui-clickability` |
| 出どころ | Moran, K. (2017) Flat UI Elements Attract Less Attention and Cause Uncertainty, NN/g https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/ 。Loranger, H. (2015) Beyond Blue Links: Making Clickable Elements Recognizable, NN/g https://www.nngroup.com/articles/clickable-elements/ |
| ソース | なし |
| 何を言っているか | 9 サイト 18 ページを強い手がかり版と弱い手がかり版（ゴーストボタン、本文と同じ見た目のリンク）にして 71 人の視線を計った実験。弱い版では課題時間が平均 22%、注視回数が 25% 増え、視線が画面全体に散った。低い情報密度・慣習的な配置・目立つ位置の 3 条件がそろえばフラットでも害は小さい |
| 確からしさ | 1 本の視線計測実験。課題は「どこを押すか見つける」だけで、実作業全体の遅れはこれより小さいと著者自身が注記。 |
| 当たるべき場面 | 押せる要素の見た目を決めるとき。装飾を減らすとき。1 画面の要素が多いとき。主操作を見た目で区別するとき。 |
| 判断の問い | 押せる要素と押せない要素は、形・色・位置のどれで区別されるか。情報密度が高い画面で手がかりを弱めていないか。主操作はほかと違う形・大きさか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### Fitts の法則とタッチターゲットの大きさ・間隔

| 欄 | 内容 |
| --- | --- |
| ID | `fitts-target-size` |
| 出どころ | Fitts, P. M. (1954) The information capacity of the human motor system in controlling the amplitude of movement. *Journal of Experimental Psychology* 47。MacKenzie, I. S. (1992) Fitts' law as a research and design tool in HCI. *Human-Computer Interaction* 7。解説: Budiu, R. (2022) Fitts's Law and Its Applications in UX, NN/g https://www.nngroup.com/articles/fitts-law/ 。Nielsen, J. (2026 閲覧) Fitts's Law: Big and Near Beats Small and Far, UX Tigers https://www.uxtigers.com/post/fitts-law 。WCAG 2.2 SC 2.5.8 Target Size (Minimum) (AA) 24×24 CSS px https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html 、SC 2.5.5 (AAA) 44×44。Apple HIG "Accessibility"（44×44 pt、最小 28×28 pt）。Material 3（48×48 dp、間隔 8 dp。未確認） |
| ソース | なし |
| 何を言っているか | 標的に到達する時間は、距離が長いほど、標的が小さいほど、対数的に増える。小さい標的ほど減速の段階が長く、誤りも増える。画面の縁は行き過ぎがないので「無限の標的」になる（マウスのみ。タッチでは効かず、むしろ縁は遅い）。指は接触面が広く遮蔽もするので、画面上の px 計算より誤りが増え（FFitts）、44 pt / 48 dp / 1 cm といった下限が別に置かれる。隣接する標的との間隔は大きさと同じくらい効く。ひとつの画面で大きくするのは主操作だけにし、破壊的な操作は小さく・遠く・隣接させない。WCAG の 24 px は全ポインタ入力の最低線で、Working Group 自身がタッチには大きい値を勧めると注記。ズームしても CSS px は変わらないので「拡大すれば足りる」は通らない |
| 確からしさ | HCI で最も再現性の高いモデルの 1 つ（原論文は未確認）。タッチの下限値は運動制御の研究と実務の折衷。WCAG は規範（AA）。 確かめた範囲（middy での確認）: NN/g、UX Tigers、WCAG 2.2 Understanding 2.5.8、Apple HIG。Fitts 1954 と MacKenzie 1992 の原論文は未確認・網の方針外。Material 3 は未確認 |
| 当たるべき場面 | ボタン、一覧の項目、小さな操作子の大きさと間隔を決めるとき。狭い画面で当たり判定が小さくなるとき。ほかの作業をしながら押してほしい標的を置くとき。 |
| 判断の問い | ほかに視線を向けながら押してほしい標的は、押せる大きさ・位置か。24×24 CSS px の正方形を内側に描けるか。描けないなら隣との中心距離は 24 px 以上か。主操作は 44 px に届くか。隣を押し間違えたら何が起きるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### オブジェクト指向 UI（OOUI / OOUX）

| 欄 | 内容 |
| --- | --- |
| ID | `object-oriented-ui` |
| 出どころ | ソシオメディア、上野学、藤井幸多 (2020) 『オブジェクト指向UIデザイン』技術評論社。改訂新版 2026-07。書誌: https://gihyo.jp/book/2020/978-4-297-11351-3 、https://www.sociomedia.co.jp/ 。Collins, D. (1995) *Designing Object-Oriented User Interfaces*。IBM *CUA Guide to User Interface Design* (1991)。Prater, S. V. の OOUX（ORCA）https://www.ooux.com/ |
| ソース | なし |
| 何を言っているか | タスク（動詞）ではなくオブジェクト（名詞）を起点に UI を組み立てる。オブジェクトが知覚でき直接働きかけられる、オブジェクトが自分の性質と状態を体現する、「対象を選んでから操作を選ぶ」順序、オブジェクト同士が協調して UI を成す。手順は、名詞の抽出 → メインオブジェクトとそのコレクション／シングルのビュー → レイアウトパターン |
| 確からしさ | 実務の経験則の体系化（コンサルティングの事例が根拠）。対照実験はない。**よくある誤用:** 「オブジェクト = DB のテーブル」。CUA も Collins も、ユーザーの関心対象とプログラムのオブジェクトを分けている。 確かめた範囲（middy での確認）: gihyo.jp の書誌と目次、sociomedia.co.jp。本文、Collins、CUA、ooux.com は未確認 |
| 当たるべき場面 | 画面より先に、扱う対象（名詞）を決めるとき。新しい操作を「どの対象の、一覧と 1 つのどちらのビューに属するか」で位置づけるとき。 |
| 判断の問い | この操作はどの対象に属し、一覧（コレクション）と 1 つ（シングル）のどちらの画面にあるべきか。先に対象を選ばせてから操作を出しているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 段階的開示

| 欄 | 内容 |
| --- | --- |
| ID | `progressive-disclosure` |
| 出どころ | Nielsen, J. (2006) Progressive Disclosure, NN/g https://www.nngroup.com/articles/progressive-disclosure/ 。関連: WCAG 2.2 SC 1.4.13 Content on Hover or Focus |
| ソース | なし |
| 何を言っているか | 最初は重要な少数だけ見せ、残りは求められたら出す。初期画面に出ていること自体が「重要だ」という合図になる。うまくいく条件は、初期と二次の切り分けが正しいこと（頻繁に使うものは初期に）と、二次へ進む入口が見えて中身が予想できること。3 段以上は迷子になりやすい |
| 確からしさ | 実務の経験則（NN/g の多数の評価研究の要約）。「2 段まで」は目安。 |
| 当たるべき場面 | 状態が生まれるまで出さない、を実装するとき。説明の量（見出しだけ／理由まで／詳細まで）をいつ出すか決めるとき。「もっと見る」を足すとき。慣れたら薄くできる形を作るとき。 |
| 判断の問い | 初めに出すものは、頻繁に要るものだけか。二次の情報への入口は見えて、押すと何が出るか予想できるか。段が 3 つ以上になっていないか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 選択と既定値

### 選択過多（再現性に注意）と既定値の力

| 欄 | 内容 |
| --- | --- |
| ID | `choice-overload-defaults` |
| 出どころ | Iyengar, S. S. & Lepper, M. R. (2000) When choice is demotivating. *JPSP* 79(6)。Scheibehenne, B., Greifeneder, R. & Todd, P. M. (2010) Can there ever be too many options? *Journal of Consumer Research* 37(3). https://doi.org/10.1086/651235 。Chernev, A., Böckenholt, U. & Goodman, J. (2015) *Journal of Consumer Psychology* 25(2)。Nielsen, J. (2005) The Power of Defaults, NN/g https://www.nngroup.com/articles/the-power-of-defaults/ 。Loranger, H. (2015) Simplicity Wins over Abundance of Choice, NN/g https://www.nngroup.com/articles/simplicity-vs-choice/ |
| ソース | なし |
| 何を言っているか | 「選択肢が多いと選べない・満足が下がる」という 2000 年の有名な結果は、2010 年のメタ分析（50 実験）では平均効果がほぼゼロで研究間のばらつきが大きく、2015 年のメタ分析は、選択肢の複雑さ・課題の難しさ・好みの不確かさ・目的の 4 条件がそろうと出て、そろわなければ消えるとした（いずれも未確認）。一方、既定値の力は観察が安定している: 検索結果の 1 位と 2 位を密かに入れ替えても、1 位のクリック率は 42% → 34% に下がるだけで、ユーザーは上にあるものを選ぶ（Joachims らの研究、NN/g）。既定値は「その場の見本」と「よくある値の省力」の 2 つの役を持つ。NN/g は多機能化が判断の労力を増やすと経験則として言う |
| 確からしさ | **選択過多は再現性に議論がある。** 「選択肢は少ないほど良い」は一般則として成り立たない。成り立つのは、初心者が好みを言語化できず、違いが分かりにくい選択肢を決めなければならないとき。既定値の力は実験と観察で安定。 確かめた範囲（middy での確認）: NN/g の 2 記事。Iyengar & Lepper、Scheibehenne ら、Chernev らの原論文は未確認・網の方針外 |
| 当たるべき場面 | 候補や選択肢の数を決めるとき。既定値を決めるとき。 |
| 判断の問い | ユーザーはこの選択肢の違いを判断できる状態か。できないなら、数を減らすより、既定値で試して比べられるようにする方が効くか。既定値は最初の価値を速く届けるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 待ちと応答

### 応答時間のしきい値（0.1 / 1 / 10 秒）と進捗表示の形

| 欄 | 内容 |
| --- | --- |
| ID | `response-time-limits` |
| 出どころ | Miller, R. B. (1968) Response time in man-computer conversational transactions. *AFIPS FJCC* 33。Card, Robertson & Mackinlay (1991) The information visualizer. *CHI '91*。Nielsen, J. (1993) *Usability Engineering* 5 章、同 Response Times: The 3 Important Limits https://www.nngroup.com/articles/response-times-3-important-limits/ 、Powers of 10: Time Scales in UX https://www.nngroup.com/articles/powers-of-10-time-scales-in-ux/ 。Sherwin, K. (2014) Progress Indicators Make a Slow System Less Insufferable, NN/g https://www.nngroup.com/articles/progress-indicators/ 。Harrison, C. et al. (2007) Rethinking the progress bar. *UIST '07*。Doherty & Thadhani (1982) IBM 技術報告 |
| ソース | なし |
| 何を言っているか | 0.1 秒以内なら自分が直接操作している感覚が保たれ、1 秒以内なら思考の流れが切れず、10 秒を超えると注意がほかへ移る。1 秒を超える待ちには働いていることの表示、10 秒を超えるなら完了の見込み（割合）と中断の手段を出し、戻ってきたユーザーが再定位する前提で設計する。2〜10 秒はループするアニメーションで足り、1 秒未満にそれを出すと却って気になる。操作の直後に受け付けたことを示す（押された状態）。進捗表示は体感を変え、ある研究では表示ありの方が 3 倍長く待てた。速すぎて追えない変化（表示の慣性）も避ける。Harrison らは、同じ時間でも後半で加速するバーが速く感じられると報告（未確認） |
| 確からしさ | 0.1 / 1 / 10 は知覚の実験と実務の経験則を合わせた目安で、精密な定数ではない。**Doherty しきい値（400 ms）は 1980 年代の端末でのプログラマの生産性の観察で、人間の知覚限界ではない。** 「Laws of UX」などで法則のように引かれるが、独立した再現は見つけていない。使うなら「速いほど操作が増える」という向きだけ。 確かめた範囲（middy での確認）: NN/g の 3 記事。Miller 1968、Card ら 1991、Harrison ら 2007、Doherty & Thadhani は未確認・ACM のボット遮断と著者ページの網の方針外 |
| 当たるべき場面 | 操作から反応までの遅延（再描画、音や映像の開始、保存）。LLM や外部の API の応答待ち（数秒〜十数秒、長さが予測できない）。 |
| 判断の問い | 操作から反応まで 0.1 秒を超える操作はどれか。1 秒を超える待ちに、進んでいることの表示はあるか。10 秒を超えうる待ちで、注意が離れても戻れる手がかりと中断の手段はあるか。待ちの長さは予測できるか。できないなら、偽の進捗より「状態の変化」（送った内容が残っている、前の結果は使える）を見せているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 学習の負荷

### 認知負荷理論（内在・外在）と一貫性（関係のない情報は削る）

| 欄 | 内容 |
| --- | --- |
| ID | `cognitive-load-coherence` |
| 出どころ | Sweller, J. (1988) Cognitive load during problem solving. *Cognitive Science* 12。Sweller, van Merriënboer & Paas (2019) Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review* 31. https://doi.org/10.1007/s10648-019-09465-5 。Whitenton, K. (2013) Minimize Cognitive Load to Maximize Usability, NN/g https://www.nngroup.com/articles/minimize-cognitive-load/ 。Sundararajan, N. & Adesope, O. O. (2020) Keep it coherent: A meta-analysis of the seductive details effect. *Educational Psychology Review* 32(3)。Mayer の一貫性原理（*Multimedia Learning* 3rd ed.） |
| ソース | なし |
| 何を言っているか | 学習時の作業記憶の負荷を、内容そのものの複雑さ（内在）と、提示の仕方で生じる無駄（外在）に分け、外在を削って作業記憶を内容に回す。NN/g の言い換え: 内在負荷は消せないし消すべきでもない。外在負荷（意味のない装飾、記憶や判断を強いる手順）を削り、既存のメンタルモデルに乗せ、課題を肩代わりする（見せる、再表示する、既定値）。学習目標に関係ない挿話・装飾を足すと、面白くはなるが学習は下がる（誘惑的詳細。メタ分析で小〜中の負の効果） |
| 確からしさ | 多数の効果が実験で反復。負荷の測定法と「学習関連負荷」の定義には批判がある。誘惑的詳細の効果は小さく、動機を保つ効果との兼ね合いは未解決。ux-principles 3 章の冒頭は理論の要点を正しく踏まえている。 確かめた範囲（middy での確認）: NN/g の記事。Sweller 1988、Sweller ら 2019、Sundararajan & Adesope 2020 は未確認・Springer が網の方針外 |
| 当たるべき場面 | 学習や理解のための画面で、何を削り、何を残すかの判断すべて。「内容の難しさは削らず、画面の理解に使う負荷を削る」の根拠。説明に雰囲気の形容や雑学を足したくなったとき。 |
| 判断の問い | この要素の理解に使う負荷は、内容の理解に向かうか、画面の操作・配置の解読に消えるか。この文・絵は内容の理解に寄与するか、雰囲気づくりか。雰囲気づくりなら、理解の文と同じ場所・同じ重さで出す必要があるか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 色とコントラスト

### 色だけに頼らない（WCAG 1.4.1）

| 欄 | 内容 |
| --- | --- |
| ID | `color-not-sole-means` |
| 出どころ | WCAG 2.2 SC 1.4.1 Use of Color (A) https://www.w3.org/TR/WCAG22/#use-of-color 。Understanding: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html |
| ソース | なし |
| 何を言っているか | 情報の伝達、操作の指示、応答の促し、要素の区別を色だけで行わない。色相だけでなく明度も違い、相対輝度のコントラスト比が 3:1 以上なら「別の視覚的な区別」と数えてよい。ただし「緑なら有効」のように特定の色を言い当てる必要がある場合は、比に関係なく別の手がかりが要る。色分け自体を禁じるものではない |
| 確からしさ | 規範（A）。 |
| 当たるべき場面 | 分類や状態を色で分けるとき。今の位置の強調。選択中や固定中の表示。エラーの表示。 |
| 判断の問い | 色を白黒にしても、同じ情報が読めるか。分類は文字・形・位置でも区別されているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### コントラスト: 文字（1.4.3）と文字以外（1.4.11）、WCAG 3 / APCA の位置づけ

| 欄 | 内容 |
| --- | --- |
| ID | `contrast-wcag` |
| 出どころ | WCAG 2.2 SC 1.4.3 Contrast (Minimum) (AA): 文字 4.5:1、大きな文字 3:1。SC 1.4.11 Non-text Contrast (AA): 3:1。Understanding Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html 。W3C *WCAG 3.0* Working Draft https://www.w3.org/TR/wcag-3.0/ 。Somers, A. *APCA* https://github.com/Myndex/SAPC-APCA |
| ソース | なし |
| 何を言っているか | 部品は「存在と操作法がわかるのに必要な部分」が 3:1 あればよく、フォーカス表示は常に必要、非活性の部品は対象外。細い線はアンチエイリアスで見かけの濃さが落ちるので太くするか比を余らせる。状態の印は部品内部の色に対して測る。WCAG 3 は作業草案で、文字コントラストのアルゴリズムは未決定。APCA は候補の 1 つで、明暗の極性とフォントサイズ・太さを考慮する知覚ベースの指標 |
| 確からしさ | 1.4.3 / 1.4.11 は規範（AA）。3:1 の閾値は丸めない。**WCAG 3 は規範ではなく、適合の根拠は今も WCAG 2.2。** **よくある誤用:** 「APCA を使えば WCAG 2 の比は無視してよい」。 |
| 当たるべき場面 | ダーク・ライトの両テーマで色のトークンを決めるとき。細い線、小さな図形、状態の塗り。「WCAG 3 対応」をうたいたくなったとき。 |
| 判断の問い | 文字は 4.5:1、部品の輪郭・状態・図形の必要な部分は 3:1 を、両テーマで満たすか。細い線は太くできるか。APCA を使うなら「補助」と明記しているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 色覚多様性とカテゴリ色: Okabe–Ito の Color Universal Design

| 欄 | 内容 |
| --- | --- |
| ID | `color-universal-design` |
| 出どころ | 岡部正隆・伊藤啓 "Color Universal Design (CUD)" https://jfly.uni-koeln.de/color/ （引用時は両名を記すようにと明記）。Ichihara, Okabe, Iga, Tanaka, Musha, Ito (2008) *Proc. SPIE* 6807. DOI 10.1117/12.765420 |
| ソース | なし |
| 何を言っているか | 色覚の型が違っても、印刷しても見分けられる 8 色の組（黒、橙、空色、青緑、黄、青、朱、赤紫）。赤は朱にして 1 型色覚でも黒と区別、黄と緑の間を避け、緑は青みに、紫は赤紫に。細い線と小さな文字には空色・黄より濃い青・橙。暖色と寒色を交互に、同系なら明度か彩度に差を。「色の名前で指さない」、色以外の手がかりを重ねる |
| 確からしさ | 色覚のシミュレーションと当事者の確認に基づく実務の提案。広く使われ（R・matplotlib の既定パレット）実務上の標準に近い。「8 色まで」は見分けの限界で、カテゴリは少ないほどよい。 確かめた範囲（middy での確認）: jfly のページ。SPIE 論文は未確認 |
| 当たるべき場面 | 少数のカテゴリに色を割り当てるとき。ダーク・ライトで同じカテゴリ色を保つとき。グラフや地図を足すとき。 |
| 判断の問い | カテゴリは 3〜5 以内か。色覚のシミュレーションで見分けがつくか。小さな要素に黄や空色を使っていないか。色の名前で説明していないか（「赤いもの」ではなく位置や名前で指す）。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### 知覚的に均一な色空間でトークンを作る（CIELAB / Oklab / OKLCH）

| 欄 | 内容 |
| --- | --- |
| ID | `perceptual-color-spaces` |
| 出どころ | Ottosson, B. (2020) A perceptual color space for image processing https://bottosson.github.io/posts/oklab/ 。W3C *CSS Color Module Level 4* §9 https://www.w3.org/TR/css-color-4/ 。*CSS Color Module Level 5* `color-mix()` https://www.w3.org/TR/css-color-5/ 、MDN https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix |
| ソース | なし |
| 何を言っているか | HSL/HSV は同じ「明度」でも黄と青で見た目の明るさが大きく違う。Oklab は明度 L・色度が互いに独立に近く、補間が滑らかになるよう設計された。CSS では `oklch()` / `oklab()` / `lab()` / `lch()` が標準化され、`color-mix()` で混ぜる色空間を選べる |
| 確からしさ | 色彩科学の応用。「知覚的に均一」は近似。トークンの決め方の道具であって、WCAG のコントラスト比の代替ではない。 |
| 当たるべき場面 | 両テーマでカテゴリの色を「同じ明るさ・同じ彩度」にそろえるとき。段階色（強調の濃淡）を作るとき。`color-mix` の色空間を選ぶとき。 |
| 判断の問い | トークンは OKLCH の L を揃えて作っているか。混色は `in oklch` か `in srgb` か。できた色は WCAG 2.2 の比を満たすか（均一性は比を保証しない）。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### ダークモードとコントラスト極性

| 欄 | 内容 |
| --- | --- |
| ID | `dark-mode-polarity` |
| 出どころ | Budiu, R. (2020) Dark Mode vs. Light Mode: Which Is Better?, NN/g（文献レビュー）https://www.nngroup.com/articles/dark-mode/ 。一次研究（NN/g の記述による）: Piepenbrock ほか (2013) *Ergonomics*、同 (2013) *Human Factors*、Piepenbrock, Mayr & Buchner (2014) *Ergonomics*、Dobres ほか (2017) *Applied Ergonomics*。Apple HIG "Dark Mode" |
| ソース | なし |
| 何を言っているか | 通常視力の人では、明るい背景に暗い文字（正極性）の方が読みの成績がよく、文字が小さいほど差が開く。機序は瞳孔が縮んで被写界深度が増すこと。暗い環境光では差がさらに出る。本人の主観は差を感じない。白内障などではダークが有利な場合がある。NN/g の結論: 既定はライト、切り替えは必ず提供し、OS の設定に従う。Apple は両方の外観で試し、小さな文字は 7:1 を目標にせよと言う |
| 確からしさ | 実験室研究が複数あり方向は一致。効果は環境光・文字サイズ・年齢で変わる。NN/g 自身は独自調査をしていないと明記。 確かめた範囲（middy での確認）: NN/g と Apple HIG。Piepenbrock ら・Dobres らの原著は未確認 |
| 当たるべき場面 | ダークテーマの文字の大きさとコントラストを決めるとき。狭い画面で小さい文字をダークで出すとき。 |
| 判断の問い | ダークテーマで、小さな文字は大きくするか比を上げているか。OS の設定に従い、両方で試しているか。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 支援技術

### WAI-ARIA Authoring Practices: ツールバー、リストボックス／グリッド、スライダー

| 欄 | 内容 |
| --- | --- |
| ID | `aria-authoring-practices` |
| 出どころ | W3C WAI *ARIA Authoring Practices Guide*: Toolbar https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/ 、Listbox https://www.w3.org/WAI/ARIA/apg/patterns/listbox/ 、Grid https://www.w3.org/WAI/ARIA/apg/patterns/grid/ 、Slider https://www.w3.org/WAI/ARIA/apg/patterns/slider/ 。*WAI-ARIA 1.2* https://www.w3.org/TR/wai-aria-1.2/ |
| ソース | なし |
| 何を言っているか | ツールバー: 3 つ以上の操作を 1 つの Tab 停止にまとめ、矢印キーで中を移動。リストボックス: 選択肢の名前は短く、先頭語の繰り返しを避ける。選択肢の中に見出しやボタンなどの意味を持つ要素は置けない。中に操作できる要素を並べたいならグリッド。スライダー: タッチの支援技術はジェスチャをキー操作に変換するので実機で試す |
| 確からしさ | W3C の実装指針（規範ではない）。支援技術との相性は組み合わせで変わる。 |
| 当たるべき場面 | ツールバーの Tab の回数を減らすとき。一覧の項目（`role="listbox"` と `option`）の中に、名前以外の情報や操作を足したくなったとき。スライダーを足すとき。 |
| 判断の問い | 主操作まで Tab 何回か。option の名前は短いか。option の中にボタンや見出しを入れようとしていないか（→ グリッドにするか、外に出す）。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

### ライブリージョンと状態メッセージ（うるさい読み上げの危険）

| 欄 | 内容 |
| --- | --- |
| ID | `live-regions-status` |
| 出どころ | *WAI-ARIA 1.2* Live Regions（aria-live, aria-atomic, aria-relevant, aria-busy）https://www.w3.org/TR/wai-aria-1.2/ 。WCAG 2.2 SC 4.1.3 Status Messages (AA) https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html 。MDN "ARIA live regions" https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions |
| ソース | なし |
| 何を言っているか | ライブリージョンは、フォーカスが別の場所にあるときに変わる領域を支援技術に知らせる。`polite` は手が空いたときに読む、`assertive` は割り込む（時間に厳しい重要事項だけ）。MDN は「重要だが、うるさいほど速くは変わらない更新」に polite を使えと言う。4.1.3 は、フォーカスを奪わずに結果・待機・進捗・エラーを知らせるメッセージを支援技術が読める形にせよという要件 |
| 確からしさ | 規範（WCAG）と実装仕様（ARIA）。支援技術の実装差が大きい。 |
| 当たるべき場面 | 画面の変化を支援技術に伝えるとき。自動で変わる領域に `aria-live` を付けるかどうか決めるとき。 |
| 判断の問い | この領域は数秒ごとに変わるが、それを全部読み上げさせたいか。読み上げるなら短い状態だけにして、長い文は別の領域にできないか。役割は status（結果の通知）か、読者が自分で辿る内容か。 |
| 対象 | なし |
| 確認 | 2026-11-09 / 間隔 365 日 |

## 外したもの

| 知見 | 外した理由 |
| --- | --- |
| Hick–Hyman の法則と、その誤用 | middy の索引で、出どころを開けていない（未確認（ACM DL はボット遮断、Taylor & Francis は網の方針外。NN/g に該当する解説記事はなかった。書誌は検索結果の抄録で照合））。開けたら項目にする |
| 望ましい困難と「学習と成績の乖離」 | middy の索引で、出どころを開けていない（未確認（UCLA の著者ラボ、SAGE が網の方針外。書誌は検索結果で照合））。開けたら項目にする |
| 熟達の逆転効果（初心者に効く支援が、経験者には邪魔になる） | middy の索引で、出どころを開けていない（未確認（Taylor & Francis、Springer が網の方針外。書誌は検索結果の抄録で照合））。開けたら項目にする |
