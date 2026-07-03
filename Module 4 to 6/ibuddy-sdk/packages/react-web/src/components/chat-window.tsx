import { useEffect, useRef, useState, type FC, type FormEvent, type KeyboardEvent } from "react";
import type { WidgetMessage } from "../types.js";
import { useAutoResizeTextarea } from "../hooks/use-auto-resize-textarea.js";
import { ChatMessage } from "./chat-message.js";
import { TypingIndicator } from "./typing-indicator.js";

export const ChatWindow: FC<{
  isLoading: boolean;
  isOpen: boolean;
  messages: WidgetMessage[];
  onClose: () => void;
  onRetry: (messageId: string) => void;
  onSend: (query: string) => Promise<unknown>;
  onClear: () => void;
  placeholder: string;
  subtitle: string;
  title: string;
  welcomeMessage?: string;
}> = ({
  isLoading,
  isOpen,
  messages,
  onClear,
  onClose,
  onRetry,
  onSend,
  placeholder,
  subtitle,
  title,
  welcomeMessage
}) => {
  const [draft, setDraft] = useState("");
  const bodyRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  useAutoResizeTextarea(textareaRef, draft);

  useEffect(() => {
    if (!isOpen || !bodyRef.current) {
      return;
    }

    if (typeof bodyRef.current.scrollTo === "function") {
      bodyRef.current.scrollTo({
        top: bodyRef.current.scrollHeight,
        behavior: "smooth"
      });
      return;
    }

    bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
  }, [isLoading, isOpen, messages]);

  useEffect(() => {
    if (isOpen) {
      textareaRef.current?.focus();
    }
  }, [isOpen]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const normalizedDraft = draft.trim();

    if (normalizedDraft.length === 0 || isLoading) {
      return;
    }

    setDraft("");
    void onSend(normalizedDraft);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSubmit(event as unknown as FormEvent<HTMLFormElement>);
    }
  };

  return (
    <section className="ibuddy-widget-panel" aria-label="iBuddy chat window">
      <header className="ibuddy-widget-header">
        <div className="ibuddy-widget-header-copy">
          <h2 className="ibuddy-widget-title">{title}</h2>
          <p className="ibuddy-widget-subtitle">{subtitle}</p>
        </div>
        <div className="ibuddy-widget-header-actions">
          <span className="ibuddy-widget-pill">
            <span className="ibuddy-widget-pill-icon" aria-hidden="true">
              <svg fill="none" height="12" viewBox="0 0 12 12" width="12">
                <circle cx="6" cy="6" fill="currentColor" r="6" />
                <path
                  d="M3.4 6.1 5.05 7.75 8.6 4.2"
                  stroke="#ffffff"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="1.4"
                />
              </svg>
            </span>
            <span>Live</span>
          </span>
          <button
            aria-label="Clear conversation"
            className="ibuddy-widget-icon-button"
            onClick={onClear}
            type="button"
          >
            <svg fill="none" height="16" viewBox="0 0 24 24" width="16">
              <path
                d="M6 7h12M9 7V5.8c0-.67 0-1.01.13-1.27a1.2 1.2 0 0 1 .52-.53C9.91 3.87 10.24 3.87 10.9 3.87h2.2c.66 0 .99 0 1.25.13.22.11.41.3.52.53.13.26.13.6.13 1.27V7m-7 0 .63 10.19c.04.7.06 1.05.21 1.31.14.24.35.44.6.58.29.15.64.15 1.34.15h2.84c.7 0 1.05 0 1.34-.15.25-.14.46-.34.6-.58.15-.26.17-.61.21-1.31L16 7"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.8"
              />
            </svg>
          </button>
          <button
            aria-label="Collapse chat"
            className="ibuddy-widget-icon-button"
            onClick={onClose}
            type="button"
          >
            <svg fill="none" height="16" viewBox="0 0 24 24" width="16">
              <path
                d="M6 12h12"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.8"
              />
            </svg>
          </button>
        </div>
      </header>

      <div className="ibuddy-widget-body" ref={bodyRef}>
        <div className="ibuddy-widget-body-spacer" />

        {messages.length === 0 && !isLoading ? (
          <div className="ibuddy-widget-empty">
            <h3 className="ibuddy-widget-empty-title">Ask iBuddy anything</h3>
            <p className="ibuddy-widget-empty-copy">
              {welcomeMessage ??
                "Start the conversation and iBuddy will manage the history, responses, and references for you."}
            </p>
          </div>
        ) : null}

        <div className="ibuddy-widget-messages">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} onRetry={onRetry} />
          ))}
          {isLoading ? <TypingIndicator /> : null}
        </div>
      </div>

      <footer className="ibuddy-widget-footer">
        <form onSubmit={handleSubmit}>
          <div className="ibuddy-widget-input-shell">
            <textarea
              aria-label="Message input"
              className="ibuddy-widget-input"
              disabled={isLoading}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              ref={textareaRef}
              rows={1}
              value={draft}
            />
            <button
              aria-label="Send message"
              className="ibuddy-widget-send"
              disabled={isLoading || draft.trim().length === 0}
              type="submit"
            >
              <svg fill="none" height="16" viewBox="0 0 24 24" width="16">
                <path
                  d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                />
              </svg>
            </button>
          </div>
        </form>
        {isLoading ? <p className="ibuddy-widget-footer-note">Generating response...</p> : null}
      </footer>
    </section>
  );
};
