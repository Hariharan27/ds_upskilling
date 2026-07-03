import { IBuddyError } from "./base.js";

export class APIError extends IBuddyError {
  public readonly status: number;
  public readonly statusText: string;
  public readonly responseBody?: unknown;

  public constructor(
    message: string,
    status: number,
    statusText: string,
    responseBody?: unknown
  ) {
    super(message, "API_ERROR");
    this.name = "APIError";
    this.status = status;
    this.statusText = statusText;
    this.responseBody = responseBody;
  }
}
