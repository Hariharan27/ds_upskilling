from app.ai.graphs.route_decision import RouteDecision


# ---------------------------------------------------------
# Policy phrases
# ---------------------------------------------------------

LEAVE_POLICY_PHRASES = [
    "what is the leave policy",
    "what are the leave rules",
    "what are the leave guidelines",
    "how does the leave policy work",
    "what are the leave entitlements",
    "how many leaves am i entitled to",
    "how many leave days are allowed",
    "how many paid leaves are allowed",
    "what is the total leave entitlement",
    "what is my yearly leave entitlement",
    "how many days of paid leave do employees get",
    "how many casual leaves are allowed",
    "how many sick leaves are allowed",
    "how many earned leaves are allowed",
    "how many cl days are allowed",
    "how many sl days are allowed",
    "how many el days are allowed",
    "when are leaves credited",
    "how are leaves credited",
    "when do i get my leave credits",
    "how often are leaves credited",
    "can i carry forward leave",
    "can casual leave be carried forward",
    "can sick leave be carried forward",
    "can earned leave be carried forward",
    "can unused earned leave be carried over",
    "how much earned leave can be carried forward",
    "what happens to unused leave",
    "what happens to unused casual leave",
    "does unused leave expire",
    "does cl lapse",
    "does sl lapse",
    "what is the el accumulation limit",
    "what is the maximum el balance",
    "can i encash earned leave",
    "what is leave encashment",
    "how does leave encashment work",
    "how much el can be encashed",
    "when can i encash el",
    "who is eligible for el encashment",
    "how is el encashment calculated",
    "how is leave encashment paid",
    "what is the maternity leave policy",
    "how many maternity leave days are allowed",
    "what is the paternity leave policy",
    "how many paternity leave days are allowed",
    "what is the adoption leave policy",
    "what are the maternity leave eligibility rules",
    "what are the paternity leave eligibility rules",
    "how do i apply for leave",
    "what is the process to apply for leave",
    "where do i apply for leave",
    "what is the leave application process",
    "does leave need manager approval",
]


WFH_POLICY_PHRASES = [
    "what is the wfh policy",
    "what is the work from home policy",
    "what are the wfh rules",
    "what are the work from home rules",
    "how does the wfh policy work",
    "who is eligible for wfh",
    "who is eligible for work from home",
    "how many wfh days are allowed",
    "how many days can i work from home",
    "how many days of wfh are allowed",
    "how many work from home days are allowed",
    "how often can employees work remotely",
    "what is the monthly wfh allowance",
    "are there limits on working from home",
    "what is the mandatory wfh day",
    "how many mandatory wfh days are there",
    "can wfh be carried forward",
    "can work from home be carried forward",
    "what happens if i exceed wfh days",
    "what happens if i exceed the wfh limit",
    "what are the wfh eligibility criteria",
    "what are the wfh approval criteria",
    "what are the wfh requirements",
    "what are the wfh responsibilities",
    "what are the wfh security requirements",
]


IT_POLICY_PHRASES = [
    "what is the it policy",
    "what is the it asset policy",
    "what are the it asset rules",
    "what are the it asset guidelines",
    "what is the laptop policy",
    "what are the laptop security rules",
    "what should i do if my laptop is damaged",
    "what should i do if my laptop is broken",
    "what should i do if my laptop is lost",
    "what should i do if my laptop is stolen",
    "what happens if an it asset is damaged",
    "what happens if an it asset is lost",
    "what happens if an it asset is stolen",
    "what should i do with a damaged company laptop",
    "what are the rules for company it equipment",
    "how should i protect my laptop",
    "what are the laptop security best practices",
    "how do i return company assets",
]


CERTIFICATION_POLICY_PHRASES = [
    "what is the certification reimbursement policy",
    "what is the certification reimbursement process",
    "can certification fees be reimbursed",
    "who is eligible for certification reimbursement",
    "what are the certification reimbursement eligibility criteria",
    "how do i claim certification reimbursement",
    "how do i apply for certification reimbursement",
    "when should i claim certification reimbursement",
    "when can i claim certification reimbursement",
    "how long do i have to claim certification reimbursement",
    "what certifications are eligible for reimbursement",
    "are aws certifications reimbursed",
    "are azure certifications reimbursed",
    "are fundamental certifications reimbursed",
    "does the company reimburse certification fees",
    "does the company pay for professional certifications",
]


EMPLOYEE_BENEFITS_POLICY_PHRASES = [
    "what is the employee benefits policy",
    "what is the wedding gift policy",
    "what is the marriage gift policy",
    "what is the newborn gift policy",
    "what is the new born baby gift policy",
    "how much is the wedding gift",
    "how much is the marriage gift",
    "how much do we get for the marriage benefit",
    "how much is the newborn gift",
    "how much is the baby gift",
    "am i eligible for the wedding gift",
    "am i eligible for the marriage gift",
    "am i eligible for the newborn gift",
    "who is eligible for the wedding gift",
    "who is eligible for the newborn gift",
    "how do i claim the wedding gift",
    "how do i claim the newborn gift",
    "when will the wedding voucher be processed",
    "when will the newborn voucher be processed",
]


HOLIDAY_POLICY_PHRASES = [
    "what are the company holidays",
    "what is the holiday list",
    "show me the holiday list",
    "what are the holidays in 2026",
    "company holidays 2026",
    "company holiday list 2026",
    "what are the public holidays",
    "when is pongal",
    "when is republic day",
    "when is ramzan",
    "when is tamil new year",
    "when is may day",
    "when is independence day",
    "when is vinayakar chathurthi",
    "when is gandhi jayanthi",
    "when is ayudha poojai",
    "when is diwali",
    "when is christmas",
    "is diwali a holiday",
    "is pongal a holiday",
    "is christmas a holiday",
    "what is the next company holiday",
    "when is the next company holiday",
    "what is the upcoming holiday",
]


