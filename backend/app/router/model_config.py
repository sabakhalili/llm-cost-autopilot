# Tier -> model mapping. Deliberately spans both providers so the routing
# abstraction is demonstrably provider-agnostic, not just provider-capable.
MODELS = {
    "simple": {
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "display_name": "GPT-4o mini",
    },
    "medium": {
        "provider": "anthropic",
        "model_id": "claude-haiku-4-5-20251001",
        "display_name": "Claude Haiku 4.5",
    },
    "hard": {
        "provider": "openai",
        "model_id": "gpt-4o",
        "display_name": "GPT-4o",
    },
}

# Cost-vs-baseline is always computed against this tier's model, i.e. "what
# would this call have cost if we always used the flagship model".
BASELINE_TIER = "hard"

# The classifier always runs on a fixed cheap/fast model, independent of
# which provider ends up serving the actual request — keeps the routing
# decision itself cheap while the router is free to pick the best provider
# per tier.
CLASSIFIER_PROVIDER = "anthropic"
CLASSIFIER_MODEL_ID = "claude-haiku-4-5-20251001"


def baseline_model_id() -> str:
    return MODELS[BASELINE_TIER]["model_id"]


def baseline_display_name() -> str:
    return MODELS[BASELINE_TIER]["display_name"]
