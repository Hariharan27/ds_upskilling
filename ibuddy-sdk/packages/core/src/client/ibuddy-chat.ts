import { resolveConfig } from "../config/index.js";
import type { IBuddyChatConfig, IBuddyHeaders } from "../config/index.js";
import { ConversationManager, MemoryManager } from "../managers/index.js";
import type { IBuddyAskResult, IBuddyMessage } from "../models/index.js";
import { APIClient } from "./api-client.js";
import { ChatClient } from "./chat-client.js";

export class IBuddyChat {
  private readonly apiClient: APIClient;
  private readonly chatClient: ChatClient;

  public constructor(config: IBuddyChatConfig) {
    const resolvedConfig = resolveConfig(config);
    const conversationManager = new ConversationManager(new MemoryManager());

    this.apiClient = new APIClient({
      baseUrl: resolvedConfig.baseUrl,
      endpoint: resolvedConfig.endpoint,
      headers: resolvedConfig.headers,
      timeout: resolvedConfig.timeout,
      fetch: resolvedConfig.fetch
    });

    this.chatClient = new ChatClient(this.apiClient, conversationManager);
  }

  public ask(query: string): Promise<IBuddyAskResult> {
    return this.chatClient.ask(query);
  }

  public clear(): void {
    this.chatClient.clear();
  }

  public history(): IBuddyMessage[] {
    return this.chatClient.history();
  }

  public importHistory(messages: IBuddyMessage[]): IBuddyMessage[] {
    return this.chatClient.importHistory(messages);
  }

  public exportHistory(): IBuddyMessage[] {
    return this.chatClient.exportHistory();
  }

  public setHeaders(headers: IBuddyHeaders): void {
    this.apiClient.setHeaders(headers);
  }
}
