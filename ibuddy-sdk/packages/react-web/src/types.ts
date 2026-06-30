import type { CSSProperties } from "react";
import type { IBuddyAskResult, IBuddyChatConfig, IBuddyMessage } from "@ibuddy/core";

export type IBuddyWidgetTheme = "light" | "dark" | "system";

export interface IBuddyChatWidgetProps
  extends Pick<IBuddyChatConfig, "baseUrl" | "endpoint" | "headers" | "timeout"> {
  title?: string;
  subtitle?: string;
  placeholder?: string;
  launcherLabel?: string;
  welcomeMessage?: string;
  theme?: IBuddyWidgetTheme;
  initialOpen?: boolean;
  className?: string;
  style?: CSSProperties;
  onError?: (error: Error) => void;
  onMessageSent?: (query: string) => void;
  onMessageReceived?: (result: IBuddyAskResult) => void;
}

export interface WidgetMessage extends IBuddyMessage {
  status: "sent" | "failed";
}
