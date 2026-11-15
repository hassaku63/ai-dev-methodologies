#!/usr/bin/env bash
# Adopts core into an empty repository and checks the result:
#   1. `make check` passes right after adoption.
#   2. A second run changes nothing.
#   3. A managed file changed by hand is kept; an untouched one is updated.
#   4. An owned file is never overwritten.
#   5. A second plugin (aws-ops) keeps the lock lines of the first.
#   6. aws-iac's check runs every step with stub tools, fails when a tool
#      fails or is missing, and calls nothing its guard would stop.
#   7. knowledge's mapping check accepts catalog IDs and rejects unknown,
#      duplicated, empty and malformed rows and local entries.
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
grep -q '^kept     scripts/check-pr-size.sh$' "$work/third.log" || fail "a hand-edited managed file was not kept"
grep -q '^# local change$' "$repo/scripts/check-pr-size.sh" || fail "a hand-edited managed file was overwritten"
grep -q '^updated  docs/dev/docs-hygiene.md$' "$work/third.log" || fail "an untouched stale managed file was not updated"
bash "$adopt" "$repo" > "$work/fourth.log"
grep -q '^kept     scripts/check-pr-size.sh$' "$work/fourth.log" || fail "a kept file was not reported on the next run"

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

# 8. --dry-run writes nothing
dry="$work/dry"; mkdir "$dry"; git -C "$dry" init -q
bash "$adopt" --dry-run "$dry" > /dev/null
[ "$(ls -A "$dry")" = ".git" ] || fail "--dry-run wrote files"

echo "test-adopt: ok"
