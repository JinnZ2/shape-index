# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Data structures for structural-shape entries.

SHAPE_SPEC.md is upstream of this file. A SHAPE is the constraint set a
geometry is a solution to -- not the geometry, not the name. This module
records a signature, which is a geometry description, plus the constraint
proposed to generate it. Those are different objects and the schema keeps
them apart rather than letting the signature stand for the shape.

The schema deliberately keeps an unidentified constraint as None. That is
honest evidence, not a provisional success state.

The switch-and-gate pair is typed rather than free text. Free-text slots are
filled in the vocabulary of whoever writes the entry, so comparing them is a
vocabulary operation one level down from comparing names: it escapes matching
what the fields call the shape and starts matching what the indexer calls the
slots. The controlled terms below are the only slots that carry structural
weight in matching. The free text is kept beside them because it is what a
person reads, but it is scored as vocabulary, which is what it is.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence, Tuple


class Status(str, Enum):
    """Lifecycle state of an indexed shape."""

    CANDIDATE = "CANDIDATE"
    MULTI_DOMAIN = "MULTI_DOMAIN"
    CONSTRAINT_IDENTIFIED = "CONSTRAINT_IDENTIFIED"
    BROKEN = "BROKEN"


class EntryKind(str, Enum):
    """SHAPE_SPEC section 10 classification, derived rather than declared.

    SHAPE_ENTRY    carries a removal test: which constraint, if removed,
                   changes the geometry, plus a case where that constraint is
                   genuinely absent and the form differs.
    GEOMETRY_NOTE  does not. Per SHAPE_SPEC section 10 this is not a shape
                   entry and is marked as such rather than quietly counted as
                   one. The record does not report a shape it has not tested.
    """

    SHAPE_ENTRY = "SHAPE_ENTRY"
    GEOMETRY_NOTE = "GEOMETRY_NOTE"


class Provenance(str, Enum):
    """How the entry was introduced into the index."""

    AUTHORED = "AUTHORED"
    MODEL_SEEDED = "MODEL_SEEDED"


class SwitchDirection(str, Enum):
    """Which way the switched quantity moves when the gate opens."""

    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    BIDIRECTIONAL = "BIDIRECTIONAL"
    UNSPECIFIED = "UNSPECIFIED"


class SwitchPeriodicity(str, Enum):
    """Whether the switching is phased to a cycle."""

    PERIODIC = "PERIODIC"
    APERIODIC = "APERIODIC"
    UNSPECIFIED = "UNSPECIFIED"


class ClosureMode(str, Enum):
    """Whether the omitted relation has a referent outside the formalism.

    This is a property of the relation, which is the same KIND of term as
    every other typed slot. It was first stated as a counterfactual -- "after
    the omitted relation is written into the model, does the credited quantity
    return?" -- which names a repair action rather than a property, and made
    this slot a different kind of thing from the rest of the vocabulary. The
    counterfactual is a consequence of the property, not its definition.

    REPRESENTATIONAL   NO referent outside the formalism. The relation is a
                       coordinate artifact; there is no coupling in the world
                       to find. (Consequence: writing it in returns the
                       quantity, physics untouched.)
    PHYSICAL           YES, a referent outside the formalism. The bath is
                       real, the rails are actually shared, the cluster
                       members really do resemble each other. (Consequence:
                       writing it in reports the loss and does not reverse
                       it; only the apparatus returns the quantity.)
    IRREDUCIBLE        a referent exists and no change of apparatus removes
                       it.

    FALSIFIER FOR THIS SLOT: the map/territory cut collapses if a coordinate
    artifact IS the measurement apparatus, because then the relation is both
    inside and outside the formalism at once. Watch for that case; it retires
    the distinction and folds the two entries it separates. See OPEN.md --
    `independence_credited_vs_joint`'s category-weld instance may already be
    it, and is flagged rather than resolved.

    This slot exists because two entries were being separated by a free-text
    discriminator alone, which the structural layer does not read. A
    discriminator carrying that load in prose is a defect, not a finished
    entry.
    """

    REPRESENTATIONAL = "REPRESENTATIONAL"
    PHYSICAL = "PHYSICAL"
    IRREDUCIBLE = "IRREDUCIBLE"
    UNSPECIFIED = "UNSPECIFIED"


