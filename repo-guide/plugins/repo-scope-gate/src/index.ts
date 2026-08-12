import {
  definePluginEntry,
  type OpenClawPluginDefinition,
} from "openclaw/plugin-sdk/plugin-entry";

const CLEARLY_UNRELATED_PATTERNS = [
  /\bwhat is the capital of\b/i,
  /\bwho is the president of\b/i,
  /\bwhat is the weather\b/i,
  /\bweather forecast\b/i,
  /\brecipe for\b/i,
  /\bmovie recommendation\b/i,
  /\bsong recommendation\b/i,
  /\btranslate this\b/i,
];

function isClearlyUnrelated(prompt: string): boolean {
  return CLEARLY_UNRELATED_PATTERNS.some((pattern) =>
    pattern.test(prompt),
  );
}

const plugin: OpenClawPluginDefinition = definePluginEntry({
  id: "repo-scope-gate",
  name: "Repo Scope Gate",
  description: "Blocks agent runs that are clearly unrelated to the repository.",

  register(api) {
    api.on("before_agent_run", async (event) => {
      if (isClearlyUnrelated(event.prompt)) {
        return {
          outcome: "block",
          reason: "request-outside-repository-scope",
          message:
            "I can only help with questions related to this repository and OpenClaw workspace.",
        };
      }

      return {
        outcome: "pass",
      };
    });
  },
});

export default plugin;