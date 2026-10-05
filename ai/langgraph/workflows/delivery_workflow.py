import re
from pathlib import Path
from typing import Any
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from ai.agents.intent.intent_agent import classify_ambiguous_intent
from ai.langgraph.state.delivery_state import DeliveryState
from ai.tools.support_tools import get_delivery_status, get_order

PROJECT_ROOT = Path(__file__).resolve().parents[3]
POLICY_ROOT = PROJECT_ROOT / "knowledge_base"
ORDER_PATTERN = re.compile(r"\b(?:DS-\d{4}|#\d{5,})\b", re.IGNORECASE)


def input_guardrail(state: DeliveryState) -> dict[str, Any]:
    message = state.get("customer_message", "").strip()
    if not message or len(message) > 4000:
        return {"errors": ["Message must contain 1 to 4000 characters."], "escalated": True}
    if re.search(r"ignore (?:all )?(?:previous|prior) instructions|reveal (?:the )?(?:system prompt|secrets)", message, re.IGNORECASE):
        return {
            "errors": ["The request could not be safely processed."],
            "escalated": True,
            "workflow_status": ["Reviewing request safety"],
        }
    return {"workflow_status": ["Understanding request"]}


def classify_intent(state: DeliveryState) -> dict[str, Any]:
    message = state["customer_message"].lower()
    order_match = ORDER_PATTERN.search(state["customer_message"])
    if any(word in message for word in ("human", "representative", "agent please")):
        intent = "HUMAN_ESCALATION"
    elif "didn't receive" in message or "did not receive" in message or "not received" in message:
        intent = "DELIVERED_NOT_RECEIVED"
    elif "damaged" in message or "broken" in message:
        intent = "DAMAGED_ITEM"
    elif "late" in message or "delayed" in message:
        intent = "LATE_DELIVERY"
    elif "refund" in message:
        intent = "REFUND"
    elif "cancel" in message:
        intent = "CANCELLATION"
    elif "replace" in message or "replacement" in message:
        intent = "REPLACEMENT"
    elif "track" in message or "where is" in message or "status" in message:
        intent = "ORDER_STATUS"
    else:
        intent = "GENERAL_POLICY"
    confidence = 0.92 if intent != "GENERAL_POLICY" else 0.65
    if confidence < 0.8:
        model_result = classify_ambiguous_intent(state["customer_message"])
        if model_result is not None:
            intent = model_result.intent
            confidence = model_result.confidence
            order_id = model_result.extracted_order_id or (order_match.group(0).lstrip("#").upper() if order_match else None)
        else:
            order_id = order_match.group(0).lstrip("#").upper() if order_match else None
    else:
        order_id = order_match.group(0).lstrip("#").upper() if order_match else None
    return {
        "intent": intent,
        "intent_confidence": confidence,
        "order_id": order_id,
        "workflow_status": ["Understanding request", "Checking order"],
    }


def supervise(state: DeliveryState) -> dict[str, Any]:
    return {"workflow_status": [*state.get("workflow_status", []), "Planning support steps"]}


def plan(state: DeliveryState) -> dict[str, Any]:
    steps = ["Verify order ownership", "Check delivery information", "Review applicable policy", "Validate response"]
    if state.get("intent") == "HUMAN_ESCALATION":
        steps = ["Route request to human support"]
    return {"plan": steps}


def route(state: DeliveryState) -> dict[str, Any]:
    intent = state.get("intent", "GENERAL_POLICY")
    if intent in {"LATE_DELIVERY", "DELIVERED_NOT_RECEIVED", "ORDER_STATUS"}:
        agent = "delivery"
    elif intent in {"DAMAGED_ITEM", "REFUND", "CANCELLATION", "REPLACEMENT"}:
        agent = "resolution_support"
    elif intent == "HUMAN_ESCALATION":
        agent = "human_support"
    else:
        agent = "policy_support"
    return {"selected_agent": agent}


