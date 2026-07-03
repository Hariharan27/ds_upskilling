# iBuddy Frontend SDK

User guide for integrating the iBuddy SDK and React web UI package into your application.

## Packages

- `@ibuddy/core`: Framework-agnostic TypeScript SDK for chat orchestration.
- `@ibuddy/react-web`: React chat widget built on top of `@ibuddy/core`.

## Install

If you publish these packages to npm, consumers can install them with:

```bash
npm install @ibuddy/core @ibuddy/react-web
```

Until then, this repository uses local npm workspaces, so the sample app works because it consumes the local packages from this repo.

## Backend Contract

The SDK expects a `POST` endpoint with this request shape:

```json
{
  "query": "Hello",
  "conversation_history": []
}
```

Expected response:

```json
{
  "answer": "Hi there",
  "sources": [],
  "input_tokens": 0,
  "output_tokens": 0,
  "total_tokens": 0
}
```

## Use The SDK

Import `IBuddyChat` from `@ibuddy/core` and let the SDK manage the conversation history for you.

```ts
import { IBuddyChat } from "@ibuddy/core";

const chat = new IBuddyChat({
  baseUrl: "http://localhost:8000",
  endpoint: "/api/v1/chat",
  headers: {
    Authorization: "Bearer token"
  },
  timeout: 30000
});

const result = await chat.ask("Hello");

console.log(result.answer);
console.log(result.sources);
console.log(result.usage.totalTokens);
```

### Available SDK Methods

```ts
chat.ask("Hello");
chat.clear();
chat.history();
chat.importHistory(messages);
chat.exportHistory();
chat.setHeaders({
  Authorization: "Bearer updated-token"
});
```

### Update Headers Without Recreating The SDK

```ts
chat.setHeaders({
  Authorization: "Bearer next-token",
  "X-Tenant-Id": "tenant-123"
});
```

### Read Conversation History

```ts
const history = chat.history();

history.forEach((message) => {
  console.log(message.role, message.content, message.timestamp);
});
```

### Import Existing Messages

```ts
chat.importHistory([
  {
    id: "msg_1",
    role: "user",
    content: "Hello",
    timestamp: new Date().toISOString()
  },
  {
    id: "msg_2",
    role: "assistant",
    content: "Hi, how can I help?",
    timestamp: new Date().toISOString()
  }
]);
```

## Use The React Web UI Package

Import `IBuddyChatWidget` from `@ibuddy/react-web`.

```tsx
import { IBuddyChatWidget } from "@ibuddy/react-web";

export function SupportPage() {
  return (
    <IBuddyChatWidget
      baseUrl="http://localhost:8000"
      endpoint="/api/v1/chat"
      title="iBuddy Assistant"
      subtitle="Enterprise AI support"
      placeholder="Ask iBuddy anything..."
      launcherLabel="Chat with iBuddy"
      theme="system"
    />
  );
}
```

### Widget Props

- `baseUrl`: Required backend base URL.
- `endpoint`: Required chat endpoint.
- `headers`: Optional request headers.
- `timeout`: Optional request timeout in milliseconds.
- `title`: Optional window title.
- `subtitle`: Optional helper text.
- `placeholder`: Optional input placeholder.
- `launcherLabel`: Optional floating launcher label.
- `welcomeMessage`: Optional empty-state message.
- `theme`: Optional `light`, `dark`, or `system`.
- `initialOpen`: Optional boolean to open the widget by default.
- `className`: Optional root class name.
- `style`: Optional inline style object.
- `onError`: Optional callback for request failures.
- `onMessageSent`: Optional callback when a user message is submitted.
- `onMessageReceived`: Optional callback when the assistant response is received.

### Widget With Auth Headers

```tsx
import { IBuddyChatWidget } from "@ibuddy/react-web";

export function App() {
  return (
    <IBuddyChatWidget
      baseUrl="http://localhost:8000"
      endpoint="/api/v1/chat"
      headers={{
        Authorization: "Bearer token"
      }}
      theme="dark"
      onError={(error) => {
        console.error(error.message);
      }}
      onMessageReceived={(result) => {
        console.log(result.answer);
      }}
    />
  );
}
```

## Package Selection

Use `@ibuddy/core` when:

- You want to build your own UI.
- You need framework-independent chat logic.
- You want direct access to the SDK methods and history management.

Use `@ibuddy/react-web` when:

- You want a ready-to-use React chat widget.
- You want the SDK logic plus a production-ready web interface.
- You want a minimal integration surface in a React application.

## Local Example

A working integration example is available in [examples/react-web-example](/Users/ideas2it/Documents/Data Science &Gen AI/IBuddy SDK/examples/react-web-example).

### Step By Step

1. Install dependencies from the project root.

```bash
npm install
```

2. Create an env file for the sample app.

Copy [examples/react-web-example/.env.example](/Users/ideas2it/Documents/Data Science &Gen AI/IBuddy SDK/examples/react-web-example/.env.example) to `examples/react-web-example/.env`.

```bash
cp examples/react-web-example/.env.example examples/react-web-example/.env
```

3. Update the backend values in `examples/react-web-example/.env`.

```bash
VITE_IBUDDY_BASE_URL=http://localhost:8000
VITE_IBUDDY_ENDPOINT=/api/v1/chat
```

4. Start your backend so the sample can reach the chat API.

5. Start the sample app.

```bash
npm run dev --workspace react-web-example
```

6. Open the local Vite URL in your browser and test the widget.

The sample app reads these env variables:

- `VITE_IBUDDY_BASE_URL`
- `VITE_IBUDDY_ENDPOINT`
