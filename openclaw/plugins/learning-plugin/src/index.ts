import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";
import { LeaveService } from "./services/leave.service.js";

const leaveService = new LeaveService();

export default defineToolPlugin({
  id: "learning-plugin",
  name: "Learning Plugin",
  description: "Add Learning Plugin tools to OpenClaw.",
  tools: (tool) => [
    tool({
      name: "echo",
      description: "Echo input text.",
      parameters: Type.Object({
        input: Type.String({ description: "Text to echo." }),
      }),
      execute: async ({ input }) => {
        console.log("Echo Tool Invoked:", input);

        return await leaveService.getLeaveBalance();
      },
    }),
  ],
});
