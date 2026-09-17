import asyncio
import random
import time

from app.router.model_config import MODELS
from app.router.providers.base import ModelResponse

# Tier-correlated latency/output ranges so harder tiers visibly take longer
# and say more in a live demo, without needing real API calls.
_TIER_LATENCY_MS = {"simple": (150, 400), "medium": (400, 900), "hard": (900, 2200)}
_TIER_OUTPUT_MULTIPLIER = {"simple": (0.8, 1.5), "medium": (1.5, 3.0), "hard": (3.0, 6.0)}

_MODEL_ID_TO_TIER = {cfg["model_id"]: tier for tier, cfg in MODELS.items()}


class MockProvider:
    async def call_model(
        self, prompt: str, model_id: str, history: list[dict] | None = None
    ) -> ModelResponse:
        tier = _MODEL_ID_TO_TIER.get(model_id, "simple")

        latency_low, latency_high = _TIER_LATENCY_MS[tier]
        latency_ms = random.uniform(latency_low, latency_high)

        start = time.perf_counter()
        await asyncio.sleep(latency_ms / 1000)
        actual_latency_ms = (time.perf_counter() - start) * 1000

        input_tokens = max(1, round(len(prompt.split()) * 1.3))

        mult_low, mult_high = _TIER_OUTPUT_MULTIPLIER[tier]
        output_tokens = max(10, round(input_tokens * random.uniform(mult_low, mult_high)))

        snippet = prompt.strip().splitlines()[0][:80]
        text = (
            f"[mock {tier} response] Here's my take on: \"{snippet}\" — "
            f"this is a simulated reply so the demo runs without live API keys."
        )

        return ModelResponse(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=actual_latency_ms,
        )
