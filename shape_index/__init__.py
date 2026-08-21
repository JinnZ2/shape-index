# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""A small, inspectable index of recurring structural signatures."""

from .entries import ENTRIES, SUPPLY_COUPLED_DRAW
from .match import (
    MatchResult,
    SlotOverlap,
    compare,
    compare_signatures,
    explain,
    rank_candidates,
    self_consistency,
)
from .schema import (
    GateType,
    Instance,
    Provenance,
    ShapeEntry,
    Signature,
    Status,
    SwitchDirection,
    SwitchPeriodicity,
)

__all__ = [
    "ENTRIES",
    "SUPPLY_COUPLED_DRAW",
    "GateType",
    "Instance",
    "MatchResult",
    "Provenance",
    "ShapeEntry",
    "Signature",
    "SlotOverlap",
    "Status",
    "SwitchDirection",
    "SwitchPeriodicity",
    "compare",
    "compare_signatures",
    "explain",
    "rank_candidates",
    "self_consistency",
]
