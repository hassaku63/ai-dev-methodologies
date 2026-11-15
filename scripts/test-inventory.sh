#!/usr/bin/env bash
# Checks the inventory of the fictional example (examples/ops-example):
#   1. summarize_inventory.py's output equals the committed record.
#   2. collect.sh, run against a stub `aws`, makes only calls the aws-ops guard
#      would let through, batches ECS services by ten, and goes on after a
#      failed call, leaving an .error file that the record mentions.
# Part of `make check`. Needs bash and python3.
set -euo pipefail
cd "$(dirname "$0")/.."

skill=plugins/aws-ops/skills/inventory
ex=examples/ops-example
work=$(mktemp -d)
trap 'rm -rf "${work:?}"' EXIT
fail() { echo "test-inventory: FAILED: $*" >&2; exit 1; }

# 1. the record of the example
python3 "$skill/summarize_inventory.py" --raw "$ex/fixtures/inventory" --apps "$ex/ops/apps.json" \
  --account 111122223333 --date 2026-11-01 > "$work/inventory.md"
diff -u "$ex/ops/inventory.md" "$work/inventory.md" \
  || fail "the record differs from the committed one (see examples/ops-example/README.md to regenerate)"

# 2. collect.sh against a stub aws
mkdir "$work/bin"
cat > "$work/bin/aws" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$AWS_STUB_LOG"
case "$1 $2" in
  "ecs list-clusters") echo '{"clusterArns": ["arn:aws:ecs:us-east-1:111122223333:cluster/example"]}' ;;
  "ecs list-services")
    printf '{"serviceArns": ['
    for i in 1 2 3 4 5 6 7 8 9 10 11; do printf '"arn:aws:ecs:us-east-1:111122223333:service/example/svc-%s", ' "$i"; done
    echo '"arn:aws:ecs:us-east-1:111122223333:service/example/svc-12"]}' ;;
  "rds describe-db-instances") echo "An error occurred (AccessDenied) when calling the DescribeDBInstances operation" >&2; exit 254 ;;
  *) echo '{}' ;;
esac
STUB
chmod +x "$work/bin/aws"
AWS_STUB_LOG="$work/calls.log" PATH="$work/bin:$PATH" bash "$skill/collect.sh" "$work/raw" us-east-1 > "$work/collect.log" 2>&1 \
  || { cat "$work/collect.log" >&2; fail "collect.sh failed"; }

python3 - "$work/calls.log" <<'PY' || fail "collect.sh made a call the guard would not let through"
import sys
sys.path.insert(0, "plugins/aws-ops/hooks")
from guard_aws import judge
bad = [line for line in open(sys.argv[1]).read().splitlines() if judge(line.split())[0] != "allow"]
print("\n".join(bad), file=sys.stderr)
sys.exit(1 if bad else 0)
PY
[ "$(grep -c '^ecs describe-services ' "$work/calls.log")" = 2 ] || fail "twelve ECS services were not described in two batches"
[ -f "$work/raw/us-east-1/db-instances.error" ] || fail "a failed call left no .error file"
[ ! -e "$work/raw/us-east-1/db-instances.json" ] || fail "a failed call left a .json file"
[ -f "$work/raw/us-east-1/vpcs.json" ] || fail "a call after nothing failed left no file"
python3 "$skill/summarize_inventory.py" --raw "$work/raw" > "$work/partial.md"
grep -q '取得できなかったもの.*db-instances' "$work/partial.md" || fail "the record does not mention the part that could not be fetched"

echo "test-inventory: ok"
