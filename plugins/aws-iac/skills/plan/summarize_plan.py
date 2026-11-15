#!/usr/bin/env python3
"""Summarises a Terraform plan as Markdown, with replacements and deletions first.

Usage:
  summarize_plan.py [--out summary.md] plan.json

plan.json is what `terraform show -json <planfile>` prints.

Only addresses, resource types, actions and attribute names are printed, never
attribute values: a plan can hold secrets. The same input always gives the same
output. Python 3 standard library only.
"""
import argparse
import json
import sys

# Types that hold data or identity: replacing or deleting one loses something
# that the next apply does not bring back.
STATEFUL = {
    "aws_db_instance", "aws_rds_cluster", "aws_rds_cluster_instance", "aws_dynamodb_table",
    "aws_s3_bucket", "aws_ebs_volume", "aws_efs_file_system", "aws_instance",
    "aws_elasticache_cluster", "aws_elasticache_replication_group", "aws_opensearch_domain",
    "aws_elasticsearch_domain", "aws_redshift_cluster", "aws_docdb_cluster", "aws_neptune_cluster",
    "aws_msk_cluster", "aws_kinesis_stream", "aws_sqs_queue", "aws_kms_key",
    "aws_secretsmanager_secret", "aws_ssm_parameter", "aws_cloudwatch_log_group",
    "aws_ecr_repository", "aws_backup_vault", "aws_cognito_user_pool", "aws_route53_zone",
}
LABELS = {"create": "作成", "update": "変更", "replace": "置き換え", "delete": "削除",
          "forget": "state から外す", "no-op": "変更なし", "read": "読み取り"}
ORDER = ["replace", "delete", "forget", "update", "create"]
REASONS = {
    "replace_because_cannot_update": "この属性は、作り直さないと変えられない",
    "replace_because_tainted": "taint されている",
    "replace_by_request": "置き換えが指定された（-replace）",
    "replace_by_triggers": "replace_triggered_by による",
    "delete_because_no_resource_config": "コードから定義が消えた",
    "delete_because_no_module": "モジュールが消えた",
    "delete_because_wrong_repetition": "count / for_each の形が変わった",
    "delete_because_count_index": "count の範囲から外れた",
    "delete_because_each_key": "for_each のキーから外れた",
    "delete_because_no_move_target": "moved の移動先が無い",
}


def action_of(change):
    actions = change.get("actions") or []
    if "delete" in actions and "create" in actions:
        return "replace"
    return actions[0] if actions else "no-op"


def changed_attributes(change):
    """Names of the top-level attributes that differ, or become known only after apply."""
    before = change.get("before") or {}
    after = change.get("after") or {}
    unknown = change.get("after_unknown") or {}
    names = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
    names |= {k for k, v in unknown.items() if v and k in before}
    return sorted(names)


def path_text(path):
    return ".".join(str(p) for p in path)


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ") or "—"


def render(plan):
    changes = []
    for rc in plan.get("resource_changes") or []:
        if rc.get("mode") != "managed":
            continue
        change = rc.get("change") or {}
        changes.append({
            "address": rc.get("address", ""), "type": rc.get("type", ""),
            "action": action_of(change), "change": change,
            "reason": rc.get("action_reason", ""),
            "importing": bool(change.get("importing")),
        })
    acted = [c for c in changes if c["action"] in ORDER]
    acted.sort(key=lambda c: (ORDER.index(c["action"]), c["address"]))
    count = {a: sum(1 for c in acted if c["action"] == a) for a in ORDER}
    unchanged = sum(1 for c in changes if c["action"] == "no-op")

    out = ["# plan の要約", ""]
    if not acted:
        out += [f"変更はない（変更なしのリソース {unchanged}）。", ""]
    else:
        parts = [f"{LABELS[a]} {count[a]}" for a in ("create", "update", "replace", "delete", "forget") if count[a]]
        out += ["、".join(parts) + f"（変更なし {unchanged}）。", ""]
    out += ["属性の値は載せない（plan には秘密情報が入りうる）。値は、手元の plan で確かめる。", ""]

    risky = [c for c in acted if c["action"] in ("replace", "delete", "forget")]
    out += ["## 注意して見るもの", ""]
    if not risky:
        out += ["置き換えも削除もない。", ""]
    else:
        out += ["置き換えと削除。「データを持つ」は、作り直すと中身や識別子が失われる種類。", "",
                "| 操作 | リソース | データを持つ | 理由 |", "| --- | --- | --- | --- |"]
        for c in risky:
            reason = REASONS.get(c["reason"], c["reason"])
            paths = [path_text(p) for p in c["change"].get("replace_paths") or []]
            if paths:
                reason = (reason + "。" if reason else "") + "原因の属性: " + "、".join(f"`{p}`" for p in paths)
            out.append(f"| {LABELS[c['action']]} | `{cell(c['address'])}` | "
                       f"{'**はい**' if c['type'] in STATEFUL else 'いいえ'} | {cell(reason)} |")
        out.append("")

    out += ["## すべての変更", ""]
    if acted:
        out += ["| 操作 | リソース | 変わる属性 |", "| --- | --- | --- |"]
        for c in acted:
            attrs = "—"
            if c["action"] in ("update", "replace"):
                names = changed_attributes(c["change"])
                attrs = "、".join(f"`{n}`" for n in names) if names else "（属性の差は読み取れなかった）"
            label = LABELS[c["action"]] + ("（import を伴う）" if c["importing"] else "")
            out.append(f"| {label} | `{cell(c['address'])}` | {attrs} |")
    else:
        out.append("（なし）")
    out.append("")

    drift = sorted({d.get("address", "") for d in plan.get("resource_drift") or []})
    if drift:
        out += ["## コードの外で変わっていたもの", "",
                "前回の反映のあとに、Terraform の外で変わっていたリソース。この plan は、それを踏まえている。", ""]
        out += [f"- `{a}`" for a in drift] + [""]

    outputs = sorted(name for name, ch in (plan.get("output_changes") or {}).items()
                     if action_of(ch) != "no-op")
    if outputs:
        out += ["## 出力の変更", ""] + [f"- `{n}`" for n in outputs] + [""]
    return "\n".join(out).rstrip("\n") + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out")
    parser.add_argument("plan")
    args = parser.parse_args()
    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    if "resource_changes" not in plan and "format_version" not in plan:
        raise SystemExit(f"summarize-plan: {args.plan}: not the output of `terraform show -json <planfile>`")
    report = render(plan)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
