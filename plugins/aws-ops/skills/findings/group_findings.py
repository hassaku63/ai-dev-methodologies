#!/usr/bin/env python3
"""Groups Security Hub findings by application and writes a Markdown report.

Usage:
  group_findings.py --apps ops/apps.json [--date YYYY-MM-DD] [--all]
                    [--out report.md] findings.json [findings.json ...]

Input: the JSON that `aws securityhub get-findings` prints (an object with a
"Findings" list), or a bare list of findings in the same format (ASFF).

Applications are defined in the apps file:
  {"apps": [{"name": "...", "description": "...",
             "match": {"tags": {"App": "x"}, "name_prefixes": ["x-"],
                       "arn_patterns": ["arn:aws:ecs:*:*:service/*/x-*"],
                       "accounts": ["111122223333"]}}]}
A resource belongs to the first application, in file order, for which any one
of the matchers holds. `tags` holds when every listed tag has the listed value.
`name_prefixes` holds when a part of the resource identifier starts with one of
the prefixes (for an ARN: the parts after the account, split on "/" and ":").

By default only findings that still need attention are counted: record state
ACTIVE, workflow status NEW or NOTIFIED, compliance status not PASSED.
`--all` counts everything.

The same input always gives the same output: nothing is read from the clock or
the network. Python 3 standard library only.
"""
import argparse
import fnmatch
import json
import re
import sys
from collections import defaultdict

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]
UNMAPPED = "（どのアプリケーションにも当たらない）"
RESOURCES_SHOWN = 10


def load_findings(paths):
    findings = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("Findings", []) if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise SystemExit(f"group-findings: {path}: no list of findings")
        findings.extend(items)
    return findings


