# agent/graph.py
from langgraph.graph import StateGraph, END
from langchain.schema import BaseMessage
from typing import TypedDict, List, Union

from .nodes.classifier import classify_ticket
from .nodes.retriever import retrieve_context
from .nodes.drafter import generate_draft
from .nodes.reviewer import review_draft
from .nodes.escalation import log_escalation

RETRY_LIMIT = 2

class SupportState(TypedDict):
    subject: str
    description: str
    category: str
    context: List[str]
    draft: str
    review_result: str
    review_feedback: str
    attempt: int
    final_response: str

def finalize_response(state):
    return {**state, "final_response": state["draft"]}

def build_support_agent():
    builder = StateGraph(SupportState)

    # Add all nodes
    builder.add_node("classify", classify_ticket)
    builder.add_node("retrieve", retrieve_context)
    builder.add_node("draft", generate_draft)
    builder.add_node("review", review_draft)
    builder.add_node("escalate", log_escalation)
    builder.add_node("finalize", finalize_response)

    # Set entry point
    builder.set_entry_point("classify")

    # Add sequential edges
    builder.add_edge("classify", "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "review")

    # Define routing logic after review
    def route_after_review(state):
        current_attempt = state.get("attempt", 1)
        
        if state.get("review_result") == "approved":
            return "finalize"
        elif current_attempt >= RETRY_LIMIT:
            return "escalate"
        else:
            # Increment attempt counter and retry
            state["attempt"] = current_attempt + 1
            return "draft"

    # Add conditional edges with explicit mapping
    builder.add_conditional_edges(
        "review",
        route_after_review,
        ["finalize", "escalate", "draft"]
    )
    
    # Add terminal edges
    builder.add_edge("finalize", END)
    builder.add_edge("escalate", END)

    return builder.compile()

graph = build_support_agent()