# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""A small, inspectable index of recurring structural signatures."""

from .entries import ENTRIES, SUPPLY_COUPLED_DRAW
from .match import MatchResult, SlotOverlap, compare, explain, rank_candidates
from .schema import Instance, Provenance, ShapeEntry, Signature, Status

__all__ = [
    "ENTRIES",
    "SUPPLY_COUPLED_DRAW",
    "Instance",
    "MatchResult",
    "Provenance",
    "ShapeEntry",
    "Signature",
    "SlotOverlap",
    "Status",
    "compare",
    "explain",
    "rank_candidates",
]