def run_specialist(state: DeliveryState) -> dict[str, Any]:
    if state.get("selected_agent") == "human_support":
        return {"escalated": True, "workflow_status": [*state.get("workflow_status", []), "Preparing human handoff"]}
    order_id = state.get("order_id")
    if not order_id:
        return {
            "errors": ["An order number is needed to check a specific delivery."],
            "workflow_status": [*state.get("workflow_status", []), "Waiting for order number"],
        }
    order = get_order.invoke({"order_id": order_id, "customer_id": state["customer_id"]})
    delivery = get_delivery_status.invoke({"order_id": order_id, "customer_id": state["customer_id"]})
    if not order or not delivery:
        return {
            "errors": ["No matching order was found for this customer."],
            "workflow_status": [*state.get("workflow_status", []), "Order could not be verified"],
        }
    return {
        "order_data": order,
        "delivery_data": delivery,
        "tool_results": {"get_order": "success", "get_delivery_status": "success"},
        "workflow_status": [*state.get("workflow_status", []), "Checking delivery status"],
    }


def retrieve_policy(state: DeliveryState) -> dict[str, Any]:
    intent = state.get("intent", "GENERAL_POLICY")
    if intent == "DELIVERED_NOT_RECEIVED":
        policy_path = POLICY_ROOT / "delivery_policies" / "delivered_not_received.md"
    elif intent in {"LATE_DELIVERY", "ORDER_STATUS"}:
        policy_path = POLICY_ROOT / "delivery_policies" / "delivery_tracking.md"
    elif intent in {"REFUND", "DAMAGED_ITEM"}:
        policy_path = POLICY_ROOT / "damaged_item_policies" / "damage_claims.md"
    else:
        policy_path = POLICY_ROOT / "faq" / "support_basics.md"
    if not policy_path.is_file():
        return {"policy_evidence": [], "errors": ["INSUFFICIENT_EVIDENCE"]}
    text = policy_path.read_text(encoding="utf-8").strip()
    title = text.splitlines()[0].removeprefix("# ")
    excerpt = " ".join(line.strip() for line in text.splitlines()[1:] if line.strip() and not line.startswith("#"))
    return {
        "policy_evidence": [{"source": policy_path.name, "section": title, "excerpt": excerpt}],
        "workflow_status": [*state.get("workflow_status", []), "Reviewing support policy"],
    }


def propose_resolution(state: DeliveryState) -> dict[str, Any]:
    order = state.get("order_data")
    delivery = state.get("delivery_data")
    evidence = state.get("policy_evidence", [])
    if state.get("escalated"):
        proposed = {"status": "escalated", "action": "human_handoff", "evidence_sources": []}
    elif state.get("errors"):
        proposed = {"status": "needs_information", "action": "request_information", "evidence_sources": []}
    elif not order or not delivery or not evidence:
        proposed = {"status": "escalated", "action": "human_handoff", "evidence_sources": []}
    elif state.get("intent") == "DELIVERED_NOT_RECEIVED":
        proposed = {
            "status": "guidance_provided",
            "action": "check_delivery_location_then_contact_support_if_unresolved",
            "evidence_sources": [evidence[0]["source"]],
        }
    elif state.get("intent") in {"LATE_DELIVERY", "ORDER_STATUS"}:
        proposed = {
            "status": "tracking_shared",
            "action": "share_verified_tracking",
            "evidence_sources": [evidence[0]["source"]],
        }
    else:
        proposed = {
            "status": "human_review_required",
            "action": "escalate_for_eligibility_review",
            "evidence_sources": [evidence[0]["source"]],
        }
    return {"proposed_resolution": proposed, "workflow_status": [*state.get("workflow_status", []), "Validating resolution"]}


def critic(state: DeliveryState) -> dict[str, Any]:
    proposal = state.get("proposed_resolution", {})
    has_basis = bool(state.get("errors") or state.get("escalated") or (
        state.get("order_data") and state.get("delivery_data") and state.get("policy_evidence")
    ))
    return {"critic_result": "supported" if proposal and has_basis else "unsupported"}


