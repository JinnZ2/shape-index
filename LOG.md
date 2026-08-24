<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# Log

## 2026-08-21

Repository opened after a live run in which a match was found by shape across two literatures with no shared vocabulary, before any schema existed.

The shape, the shape-not-vocabulary cut, and the constraint-generates-shape premise are the author’s. The field names, scoring function, and this write-up are model-generated. Instances are cited sources, not authored claims.

## 2026-08-21 (later)

First audit of the seed against its own stated constraints. Three defects found
and repaired: the CC0 dedication was duplicated in every Markdown file and was
rendering as a heading; matching compared slots by exact string equality rather
than by field-wise overlap, so any index of separately worded entries would have
scored zero across the board; and `rank_candidates` returned the query as its own
best match.

The constraints are now enforced by the test suite rather than asserted in prose:
CC0 header once per file, standard library only, and every source file parsed with
`ast.parse(..., feature_version=(3, 9))`. Matching gained per-slot overlap
evidence and an `explain()` rendering, and is covered by a test that two entries
with the same structure and different field names must match, alongside one that
two entries with the same words and a transposed switch-and-gate must not.

`CLAUDE.md` added: the working constraints, the entry-writing conventions, and the
things not to build here.

## 2026-08-21 (third)

Review found the matcher was still lexical. Token overlap inside a slot escapes
matching what the fields call the shape and starts matching what the indexer
calls the slots — one level down the same trap. Run against the seed's own two
instrumented instances, worded as anthropology and zooarchaeology would each word
them, the founding example scored 0.0952 against itself, and the only shared token
was the English word "intensity". The repository's own example did not match
itself.

The check could not be run inside the repository at all: instances carried a
citation and an instrument but no slots, so no per-domain filling was ever
recorded and nothing compared one instance to another. A passing suite that never
runs entry-against-entry does not test the thing.

Repaired. `Instance.signature` records each field's own filling of the slots, in
that field's words, and is `None` where a field has no name for the shape.
The switch-and-gate pair is typed: `gate_type`, `switch_direction`,
`switch_periodicity`, from controlled vocabularies. Matching now scores a
structural layer and a lexical layer and reports them separately. The seed against
itself: structural 0.75, lexical 0.04, with the one structural disagreement —
aperiodic household surplus against periodic foddering — surfaced rather than
averaged away.

`CONSTRAINT_IDENTIFIED` now requires `constraint_stated=True`, enforced in the
schema. The status had been documented as covering a constraint "argued or
asserted", which discarded the field that exists to separate those. An asserted
but unargued constraint is recorded and stays `MULTI_DOMAIN`.

Also enforced: no file carries an author-profile or working-style heading.

## 2026-08-22

`AUDIT_CONTRACT.md` added, governing report form rather than repository
content. Audited against the session that produced it: three clauses held,
three were partial, and five had been violated — structure-first, no restating
the conclusion, wording-is-not-a-decision, pick-a-term-and-move-on, and
confidence-reported-separately. The last of these had been violated by treating
a hedge ("it's a shape-index hit, I think") as grounds to withhold the entry.
Resolving a confidence marker downward is still resolving it.

Two clauses generated schema work. `GateType.REPRESENTATION` was added under
"pick one, define it, move on", closing the refusal recorded in the entry
above. `ClosureMode` was added under "a free-text discriminator carrying load
is a flagged defect": the separation between `occupied_set_vs_space` and
`independence_credited_vs_joint` — whether adding the omitted relation returns
the quantity — lived only in prose the structural layer does not read.

Measured effect: the two entries scored `structural=1.0000 on 1 slot` against
each other before, and `structural=0.6000 on 3 slots` after, with the
disagreement carried in `closure_mode`. `closure_mode` is weighted equal to
`gate_type`, so the discriminating slot cannot be outvoted by the slots that
agree. Tests 33 to 39.

## 2026-08-22 (second)

`AUDIT_CONTRACT.md` gained a Purpose statement and a Cross-model handoff
section. Audited against the session that produced them: four violations, one
clause held.

The Purpose clause names what the rules are for — holding the translation
layer count at one, so that mismatch between the author's model of a system
and a language model's stays attributable. Under it, the previous report is a
violation: it was written in the author's telegraphic register, reading
"structure first" as *adopt the notation* rather than *show the artifact*.
Mimicry reads as compliance and adds the second layer the clause exists to
prevent. The consequence is now written into the contract beside the clause it
qualifies.

The handoff section produced a correction in `qrng-pair-search/` in the
Simulators repository. That folder audited a co-produced document as a single
layer and attributed its prose to a person — "the drop itself names", "the
delivered drop stated". Material arriving co-produced cannot have its layers
separated from inside the folder, so crediting either a claim or a mistake to
an author requires knowing which layer produced it. The content audit is
unchanged: the prose names a failure mode, the table contradicts it, and the
table is what a verdict is computed from. The attribution was removed rather
than reassigned.

Not built, recorded as a gap: `provenance` is one flag per entry, so the
schema cannot record that one slot came from a user contribution and another
from a model overlay. The handoff section assumes those layers are separable;
the schema assumes they are not. Three entries is too thin a basis to add a
per-slot provenance field, and every entry in the index is currently
`MODEL_SEEDED`, so nothing is presently mis-recorded.

