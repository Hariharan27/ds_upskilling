export const widgetStyles = `
.ibuddy-widget {
  --ibuddy-bg: #f4f7fb;
  --ibuddy-panel: rgba(255, 255, 255, 0.96);
  --ibuddy-panel-strong: #ffffff;
  --ibuddy-border: rgba(15, 23, 42, 0.08);
  --ibuddy-border-strong: rgba(15, 23, 42, 0.14);
  --ibuddy-shadow: 0 32px 80px rgba(15, 23, 42, 0.18);
  --ibuddy-text: #0f172a;
  --ibuddy-text-muted: #526079;
  --ibuddy-brand: #0f766e;
  --ibuddy-brand-strong: #115e59;
  --ibuddy-brand-soft: rgba(15, 118, 110, 0.12);
  --ibuddy-accent: #0891b2;
  --ibuddy-user-bubble: linear-gradient(135deg, #0f766e 0%, #0f5f91 100%);
  --ibuddy-assistant-bubble: #ffffff;
  --ibuddy-input: rgba(255, 255, 255, 0.92);
  --ibuddy-danger: #b91c1c;
  --ibuddy-danger-soft: rgba(185, 28, 28, 0.1);
  color: var(--ibuddy-text);
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
}

.ibuddy-widget[data-theme="dark"] {
  --ibuddy-bg: #08111f;
  --ibuddy-panel: rgba(10, 18, 30, 0.94);
  --ibuddy-panel-strong: #0f1c2d;
  --ibuddy-border: rgba(148, 163, 184, 0.12);
  --ibuddy-border-strong: rgba(148, 163, 184, 0.2);
  --ibuddy-shadow: 0 36px 90px rgba(2, 8, 23, 0.55);
  --ibuddy-text: #e2e8f0;
  --ibuddy-text-muted: #94a3b8;
  --ibuddy-brand: #2dd4bf;
  --ibuddy-brand-strong: #5eead4;
  --ibuddy-brand-soft: rgba(45, 212, 191, 0.14);
  --ibuddy-accent: #38bdf8;
  --ibuddy-user-bubble: linear-gradient(135deg, #0f766e 0%, #0369a1 100%);
  --ibuddy-assistant-bubble: #0f1c2d;
  --ibuddy-input: rgba(15, 28, 45, 0.96);
  --ibuddy-danger: #fca5a5;
  --ibuddy-danger-soft: rgba(248, 113, 113, 0.12);
}

.ibuddy-widget *,
.ibuddy-widget *::before,
.ibuddy-widget *::after {
  box-sizing: border-box;
}

.ibuddy-widget button,
.ibuddy-widget input {
  font: inherit;
}

.ibuddy-widget-shell {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 2147483000;
}

.ibuddy-widget-panel {
  width: min(420px, calc(100vw - 32px));
  height: min(720px, calc(100vh - 120px));
  display: flex;
  flex-direction: column;
  border: 1px solid var(--ibuddy-border);
  border-radius: 28px;
  overflow: hidden;
  background:
    radial-gradient(circle at top, rgba(8, 145, 178, 0.16), transparent 34%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0)),
    var(--ibuddy-panel);
  backdrop-filter: blur(22px);
  box-shadow: var(--ibuddy-shadow);
  transform-origin: bottom right;
  animation: ibuddy-panel-enter 220ms ease-out;
}

.ibuddy-widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 20px 18px;
  border-bottom: 1px solid var(--ibuddy-border);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), transparent);
}

.ibuddy-widget-header-copy {
  min-width: 0;
}

.ibuddy-widget-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.ibuddy-widget-subtitle {
  margin: 6px 0 0;
  color: var(--ibuddy-text-muted);
  font-size: 13px;
}

.ibuddy-widget-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ibuddy-widget-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--ibuddy-brand-soft);
  color: var(--ibuddy-brand);
  font-size: 12px;
  font-weight: 600;
}

.ibuddy-widget-pill-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #16a34a;
  filter: drop-shadow(0 0 8px rgba(22, 163, 74, 0.25));
}

.ibuddy-widget-icon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--ibuddy-border);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--ibuddy-text);
  cursor: pointer;
  transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

.ibuddy-widget-icon-button:hover {
  transform: translateY(-1px);
  border-color: var(--ibuddy-border-strong);
}

.ibuddy-widget-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(circle at top right, rgba(8, 145, 178, 0.08), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.02), transparent),
    var(--ibuddy-bg);
  scroll-behavior: smooth;
}

.ibuddy-widget-body-spacer {
  flex: 1;
}

.ibuddy-widget-empty {
  padding: 20px;
  border: 1px solid var(--ibuddy-border);
  border-radius: 22px;
  background: color-mix(in srgb, var(--ibuddy-panel-strong) 84%, transparent);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.ibuddy-widget-empty-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.ibuddy-widget-empty-copy {
  margin: 0;
  color: var(--ibuddy-text-muted);
  line-height: 1.55;
}

.ibuddy-widget-messages {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ibuddy-widget-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 88%;
  animation: ibuddy-message-enter 200ms ease-out;
}

.ibuddy-widget-row[data-role="user"] {
  align-self: flex-end;
  align-items: flex-end;
}

.ibuddy-widget-row[data-role="assistant"] {
  align-self: flex-start;
  align-items: flex-start;
}

.ibuddy-widget-bubble {
  padding: 14px 16px;
  border-radius: 20px;
  line-height: 1.6;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  border: 1px solid transparent;
}

.ibuddy-widget-bubble--markdown {
  white-space: normal;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-p {
  margin: 0 0 10px;
  line-height: 1.65;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-p:last-child {
  margin-bottom: 0;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-h3 {
  margin: 12px 0 6px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-h4 {
  margin: 10px 0 4px;
  font-size: 13px;
  font-weight: 700;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-ul {
  margin: 6px 0 10px;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-ul:last-child {
  margin-bottom: 0;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-ul li {
  line-height: 1.6;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-mixed {
  margin: 6px 0;
}

.ibuddy-widget-bubble--markdown .ibuddy-md-line {
  display: block;
  line-height: 1.65;
}

.ibuddy-widget-bubble--markdown strong {
  font-weight: 700;
}

.ibuddy-widget-bubble--markdown em {
  font-style: italic;
}

.ibuddy-widget-row[data-role="assistant"] .ibuddy-widget-bubble {
  background: var(--ibuddy-assistant-bubble);
  border-color: var(--ibuddy-border);
  color: var(--ibuddy-text);
  box-shadow: 0 12px 34px rgba(15, 23, 42, 0.08);
}

.ibuddy-widget-row[data-role="user"] .ibuddy-widget-bubble {
  background: var(--ibuddy-user-bubble);
  color: #f8fafc;
  box-shadow: 0 16px 36px rgba(15, 118, 110, 0.24);
}

.ibuddy-widget-row[data-status="failed"] .ibuddy-widget-bubble {
  border-color: var(--ibuddy-danger);
  background: var(--ibuddy-danger-soft);
  color: var(--ibuddy-danger);
  box-shadow: none;
}

.ibuddy-widget-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--ibuddy-text-muted);
  font-size: 12px;
}

.ibuddy-widget-retry {
  border: 0;
  padding: 0;
  background: none;
  color: var(--ibuddy-danger);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.ibuddy-widget-sources {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ibuddy-widget-source {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  max-width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--ibuddy-border);
  border-radius: 14px;
  background: color-mix(in srgb, var(--ibuddy-panel-strong) 88%, transparent);
  color: var(--ibuddy-text);
  text-decoration: none;
  transition: transform 160ms ease, border-color 160ms ease;
}

.ibuddy-widget-source:hover {
  transform: translateY(-1px);
  border-color: var(--ibuddy-border-strong);
}

.ibuddy-widget-source-copy {
  min-width: 0;
}

.ibuddy-widget-source-title {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 12px;
  font-weight: 600;
}

.ibuddy-widget-source-url {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--ibuddy-text-muted);
  font-size: 11px;
}

.ibuddy-widget-footer {
  padding: 18px 20px 20px;
  border-top: 1px solid var(--ibuddy-border);
  background: linear-gradient(180deg, transparent, rgba(255, 255, 255, 0.02));
}

.ibuddy-widget-input-shell {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px 10px 14px;
  border: 1.5px solid var(--ibuddy-border);
  border-radius: 22px;
  background: var(--ibuddy-input);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  transition: border-color 160ms ease, box-shadow 160ms ease;
}

.ibuddy-widget-input-shell:focus-within {
  border-color: var(--ibuddy-brand);
  box-shadow: 0 0 0 3px var(--ibuddy-brand-soft), inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.ibuddy-widget-input {
  flex: 1;
  min-height: 24px;
  max-height: 132px;
  resize: none;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--ibuddy-text);
  font-size: 14px;
  line-height: 1.55;
}

.ibuddy-widget-input::placeholder {
  color: var(--ibuddy-text-muted);
}

.ibuddy-widget-send {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 38px;
  height: 38px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--ibuddy-brand) 0%, var(--ibuddy-accent) 100%);
  color: white;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(8, 145, 178, 0.3);
  transition: transform 160ms ease, opacity 160ms ease, box-shadow 160ms ease;
}

.ibuddy-widget-send:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(8, 145, 178, 0.35);
}

.ibuddy-widget-send:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}

.ibuddy-widget-footer-note {
  margin: 10px 2px 0;
  color: var(--ibuddy-text-muted);
  font-size: 11px;
}

.ibuddy-widget-launcher {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border: 0;
  border-radius: 999px;
  background: linear-gradient(135deg, #0f172a 0%, #0f766e 100%);
  color: white;
  cursor: pointer;
  box-shadow: 0 28px 64px rgba(15, 23, 42, 0.28);
  animation: ibuddy-launcher-enter 180ms ease-out;
}

.ibuddy-widget-launcher-label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.ibuddy-widget-launcher-title {
  font-size: 13px;
  font-weight: 600;
}

.ibuddy-widget-launcher-copy {
  font-size: 11px;
  opacity: 0.82;
}

.ibuddy-widget-launcher-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
}

.ibuddy-widget-typing {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px;
  border-radius: 20px;
  border: 1px solid var(--ibuddy-border);
  background: var(--ibuddy-assistant-bubble);
  box-shadow: 0 12px 34px rgba(15, 23, 42, 0.08);
}

.ibuddy-widget-typing-dots {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.ibuddy-widget-typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--ibuddy-brand);
  animation: ibuddy-dot-bounce 1.2s infinite ease-in-out;
}

.ibuddy-widget-typing-dot:nth-child(2) {
  animation-delay: 120ms;
}

.ibuddy-widget-typing-dot:nth-child(3) {
  animation-delay: 240ms;
}

@keyframes ibuddy-dot-bounce {
  0%, 80%, 100% {
    transform: scale(0.55);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes ibuddy-panel-enter {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes ibuddy-launcher-enter {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes ibuddy-message-enter {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .ibuddy-widget-shell {
    right: 16px;
    left: 16px;
    bottom: 16px;
  }

  .ibuddy-widget-panel {
    width: 100%;
    height: min(78vh, 720px);
  }

  .ibuddy-widget-row {
    max-width: 94%;
  }

  .ibuddy-widget-launcher {
    width: 100%;
    justify-content: center;
  }
}
`;
