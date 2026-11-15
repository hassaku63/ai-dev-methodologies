#!/usr/bin/env python3
"""Lists catalog entries that may have gone stale (ADR-0011):
  1. Entries past their review date (確認 date + 間隔).
  2. Source URLs that no longer open, or that now answer from another place.
  3. Entries whose recorded Git source file has changed since the recorded commit.

It depends on the date and the network, so it is NOT part of `make check`:
the monthly workflow runs it and opens an issue from the report.

Usage: python3 scripts/knowledge-staleness.py [--offline]
  --offline   only the date check (no network)
Environment:
  TODAY=YYYY-MM-DD   override today's date (for testing)
  GH_TOKEN           optional; raises the GitHub API rate limit
Prints a Markdown report to stdout. Exit status: 0 nothing found, 3 findings.
Python 3 standard library only.
"""
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/knowledge/lib"))
from catalog import load  # noqa: E402

CATALOG = ROOT / "plugins/knowledge/catalog"
URL = re.compile(r"https?://[^\s)|`、。「」<>]+")
AGENT = "Mozilla/5.0 (ai-dev-methodologies knowledge-staleness)"


def label(kind, title):
    return ("標準: " if kind == "standards" else "") + title


def overdue(found, today):
    out = []
    for kind, _pack, title, fields, _path, _line in found:
        m = re.match(r"(\d{4}-\d{2}-\d{2}) / 間隔 (\d+) 日", fields.get("確認", ""))
        if not m:
            continue
        checked = datetime.date.fromisoformat(m.group(1))
        if today > checked + datetime.timedelta(days=int(m.group(2))):
            out.append(f"- {label(kind, title)}（確認日 {m.group(1)}、間隔 {m.group(2)} 日）")
    return out


def fetch(url, accept=None):
    headers = {"User-Agent": AGENT}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.status, r.geturl(), r.read()


def urls(found):
    seen = set()
    for _kind, _pack, _title, fields, _path, _line in found:
        for name in ("出どころ", "一次情報"):
            for url in URL.findall(fields.get(name, "")):
                seen.add(url.rstrip(".,"))
    return sorted(seen)


def check_urls(found):
    broken, moved, refused = [], [], []
    for url in urls(found):
        try:
            _status, final, _body = fetch(url)
        except urllib.error.HTTPError as e:
            (refused if e.code in (401, 403, 429) else broken).append(f"- {url}（{e.code}）")
            continue
        except (urllib.error.URLError, OSError) as e:
            broken.append(f"- {url}（{getattr(e, 'reason', e)}）")
            continue
        def bare(u):
            # The fragment never reaches the server; a trailing slash, http->https,
            # "www." and an explicit :443 are not moves.
            u = re.sub(r"^https?://(www\.)?", "", u.split("#", 1)[0]).rstrip("/")
            return u.replace(":443/", "/", 1)
        # A DOI always redirects to the publisher: that is how it works, not a move.
        if url.startswith(("https://doi.org/", "https://dx.doi.org/")):
            continue
        if bare(url) != bare(final):
            moved.append(f"- {url} → {final}")
    return broken, moved, refused


def check_sources(found):
    changed, unknown = [], []
    for _kind, _pack, title, fields, _path, _line in found:
        source = fields.get("ソース", "なし")
        if source == "なし":
            continue
        for spec in (s.strip().strip("`") for s in source.split(",")):
            repo, _, rest = spec.partition(":")
            path, _, sha = rest.rpartition("@")
            api = "https://api.github.com/repos/" + repo
            try:
                _s, _u, body = fetch(f"{api}/commits?path={path}&per_page=1", "application/vnd.github+json")
                latest = json.loads(body)[0]["sha"]
                if latest.startswith(sha):
                    continue
                # The recorded commit was the head on the day of the check, so the
                # newest commit touching the file is normally its ancestor.
                _s, _u, body = fetch(f"{api}/compare/{latest}...{sha}", "application/vnd.github+json")
                status = json.loads(body).get("status")
            except (urllib.error.URLError, OSError, ValueError, IndexError, KeyError):
                unknown.append(f"- {title}: `{spec}`")
                continue
            if status not in ("ahead", "identical"):
                changed.append(f"- {title}: `{repo}:{path}` https://github.com/{repo}/compare/{sha}...{latest}")
    return changed, unknown


def main():
    offline = sys.argv[1:] == ["--offline"]
    today = datetime.date.fromisoformat(os.environ.get("TODAY") or datetime.date.today().isoformat())
    found = load(CATALOG)
    sections = [("見直しの期限を過ぎた項目", overdue(found, today))]
    refused = []
    if not offline:
        broken, moved, refused = check_urls(found)
        changed, unknown = check_sources(found)
        sections += [("開けない出どころ", broken), ("別の場所へ移った出どころ", moved),
                     ("記録したコミットのあとに変わったソース", changed),
                     ("確かめられなかったソース（ファイルが移ったか、API が答えなかった）", unknown)]
    if not any(items for _, items in sections):
        print(f"knowledge-staleness: nothing to review ({today})")
        return 0
    out = [f"# 知識の目録の鮮度の報告（{today}）", "", "確かめ直す手順は `docs/dev/knowledge-review.md`。"]
    for heading, items in sections:
        if items:
            out += ["", f"## {heading}", ""] + items
    if refused:
        out += ["", "## 自動の確認を拒んだサイト（参考。ページの有無は分からない）", ""] + refused
    print("\n".join(out))
    return 3


if __name__ == "__main__":
    sys.exit(main())
