# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Match entries by structural slots rather than by names.

Two layers are scored and reported separately, never blended into a single
headline number. The structural layer compares the typed switch-and-gate slots,
which are drawn from a controlled vocabulary. The lexical layer compares the
free-text slots by token overlap, which is a vocabulary operation and is
labelled as one. An entry that scores high structurally and near zero lexically
is the case this index exists for: the same shape, worded with no shared terms.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Optional, Tuple

from .schema import ShapeEntry, Signature


# Within the structural layer the gate carries the most weight, then the two
# switch descriptors. Within the lexical layer held-constant leads and units
# trail, as before; the free-text switch and gate slots sit near the bottom
# because their typed counterparts already carry that claim.
STRUCTURAL_WEIGHTS = {
    "gate_type": 2.0,
    "closure_mode": 2.0,
    "switch_direction": 1.0,
    "switch_periodicity": 1.0,
}

LEXICAL_WEIGHTS = {
    "flows": 1.0,
    "held_constant": 1.5,
    "constraint": 1.5,
    "switches": 0.5,
    "gated_on": 0.5,
    "units": 0.5,
}

SLOT_WEIGHTS = dict(STRUCTURAL_WEIGHTS)
SLOT_WEIGHTS.update(LEXICAL_WEIGHTS)

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

_STRUCTURAL_ORDER = (
    "gate_type", "closure_mode", "switch_direction", "switch_periodicity",
)
_LEXICAL_ORDER = ("flows", "switches", "gated_on", "held_constant", "units", "constraint")


@dataclass(frozen=True)
class SlotOverlap:
    """The evidence from a single slot, kept so a reader can reject it.

    `one_sided` marks a slot filled on one side and unset on the other. It
    scores 0.0 and stays in the denominator, because one-sided evidence
    should cost something -- but it is an ABSTENTION, not a disagreement,
    and reporting the two identically lets a pair that agrees on everything
    both sides specify look like a pair that disagrees.
    """

    slot: str
    layer: str
    overlap: float
    shared: Tuple[str, ...]
    left_only: Tuple[str, ...]
    right_only: Tuple[str, ...]
    one_sided: bool = False


@dataclass(frozen=True)
class MatchResult:
    """A ranked candidate together with the slots that produced the match."""

    shape_id: str
    score: float
    structural_score: float
    lexical_score: float
    matched_slots: Tuple[str, ...]
    slots: Tuple[SlotOverlap, ...]

    def overlap(self, slot: str) -> float:
        """Return the recorded overlap for one slot, or 0.0 if incomparable."""

        for entry in self.slots:
            if entry.slot == slot:
                return entry.overlap
        return 0.0

    def layer(self, name: str) -> Tuple[SlotOverlap, ...]:
        """Return the slots belonging to one layer."""

        return tuple(entry for entry in self.slots if entry.layer == name)

    def abstentions(self, name: str) -> int:
        """Slots in a layer where one side is unset: abstention, not conflict.

        A pair that agrees on every slot both sides fill, and abstains on one,
        scores below 1.0. Read the shortfall against this count before reading
        it as disagreement.
        """

        return len([e for e in self.layer(name) if e.one_sided])

    def support(self, name: str) -> int:
        """How many comparable slots a layer's score actually rests on.

        A layer score of 1.0 carries very different weight depending on
        whether three slots agreed or one did, and the score alone cannot
        say which. Reporting the score without its support reproduces, one
        level down, the collapse this module refuses everywhere else: a
        single number standing in for evidence a reader should be able to
        weigh. Always read a layer score against its support.
        """

        return len(self.layer(name))


def _tokens(value: object) -> Tuple[str, ...]:
    cleaned = []
    for token in str(value).lower().replace("/", " ").replace(",", " ").split():
        token = token.strip("().;:\"'")
        if token and token not in _STOPWORDS:
            cleaned.append(token)
    return tuple(cleaned)


def _lexical_slot(slot: str, left: object, right: object,
                  one_sided: bool = False) -> SlotOverlap:
    left_tokens = set(_tokens(left))
    right_tokens = set(_tokens(right))
    union = left_tokens | right_tokens
    shared = left_tokens & right_tokens
    overlap = float(len(shared)) / float(len(union)) if union else 0.0
    return SlotOverlap(
        slot=slot,
        layer="lexical",
        overlap=round(overlap, 4),
        shared=tuple(sorted(shared)),
        left_only=tuple(sorted(left_tokens - right_tokens)),
        right_only=tuple(sorted(right_tokens - left_tokens)),
        one_sided=one_sided,
    )


def _structural_slot(slot: str, left: Enum, right: Enum,
                     one_sided: bool = False) -> SlotOverlap:
    """Controlled terms are identical or they are not. There is no partial."""

    same = left is right
    return SlotOverlap(
        slot=slot,
        layer="structural",
        overlap=1.0 if same else 0.0,
        shared=(left.value,) if same else (),
        left_only=() if same else (left.value,),
        right_only=() if same else (right.value,),
        one_sided=one_sided,
    )


def _is_unset(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, Enum):
        return value.value == "UNSPECIFIED"
    return not str(value).strip()


def _score(overlaps, weights) -> float:
    total = sum(weights[item.slot] for item in overlaps)
    if not total:
        return 0.0
    weighted = sum(weights[item.slot] * item.overlap for item in overlaps)
    return weighted / total


