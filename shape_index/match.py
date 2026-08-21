# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Match entries by structural slots rather than by names."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from .schema import ShapeEntry


# The switch-and-gate pair carries the most weight. Units are useful context,
# but are deliberately the weakest signal.
SLOT_WEIGHTS = {
    "flows": 1.0,
    "switches": 2.0,
    "gated_on": 2.0,
    "held_constant": 1.5,
    "units": 0.5,
    "constraint": 1.5,
}

# A slot is reported as matched at or above this overlap. The threshold is a
# reporting convenience only; the underlying overlap is always carried through
# so that a reader can disagree with it.
MATCH_THRESHOLD = 0.5

# Function words carry no structural information, so they are dropped before
# comparison. This list is deliberately tiny: domain terms are never stripped,
# because deciding which terms are unimportant is the reader's call.
_STOPWORDS = frozenset(
    (
        "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "of",
        "on", "or", "the", "to", "with",
    )
)


@dataclass(frozen=True)
class SlotOverlap:
    """The evidence from a single slot, kept so a reader can reject it."""

    slot: str
    overlap: float
    shared: Tuple[str, ...]
    left_only: Tuple[str, ...]
    right_only: Tuple[str, ...]


@dataclass(frozen=True)
class MatchResult:
    """A ranked candidate together with the slots that produced the match."""

    shape_id: str
    score: float
    matched_slots: Tuple[str, ...]
    slots: Tuple[SlotOverlap, ...]

    def overlap(self, slot: str) -> float:
        """Return the recorded overlap for one slot, or 0.0 if incomparable."""

        for entry in self.slots:
            if entry.slot == slot:
                return entry.overlap
        return 0.0


def _tokens(value: object) -> Tuple[str, ...]:
    cleaned = []
    for token in str(value).lower().replace("/", " ").replace(",", " ").split():
        token = token.strip("().;:\"'")
        if token and token not in _STOPWORDS:
            cleaned.append(token)
    return tuple(cleaned)


def _compare_slot(slot: str, left: object, right: object) -> SlotOverlap:
    left_tokens = set(_tokens(left))
    right_tokens = set(_tokens(right))
    union = left_tokens | right_tokens
    shared = left_tokens & right_tokens
    overlap = float(len(shared)) / float(len(union)) if union else 0.0
    return SlotOverlap(
        slot=slot,
        overlap=round(overlap, 4),
        shared=tuple(sorted(shared)),
        left_only=tuple(sorted(left_tokens - right_tokens)),
        right_only=tuple(sorted(right_tokens - left_tokens)),
    )


def compare(left: ShapeEntry, right: ShapeEntry) -> MatchResult:
    """Return a transparent structural comparison of two entries.

    Slots are scored on field-wise token overlap and weighted so that the
    switch-and-gate pair dominates, held-constant follows, and units count for
    least. A slot that is unset on both sides is incomparable and is left out
    of the score entirely; a slot set on one side only scores zero and is kept
    in the denominator, because one-sided evidence should cost something.

    High signature overlap is a prompt to check, not a finding. The tool
    proposes; the reading is done by a person. In particular, this function
    does not inspect shape ids, name strings, citations, or domain labels as
    evidence of a match: matching on those would reproduce the exclusion
    mechanism this index exists to route around.
    """

    slot_values = {
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

    overlaps = []
    weighted = 0.0
    total = 0.0
    for slot in ("flows", "switches", "gated_on", "held_constant", "units", "constraint"):
        left_value, right_value = slot_values[slot]
        if not left_value and not right_value:
            continue
        result = _compare_slot(slot, left_value or "", right_value or "")
        overlaps.append(result)
        weighted += SLOT_WEIGHTS[slot] * result.overlap
        total += SLOT_WEIGHTS[slot]

    score = weighted / total if total else 0.0
    matched = tuple(
        result.slot for result in overlaps if result.overlap >= MATCH_THRESHOLD
    )
    return MatchResult(
        shape_id=right.shape_id,
        score=round(score, 4),
        matched_slots=matched,
        slots=tuple(overlaps),
    )


def rank_candidates(
    query: ShapeEntry,
    candidates: Iterable[ShapeEntry],
    exclude_self: bool = True,
) -> List[MatchResult]:
    """Rank candidates and retain the matched slots for human inspection."""

    results = []
    for candidate in candidates:
        if exclude_self and candidate.shape_id == query.shape_id:
            continue
        results.append(compare(query, candidate))
    return sorted(results, key=lambda result: (-result.score, result.shape_id))


def explain(result: MatchResult) -> str:
    """Render a result as slot-by-slot evidence, never as a bare number.

    The rendering exists so that a reader can see why two entries matched and
    reject the match. Callers that want only the number should reconsider.
    """

    lines = ["%s  score=%.4f" % (result.shape_id, result.score)]
    for slot in result.slots:
        marker = "match" if slot.overlap >= MATCH_THRESHOLD else "     "
        lines.append(
            "  %-14s %-5s overlap=%.2f shared=%s"
            % (slot.slot, marker, slot.overlap, ", ".join(slot.shared) or "-")
        )
        if slot.left_only or slot.right_only:
            lines.append(
                "                       left-only=%s right-only=%s"
                % (", ".join(slot.left_only) or "-", ", ".join(slot.right_only) or "-")
            )
    lines.append("  Overlap is a prompt to check, not a finding.")
    return "\n".join(lines)