class GateType(str, Enum):
    """What the switch is gated on, in controlled terms.

    AVAILABILITY gates on upstream supply; DEMAND on downstream requirement;
    THRESHOLD on a level being crossed; PHASE on position within a cycle;
    STATE on the internal condition of the dependent party.

    REPRESENTATION gates on whether a relation among the parts is present in
    the formalism, rather than on any physical quantity. It was added after
    two entries in a row could not be typed by the other five, which named
    only properties of a physical quantity. The failure is recorded in
    OPEN.md and in LOG.md before this term; the record shows the vocabulary
    failing before it shows it patched.
    """

    AVAILABILITY = "AVAILABILITY"
    DEMAND = "DEMAND"
    THRESHOLD = "THRESHOLD"
    PHASE = "PHASE"
    STATE = "STATE"
    REPRESENTATION = "REPRESENTATION"
    UNSPECIFIED = "UNSPECIFIED"


@dataclass(frozen=True)
class Signature:
    """The structural slots used for matching, not the vocabulary.

    The four typed slots carry the structural claim. The five free-text slots
    record how this filling was worded, and are scored separately as lexical
    evidence so that the two are never conflated in one number.
    """

    flows: str
    switches: str
    gated_on: str
    held_constant: str
    units: str
    switch_direction: SwitchDirection = SwitchDirection.UNSPECIFIED
    switch_periodicity: SwitchPeriodicity = SwitchPeriodicity.UNSPECIFIED
    gate_type: GateType = GateType.UNSPECIFIED
    closure_mode: ClosureMode = ClosureMode.UNSPECIFIED


@dataclass(frozen=True)
class Instance:
    """A domain-specific observation of a structural shape.

    `signature` is that field's own filling of the slots, in that field's
    words. It is optional because a field may have no name and no filling for
    the shape at all, which is itself worth recording. Where it is present, an
    entry can be checked against itself across its own domains.
    """

    domain: str
    field_name: str
    instrument: str
    units: str
    citation: str
    scale: str
    signature: Optional[Signature] = None


@dataclass(frozen=True)
class ShapeEntry:
    """An indexed structural signature and its evidence."""

    shape_id: str
    signature: Signature
    constraint: Optional[str]
    constraint_stated: bool
    instances: Tuple[Instance, ...] = field(default_factory=tuple)
    scale: str = ""
    discriminator: str = ""
    # SHAPE_SPEC section 4. Which constraint, if REMOVED, changes the
    # geometry -- and a case where that constraint is genuinely absent, with
    # the form observed to differ. None until the test has been stated; the
    # entry is then a geometry note, not a shape entry.
    removal_test: Optional[str] = None
    status: Status = Status.CANDIDATE
    provenance: Provenance = Provenance.AUTHORED
    # METHOD_SPEC section 5. A read is a marker, not a result. Confidence is
    # a readout reported SEPARATELY from the pattern, with the level at which
    # an operator would act on it. None means no gradient has been stated --
    # not zero, not one. Assigning a number where none was given resolves a
    # marker on its behalf, which is what section 5 forbids.
    confidence: Optional[float] = None
    comfort_threshold: Optional[float] = None

    def __post_init__(self) -> None:
        if self.constraint_stated and not self.constraint:
            raise ValueError("constraint_stated=True requires a constraint")
        if not self.shape_id:
            raise ValueError("shape_id must not be empty")
        for name in ("confidence", "comfort_threshold"):
            value = getattr(self, name)
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError("%s must lie in [0.0, 1.0]" % name)
        if self.status is Status.CONSTRAINT_IDENTIFIED and not self.constraint_stated:
            # constraint_stated exists to separate an argued constraint from an
            # asserted one. Promoting on assertion alone would discard the field.
            raise ValueError(
                "CONSTRAINT_IDENTIFIED requires constraint_stated=True: an "
                "asserted but unargued constraint stays MULTI_DOMAIN with the "
                "constraint recorded and unpromoted"
            )

    def kind(self) -> EntryKind:
        """SHAPE_SPEC section 10. A shape entry carries a removal test."""

        if self.removal_test:
            return EntryKind.SHAPE_ENTRY
        return EntryKind.GEOMETRY_NOTE

    def instrumented_instances(self) -> Tuple[Instance, ...]:
        """Instances that record their own field's filling of the slots."""

        return tuple(
            instance for instance in self.instances if instance.signature is not None
        )

    @classmethod
    def from_instances(
        cls,
        shape_id: str,
        signature: Signature,
        constraint: Optional[str],
        constraint_stated: bool,
        instances: Sequence[Instance],
        scale: str,
        discriminator: str,
        status: Status,
        provenance: Provenance,
    ) -> "ShapeEntry":
        return cls(
            shape_id=shape_id,
            signature=signature,
            constraint=constraint,
            constraint_stated=constraint_stated,
            instances=tuple(instances),
            scale=scale,
            discriminator=discriminator,
            status=status,
            provenance=provenance,
        )
