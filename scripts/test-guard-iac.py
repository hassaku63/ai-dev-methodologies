#!/usr/bin/env python3
"""Checks the aws-iac guard hook against a table of commands. Part of `make check`."""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "plugins/aws-iac/hooks/guard_iac.py"

CASES = [
    # planning
    ("allow", "terraform init"),
    ("allow", "terraform init -backend-config=env/dev.hcl"),
    ("allow", "terraform fmt -check -recursive"),
    ("allow", "terraform validate"),
    ("allow", "terraform plan -out=tfplan"),
    ("allow", "terraform -chdir=envs/dev plan -var-file=dev.tfvars -out tfplan"),
    ("allow", "terraform show -json tfplan > plan.json"),
    ("allow", "terraform state list"),
    ("allow", "terraform workspace select dev && terraform plan"),
    ("allow", "terraform version"),
    ("allow", "tofu plan -out=tfplan"),
    ("allow", "terragrunt run-all plan"),
    ("allow", "terragrunt hclfmt --terragrunt-check"),
    ("allow", "cdk synth"),
    ("allow", "npx cdk diff OrderStack --profile audit"),
    ("allow", "cdk ls"),
    ("allow", "cd infra && npm ci && npx cdk synth --quiet"),
    ("allow", "tflint --recursive && checkov -d ."),
    ("allow", "aws sts get-caller-identity"),
    ("allow", "git status"),
    # applying
    ("deny", "terraform apply"),
    ("deny", "terraform apply -auto-approve tfplan"),
    ("deny", "terraform -chdir=envs/prod apply"),
    ("deny", "terraform destroy"),
    ("deny", "terraform plan -out=tfplan && terraform apply tfplan"),
    ("deny", "terraform import aws_s3_bucket.example example-bucket"),
    ("deny", "terraform refresh"),
    ("deny", "terraform test"),
    ("deny", "terraform taint aws_instance.example"),
    ("deny", "terraform force-unlock 0123"),
    ("deny", "tofu apply"),
    ("deny", "terragrunt run-all apply"),
    ("deny", "terragrunt destroy"),
    ("deny", "cdk deploy"),
    ("deny", "npx cdk deploy --all --require-approval never"),
    ("deny", "yarn cdk destroy OrderStack"),
    ("deny", "npx aws-cdk deploy"),
    ("deny", "npx cdk@2 deploy --all"),
    ("deny", "npx aws-cdk@2.150.0 destroy OrderStack"),
    ("allow", "npx aws-cdk diff"),
    ("allow", "npx cdk@2 synth"),
    ("deny", "npm run cdk -- deploy"),
    ("deny", "cdk bootstrap"),
    ("deny", "cdk watch"),
    ("deny", "cdk import"),
    ("deny", "bash -c 'cd infra && terraform apply -auto-approve'"),
    ("deny", "aws cloudformation deploy --stack-name example --template-file t.yaml"),
    # the state
    ("deny", "terraform state rm aws_instance.example"),
    ("deny", "terraform state mv aws_instance.a aws_instance.b"),
    ("deny", "terraform state pull > state.json"),
    ("deny", "terraform state push state.json"),
    ("deny", "terraform init -migrate-state"),
    ("deny", "terraform workspace delete old"),
    ("deny", "terraform workspace select -or-create=true feature-x"),
    ("deny", "terraform workspace new feature-x"),
    # may print secrets, or cannot tell
    ("ask", "terraform output -json"),
    ("ask", "terraform state show aws_db_instance.example"),
    ("ask", "terraform console"),
    ("ask", "terraform plan -var 'x=unterminated"),
]


def run(command):
    event = {"tool_name": "Bash", "tool_input": {"command": command}}
    proc = subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(event),
        capture_output=True, text=True, check=False,
    )
    if proc.returncode == 2:
        return "deny"
    if proc.returncode != 0:
        return f"error {proc.returncode}: {proc.stderr.strip()}"
    if proc.stdout.strip():
        return json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"]
    return "allow"


def main():
    failures = [f"  expected {expected}, got {run(command)}: {command!r}"
                for expected, command in CASES if run(command) != expected]
    if failures:
        print("test-guard-iac: FAILED", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"test-guard-iac: ok ({len(CASES)} commands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
