#!/usr/bin/env bash
# Checks the infrastructure code without touching any infrastructure or state.
# Part of `make check` (target iac-check) and CI.
#
# The roots to check are listed in scripts/iac-roots.txt, one per line:
#   terraform <directory>   fmt -check, init -backend=false, validate, and
#                           tflint when the directory has a .tflint.hcl
#   cdk <directory>         cdk synth (the dependencies must be installed)
#
# A tool that a listed root needs and that is not installed is a failure, not
# a skip: a check that silently does nothing protects nothing.
# Needs bash, plus terraform / tflint / npx for the roots that use them.
#
# Managed by ai-dev-methodologies (aws-iac). Local edits are kept on update, but
# the file then stops receiving updates; see .agents/methodology.lock.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

roots=scripts/iac-roots.txt
[ -f "$roots" ] || { echo "iac-check: $roots not found" >&2; exit 1; }

failed=0
problem() { echo "iac-check: $*" >&2; failed=$((failed + 1)); }
need() { command -v "$1" >/dev/null || { problem "$1 not found (needed for: $2)"; return 1; }; }
step() { # step <description> <command...>
  local what=$1
  shift
  if "$@"; then echo "iac-check: ok      $what"; else problem "FAILED  $what"; fi
}

in_dir() { # in_dir <directory> <command...>
  local dir=$1
  shift
  (cd "$dir" && "$@")
}

checked=0
while IFS= read -r line || [ -n "$line" ]; do
  line="${line%%#*}"
  read -r kind dir extra <<< "$line"
  [ -z "${kind:-}" ] && continue
  if [ -z "${dir:-}" ] || [ -n "${extra:-}" ]; then problem "$roots: cannot read the line: $line"; continue; fi
  [ -d "$dir" ] || { problem "$roots: no such directory: $dir"; continue; }
  checked=$((checked + 1))
  case "$kind" in
    terraform)
      need terraform "$dir" || continue
      step "terraform fmt       $dir" terraform fmt -check -recursive -diff "$dir"
      step "terraform init      $dir" terraform -chdir="$dir" init -backend=false -input=false
      step "terraform validate  $dir" terraform -chdir="$dir" validate
      if [ -f "$dir/.tflint.hcl" ]; then
        need tflint "$dir/.tflint.hcl" && step "tflint              $dir" tflint --chdir="$dir"
      fi
      ;;
    cdk)
      need npx "$dir" || continue
      step "cdk synth           $dir" in_dir "$dir" npx cdk synth --quiet
      ;;
    *) problem "$roots: unknown kind: $kind (expected terraform or cdk)" ;;
  esac
done < "$roots"

if [ "$failed" -gt 0 ]; then
  echo "iac-check: FAILED ($failed problems)" >&2
  exit 1
fi
echo "iac-check: ok ($checked roots)"
