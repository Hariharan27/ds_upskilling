# Building My Personal GitHub Assistant with OpenClaw

## Goal

Build a personal AI assistant using OpenClaw that is accessible from Telegram.

Initial scope:

- Receive messages from Telegram
- Route them to a dedicated OpenClaw agent
- Get natural language responses from the configured LLM

---

# Phase 1 – Telegram Connected Agent

## 1. Create a dedicated agent

```bash
openclaw agents add github-assistant \
  --workspace ~/.openclaw/workspace-github
```

Verify:

```bash
openclaw agents list
```

---

## 2. Create a Telegram Bot

- Open Telegram
- Search for **@BotFather**
- Run:

```text
/newbot
```

- Choose a bot name
- Copy the Bot Token

Example:

```text
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 3. Configure the Telegram Bot Token

Export the token before starting the gateway.

```bash
export TELEGRAM_BOT_TOKEN="<BOT_TOKEN>"
```

Verify:

```bash
echo $TELEGRAM_BOT_TOKEN
```

> **Important:** Do **not** escape the colon (`:`). The token should look exactly as provided by BotFather.

Correct:

```text
123456789:AAxxxx...
```

Incorrect:

```text
123456789\:AAxxxx...
```

---

## 4. Bind Telegram to the Agent

```bash
openclaw agents bind \
    --agent github-assistant \
    --bind telegram
```

This creates a route in `~/.openclaw/openclaw.json` similar to:

```json
"bindings": [
  {
    "type": "route",
    "agentId": "github-assistant",
    "match": {
      "channel": "telegram"
    }
  }
]
```

---

## 5. Start the Gateway

```bash
openclaw gateway
```

Successful startup should include logs similar to:

```text
[gateway] ready

[telegram] [default] starting provider

[telegram] isolated polling ingress started
```

---

## 6. Pair the Telegram Account

Open the bot.

Send:

```text
hello
```

The first message triggers the OpenClaw pairing flow.

Approve the pairing.

Once paired, all future messages are routed to the configured agent.

---

## 7. Verify End-to-End

Send:

```text
What is Python?
```

Expected flow:

```text
Telegram
      │
      ▼
OpenClaw Gateway
      │
      ▼
github-assistant Agent
      │
      ▼
Together AI
      │
      ▼
Telegram Response
```

If the bot replies, Phase 1 is complete.

---

# Outcome

✅ Dedicated OpenClaw Agent

✅ Telegram Channel Connected

✅ Agent Routing Configured

✅ Together AI Model Responding

✅ End-to-End Natural Language Conversation Working

---

# Next Phase

Connect GitHub to the agent so it can answer:

> Show my open pull requests

using existing OpenClaw capabilities before adding custom skills.