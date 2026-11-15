#!/usr/bin/env bash
# Adopts core into an empty repository and checks the result:
#   1. `make check` passes right after adoption.
#   2. A second run changes nothing.
#   3. A managed file changed by hand is kept; an untouched one is updated.
#   4. An owned file is never overwritten.
# Part of `make check`. Needs bash, git, make.
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

# 5. --dry-run writes nothing
dry="$work/dry"; mkdir "$dry"; git -C "$dry" init -q
bash "$adopt" --dry-run "$dry" > /dev/null
[ "$(ls -A "$dry")" = ".git" ] || fail "--dry-run wrote files"

echo "test-adopt: ok"
