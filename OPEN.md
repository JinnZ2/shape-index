<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# Open questions

Most candidate shapes have no identified constraint. The schema permits `None`; this is honest rather than provisional.

Scale and resolution are untested fields. The claim that holographic, fractal, and branching descriptions are one shape at different sampling resolutions is unverified and remains a question.

Matching currently operates over a hand-populated index of approximately ten entries in the intended future form. This seed repository makes no claim about recall.

Absence of a term in a literature is not absence of the structure. Every null result should record which vocabulary was searched.

The matching threshold is uncalibrated. Slot overlap is scored by token
intersection over union, and the cutoff above which a slot is reported as matched
is a reporting convenience chosen without evidence.

Only the switch-and-gate pair is typed. `flows`, `held_constant`, and `units`
remain free text and are therefore still matched as vocabulary: the seed's own
two instances score 0.00 on every one of them while describing the same
structure. That is why the seed's self-check reaches 0.75 structurally and not
1.00 — the untyped slots contribute nothing. Whether those slots should also be
typed, and by what terms, is open. Typing `flows` by conserved quantity is the
obvious candidate, since conservation is the premise's own example of a
shape-generating constraint, but it has not been tried.

The controlled term lists are model-proposed and untested. `GateType` in
particular — AVAILABILITY, DEMAND, THRESHOLD, PHASE, STATE — is one person's cut
at a taxonomy that ought to come from reading entries, not from writing a schema.
The lists will be wrong in ways that only show up when a shape refuses to fit, and
a shape that refuses to fit is evidence about the list, not about the shape.

The typed slots move the problem rather than dissolving it. Whoever assigns
`gate_type` is doing the reading that the match then reports, so the index records
a judgement, not a measurement. Two people typing the same instance differently is
the test that matters and has not been run.

The gate vocabulary cannot type two of the three entries. `occupied_set_vs_space`
and `independence_credited_vs_joint` are both gated on whether a relation is
represented in the model, and `GateType` has no term for a property of the
representation — AVAILABILITY, DEMAND, THRESHOLD, PHASE and STATE all name
properties of a physical quantity. Both entries therefore carry
`gate_type=UNSPECIFIED`, and the two shapes that most need separating are the
two the typed layer cannot see. A term is needed. It has not been added here
because three entries is a thin basis for a taxonomy decision that changes
every future match, and because the schema's own record should show the
vocabulary failing before it shows it patched.

The consequence is measurable and worse than a gap. With the gate unspecified
on both sides and periodicity unspecified on both, the structural comparison of
those two entries falls through to `switch_direction` alone — where both are
DECREASE — and reports `structural=1.0000`. A perfect structural match resting
on one slot. `MatchResult.support()` and `explain()` now report the slot count
beside the score and flag the one-slot case, so the number can no longer be
read as broad agreement; but the underlying problem is that the index currently
cannot distinguish those two entries at all.

What would distinguish them is not in any typed slot: whether adding the
omitted relation to the model returns the quantity. For
`occupied_set_vs_space` it does and the fix is representational; for
`independence_credited_vs_joint` it does not and the fix is physical. That
distinction is carried only in free-text discriminators, which the structural
layer does not read. Whether it should become a typed slot of its own, or
whether the two entries are one shape and should be merged, is open.

The gate-vocabulary failure recorded above is now patched, and the patch is
itself a claim. `GateType.REPRESENTATION` and the `ClosureMode` slot were added
from three entries — a thin basis, and thinner than the rule that taxonomies
should come from reading entries. The two terms may be wrong in the same way the
original five were: `REPRESENTATION` names an absence of physical gating rather
than a positive kind, and `ClosureMode` has three values chosen to separate two
entries. Both are more likely to break than the terms that have survived
several entries.

What the patch bought is measurable. `independence_credited_vs_joint` against
`occupied_set_vs_space` scored `structural=1.0000 on 1 slot` before it and
`structural=0.6000 on 3 slots` after, with the disagreement in `closure_mode`
where the claim actually sits. What it cost is that a separation which was
visible as a defect is now absorbed into a score, and the next reader will not
see that it was ever in doubt.

`provenance` is one flag per entry and the cross-model handoff section of
`AUDIT_CONTRACT.md` asks for two layers to be separated — user contribution
from model overlay — before an audit begins. The schema cannot record that
separation: an entry is `AUTHORED` or `MODEL_SEEDED` whole. Nothing is
mis-recorded today, because every entry in the index is `MODEL_SEEDED`. The
question is what happens to the first entry where a person supplies the
signature slots and a model supplies the instance list, which is the shape
most of these entries have arrived in. Whether provenance belongs per-slot,
per-instance, or nowhere is open.

