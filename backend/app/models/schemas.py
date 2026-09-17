from pydantic import BaseModel


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    history: list[HistoryMessage] = []


class RoutingMetadata(BaseModel):
    complexity_tier: str
    classifier_reason: str
    override_applied: bool
    override_reason: str | None
    reason: str
    provider: str
    model_id: str
    model_display_name: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_actual: float
    cost_baseline: float
    cost_saved: float
    baseline_model_display_name: str


class ChatResponse(BaseModel):
    id: str
    reply: str
    routing: RoutingMetadata


class TierCounts(BaseModel):
    simple: int = 0
    medium: int = 0
    hard: int = 0


class StatsSummary(BaseModel):
    total_requests: int
    total_cost_actual: float
    total_cost_baseline: float
    total_saved: float
    by_tier: TierCounts
