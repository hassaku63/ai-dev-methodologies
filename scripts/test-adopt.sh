#!/usr/bin/env bash
# Adopts core into an empty repository and checks the result:
#   1. `make check` passes right after adoption.
#   2. A second run changes nothing.
#   3. A managed file changed by hand is kept; an untouched one is updated.
#      With a new version of the plugin, a hand-edited file it changes is kept
#      and its new version named; taking the new version makes it the same.
#   4. An owned file is never overwritten.
#   5. A second plugin (aws-ops) keeps the lock lines of the first.
#   6. aws-iac's check runs every step with stub tools, fails when a tool
#      fails or is missing, and calls nothing its guard would stop.
#   7. knowledge's mapping check accepts catalog IDs and rejects unknown,
#      duplicated, empty and malformed rows and local entries, and an entry
#      written for another version of a dependency the repository uses.
# Part of `make check`. Needs bash, git, make.
# Backticks inside single quotes are Markdown here, not command substitution.
# shellcheck disable=SC2016
set -euo pipefail
cd "$(dirname "$0")/.."

adopt="$PWD/plugins/core/skills/adopt/adopt.sh"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
repo="$work/example"
mkdir "$repo"
git -C "$repo" init -q

fail() { echo "test-adopt: FAILED: $*" >&2; exit 1; }

# 1. adoption, then every gate
bash "$adopt" "$repo" > "$work/first.log"
grep -q '^added    scripts/check-docs.sh$' "$work/first.log" || fail "check-docs.sh was not added"
grep -q '^created  AGENTS.md$' "$work/first.log" || fail "AGENTS.md was not created"
grep -q '^# AGENTS.md — 開発ガイド$' "$repo/AGENTS.md" || fail "AGENTS.md has no title"
grep -q 'example で作業する' "$repo/AGENTS.md" || fail "the project name was not filled in"
if grep -rq '{{' "$repo" --exclude-dir=.git --exclude=ci.yml; then fail "a placeholder was left"; fi
make -C "$repo" check > "$work/check.log" 2>&1 || { cat "$work/check.log" >&2; fail "make check does not pass after adoption"; }

# 2. idempotent
cp "$repo/.agents/methodology.lock" "$work/lock.before"
bash "$adopt" "$repo" > "$work/second.log"
if grep -Eqv '^(same|exists) ' "$work/second.log"; then cat "$work/second.log" >&2; fail "the second run changed something"; fi
cmp -s "$work/lock.before" "$repo/.agents/methodology.lock" || fail "the lock changed on the second run"

# 3. a hand-edited managed file is kept; a stale untouched one is updated
echo "# local change" >> "$repo/scripts/check-pr-size.sh"
stale="$repo/docs/dev/docs-hygiene.md"
echo "stale" > "$stale"
stale_hash=$( (sha256sum "$stale" 2>/dev/null || shasum -a 256 "$stale") | cut -d' ' -f1)
awk -v h="$stale_hash" '$3 == "docs/dev/docs-hygiene.md" { $2 = h } { print }' "$repo/.agents/methodology.lock" > "$work/lock.tmp"
cp "$work/lock.tmp" "$repo/.agents/methodology.lock"
bash "$adopt" "$repo" > "$work/third.log"
grep -q '^edited   scripts/check-pr-size.sh$' "$work/third.log" || fail "a hand-edited managed file with nothing new upstream was not reported as edited"
grep -q '^# local change$' "$repo/scripts/check-pr-size.sh" || fail "a hand-edited managed file was overwritten"
grep -q '^updated  docs/dev/docs-hygiene.md$' "$work/third.log" || fail "an untouched stale managed file was not updated"
bash "$adopt" "$repo" > "$work/fourth.log"
grep -q '^edited   scripts/check-pr-size.sh$' "$work/fourth.log" || fail "an edited file was not reported on the next run"

