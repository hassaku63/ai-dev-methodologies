.DEFAULT_GOAL := help

.PHONY: help check docs-check shell-lint test-adopt test-guard-aws test-guard-iac test-findings test-inventory plugin-validate pr-size

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Every gate. CI calls this same target; each check is listed in docs/dev/harness.md.
check: docs-check shell-lint test-adopt test-guard-aws test-guard-iac test-findings test-inventory ## Run every gate

docs-check: ## Verify links, paths and the index in Markdown (scripts/check-docs.sh)
	bash scripts/check-docs.sh

SHELL_FILES := scripts/*.sh plugins/*/skills/*/*.sh plugins/*/skills/*/assets/managed/scripts/*.sh
shell-lint: ## shellcheck this repository's scripts and the scripts it hands out
	@command -v shellcheck >/dev/null || { echo "shellcheck not found: apt install shellcheck, brew install shellcheck, or pip install shellcheck-py"; exit 1; }
	shellcheck $(SHELL_FILES)

test-adopt: ## Adopt core into an empty repository and check the result (scripts/test-adopt.sh)
	bash scripts/test-adopt.sh

test-guard-aws: ## Check the aws-ops guard hook against a table of commands (scripts/test-guard-aws.py)
	python3 scripts/test-guard-aws.py

test-guard-iac: ## Check the aws-iac guard hook against a table of commands (scripts/test-guard-iac.py)
	python3 scripts/test-guard-iac.py

test-findings: ## Check the findings report of the fictional example (scripts/test-findings.sh)
	bash scripts/test-findings.sh

test-inventory: ## Check the inventory of the fictional example and collect.sh against a stub aws (scripts/test-inventory.sh)
	bash scripts/test-inventory.sh

plugin-validate: ## Validate the marketplace and its plugins (needs the claude CLI; not part of check)
	claude plugin validate .

PR_BASE ?= origin/main
pr-size: ## Count the lines this branch changes against PR_BASE (default origin/main); warn over 600, fail over 1000
	bash scripts/check-pr-size.sh $(PR_BASE)
