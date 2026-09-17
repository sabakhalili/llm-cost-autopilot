import uuid

from fastapi import APIRouter

from app.db.logging import log_request
from app.models.schemas import ChatRequest, ChatResponse, RoutingMetadata
from app.router import route_and_execute

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    history = [{"role": m.role, "content": m.content} for m in request.history]

    result = await route_and_execute(request.message, history)
    log_request(request.conversation_id, request.message, result)

    return ChatResponse(
        id=str(uuid.uuid4()),
        reply=result.reply_text,
        routing=RoutingMetadata(
            complexity_tier=result.complexity_tier,
            classifier_reason=result.classifier_reason,
            override_applied=result.override_applied,
            override_reason=result.override_reason,
            reason=result.reason,
            provider=result.provider,
            model_id=result.model_id,
            model_display_name=result.model_display_name,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            latency_ms=result.latency_ms,
            cost_actual=result.cost_actual,
            cost_baseline=result.cost_baseline,
            cost_saved=result.cost_saved,
            baseline_model_display_name=result.baseline_model_display_name,
        ),
    )
