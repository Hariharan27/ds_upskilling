GOLDEN_DATASET_VERSION = "v1"

GOLDEN_DATASET = [
    {
        "id": "policy_wfh_limit",
        "question": "How many WFH days are allowed?",
        "expected_intent": "policy",
        "expected_behavior": "grounded_policy_answer",
    },
    {
        "id": "policy_leave_entitlement",
        "question": "How many leave days am I entitled to?",
        "expected_intent": "policy",
        "expected_behavior": "grounded_policy_answer",
    },
    {
        "id": "leave_balance",
        "question": "How many leave days do I have left?",
        "expected_intent": "leave",
        "expected_behavior": "employee_action",
    },
    {
        "id": "wfh_request",
        "question": "Can I work from home tomorrow?",
        "expected_intent": "wfh",
        "expected_behavior": "employee_action",
    },
    {
        "id": "attendance",
        "question": "Show me my attendance for this month.",
        "expected_intent": "attendance",
        "expected_behavior": "employee_action",
    },
    {
        "id": "it_ticket",
        "question": "Create an IT support ticket for my laptop.",
        "expected_intent": "ticket",
        "expected_behavior": "employee_action",
    },
    {
        "id": "unknown",
        "question": "What is the weather today?",
        "expected_intent": "unknown",
        "expected_behavior": "unsupported_request",
    },
]