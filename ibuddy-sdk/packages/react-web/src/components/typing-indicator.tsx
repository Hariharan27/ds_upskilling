import type { FC } from "react";

export const TypingIndicator: FC = () => (
  <div className="ibuddy-widget-row" data-role="assistant" data-status="sent">
    <div className="ibuddy-widget-typing" aria-live="polite" aria-label="Assistant is typing">
      <div className="ibuddy-widget-typing-dots" aria-hidden="true">
        <span className="ibuddy-widget-typing-dot" />
        <span className="ibuddy-widget-typing-dot" />
        <span className="ibuddy-widget-typing-dot" />
      </div>
      <span>iBuddy is preparing a response</span>
    </div>
  </div>
);
