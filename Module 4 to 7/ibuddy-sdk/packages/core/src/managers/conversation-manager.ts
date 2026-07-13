import type {
  IBuddyConversationHistoryItem,
  IBuddyMessage,
  IBuddyRole,
  IBuddySourceReference
} from "../models/index.js";
import { ValidationError } from "../errors/index.js";
import { createMessageId } from "../utils/index.js";
import { MemoryManager } from "./memory-manager.js";

export class ConversationManager {
  public constructor(private readonly memoryManager: MemoryManager = new MemoryManager()) {}

  public addMessage(
    role: IBuddyRole,
    content: string,
    options?: { sources?: IBuddySourceReference[]; timestamp?: string }
  ): IBuddyMessage {
    const normalizedContent = content.trim();

    if (normalizedContent.length === 0) {
      throw new ValidationError("Message content cannot be empty.");
    }

    const message: IBuddyMessage = {
      id: createMessageId(),
      role,
      content: normalizedContent,
      timestamp: options?.timestamp ?? new Date().toISOString(),
      ...(options?.sources ? { sources: options.sources } : {})
    };

    this.memoryManager.appendMessage(message);

    return message;
  }

  public clear(): void {
    this.memoryManager.clear();
  }

  public history(): IBuddyMessage[] {
    return this.memoryManager.getMessages();
  }

  public exportHistory(): IBuddyMessage[] {
    return this.history();
  }

  public importHistory(messages: IBuddyMessage[]): IBuddyMessage[] {
    const normalizedMessages = messages.map((message) => this.normalizeMessage(message));
    this.memoryManager.setMessages(normalizedMessages);
    return this.history();
  }

  public toRequestHistory(): IBuddyConversationHistoryItem[] {
    return this.history().map((message) => ({
      role: message.role,
      content: message.content
    }));
  }

  private normalizeMessage(message: IBuddyMessage): IBuddyMessage {
    if (!message.id || !message.role || !message.content || !message.timestamp) {
      throw new ValidationError("Imported history contains an invalid message.");
    }

    const normalizedContent = message.content.trim();

    if (normalizedContent.length === 0) {
      throw new ValidationError("Imported history contains an empty message.");
    }

    return {
      id: message.id,
      role: message.role,
      content: normalizedContent,
      timestamp: message.timestamp,
      ...(message.sources ? { sources: [...message.sources] } : {})
    };
  }
}
