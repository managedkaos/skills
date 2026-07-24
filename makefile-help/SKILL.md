---
name: makefile-help
description: >-
  Annotate a Makefile with self-documenting help targets. Adds a `help` target
  as the default and appends inline ## descriptions to every user-facing target.
when_to_use: >-
  annotate makefile, makefile help, document makefile, add makefile comments,
  self-documenting make targets, onboard makefile
argument-hint: [path/to/Makefile]
arguments: [filepath]
allowed-tools: Read Edit
disable-model-invocation: false
paths: "**/*.Makefile, Makefile"
---

# Annotate Makefile with Self-Documenting Help

## Task

Read the Makefile at `$filepath` (if no path given, look for `Makefile` or `GNUmakefile` in the working directory). Add self-documenting help annotations to all user-facing targets.

## The Pattern

Every user-facing target gets a `## Description` annotation inline on the `:` line:

```makefile
target-name: dependencies ## Short description of what this target does
	recipe commands
```

The `help` target must be the **first target** in the file (making it the default). It uses this exact recipe:

```makefile
help: ## Display available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
```

## Rules

1. `help` must be the first target so `make` with no arguments shows help.
2. Annotate every target that a user would invoke directly.
3. Do NOT annotate internal/helper targets prefixed with `_` or `.`.
4. Descriptions must be:
   - A single line, no period at the end
   - Imperative mood ("Build the binary" not "Builds the binary")
   - Under 60 characters
   - Specific enough to distinguish from other targets
5. Preserve existing behavior — only add/modify the `## comment` portion. Never change target names, dependencies, or recipes.
6. If `help` already exists, verify it uses the correct awk pattern and update if needed.
7. Keep related targets adjacent. Do not reorder unrelated targets.
8. If a `.PHONY` declaration exists, add `help` to it.

## Procedure

1. Read the entire Makefile.
2. If no `help` target exists, insert it as the first target (after variable declarations, `.PHONY`, or includes at the top).
3. For each user-facing target, determine its purpose from the recipe and add `## Description` inline.
4. Write back the updated Makefile using Edit.

## Example

Before:
```makefile
build:
	go build -o bin/app ./cmd/app

test:
	go test ./...

lint:
	golangci-lint run
```

After:
```makefile
help: ## Display available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the application binary
	go build -o bin/app ./cmd/app

test: ## Run the test suite
	go test ./...

lint: ## Run the linter
	golangci-lint run
```

## Validation

After updating, confirm:
- `make` (no args) would print the help table
- Every public target has a `## Description`
- No internal targets leak into help output
- The awk field separator `:.*## ` matches all annotated lines
