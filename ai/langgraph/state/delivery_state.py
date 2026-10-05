from typing import Any, TypedDict


class DeliveryState(TypedDict, total=False):
    user_id: str
    session_id: str
    customer_message: str
    intent: str
    intent_confidence: float
    customer_id: str
    order_id: str | None
    order_data: dict[str, Any] | None
    delivery_data: dict[str, Any] | None
    plan: list[str]
    selected_agent: str
    tool_results: dict[str, Any]
    policy_evidence: list[dict[str, str]]
    proposed_resolution: dict[str, Any]
    critic_result: str
    validation_errors: list[str]
    escalated: bool
    final_response: str
    errors: list[str]
    workflow_status: list[str]