# Run Code Review

Use this agent through a normal OpenClaw agent turn and explicitly reference the skill.

## Recommended Command

```bash
openclaw agent --agent main --message 'Use $code-review to review this folder: /absolute/path/to/project'
```

## Recommended Prompt Shape

Use this prompt pattern:

```text
Use $code-review to review this folder: /absolute/path/to/project
Focus on file-wise coding standards feedback and an overall summary.
```

## Narrower Scope Examples

```bash
openclaw agent --agent main --message 'Use $code-review to review this folder: /absolute/path/to/project. Focus on Python standards.'
```

```bash
openclaw agent --agent main --message 'Use $code-review to review this folder: /absolute/path/to/project/src. Prioritize critical issues only.'
```

## Best Practice

- pass one clear folder path
- explicitly reference `$code-review`
- keep the request focused
- ask for deeper verification only when you want lint/test/build checks considered