def _compare_slots(
    left: Signature,
    right: Signature,
    left_constraint: Optional[str] = None,
    right_constraint: Optional[str] = None,
) -> Tuple[SlotOverlap, ...]:
    """Score every comparable slot.

    A slot unset on both sides is incomparable and is dropped rather than
    scored as agreement. A slot set on one side only scores zero and stays in
    the denominator, because one-sided evidence should cost something.
    """

    typed = {
        "gate_type": (left.gate_type, right.gate_type),
        "closure_mode": (left.closure_mode, right.closure_mode),
        "switch_direction": (left.switch_direction, right.switch_direction),
        "switch_periodicity": (left.switch_periodicity, right.switch_periodicity),
    }
    free = {
        "flows": (left.flows, right.flows),
        "switches": (left.switches, right.switches),
        "gated_on": (left.gated_on, right.gated_on),
        "held_constant": (left.held_constant, right.held_constant),
        "units": (left.units, right.units),
        "constraint": (left_constraint, right_constraint),
    }

    overlaps = []
    for slot in _STRUCTURAL_ORDER:
        left_value, right_value = typed[slot]
        if _is_unset(left_value) and _is_unset(right_value):
            continue
        one_sided = _is_unset(left_value) != _is_unset(right_value)
        overlaps.append(
            _structural_slot(slot, left_value, right_value, one_sided))
    for slot in _LEXICAL_ORDER:
        left_value, right_value = free[slot]
        if _is_unset(left_value) and _is_unset(right_value):
            continue
        one_sided = _is_unset(left_value) != _is_unset(right_value)
        overlaps.append(_lexical_slot(
            slot, left_value or "", right_value or "", one_sided))
    return tuple(overlaps)


def _result(shape_id: str, overlaps: Tuple[SlotOverlap, ...]) -> MatchResult:
    structural = [item for item in overlaps if item.layer == "structural"]
    lexical = [item for item in overlaps if item.layer == "lexical"]
    return MatchResult(
        shape_id=shape_id,
        score=round(_score(overlaps, SLOT_WEIGHTS), 4),
        structural_score=round(_score(structural, STRUCTURAL_WEIGHTS), 4),
        lexical_score=round(_score(lexical, LEXICAL_WEIGHTS), 4),
        matched_slots=tuple(
            item.slot for item in overlaps if item.overlap >= MATCH_THRESHOLD
        ),
        slots=overlaps,
    )


def compare_signatures(left: Signature, right: Signature, label: str = "") -> MatchResult:
    """Compare two slot fillings directly, without entry-level constraints."""

    return _result(label, _compare_slots(left, right))


def compare(left: ShapeEntry, right: ShapeEntry) -> MatchResult:
    """Return a transparent structural comparison of two entries.

    High signature overlap is a prompt to check, not a finding. The tool
    proposes; the reading is done by a person. In particular, this function
    does not inspect shape ids, name strings, citations, or domain labels as
    evidence of a match: matching on those would reproduce the exclusion
    mechanism this index exists to route around.
    """

    return _result(
        right.shape_id,
        _compare_slots(left.signature, right.signature, left.constraint, right.constraint),
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


def self_consistency(entry: ShapeEntry) -> List[Tuple[str, str, MatchResult]]:
    """Compare an entry against itself across its own instrumented domains.

    An entry claims that several fields describe one structure. This runs that
    claim as a comparison: every pair of instances that records its own field's
    filling of the slots, scored the same way two separate entries would be. An
    entry whose own instances do not match structurally is making a claim the
    index cannot see.
    """

    instrumented = entry.instrumented_instances()
    pairs = []
    for index, left in enumerate(instrumented):
        for right in instrumented[index + 1:]:
            label = "%s vs %s" % (left.domain, right.domain)
            pairs.append(
                (
                    left.domain,
                    right.domain,
                    compare_signatures(left.signature, right.signature, label),
                )
            )
    return pairs


def explain(result: MatchResult) -> str:
    """Render a result as slot-by-slot evidence, never as a bare number.

    The rendering exists so that a reader can see why two entries matched and
    reject the match. Callers that want only the number should reconsider.
    """

    lines = [
        "%s" % (result.shape_id or "(unlabelled)"),
        "  structural=%.4f on %d slot(s)   lexical=%.4f on %d slot(s)"
        % (result.structural_score, result.support("structural"),
           result.lexical_score, result.support("lexical")),
        "  blended=%.4f" % result.score,
    ]
    for layer_name in ("structural", "lexical"):
        n = result.abstentions(layer_name)
        if n:
            lines.append(
                "  NOTE: %d %s slot(s) marked abst. are ABSTENTIONS -- unset on"
                % (n, layer_name)
            )
            lines.append(
                "  one side, not disagreements. The score is reduced by them."
            )
    if result.support("structural") == 1:
        lines.append(
            "  NOTE: the structural score rests on ONE slot. It cannot "
            "distinguish"
        )
        lines.append(
            "  agreement from absence of anything to disagree about."
        )
    for layer in ("structural", "lexical"):
        slots = result.layer(layer)
        if not slots:
            continue
        lines.append("  [%s]" % layer)
        for slot in slots:
            if slot.one_sided:
                marker = "abst."
            elif slot.overlap >= MATCH_THRESHOLD:
                marker = "match"
            else:
                marker = "     "
            lines.append(
                "    %-19s %-5s overlap=%.2f shared=%s"
                % (slot.slot, marker, slot.overlap, ", ".join(slot.shared) or "-")
            )
            if slot.left_only or slot.right_only:
                lines.append(
                    "                              left=%s right=%s"
                    % (", ".join(slot.left_only) or "-", ", ".join(slot.right_only) or "-")
                )
    lines.append("  Overlap is a prompt to check, not a finding.")
    return "\n".join(lines)
