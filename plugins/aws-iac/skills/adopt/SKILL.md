---
name: adopt
description: ai-dev-methodologies の aws-iac を、今のリポジトリに導入する。Terraform や CDK のコードの検査を make check に入れ、エージェントが計画までを行う前提を所有者と確かめる。core を導入済みのリポジトリで使う。
disable-model-invocation: true
---

# adopt（aws-iac）

Terraform や CDK で AWS のインフラを管理するリポジトリに、`aws-iac` を入れる。先に `core` を導入しておく（`AGENTS.md` と `make check` があること）。無ければ、`core` のスキル `adopt` を先に行う。

## 手順

1. **調べる。** インフラのコードの場所を全部見つける。Terraform は `terraform plan` を走らせるディレクトリ（ルートモジュール）、CDK は `cdk.json` のあるディレクトリ。環境の分け方（ディレクトリ、ワークスペース、変数のファイル）と、今ある検査（CI、lint の設定、pre-commit）も読む。
2. **置かれるものを見せる。** `bash <このスキルのディレクトリ>/adopt.sh --dry-run <リポジトリの最上位>` を走らせ、結果を所有者に示す。
3. **置く。** 作業用のブランチで、`--dry-run` を外して走らせる。
4. **検査をつなぐ。**
   - 置かれた `iac-roots.txt`（`scripts/` の下）に、1 で見つけた場所を書く。書き方は、そのファイルの冒頭にある。
   - `Makefile` に `iac-check` のターゲット（置かれた `check-iac.sh` を `bash` で呼ぶ）を足し、`check` から呼ぶ。
   - `docs/dev/harness.md` に、検査の行を足す（書式、初期化と検証、lint、synth）。
   - CI に、要る道具の導入を足す（Terraform、tflint、Node）。版は、リポジトリが固定しているもの（`.terraform-version`、`required_version`、`.tool-versions`、`package.json`）に合わせる。
   - `.gitignore` に `.terraform/` と `cdk.out/` が無ければ足す。
   - すでにある検査（tfsec、checkov、cdk-nag など）は、消さずに `check` から呼ぶ。無いものを足すかどうかは、所有者に示して決めてもらう。
5. **plugin を有効にする。** `.claude/settings.json` の `enabledPlugins` に `aws-iac@ai-dev-methodologies` を足す。
6. **任せる範囲を書く。** `AGENTS.md` のガードレールに、次を足す。
   - エージェントは、変更の計画（`terraform plan`、`cdk diff`、`cdk synth`）までを行う。反映（`terraform apply`、`cdk deploy`）は所有者が行う。
   - state を触らない（`import`、`state rm`、`force-unlock` など）。要るときは、所有者への提案として書く。
   - 反映を呼ぶスクリプトや `Makefile` のターゲットを走らせない（リポジトリにあれば、名前を挙げて書く）。
   - 属性の値や出力の値（秘密情報を含みうる）を、会話・PR・Issue に写さない。
7. **所有者の OK が要る変更を書く。** `docs/dev/workflow.md` の「`ready` にしない」と「マージ」の「所有者の OK を待つもの」の一覧に、インフラの構成を変える PR は所有者の OK を待つ、を足す。
8. **認証情報を所有者に用意してもらう。** エージェントが使う AWS の認証情報は、計画に要る権限まで（リソースの読み取りと、state の読み取り）にする。フックは反映を止めるが、安全網で、防壁は認証情報の権限。エージェントは、認証情報を作らない・書き換えない。
9. **確かめる。** `make check` を通す。通らなければ、検査を弱めずに、コードを直すか、直せない理由を所有者に示す。
10. **報告する。** 置いたファイル、つないだ検査、所有者が決めること、を一覧にする。

## 新しい版に合わせる

導入済みのリポジトリでは、手順 2 から行う。コピーするファイルの結果（`same`、`updated`、`edited`、`kept`）の読み方と、`kept` のときの手順は、`core` のスキル `adopt` の「新しい版に合わせる」と同じ。

## 守ること

- 反映しない。state を触らない。
- 今ある検査を消さない。
