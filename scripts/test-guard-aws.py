#!/usr/bin/env python3
"""Checks the aws-ops guard hook against a table of commands. Part of `make check`."""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "plugins/aws-ops/hooks/guard_aws.py"

CASES = [
    # reads
    ("allow", "aws ec2 describe-instances --region ap-northeast-1"),
    ("allow", "aws --profile audit --region us-east-1 securityhub get-findings --max-items 100"),
    ("allow", "aws --output json ec2 describe-vpcs | jq '.Vpcs[].VpcId'"),
    ("allow", "aws sts get-caller-identity"),
    ("allow", "aws s3 ls"),
    ("allow", "aws s3api list-buckets && aws s3api get-bucket-policy --bucket example"),
    ("allow", "aws ssm get-parameter --name /example/flag"),
    ("allow", "aws configure list"),
    ("allow", "aws ec2 help"),
    ("allow", "aws --version"),
    ("allow", "aws ec2 wait instance-running --instance-ids i-0123456789abcdef0"),
    ("allow", "aws logs filter-log-events --log-group-name /example/app"),
    ("allow", "for r in us-east-1 us-west-2; do aws ec2 describe-subnets --region $r > $r.json; done"),
    ("allow", "ids=$(aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text)"),
    ("allow", "/usr/local/bin/aws iam list-roles"),
    # not about aws
    ("allow", "git status"),
    ("allow", "ls plugins/aws-ops && cat docs/aws-notes.md"),
    ("allow", "grep -r 'aws_instance' ."),
    # writes
    ("deny", "aws ec2 terminate-instances --instance-ids i-0123456789abcdef0"),
    ("deny", "aws --profile admin ec2 stop-instances --instance-ids i-0123456789abcdef0"),
    ("deny", "aws s3 rm s3://example-bucket --recursive"),
    ("deny", "aws s3 cp s3://example-bucket/data.csv ."),
    ("deny", "aws iam create-access-key --user-name example"),
    ("deny", "aws securityhub batch-update-findings --finding-identifiers Id=x,ProductArn=y"),
    ("deny", "aws ec2 describe-instances && aws ec2 delete-security-group --group-id sg-0123456789abcdef0"),
    ("deny", "aws ec2 describe-instances\naws rds delete-db-instance --db-instance-identifier example"),
    ("deny", "echo $(aws lambda update-function-configuration --function-name example)"),
    ("deny", "echo `aws lambda delete-function --function-name example`"),
    ("deny", "bash -c 'aws ec2 run-instances --image-id ami-0123456789abcdef0'"),
    ("deny", "aws ec2 describe-instances --query 'x' --output text | xargs -I{} sh -c 'aws ec2 terminate-instances --instance-ids {}'"),
    ("deny", "aws configure set region us-east-1"),
    ("deny", "AWS_PROFILE=admin aws ec2 terminate-instances --instance-ids i-0123456789abcdef0"),
    ("deny", "sudo \"aws\" ec2 reboot-instances --instance-ids i-0123456789abcdef0"),
    ("deny", "aws cloudformation deploy --stack-name example --template-file t.yaml"),
    # reads of secrets and data
    ("deny", "aws secretsmanager get-secret-value --secret-id example"),
    ("deny", "aws ssm get-parameter --name /example/password --with-decryption"),
    ("deny", "aws s3api get-object --bucket example --key data.csv out.csv"),
    ("deny", "aws sts assume-role --role-arn arn:aws:iam::111122223333:role/example --role-session-name x"),
    ("deny", "aws ecr get-login-password"),
    ("deny", "aws dynamodb get-item --table-name example --key '{}'"),
    # cannot tell
    ("ask", "aws ec2"),
    ("ask", "aws sso login --profile audit"),
    ("ask", "aws ec2 describe-instances --filters 'Name=tag:App,Values=x"),
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
        decision = json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"]
        return decision
    return "allow"


def main():
    failures = []
    for expected, command in CASES:
        got = run(command)
        if got != expected:
            failures.append(f"  expected {expected}, got {got}: {command!r}")
    # Other tools and malformed input pass through.
    other = subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps({"tool_name": "Read", "tool_input": {}}),
        capture_output=True, text=True, check=False,
    )
    if other.returncode != 0 or other.stdout:
        failures.append("  a non-Bash tool was not passed through")
    if failures:
        print("test-guard-aws: FAILED", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"test-guard-aws: ok ({len(CASES)} commands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
