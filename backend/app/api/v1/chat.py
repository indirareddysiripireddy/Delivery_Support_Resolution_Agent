from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ai.langgraph.workflows.delivery_workflow import run_delivery_workflow
from backend.app.core.config import get_settings
from backend.app.core.security import require_demo_identity
from backend.app.schemas.chat import ChatRequest, ChatResponse, EvidenceReference

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    customer_id: Annotated[str, Depends(require_demo_identity)],
) -> ChatResponse:
    if len(request.message) > get_settings().max_message_length:
        raise HTTPException(status_code=422, detail="Message exceeds configured size limit")
    state = run_delivery_workflow(request.message, customer_id, request.session_id)
    delivery = state.get("delivery_data")
    order = state.get("order_data")
    return ChatResponse(
        session_id=state["session_id"],
        intent=state.get("intent", "UNCLASSIFIED"),
        status=state.get("proposed_resolution", {}).get("status", "escalated"),
        response=state.get("final_response", "A support specialist can help with this request."),
        order={key: str(order[key]) for key in ("order_id", "item_summary", "status", "total", "currency")} if order else None,
        delivery={key: str(delivery[key]) for key in ("status", "delivered_at", "carrier", "tracking_id")} if delivery else None,
        evidence=[EvidenceReference(**item) for item in state.get("policy_evidence", [])],
        workflow_status=state.get("workflow_status", []),
    )