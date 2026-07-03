import { IBuddyError } from "./base.js";

export class ValidationError extends IBuddyError {
  public constructor(message: string) {
    super(message, "VALIDATION_ERROR");
    this.name = "ValidationError";
  }
}
