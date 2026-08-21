# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Hand-populated seed entries for the shape index."""

from .schema import Instance, Provenance, ShapeEntry, Signature, Status


SUPPLY_COUPLED_DRAW = ShapeEntry.from_instances(
    shape_id="supply_coupled_draw",
    signature=Signature(
        flows="dietary calories",
        switches="draw magnitude",
        gated_on="household surplus availability",
        held_constant="protection / shelter",
        units="permil amplitude d13C, d15N",
    ),
    constraint=(
        "energy availability under variable supply; a fixed draw runs the "
        "dependent agent's own foraging capability down, while a variable "
        "draw preserves it"
    ),
    constraint_stated=False,
    instances=(
        Instance(
            domain="anthropology",
            field_name="provisioning regime",
            instrument="ethnographic record",
            units="n.a.",
            citation="Lupo 2019",
            scale="household / individual animal",
        ),
        Instance(
            domain="zooarchaeology",
            field_name="seasonal fodder supplementation",
            instrument="sequential intra-tooth isotopes",
            units="permil amplitude d13C, d15N",
            citation="Balasse et al.; Vinca-Belo brdo; Perdigoes",
            scale="household / individual animal",
        ),
        Instance(
            domain="resource-allocation models",
            field_name="no name",
            instrument="absent or fixed coefficient",
            units="n.a.",
            citation="see uninstrumented/coupling_audit",
            scale="household / individual animal",
        ),
    ),
    scale="household / individual animal",
    discriminator=(
        "within-individual sequential spread phased to season, versus "
        "between-individual spread (status class), versus strontium "
        "co-variation (mobility)"
    ),
    status=Status.MULTI_DOMAIN,
    provenance=Provenance.MODEL_SEEDED,
)


ENTRIES = (SUPPLY_COUPLED_DRAW,)
