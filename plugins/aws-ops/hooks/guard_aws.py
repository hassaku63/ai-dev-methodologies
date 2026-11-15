#!/usr/bin/env python3
"""PreToolUse hook: keeps the agent's AWS CLI calls read-only.

Reads the hook input (JSON) on stdin and looks at every `aws` invocation in a
Bash command.

  every invocation is a known read   exit 0, no output (normal permissions apply)
  one is not a read, or reads data   exit 2, reason on stderr (the call is blocked)
  one cannot be understood           exit 0, JSON asking for the owner's permission

This is a safety net, not the barrier. The barrier is the AWS credential the
agent runs with, which must be read-only (ADR-0005 of ai-dev-methodologies).

Python 3 standard library only.
"""
import json
import re
import shlex
import sys

# An operation is a read when it is one of these words or starts with one of
# them followed by "-" (describe-instances, get-findings, list-buckets).
READ_VERBS = (
    "describe", "get", "list", "batch-get", "lookup", "search", "head", "view",
    "check", "estimate", "validate", "simulate", "filter", "tail", "select",
    "wait", "help",
)

# Reads that return secrets, credentials or stored data rather than
# configuration. An operation of "*" covers the whole service.
DATA_READS = {
    ("secretsmanager", "get-secret-value"),
    ("secretsmanager", "batch-get-secret-value"),
    ("s3api", "get-object"),
    ("s3api", "select-object-content"),
    ("ecr", "get-login-password"),
    ("ecr", "get-authorization-token"),
    ("ec2", "get-password-data"),
    ("dynamodb", "get-item"),
    ("dynamodb", "batch-get-item"),
    ("sqs", "receive-message"),
    ("kinesis", "get-records"),
    ("codeartifact", "get-authorization-token"),
    ("sts", "*"),
}
DATA_READ_EXCEPTIONS = {("sts", "get-caller-identity")}
DECRYPTING = {
    ("ssm", "get-parameter"), ("ssm", "get-parameters"),
    ("ssm", "get-parameters-by-path"), ("ssm", "get-parameter-history"),
}

# Services whose commands do not follow the verb pattern: allowed operations.
SPECIAL = {
    "s3": {"ls"},
    "configure": {"list", "list-profiles", "get"},
}
# Signing in is for the owner to do.
ASK_SERVICES = {"sso", "login", "logout"}

GLOBAL_OPTIONS_WITH_VALUE = {
    "--profile", "--region", "--output", "--endpoint-url", "--query", "--color",
    "--ca-bundle", "--cli-read-timeout", "--cli-connect-timeout",
    "--cli-binary-format",
}
PUNCTUATION = set("();<>|&")


def is_read(operation):
    return any(operation == v or operation.startswith(v + "-") for v in READ_VERBS)


def judge(args):
    """Returns (decision, text) for the arguments after `aws`."""
    positional = []
    flags = set()
    skip = False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg.startswith("-"):
            flags.add(arg.split("=", 1)[0])
            if arg in GLOBAL_OPTIONS_WITH_VALUE:
                skip = True
            continue
        positional.append(arg)
        if len(positional) == 2:
            break
    # Flags after the operation matter too (--with-decryption).
    flags.update(a.split("=", 1)[0] for a in args if a.startswith("-"))
    text = "aws " + " ".join(positional)

    if "--version" in flags or not positional or positional[0] == "help":
        return "allow", text
    service = positional[0]
    if service in ASK_SERVICES:
        return "ask", text
    if len(positional) < 2:
        return "ask", text
    operation = positional[1]
    if operation == "help":
        return "allow", text
    if service in SPECIAL:
        return ("allow" if operation in SPECIAL[service] else "deny"), text
    if not is_read(operation):
        return "deny", text
    key = (service, operation)
    if key not in DATA_READ_EXCEPTIONS and (key in DATA_READS or (service, "*") in DATA_READS):
        return "deny", text + " (reads secrets, credentials or stored data)"
    if key in DECRYPTING and "--with-decryption" in flags:
        return "deny", text + " --with-decryption (reads a secret value)"
    return "allow", text


def invocations(command, judges=None, depth=0):
    """Yields (decision, text) for every invocation of a judged command.

    judges maps a command name to the function that judges its arguments;
    by default only `aws` is judged.
    """
    judges = judges or {"aws": judge}
    embedded = re.compile(r"(^|[\s;|&(])(" + "|".join(map(re.escape, judges)) + r")\s")
    # Command substitutions and new lines start a new command.
    # A backslash at the end of a line continues the same command.
    flat = command.replace("\\\n", " ")
    flat = flat.replace("$(", " ; ").replace("`", " ; ").replace("\n", " ; ")
    try:
        lexer = shlex.shlex(flat, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        if embedded.search(" " + command):
            yield "ask", "a command that could not be parsed"
        return

    i = 0
    while i < len(tokens):
        token = tokens[i]
        name = token.rsplit("/", 1)[-1]
        if name in judges:
            j = i + 1
            while j < len(tokens) and not set(tokens[j]) <= PUNCTUATION:
                j += 1
            yield judges[name](tokens[i + 1:j])
            i = j
            continue
        # A quoted script: bash -c "aws ...", xargs sh -c '...'.
        if embedded.search(token):
            if depth >= 3:
                yield "ask", "a deeply nested command"
            else:
                yield from invocations(token, judges, depth + 1)
        i += 1


def run(judges, blocked, undecided):
    """The hook: reads the event on stdin, prints the decision, returns the exit code."""
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if event.get("tool_name") != "Bash":
        return 0
    command = (event.get("tool_input") or {}).get("command") or ""
    found = list(invocations(command, judges))
    denied = [text for decision, text in found if decision == "deny"]
    asked = [text for decision, text in found if decision == "ask"]

    if denied:
        print(blocked.format("; ".join(denied)), file=sys.stderr)
        return 2
    if asked:
        json.dump({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": undecided.format("; ".join(asked)),
            }
        }, sys.stdout)
    return 0


def main():
    return run(
        {"aws": judge},
        "aws-ops guard: blocked, not a read-only call: {}.\n"
        "This repository is at the 'investigate and report' level: the agent only "
        "reads AWS. Do not look for another way to run it. Write the command into "
        "the report as a proposed action for the owner.",
        "aws-ops guard could not tell whether this is read-only: {}",
    )


if __name__ == "__main__":
    sys.exit(main())