def load_apps(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    apps = data.get("apps")
    if not isinstance(apps, list):
        raise SystemExit(f"group-findings: {path}: \"apps\" must be a list")
    names = set()
    for app in apps:
        name = app.get("name")
        if not name or name in names:
            raise SystemExit(f"group-findings: {path}: every app needs a unique \"name\"")
        names.add(name)
        unknown = set(app.get("match", {})) - {"tags", "name_prefixes", "arn_patterns", "accounts"}
        if unknown:
            raise SystemExit(f"group-findings: {path}: {name}: unknown matcher {sorted(unknown)}")
    return apps


def needs_attention(finding):
    if finding.get("RecordState", "ACTIVE") != "ACTIVE":
        return False
    if (finding.get("Workflow") or {}).get("Status", "NEW") not in ("NEW", "NOTIFIED"):
        return False
    return (finding.get("Compliance") or {}).get("Status") != "PASSED"


def resource_names(resource_id):
    """The parts of an identifier that can carry a name.

    For an ARN these are the parts of the resource section, split on "/" and
    ":" (task-definition/order-api:42 gives task-definition, order-api, 42).
    """
    parts = resource_id.split(":", 5)
    resource = parts[5] if len(parts) == 6 and parts[0] == "arn" else resource_id
    return [p for p in re.split(r"[/:]", resource) if p]


def app_of(resource, account, apps):
    rid = resource.get("Id", "")
    tags = resource.get("Tags") or {}
    names = resource_names(rid)
    for app in apps:
        match = app.get("match", {})
        wanted = match.get("tags")
        if wanted and all(tags.get(k) == v for k, v in wanted.items()):
            return app["name"]
        if any(n.startswith(p) for n in names for p in match.get("name_prefixes", [])):
            return app["name"]
        if any(fnmatch.fnmatchcase(rid, p) for p in match.get("arn_patterns", [])):
            return app["name"]
        if account in match.get("accounts", []):
            return app["name"]
    return UNMAPPED


def severity_of(finding):
    label = (finding.get("Severity") or {}).get("Label", "INFORMATIONAL")
    return label if label in SEVERITIES else "INFORMATIONAL"


def issue_of(finding):
    """What groups findings into one action: the control, else the title."""
    control = (finding.get("Compliance") or {}).get("SecurityControlId")
    title = finding.get("Title", "(no title)")
    return (control or "", title)


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def build(findings, apps):
    # app -> issue -> {"severity", "url", "product", "resources": set}
    grouped = defaultdict(dict)
    for finding in findings:
        account = finding.get("AwsAccountId", "")
        region = finding.get("Region", "")
        url = (((finding.get("Remediation") or {}).get("Recommendation") or {}).get("Url")) or ""
        for resource in finding.get("Resources") or [{"Id": "(no resource)"}]:
            app = app_of(resource, account, apps)
            entry = grouped[app].setdefault(issue_of(finding), {
                "severity": severity_of(finding), "url": url,
                "product": finding.get("ProductName", ""), "resources": set(),
            })
            # One issue can carry several severities; keep the worst.
            if SEVERITIES.index(severity_of(finding)) < SEVERITIES.index(entry["severity"]):
                entry["severity"] = severity_of(finding)
            entry["url"] = entry["url"] or url
            entry["resources"].add((
                resource.get("Id", ""), resource.get("Type", ""), account, region,
                tuple(sorted((resource.get("Tags") or {}).items())),
            ))
    return grouped


def counts(issues):
    row = dict.fromkeys(SEVERITIES, 0)
    for entry in issues.values():
        row[entry["severity"]] += len(entry["resources"])
    return row


def render(grouped, apps, date, total, counted):
    order = [a["name"] for a in apps if a["name"] in grouped]
    if UNMAPPED in grouped:
        order.append(UNMAPPED)
    described = {a["name"]: a.get("description", "") for a in apps}

    out = ["# Security Hub の Finding のまとめ" + (f"（{date}）" if date else ""), ""]
    out.append(f"取得した Finding は {total} 件。うち、対応が要るものは {counted} 件"
               "（記録の状態が ACTIVE、ワークフローの状態が NEW か NOTIFIED、準拠の状態が PASSED でないもの）。")
    out.append("件数は、Finding とリソースの組で数える。")
    out += ["", "## 全体", "",
            "| アプリケーション | " + " | ".join(SEVERITIES) + " | 計 |",
            "| --- |" + " ---: |" * (len(SEVERITIES) + 1)]
    for name in order:
        row = counts(grouped[name])
        out.append(f"| {cell(name)} | " + " | ".join(str(row[s]) for s in SEVERITIES)
                   + f" | {sum(row.values())} |")
    if not order:
        out.append("| （なし） |" + " 0 |" * (len(SEVERITIES) + 1))

    for name in order:
        out += ["", f"## {name}", ""]
        if described.get(name):
            out += [described[name], ""]
        if name == UNMAPPED:
            out += ["アプリケーションの単位の定義（`ops/apps.json`）のどれにも当たらなかったリソース。"
                    "タグや名前を見て、定義に足すかどうかを所有者が決める。", ""]
        issues = sorted(
            grouped[name].items(),
            key=lambda kv: (SEVERITIES.index(kv[1]["severity"]), -len(kv[1]["resources"]), kv[0]),
        )
        out += ["| 重大度 | 項目 | リソース | 対処の手引き |", "| --- | --- | ---: | --- |"]
        for (control, title), entry in issues:
            label = f"[{control}] {title}" if control else title
            link = f"[手引き]({entry['url']})" if entry["url"] else "—"
            out.append(f"| {entry['severity']} | {cell(label)} | {len(entry['resources'])} | {link} |")
        for (control, title), entry in issues:
            label = f"[{control}] {title}" if control else title
            out += ["", f"### {label}", "", f"重大度 {entry['severity']}。"
                    + (f"検出元は {entry['product']}。" if entry["product"] else ""), ""]
            resources = sorted(entry["resources"])
            for rid, rtype, account, region, tags in resources[:RESOURCES_SHOWN]:
                where = "、".join(x for x in (rtype, account, region) if x)
                line = f"- `{rid}`" + (f"（{where}）" if where else "")
                if name == UNMAPPED and tags:
                    line += " タグ: " + ", ".join(f"{k}={v}" for k, v in tags)
                out.append(line)
            if len(resources) > RESOURCES_SHOWN:
                out.append(f"- ほか {len(resources) - RESOURCES_SHOWN} 件")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apps", required=True)
    parser.add_argument("--date", default="")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("findings", nargs="+")
    args = parser.parse_args()

    apps = load_apps(args.apps)
    findings = load_findings(args.findings)
    selected = findings if args.all else [f for f in findings if needs_attention(f)]
    report = render(build(selected, apps), apps, args.date, len(findings), len(selected))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
