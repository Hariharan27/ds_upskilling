import { IBuddyError } from "./base.js";

export class TimeoutError extends IBuddyError {
  public constructor(message = "The request timed out.") {
    super(message, "TIMEOUT_ERROR");
    this.name = "TimeoutError";
  }
}
