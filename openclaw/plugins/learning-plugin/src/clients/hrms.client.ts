export class HrmsClient {
  async getLeaveBalance() {
    console.log("📡 HRMS Client Called");

    return {
      employeeId: "386",
      leaveBalance: 12,
      leaveType: "Casual Leave",
      source: "HRMS Client",
      message: "Leave balance fetched successfully."
    };
  }
}