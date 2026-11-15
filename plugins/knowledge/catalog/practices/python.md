# Python

Python のコード、依存、配布の判断。項目の形は `plugins/knowledge/catalog/README.md`。

### ライブラリは、自分のロガーに NullHandler 以外のハンドラを付けない

| 欄 | 内容 |
| --- | --- |
| ID | `py-library-logging` |
| 出どころ | Python の文書「Logging HOWTO」の「Configuring Logging for a Library」。https://docs.python.org/3/howto/logging.html |
| ソース | なし |
| 何を言っているか | ライブラリの中では、`logging.getLogger(__name__)` のように、一意で見分けやすい名前のロガーを使い、ルートのロガーに出さない。ライブラリのロガーには、`NullHandler` 以外のハンドラを付けない。どのハンドラを使うかは、ライブラリを使うアプリケーションが決めることで、ライブラリが付けると、アプリケーションのテストやログの出し方を妨げる。ライブラリが使うロガーの名前は、文書に書く。 |
| 確からしさ | 公式の推奨（強く勧める、と書かれている）。設定が無いとき、WARNING 以上が標準エラーに出るのが望ましい既定とされ、それも止めたいときだけ `NullHandler` を付ける。誤用: ライブラリやモジュールの読み込みのときに `logging.basicConfig()` を呼ぶ。ライブラリの中で `logging.info()` のようにルートのロガーに出す。 |
| 当たるべき場面 | 他から読み込まれるモジュールやパッケージに、ログを足すとき。ログの設定（ハンドラ、書式、レベル）をどこで行うか決めるとき。Lambda の関数のように、実行の環境がログの設定を持っているとき。 |
| 判断の問い | ログの設定（`basicConfig`、ハンドラの追加）は、アプリケーションの入口の 1 か所だけで行っているか。読み込まれる側のコードは、`getLogger(__name__)` のロガーだけを使っているか。 |
| 対象 | `python@3` |
| 確認 | 2026-11-15 / 間隔 365 日 |

### 時刻は、タイムゾーンを持つ aware な datetime で扱う

| 欄 | 内容 |
| --- | --- |
| ID | `py-aware-datetime` |
| 出どころ | Python の文書「datetime」の「Aware and naive objects」と `datetime.utcnow()`。https://docs.python.org/3/library/datetime.html |
| ソース | なし |
| 何を言っているか | datetime には、タイムゾーンの情報を持ち、ほかの時刻との前後が一意に決まる aware なものと、それを持たない naive なものがある。naive なものは、多くのメソッドで地方時として扱われる。`datetime.utcnow()` は UTC の時刻を naive で返すので、v3.12 で非推奨になった。今の UTC の時刻は `datetime.now(timezone.utc)` で得る。 |
| 確からしさ | 公式の文書。naive なものは、地方時か UTC か別の何かかを、プログラムが決める（扱いやすいが、取り違えやすい）。誤用: `utcnow()` の結果に `.timestamp()` を使い、地方時として解釈されてずれる。aware と naive を比べて例外を出す。 |
| 当たるべき場面 | 時刻を作る、保存する、比べる、外の API（AWS の SDK など）とやり取りするコードを書くとき。`utcnow()` や `utcfromtimestamp()` を見つけたとき。 |
| 判断の問い | この時刻は aware か。naive なら、どのタイムゾーンとして扱うかが、コードのどこで決まっているか。`utcnow()` を使っていないか。 |
| 対象 | `python@3` |
| 確認 | 2026-11-15 / 間隔 365 日 |

### subprocess は shell=True を使わず、引数を一覧で渡す

