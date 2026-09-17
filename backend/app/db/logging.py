import uuid

from app.db.database import get_session
from app.db.models import RequestLog
from app.router.engine import RoutingResult


def log_request(conversation_id: str, prompt: str, result: RoutingResult) -> str:
    entry_id = str(uuid.uuid4())
    entry = RequestLog(
        id=entry_id,
        conversation_id=conversation_id,
        prompt=prompt,
        reply=result.reply_text,
        complexity_tier=result.complexity_tier,
        classifier_reason=result.classifier_reason,
        override_applied=result.override_applied,
        override_reason=result.override_reason,
        provider=result.provider,
        model_id=result.model_id,
        model_display_name=result.model_display_name,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
        cost_actual=result.cost_actual,
        cost_baseline=result.cost_baseline,
        cost_saved=result.cost_saved,
    )
    with get_session() as session:
        session.add(entry)
        session.commit()
    return entry_id
