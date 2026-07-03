import type { IBuddyMessage } from "../models/index.js";

export interface MemoryStore {
  get(): IBuddyMessage[];
  set(messages: IBuddyMessage[]): void;
  clear(): void;
}

export class InMemoryStore implements MemoryStore {
  private messages: IBuddyMessage[] = [];

  public get(): IBuddyMessage[] {
    return [...this.messages];
  }

  public set(messages: IBuddyMessage[]): void {
    this.messages = [...messages];
  }

  public clear(): void {
    this.messages = [];
  }
}

export class MemoryManager {
  public constructor(private readonly store: MemoryStore = new InMemoryStore()) {}

  public getMessages(): IBuddyMessage[] {
    return this.store.get();
  }

  public setMessages(messages: IBuddyMessage[]): void {
    this.store.set(messages);
  }

  public appendMessage(message: IBuddyMessage): void {
    const messages = this.store.get();
    messages.push(message);
    this.store.set(messages);
  }

  public clear(): void {
    this.store.clear();
  }
}
