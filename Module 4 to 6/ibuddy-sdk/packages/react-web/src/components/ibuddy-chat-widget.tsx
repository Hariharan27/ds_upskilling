import { useState, type FC } from "react";
import { useChatWidget } from "../hooks/use-chat-widget.js";
import { useResolvedTheme } from "../hooks/use-resolved-theme.js";
import { widgetStyles } from "../theme.js";
import type { IBuddyChatWidgetProps } from "../types.js";
import { ChatWindow } from "./chat-window.js";
import { LauncherButton } from "./launcher-button.js";

export const IBuddyChatWidget: FC<IBuddyChatWidgetProps> = ({
  className,
  initialOpen = false,
  launcherLabel = "Chat with iBuddy",
  placeholder = "Ask a question...",
  style,
  subtitle = "Enterprise AI support",
  theme = "system",
  title = "IBuddy",
  welcomeMessage,  
  ...chatProps
}) => {
  const [isOpen, setIsOpen] = useState(initialOpen);
  const resolvedTheme = useResolvedTheme(theme);
  const { clearConversation, isLoading, messages, retryMessage, sendMessage } = useChatWidget(chatProps);

  return (
    <div
      className={["ibuddy-widget", className].filter(Boolean).join(" ")}
      data-theme={resolvedTheme}
      style={style}
    >
      <style>{widgetStyles}</style>
      <div className="ibuddy-widget-shell">
        {isOpen ? (
          <ChatWindow
            isLoading={isLoading}
            isOpen={isOpen}
            messages={messages}
            onClear={clearConversation}
            onClose={() => setIsOpen(false)}
            onRetry={(messageId) => void retryMessage(messageId)}
            onSend={sendMessage}
            placeholder={placeholder}
            subtitle={subtitle}
            title={title}
            {...(welcomeMessage ? { welcomeMessage } : {})}
          />
        ) : (
          <LauncherButton label={launcherLabel} onClick={() => setIsOpen(true)} />
        )}
      </div>
    </div>
  );
};
