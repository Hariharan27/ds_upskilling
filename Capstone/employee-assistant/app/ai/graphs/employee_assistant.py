from langgraph.graph import END, START, StateGraph

from app.ai.graphs.router import route_message
from app.ai.graphs.state import EmployeeAssistantState
from app.services.rag_service import answer_policy_question

def router_node(
    state: EmployeeAssistantState,
) -> dict:
    """Classify the employee message."""

    decision = route_message(state["message"])

    return {
        "intent": decision.intent,
    }


def route_by_intent(
    state: EmployeeAssistantState,
) -> str:
    """Return the graph route selected by the router."""

    return state["intent"]


def policy_node(
    state: EmployeeAssistantState,
) -> dict:
    """Answer a policy question using the existing RAG pipeline."""

    response = answer_policy_question(state["message"])

    return {
        "response": response.answer,
        "sources": response.sources,
    }


def build_employee_assistant_graph():
    graph = StateGraph(EmployeeAssistantState)

    graph.add_node("router", router_node)
    graph.add_node("policy", policy_node)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "policy": "policy",
            "attendance": END,
            "leave": END,
            "wfh": END,
            "ticket": END,
            "unknown": END,
        },
    )

    graph.add_edge("policy", END)

    return graph.compile()


employee_assistant_graph = build_employee_assistant_graph()