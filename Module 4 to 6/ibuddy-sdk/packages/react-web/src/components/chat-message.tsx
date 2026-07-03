import type { FC } from "react";
import type { IBuddySourceReference } from "@ibuddy/core";
import type { WidgetMessage } from "../types.js";
import { formatTimestamp } from "../utils/format.js";
import { renderMarkdown } from "../utils/markdown.js";

function SourceReference({ source }: { source: IBuddySourceReference }) {
  const title = source.title ?? source.url ?? source.id ?? "Reference";
  const href = typeof source.url === "string" ? source.url : undefined;

  if (!href) {
    return (
      <div className="ibuddy-widget-source">
        <div className="ibuddy-widget-source-copy">
          <span className="ibuddy-widget-source-title">{title}</span>
          {typeof source.snippet === "string" && source.snippet.length > 0 ? (
            <span className="ibuddy-widget-source-url">{source.snippet}</span>
          ) : null}
        </div>
      </div>
    );
  }

  return (
    <a
      className="ibuddy-widget-source"
      href={href}
      rel="noreferrer"
      target="_blank"
      title={title}
    >
      <div className="ibuddy-widget-source-copy">
        <span className="ibuddy-widget-source-title">{title}</span>
        <span className="ibuddy-widget-source-url">{href}</span>
      </div>
    </a>
  );
}

export const ChatMessage: FC<{
  message: WidgetMessage;
  onRetry: (messageId: string) => void;
}> = ({ message, onRetry }) => {
  const timestamp = formatTimestamp(message.timestamp);

  return (
    <div className="ibuddy-widget-row" data-role={message.role} data-status={message.status}>
      {message.role === "assistant" ? (
        <div
          className="ibuddy-widget-bubble ibuddy-widget-bubble--markdown"
          dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }}
        />
      ) : (
        <div className="ibuddy-widget-bubble">{message.content}</div>
      )}
      {message.role === "assistant" && message.sources && message.sources.length > 0 ? (
        <div className="ibuddy-widget-sources">
          {message.sources.map((source, index) => (
            <SourceReference
              key={source.id ?? source.url ?? `${message.id}_source_${index}`}
              source={source}
            />
          ))}
        </div>
      ) : null}
      <div className="ibuddy-widget-meta">
        {timestamp ? <span>{timestamp}</span> : null}
        {message.status === "failed" ? (
          <button className="ibuddy-widget-retry" onClick={() => onRetry(message.id)} type="button">
            Retry
          </button>
        ) : null}
      </div>
    </div>
  );
};
