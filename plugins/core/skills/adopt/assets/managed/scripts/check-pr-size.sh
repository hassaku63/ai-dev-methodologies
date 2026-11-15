#!/usr/bin/env bash
# Counts the lines a change touches and enforces the PR size budget:
#   more than 600 lines: warn (exit 0)    more than 1000 lines: fail (exit 1)
# A line counts once when added and once when removed. Files git treats as
# binary do not count, nor do the paths listed in scripts/pr-size-excludes.txt
# (one git pathspec pattern per line, e.g. package-lock.json or *.gen.ts).
#
# Usage: bash scripts/check-pr-size.sh <base> [head]
#   Compares head (default HEAD) with its merge base with <base>.
#   In CI on a pull request, HEAD is the merge commit and <base> is HEAD^1.
# Not part of `make check`: it needs a base to compare with (docs/dev/harness.md).
#
# Managed by ai-dev-methodologies (core). Local edits are kept on update, but
# the file then stops receiving updates; see .agents/methodology.lock.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

base=${1:?usage: check-pr-size.sh <base> [head]}
head=${2:-HEAD}
warn_over=600
fail_over=1000

excludes=()
if [ -f scripts/pr-size-excludes.txt ]; then
  while IFS= read -r line; do
    line="${line%%#*}"
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    [ -n "$line" ] && excludes+=(":(exclude)$line")
  done < scripts/pr-size-excludes.txt
fi

# "added<TAB>removed<TAB>path"; binary files show "-" and are skipped.
# quotePath=false keeps non-ASCII file names readable in the list.
if ! stat=$(git -c core.quotePath=false diff --numstat "$base...$head" -- . ${excludes[@]+"${excludes[@]}"}); then
  echo "pr-size: cannot compare $base...$head (is the base fetched?)" >&2
  exit 2
fi
counted=$(printf '%s\n' "$stat" | awk -F '\t' 'NF == 3 && $1 != "-" { print $1 + $2 "\t" $3 }' | sort -t $'\t' -k1,1nr)
total=$(printf '%s\n' "$counted" | awk -F '\t' 'NF { s += $1 } END { print s + 0 }')

echo "pr-size: $total lines changed against $base (binaries and scripts/pr-size-excludes.txt not counted)"
if [ -n "$counted" ]; then
  echo "pr-size: largest files:"
  printf '%s\n' "$counted" | head -n 5 | awk -F '\t' '{ printf "  %6d  %s\n", $1, $2 }'
fi

if [ "$total" -gt "$fail_over" ]; then
  echo "::error::This change touches $total lines, over the budget of $fail_over. Split it into slices (docs/dev/workflow.md)."
  exit 1
fi
if [ "$total" -gt "$warn_over" ]; then
  echo "::warning::This change touches $total lines, over $warn_over. Consider splitting it."
fi
exit 0
