from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class RequestLog(SQLModel, table=True):
    id: str = Field(primary_key=True)
    conversation_id: str
    prompt: str
    reply: str

    complexity_tier: str
    classifier_reason: str
    override_applied: bool
    override_reason: str | None

    provider: str
    model_id: str
    model_display_name: str

    input_tokens: int
    output_tokens: int
    latency_ms: float

    cost_actual: float
    cost_baseline: float
    cost_saved: float

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
