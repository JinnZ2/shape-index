# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

"""Hand-populated seed entries for the shape index."""

from .schema import (
    ClosureMode,
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


# ---------------------------------------------------------------------------
# occupied_set_vs_space
#
# constraint_stated=True with status=MULTI_DOMAIN is deliberate, not an
# oversight. The two flags answer different questions: constraint_stated
# records that the constraint is ARGUED rather than merely named, and the
# constraint text below does argue it. CONSTRAINT_IDENTIFIED would additionally
# require that the argument had been measured across the instances, and it has
# not been. The schema permits argued-but-unmeasured to sit at MULTI_DOMAIN;
# that is the state this entry is in.
#
# gate_type=REPRESENTATION and closure_mode=REPRESENTATIONAL. Both terms were
# added after this entry and the next one refused to type under the original
# five gate terms, which named only properties of a physical quantity. The
# refusal is recorded in OPEN.md and LOG.md ahead of the patch.
#
# closure_mode is what separates this entry from independence_credited_vs_joint:
# here adding the omitted constraint returns the quantity with the physics
# untouched, so the gap is REPRESENTATIONAL.

_FOLDING_SIGNATURE = Signature(
    flows="enumeration cost, in conformations",
    switches="conformations priced: full torsion space versus observed folds",
    gated_on="whether the funnelled energy landscape is in the model",
    held_constant="the folding process itself",
    units="conformations",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.REPRESENTATIONAL,
)

_TENSOR_NETWORK_SIGNATURE = Signature(
    flows="classical representation cost, in real parameters",
    switches="state-space size priced: Hilbert dimension versus bond dimension",
    gated_on="whether the entanglement area law is in the representation",
    held_constant="the quantum state and its Hamiltonian",
    units="Hilbert-space dimension, bond dimension",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.REPRESENTATIONAL,
)

_CONTROL_MANIFOLD_SIGNATURE = Signature(
    flows="dynamic-programming cost, in evaluated states",
    switches="states priced: full grid versus the reachable manifold",
    gated_on="whether the trajectory manifold is identified in the model",
    held_constant="the plant and its dynamics",
    units="state-space dimension",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.REPRESENTATIONAL,
)


OCCUPIED_SET_VS_SPACE = ShapeEntry.from_instances(
    shape_id="occupied_set_vs_space",
    signature=Signature(
        flows="enumeration cost, in operations",
        switches=(
            "the count being priced: the full configuration space versus the "
            "set the system occupies"
        ),
        gated_on=(
            "whether the constraint selecting the occupied set is represented "
            "in the formalism"
        ),
        held_constant="the physical process, unchanged across both prices",
        units="operations",
        switch_direction=SwitchDirection.DECREASE,
        switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
        gate_type=GateType.REPRESENTATION,
        closure_mode=ClosureMode.REPRESENTATIONAL,
    ),
    constraint=(
        "the configuration space is generated by the coordinate choice, not "
        "by the system; the occupied set is what the system's actual "
        "constraints leave. Where the selecting constraint is absent from the "
        "formalism, the enumeration prices the coordinates."
    ),
    constraint_stated=True,
    instances=(
        Instance(
            domain="protein folding",
            field_name="Levinthal's paradox",
            instrument="conformational enumeration versus observed fold census",
            units="conformations, ops",
            citation=(
                "Levinthal 1969; funnelled landscape: Bryngelson & Wolynes "
                "1987, PNAS 84:7524; fold census: SCOP / CATH. ~3**300 space "
                "against a few thousand observed folds."
            ),
            scale="molecular",
            signature=_FOLDING_SIGNATURE,
        ),
        Instance(
            domain="quantum many-body",
            field_name="curse of dimensionality; area law versus volume law",
            instrument="tensor-network representation, DMRG",
            units="Hilbert-space dimension, bond dimension",
            citation=(
                "White 1992, Phys Rev Lett 69:2863; Eisert, Cramer & Plenio "
                "2010, Rev Mod Phys 82:277. d**N against polynomial for "
                "area-law states."
            ),
            scale="molecular to condensed matter",
            signature=_TENSOR_NETWORK_SIGNATURE,
        ),
        Instance(
            domain="statistical mechanics",
            field_name="entropy as observer-relative",
            instrument="choice of macrovariables",
            units="bits, joules per kelvin",
            citation=(
                "Jaynes 1957, Phys Rev 106:620; Jaynes 1965, Am J Phys "
                "33:391. The quantity depends on the coarse-graining chosen, "
                "not on the gas."
            ),
            scale="thermodynamic",
            # No signature: the slot filling for this instance was not
            # supplied, and inventing one would author the match rather than
            # record it.
            signature=None,
        ),
        Instance(
            domain="algorithmic information",
            field_name="Kolmogorov complexity; uncomputability",
            instrument="compression ratio on real corpora",
            units="bits",
            citation=(
                "Kolmogorov 1965; Chaitin 1966; Li & Vitanyi, An Introduction "
                "to Kolmogorov Complexity. Incompressible strings are generic "
                "in measure and near-absent in encountered data."
            ),
            scale="corpus",
            signature=None,
        ),
        Instance(
            domain="cryptography",
            field_name="worst-case versus average-case hardness",
            instrument="reduction proofs",
            units="security parameter",
            citation=(
                "Impagliazzo 1995, Structure in Complexity Theory; Ajtai "
                "1996, STOC. INCLUDED AS AN UNRESOLVED CASE, NOT AS SUPPORT: "
                "the gap is a standing open problem, not a resolved instance "
                "of this shape."
            ),
            scale="asymptotic",
            signature=None,
        ),
        Instance(
            domain="optimal control",
            field_name="curse of dimensionality in dynamic programming",
            instrument="manifold or subspace identification",
            units="state-space dimension",
            citation=(
                "Bellman 1957, Dynamic Programming. Dissolved where the "
                "trajectory manifold is low-dimensional."
            ),
            scale="plant / trajectory",
            signature=_CONTROL_MANIFOLD_SIGNATURE,
        ),
        Instance(
            domain="simulation cost of Earth",
            field_name="no name found",
            instrument="Lloyd bound against itemized process classes",
            units="operations",
            citation=(
                "Lloyd 2002, Phys Rev Lett 88:237901, for the ~1e120 figure; "
                "see simulation-hypothesis-budget/SCALING_CLASSES.md. Note "
                "the figure is routinely cited as Lloyd 1999, which is the "
                "preprint date of the Nature 2000 paper, not of this bound."
            ),
            scale="planetary to cosmological",
            signature=None,
        ),
    ),
    scale=(
        "spans molecular to cosmological; the shape is scale-free with "
        "respect to the domains listed"
    ),
    discriminator=(
        "the cost gap closes when the selecting constraint is added to the "
        "representation, with the physics untouched, and does not close when "
        "the constraint is genuinely absent from the physics. Positive cases: "
        "funnelled folding, area-law tensor networks, control manifolds. "
        "Negative case that must stay negative: volume-law entangled states, "
        "where no representation change recovers polynomial cost. The entry "
        "breaks if a case is found where adding the known constraint fails to "
        "close the gap, or where the gap closes with no constraint identified."
    ),
    status=Status.MULTI_DOMAIN,
    provenance=Provenance.MODEL_SEEDED,
)


# ---------------------------------------------------------------------------
# independence_credited_vs_joint
#
# This entry sits close to occupied_set_vs_space and is kept separate on the
# strength of its discriminator, not on the strength of its wording. Both
# switch a count on whether a relation is present in the formalism, and both
# switch DECREASE. What separates them is what closes the gap:
#
#   occupied_set_vs_space   adding the omitted constraint closes the gap with
#                           the physics untouched. The fix is representational.
#                           The coordinates had invented freedom that was
#                           never there.
#
#   this entry              adding the omitted coupling does NOT return the
#                           credited quantity. Writing the channel into the
#                           model tells you the truth; it does not restore the
#                           independence. The fix is physical -- separate the
#                           rails, split the pump -- or there is no fix.
#
# If that discriminator fails, these are one shape and this entry should be
# folded into the other as further instances rather than left standing.
#
# closure_mode=PHYSICAL is the slot that carries the separation from
# occupied_set_vs_space. It was free text in the discriminator until the
# structural layer was given a term for it; a discriminator carrying that load
# in prose is a defect, because the layer that does the matching cannot read it.

_ENTROPY_SOURCE_SIGNATURE = Signature(
    flows="min-entropy, in bits per sample",
    switches="entropy credited: sum over legs versus the joint distribution",
    gated_on="whether the shared bath coupling the legs is in the model",
    held_constant="each leg's own noise process",
    units="bits of min-entropy",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.PHYSICAL,
)

_REDUNDANCY_SIGNATURE = Signature(
    flows="failure probability, per demand",
    switches="redundancy credited: product over channels versus joint failure",
    gated_on="whether the common cause is in the fault tree",
    held_constant="each channel's own failure rate",
    units="probability per demand, beta factor",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.PHYSICAL,
)

_SAMPLE_SIZE_SIGNATURE = Signature(
    flows="information, in independent observations",
    switches="observations credited: raw count versus effective sample size",
    gated_on="whether the clustering or autocorrelation is in the design",
    held_constant="each observation's own measurement",
    units="observations, design effect",
    switch_direction=SwitchDirection.DECREASE,
    switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
    gate_type=GateType.REPRESENTATION,
    closure_mode=ClosureMode.PHYSICAL,
)


INDEPENDENCE_CREDITED_VS_JOINT = ShapeEntry.from_instances(
    shape_id="independence_credited_vs_joint",
    signature=Signature(
        flows="independent degrees of freedom, counted in components or bits",
        switches=(
            "the count being credited: the sum over the parts versus the "
            "joint state of the parts"
        ),
        gated_on=(
            "whether the channel coupling the parts is represented in the "
            "model"
        ),
        held_constant=(
            "the parts and their individual behaviour, unchanged across both "
            "counts"
        ),
        units="components, bits of min-entropy, effective sample size",
        switch_direction=SwitchDirection.DECREASE,
        switch_periodicity=SwitchPeriodicity.UNSPECIFIED,
        gate_type=GateType.REPRESENTATION,
        closure_mode=ClosureMode.PHYSICAL,
    ),
    constraint=(
        "a shared channel is a physical path. Where two parts couple to one "
        "bath, their joint state carries fewer degrees of freedom than the "
        "sum of their separate states, and no accounting that omits the "
        "channel recovers the difference. The omission is in the model; the "
        "coupling is in the world. This is why the correction is not "
        "symmetric with occupied_set_vs_space: there the surplus was an "
        "artifact of the coordinates and removing it costs nothing, here the "
        "deficit is in the apparatus and only the apparatus can return it."
    ),
    constraint_stated=True,
    instances=(
        Instance(
            domain="hardware entropy sources",
            field_name="correlated drift; shared noise floor",
            instrument="cross-correlation under driven bath perturbation",
            units="bits of min-entropy",
            citation=(
                "Chor & Goldreich 1988, SIAM J Comput 17:230, for two-source "
                "extraction requiring independence; NIST SP 800-90B for "
                "min-entropy accounting under non-IID sources. Worked in "
                "qrng-pair-search/ in this ecosystem."
            ),
            scale="board / device",
            signature=_ENTROPY_SOURCE_SIGNATURE,
        ),
        Instance(
            domain="reliability engineering",
            field_name="common-cause failure",
            instrument="beta-factor model; common-cause failure database",
            units="probability per demand, beta factor",
            citation=(
                "Fleming 1975, Proc 6th Pittsburgh Conf on Modeling and "
                "Simulation, for the beta-factor model; IEC 61508; "
                "NUREG/CR-6268 common-cause failure database. Nominal "
                "redundancy N against a much smaller effective redundancy."
            ),
            scale="plant / safety system",
            signature=_REDUNDANCY_SIGNATURE,
        ),
        Instance(
            domain="survey statistics",
            field_name="design effect; effective sample size",
            instrument="deff estimation from cluster and weight structure",
            units="observations, design effect",
            citation=(
                "Kish 1965, Survey Sampling. n_eff = n / deff; clustered "
                "observations are credited as n and carry the information of "
                "n_eff."
            ),
            scale="survey / cluster",
            signature=_SAMPLE_SIZE_SIGNATURE,
        ),
        Instance(
            domain="metrology",
            field_name="correlated systematic uncertainty",
            instrument="covariance matrix over input quantities",
            units="combined standard uncertainty",
            citation=(
                "BIPM JCGM 100:2008 (GUM), clauses on correlated input "
                "quantities; CODATA adjustments carry the full covariance "
                "matrix because measurements sharing a calibration standard "
                "are not independent inputs."
            ),
            scale="instrument / laboratory",
            # No signature: the slot filling for this instance was not
            # supplied and is not transcribable from the citation alone.
            signature=None,
        ),
        Instance(
            domain="measurement language",
            field_name="category weld",
            instrument="component divergence cases per term",
            units="n_cases, divergence span",
            citation=(
                "category-weld/MECHANISM_09.md in this ecosystem. A term "
                "fusing two or more independent quantities into one handle, "
                "where components move to opposite extremes without the "
                "record moving. The channel here is the language, not a bath."
            ),
            scale="term / record",
            signature=None,
        ),
    ),
    scale=(
        "spans device to survey population; the shape is scale-free with "
        "respect to the domains listed"
    ),
    discriminator=(
        "after the omitted coupling is written into the model, does the "
        "credited quantity return? If it returns, the gap was representational "
        "and the case belongs to occupied_set_vs_space. If it does not return, "
        "and only a change to the apparatus recovers it -- separate rails, "
        "split pump, decluster the sample -- the case belongs here. Nearest "
        "rival explanation is that these are one shape and the two directions "
        "are a story told about it; the measurement that separates them is "
        "whether any re-representation restores the credited independence. A "
        "case where it does breaks this entry."
    ),
    status=Status.MULTI_DOMAIN,
    provenance=Provenance.MODEL_SEEDED,
)


ENTRIES = (
    SUPPLY_COUPLED_DRAW,
    OCCUPIED_SET_VS_SPACE,
    INDEPENDENCE_CREDITED_VS_JOINT,
)
