import { IBuddyChat, type IBuddyAskResult, type IBuddyMessage } from "@ibuddy/core";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { IBuddyChatWidgetProps, WidgetMessage } from "../types.js";

const MIN_TYPING_INDICATOR_MS = 450;

function toWidgetMessages(messages: IBuddyMessage[]): WidgetMessage[] {
  return messages.map((message) => ({
    ...message,
    status: "sent"
  }));
}

function wait(duration: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, duration);
  });
}

export function useChatWidget(props: IBuddyChatWidgetProps) {
  const {
    baseUrl,
    endpoint,
    headers,
    timeout,
    onError,
    onMessageReceived,
    onMessageSent
  } = props;

  const chatRef = useRef<IBuddyChat | null>(null);
  const isLoadingRef = useRef(false);
  const pendingMessageRef = useRef<string | null>(null);
  const loadingStartedAtRef = useRef<number | null>(null);
  const [messages, setMessages] = useState<WidgetMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    isLoadingRef.current = isLoading;
  }, [isLoading]);

  useEffect(() => {
    const chat = new IBuddyChat({
      baseUrl,
      endpoint,
      ...(headers ? { headers } : {}),
      ...(timeout ? { timeout } : {})
    });

    chatRef.current = chat;
    setMessages(toWidgetMessages(chat.history()));
    setIsLoading(false);
    pendingMessageRef.current = null;
  }, [baseUrl, endpoint, timeout]);

  useEffect(() => {
    if (!headers || !chatRef.current) {
      return;
    }

    chatRef.current.setHeaders(headers);
  }, [headers]);

  const sendMessage = useCallback(
    async (query: string) => {
      const chat = chatRef.current;
      const normalizedQuery = query.trim();

      if (!chat || normalizedQuery.length === 0 || isLoadingRef.current) {
        return null;
      }

      const optimisticMessage: WidgetMessage = {
        id: `pending_${Date.now()}`,
        role: "user",
        content: normalizedQuery,
        timestamp: new Date().toISOString(),
        status: "sent"
      };

      pendingMessageRef.current = optimisticMessage.id;
      loadingStartedAtRef.current = Date.now();
      setMessages((currentMessages) => [...currentMessages, optimisticMessage]);
      setIsLoading(true);
      onMessageSent?.(normalizedQuery);

      try {
        const result = await chat.ask(normalizedQuery);
        await ensureMinimumTypingVisibility(loadingStartedAtRef.current);
        setMessages(toWidgetMessages(result.history));
        setIsLoading(false);
        pendingMessageRef.current = null;
        loadingStartedAtRef.current = null;
        onMessageReceived?.(result);
        return result;
      } catch (error) {
        const typedError = error instanceof Error ? error : new Error("Unable to send message.");

        // Log the full error (including cause) so the root issue is visible in the browser console.
        console.error("[IBuddy] sendMessage failed:", typedError);
        if ("cause" in typedError && typedError.cause !== undefined) {
          console.error("[IBuddy] Caused by:", typedError.cause);
        }

        await ensureMinimumTypingVisibility(loadingStartedAtRef.current);
        setMessages((currentMessages) =>
          currentMessages.map((message) =>
            message.id === pendingMessageRef.current
              ? {
                  ...message,
                  status: "failed"
                }
              : message
          )
        );
        setIsLoading(false);
        pendingMessageRef.current = null;
        loadingStartedAtRef.current = null;
        onError?.(typedError);
        return typedError;
      }
    },
    [onError, onMessageReceived, onMessageSent]
  );

  const retryMessage = useCallback(
    async (messageId: string) => {
      const failedMessage = messages.find((message) => message.id === messageId && message.status === "failed");

      if (!failedMessage) {
        return null;
      }

      setMessages((currentMessages) => currentMessages.filter((message) => message.id !== messageId));
      return sendMessage(failedMessage.content);
    },
    [messages, sendMessage]
  );

  const clearConversation = useCallback(() => {
    const chat = chatRef.current;

    if (!chat) {
      return;
    }

    chat.clear();
    setMessages([]);
    setIsLoading(false);
    pendingMessageRef.current = null;
    loadingStartedAtRef.current = null;
  }, []);

  const lastAssistantMessage = useMemo(
    () => [...messages].reverse().find((message) => message.role === "assistant") ?? null,
    [messages]
  );

  return {
    clearConversation,
    isLoading,
    lastAssistantMessage,
    messages,
    retryMessage,
    sendMessage
  };
}

async function ensureMinimumTypingVisibility(startedAt: number | null): Promise<void> {
  if (startedAt === null) {
    return;
  }

  const elapsed = Date.now() - startedAt;
  const remaining = MIN_TYPING_INDICATOR_MS - elapsed;

  if (remaining > 0) {
    await wait(remaining);
  }
}
