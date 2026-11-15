"""Application definitions (ops/apps.json) and how a resource is matched to one.

  {"apps": [{"name": "...", "description": "...",
             "match": {"tags": {"App": "x"}, "name_prefixes": ["x-"],
                       "arn_patterns": ["arn:aws:ecs:*:*:service/*/x-*"],
                       "accounts": ["111122223333"]}}]}

A resource belongs to the first application, in file order, for which any one
of the matchers holds:
  tags           every listed tag has the listed value
  name_prefixes  a part of the resource identifier starts with one of them
                 (for an ARN: the parts after the account, split on "/" and ":")
  arn_patterns   the identifier matches one of the shell-style patterns
  accounts       the resource is in one of the accounts

Python 3 standard library only.
"""
import fnmatch
import json
import re

MATCHERS = {"tags", "name_prefixes", "arn_patterns", "accounts"}


def load_apps(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    apps = data.get("apps")
    if not isinstance(apps, list):
        raise SystemExit(f"apps: {path}: \"apps\" must be a list")
    names = set()
    for app in apps:
        name = app.get("name")
        if not name or name in names:
            raise SystemExit(f"apps: {path}: every app needs a unique \"name\"")
        names.add(name)
        unknown = set(app.get("match", {})) - MATCHERS
        if unknown:
            raise SystemExit(f"apps: {path}: {name}: unknown matcher {sorted(unknown)}")
    return apps


def resource_names(resource_id):
    """The parts of an identifier that can carry a name.

    For an ARN these are the parts of the resource section, split on "/" and
    ":" (task-definition/order-api:42 gives task-definition, order-api, 42).
    """
    parts = resource_id.split(":", 5)
    resource = parts[5] if len(parts) == 6 and parts[0] == "arn" else resource_id
    return [p for p in re.split(r"[/:]", resource) if p]


def app_of(rid, tags, account, apps):
    """The name of the application a resource belongs to, or None."""
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
    return None
