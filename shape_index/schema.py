# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Data structures for structural-shape entries.

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


class GateType(str, Enum):
    """What the switch is gated on, in controlled terms.

    AVAILABILITY gates on upstream supply; DEMAND on downstream requirement;
    THRESHOLD on a level being crossed; PHASE on position within a cycle;
    STATE on the internal condition of the dependent party.
    """

    AVAILABILITY = "AVAILABILITY"
    DEMAND = "DEMAND"
    THRESHOLD = "THRESHOLD"
    PHASE = "PHASE"
    STATE = "STATE"
    UNSPECIFIED = "UNSPECIFIED"


@dataclass(frozen=True)
class Signature:
    """The structural slots used for matching, not the vocabulary.

    The three typed slots carry the structural claim. The five free-text slots
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
    status: Status = Status.CANDIDATE
    provenance: Provenance = Provenance.AUTHORED

    def __post_init__(self) -> None:
        if self.constraint_stated and not self.constraint:
            raise ValueError("constraint_stated=True requires a constraint")
        if not self.shape_id:
            raise ValueError("shape_id must not be empty")
        if self.status is Status.CONSTRAINT_IDENTIFIED and not self.constraint_stated:
            # constraint_stated exists to separate an argued constraint from an
            # asserted one. Promoting on assertion alone would discard the field.
            raise ValueError(
                "CONSTRAINT_IDENTIFIED requires constraint_stated=True: an "
                "asserted but unargued constraint stays MULTI_DOMAIN with the "
                "constraint recorded and unpromoted"
            )

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
