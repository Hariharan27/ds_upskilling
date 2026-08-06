# OpenClaw Plugin Development Journey

**Framework Version:** OpenClaw 2026.7.1-2

**Goal**

Learn the complete OpenClaw plugin lifecycle from scratch by creating a custom Tool Plugin, understanding the runtime architecture, and verifying each stage experimentally instead of making assumptions.

---

# Overall Architecture

```text
                    Workspace
                        │
                        ▼
                AGENTS / IDENTITY
                        │
                        ▼
                  OpenClaw Agent
                        │
                        ▼
                     Gateway
                        │
                        ▼
                 Plugin Discovery
                        │
                        ▼
                dist/index.js
                        │
                        ▼
              defineToolPlugin()
                        │
                        ▼
                 Tool Registry
                        │
                        ▼
                  LLM Tool Calling
                        │
                        ▼
                  execute()
                        │
                        ▼
                  Tool Result
                        │
                        ▼
                Final AI Response
```

---

# Phase 1 – Environment Verification

## Objective

Verify the OpenClaw installation before creating anything.

## Commands

```bash
openclaw --version

openclaw doctor

openclaw agents list
```

## Learned

- Verified OpenClaw installation.
- Verified plugin subsystem.
- Verified Together AI model.
- Inspected existing agents.

---

# Phase 2 – Creating a New Agent

## Command

```bash
openclaw agents add learning \
  --workspace "<workspace>" \
  --model together/openai/gpt-oss-20b
```

## Learned

- Agents are registered separately from the workspace.
- Workspace can be any folder.
- Runtime state is not immediately created.

---

# Phase 3 – Agent Runtime

Before first execution:

```text
~/.openclaw/agents/learning

└── sessions/
```

After starting the agent:

```text
~/.openclaw/agents/learning

├── agent/
│   ├── openclaw-agent.sqlite
│   ├── sqlite-shm
│   └── sqlite-wal
└── sessions/
```

## Discovery

✅ Runtime is lazily initialized.

The SQLite database is created only after the first execution.

---

# Phase 4 – Workspace Structure

Workspace contains:

```text
AGENTS.md
BOOTSTRAP.md
HEARTBEAT.md
IDENTITY.md
SOUL.md
TOOLS.md
USER.md
```

## Learned

Workspace owns:

- Identity
- Instructions
- Tool documentation
- User context

Runtime data is stored separately.

---

# Phase 5 – Creating the Plugin

## Command

```bash
openclaw plugins init learning-plugin \
    --directory <plugin-folder>
```

Generated:

```text
learning-plugin/

├── openclaw.plugin.json
├── package.json
├── README.md
├── src/
│   ├── index.ts
│   └── index.test.ts
├── tsconfig.json
└── vitest.config.ts
```

---

# Phase 6 – Understanding Plugin Structure

## Manifest

```text
openclaw.plugin.json
```

Contains:

- id
- version
- activation
- contracts
- config schema

---

## package.json

Contains:

- build scripts
- validation scripts
- plugin metadata
- OpenClaw extension entry

---

## Plugin Entry

```ts
defineToolPlugin({
    ...
})
```

Registers:

```ts
tool({
    ...
})
```

No manual registration required.

---

# Phase 7 – Understanding defineToolPlugin()

Architecture:

```text
defineToolPlugin()

        │

        ▼

tool()

        │

        ▼

execute()
```

Everything starts from `defineToolPlugin()`.

---

# Phase 8 – Build Lifecycle

## Commands

```bash
npm install

npm run plugin:build
```

Pipeline:

```text
TypeScript

↓

tsc

↓

dist/index.js

↓

plugins build

↓

Manifest Synchronization
```

## Verified

`plugins build`

- imports `dist/index.js`
- synchronizes `openclaw.plugin.json`
- synchronizes `package.json`

---

# Phase 9 – Runtime Discovery

Compiled file:

```text
dist/index.js
```

Still contains:

```ts
defineToolPlugin(...)
```

## Discovery

OpenClaw loads plugins at runtime.

No code generation.

No wrapper generation.

---

# Phase 10 – Plugin Installation

Command

```bash
openclaw plugins install --link <plugin-folder>
```

## Learned

Development mode uses symbolic linking.

Plugin is not copied.

---

# Phase 11 – Plugin Inspection

Commands

```bash
openclaw plugins list --verbose

openclaw plugins inspect learning-plugin
```

Learned

Plugin:

```text
Status: loaded

Source:

dist/index.js
```

Meaning:

Runtime loads:

```text
dist/index.js
```

not

```text
src/index.ts
```

---

# Phase 12 – Gateway Restart

After installation:

Gateway restart required.

Plugin becomes available to runtime.

---

# Phase 13 – First Tool Execution

Prompt:

```
Use the echo tool with input "Hello OpenClaw"
```

Observed:

```text
_output

↓

final
```

## Verified Runtime

```text
User

↓

LLM

↓

Tool Selection

↓

Plugin

↓

execute()

↓

Tool Result

↓

LLM Final Response
```

---

# Phase 14 – Modifying the Plugin

Changed

```ts
execute(...)
```

to

```ts
return {
    message: "🚀 Hello from my Learning Plugin!",
    plugin: "learning-plugin",
    version: "0.1.0",
    receivedInput: input
}
```

Rebuilt plugin.

Restarted gateway.

Executed tool again.

Observed:

```
🚀 Hello from my Learning Plugin!
```

## Verified

Our plugin code is actually executing.

---

# Complete Runtime Flow

```text
User Prompt
      │
      ▼
LLM (gpt-oss-20b)
      │
      ▼
Tool Selection
      │
      ▼
Gateway
      │
      ▼
Plugin Loader
      │
      ▼
dist/index.js
      │
      ▼
defineToolPlugin()
      │
      ▼
tool()
      │
      ▼
execute()
      │
      ▼
Tool Result
      │
      ▼
LLM Final Response
```

---

# Verified Discoveries

## ✅ Verified from Documentation

- Plugin scaffold generated using `plugins init`
- `plugins build` imports `dist/index.js`
- `plugins build` synchronizes plugin metadata
- Local development uses `plugins install --link`

---

## ✅ Verified Experimentally

- Agent runtime is lazily initialized.
- Workspace owns agent markdown files.
- Runtime state stored separately.
- Plugins are loaded from `dist/index.js`.
- Gateway restart required after installation.
- `defineToolPlugin()` executes at runtime.
- Tool registration happens automatically.
- Tool execution invokes our custom `execute()` function.
- Plugin modifications require rebuild + gateway restart.

---

# Development Lifecycle

```text
Create Agent

↓

Create Plugin

↓

Build Plugin

↓

Install Plugin

↓

Restart Gateway

↓

Inspect Plugin

↓

Run Agent

↓

Invoke Tool

↓

execute()

↓

Tool Result

↓

LLM Response
```

---

# Future Roadmap

- Refactor plugin into production structure.
- Replace sample `echo` tool with custom `hello` tool.
- Add calculator tool.
- Add external REST API integration.
- Add enterprise HRMS tools.
- Explore capability plugins and provider plugins.
- Understand tool debugging and raw execution traces.

---

# Key Takeaways

- OpenClaw separates workspace, runtime, and plugins.
- Plugins are independent Node.js packages.
- `defineToolPlugin()` is the runtime entry point.
- `plugins build` synchronizes plugin metadata.
- Runtime loads `dist/index.js`.
- Gateway is responsible for plugin loading.
- LLM automatically discovers registered tools.
- `execute()` contains the actual business logic.
- The LLM decides how much of the tool result to expose in the final response.