An external report predicted structural scores for five candidate shapes
against the index. Four of five did not reproduce:

    left                              right                  predicted   actual
    bottleneck_limited_throughput     supply_coupled_draw     0.67 / 2   0.75 / 3
    threshold_with_memory             supply_coupled_draw     0.25 / 2   0.25 / 3
    failure_containment_by_partition  supply_coupled_draw     0.17 / 2   0.00 / 3
    failure_containment_by_partition  occupied_set_vs_space   0.20 / 3   0.17 / 4
    setpoint_regulation               threshold_with_memory   1.00 / 3   1.00 / 3

The report states the rule correctly — a slot unset on one side scores 0.0 —
and then computes every score as though such a slot were dropped from the
denominator instead of kept in it. Stated rule and applied rule differ, which
is why the slot counts are short by one in four rows out of five. The one row
that reproduces is the one where no slot is one-sided.

That surfaced a defect here, not only there. `supply_coupled_draw` carries
`switch_periodicity=UNSPECIFIED` deliberately, because its own instances
disagree. Every candidate specifies a periodicity, so every comparison against
the seed took a one-sided penalty that reports nothing about either shape.
`bottleneck_limited_throughput` against the seed scored 0.75, and `explain()`
rendered the shortfall exactly as it renders a disagreement — so a pair that
agrees on **every slot both sides fill** looked like a pair with a conflict.
The nearest-rival collision was worse than the score showed, and the
presentation was hiding it. `SlotOverlap.one_sided` and
`MatchResult.abstentions()` now separate abstention from disagreement in the
reporting; the scoring is unchanged, because one-sided evidence should still
cost something. Whether it should is now a question worth asking, and is open:
an entry that honestly abstains is currently penalised against every entry
that commits.

A second finding the report did not reach. Four of its five candidates are
`gate_type=THRESHOLD`, and they score 0.50 to 1.00 against one another —
`setpoint_regulation` against `threshold_with_memory` is 1.0000 on three
slots. THRESHOLD is behaving as a bucket rather than a discriminator, which is
the same failure the original five gate terms had, at a different term. The
report's own question — THRESHOLD versus STATE for bulkheads and membranes —
is a smaller version of this and does not fix it.

An addendum arrived describing the collision between `occupied_set_vs_space`
and `independence_credited_vs_joint` as live: `gate_type` unspecified on both,
structural falling through to `switch_direction` and returning 1.0. That state
is two commits old. `GateType.REPRESENTATION` and `ClosureMode` were added
after the failure was recorded, and the pair now scores 0.6000 on three slots
with the disagreement in `closure_mode`. The addendum's §2 — GateType
deliberately not added — describes the same superseded state. Its proposed
`COLLISION_REGISTER` is not implemented, because a register that surfaces a
discriminator alongside a score is what a typed slot already does, and adding
one would put the same distinction in two places.

What the addendum carries that the schema did not: the discriminator restated
as a **property** rather than a counterfactual. "After the omitted relation is
written into the model, does the credited quantity return?" names a repair
action, which made `ClosureMode` a different KIND of term from every other
typed slot. "Does the omitted relation have a referent outside the formalism?"
is a property of the relation, same kind as the rest. The values map one to
one — REPRESENTATIONAL is NO, PHYSICAL is YES — so the slot was right and its
definition was not. Redefined; the counterfactual is now recorded as a
consequence.

The falsifier that came with it is live and may already have fired. The cut
collapses if a coordinate artifact IS the measurement apparatus, because the
relation is then inside and outside the formalism at once. The category-weld
instance of `independence_credited_vs_joint` is a shared word in the
instrument — a representational object that is also the apparatus doing the
measuring. It is marked as territory in the source table and it is the shape
of the collapse condition. Flagged, not resolved: whether that instance
retires the discriminator and folds the two entries is open, and it is the
single most consequential open question in the index.

Support gating is implemented as proposed. `MatchResult.verdict(layer)`
returns UNRESOLVED below `MIN_SUPPORT = 2` comparable slots, whatever the
score, and `explain()` prints the verdict beside the score. Scoring semantics
are untouched: this reads a score, it does not compute one.
