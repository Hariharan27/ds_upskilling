ROUTING_EVALUATION_DATASET = [
    # -------------------------
    # Leave policy
    # -------------------------
    ("What is the leave policy?", "policy"),
    ("How many leave days are allowed?", "policy"),
    ("How many casual leaves are allowed?", "policy"),
    ("Can earned leave be carried forward?", "policy"),
    ("How does leave encashment work?", "policy"),
    ("How do I apply for leave?", "policy"),

    # Leave action / employee-specific
    ("Apply leave tomorrow", "leave"),
    ("Apply for leave next Monday", "leave"),
    ("Show my leave balance", "leave"),
    ("How much leave do I have left?", "leave"),
    ("Show my leave history", "leave"),

    # -------------------------
    # WFH policy
    # -------------------------
    ("What is the WFH policy?", "policy"),
    ("How many WFH days are allowed?", "policy"),
    ("Who is eligible for work from home?", "policy"),
    ("Can WFH be carried forward?", "policy"),

    # WFH action
    ("Apply WFH tomorrow", "wfh"),
    ("Request work from home tomorrow", "wfh"),
    ("Take WFH tomorrow", "wfh"),

    # -------------------------
    # IT policy
    # -------------------------
    ("What is the IT asset policy?", "policy"),
    ("What should I do if my laptop is damaged?", "policy"),
    ("What should I do if my laptop is stolen?", "policy"),
    ("What are the laptop security rules?", "policy"),

    # Ticket
    ("Raise an IT ticket", "ticket"),
    ("Create a ticket", "ticket"),
    ("Report a laptop issue", "ticket"),

    # -------------------------
    # Other policies
    # -------------------------
    ("What is the certification reimbursement policy?", "policy"),
    ("Can certification fees be reimbursed?", "policy"),

    ("What is the wedding gift policy?", "policy"),
    ("How much is the newborn gift?", "policy"),

    ("What is the holiday list?", "policy"),
    ("What is the upcoming holiday?", "policy"),

    ("What are Docker Points?", "policy"),
    ("What is the long service award?", "policy"),

    ("What is the staff loan policy?", "policy"),
    ("How much staff loan can I get?", "policy"),

    ("What is the team outing policy?", "policy"),
    ("How much is the team outing budget?", "policy"),

    # -------------------------
    # Ambiguous → should fall back
    # -------------------------
    ("Can I take leave?", None),
    ("Can I work from home?", None),
    ("I need some leave", None),
    ("I have an issue with my laptop", None),
]