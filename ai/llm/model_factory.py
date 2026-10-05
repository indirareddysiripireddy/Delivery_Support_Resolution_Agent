from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from backend.app.core.config import get_settings

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI


@lru_cache
def get_chat_model() -> ChatOpenAI | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
        timeout=12,
        max_retries=1,
    )