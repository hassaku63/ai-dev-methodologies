#!/usr/bin/env python3
"""Prints catalog entries as rows for a mapping table.

Usage: list_items.py <practices|standards> [<pack> ...]

With no pack, lists the packs and how many entries each holds. With packs,
prints one table row per entry: the ID, "—" and "未定" for practices, or the
ID and "—" for standards.
Python 3 standard library only.
"""
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "lib"))
from catalog import FIELDS, load  # noqa: E402


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in FIELDS:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    kind, packs = sys.argv[1], sys.argv[2:]
    found = [e for e in load(ROOT / "catalog") if e[0] == kind]
    if not packs:
        for pack, n in sorted(Counter(e[1] for e in found).items()):
            print(f"{pack}\t{n}")
        return 0
    unknown = set(packs) - {e[1] for e in found}
    if unknown:
        print(f"list-items: no such pack: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    for _kind, pack, title, fields, _path, _line in found:
        if pack in packs:
            tail = " | — | 未定 |" if kind == "practices" else " | — |"
            print(f"| {fields['ID']}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
