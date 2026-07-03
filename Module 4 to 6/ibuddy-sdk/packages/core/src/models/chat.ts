export type IBuddyRole = "user" | "assistant";

export interface IBuddySourceReference {
  id?: string;
  title?: string;
  url?: string;
  snippet?: string;
  [key: string]: unknown;
}

export interface IBuddyTokenUsage {
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}

export interface IBuddyMessage {
  id: string;
  role: IBuddyRole;
  content: string;
  timestamp: string;
  sources?: IBuddySourceReference[];
}

export interface IBuddyConversationHistoryItem {
  role: IBuddyRole;
  content: string;
}

export interface IBuddyChatRequest {
  query: string;
  conversation_history: IBuddyConversationHistoryItem[];
}

export interface IBuddyChatResponse {
  answer: string;
  sources: (IBuddySourceReference | string)[];
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}

export interface IBuddyAskResult {
  answer: string;
  sources: IBuddySourceReference[];
  usage: IBuddyTokenUsage;
  message: IBuddyMessage;
  history: IBuddyMessage[];
}
