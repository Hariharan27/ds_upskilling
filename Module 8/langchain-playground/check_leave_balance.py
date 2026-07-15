from langchain_core.tools import tool

@tool
def check_leave_balance(employee_id:str)-> str:
    """
    Get the remaining leave balance for an employee.

    Args:
        employee_id: Unique ID of the employee.
    """

    print(
        f"\n[TOOL EXECUTED] "
        f"Checking leave balance for {employee_id}"
    )

    return "The employee has 8 casual leaves remaining."
