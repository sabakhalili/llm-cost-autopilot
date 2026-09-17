import time

from anthropic import AsyncAnthropic

from app.config import settings
from app.router.providers.base import ModelResponse

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


class AnthropicProvider:
    async def call_model(
        self, prompt: str, model_id: str, history: list[dict] | None = None
    ) -> ModelResponse:
        messages = list(history or []) + [{"role": "user", "content": prompt}]

        start = time.perf_counter()
        response = await _get_client().messages.create(
            model=model_id, max_tokens=1024, messages=messages
        )
        latency_ms = (time.perf_counter() - start) * 1000

        text = "".join(block.text for block in response.content if block.type == "text")

        return ModelResponse(
            text=text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency_ms,
        )