# 3b. a new version of the plugin: a hand-edited file it changes is kept and named for comparison,
#     an untouched one is updated, and nothing is lost from the lock
newer="$work/newer-plugin"
cp -RL "$PWD/plugins/core" "$newer"
echo "# upstream change" >> "$newer/skills/adopt/assets/managed/scripts/check-pr-size.sh"
echo "upstream change" >> "$newer/skills/adopt/assets/managed/docs/dev/docs-hygiene.md"
bash "$newer/skills/adopt/adopt.sh" "$repo" > "$work/newer.log"
grep -q '^kept     scripts/check-pr-size.sh$' "$work/newer.log" || fail "a hand-edited file that the new version changes was not kept"
grep -qxF "         new version: $newer/skills/adopt/assets/managed/scripts/check-pr-size.sh" "$work/newer.log" \
  || fail "the kept file's new version was not named"
grep -q '^# local change$' "$repo/scripts/check-pr-size.sh" || fail "a hand-edited file was overwritten by a new version"
grep -q '^updated  docs/dev/docs-hygiene.md$' "$work/newer.log" || fail "an untouched file was not updated to the new version"
grep -q '^upstream change$' "$repo/docs/dev/docs-hygiene.md" || fail "the new version's content did not arrive"
diff -u "$repo/scripts/check-pr-size.sh" "$newer/skills/adopt/assets/managed/scripts/check-pr-size.sh" > "$work/kept.diff" || true
grep -q '^-# local change$' "$work/kept.diff" || fail "the diff of a kept file does not show the local change"
grep -q '^+# upstream change$' "$work/kept.diff" || fail "the diff of a kept file does not show the new version's change"
# Taking the new version by hand makes the file untouched again.
cp "$newer/skills/adopt/assets/managed/scripts/check-pr-size.sh" "$repo/scripts/check-pr-size.sh"
bash "$newer/skills/adopt/adopt.sh" "$repo" > "$work/newer2.log"
grep -q '^same     scripts/check-pr-size.sh$' "$work/newer2.log" || fail "a file taken from the new version was not seen as the same"
# Back to the current version for the rest of the test.
bash "$adopt" "$repo" > /dev/null
cp "$PWD/plugins/core/skills/adopt/assets/managed/scripts/check-pr-size.sh" "$repo/scripts/check-pr-size.sh"
cp "$PWD/plugins/core/skills/adopt/assets/managed/docs/dev/docs-hygiene.md" "$repo/docs/dev/docs-hygiene.md"
bash "$adopt" "$repo" > /dev/null

# 4. an owned file is not overwritten
echo "mine" > "$repo/AGENTS.md"
bash "$adopt" "$repo" > "$work/fifth.log"
grep -q '^exists   AGENTS.md$' "$work/fifth.log" || fail "an owned file was not reported as existing"
[ "$(cat "$repo/AGENTS.md")" = "mine" ] || fail "an owned file was overwritten"

# 5. a second plugin adds its files and keeps the first plugin's lines in the lock
second="$work/second"; mkdir "$second"; git -C "$second" init -q
bash "$adopt" "$second" > /dev/null
core_lines=$(grep -c ' core$' "$second/.agents/methodology.lock")
bash "$PWD/plugins/aws-ops/skills/adopt/adopt.sh" "$second" > "$work/ops.log"
grep -q '^added    ops/raw/.gitignore$' "$work/ops.log" || fail "aws-ops did not add ops/raw/.gitignore"
grep -q '^created  ops/apps.json$' "$work/ops.log" || fail "aws-ops did not create ops/apps.json"
[ "$(grep -c ' core$' "$second/.agents/methodology.lock")" = "$core_lines" ] || fail "aws-ops dropped lines of core from the lock"
grep -q '^file [0-9a-f]* ops/raw/.gitignore aws-ops$' "$second/.agents/methodology.lock" || fail "the lock has no line for aws-ops"
bash "$adopt" "$second" > "$work/core-again.log"
if grep -Eqv '^(same|exists) ' "$work/core-again.log"; then fail "core changed something after aws-ops"; fi
grep -q ' aws-ops$' "$second/.agents/methodology.lock" || fail "core dropped lines of aws-ops from the lock"
touch "$second/ops/raw/fetched.json"
[ -z "$(git -C "$second" status --porcelain -- ops/raw/fetched.json)" ] || fail "ops/raw is not ignored"
make -C "$second" check > "$work/check2.log" 2>&1 || { cat "$work/check2.log" >&2; fail "make check does not pass after aws-ops"; }

