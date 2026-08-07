# Validation Policy

Use this guide when deciding whether to run tests, linters, builds, or other project checks during a review.

## When To Validate

Try validation when:

- a finding depends on actual runtime or build behavior
- the project clearly provides an existing lint, test, or build command
- a suspected issue can be confirmed cheaply and safely
- the user explicitly asks for stronger verification

## What To Prefer

Prefer existing project checks over inventing new ones, such as:

- lint commands already defined by the project
- test commands already defined by the project
- type-check commands
- build commands that are part of the normal workflow

## What Not To Do

Do not:

- install new dependencies just to validate a review
- create custom validation scripts unless the user explicitly asks
- run risky or destructive commands
- treat missing tooling as a defect by itself unless the project signals that tooling is expected

## Reporting Rule

If you ran validation, report:

- which command or check was used
- whether it passed, failed, or could not run
- how that affected confidence in the finding

If you did not run validation, say whether the point is:

- a confirmed issue from visible code
- a likely risk
- an assumption needing verification

## Approval Awareness

Keep validation scoped and minimal.

If a command would require extra approval, avoid it unless it meaningfully improves the review quality or the user explicitly wants deeper verification.
