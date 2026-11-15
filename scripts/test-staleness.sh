#!/usr/bin/env bash
# Checks the date part of the catalog staleness report (scripts/knowledge-staleness.py
# --offline) with a fixed date, so the result does not depend on today:
#   1. On the day the entries were checked, nothing is reported.
#   2. Long after it, every entry is reported, and the exit status is 3.
# Part of `make check`. Needs bash and python3.
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "test-staleness: FAILED: $*" >&2; exit 1; }

first=$(python3 - <<'PY'
import sys
sys.path.insert(0, "plugins/knowledge/lib")
from catalog import load
print(min(fields["確認"].split()[0] for _k, _p, _t, fields, _f, _l in load("plugins/knowledge/catalog")))
PY
)
TODAY=$first python3 scripts/knowledge-staleness.py --offline > /dev/null || fail "entries were reported on the day they were checked"
status=0
TODAY=2999-01-01 python3 scripts/knowledge-staleness.py --offline > "${TMPDIR:-/tmp}/staleness.$$" || status=$?
count=$(grep -c '^- ' "${TMPDIR:-/tmp}/staleness.$$" || true)
rm -f "${TMPDIR:-/tmp}/staleness.$$"
[ "$status" = 3 ] || fail "the exit status was $status, not 3, with overdue entries"
total=$(python3 -c 'import sys; sys.path.insert(0, "plugins/knowledge/lib"); from catalog import load; print(len(load("plugins/knowledge/catalog")))')
[ "$count" = "$total" ] || fail "$count of $total entries were reported as overdue"
echo "test-staleness: ok"
