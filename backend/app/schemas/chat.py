from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=80)


class EvidenceReference(BaseModel):
    source: str
    section: str
    excerpt: str


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    status: str
    response: str
    order: dict[str, str] | None = None
    delivery: dict[str, str] | None = None
    evidence: list[EvidenceReference] = Field(default_factory=list)
    workflow_status: list[str] = Field(default_factory=list)