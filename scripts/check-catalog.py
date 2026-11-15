#!/usr/bin/env python3
"""Checks the shape of the knowledge catalog (plugins/knowledge/catalog). Part of `make check`.

Also checks that the ID list adoption copies (.agents/knowledge-ids.txt in the
assets of the knowledge plugin) matches the catalog. `--write-ids` rewrites it.

It looks only at the files, never at the date or the network, so the same
commit always gives the same result.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/knowledge/lib"))
from catalog import check, load, snapshot  # noqa: E402


def main():
    root = ROOT / "plugins/knowledge/catalog"
    if sys.argv[1:] == ["--write-ids"]:
        ids = ROOT / "plugins/knowledge/skills/adopt/assets/managed/.agents/knowledge-ids.txt"
        ids.write_text(snapshot(root), encoding="utf-8")
        print(f"catalog-check: wrote {ids.relative_to(ROOT)}")
        return 0
    problems = check(root)
    if problems:
        print("\n".join(f"catalog-check: {p}" for p in problems), file=sys.stderr)
        print("catalog-check: FAILED", file=sys.stderr)
        return 1
    ids = ROOT / "plugins/knowledge/skills/adopt/assets/managed/.agents/knowledge-ids.txt"
    if not ids.exists() or ids.read_text(encoding="utf-8") != snapshot(root):
        print(f"catalog-check: {ids.relative_to(ROOT)} does not match the catalog; regenerate it with"
              " `python3 scripts/check-catalog.py --write-ids`", file=sys.stderr)
        return 1
    found = load(root)
    packs = sorted({(k, p) for k, p, *_ in found})
    print(f"catalog-check: ok ({len(found)} entries in {len(packs)} packs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
