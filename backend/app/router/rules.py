import re
from typing import Callable

TIER_ORDER = {"simple": 0, "medium": 1, "hard": 2}

CODE_PATTERN = re.compile(
    r"```|\bdef \w+\(|\bfunction \w+\(|\bclass \w+[:{]|;\s*\n", re.MULTILINE
)


def code_override(prompt: str) -> tuple[bool, str | None]:
    return (True, "contains code") if CODE_PATTERN.search(prompt) else (False, None)


# Extensible list of (predicate, floor_tier) pairs. Add more rules here as
# classifier blind spots are discovered.
OVERRIDE_RULES: list[tuple[Callable[[str], tuple[bool, str | None]], str]] = [
    (code_override, "medium"),
]


def apply_overrides(prompt: str, classifier_tier: str) -> tuple[str, bool, str | None]:
    """Apply override rules on top of the classifier's tier.

    Overrides only ever raise the tier, never lower it — a rule can't
    downgrade a request the classifier already flagged as higher-risk.
    """
    final_tier = classifier_tier
    applied = False
    reason: str | None = None

    for predicate, floor_tier in OVERRIDE_RULES:
        matched, label = predicate(prompt)
        if matched and TIER_ORDER[floor_tier] > TIER_ORDER[final_tier]:
            final_tier = floor_tier
            applied = True
            reason = label

    return final_tier, applied, reason
