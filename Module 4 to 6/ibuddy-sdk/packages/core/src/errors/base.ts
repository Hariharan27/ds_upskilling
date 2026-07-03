export class IBuddyError extends Error {
  public readonly code: string;
  public readonly cause?: unknown;

  public constructor(message: string, code = "IBUDDY_ERROR", cause?: unknown) {
    super(message);
    this.name = "IBuddyError";
    this.code = code;
    this.cause = cause;
  }
}
