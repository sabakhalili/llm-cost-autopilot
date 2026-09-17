# $ per 1M tokens. These are illustrative placeholders — verify against each
# provider's current pricing page before flipping MOCK_MODE off for a live demo.
# Deliberately monotonic across tiers (simple < medium < hard) so the router
# never reports negative savings when it steps down a tier.
PRICING_TABLE = {
    "gpt-4o-mini": {"input_per_1m": 0.15, "output_per_1m": 0.60},
    "claude-haiku-4-5-20251001": {"input_per_1m": 0.80, "output_per_1m": 4.00},
    "gpt-4o": {"input_per_1m": 2.50, "output_per_1m": 10.00},
}


def calculate_cost(model_id: str, input_tokens: int, output_tokens: int) -> float:
    pricing = PRICING_TABLE[model_id]
    return (
        (input_tokens / 1_000_000) * pricing["input_per_1m"]
        + (output_tokens / 1_000_000) * pricing["output_per_1m"]
    )
