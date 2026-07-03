import { IBuddyError } from "./base.js";

export class ConfigurationError extends IBuddyError {
  public constructor(message: string) {
    super(message, "CONFIGURATION_ERROR");
    this.name = "ConfigurationError";
  }
}
