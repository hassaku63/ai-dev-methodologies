"""Reads the knowledge catalog and checks the shape of its entries.

The catalog holds two kinds of entry, one Markdown file per pack:
  catalog/practices/<pack>.md   development practices
  catalog/standards/<pack>.md   industry standards

An entry is a "### <title>" heading followed by a two-column table of fields
("| 欄 | 内容 |"). The fields of each kind are in FIELDS below; their meaning is
in catalog/README.md. Tables under other headings ("## 外したもの") are not
entries.

Python 3 standard library only.
"""
import re
from pathlib import Path

FIELDS = {
    "practices": ["ID", "出どころ", "ソース", "何を言っているか", "確からしさ",
                  "当たるべき場面", "判断の問い", "対象", "確認"],
    "standards": ["ID", "発行元", "何を決めているか", "一次情報", "状態",
                  "当たるべき場面", "確認"],
}
URL_FIELD = {"practices": "出どころ", "standards": "一次情報"}

ID = re.compile(r"^`([a-z0-9]+(?:-[a-z0-9]+)*)`$")
SOURCE = re.compile(r"^`[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:[^`@\s]+@[0-9a-f]{7,40}`$")
CHECKED = re.compile(r"^\d{4}-\d{2}-\d{2} / 間隔 \d+ 日$")
# A target: "なし", or backticked "name@version" items separated by ", ".
TARGET_ITEM = re.compile(r"^`(?:@[a-z0-9._-]+/)?[a-z0-9._/-]+@\d+(?:\.\d+)?`$")


def entries(path):
    """Yields (title, {field: value}, line number) for each entry of a file."""
    title, fields, line_no = None, {}, 0
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            if title is not None:
                yield title, fields, line_no
            title, fields, line_no = (line[4:].strip(), {}, n) if line.startswith("### ") else (None, {}, 0)
            continue
        if title is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("欄", "") or set(cells[0]) <= set("-: "):
            continue
        fields[cells[0]] = "|".join(cells[1:]).strip()
    if title is not None:
        yield title, fields, line_no


def check_entry(kind, title, fields):
    """Returns the problems of one entry, as strings."""
    problems = []
    for name in FIELDS[kind]:
        if name not in fields:
            problems.append(f"missing field: {name}")
        elif not fields[name]:
            problems.append(f"empty field: {name}")
    for name in fields:
        if name not in FIELDS[kind]:
            problems.append(f"unknown field: {name}")
    value = fields.get("ID", "")
    if value and not ID.match(value):
        problems.append(f"ID must be backticked kebab-case: {value}")
    url_field = URL_FIELD[kind]
    if fields.get(url_field) and "https://" not in fields[url_field]:
        problems.append(f"{url_field} has no https URL")
    source = fields.get("ソース")
    if kind == "practices" and source and source != "なし":
        for part in (p.strip() for p in source.split(",")):
            if not SOURCE.match(part):
                problems.append(f"ソース must be `owner/repo:path@commit` or なし: {part}")
    target = fields.get("対象")
    if kind == "practices" and target and target != "なし":
        for part in (p.strip() for p in target.split(",")):
            if not TARGET_ITEM.match(part):
                problems.append(f"対象 must be なし or `name@major[.minor]`: {part}")
    checked = fields.get("確認")
    if checked and not CHECKED.match(checked):
        problems.append(f"確認 must be YYYY-MM-DD / 間隔 N 日: {checked}")
    return problems


def snapshot(root):
    """The lines of the ID list that adopted repositories check their mapping against.

    One line per entry: "<kind> <ID> <pack> <target>", where target is the
    対象 field without backticks and spaces ("なし" when none).
    """
    lines = ["# Generated from the ai-dev-methodologies knowledge catalog. Do not edit by hand.",
             "# <kind> <ID> <pack> <target>"]
    for kind, pack, _title, fields, _path, _line in sorted(load(root), key=lambda e: (e[0], e[3].get("ID", ""))):
        target = fields.get("対象", "なし").replace("`", "").replace(" ", "") or "なし"
        lines.append(f"{kind} {fields.get('ID', '').strip('`')} {pack} {target}")
    return "\n".join(lines) + "\n"


def load(root):
    """All entries under a catalog root: list of (kind, pack, title, fields, path, line)."""
    found = []
    for kind in FIELDS:
        for path in sorted((Path(root) / kind).glob("*.md")):
            for title, fields, line in entries(path):
                found.append((kind, path.stem, title, fields, path, line))
    return found


def check(root):
    """Returns the problems of a whole catalog, as strings."""
    problems, seen = [], {}
    found = load(root)
    if not found:
        problems.append(f"{root}: no entries")
    for kind, _pack, title, fields, path, line in found:
        where = f"{path}:{line}: {title}"
        problems += [f"{where}: {p}" for p in check_entry(kind, title, fields)]
        m = ID.match(fields.get("ID", ""))
        if m:
            if m.group(1) in seen:
                problems.append(f"{where}: ID also used at {seen[m.group(1)]}: {m.group(1)}")
            seen[m.group(1)] = where
    return problems
