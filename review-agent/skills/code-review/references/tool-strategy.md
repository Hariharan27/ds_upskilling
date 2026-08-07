# Tool Strategy

Use this guide to decide which built-in OpenClaw capabilities to use during a code review.

## Default Tool Order

Prefer this order:

1. workspace-aware search and file reading
2. local `exec` for safe project inspection when shell commands are useful
3. remote analysis tools only when they truly fit the task

## Use Local File/Workspace Capabilities For

Use normal workspace-aware reading and search for:

- finding source files
- reading code and config
- locating repeated patterns
- checking manifests, tests, and CI files
- gathering evidence for review findings

## Use `exec` For

Use local `exec` only when shell inspection is the simplest way to understand the project, such as:

- listing files
- searching large trees efficiently
- printing config or manifest files
- running safe read-oriented inspection commands
- optionally running existing lint or test commands when that helps validate a finding

When using `exec`:

- keep commands scoped to the target project folder
- prefer read-only inspection first
- do not mutate project files unless the user explicitly asks for fixes
- avoid unnecessary approvals or risky commands

## Do Not Prefer Remote `code_execution` For

Do not use remote `code_execution` as the normal review path for local repositories because it:

- runs on xAI servers
- cannot access local project files directly
- is better for isolated calculations than repository inspection

Use it only if the user explicitly wants remote analysis of data already extracted from the project.

## Verification Rule

If a finding depends on actual project behavior, prefer:

- reading the relevant code first
- then running existing tests, linters, or build checks if needed and safe

If you cannot verify behavior, report the issue as a likely risk or assumption instead of a confirmed defect.
