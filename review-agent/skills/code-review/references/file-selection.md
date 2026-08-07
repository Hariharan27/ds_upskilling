# File Selection

Use this guide when deciding which files to review first and which files to skip.

## Review First

Prioritize these files:

- application source files
- library source files
- shared utilities
- entry points
- API routes
- business logic
- tests that describe expected behavior
- lint, formatter, type-check, and build configuration
- dependency manifests
- CI or workflow files when they affect quality gates

## Usually Skip

Skip these by default unless the user asks for them:

- `node_modules/`
- `.git/`
- `.next/`
- `dist/`
- `build/`
- `coverage/`
- `.cache/`
- compiled binaries
- minified assets
- lock-generated vendor output
- generated SDKs or generated clients
- large media files
- `.env` files and secret-bearing files

## Generated File Heuristics

Treat a file as generated or low-value review material when it is clearly marked by signals such as:

- `generated`
- `auto-generated`
- `do not edit`
- build artifact headers
- machine-produced bundles or minified output

If generated code appears to be committed incorrectly or is causing project risk, mention that in the summary instead of spending most of the review on the generated content.

## Priority Heuristics

If the project is large, prefer this order:

1. dependency manifest and top-level config
2. main source directories
3. core business logic
4. tests
5. secondary tooling and workflow files

## Reporting Scope

If you skip files or directories, say so briefly in the review scope statement.
