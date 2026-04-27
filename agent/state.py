"""State definition for the StayEase AI agent."""

from typing import TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State object passed between nodes in the LangGraph agent.

    Fields:
        messages: Full conversation history for LLM context.
        intent: Parsed user intent — one of search, details, book, escalate.
        tool_name: Name of the tool to invoke.
        tool_input: Parameters for the selected tool.
        tool_output: Result returned from the tool call.
        conversation_id: Links this run to a persisted conversation.
    """

    messages: list[BaseMessage]
    intent: str
    tool_name: str
    tool_input: dict
    tool_output: dict
    conversation_id: str