#!/usr/bin/env bash
# Checks the plan summary of the fictional example (examples/iac-example):
#   1. The script's output equals the committed summary.
#   2. No attribute value of the plan appears in the summary.
#   3. A plan without changes says so; a file that is not a plan is rejected.
# Part of `make check`. Needs bash and python3.
set -euo pipefail
cd "$(dirname "$0")/.."

script=plugins/aws-iac/skills/plan/summarize_plan.py
ex=examples/iac-example
work=$(mktemp -d)
trap 'rm -rf "${work:?}"' EXIT
fail() { echo "test-plan: FAILED: $*" >&2; exit 1; }

python3 "$script" "$ex/fixtures/plan.json" > "$work/summary.md"
diff -u "$ex/plan-summary.md" "$work/summary.md" \
  || fail "the summary differs from the committed one (see examples/iac-example/README.md to regenerate)"

grep -q 'fictional-.*-password' "$ex/fixtures/plan.json" || fail "the fixture holds no value to look for"
if grep -Eq 'fictional-(old|new)-password|python3\.12|0\.0\.0\.0/0' "$work/summary.md"; then
  fail "an attribute value leaked into the summary"
fi
grep -q 'data\.aws_caller_identity' "$work/summary.md" && fail "a data source was listed as a change"

echo '{"format_version": "1.2", "resource_changes": []}' > "$work/empty.json"
python3 "$script" "$work/empty.json" | grep -q '変更はない' || fail "an empty plan does not say that nothing changes"

echo '{"Findings": []}' > "$work/other.json"
if python3 "$script" "$work/other.json" > /dev/null 2>&1; then fail "a file that is not a plan was accepted"; fi

echo "test-plan: ok"
