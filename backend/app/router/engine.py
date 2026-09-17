from dataclasses import dataclass

from app.router.classifier import classify_complexity
from app.router.model_config import MODELS, baseline_display_name, baseline_model_id
from app.router.pricing import calculate_cost
from app.router.providers.base import ModelResponse
from app.router.providers.factory import get_provider
from app.router.rules import apply_overrides


@dataclass
class RoutingResult:
    reply_text: str
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


def _build_reason(classifier_reason: str, override_applied: bool, override_reason: str | None, model_display_name: str) -> str:
    reason = f"Routed to {model_display_name} — classified as {classifier_reason}"
    if override_applied and override_reason:
        reason += f"; bumped tier — {override_reason}"
    return reason


async def route_and_execute(prompt: str, history: list[dict] | None = None) -> RoutingResult:
    """Public entry point for the routing engine.

    Pure async Python with no FastAPI or database dependency — callable
    standalone from any future client (CLI, another app) that wants to
    reuse the routing logic as middleware.

    Future extension point: sample a % of requests, fire a parallel call to
    a higher tier, and score both with an LLM judge (shadow-check
    validation). Deferred for v1 — see README "Future Work".
    """
    classifier_tier, classifier_reason = await classify_complexity(prompt)
    final_tier, override_applied, override_reason = apply_overrides(prompt, classifier_tier)

    model_cfg = MODELS[final_tier]
    model_response: ModelResponse = await get_provider(model_cfg["provider"]).call_model(
        prompt, model_cfg["model_id"], history
    )

    cost_actual = calculate_cost(
        model_cfg["model_id"], model_response.input_tokens, model_response.output_tokens
    )
    cost_baseline = calculate_cost(
        baseline_model_id(), model_response.input_tokens, model_response.output_tokens
    )

    reason = _build_reason(classifier_reason, override_applied, override_reason, model_cfg["display_name"])

    return RoutingResult(
        reply_text=model_response.text,
        complexity_tier=final_tier,
        classifier_reason=classifier_reason,
        override_applied=override_applied,
        override_reason=override_reason,
        reason=reason,
        provider=model_cfg["provider"],
        model_id=model_cfg["model_id"],
        model_display_name=model_cfg["display_name"],
        input_tokens=model_response.input_tokens,
        output_tokens=model_response.output_tokens,
        latency_ms=model_response.latency_ms,
        cost_actual=cost_actual,
        cost_baseline=cost_baseline,
        cost_saved=cost_baseline - cost_actual,
        baseline_model_display_name=baseline_display_name(),
    )
