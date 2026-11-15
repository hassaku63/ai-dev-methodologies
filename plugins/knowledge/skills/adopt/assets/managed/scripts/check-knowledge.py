#!/usr/bin/env python3
"""Checks the knowledge mapping tables of this repository. Part of `make check`.

  docs/knowledge/practices.md   which practices this repository uses
  docs/knowledge/standards.md   which standards this repository uses

Each file has a "## 使う項目" table that names catalog entries by ID, an
optional "## このリポジトリの項目" section with entries of its own (in the
catalog's format), and an optional "## 外したもの" table.

The catalog itself lives in the ai-dev-methodologies plugin `knowledge`; the
IDs it holds are listed in .agents/knowledge-ids.txt, which adoption copies
and updates. An ID that is missing there may be newer than the list: adopt
again to refresh it.

It looks only at files, never at the date or the network.
Python 3 standard library only.

Managed by ai-dev-methodologies (knowledge). Local edits are kept on update, but
the file then stops receiving updates; see .agents/methodology.lock.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent / "knowledge"))
from catalog import ID, check_entry, entries  # noqa: E402

MAPPINGS = {
    "practices": ("docs/knowledge/practices.md", ["項目", "このリポジトリでの場面", "このプロジェクトの立場"]),
    "standards": ("docs/knowledge/standards.md", ["項目", "このリポジトリとの接点"]),
}
LIMIT = 40


def catalog_ids():
    path = ROOT / ".agents/knowledge-ids.txt"
    ids = {kind: set() for kind in MAPPINGS}
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2 and not line.startswith("#") and parts[0] in ids:
            ids[parts[0]].add(parts[1])
    return ids


def sections(text):
    """{"## heading": [lines]} of a Markdown file."""
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return out


def rows(lines):
    """The cells of the table rows in lines, after the header and the rule."""
    table = [line for line in lines if line.startswith("|")]
    return [[c.strip() for c in line.strip().strip("|").split("|")] for line in table]


def check_mapping(kind, path, columns, known):
    problems = []
    text = (ROOT / path).read_text(encoding="utf-8")
    parts = sections(text)
    if "使う項目" not in parts:
        return [f"{path}: no \"## 使う項目\" section"]
    table = rows(parts["使う項目"])
    if not table or table[0] != columns:
        return [f"{path}: the 使う項目 table must have the columns: " + " | ".join(columns)]

    local = {}
    local_file = ROOT / path
    for title, fields, line in entries(local_file):
        where = f"{path}:{line}: {title}"
        if "このリポジトリの項目" not in parts:
            continue
        problems += [f"{where}: {p}" for p in check_entry(kind, title, fields)]
        m = ID.match(fields.get("ID", ""))
        if m:
            if m.group(1) in known[kind]:
                problems.append(f"{where}: ID is already used by the catalog: {m.group(1)}")
            local[m.group(1)] = where

    used = []
    for cells in table[2:]:
        if len(cells) != len(columns):
            problems.append(f"{path}: a row of 使う項目 does not have {len(columns)} cells: {' | '.join(cells)}")
            continue
        m = ID.match(cells[0])
        if not m:
            problems.append(f"{path}: 項目 must be a backticked ID: {cells[0]}")
            continue
        entry_id = m.group(1)
        if entry_id in used:
            problems.append(f"{path}: {entry_id} is listed twice")
        used.append(entry_id)
        if entry_id not in known[kind] and entry_id not in local:
            problems.append(f"{path}: {entry_id} is neither in the catalog (.agents/knowledge-ids.txt) "
                            "nor in このリポジトリの項目 (a newer catalog entry needs adopting again)")
        for name, value in zip(columns[1:], cells[1:]):
            if not value:
                problems.append(f"{path}: {entry_id}: empty {name} (write — or 未定)")
    for entry_id, where in local.items():
        if entry_id not in used:
            problems.append(f"{where}: a local entry that 使う項目 does not list: {entry_id}")
    if len(used) > LIMIT:
        problems.append(f"{path}: {len(used)} entries in 使う項目, over the limit of {LIMIT}; remove some first")
    return problems


def main():
    known = catalog_ids()
    if known is None:
        print("knowledge-check: .agents/knowledge-ids.txt not found (adopt knowledge again)", file=sys.stderr)
        return 1
    problems, counted = [], []
    for kind, (path, columns) in MAPPINGS.items():
        if not (ROOT / path).exists():
            continue
        found = check_mapping(kind, path, columns, known)
        problems += found
        counted.append(path)
    if not counted:
        problems.append("no mapping table (docs/knowledge/practices.md or docs/knowledge/standards.md)")
    if problems:
        print("\n".join(f"knowledge-check: {p}" for p in problems), file=sys.stderr)
        print("knowledge-check: FAILED", file=sys.stderr)
        return 1
    print("knowledge-check: ok (" + ", ".join(counted) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