# 6. aws-iac adds its check; with stub tools the check runs every step and fails when one fails
bash "$PWD/plugins/aws-iac/skills/adopt/adopt.sh" "$second" > "$work/iac.log"
grep -q '^added    scripts/check-iac.sh$' "$work/iac.log" || fail "aws-iac did not add scripts/check-iac.sh"
grep -q ' aws-ops$' "$second/.agents/methodology.lock" || fail "aws-iac dropped lines of aws-ops from the lock"
mkdir -p "$second/envs/dev" "$second/infra" "$work/stub"
echo 'terraform {}' > "$second/envs/dev/main.tf"
echo '{}' > "$second/infra/cdk.json"
touch "$second/envs/dev/.tflint.hcl"
printf 'terraform envs/dev\ncdk infra  # the app\n' >> "$second/scripts/iac-roots.txt"
for tool in terraform tflint npx; do
  cat > "$work/stub/$tool" <<STUB
#!/usr/bin/env bash
echo "$tool \$*" >> "\$STUB_LOG"
[ "\${STUB_FAIL:-}" != "$tool" ]
STUB
  chmod +x "$work/stub/$tool"
done
STUB_LOG="$work/iac-calls.log" PATH="$work/stub:$PATH" bash "$second/scripts/check-iac.sh" > "$work/iac-check.log" 2>&1 \
  || { cat "$work/iac-check.log" >&2; fail "check-iac.sh failed with passing tools"; }
for call in 'terraform fmt -check -recursive -diff envs/dev' 'terraform -chdir=envs/dev init -backend=false -input=false' \
            'terraform -chdir=envs/dev validate' 'tflint --chdir=envs/dev' 'npx cdk synth --quiet'; do
  grep -qxF -- "$call" "$work/iac-calls.log" || fail "check-iac.sh did not run: $call"
done
python3 - "$work/iac-calls.log" <<'PY' || fail "check-iac.sh made a call the aws-iac guard would not let through"
import sys
sys.path.insert(0, "plugins/aws-iac/hooks")
from guard_iac import JUDGES
bad = []
for line in open(sys.argv[1]).read().splitlines():
    name, *args = line.split()
    if name in JUDGES and JUDGES[name](args)[0] != "allow":
        bad.append(line)
    if name == "npx" and JUDGES["cdk"](args[1:])[0] != "allow":
        bad.append(line)
print("\n".join(bad), file=sys.stderr)
sys.exit(1 if bad else 0)
PY
if STUB_FAIL=tflint STUB_LOG="$work/iac-calls2.log" PATH="$work/stub:$PATH" bash "$second/scripts/check-iac.sh" > /dev/null 2>&1; then
  fail "check-iac.sh passed although a tool failed"
fi
if STUB_LOG=/dev/null PATH="/usr/bin:/bin" bash "$second/scripts/check-iac.sh" > /dev/null 2>&1; then
  fail "check-iac.sh passed although the tools are missing"
fi

