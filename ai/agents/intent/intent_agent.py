import logging
from typing import Literal

from httpx import HTTPError
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field

from ai.llm.model_factory import get_chat_model
from ai.prompts.prompt_manager import load_prompt

logger = logging.getLogger(__name__)
try:
    from openai import APIError as OpenAIAPIError
except ImportError:
    OPENAI_ERRORS: tuple[type[BaseException], ...] = ()
else:
    OPENAI_ERRORS = (OpenAIAPIError,)

MODEL_ERRORS = (HTTPError, ImportError, OutputParserException, TimeoutError, ValueError) + OPENAI_ERRORS

Intent = Literal[
    "ORDER_STATUS",
    "LATE_DELIVERY",
    "DELIVERED_NOT_RECEIVED",
    "FAILED_DELIVERY",
    "DAMAGED_ITEM",
    "WRONG_ITEM",
    "MISSING_ITEM",
    "REFUND",
    "CANCELLATION",
    "REPLACEMENT",
    "ADDRESS_CHANGE",
    "DELIVERY_PARTNER",
    "GENERAL_POLICY",
    "HUMAN_ESCALATION",
]


class IntentClassification(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0, le=1)
    extracted_order_id: str | None = None
    extracted_entities: dict[str, str] = Field(default_factory=dict)
    urgency: Literal["low", "normal", "high"] = "normal"
    required_information: list[str] = Field(default_factory=list)


def classify_ambiguous_intent(message: str) -> IntentClassification | None:
    try:
        model = get_chat_model()
        if model is None:
            return None
        prompt = load_prompt("intent/classify.md")
        classifier = model.with_structured_output(IntentClassification)
        return classifier.invoke(prompt.format(customer_message=message))
    except MODEL_ERRORS as exc:
        logger.warning("intent_classification_fallback", extra={"error_type": type(exc).__name__})
        return None