# Makefile Help Annotation

## Task

When asked to update a Makefile, add self-documenting help annotations to all targets.

## The Pattern

Every user-facing target gets a `## Description` annotation on the same `:` line:

```makefile
target-name: dependencies ## Short description of what this target does
	recipe commands
```

The `help` target (always the first target, making it the default) uses `awk` to extract and display these annotations:

```makefile
help: ## Display available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
```

## Rules

1. **`help` must be the first target** in the Makefile so `make` with no arguments shows help.
2. **Annotate every target** that a user would invoke directly.
3. **Do NOT annotate** internal/helper targets prefixed with `_` or `.` — these are implementation details.
4. **Descriptions must be:**
   - A single line, no period at the end
   - Imperative mood ("Build the binary" not "Builds the binary")
   - Under 60 characters
   - Specific enough to distinguish from other targets
5. **Preserve existing behavior** — only add/modify the `## comment` portion. Never change target names, dependencies, or recipes.
6. **If `help` already exists**, verify it uses the correct awk pattern and update if needed.
7. **Group related targets** by keeping them adjacent. Do not reorder unrelated targets.

## Onboarding an Existing Makefile

When a Makefile has no annotations yet:

1. Read the entire Makefile to understand all targets and their recipes.
2. Insert the `help` target as the first target (after any variable declarations, `.PHONY`, or includes at the top).
3. For each existing target, determine its purpose from the recipe commands and add a `## Description`.
4. If a `.PHONY` declaration exists, add `help` to it.

## Examples

```makefile
# Before
build:
	go build -o bin/app ./cmd/app

test:
	go test ./...

lint:
	golangci-lint run
```

```makefile
# After
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
- Every public target appears in the help output
- No internal targets leak into help output
- The awk field separator pattern `:.*## ` matches all annotated lines


## Standalone Prompt

Use this as a one-shot prompt when asking AI to annotate an existing Makefile.

---

## Prompt

```
Review the following Makefile and add self-documenting help annotations.

Requirements:
- Add a `help` target as the FIRST target with this exact recipe:
  help: ## Display available targets
  	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
- For every user-facing target, append `## Description` to its rule line (after the colon and any dependencies, before any line break).
- Descriptions: imperative mood, under 60 chars, no trailing period.
- Do NOT annotate internal targets (those starting with _ or .).
- Do NOT change target names, dependencies, variable assignments, or recipes.
- If .PHONY exists, include `help` in it.

Output the complete updated Makefile.
```
