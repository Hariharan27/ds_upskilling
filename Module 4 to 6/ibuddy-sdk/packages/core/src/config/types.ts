export type IBuddyHeaders = Record<string, string>;

export interface IBuddyChatConfig {
  baseUrl: string;
  endpoint: string;
  headers?: IBuddyHeaders;
  timeout?: number;
  fetch?: typeof globalThis.fetch;
}

export interface ResolvedIBuddyChatConfig {
  baseUrl: string;
  endpoint: string;
  headers: IBuddyHeaders;
  timeout: number;
  fetch: typeof globalThis.fetch;
}