REWARDS_POLICY_PHRASES = [
    "what is the rewards and recognition policy",
    "what is the rnr policy",
    "what are docker points",
    "how do docker points work",
    "how are docker points allocated",
    "how do i earn docker points",
    "how can i get docker points",
    "can docker points be redeemed",
    "how do i redeem docker points",
    "how can i redeem my docker points",
    "where can i redeem docker points",
    "what can i redeem docker points for",
    "how much are docker points worth",
    "what are long service awards",
    "what is the long service award",
    "who is eligible for long service awards",
    "when do i get the long service award",
    "what is the reward for 3 years of service",
    "what is the reward for 5 years of service",
    "what is the reward for 10 years of service",
    "what is the reward for 15 years of service",
    "what are quarterly awards",
    "how do quarterly awards work",
]


STAFF_LOAN_POLICY_PHRASES = [
    "what is the staff loan policy",
    "what is the employee loan policy",
    "can i get a staff loan",
    "can employees get a staff loan",
    "am i eligible for a staff loan",
    "who is eligible for a staff loan",
    "what are the staff loan eligibility criteria",
    "how much staff loan can i get",
    "what is the maximum staff loan amount",
    "what is the maximum loan amount",
    "what is the loan repayment period",
    "how is the staff loan repaid",
    "how are loan emi deducted",
    "what is the staff loan interest rate",
    "can i take another staff loan",
    "when can i take another staff loan",
    "what is the loan cooling period",
    "what happens if i leave the company with a staff loan",
    "how do i apply for a staff loan",
    "what is the staff loan application process",
]


TEAM_OUTING_POLICY_PHRASES = [
    "what is the team outing policy",
    "what is the team outing reimbursement policy",
    "who is eligible for team outing reimbursement",
    "am i eligible for team outing reimbursement",
    "what is the team outing budget",
    "how much is the team outing budget",
    "what is the team outing budget per employee",
    "what is the budget for team outings",
    "when does the team outing budget expire",
    "what is the team outing budget cycle",
    "can the team outing budget be carried forward",
    "what expenses are covered under team outing",
    "what expenses are reimbursed for team outing",
    "are travel expenses covered in team outing",
    "are gifts covered under team outing",
    "are liquor expenses reimbursed",
    "are cigarette expenses reimbursed",
    "how do i apply for team outing reimbursement",
    "how do i claim team outing reimbursement",
    "what is the team outing reimbursement process",
]


# ---------------------------------------------------------
# Employee-specific / action phrases
# ---------------------------------------------------------

LEAVE_ACTION_PHRASES = [
    "apply leave",
    "apply for leave",
    "apply my leave",
    "submit leave",
    "submit a leave request",
    "create a leave request",
    "raise a leave request",
    "request leave",
    "request for leave",
    "book leave",
    "take leave today",
    "take leave tomorrow",
    "take leave on",
    "take leave from",
    "show my leave balance",
    "check my leave balance",
    "what is my leave balance",
    "how much leave do i have left",
    "how many leaves do i have left",
    "show me how much leave i have remaining",
    "show my leave history",
    "check my leave history",
    "what leave have i taken",
]


WFH_ACTION_PHRASES = [
    "apply wfh",
    "apply for wfh",
    "request wfh",
    "request work from home",
    "apply for work from home",
    "take wfh",
    "take work from home",
    "work from home tomorrow",
    "work from home today",
    "request wfh tomorrow",
    "apply wfh tomorrow",
    "can i take wfh tomorrow",
    "work remotely tomorrow",
]


TICKET_ACTION_PHRASES = [
    "raise an it ticket",
    "create an it ticket",
    "raise a ticket",
    "create a ticket",
    "raise an it support ticket",
    "create an it support ticket",
    "report an it issue",
    "report a laptop issue",
    "report a technical issue",
    "report a technical problem",
    "create an it support request",
]


def _matches(message: str, phrases: list[str]) -> bool:
    """Return True when a known high-confidence phrase is present."""
    return any(phrase in message for phrase in phrases)


def deterministic_route(message: str) -> RouteDecision | None:
    """
    Route only high-confidence messages without calling the router LLM.

    Returns:
        RouteDecision: when the intent is confidently known.
        None: when the router LLM should decide.
    """
    normalized = " ".join(message.strip().lower().split())
    normalized = normalized.replace("what's", "what is")

    # Policy first.
    # This prevents questions such as:
    # "How do I apply for leave?"
    # from being treated as an actual leave action.
    if _matches(normalized, LEAVE_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, WFH_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, IT_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, CERTIFICATION_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, EMPLOYEE_BENEFITS_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, HOLIDAY_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, REWARDS_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, STAFF_LOAN_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    if _matches(normalized, TEAM_OUTING_POLICY_PHRASES):
        return RouteDecision(intent="policy")

    # Employee-specific actions/checks.
    if _matches(normalized, LEAVE_ACTION_PHRASES):
        return RouteDecision(intent="leave")

    if _matches(normalized, WFH_ACTION_PHRASES):
        return RouteDecision(intent="wfh")

    if _matches(normalized, TICKET_ACTION_PHRASES):
        return RouteDecision(intent="ticket")

    # Not confident enough → let the LLM router decide.
    return None