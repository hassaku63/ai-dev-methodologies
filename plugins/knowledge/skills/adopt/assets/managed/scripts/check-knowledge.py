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

For entries whose 対象 names a technology and version (`react@19`,
`go@1.27`, `hashicorp/aws@5`), the version this repository uses is read from
its dependency files (package-lock.json or package.json, go.mod,
.tool-versions, .terraform-version, .terraform.lock.hcl, requirements*.txt,
.python-version) and a different version fails: the entry was written for
another version, so re-open its source before relying on it. A technology the
repository does not use is not checked.

It looks only at files, never at the date or the network.
Python 3 standard library only.

Managed by ai-dev-methodologies (knowledge). Local edits are kept on update, but
the file then stops receiving updates; see .agents/methodology.lock.
"""
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent / "knowledge"))
from catalog import ID, check_entry, entries  # noqa: E402

TOOL_NAMES = {"nodejs": "node", "golang": "go", "python": "python", "terraform": "terraform",
              "opentofu": "tofu"}

MAPPINGS = {
    "practices": ("docs/knowledge/practices.md", ["項目", "このリポジトリでの場面", "このプロジェクトの立場"]),
    "standards": ("docs/knowledge/standards.md", ["項目", "このリポジトリとの接点"]),
}
LIMIT = 40


def catalog_ids():
    """({kind: set of IDs}, {ID: [target specs]}), or None without the list."""
    path = ROOT / ".agents/knowledge-ids.txt"
    ids = {kind: set() for kind in MAPPINGS}
    targets = {}
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2 and not line.startswith("#") and parts[0] in ids:
            ids[parts[0]].add(parts[1])
            if len(parts) >= 4 and parts[3] != "なし":
                targets[parts[1]] = parts[3].split(",")
    return ids, targets


def tracked(pattern):
    """Files matching a base-name pattern that git knows of (tracked, or untracked and not ignored)."""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others",
                              "--exclude-standard"], capture_output=True, check=True).stdout
        names = [n for n in out.decode("utf-8").split("\0") if n]
    except (OSError, subprocess.CalledProcessError):
        names = [str(p.relative_to(ROOT)) for p in ROOT.rglob(pattern)]
    for name in sorted(set(names)):
        path = ROOT / name
        if fnmatch.fnmatch(path.name, pattern) and path.is_file():
            yield path


def version_numbers(text):
    m = re.search(r"(\d+)(?:\.(\d+))?", text)
    return (m.group(1), m.group(2)) if m else None


def used_versions():
    """{name: [(major, minor or None, file)]} read from the dependency files."""
    found = {}

    def add(name, version, path):
        numbers = version_numbers(version)
        if numbers:
            found.setdefault(name, []).append((numbers[0], numbers[1], str(path.relative_to(ROOT))))

    for path in tracked("package-lock.json"):
        packages = json.loads(path.read_text(encoding="utf-8")).get("packages", {})
        for key, info in packages.items():
            if key.startswith("node_modules/") and key.count("node_modules/") == 1 and "version" in info:
                add(key[len("node_modules/"):], info["version"], path)
    for path in tracked("package.json"):
        if (path.parent / "package-lock.json").exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for group in ("dependencies", "devDependencies"):
            for name, spec in (data.get(group) or {}).items():
                add(name, spec, path)
    for path in tracked("go.mod"):
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^go\s+(\S+)", line)
            if m:
                add("go", m.group(1), path)
            m = re.match(r"^\s*(?:require\s+)?([a-z0-9.-]+\.[a-z]+/\S+)\s+v(\S+)", line)
            if m:
                add(m.group(1), m.group(2), path)
    for path in tracked(".tool-versions"):
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0] in TOOL_NAMES:
                add(TOOL_NAMES[parts[0]], parts[1], path)
    for name, tool in ((".terraform-version", "terraform"), (".python-version", "python"), (".nvmrc", "node")):
        for path in tracked(name):
            add(tool, path.read_text(encoding="utf-8").strip(), path)
    for path in tracked(".terraform.lock.hcl"):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r'provider\s+"(?:[^"/]+/)?([^"]+)"\s*\{[^}]*?version\s*=\s*"([^"]+)"', text, re.S):
            add(m.group(1), m.group(2), path)
    for pattern in ("requirements*.txt",):
        for path in tracked(pattern):
            for line in path.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^([A-Za-z0-9_.-]+)\s*==\s*(\S+)", line)
                if m:
                    add(m.group(1).lower(), m.group(2), path)
    return found


def check_versions(path, used_ids, targets, versions):
    """Problems for used entries whose 対象 differs from the version in use."""
    problems = []
    for entry_id in used_ids:
        for spec in targets.get(entry_id, []):
            name, _, wanted = spec.rpartition("@")
            want = wanted.split(".")
            for major, minor, where in versions.get(name, []):
                if major != want[0] or (len(want) > 1 and minor is not None and minor != want[1]):
                    have = major + (f".{minor}" if len(want) > 1 and minor is not None else "")
                    problems.append(f"{path}: {entry_id} is written for {spec}, but {where} uses {name}@{have}; "
                                    "re-open its source and update the entry (or 外したもの)")
    return problems


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


def check_mapping(kind, path, columns, known, targets, versions):
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
            target = fields.get("対象", "なし")
            if target and target != "なし":
                targets[m.group(1)] = target.replace("`", "").replace(" ", "").split(",")

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
    problems += check_versions(path, used, targets, versions)
    if len(used) > LIMIT:
        problems.append(f"{path}: {len(used)} entries in 使う項目, over the limit of {LIMIT}; remove some first")
    return problems


def main():
    loaded = catalog_ids()
    if loaded is None:
        print("knowledge-check: .agents/knowledge-ids.txt not found (adopt knowledge again)", file=sys.stderr)
        return 1
    known, targets = loaded
    versions = used_versions()
    problems, counted = [], []
    for kind, (path, columns) in MAPPINGS.items():
        if not (ROOT / path).exists():
            continue
        found = check_mapping(kind, path, columns, known, dict(targets), versions)
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