| 欄 | 内容 |
| --- | --- |
| ID | `py-subprocess-no-shell` |
| 出どころ | Python の文書「subprocess」の「Security Considerations」。https://docs.python.org/3/library/subprocess.html |
| ソース | なし |
| 何を言っているか | `subprocess` は、暗黙にシェルを呼ばない。そのため、シェルの特殊な文字を含めて、引数はそのまま子のプロセスに渡る。`shell=True` でシェルを明示的に呼ぶときは、空白と特殊な文字を適切に引用して、シェルへの注入を防ぐ責任がアプリケーションにある（POSIX では `shlex.quote()` が使える）。Windows では、バッチファイルは引数によらずシェルで起動されることがある。 |
| 確からしさ | 公式の文書。誤用: 文字列を組み立てて `shell=True` で渡す。外から来た値（ファイル名、リソースの名前）をコマンドの文字列に埋め込む。 |
| 当たるべき場面 | Python から外のコマンド（`aws`、`git`、`terraform` など）を呼ぶコードを書く、レビューするとき。 |
| 判断の問い | `shell=True` を使っていないか。使うなら、シェルが要る理由（パイプ、展開）を言え、外から来た値をすべて引用しているか。引数を一覧で渡す形にできないか。 |
| 対象 | `python@3` |
| 確認 | 2026-11-15 / 間隔 365 日 |

### 配る依存は抽象的に、環境の依存は固定して持つ

| 欄 | 内容 |
| --- | --- |
| ID | `py-abstract-vs-pinned-requirements` |
| 出どころ | Python Packaging User Guide「install_requires vs requirements files」。https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/ 。同「Writing your pyproject.toml」。https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ |
| ソース | なし |
| 何を言っているか | パッケージの依存（`pyproject.toml` の `dependencies`、setuptools の `install_requires`）には、動くのに最小限要るものを、分かっている下限と上限だけで書く。特定の版への固定や、依存の依存を書くのは、利用者が依存の更新の利益を得られなくなるので勧めない。どこから入れるかは決めない（抽象的）。一方、requirements のファイルは、1 つの環境を再現するために、すべてを版で固定し、取得先も決める（具体的）ことが多い。`requires-python` に上限を付けるのは、よく考えてからにする。テストや lint の依存は `[dependency-groups]` に書ける。 |
| 確からしさ | 公式の文書（Python Packaging Authority）。ライブラリとアプリケーションで使い分ける考え方で、デプロイするだけのアプリケーション（Lambda の関数など）では、環境の固定の方が主になる（推測。ページはライブラリの依存と環境の依存を比べている）。誤用: ライブラリの `dependencies` に、`==` で依存の依存まで固定する。アプリケーションの環境を固定せず、デプロイのたびに違う版が入る。 |
| 当たるべき場面 | `pyproject.toml` の依存を書く、変えるとき。requirements のファイルやロックファイル（uv、Poetry など）を足すか決めるとき。 |
| 判断の問い | このプロジェクトは、他に読み込まれるライブラリか、デプロイするアプリケーションか。ライブラリなら、依存は範囲で書いているか。アプリケーションなら、デプロイする環境は版で固定され、それがコミットされているか。 |
| 対象 | なし |
| 確認 | 2026-11-15 / 間隔 365 日 |

### src のレイアウトで、開発中のコードを誤って読み込まない

| 欄 | 内容 |
| --- | --- |
| ID | `py-src-layout` |
| 出どころ | Python Packaging User Guide「src layout vs flat layout」。https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ |
| ソース | なし |
| 何を言っているか | flat のレイアウトは、読み込まれるパッケージを最上位のディレクトリに置く。src のレイアウトは `src/` の下に置く。Python は今のディレクトリを読み込みの道の先頭に入れるので、flat では、入れたものではなく開発中の写しが読み込まれ、配布物にファイルが入っていないことに気づけないことがある。src では、動かすのにインストール（開発中は編集可能なインストール）が要るが、その誤りを防ぎ、読み込ませるつもりのファイルだけが読み込める。 |
| 確からしさ | 公式の文書の「議論」の節で、どちらを使えとは言わず、違いを並べている（流儀が割れる）。誤用: src のレイアウトにしたのに、テストで `sys.path` を書き換えて、インストールせずに読み込む。 |
| 当たるべき場面 | 新しい Python のプロジェクトのディレクトリの形を決めるとき。テストでは通るのに、配布物やデプロイ物で読み込みに失敗したとき。 |
| 判断の問い | このプロジェクトは配布物（wheel など）を作るか。作るなら、テストはインストールしたものに対して走っているか（flat のレイアウトでは、開発中の写しに対して走っていないか）。 |
| 対象 | なし |
| 確認 | 2026-11-15 / 間隔 365 日 |
