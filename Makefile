help: ## Display available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Sync skills into all configured tool directories
	@python3 ./_tools/sync.py

test: ## Run tests and report exit status
	@python3 -m unittest discover -s _tools -p 'test_*.py' -v; python3 _tools/sync.py; status=$$?; printf 'exit=%s\n' "$$status"

index: ## Update README.md with skills index
	@python3 ./_tools/index.py

.PHONY: help sync test index
