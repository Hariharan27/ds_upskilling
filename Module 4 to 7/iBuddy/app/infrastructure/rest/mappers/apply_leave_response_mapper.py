class ApplyLeaveResponseMapper:
    """
    Maps the HRMS Apply Leave API response
    into business context for response generation.
    """

    def map(
        self,
        response: dict,
    ) -> str:

        entity = response.get(
            "entity",
            {},
        )

        return (
            "Leave request submitted successfully.\n"
            f"Request ID: {entity.get('id')}\n"
            f"Approval Status: {entity.get('approvalStatus')}"
        )