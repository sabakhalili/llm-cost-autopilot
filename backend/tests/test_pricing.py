from app.router.pricing import calculate_cost


def test_calculate_cost_basic():
    cost = calculate_cost("gpt-4o-mini", input_tokens=1_000_000, output_tokens=1_000_000)
    assert cost == 0.15 + 0.60


def test_calculate_cost_zero_tokens():
    assert calculate_cost("gpt-4o", input_tokens=0, output_tokens=0) == 0.0


def test_cheaper_model_costs_less_for_same_tokens():
    cheap = calculate_cost("gpt-4o-mini", input_tokens=1000, output_tokens=1000)
    expensive = calculate_cost("gpt-4o", input_tokens=1000, output_tokens=1000)
    assert cheap < expensive
