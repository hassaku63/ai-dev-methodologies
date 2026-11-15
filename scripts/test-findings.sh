#!/usr/bin/env bash
# Checks the findings report of the fictional example (examples/ops-example):
#   1. The script's output equals the committed report.
#   2. Findings that need no attention are left out, and --all counts them.
#   3. A broken apps file is rejected.
# Part of `make check`. Needs bash and python3.
set -euo pipefail
cd "$(dirname "$0")/.."

script=plugins/aws-ops/skills/findings/group_findings.py
ex=examples/ops-example
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
fail() { echo "test-findings: FAILED: $*" >&2; exit 1; }

python3 "$script" --apps "$ex/ops/apps.json" --date 2026-11-01 "$ex/fixtures/findings.json" > "$work/report.md"
diff -u "$ex/ops/findings/2026-11-01.md" "$work/report.md" \
  || fail "the report differs from the committed one (see examples/ops-example/README.md to regenerate)"

grep -q 'EC2\.7\|CloudTrail\.1\|EC2\.2\]' "$work/report.md" && fail "a finding that needs no attention was counted"
python3 "$script" --apps "$ex/ops/apps.json" --all "$ex/fixtures/findings.json" > "$work/all.md"
grep -q 'CloudTrail\.1' "$work/all.md" || fail "--all did not count every finding"

echo '{"apps": []}' > "$work/empty.json"
python3 "$script" --apps "$work/empty.json" "$ex/fixtures/findings.json" > "$work/empty.md"
grep -q '^| order-api ' "$work/empty.md" && fail "an application appeared without a definition"

echo '{"apps": [{"name": "x", "match": {"tag": {}}}]}' > "$work/bad.json"
if python3 "$script" --apps "$work/bad.json" "$ex/fixtures/findings.json" > /dev/null 2>&1; then
  fail "an unknown matcher was accepted"
fi

echo "test-findings: ok"
