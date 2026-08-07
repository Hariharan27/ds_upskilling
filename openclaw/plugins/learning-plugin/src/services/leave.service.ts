import { HrmsClient } from "../clients/hrms.client.js";

const hrmsClient = new HrmsClient();

export class LeaveService {
  async getLeaveBalance() {
    console.log("📦 LeaveService Called");

    return await hrmsClient.getLeaveBalance();
  }
}