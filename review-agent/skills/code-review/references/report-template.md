# Report Template

Use this structure for the final code review output.

## Scope

Start with a short scope statement that includes:

- target folder reviewed
- important inclusions
- important exclusions or skipped areas

## File-wise Review

Create one section per relevant file.

Recommended shape:

```md
### path/to/file.ext

What is good:
- ...

Findings:
- [high|medium|low] ...

Suggested improvement:
- ...
```

Notes:

- If a file has no meaningful issues, say so briefly instead of forcing findings.
- Use severity only when it adds clarity.
- Keep findings concrete and tied to visible code.

## Overall Summary

End with a concise project-level summary that includes:

- overall code quality impression
- recurring strengths
- recurring risks
- top priorities to fix first

## Style Rules

- Prefer Markdown headings over raw dumps.
- Keep each finding actionable.
- Avoid repeating the same issue across many files without summarizing the pattern.
- If many files share one problem, mention the repeated pattern in the overall summary too.
