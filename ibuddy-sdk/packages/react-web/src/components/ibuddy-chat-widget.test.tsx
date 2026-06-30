import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { IBuddyChatWidget } from "./ibuddy-chat-widget.js";

function createChatResponse(answer: string) {
  return new Response(
    JSON.stringify({
      answer,
      sources: [],
      input_tokens: 10,
      output_tokens: 12,
      total_tokens: 22
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json"
      }
    }
  );
}

describe("IBuddyChatWidget functional flow", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("submits a message, calls the API, shows loading, and renders the answer", async () => {
    let resolveFetch: ((response: Response) => void) | null = null;
    const fetchMock = vi.fn(
      () =>
        new Promise<Response>((resolve) => {
          resolveFetch = resolve;
        })
    );

    globalThis.fetch = fetchMock as typeof globalThis.fetch;

    render(
      <IBuddyChatWidget
        baseUrl="http://localhost:8000"
        endpoint="/api/v1/chat"
        initialOpen
        theme="light"
        title="Ibuddy"
      />
    );

    fireEvent.change(screen.getByLabelText("Message input"), {
      target: { value: "Hello iBuddy" }
    });
    fireEvent.click(screen.getByLabelText("Send message"));

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    const firstCall = fetchMock.mock.calls[0];
    const requestUrl = firstCall?.[0];
    const requestInit = firstCall?.[1] as RequestInit | undefined;

    expect(requestUrl).toBe("http://localhost:8000/api/v1/chat");
    expect(requestInit).toMatchObject({
      method: "POST"
    });
    expect(JSON.parse(String(requestInit?.body))).toEqual({
      query: "Hello iBuddy",
      conversation_history: []
    });

    expect(screen.getByText("iBuddy is preparing a response")).toBeTruthy();

    expect(resolveFetch).toBeTypeOf("function");
    resolveFetch?.(createChatResponse("Hello from backend"));

    await waitFor(
      () => {
        expect(screen.getByText("Hello from backend")).toBeTruthy();
      },
      { timeout: 1500 }
    );
  });

  it("sends conversation history on the second API call", async () => {
    const fetchMock = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(createChatResponse("First reply"))
      .mockResolvedValueOnce(createChatResponse("Second reply"));

    globalThis.fetch = fetchMock as typeof globalThis.fetch;

    render(
      <IBuddyChatWidget
        baseUrl="http://localhost:8000"
        endpoint="/api/v1/chat"
        initialOpen
        theme="light"
      />
    );

    fireEvent.change(screen.getByLabelText("Message input"), {
      target: { value: "First question" }
    });
    fireEvent.click(screen.getByLabelText("Send message"));

    await waitFor(
      () => {
        expect(screen.getByText("First reply")).toBeTruthy();
      },
      { timeout: 1500 }
    );

    fireEvent.change(screen.getByLabelText("Message input"), {
      target: { value: "Second question" }
    });
    fireEvent.click(screen.getByLabelText("Send message"));

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(2);
    });

    const secondRequest = fetchMock.mock.calls[1]?.[1];
    expect(JSON.parse(String(secondRequest?.body))).toEqual({
      query: "Second question",
      conversation_history: [
        {
          role: "user",
          content: "First question"
        },
        {
          role: "assistant",
          content: "First reply"
        }
      ]
    });

    await waitFor(
      () => {
        expect(screen.getByText("Second reply")).toBeTruthy();
      },
      { timeout: 1500 }
    );
  });
});
