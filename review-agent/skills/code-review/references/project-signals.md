# Project Signals

Use this guide to infer the project's main languages, frameworks, and likely quality checks before reviewing source files deeply.

## Read Early

Look for top-level signals such as:

- `package.json`
- `tsconfig.json`
- `pyproject.toml`
- `requirements.txt`
- `poetry.lock`
- `Pipfile`
- `Cargo.toml`
- `go.mod`
- `pom.xml`
- `build.gradle`
- `Gemfile`
- `.eslintrc*`
- `eslint.config.*`
- `.prettierrc*`
- `ruff.toml`
- `mypy.ini`
- `pytest.ini`
- `tox.ini`
- `.golangci.*`
- `.github/workflows/*`
- `Makefile`

## Infer From Signals

Use visible config and manifest files to infer:

- primary language
- framework
- formatter or linter
- test framework
- build system
- type-checking setup

Examples:

- `package.json` + `tsconfig.json` suggests JavaScript/TypeScript review expectations
- `pyproject.toml` + `ruff.toml` suggests Python style and lint signals
- `Cargo.toml` suggests Rust project structure and tooling
- `go.mod` suggests Go module layout and Go tooling

## Review Implication

Use the discovered signals to decide:

- which directories are most important
- which config files define the project's standards
- whether test or lint commands are worth checking
- which idioms are normal for that language/framework

## Safety Rule

Do not assume a framework or convention without evidence from files in the project.

If signals conflict, mention the ambiguity briefly in the scope or summary.
