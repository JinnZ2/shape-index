# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Match entries by structural slots rather than by names."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .schema import ShapeEntry


@dataclass(frozen=True)
class MatchResult:
    """A ranked candidate with the slots that produced the match."""

    shape_id: str
    score: float
    matched_slots: Tuple[str, ...]


# The switch-and-gate pair carries the most weight. Units are useful context,
# but are deliberately the weakest signal.
_WEIGHTS = {
    "flows": 1.0,
    "switches": 2.0,
    "gated_on": 2.0,
    "held_constant": 1.5,
    "units": 0.5,
    "constraint": 1.5,
}


def _normalise(value: object) -> str:
    return " ".join(str(value).lower().split())


def compare(left: ShapeEntry, right: ShapeEntry) -> MatchResult:
    """Return a transparent structural comparison of two entries.

    High signature overlap is a prompt to check, not a finding. The tool
    proposes; the reading is done by a person. In particular, this function
    does not inspect name strings, citations, or domain labels as evidence of
    a match.
    """

    slots: Dict[str, Tuple[object, object]] = {
        "flows": (left.signature.flows, right.signature.flows),
        "switches": (left.signature.switches, right.signature.switches),
        "gated_on": (left.signature.gated_on, right.signature.gated_on),
        "held_constant": (
            left.signature.held_constant,
            right.signature.held_constant,
        ),
        "units": (left.signature.units, right.signature.units),
        "constraint": (left.constraint, right.constraint),
    }
    matched = tuple(
        name for name, (left_value, right_value) in slots.items()
        if left_value is not None
        and right_value is not None
        and _normalise(left_value) == _normalise(right_value)
    )
    total = sum(_WEIGHTS.values())
    score = sum(_WEIGHTS[name] for name in matched) / total
    return MatchResult(right.shape_id, round(score, 4), matched)


def rank_candidates(
    query: ShapeEntry,
    candidates: Iterable[ShapeEntry],
) -> List[MatchResult]:
    """Rank candidates and retain the matched slots for human inspection."""

    results = [compare(query, candidate) for candidate in candidates]
    return sorted(results, key=lambda result: (-result.score, result.shape_id))
