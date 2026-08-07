# Review Rubric

Use this rubric when giving coding-standards feedback across different languages and frameworks.

## Core Review Dimensions

Check each relevant file for:

- correctness
- readability
- maintainability
- consistency
- testability
- error handling
- security-sensitive mistakes
- obvious performance issues when they are visible in code

## What Good Looks Like

Prefer code that is:

- clear to read
- small in responsibility
- consistent with surrounding project style
- explicit about edge cases
- easy to test
- safe with inputs, outputs, and failures

## Common Findings

Watch for issues such as:

- unclear naming
- duplicated logic
- overly large functions or classes
- hidden side effects
- weak input validation
- missing or inconsistent error handling
- dead code
- commented-out code that should be removed
- inconsistent formatting or structure
- tightly coupled logic that is hard to test

## Severity Guidance

Use severity only when it improves clarity:

- `high`: correctness, security, data-loss, or major maintainability risk
- `medium`: likely bug risk, poor design choice, or repeated standards issue
- `low`: minor clarity, consistency, or cleanup issue

## Language-Agnostic Rule

Do not force one language's conventions onto another language. Review against:

- the language's normal idioms
- the visible style of the project
- the project's own config files when present

## Evidence Rule

Base findings on visible code, config, or project structure.

If something might be a problem but is not provable from the files reviewed, label it as a risk or assumption instead of a definite defect.
