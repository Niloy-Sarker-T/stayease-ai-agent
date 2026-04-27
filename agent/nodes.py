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
    """Use the LLM to extract intent and parameters from the latest user message.

    Updates: intent, tool_name, tool_input.
    Next: route (conditional edge).
    """
    # TODO: Call Groq LLM with a structured prompt that returns JSON like:
    # {
    #   "intent": "search",
    #   "tool_name": "search_available_properties",
    #   "tool_input": {"location": "Cox's Bazar", "check_in": "...", ...}
    # }
    #
    # Pseudocode:
    # llm = ChatGroq(model="llama3-70b-8192")
    # response = llm.invoke(system_prompt + state["messages"])
    # parsed = json.loads(response.content)

    parsed: dict = {
        "intent": "search",
        "tool_name": "search_available_properties",
        "tool_input": {
            "location": "Cox's Bazar",
            "check_in": "2025-01-15",
            "check_out": "2025-01-17",
            "guests": 2,
        },
    }

    return {
        "intent": parsed["intent"],
        "tool_name": parsed["tool_name"],
        "tool_input": parsed["tool_input"],
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
    """Use the LLM to format tool output into a friendly natural language reply.

    Updates: messages (appends AI response).
    Next: END.
    """
    # TODO: Call Groq LLM with tool_output and conversation context
    # to generate a human-friendly response.
    #
    # Pseudocode:
    # llm = ChatGroq(model="llama3-70b-8192")
    # prompt = f"Format this data as a helpful reply: {state['tool_output']}"
    # response = llm.invoke(state["messages"] + [HumanMessage(content=prompt)])

    reply = AIMessage(content=f"Here are the results: {state['tool_output']}")

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