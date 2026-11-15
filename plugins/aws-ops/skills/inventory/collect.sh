#!/usr/bin/env bash
# Fetches the network and compute configuration of one or more regions with the
# AWS CLI and stores the raw JSON, one file per call.
#
# Usage: bash collect.sh <output-directory> <region> [<region> ...]
#   Writes <output-directory>/<region>/<name>.json. A call that fails leaves
#   <name>.error with the message and the script goes on, so a missing
#   permission for one service does not stop the rest.
#
# Every call is a read (describe-*, list-*, get-*, select-*, search): nothing is
# changed. The
# credential and profile come from the environment (AWS_PROFILE and so on).
# Needs bash, the aws CLI and python3.
set -uo pipefail

out=${1:?usage: collect.sh <output-directory> <region> [<region> ...]}
shift
[ "$#" -ge 1 ] || { echo "usage: collect.sh <output-directory> <region> [<region> ...]" >&2; exit 2; }

failed=0
fetch() { # fetch <region> <name> <aws arguments...>
  local region=$1 name=$2
  shift 2
  local dir="$out/$region"
  mkdir -p "$dir"
  local message
  if message=$(aws "$@" --region "$region" --output json 2>&1 > "$dir/$name.json.part"); then
    mv "$dir/$name.json.part" "$dir/$name.json"
    if [ -e "$dir/$name.error" ]; then unlink "$dir/$name.error"; fi
    echo "fetched  $region/$name"
  else
    unlink "$dir/$name.json.part"
    if [ -e "$dir/$name.json" ]; then unlink "$dir/$name.json"; fi
    printf '%s\n' "$message" > "$dir/$name.error"
    failed=$((failed + 1))
    echo "failed   $region/$name ($(printf '%s' "$message" | head -n 1))"
  fi
}
# Prints the strings of a JSON list in a file, one per line.
strings() { python3 -c 'import json, sys; [print(x) for x in json.load(open(sys.argv[1])).get(sys.argv[2], [])]' "$1" "$2"; }

for region in "$@"; do
  fetch "$region" vpcs ec2 describe-vpcs
  fetch "$region" subnets ec2 describe-subnets
  fetch "$region" route-tables ec2 describe-route-tables
  fetch "$region" internet-gateways ec2 describe-internet-gateways
  fetch "$region" nat-gateways ec2 describe-nat-gateways
  fetch "$region" vpc-endpoints ec2 describe-vpc-endpoints
  fetch "$region" vpc-peering-connections ec2 describe-vpc-peering-connections
  fetch "$region" security-groups ec2 describe-security-groups
  fetch "$region" instances ec2 describe-instances
  fetch "$region" load-balancers elbv2 describe-load-balancers
  fetch "$region" lambda-functions lambda list-functions
  fetch "$region" db-instances rds describe-db-instances
  fetch "$region" ecs-clusters ecs list-clusters

  # Discovery: every resource the account knows of, whatever its type, so that
  # types without a table of their own still show up in the record. Each source
  # has gaps (Config: recorded types only; tagging: resources that have or had
  # tags; Resource Explorer: needs an index, at most 1000 results), so all
  # three are tried and the record says which ones answered.
  fetch "$region" discovered-config configservice select-resource-config \
    --expression "SELECT arn, resourceType, resourceName, tags WHERE awsRegion = '$region'"
  fetch "$region" discovered-tagged resourcegroupstaggingapi get-resources
  fetch "$region" discovered-explorer resource-explorer-2 search --query-string "region:$region"

  # ECS services: list per cluster, then describe ten at a time (the API limit).
  if [ -f "$out/$region/ecs-clusters.json" ]; then
    n=0
    while IFS= read -r cluster; do
      n=$((n + 1))
      fetch "$region" "ecs-service-arns-$n" ecs list-services --cluster "$cluster"
      [ -f "$out/$region/ecs-service-arns-$n.json" ] || continue
      batch=()
      m=0
      while IFS= read -r service; do
        batch+=("$service")
        if [ "${#batch[@]}" -eq 10 ]; then
          m=$((m + 1))
          fetch "$region" "ecs-services-$n-$m" ecs describe-services --cluster "$cluster" --services "${batch[@]}"
          batch=()
        fi
      done < <(strings "$out/$region/ecs-service-arns-$n.json" serviceArns)
      if [ "${#batch[@]}" -gt 0 ]; then
        m=$((m + 1))
        fetch "$region" "ecs-services-$n-$m" ecs describe-services --cluster "$cluster" --services "${batch[@]}"
      fi
    done < <(strings "$out/$region/ecs-clusters.json" clusterArns)
  fi
done

if [ "$failed" -gt 0 ]; then
  echo "collect: $failed call(s) failed; the inventory will say which parts are missing" >&2
fi
exit 0