def validate(state: DeliveryState) -> dict[str, Any]:
    errors: list[str] = []
    proposal = state.get("proposed_resolution", {})
    if not proposal.get("status") or not proposal.get("action"):
        errors.append("Resolution is missing required fields.")
    if proposal.get("action") in {"approve_refund", "cancel_order", "create_replacement"}:
        errors.append("This workflow is not authorized to perform transactional actions.")
    if proposal.get("evidence_sources") and not state.get("policy_evidence"):
        errors.append("Resolution cites unavailable policy evidence.")
    if state.get("critic_result") != "supported":
        errors.append("Resolution lacks sufficient supporting evidence.")
    return {"validation_errors": errors}


def replan(state: DeliveryState) -> dict[str, Any]:
    return {
        "escalated": True,
        "proposed_resolution": {
            "status": "escalated",
            "action": "human_handoff",
            "evidence_sources": [],
        },
        "validation_errors": [],
        "workflow_status": [*state.get("workflow_status", []), "Escalating for human review"],
    }


def respond(state: DeliveryState) -> dict[str, Any]:
    if state.get("validation_errors"):
        response = "I couldn't safely confirm a resolution, so I've prepared this for support review."
    elif state.get("escalated"):
        response = "I'll route this to a support specialist for follow-up."
    elif state.get("errors"):
        if "No matching order was found" in state["errors"][0]:
            response = "I couldn't match that order to your account. Please check the order number or contact support."
        else:
            response = "Please share your order number so I can check the delivery against your account."
    elif state.get("delivery_data"):
        delivery = state["delivery_data"]
        evidence = state.get("policy_evidence", [{}])[0]
        if delivery.get("status") == "delivered":
            response = (
                f"Order {state['order_id']} is marked delivered by {delivery.get('carrier')} at "
                f"{delivery.get('delivered_at')}. {evidence.get('excerpt', '')}"
            )
        else:
            response = (
                f"Order {state['order_id']} is currently {delivery.get('status')} with "
                f"{delivery.get('carrier')}. Tracking reference: {delivery.get('tracking_id')}."
            )
    else:
        response = "I couldn't find enough verified information to answer that. A support specialist can help."
    return {"final_response": response, "workflow_status": [*state.get("workflow_status", []), "Preparing customer response"]}


def _next_after_input(state: DeliveryState) -> str:
    return "respond" if state.get("escalated") else "intent"


def _next_after_validation(state: DeliveryState) -> str:
    return "replan" if state.get("validation_errors") else "respond"


def build_delivery_workflow():
    graph = StateGraph(DeliveryState)
    graph.add_node("input_guardrail", input_guardrail)
    graph.add_node("intent", classify_intent)
    graph.add_node("supervisor", supervise)
    graph.add_node("planner", plan)
    graph.add_node("router", route)
    graph.add_node("specialist", run_specialist)
    graph.add_node("policy", retrieve_policy)
    graph.add_node("resolution", propose_resolution)
    graph.add_node("critic", critic)
    graph.add_node("validator", validate)
    graph.add_node("replan", replan)
    graph.add_node("respond", respond)
    graph.add_edge(START, "input_guardrail")
    graph.add_conditional_edges("input_guardrail", _next_after_input, {"intent": "intent", "respond": "respond"})
    graph.add_edge("intent", "supervisor")
    graph.add_edge("supervisor", "planner")
    graph.add_edge("planner", "router")
    graph.add_edge("router", "specialist")
    graph.add_edge("specialist", "policy")
    graph.add_edge("policy", "resolution")
    graph.add_edge("resolution", "critic")
    graph.add_edge("critic", "validator")
    graph.add_conditional_edges("validator", _next_after_validation, {"replan": "replan", "respond": "respond"})
    graph.add_edge("replan", "respond")
    graph.add_edge("respond", END)
    return graph.compile()


delivery_workflow = build_delivery_workflow()


def run_delivery_workflow(message: str, customer_id: str, session_id: str | None = None) -> DeliveryState:
    return delivery_workflow.invoke({
        "customer_message": message,
        "customer_id": customer_id,
        "user_id": customer_id,
        "session_id": session_id or str(uuid4()),
        "errors": [],
        "validation_errors": [],
        "workflow_status": [],
    })