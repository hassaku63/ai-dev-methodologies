#!/usr/bin/env bash
# Copies the files of ai-dev-methodologies (core) into a repository.
#
# Usage: bash adopt.sh [--dry-run] <target-repository-root>
#
# Two kinds of files (ADR-0003 of ai-dev-methodologies):
#   managed  copied as they are; their hashes go to .agents/methodology.lock.
#            On a later run a managed file is replaced only if it still has the
#            hash in the lock. A file changed by hand is kept and reported.
#   owned    created from a template only when absent. Never overwritten.
#
# Prints one line per file: "<result> <path>". Needs bash, git, awk, sed and
# sha256sum or shasum.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
assets="$here/assets"

dry=0
if [ "${1:-}" = "--dry-run" ]; then dry=1; shift; fi
target=${1:?usage: adopt.sh [--dry-run] <target-repository-root>}
target=$(cd "$target" && pwd -P)

top=$(git -C "$target" rev-parse --show-toplevel 2>/dev/null) || { echo "adopt: $target is not a git repository" >&2; exit 2; }
top=$(cd "$top" && pwd -P)
[ "$top" = "$target" ] || { echo "adopt: $target is not the repository root ($top)" >&2; exit 2; }

project=$(basename "$target")
lock="$target/.agents/methodology.lock"

sha() {
  if command -v sha256sum >/dev/null; then sha256sum "$1" | cut -d' ' -f1
  else shasum -a 256 "$1" | cut -d' ' -f1; fi
}
locked_hash() {
  [ -f "$lock" ] || return 0
  awk -v p="$1" '$1 == "file" && $3 == p { print $2 }' "$lock"
}
put() { # put <source> <destination>
  [ "$dry" -eq 1 ] && return 0
  mkdir -p "$(dirname "$2")"
  cp "$1" "$2"
}

entries=$(mktemp)
trap 'rm -f "$entries"' EXIT

# --- managed ---------------------------------------------------------------
while IFS= read -r src; do
  rel="${src#"$assets/managed/"}"
  dst="$target/$rel"
  new=$(sha "$src")
  if [ ! -e "$dst" ]; then
    put "$src" "$dst"; echo "added    $rel"; echo "file $new $rel" >> "$entries"
    continue
  fi
  cur=$(sha "$dst")
  old=$(locked_hash "$rel")
  if [ "$cur" = "$new" ]; then
    echo "same     $rel"; echo "file $new $rel" >> "$entries"
  elif [ -n "$old" ] && [ "$cur" = "$old" ]; then
    put "$src" "$dst"; echo "updated  $rel"; echo "file $new $rel" >> "$entries"
  else
    # Changed by hand, or it was there before the first adoption.
    echo "kept     $rel"; echo "file ${old:-local} $rel" >> "$entries"
  fi
done < <(find "$assets/managed" -type f | sort)

# --- owned -----------------------------------------------------------------
while IFS= read -r src; do
  rel="${src#"$assets/owned/"}"
  rel="${rel%.tmpl}"
  dst="$target/$rel"
  if [ -e "$dst" ]; then
    echo "exists   $rel"
    continue
  fi
  if [ "$dry" -eq 0 ]; then
    mkdir -p "$(dirname "$dst")"
    sed "s/{{PROJECT}}/$project/g" "$src" > "$dst"
  fi
  echo "created  $rel"
done < <(find "$assets/owned" -type f -name '*.tmpl' | sort)

# --- lock ------------------------------------------------------------------
if [ "$dry" -eq 0 ]; then
  mkdir -p "$(dirname "$lock")"
  {
    echo "# Written by ai-dev-methodologies (core) adopt.sh. Do not edit by hand."
    echo "# file <sha256 at adoption | local> <path>: 'local' marks a file kept as found."
    echo "source hassaku63/ai-dev-methodologies"
    echo "plugin core"
    cat "$entries"
  } > "$lock"
fi
