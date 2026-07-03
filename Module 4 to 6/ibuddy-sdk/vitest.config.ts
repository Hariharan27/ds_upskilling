import { resolve } from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: {
    alias: {
      "@ibuddy/core": resolve(__dirname, "packages/core/src/index.ts"),
      "@ibuddy/react-web": resolve(__dirname, "packages/react-web/src/index.ts")
    }
  },
  test: {
    environment: "jsdom",
    include: ["packages/**/*.test.ts", "packages/**/*.test.tsx"]
  }
});
