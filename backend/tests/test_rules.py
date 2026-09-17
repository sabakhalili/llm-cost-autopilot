from app.router.rules import apply_overrides


def test_code_override_bumps_simple_to_medium():
    prompt = "```python\nprint('hi')\n```"
    tier, applied, reason = apply_overrides(prompt, "simple")
    assert tier == "medium"
    assert applied is True
    assert reason == "contains code"


def test_code_override_never_downgrades_hard():
    prompt = "```python\nprint('hi')\n```"
    tier, applied, reason = apply_overrides(prompt, "hard")
    assert tier == "hard"
    assert applied is False
    assert reason is None


def test_no_override_when_no_code_present():
    prompt = "What does basis point mean?"
    tier, applied, reason = apply_overrides(prompt, "simple")
    assert tier == "simple"
    assert applied is False
    assert reason is None


def test_code_override_does_not_change_already_medium_tier_label():
    prompt = "def foo():\n    pass\n"
    tier, applied, reason = apply_overrides(prompt, "medium")
    assert tier == "medium"
    assert applied is False
