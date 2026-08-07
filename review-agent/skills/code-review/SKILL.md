---
name: code-review
description: Review a project folder file by file and produce coding-standards feedback plus an overall summary.
---

# Code Review

Use this skill when the user asks for a code review of a project, repository, or folder.

## Goal

Review a target codebase file by file, identify relevant issues, and return:

- per-file findings
- coding standards and maintainability feedback
- an overall project summary

## Input Contract

Expected input:

- a folder path
- optionally a narrower scope such as specific files, languages, or review focus

If the user provides a folder path, use it as the review root.

If the user does not provide a folder path, ask for exactly one before starting the review.

If the path is ambiguous, ask a short clarifying question instead of guessing across multiple folders.

## Working Rules

- For tool choice, read `{baseDir}/references/tool-strategy.md` before starting the review.
- Prefer OpenClaw built-in capabilities for search, file reading, and execution before proposing custom tooling.
- Review the target project folder, not the current agent workspace, unless the user explicitly asks for the workspace itself.
- Work incrementally and keep the review scoped to the requested folder.
- Ignore irrelevant files unless the user asks otherwise.
- For file discovery and exclusions, read `{baseDir}/references/file-selection.md` before scanning the target tree.

## Review Process

1. Identify the target folder.
2. Read `{baseDir}/references/project-signals.md` before scanning the project.
3. Discover relevant source files and config files.
4. Infer the main languages and frameworks from the files present.
5. Read the most important files first.
6. Before judging code quality, read `{baseDir}/references/review-rubric.md`.
7. Read `{baseDir}/references/validation-policy.md` before running checks or confirming behavior.
8. Review file by file for:
   - correctness risks
   - code clarity
   - maintainability
   - consistency
   - obvious standards violations
9. Produce a concise overall summary after the file-wise review.

## Invocation Examples

Examples of valid requests:

- `Review /path/to/project`
- `Review ./src and focus on Python standards`
- `/code-review /path/to/repo`
- `Use $code-review for this folder: ./backend`

## Output Format

Before writing the final review, read `{baseDir}/references/report-template.md` and follow that structure.

## Guardrails

- Do not rewrite the whole codebase unless the user explicitly asks for fixes.
- Do not invent project requirements that are not visible in the code or user request.
- Call out assumptions and missing verification clearly.
- If the project is large, review the highest-signal files first and say what was not reviewed yet.
