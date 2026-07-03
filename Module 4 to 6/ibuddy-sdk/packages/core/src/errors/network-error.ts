import { IBuddyError } from "./base.js";

export class NetworkError extends IBuddyError {
  public constructor(message: string, cause?: unknown) {
    super(message, "NETWORK_ERROR", cause);
    this.name = "NetworkError";
  }
}
