# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Hand-populated seed entries for the shape index."""

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


# Each instrumented instance records its own field's filling of the slots, in
# that field's words. The two fillings share almost no vocabulary, which is the
# point: the entry has to match itself on the typed slots or it is not making a
# claim the index can see. See test_shape_index.SelfConsistencyTests.
_ANTHROPOLOGY_SIGNATURE = Signature(
    flows="dietary calories",
    switches="provisioning intensity",
    gated_on="household surplus",
    held_constant="shelter and protection",
    units="n.a.",
    switch_direction=SwitchDirection.BIDIRECTIONAL,
    switch_periodicity=SwitchPeriodicity.APERIODIC,
    gate_type=GateType.AVAILABILITY,
)

_ZOOARCHAEOLOGY_SIGNATURE = Signature(
    flows="foddered plant intake",
    switches="supplementation intensity",
    gated_on="seasonal forage availability",
    held_constant="penning",
    units="permil amplitude d13C, d15N",
    switch_direction=SwitchDirection.BIDIRECTIONAL,
    switch_periodicity=SwitchPeriodicity.PERIODIC,
    gate_type=GateType.AVAILABILITY,
)


SUPPLY_COUPLED_DRAW = ShapeEntry.from_instances(
    shape_id="supply_coupled_draw",
    signature=Signature(
        flows="dietary calories",
        switches="draw magnitude",
        gated_on="household surplus availability",
        held_constant="protection / shelter",
        units="permil amplitude d13C, d15N",
        switch_direction=SwitchDirection.BIDIRECTIONAL,
        # The two instrumented instances disagree here: household surplus is
        # aperiodic, seasonal foddering is periodic. Recorded as unspecified at
        # entry level rather than resolved by picking one.
        switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
        gate_type=GateType.AVAILABILITY,
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
            signature=_ANTHROPOLOGY_SIGNATURE,
        ),
        Instance(
            domain="zooarchaeology",
            field_name="seasonal fodder supplementation",
            instrument="sequential intra-tooth isotopes",
            units="permil amplitude d13C, d15N",
            citation="Balasse et al.; Vinca-Belo brdo; Perdigoes",
            scale="household / individual animal",
            signature=_ZOOARCHAEOLOGY_SIGNATURE,
        ),
        Instance(
            domain="resource-allocation models",
            field_name="no name",
            instrument="absent or fixed coefficient",
            units="n.a.",
            citation="see uninstrumented/coupling_audit",
            scale="household / individual animal",
            # No signature: the field has no name and no filling for the shape.
            # That absence is the observation, not a gap to be invented into.
            signature=None,
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
