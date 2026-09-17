import json
import re

from app.config import settings
from app.router.model_config import CLASSIFIER_MODEL_ID, CLASSIFIER_PROVIDER
from app.router.providers.factory import get_provider

CLASSIFIER_PROMPT_TEMPLATE = """You are a prompt-complexity classifier for an LLM routing system.
Classify the user's prompt below into exactly one tier:

- "simple": factual lookups, definitions, short conversational replies, basic
  rewriting/formatting. A fast, cheap model can answer well.
- "medium": multi-step reasoning, synthesis/comparison, moderate analysis,
  bounded but non-trivial tasks.
- "hard": complex multi-step reasoning, code generation/debugging, long-form
  structured analysis, tasks with many interacting constraints.

Respond with ONLY a JSON object, no other text:
{{"tier": "simple" | "medium" | "hard", "reason": "<short phrase, under 12 words>"}}

User prompt to classify:
\"\"\"
{prompt}
\"\"\"
"""

_SIMPLE_KEYWORDS = ("what is", "what does", "define", "meaning of", "who is", "when did")
_MEDIUM_KEYWORDS = ("compare", "tradeoff", "trade-off", "pros and cons", "differences between")
_HARD_KEYWORDS = ("write a function", "write a python", "write code", "debug", "optimize this", "algorithm", "implement a")


def _mock_classify(prompt: str) -> tuple[str, str]:
    lowered = prompt.lower()
    word_count = len(prompt.split())

    if any(kw in lowered for kw in _HARD_KEYWORDS) or word_count > 55:
        return "hard", "long or code-generation request (mock heuristic)"
    if any(kw in lowered for kw in _SIMPLE_KEYWORDS) and word_count < 20:
        return "simple", "short factual lookup (mock heuristic)"
    if any(kw in lowered for kw in _MEDIUM_KEYWORDS) or word_count > 30:
        return "medium", "comparative or multi-step reasoning (mock heuristic)"
    return "simple" if word_count < 15 else "medium", "moderate-length request (mock heuristic)"


def _parse_classifier_output(text: str) -> tuple[str, str]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    payload = json.loads(match.group(0) if match else text)
    tier = payload["tier"]
    if tier not in ("simple", "medium", "hard"):
        raise ValueError(f"Unexpected tier from classifier: {tier!r}")
    return tier, payload.get("reason", "")


async def classify_complexity(prompt: str) -> tuple[str, str]:
    """Returns (tier, reason)."""
    if settings.mock_mode:
        return _mock_classify(prompt)

    provider = get_provider(CLASSIFIER_PROVIDER)
    response = await provider.call_model(
        CLASSIFIER_PROMPT_TEMPLATE.format(prompt=prompt), CLASSIFIER_MODEL_ID
    )
    return _parse_classifier_output(response.text)
