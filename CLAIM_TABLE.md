<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# CLAIM TABLE — shape-index

Every repo in this ecosystem carries one; this repository did not until now,
and 23 folders in the Simulators repository already did. `READING_PROTOCOL.md`
states the refutation protocol these claims run under.

## REFUTATION PROTOCOL

A break is a measurement, not an objection to be answered. When a claim is
refuted the claim gets updated. **The code does not get retuned to preserve
it.** Claims here are about the instrument, not about the world — this
repository indexes shapes, and the shapes' own claims live in their entries.

---

**S1.** The seed entry matches itself structurally across its instrumented
instances and does not match itself lexically.

*Falsifier:* lexical overlap rising to meet structural, or structural falling
below `MATCH_THRESHOLD`, across the same two instances.

*Status:* SUPPORTED, measured. `structural=0.75 lexical=0.04` for anthropology
against zooarchaeology. This is the case the index exists for and the only one
in it.

---

**S2.** The original five `GateType` terms could not type two of the three
entries, because all five named properties of a physical quantity and the gate
in question is a property of the representation.

*Falsifier:* a reading of `occupied_set_vs_space` or
`independence_credited_vs_joint` under `AVAILABILITY`, `DEMAND`, `THRESHOLD`,
`PHASE` or `STATE` that a second reader accepts.

*Status:* SUPPORTED, then patched with `REPRESENTATION`. The patch rests on
three entries, which is thinner than the rule that taxonomies come from
reading entries.

---

**S3.** A layer score resting on one comparable slot cannot distinguish
agreement from there being nothing to disagree about.

*Falsifier:* a use in which `structural=1.0` on one slot and on three slots
warrant the same action.

*Status:* SUPPORTED. `MIN_SUPPORT = 2`; `verdict()` returns `UNRESOLVED` below
it. Scoring unchanged — the guard reads a score, it does not compute one.

---

**S4.** The structural layer compares the geometry, not the constraint.

*Falsifier:* showing that `gate_type`, `closure_mode`, `switch_direction` and
`switch_periodicity` are constraint descriptions rather than descriptions of
the geometry.

*Status:* SUPPORTED and **UNFIXED.** `SHAPE_SPEC` section 1 says the shape IS
the constraint set and the geometry is only its readout; section 2 names
"matching geometries across domains" as the failure mode. The constraint is
scored in the lexical layer by token overlap at weight 1.5, so two entries can
take a full structural match with no shared constraint at all. Pinned by test.
The largest open question here.

---

**S5.** No entry in the index is a shape entry.

*Falsifier:* an entry carrying a removal test — which constraint, if removed,
changes the geometry, plus a case where it is genuinely absent and the form
differs.

*Status:* SUPPORTED. Three of three are `GEOMETRY_NOTE` per `SHAPE_SPEC`
section 10, asserted by test. The field was added so the count could be taken.

---

**S6.** `MULTI_DOMAIN` upgrades an entry on instance count alone.

*Falsifier:* a reading of that status that does not reduce to counting
domains.

*Status:* SUPPORTED and **UNRESOLVED.** `METHOD_SPEC` section 5 says a read is
not upgraded by more instances sharing the geometry without a checked
constraint set. All three entries hold `MULTI_DOMAIN` on 3, 7 and 5 instances,
with no removal test. Pinned by test rather than fixed, so the conflict is
visible before it is resolved.

---

**S7.** A slot filled on one side and unset on the other penalises an entry
that abstains against every entry that commits.

*Falsifier:* an argument that abstention should cost exactly what disagreement
costs.

*Status:* SUPPORTED as arithmetic; the design question is open. `one_sided`
and `abstentions()` separate the two in the reporting. Scoring is unchanged,
because one-sided evidence should still cost something — whether that is right
is in `OPEN.md`.

---

**S8.** `occupied_set_vs_space` and `independence_credited_vs_joint` are two
shapes, not one.

*Falsifier:* supplied by `ClosureMode`'s own definition — the map/territory cut
collapses if a coordinate artifact IS the measurement apparatus, because the
relation is then inside and outside the formalism at once.

*Status:* SUPPORTED by `closure_mode`, and **the falsifier may already have
fired.** The `category-weld` instance of `independence_credited_vs_joint` is a
shared word in the instrument: a representational object that is also the
apparatus doing the measuring. Flagged, not resolved. If it fires, the two
entries fold and `S8` is refuted rather than defended.

---

**S9.** *Withdrawn.* An earlier claim held that the seed's structural
self-match rested on three comparable slots. It rests on two: the seed's
entry-level `switch_periodicity` is deliberately `UNSPECIFIED` because its own
instances disagree, and unspecified on both sides is incomparable rather than
agreed. The test asserting three was the thing that was wrong.