# 7. knowledge: the mapping check passes with catalog IDs, and catches the usual mistakes
bash "$PWD/plugins/knowledge/skills/adopt/adopt.sh" "$second" > "$work/knowledge.log"
grep -q '^added    scripts/check-knowledge.py$' "$work/knowledge.log" || fail "knowledge did not add scripts/check-knowledge.py"
grep -q '^added    scripts/knowledge/catalog.py$' "$work/knowledge.log" || fail "knowledge did not add its catalog reader"
[ ! -L "$second/scripts/knowledge/catalog.py" ] || fail "the catalog reader was copied as a symbolic link"
grep -q '^created  docs/knowledge/practices.md$' "$work/knowledge.log" || fail "knowledge did not create the practices mapping"
grep -q ' aws-iac$' "$second/.agents/methodology.lock" || fail "knowledge dropped lines of aws-iac from the lock"
kcheck() { python3 "$second/scripts/check-knowledge.py" > "$work/kcheck.log" 2>&1; }
kcheck || { cat "$work/kcheck.log" >&2; fail "the mapping check fails right after adoption"; }
practices="$second/docs/knowledge/practices.md"
cp "$practices" "$work/practices.orig"
python3 plugins/knowledge/skills/adopt/list_items.py practices general testing > "$work/rows.txt"
python3 - "$practices" "$work/rows.txt" <<'PY'
import sys
path, rows = sys.argv[1], open(sys.argv[2]).read()
text = open(path).read()
head = "| 項目 | このリポジトリでの場面 | このプロジェクトの立場 |\n| --- | --- | --- |\n"
open(path, "w").write(text.replace(head, head + rows, 1))
PY
kcheck || { cat "$work/kcheck.log" >&2; fail "the mapping check fails with rows from the catalog"; }
inject() { # inject <text after the header of 使う項目>
  cp "$work/practices.orig" "$practices"
  python3 - "$practices" "$1" <<'PY'
import sys
path, extra = sys.argv[1], sys.argv[2].replace("\\n", "\n")
text = open(path).read()
head = "| 項目 | このリポジトリでの場面 | このプロジェクトの立場 |\n| --- | --- | --- |\n"
open(path, "w").write(text.replace(head, head + extra + "\n", 1))
PY
}
inject '| `no-such-entry` | — | 未定 |'
kcheck && fail "an ID that is not in the catalog was accepted"
inject '| `yagni` | — | 未定 |\n| `yagni` | — | 未定 |'
kcheck && fail "an ID listed twice was accepted"
inject '| `yagni` | — |  |'
kcheck && fail "an empty 立場 was accepted"
inject '| yagni | — | 未定 |'
kcheck && fail "an ID without backticks was accepted"
cp "$work/practices.orig" "$practices"
printf '\n### 架空の知見\n\n| 欄 | 内容 |\n| --- | --- |\n| ID | `local-thing` |\n' >> "$practices"
python3 - "$practices" <<'PY'
import sys
path = sys.argv[1]
text = open(path).read()
# move the appended entry under このリポジトリの項目
entry = text[text.index("\n### 架空の知見"):]
text = text[:text.index("\n### 架空の知見")]
text = text.replace("## 外したもの", entry.strip("\n") + "\n\n## 外したもの", 1)
open(path, "w").write(text)
PY
kcheck && fail "a local entry with missing fields was accepted"
grep -q "missing field" "$work/kcheck.log" || fail "the local entry was not checked for its fields"
cp "$work/practices.orig" "$practices"

