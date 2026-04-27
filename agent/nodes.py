"""Node functions for the StayEase LangGraph agent."""

from langchain_core.messages import AIMessage
from agent.state import AgentState
from agent.tools import (
    search_available_properties,
    get_listing_details,
    create_booking,
)

# Map tool names to tool functions
TOOL_MAP: dict = {
    "search_available_properties": search_available_properties,
    "get_listing_details": get_listing_details,
    "create_booking": create_booking,
}


def parse_input(state: AgentState) -> dict:
    """Extract intent from user message using simple rule-based logic."""

    # Get latest user message
    user_message = state["messages"][-1].content.lower()

    # Default values
    intent = "search"
    tool_name = "search_available_properties"
    tool_input = {}

    # --- BOOKING INTENT ---
    if "book" in user_message or "confirm booking" in user_message:
        intent = "book"
        tool_name = "create_booking"

        tool_input = {
            "listing_id": 1,  # placeholder for skeleton
            "guest_name": "Test User",
            "check_in": "2025-01-15",
            "check_out": "2025-01-17",
            "guests": 2,
        }

    # --- DETAILS INTENT ---
    elif "details" in user_message or "about" in user_message:
        intent = "details"
        tool_name = "get_listing_details"

        tool_input = {
            "listing_id": 1
        }

    # --- SEARCH INTENT (default) ---
    else:
        intent = "search"
        tool_name = "search_available_properties"

        tool_input = {
            "location": "Cox's Bazar",
            "check_in": "2025-01-15",
            "check_out": "2025-01-17",
            "guests": 2,
        }

    return {
        "intent": intent,
        "tool_name": tool_name,
        "tool_input": tool_input,
    }

def use_tool(state: AgentState) -> dict:
    """Call the selected tool with extracted parameters and store the result.

    Updates: tool_output.
    Next: respond.
    """
    tool_name: str = state["tool_name"]
    tool_input: dict = state["tool_input"]

    tool_fn = TOOL_MAP.get(tool_name)
    if tool_fn is None:
        return {"tool_output": {"error": f"Unknown tool: {tool_name}"}}

    result = tool_fn.invoke(tool_input)
    return {"tool_output": result}


def respond(state: AgentState) -> dict:
    """Use tool output and intent to generate a formatted response."""

    if state["intent"] == "search":
        content = f"Found these properties:\n{state['tool_output']}"

    elif state["intent"] == "details":
        content = f"Property details:\n{state['tool_output']}"

    elif state["intent"] == "book":
        content = f"Booking confirmed:\n{state['tool_output']}"

    else:
        content = str(state["tool_output"])

    reply = AIMessage(content=content)

    return {"messages": state["messages"] + [reply]}


def escalate(state: AgentState) -> dict:
    """Return a handoff message when the agent cannot handle the request.

    Updates: messages (appends escalation message).
    Next: END.
    """
    reply = AIMessage(
        content="I'm sorry, I can only help with searching properties, "
        "viewing listing details, and making bookings. "
        "Let me connect you with a human agent who can assist you further."
    )

    return {"messages": state["messages"] + [reply]}