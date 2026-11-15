#!/usr/bin/env python3
"""Writes a Markdown inventory from the raw JSON that collect.sh fetched.

Usage:
  summarize_inventory.py --raw <directory> [--apps ops/apps.json]
                         [--account <id>] [--date YYYY-MM-DD]
                         [--out ops/inventory.md]

<directory> holds one directory per region with the files of collect.sh.
With --apps, resources carry the application they belong to (the format and
the matching rules are in lib/apps.py of this plugin).

The same input always gives the same output: nothing is read from the clock or
the network. Python 3 standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
from apps import app_of, load_apps  # noqa: E402

ANYWHERE = {"0.0.0.0/0", "::/0"}

# Types the tables of this record describe in detail, as "<service>:<type>"
# taken from the ARN. Every other type found by discovery is listed by ARN.
DETAILED = {
    "ec2:vpc", "ec2:subnet", "ec2:route-table", "ec2:internet-gateway", "ec2:natgateway",
    "ec2:vpc-endpoint", "ec2:vpc-peering-connection", "ec2:security-group", "ec2:instance",
    "elasticloadbalancing:loadbalancer", "lambda:function", "rds:db", "ecs:cluster", "ecs:service",
}
SOURCES = [
    ("discovered-config", "AWS Config"),
    ("discovered-tagged", "タグ付けの API"),
    ("discovered-explorer", "Resource Explorer"),
]
LISTED_PER_TYPE = 10


def load(region_dir, name, key):
    """The list under `key` of <name>.json; empty when the file is missing."""
    path = region_dir / f"{name}.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get(key, [])


def load_many(region_dir, prefix, key):
    items = []
    for path in sorted(region_dir.glob(f"{prefix}-*.json")):
        with open(path, encoding="utf-8") as f:
            items.extend(json.load(f).get(key, []))
    return items


def tags_of(item):
    return {t["Key"]: t["Value"] for t in item.get("Tags") or []}


def cell(text):
    text = "" if text is None else str(text)
    return text.replace("|", "\\|").replace("\n", " ") or "—"


def code(value):
    return f"`{value}`" if value else "—"


def yes(value):
    return "はい" if value else "いいえ"


def table(header, rows):
    if not rows:
        return ["（なし）"]
    out = ["| " + " | ".join(header) + " |", "|" + " --- |" * len(header)]
    out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return out


def public_subnets(subnets, route_tables):
    """Subnet ids whose route table sends 0.0.0.0/0 to an internet gateway."""
    def to_internet(rt):
        return any(r.get("DestinationCidrBlock") == "0.0.0.0/0"
                   and str(r.get("GatewayId", "")).startswith("igw-")
                   for r in rt.get("Routes", []))
    explicit, main = {}, {}
    for rt in route_tables:
        for assoc in rt.get("Associations", []):
            if assoc.get("SubnetId"):
                explicit[assoc["SubnetId"]] = to_internet(rt)
            elif assoc.get("Main"):
                main[rt.get("VpcId")] = to_internet(rt)
    return {s["SubnetId"] for s in subnets
            if explicit.get(s["SubnetId"], main.get(s.get("VpcId"), False))}


def ports(rule):
    proto = rule.get("IpProtocol")
    if proto == "-1":
        return "すべて"
    low, high = rule.get("FromPort"), rule.get("ToPort")
    span = str(low) if low == high else f"{low}-{high}"
    return f"{proto} {span}"


def network(region_dir):
    vpcs = load(region_dir, "vpcs", "Vpcs")
    subnets = load(region_dir, "subnets", "Subnets")
    public = public_subnets(subnets, load(region_dir, "route-tables", "RouteTables"))
    out = ["### ネットワーク", ""]
    out += table(["VPC", "名前", "CIDR", "既定"], [
        [code(v["VpcId"]), tags_of(v).get("Name"), v.get("CidrBlock"), yes(v.get("IsDefault"))]
        for v in sorted(vpcs, key=lambda v: v["VpcId"])])
    out += ["", "サブネット。「外向き」は、ルートテーブルが `0.0.0.0/0` をインターネットゲートウェイに向けているもの。", ""]
    out += table(["サブネット", "名前", "VPC", "AZ", "CIDR", "外向き"], [
        [code(s["SubnetId"]), tags_of(s).get("Name"), code(s.get("VpcId")),
         s.get("AvailabilityZone"), s.get("CidrBlock"), yes(s["SubnetId"] in public)]
        for s in sorted(subnets, key=lambda s: (s.get("VpcId", ""), s.get("AvailabilityZone", ""), s["SubnetId"]))])

    rows = [["インターネットゲートウェイ", code(g["InternetGatewayId"]),
             "、".join(code(a.get("VpcId")) for a in g.get("Attachments", [])), ""]
            for g in sorted(load(region_dir, "internet-gateways", "InternetGateways"),
                            key=lambda g: g["InternetGatewayId"])]
    rows += [["NAT ゲートウェイ", code(n["NatGatewayId"]), code(n.get("VpcId")),
              f"サブネット {code(n.get('SubnetId'))}"]
             for n in sorted(load(region_dir, "nat-gateways", "NatGateways"), key=lambda n: n["NatGatewayId"])
             if n.get("State") != "deleted"]
    rows += [["VPC エンドポイント", code(e["VpcEndpointId"]), code(e.get("VpcId")),
              f"{e.get('ServiceName')}（{e.get('VpcEndpointType')}）"]
             for e in sorted(load(region_dir, "vpc-endpoints", "VpcEndpoints"), key=lambda e: e["VpcEndpointId"])]
    for p in sorted(load(region_dir, "vpc-peering-connections", "VpcPeeringConnections"),
                    key=lambda p: p["VpcPeeringConnectionId"]):
        other = p.get("AccepterVpcInfo") or {}
        rows.append(["VPC ピアリング", code(p["VpcPeeringConnectionId"]),
                     code((p.get("RequesterVpcInfo") or {}).get("VpcId")),
                     f"相手 {code(other.get('VpcId'))}（アカウント {other.get('OwnerId')}）"])
    out += ["", "出入り口。", ""]
    out += table(["種類", "ID", "VPC", "補足"], rows)
    return out


def arn_type(arn):
    """"<service>:<type>" of an ARN; the service alone when the ARN names no type."""
    parts = arn.split(":", 5)
    if len(parts) < 6 or parts[0] != "arn":
        return None
    match = re.match(r"([A-Za-z0-9_-]+)[/:]", parts[5])
    return f"{parts[2]}:{match.group(1)}" if match else parts[2]


def discovered(region_dir):
    """ARN -> {"sources": set of labels, "tags": dict}, and the labels that answered."""
    found, answered = {}, []

    def add(arn, label, tags):
        if not arn or arn_type(arn) is None:
            return
        entry = found.setdefault(arn, {"sources": set(), "tags": {}})
        entry["sources"].add(label)
        entry["tags"].update(tags)

    for name, label in SOURCES:
        path = region_dir / f"{name}.json"
        if not path.exists():
            continue
        answered.append(label)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for raw in data.get("Results", []):  # Config: each result is a JSON string
            item = json.loads(raw) if isinstance(raw, str) else raw
            tags = {t.get("key"): t.get("value") for t in item.get("tags") or [] if t.get("key")}
            add(item.get("arn"), label, tags)
        for item in data.get("ResourceTagMappingList", []):  # tagging API
            add(item.get("ResourceARN"), label, {t["Key"]: t["Value"] for t in item.get("Tags") or []})
        for item in data.get("Resources", []):  # Resource Explorer
            add(item.get("Arn"), label, {})
    return found, answered


def discovery(region_dir, app):
    found, answered = discovered(region_dir)
    out = ["", "### すべての種類", ""]
    if not answered:
        out += ["**種類を問わない発見は、どの出どころからも取れなかった。** この記録は、上の表が扱う種類だけを含む。"
                "ほかの種類のリソースがあっても、ここには現れない。", ""]
        return out
    silent = [label for _, label in SOURCES if label not in answered]
    out += ["種類を問わずに見つけたリソースの数。出どころ: " + "、".join(answered) + "。"
            + (f"取れなかった出どころ: {'、'.join(silent)}。" if silent else ""),
            "出どころには漏れがある（AWS Config は記録の対象の種類だけ、タグ付けの API はタグを持つか持ったことのあるものだけ、"
            "Resource Explorer は索引のあるリージョンで 1000 件まで）。ここに無いことは、無いことの証明にならない。", ""]
    by_type = {}
    for arn, entry in found.items():
        by_type.setdefault(arn_type(arn), []).append((arn, entry))
    out += table(["種類", "数", "詳しい表", "出どころ"], [
        [code(t), len(items), "あり" if t in DETAILED else "なし",
         "、".join(label for _, label in SOURCES if any(label in e["sources"] for _, e in items))]
        for t, items in sorted(by_type.items())])
    others = {t: items for t, items in by_type.items() if t not in DETAILED}
    if others:
        out += ["", "詳しい表が無い種類のリソース。必要なものは、個別に読み取って調べる。", ""]
        for t, items in sorted(others.items()):
            out += [f"{code(t)}（{len(items)} 件）", ""]
            for arn, entry in sorted(items)[:LISTED_PER_TYPE]:
                belongs = app(arn, entry["tags"])
                line = f"- {code(arn)}"
                if belongs != "—":
                    line += f" アプリケーション: {belongs}"
                elif entry["tags"]:
                    line += " タグ: " + ", ".join(f"{k}={v}" for k, v in sorted(entry["tags"].items()))
                out.append(line)
            if len(items) > LISTED_PER_TYPE:
                out.append(f"- ほか {len(items) - LISTED_PER_TYPE} 件")
            out.append("")
        out.pop()
    return out


def region_section(region_dir, apps, account):
    out = [f"## {region_dir.name}", ""]
    missing = sorted(p.name[:-len(".error")] for p in region_dir.glob("*.error"))
    if missing:
        out += ["取得できなかったもの（権限かサービスの状態による。該当する表は欠けている）: "
                + "、".join(code(m) for m in missing), ""]

    def app(rid, tags=None):
        return app_of(rid, tags or {}, account, apps) or "—"

    out += network(region_dir)

    instances = sorted(
        (i for r in load(region_dir, "instances", "Reservations") for i in r.get("Instances", [])
         if (i.get("State") or {}).get("Name") != "terminated"),
        key=lambda i: i["InstanceId"])
    lbs = sorted(load(region_dir, "load-balancers", "LoadBalancers"), key=lambda b: b.get("LoadBalancerName", ""))
    dbs = sorted(load(region_dir, "db-instances", "DBInstances"), key=lambda d: d.get("DBInstanceIdentifier", ""))

    open_rules = []
    for g in sorted(load(region_dir, "security-groups", "SecurityGroups"), key=lambda g: g["GroupId"]):
        for rule in g.get("IpPermissions", []):
            sources = ([r.get("CidrIp") for r in rule.get("IpRanges", [])]
                       + [r.get("CidrIpv6") for r in rule.get("Ipv6Ranges", [])])
            for source in sorted(s for s in sources if s in ANYWHERE):
                open_rules.append([code(g["GroupId"]), g.get("GroupName"), code(g.get("VpcId")),
                                   ports(rule), source])
    out += ["", "### 外から届くもの", "",
            "見直しの入り口になるもの。ここに載ることは、誤りを意味しない。意図したものかを所有者が確かめる。", "",
            "インバウンドを `0.0.0.0/0` か `::/0` に開けているセキュリティグループの規則。", ""]
    out += table(["セキュリティグループ", "名前", "VPC", "ポート", "送信元"], open_rules)
    exposed = [["インスタンス", code(i["InstanceId"]), app(i["InstanceId"], tags_of(i)),
                f"{i.get('PublicIpAddress')}、サブネット {code(i.get('SubnetId'))}"]
               for i in instances if i.get("PublicIpAddress")]
    exposed += [["ロードバランサー", b.get("LoadBalancerName"), app(b.get("LoadBalancerArn", "")),
                 f"{b.get('Type')}、{b.get('DNSName')}"] for b in lbs if b.get("Scheme") == "internet-facing"]
    exposed += [["データベース", d.get("DBInstanceIdentifier"), app(d.get("DBInstanceArn", "")), d.get("Engine")]
                for d in dbs if d.get("PubliclyAccessible")]
    out += ["", "パブリック IP を持つインスタンス、インターネット向けのロードバランサー、公開の設定のデータベース。", ""]
    out += table(["種類", "ID", "アプリケーション", "補足"], exposed)

    out += ["", "### コンピュートとデータベース", "", "インスタンス。", ""]
    out += table(["インスタンス", "名前", "アプリケーション", "種類", "状態", "サブネット", "パブリック IP"], [
        [code(i["InstanceId"]), tags_of(i).get("Name"), app(i["InstanceId"], tags_of(i)),
         i.get("InstanceType"), (i.get("State") or {}).get("Name"), code(i.get("SubnetId")),
         i.get("PublicIpAddress")] for i in instances])
    services = sorted(load_many(region_dir, "ecs-services", "services"),
                      key=lambda s: (s.get("clusterArn", ""), s.get("serviceName", "")))
    out += ["", "ECS のサービス。", ""]
    out += table(["クラスター", "サービス", "アプリケーション", "起動の種類", "希望数", "実行数"], [
        [s.get("clusterArn", "").rsplit("/", 1)[-1], s.get("serviceName"), app(s.get("serviceArn", "")),
         s.get("launchType") or "キャパシティプロバイダー", s.get("desiredCount"), s.get("runningCount")]
        for s in services])
    functions = sorted(load(region_dir, "lambda-functions", "Functions"), key=lambda f: f.get("FunctionName", ""))
    out += ["", "Lambda の関数。", ""]
    out += table(["関数", "アプリケーション", "ランタイム", "メモリ", "VPC"], [
        [f.get("FunctionName"), app(f.get("FunctionArn", "")), f.get("Runtime") or f.get("PackageType"),
         f.get("MemorySize"), code((f.get("VpcConfig") or {}).get("VpcId"))] for f in functions])
    out += ["", "ロードバランサー。", ""]
    out += table(["名前", "アプリケーション", "種類", "向き", "VPC"], [
        [b.get("LoadBalancerName"), app(b.get("LoadBalancerArn", "")), b.get("Type"),
         "インターネット向け" if b.get("Scheme") == "internet-facing" else "内部", code(b.get("VpcId"))]
        for b in lbs])
    out += ["", "データベース（RDS）。", ""]
    out += table(["識別子", "アプリケーション", "エンジン", "クラス", "マルチ AZ", "公開の設定"], [
        [d.get("DBInstanceIdentifier"), app(d.get("DBInstanceArn", "")),
         f"{d.get('Engine')} {d.get('EngineVersion')}", d.get("DBInstanceClass"),
         yes(d.get("MultiAZ")), yes(d.get("PubliclyAccessible"))] for d in dbs])
    out += discovery(region_dir, app)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--raw", required=True)
    parser.add_argument("--apps")
    parser.add_argument("--account", default="", help="the account id, for apps matched by account")
    parser.add_argument("--date", default="")
    parser.add_argument("--out")
    args = parser.parse_args()

    raw = Path(args.raw)
    regions = sorted(p for p in raw.iterdir() if p.is_dir()) if raw.is_dir() else []
    if not regions:
        raise SystemExit(f"summarize-inventory: {raw}: no region directories")
    apps = load_apps(args.apps) if args.apps else []

    out = ["# 構成の棚卸し" + (f"（{args.date}）" if args.date else ""), "",
           "AWS から読み取った構成を、そのまま表にしたもの。対象のリージョン: "
           + "、".join(p.name for p in regions) + "。", ""]
    for region_dir in regions:
        out += region_section(region_dir, apps, args.account)
        out.append("")
    report = "\n".join(out).rstrip("\n") + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
