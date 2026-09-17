import time

from openai import AsyncOpenAI

from app.config import settings
from app.router.providers.base import ModelResponse

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


class OpenAIProvider:
    async def call_model(
        self, prompt: str, model_id: str, history: list[dict] | None = None
    ) -> ModelResponse:
        messages = list(history or []) + [{"role": "user", "content": prompt}]

        start = time.perf_counter()
        response = await _get_client().chat.completions.create(
            model=model_id, messages=messages
        )
        latency_ms = (time.perf_counter() - start) * 1000

        return ModelResponse(
            text=response.choices[0].message.content or "",
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            latency_ms=latency_ms,
        )
