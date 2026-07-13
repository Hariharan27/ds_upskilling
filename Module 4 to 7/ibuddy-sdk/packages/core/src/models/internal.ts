import type { IBuddyChatResponse } from "./chat.js";
import type { IBuddyHeaders } from "../config/index.js";

export interface RequestOptions {
  headers?: IBuddyHeaders;
  signal?: AbortSignal;
  timeout?: number;
}

export interface ParsedChatResponse extends IBuddyChatResponse {
  sources: NonNullable<IBuddyChatResponse["sources"]>;
}
