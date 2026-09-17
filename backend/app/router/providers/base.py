from dataclasses import dataclass
from typing import Protocol


@dataclass
class ModelResponse:
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: float


class ModelProvider(Protocol):
    async def call_model(
        self, prompt: str, model_id: str, history: list[dict] | None = None
    ) -> ModelResponse: ...
