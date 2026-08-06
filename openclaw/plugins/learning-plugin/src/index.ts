import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";

export default defineToolPlugin({
  id: "learning-plugin",
  name: "Learning Plugin",
  description: "Add Learning Plugin tools to OpenClaw.",
  tools: (tool) => [
    tool({
      name: "echo",
      description: "Echo input text.",
      parameters: Type.Object({
        input: Type.String({ description: "Text to echo." }),
      }),
      execute: async ({ input }) => ({
  message: "🚀 Hello from my Learning Plugin!",
  receivedInput: input,
  plugin: "learning-plugin",
  version: "0.1.0",
}),
    }),
  ],
});
