import { useMemo, useState, type ChangeEvent, type FC } from "react";
import { IBuddyChatWidget } from "@ibuddy/react-web";

const DEFAULT_BASE_URL = import.meta.env.VITE_IBUDDY_BASE_URL ?? "http://localhost:8000";
const DEFAULT_ENDPOINT = import.meta.env.VITE_IBUDDY_ENDPOINT ?? "/api/v1/chat";

export const App: FC = () => {
  const [baseUrl, setBaseUrl] = useState(DEFAULT_BASE_URL);
  const [endpoint, setEndpoint] = useState(DEFAULT_ENDPOINT);
  const [authorization, setAuthorization] = useState("");
  const [theme, setTheme] = useState<"light" | "dark" | "system">("system");
  const [lastEvent, setLastEvent] = useState("Ready to connect to your iBuddy backend.");

  const headers = useMemo(() => {
    const normalizedAuthorization = authorization.trim();

    if (normalizedAuthorization.length === 0) {
      return undefined;
    }

    return {
      Authorization: normalizedAuthorization
    };
  }, [authorization]);

  const handleInputChange =
    (setter: (value: string) => void) => (event: ChangeEvent<HTMLInputElement>) => {
      setter(event.target.value);
    };

  return (
    <main className="example-shell">
      <section className="example-hero">
        <div className="example-eyebrow">iBuddy SDK Example</div>
        <h1 className="example-title">Production-ready web chat integration in one component.</h1>
        <p className="example-copy">
          Point the widget at your backend, adjust headers when needed, and test the full chat
          experience against the SDK contract.
        </p>

        <div className="example-card-grid">
          <article className="example-card">
            <h2 className="example-card-title">Backend Settings</h2>
            <label className="example-field">
              <span>Base URL</span>
              <input
                className="example-input"
                onChange={handleInputChange(setBaseUrl)}
                value={baseUrl}
              />
            </label>
            <label className="example-field">
              <span>Endpoint</span>
              <input
                className="example-input"
                onChange={handleInputChange(setEndpoint)}
                value={endpoint}
              />
            </label>
            <label className="example-field">
              <span>Authorization Header</span>
              <input
                className="example-input"
                onChange={handleInputChange(setAuthorization)}
                placeholder="Bearer token"
                value={authorization}
              />
            </label>
          </article>

          <article className="example-card">
            <h2 className="example-card-title">Widget Settings</h2>
            <div className="example-theme-toggle" role="radiogroup" aria-label="Theme selection">
              {(["system", "light", "dark"] as const).map((option) => (
                <button
                  key={option}
                  aria-checked={theme === option}
                  className="example-toggle-button"
                  data-active={theme === option}
                  onClick={() => setTheme(option)}
                  role="radio"
                  type="button"
                >
                  {option}
                </button>
              ))}
            </div>
            <div className="example-code-block">
              <span className="example-code-title">Live integration</span>
              <code>{`<IBuddyChatWidget baseUrl="${baseUrl}" endpoint="${endpoint}" />`}</code>
            </div>
            <div className="example-status">
              <span className="example-status-label">Last event</span>
              <p>{lastEvent}</p>
            </div>
          </article>
        </div>
      </section>

      <section className="example-preview">
        <article className="example-preview-card">
          <h2 className="example-card-title">How to test</h2>
          <p className="example-copy example-copy-compact">
            Start your backend using the configured env values or update the fields above, then open
            the floating launcher in the lower-right corner.
          </p>
        </article>
      </section>

      <IBuddyChatWidget
        baseUrl={baseUrl}
        endpoint={endpoint}
        initialOpen
        launcherLabel="Ask iBuddy"
        onError={(error) => setLastEvent(`Error: ${error.message}`)}
        onMessageReceived={(result) => setLastEvent(`Assistant replied with ${result.answer}`)}
        onMessageSent={(query) => setLastEvent(`Sent: ${query}`)}
        placeholder="Ask iBuddy about company policies..."
        subtitle="Helping Every Ideator Find Answers Faster"
        theme={theme}
        title="IBuddy"
        welcomeMessage=" 👋 Welcome to iBuddy!

I'm your Workplace Knowledge Companion, here to help you quickly find answers about company policies, HR guidelines, IT support, security practices, benefits, and more.

Ask me a question in natural language, and I'll search the available knowledge base to provide accurate, context-aware answers along with the relevant source documents.

How can I help you today?"
        {...(headers ? { headers } : {})}
      />
    </main>
  );
};
