"""LangGraph graph construction for the StayEase AI agent."""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import parse_input, use_tool, respond, escalate


def route_by_intent(state: AgentState) -> str:
    """Route to the next node based on the parsed intent.

    Returns:
        'use_tool' for search, details, or book intents.
        'escalate' for anything else.
    """
    intent: str = state.get("intent", "")

    if intent in ("search", "details", "book"):
        return "use_tool"
    return "escalate"


def build_graph() -> StateGraph:
    """Construct and compile the StayEase agent graph.

    Graph structure:
        parse_input -> route (conditional)
            -> use_tool -> respond -> END
            -> escalate -> END
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("parse_input", parse_input)
    graph.add_node("use_tool", use_tool)
    graph.add_node("respond", respond)
    graph.add_node("escalate", escalate)

    # Set entry point
    graph.set_entry_point("parse_input")

    # Add conditional edge from parse_input based on intent
    graph.add_conditional_edges(
        "parse_input",
        route_by_intent,
        {
            "use_tool": "use_tool",
            "escalate": "escalate",
        },
    )

    # Linear edges
    graph.add_edge("use_tool", "respond")
    graph.add_edge("respond", END)
    graph.add_edge("escalate", END)

    return graph.compile()


# Compiled agent — ready to invoke
agent = build_graph()