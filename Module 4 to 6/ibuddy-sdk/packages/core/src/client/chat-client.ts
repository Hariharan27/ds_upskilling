import { ValidationError } from "../errors/index.js";
import type {
  IBuddyAskResult,
  IBuddyChatRequest,
  IBuddyChatResponse,
  IBuddyMessage,
  IBuddySourceReference
} from "../models/index.js";
import { ConversationManager } from "../managers/index.js";
import { APIClient } from "./api-client.js";

export class ChatClient {
  public constructor(
    private readonly apiClient: APIClient,
    private readonly conversationManager: ConversationManager
  ) {}

  public async ask(query: string): Promise<IBuddyAskResult> {
    const normalizedQuery = query.trim();

    if (normalizedQuery.length === 0) {
      throw new ValidationError("Query cannot be empty.");
    }

    const previousHistory = this.conversationManager.history();
    const conversationHistory = this.conversationManager.toRequestHistory();
    this.conversationManager.addMessage("user", normalizedQuery);

    const request: IBuddyChatRequest = {
      query: normalizedQuery,
      conversation_history: conversationHistory
    };

    try {
      const response = await this.apiClient.post<IBuddyChatResponse>(request);
      const normalizedSources: IBuddySourceReference[] = (response.sources ?? []).map((source) =>
        typeof source === "string" ? { title: source } : source
      );
      const assistantMessage = this.conversationManager.addMessage("assistant", response.answer, {
        sources: normalizedSources
      });

      return this.buildAskResult(response, assistantMessage, normalizedSources);
    } catch (error) {
      this.conversationManager.importHistory(previousHistory);
      throw error;
    }
  }

  public clear(): void {
    this.conversationManager.clear();
  }

  public history(): IBuddyMessage[] {
    return this.conversationManager.history();
  }

  public importHistory(messages: IBuddyMessage[]): IBuddyMessage[] {
    return this.conversationManager.importHistory(messages);
  }

  public exportHistory(): IBuddyMessage[] {
    return this.conversationManager.exportHistory();
  }

  private buildAskResult(
    response: IBuddyChatResponse,
    assistantMessage: IBuddyMessage,
    normalizedSources: IBuddySourceReference[]
  ): IBuddyAskResult {
    return {
      answer: response.answer,
      sources: normalizedSources,
      usage: {
        inputTokens: response.input_tokens,
        outputTokens: response.output_tokens,
        totalTokens: response.total_tokens
      },
      message: assistantMessage,
      history: this.conversationManager.history()
    };
  }
}