## 2026-08-22 (third)

An external co-produced report proposed five candidate shapes with predicted
structural scores. The predictions were run against the matcher rather than
read: four of five do not reproduce. The report states the one-sided rule
correctly and then computes as though the opposite rule applied.

The run surfaced a local defect. `explain()` rendered a one-sided slot — one
side filled, the other unset — identically to a slot where the two sides
disagree. `bottleneck_limited_throughput` against `supply_coupled_draw` agrees
on every slot both sides fill and scores 0.75, and the shortfall read as a
conflict. `SlotOverlap.one_sided` and `MatchResult.abstentions()` now separate
the two in the report; scoring is unchanged.

No entries added. Several citations in the report are not usable as given —
a trade website as a source, a PMC identifier with no authors, a PMC number
outside the plausible range for its year, two 2026 references uncheckable from
the printed terms. Instances are cited sources; the gate holds.

The report's about-the-author section was not carried into the repository. It
is barred by CLAUDE.md and by AUDIT_CONTRACT.md, and its content is inferred
rather than reported.

## 2026-08-22 (fourth)

`AUDIT_CONTRACT.md` replaced with the delivered version and installed in the
Simulators repository as well, referenced from both `CLAUDE.md` files. Two new
clauses caught committed work.

**Selection and substrate** — absence of a legible reason for a mechanism is
not evidence of absence of reason. `qrng-pair-search/` had read a bath
assignment as a dropped term. Measured, the readout baths are identical across
all seven sources, so they are a constant and the pair partition is unchanged
by including them. A table built to rank pairs has a reason to carry the
discriminating set and drop the constant. The correction was withdrawn and
narrowed to the verdict word.

**Wording** — a defined technical term with a formal definition and a
sign/rate is a measurement term. "Hide the entropy in the correlation rule"
had been audited only as a secret algorithm, where the Kerckhoffs objection
holds. Read as a secret seed it names a seeded extractor, a standard
construction where the seed is key material. That reading was not recovered.

Both violations have the same shape as `occupied_set_vs_space`: a formalism
carrying a variable the system does not, and an omission read as an error when
it was a term correctly dropped. The index has an entry for it.

## 2026-08-22 (fifth)

An OPEN.md addendum arrived. Checked against the repository before installing:
sections 1 and 2 describe a state two commits old, section 5 restates a
correction this repository withdrew after measuring it, and sections 3 and 4
are live.

Installed. `ClosureMode` restated from a counterfactual to a property — "does
the omitted relation have a referent outside the formalism?" — which makes it
the same kind of term as every other typed slot instead of one that names a
repair action. Values unchanged and mapping one to one. Its falsifier is
recorded and may already have fired on the category-weld instance.

Support gating added: `verdict(layer)` returns UNRESOLVED below two comparable
slots regardless of score. Scoring untouched.

Section 5 was right about the object and wrong about the level, and so was the
withdrawal. The readout chain discriminates, but only as a property of the
deployment — which elements two legs share — not as a property of a source.
Corrected in the Simulators repository; three readings of that field are left
in its record.

Tests 41 to 44.

## 2026-08-22 (sixth)

`SHAPE_SPEC.md` installed in this repository and in Simulators, referenced from
both `CLAUDE.md` files. It defines SHAPE as the constraint set a geometry is a
solution to, and the index was audited against its section 10 rather than
filed alongside it.

The index does not meet the spec. No entry carried a removal test and the
schema had no field for one, so `removal_test` and `EntryKind` were added and
all three entries classify as `GEOMETRY_NOTE`. Zero shape entries, asserted by
test. The field exists so the count can be taken; filling it is a separate
piece of work and inventing removal tests to clear the count would be the
thing the spec is written against.

Section 2's blocked misread describes `match.py`. The structural layer
compares gate and switch descriptors, which are geometry, and the constraint
is scored as vocabulary in the lexical layer. Two entries can therefore match
structurally with no shared constraint at all. Recorded in OPEN.md with a test
pinning the current split, not restructured: comparing constraints by identity
needs a controlled vocabulary for constraints, and the gate vocabulary took
three entries and two revisions to yield one usable term.

Tests 44 to 49.

## 2026-08-22 (seventh)

`METHOD_SPEC.md` installed in both repositories and wired into both `CLAUDE.md`
files ahead of `SHAPE_SPEC.md`, per its own section 6 ordering.

Audited rather than filed. Section 1's blocked misapplication was checked
against committed text and not found: the only falsifier demand in the
ecosystem is on `custody-verification-band`'s B7, which is an individual read,
where section 1 says such demands belong.

Section 5 conflicts with `MULTI_DOMAIN`. Instance count without a checked
constraint set is not an upgrade, and instance count is the whole definition of
that status. All three entries hold it on that basis with no removal test.
Pinned by test, not resolved.

Section 5's confidence readout was absent from the schema entirely.
`confidence` and `comfort_threshold` added, range-validated, and left `None` on
every entry — a gradient nobody stated is not a gradient of zero.

`READING_PROTOCOL.md` is now referenced from four places across the two spec
files and exists in neither repository.

Tests 49 to 53.
