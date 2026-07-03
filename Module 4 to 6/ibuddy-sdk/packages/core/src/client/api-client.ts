import type { IBuddyHeaders } from "../config/index.js";
import { APIError, NetworkError, TimeoutError } from "../errors/index.js";
import type { RequestOptions } from "../models/internal.js";
import { joinUrl } from "../utils/index.js";

export class APIClient {
  private headers: IBuddyHeaders;

  public constructor(
    private readonly options: {
      baseUrl: string;
      endpoint: string;
      headers?: IBuddyHeaders;
      timeout: number;
      fetch: typeof globalThis.fetch;
    }
  ) {
    this.headers = { ...(options.headers ?? {}) };
  }

  public setHeaders(headers: IBuddyHeaders): void {
    this.headers = {
      ...this.headers,
      ...headers
    };
  }

  public getHeaders(): IBuddyHeaders {
    return { ...this.headers };
  }

  public async post<TResponse>(body: unknown, options?: RequestOptions): Promise<TResponse> {
    const controller = new AbortController();
    const timeout = options?.timeout ?? this.options.timeout;
    const signal = options?.signal ?? controller.signal;
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const url = joinUrl(this.options.baseUrl, this.options.endpoint);
    console.debug("[IBuddy] POST", url, { headers: { "Content-Type": "application/json", ...this.headers }, timeout });

    try {
      const response = await this.options.fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...this.headers,
          ...(options?.headers ?? {})
        },
        body: JSON.stringify(body),
        signal
      });

      console.debug("[IBuddy] Response", response.status, response.statusText, Object.fromEntries(response.headers.entries()));

      const responseBody = await this.parseResponseBody(response);

      console.debug("[IBuddy] Response body:", JSON.stringify(responseBody, null, 2));

      if (!response.ok) {
        throw new APIError(
          `Request failed with status ${response.status}.`,
          response.status,
          response.statusText,
          responseBody
        );
      }

      return responseBody as TResponse;
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }

      if (error instanceof Error && error.name === "AbortError") {
        throw new TimeoutError();
      }

      console.error("[IBuddy] fetch threw:", error);
      throw new NetworkError("Unable to complete the request.", error);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async parseResponseBody(response: Response): Promise<unknown> {
    const contentType = response.headers.get("content-type");

    if (contentType?.includes("application/json")) {
      return response.json();
    }

    const text = await response.text();

    if (text.length === 0) {
      return null;
    }

    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }
}
