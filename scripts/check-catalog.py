#!/usr/bin/env python3
"""Checks the shape of the knowledge catalog (plugins/knowledge/catalog). Part of `make check`.

It looks only at the files, never at the date or the network, so the same
commit always gives the same result.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/knowledge/lib"))
from catalog import check, load  # noqa: E402


def main():
    root = ROOT / "plugins/knowledge/catalog"
    problems = check(root)
    if problems:
        print("\n".join(f"catalog-check: {p}" for p in problems), file=sys.stderr)
        print("catalog-check: FAILED", file=sys.stderr)
        return 1
    found = load(root)
    packs = sorted({(k, p) for k, p, *_ in found})
    print(f"catalog-check: ok ({len(found)} entries in {len(packs)} packs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
