import { ConfigurationError } from "../errors/index.js";
import type { IBuddyChatConfig, ResolvedIBuddyChatConfig } from "./types.js";
import { DEFAULT_TIMEOUT } from "./defaults.js";

export function resolveConfig(config: IBuddyChatConfig): ResolvedIBuddyChatConfig {
  if (!config.baseUrl || config.baseUrl.trim().length === 0) {
    throw new ConfigurationError("`baseUrl` is required.");
  }

  if (!config.endpoint || config.endpoint.trim().length === 0) {
    throw new ConfigurationError("`endpoint` is required.");
  }

  const fetchImplementation = config.fetch ?? globalThis.fetch.bind(globalThis);

  if (typeof fetchImplementation !== "function") {
    throw new ConfigurationError(
      "No fetch implementation found. Provide `fetch` in the SDK configuration."
    );
  }

  return {
    baseUrl: config.baseUrl,
    endpoint: config.endpoint,
    headers: { ...(config.headers ?? {}) },
    timeout: config.timeout ?? DEFAULT_TIMEOUT,
    fetch: fetchImplementation
  };
}
