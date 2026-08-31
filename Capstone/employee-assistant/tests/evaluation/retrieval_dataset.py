RETRIEVAL_DATASET = [
    # ------------------------------------------------------------------
    # Relevant queries — Leave Policy
    # ------------------------------------------------------------------
    {
        "query": "How many days of casual leave are available per year?",
        "expected_relevant": True,
    },
    {
        "query": "How many days of sick leave are available per year?",
        "expected_relevant": True,
    },
    {
        "query": "How many days of earned leave are credited each quarter?",
        "expected_relevant": True,
    },
    {
        "query": "Can unused earned leave be carried forward?",
        "expected_relevant": True,
    },
    {
        "query": "How many days of earned leave can be encashed?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — WFH Policy
    # ------------------------------------------------------------------
    {
        "query": "How many WFH days are allowed per month?",
        "expected_relevant": True,
    },
    {
        "query": "Who is eligible for work from home?",
        "expected_relevant": True,
    },
    {
        "query": "Can WFH days be carried forward to the next week?",
        "expected_relevant": True,
    },
    {
        "query": "What happens if I take more than the allowed WFH days?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — Holiday List
    # ------------------------------------------------------------------
    {
        "query": "How many holidays are there in 2026?",
        "expected_relevant": True,
    },
    {
        "query": "What is the date of Diwali in 2026?",
        "expected_relevant": True,
    },
    {
        "query": "When is Christmas in 2026?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — Certification Reimbursement
    # ------------------------------------------------------------------
    {
        "query": "Who is eligible for certification reimbursement?",
        "expected_relevant": True,
    },
    {
        "query": "How long should an employee have worked before claiming certification reimbursement?",
        "expected_relevant": True,
    },
    {
        "query": "How many days do I have to claim certification reimbursement?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — Employee Benefits
    # ------------------------------------------------------------------
    {
        "query": "How much is the wedding gift voucher?",
        "expected_relevant": True,
    },
    {
        "query": "How much is the newborn baby gift voucher?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — Staff Loan
    # ------------------------------------------------------------------
    {
        "query": "What is the maximum staff loan amount?",
        "expected_relevant": True,
    },
    {
        "query": "Who is eligible for a staff loan?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Relevant queries — Team Outing
    # ------------------------------------------------------------------
    {
        "query": "What is the team outing budget per employee?",
        "expected_relevant": True,
    },

    # ------------------------------------------------------------------
    # Irrelevant queries
    # ------------------------------------------------------------------
    {
        "query": "What is the company's stock price today?",
        "expected_relevant": False,
    },
    {
        "query": "What is the weather today?",
        "expected_relevant": False,
    },
    {
        "query": "Who won the cricket match yesterday?",
        "expected_relevant": False,
    },
    {
        "query": "What is the current price of Bitcoin?",
        "expected_relevant": False,
    },
    {
        "query": "Who is the Prime Minister of India?",
        "expected_relevant": False,
    },
    {
        "query": "What is the capital of France?",
        "expected_relevant": False,
    },
    {
        "query": "Give me a recipe for chicken biryani.",
        "expected_relevant": False,
    },
    {
        "query": "What are the latest technology news headlines?",
        "expected_relevant": False,
    },
    {
        "query": "How do I learn Python programming?",
        "expected_relevant": False,
    },
    {
        "query": "What is the population of Chennai?",
        "expected_relevant": False,
    },
]