# 7b. a local entry written for react@19 fails while the repository uses react@18, and passes with 19
python3 - "$practices" <<'PY'
import sys
path = sys.argv[1]
text = open(path).read()
entry = """### 架空の React の知見

| 欄 | 内容 |
| --- | --- |
| ID | `local-react-thing` |
| 出どころ | 架空の出どころ。https://example.com/react |
| ソース | なし |
| 何を言っているか | 架空。 |
| 確からしさ | 架空。 |
| 当たるべき場面 | 架空。 |
| 判断の問い | 架空。 |
| 対象 | `react@19` |
| 確認 | 2026-11-15 / 間隔 90 日 |

"""
head = "| 項目 | このリポジトリでの場面 | このプロジェクトの立場 |\n| --- | --- | --- |\n"
text = text.replace(head, head + "| `local-react-thing` | — | 未定 |\n", 1)
text = text.replace("## 外したもの", entry + "## 外したもの", 1)
open(path, "w").write(text)
PY
mkdir -p "$second/web"
printf '{"packages": {"": {}, "node_modules/react": {"version": "18.3.1"}, "node_modules/x/node_modules/react": {"version": "19.0.0"}}}\n' > "$second/web/package-lock.json"
kcheck && fail "an entry written for react@19 passed while the repository uses react@18"
grep -q 'uses react@18' "$work/kcheck.log" || { cat "$work/kcheck.log" >&2; fail "the version mismatch was not reported"; }
printf '{"packages": {"node_modules/react": {"version": "19.1.0"}}}\n' > "$second/web/package-lock.json"
kcheck || { cat "$work/kcheck.log" >&2; fail "an entry written for react@19 failed while the repository uses react@19"; }
printf 'nodejs 22.4.0\ngolang 1.27.2\n' > "$second/.tool-versions"
printf 'provider "registry.terraform.io/hashicorp/aws" {\n  version     = "5.70.0"\n}\n' > "$second/envs/dev/.terraform.lock.hcl"
python3 - "$second" <<'PY' || fail "dependency versions were not read from .tool-versions, .terraform.lock.hcl or package-lock.json"
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("ck", sys.argv[1] + "/scripts/check-knowledge.py")
ck = importlib.util.module_from_spec(spec); spec.loader.exec_module(ck)
v = ck.used_versions()
assert ("22", "4") == v["node"][0][:2], v.get("node")
assert ("1", "27") == v["go"][0][:2], v.get("go")
assert ("5", "70") == v["hashicorp/aws"][0][:2], v.get("hashicorp/aws")
assert len(v["react"]) == 1, v["react"]
PY
# Python: a lock file wins over the ranges in pyproject.toml; without one, the lower bound is used
mkdir -p "$second/svc" "$second/lib"
printf '[project]\nname = "svc"\nrequires-python = ">=3.12"\ndependencies = ["Requests>=2.0"]\n' > "$second/svc/pyproject.toml"
printf 'version = 1\n\n[[package]]\nname = "requests"\nversion = "2.32.3"\n\n[[package]]\nname = "Typing_Extensions"\nversion = "4.12.2"\n' > "$second/svc/uv.lock"
printf '[project]\nname = "lib"\ndependencies = ["boto3[crt] >= 1.35, <2", "attrs"]\n' > "$second/lib/pyproject.toml"
printf '[[package]]\nname = "pydantic"\nversion = "2.9.2"\n' > "$second/poetry.lock"
python3 - "$second" <<'PY' || fail "Python dependency versions were not read from pyproject.toml, uv.lock or poetry.lock"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ck", sys.argv[1] + "/scripts/check-knowledge.py")
ck = importlib.util.module_from_spec(spec); spec.loader.exec_module(ck)
v = ck.used_versions()
got = {name: sorted((m, n, f) for m, n, f in rows) for name, rows in v.items()}
assert [r[:2] for r in got["requests"]] == [("2", "32")], got.get("requests")  # the lock, not ">=2.0"
assert ("4", "12") == got["typing-extensions"][0][:2], got.get("typing-extensions")
assert ("1", "35") == got["boto3"][0][:2], got.get("boto3")
assert "attrs" not in got, got.get("attrs")
assert ("2", "9") == got["pydantic"][0][:2], got.get("pydantic")
assert ("3", "12") == got["python"][0][:2], got.get("python")
PY
rm -r "${second:?}/svc" "${second:?}/lib" "${second:?}/poetry.lock"
rm -r "${second:?}/web" "${second:?}/.tool-versions" "${second:?}/envs/dev/.terraform.lock.hcl"
cp "$work/practices.orig" "$practices"

# 8. --dry-run writes nothing
dry="$work/dry"; mkdir "$dry"; git -C "$dry" init -q
bash "$adopt" --dry-run "$dry" > /dev/null
[ "$(ls -A "$dry")" = ".git" ] || fail "--dry-run wrote files"

echo "test-adopt: ok"
