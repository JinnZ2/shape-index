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
