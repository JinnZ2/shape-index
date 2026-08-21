# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Data structures for structural-shape entries.

The schema deliberately keeps an unidentified constraint as None. That is
honest evidence, not a provisional success state.
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


@dataclass(frozen=True)
class Instance:
    """A domain-specific observation of a structural shape."""

    domain: str
    field_name: str
    instrument: str
    units: str
    citation: str
    scale: str


@dataclass(frozen=True)
class Signature:
    """The structural slots used for matching, not the vocabulary."""

    flows: str
    switches: str
    gated_on: str
    held_constant: str
    units: str


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
