"""Transparent ordinal scoring for the GCC Compass location prototype."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any


CRITERIA = {
    "talent": "talent_signal",
    "office_cost": "office_cost_signal",
    "ecosystem": "ecosystem_depth",
}
MIN_ASSESSED_CRITERIA = 2

_ORDINAL_SCORES = {
    "very low": 1.0,
    "low": 2.0,
    "medium low": 2.5,
    "medium": 3.0,
    "medium high": 3.5,
    "high": 4.0,
    "very high": 5.0,
}


def normalize_weights(weights: Mapping[str, float]) -> dict[str, float]:
    """Return non-negative relative weights normalized to sum to one."""
    values: dict[str, float] = {}
    for criterion in CRITERIA:
        value = float(weights.get(criterion, 0))
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"Weight for {criterion!r} must be finite and non-negative.")
        values[criterion] = value

    total = sum(values.values())
    if total <= 0:
        raise ValueError("At least one criterion weight must be greater than zero.")
    return {criterion: value / total for criterion, value in values.items()}


def rounded_weight_percentages(weights: Mapping[str, float]) -> dict[str, int]:
    """Convert weights to whole percentages that add up to exactly 100."""
    normalized = normalize_weights(weights)
    exact = {key: value * 100 for key, value in normalized.items()}
    rounded = {key: math.floor(value) for key, value in exact.items()}
    remainder = 100 - sum(rounded.values())
    order = sorted(
        exact,
        key=lambda key: (exact[key] - rounded[key], -list(CRITERIA).index(key)),
        reverse=True,
    )
    for criterion in order[:remainder]:
        rounded[criterion] += 1
    return rounded


def ordinal_score(value: Any, criterion: str) -> float | None:
    """Map an assessed qualitative label to 1–5; reverse office-cost direction."""
    if criterion not in CRITERIA:
        raise ValueError(f"Unknown location criterion: {criterion!r}")
    if not isinstance(value, str):
        return None
    label = " ".join(value.casefold().replace("-", " ").replace("–", " ").split())
    score = _ORDINAL_SCORES.get(label)
    if score is None:
        return None
    return 6.0 - score if criterion == "office_cost" else score


def rank_cities(
    city_records: Sequence[Mapping[str, Any]],
    weights: Mapping[str, float],
    minimum_assessed: int = MIN_ASSESSED_CRITERIA,
) -> list[dict[str, Any]]:
    """Score assessed city signals and rank only sufficiently complete profiles."""
    if not 1 <= minimum_assessed <= len(CRITERIA):
        raise ValueError("minimum_assessed must be between 1 and the number of criteria.")

    normalized_weights = normalize_weights(weights)
    results: list[dict[str, Any]] = []
    for record in city_records:
        scores = {
            criterion: ordinal_score(record.get(column), criterion)
            for criterion, column in CRITERIA.items()
        }
        assessed = [key for key, score in scores.items() if score is not None]
        complete = len(assessed)
        enough_data = complete >= minimum_assessed
        assessed_weight = sum(normalized_weights[key] for key in assessed)
        weighted_score = None
        if enough_data and assessed_weight > 0:
            weighted_score = sum(
                scores[key] * normalized_weights[key]
                for key in assessed
                if scores[key] is not None
            ) / assessed_weight

        results.append({
            "city": str(record.get("city", "")),
            "scores": scores,
            "assessed_criteria": complete,
            "evidence_completeness": complete / len(CRITERIA),
            "score": weighted_score,
            "rank": None,
            "fit_notes": record.get("fit_notes", ""),
            "validation_note": record.get("policy_or_validation_note", ""),
            "source_url": record.get("source_url", ""),
        })

    rankable = sorted(
        (row for row in results if row["score"] is not None),
        key=lambda row: (-row["score"], row["city"].casefold()),
    )
    for rank, row in enumerate(rankable, start=1):
        row["rank"] = rank
    return sorted(
        results,
        key=lambda row: (
            row["score"] is None,
            row["rank"] if row["rank"] is not None else math.inf,
            row["city"].casefold(),
        ),
    )
