#!/usr/bin/env python3
"""PreToolUse hook: lets the agent plan infrastructure changes, not apply them.

Looks at every terraform, tofu, terragrunt, cdk and aws invocation in a Bash
command.

  every invocation is known to change nothing   exit 0, no output
  one applies, destroys or touches the state    exit 2, reason on stderr
  one cannot be understood, or may show secrets exit 0, JSON asking the owner

The aws rules are those of the aws-ops guard (guard_aws.py, read-only).

This is a safety net, not the barrier: it does not see inside scripts and
Makefile targets (`make apply`, `npm run deploy`). The barrier is the
credential the agent runs with (ADR-0005, ADR-0010 of ai-dev-methodologies).

Python 3 standard library only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard_aws import judge as judge_aws, run  # noqa: E402

# terraform / tofu subcommands that change neither the infrastructure nor the
# remote state.
TERRAFORM_SAFE = {
    "version", "fmt", "validate", "init", "get", "plan", "show", "providers",
    "graph", "metadata", "modules",
}
TERRAFORM_ASK = {"output", "console", "login", "logout"}  # may print secrets, or sign in
TERRAFORM_INIT_UNSAFE = {"-migrate-state", "-force-copy"}
TERRAFORM_NESTED = {  # subcommand -> safe second words
    "state": {"list"},
    "workspace": {"list", "show", "select"},
}
TERRAFORM_NESTED_ASK = {"state": {"show"}}  # prints attribute values

CDK_SAFE = {
    "synth", "synthesize", "diff", "list", "ls", "doctor", "docs", "doc",
    "context", "metadata", "notices", "acknowledge", "ack", "version", "init",
}
TERRAGRUNT_OWN_SAFE = {
    "hclfmt", "render-json", "graph-dependencies", "output-module-groups",
    "validate-inputs", "terragrunt-info", "hclvalidate",
}


def words(args):
    """Positional words and the set of flags (without their values)."""
    positional, flags = [], set()
    for arg in args:
        if arg == "--":
            continue
        if arg.startswith("-"):
            flags.add(arg.split("=", 1)[0])
        else:
            positional.append(arg)
    return positional, flags


def judge_terraform(args, name="terraform"):
    positional, flags = words(args)
    text = f"{name} " + " ".join(positional[:2])
    if not positional or flags & {"-version", "--version", "-help", "--help", "-h"}:
        return "allow", text
    sub = positional[0]
    second = positional[1] if len(positional) > 1 else None
    if sub == "workspace" and second == "select" and any(f.startswith("-or-create") for f in flags):
        return "deny", text + " -or-create (creates a workspace in the backend)"
    if sub in TERRAFORM_NESTED:
        if second in TERRAFORM_NESTED[sub]:
            return "allow", text
        if second in TERRAFORM_NESTED_ASK.get(sub, ()):
            return "ask", text
        return "deny", text
    text = f"{name} {sub}"
    if sub == "init" and flags & TERRAFORM_INIT_UNSAFE:
        return "deny", text + " " + " ".join(sorted(flags & TERRAFORM_INIT_UNSAFE))
    if sub in TERRAFORM_SAFE:
        return "allow", text
    if sub in TERRAFORM_ASK:
        return "ask", text
    return "deny", text


def judge_tofu(args):
    return judge_terraform(args, "tofu")


def judge_terragrunt(args):
    positional, _ = words(args)
    if positional and positional[0] in ("run-all", "run"):
        args = [a for a in args if a not in ("run-all", "run")]
        positional = positional[1:]
    if positional and positional[0] in TERRAGRUNT_OWN_SAFE:
        return "allow", "terragrunt " + positional[0]
    return judge_terraform(args, "terragrunt")


def judge_cdk(args):
    positional, flags = words(args)
    text = "cdk " + " ".join(positional[:1])
    if not positional or flags & {"--version", "--help", "-h"}:
        return "allow", text
    return ("allow" if positional[0] in CDK_SAFE else "deny"), text


JUDGES = {
    "aws": judge_aws,
    "terraform": judge_terraform,
    "tofu": judge_tofu,
    "terragrunt": judge_terragrunt,
    "cdk": judge_cdk,
}


def main():
    return run(
        JUDGES,
        "aws-iac guard: blocked: {}.\n"
        "This repository lets the agent plan infrastructure changes (plan, diff, "
        "synth), not apply them or touch the state, and read AWS, not change it. "
        "Do not look for another way to run it. Report the plan and leave the "
        "command to the owner.",
        "aws-iac guard could not tell whether this changes anything or prints secrets: {}",
    )


if __name__ == "__main__":
    sys.exit(main())
