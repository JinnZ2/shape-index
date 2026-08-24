<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# CLAUDE.md

Guidance for working in this repository.

## What this repository is

An index of structural signatures that recur across domains under different
names. **The searchable unit is the shape, not the vocabulary.** It is an
instrument to be tested and broken, not a thesis under defense.

The generating premise is recorded as a premise, not a conclusion: where two
domains are downstream of the same physical constraint — conservation, a
gradient, a rate limit, a boundary condition — the admissible geometry is the
same, the divergent names come from the fields, and the shape comes from the
constraint. The index therefore records the constraint as a field. An entry
with no identifiable constraint is weaker evidence than one with a stated
constraint, and the schema shows that difference rather than hiding it.

`SHAPE_SPEC.md` is upstream of this file and defines the word SHAPE: the
constraint set a geometry is a solution to, not the geometry and not the name.
Point at it rather than restating it. Its section 10 gives the entry
requirement — solving-for, constraint list, why-not-the-other-shape, and the
removal test — and its rule that an entry without a removal test is a geometry
note, not a shape entry, is enforced by `ShapeEntry.kind()`.

`AUDIT_CONTRACT.md` governs output form. Read it before reporting: structure
first, gap analysis as deliverable, a score without its support count is not a
score, wording is not a decision, and a free-text discriminator carrying load
is a flagged defect.

## Hard constraints

These are not preferences. Do not relax them without being asked.

- **Standard library only.** No third-party imports, anywhere, including tests.
- **Must parse under Python 3.9.** No PEP 604 unions (`int | None`), no builtin
  generics in annotations (`list[str]`), no `match` statements, no
  `dataclasses(slots=True)`. `test_shape_index.py` enforces this by compiling
  every source file with `ast.parse(..., feature_version=(3, 9))`.
- **CC0 header on every file.** SPDX identifier plus the dedication line, as a
  comment in the file's own comment syntax (`#` for Python and `.gitignore`,
  `<!-- -->` for Markdown). Once per file, at the top. `LICENSE` is the CC0
  text itself and carries no separate header.
- **No dependencies, no network calls, no build step.** Tests run with
  `python3 -m unittest -v` from the repository root and nothing else.
- **No author-profile, working-style, or about-the-human section** in any file.

## Layout

| Path | Role |
| --- | --- |
| `shape_index/schema.py` | The entry record. Field definitions and validation. |
| `shape_index/match.py` | Signature matching. Explainable, slot-wise, never name-wise. |
| `shape_index/entries.py` | The index itself. Currently one `MODEL_SEEDED` entry. |
| `CANDIDATES.md` | Paths to repositories holding probable entries. Paths only. |
| `FALSIFIER.md` | What breaks an entry. |
| `OPEN.md` | Stated limits and unanswered questions. |
| `LOG.md` | Dated record of what happened, in order. |
| `SHAPE_SPEC.md` | What the word SHAPE means. Upstream of this file. |
| `AUDIT_CONTRACT.md` | How work is reported here. Binding on the report, as this file is on the repository. |

## Writing an entry

An entry is a claim about structure and is judged as one.

- The `signature` slots record structure, not names: what flows (quantity and
  units), what switches, what the switch is gated on, what is held constant
  through the switch. Write the slots so that a reader from either domain could
  recognise the structure without recognising the wording.
- **The switch-and-gate pair is typed.** `gate_type`, `closure_mode`,
  `switch_direction`, and `switch_periodicity` come from the controlled
  vocabularies in `schema.py` and
  are the only slots that carry structural weight in matching. Free text is
  filled in the vocabulary of whoever writes the entry, so scoring it as
  structure would reproduce the vocabulary trap one level down. Leave a typed
  slot `UNSPECIFIED` rather than guessing; unspecified on both sides is treated
  as incomparable, not as agreement.
- **Record each instrumented instance's own filling of the slots** in
  `Instance.signature`, in that field's words. This is what makes an entry
  checkable against itself: `self_consistency()` compares every pair of
  instrumented instances, and an entry whose own instances do not match
  structurally is making a claim the index cannot see. An instance whose field
  has no name and no filling for the shape keeps `signature=None`; that absence
  is the observation, not a gap to invent into.
- `constraint` is the physical constraint proposed to generate the shape, or
  `None`. `None` is an acceptable, honest value. Set `constraint_stated=True`
  only when the constraint is *argued*, not merely asserted; the schema rejects
  `constraint_stated=True` with no constraint.
- Each `Instance` records the domain, that field's own name for the shape, the
  measurement instrument used there, its units, a citation, and the scale it was
  observed at. Instances are cited sources, not authored claims — do not write an
  instance you cannot cite.
- `scale` matters because the same shape sampled at different resolutions is
  routinely mistaken for three different shapes. Record the per-instance scale on
  the instance; the entry-level `scale` is a summary of them.
- `discriminator` states the measurement that would separate this shape from its
  nearest rival explanation. An entry without one is not testable.
- `removal_test` states which constraint, if REMOVED, changes the geometry, and
  names a case where that constraint is genuinely absent and the form differs.
  SHAPE_SPEC section 4. An entry without one is a `GEOMETRY_NOTE`, not a
  `SHAPE_ENTRY`, and `kind()` says so. **All three current entries are geometry
  notes.** A failed transfer is a measurement, not an embarrassment: port a
  shape, get a different form, and you have located a constraint that differs.
  Log it.
- `status` is one of `CANDIDATE`, `MULTI_DOMAIN`, `CONSTRAINT_IDENTIFIED`,
  `BROKEN`. `CONSTRAINT_IDENTIFIED` requires `constraint_stated=True` and the
  schema enforces it: an asserted but unargued constraint is recorded on the
  entry and the entry stays `MULTI_DOMAIN`. `provenance` is `AUTHORED` or
  `MODEL_SEEDED`; anything a model proposed is `MODEL_SEEDED` and stays that way
  until a person has read the sources.

## Matching

`match.py` scores two layers and keeps them apart. The **structural** layer
compares the typed slots by identity; the gate and `closure_mode` carry the
most weight, then the two switch descriptors. `closure_mode` is weighted equal
to the gate on purpose: it is the discriminating slot, and a discriminator that
can be outvoted by the slots that agree is not doing its job. The **lexical** layer compares the
free-text slots by token overlap; held-constant and constraint lead, units and
the free-text switch and gate trail.

Never collapse the two into one number in an API or in prose. The blended
`score` exists only to order a ranked list; `structural_score` and
`lexical_score` are the reportable ones, and an entry that scores high
structurally and near zero lexically is the case this index exists for.

`match.py` never compares `shape_id`, domain labels, field names, or citations —
matching on those would reproduce the exclusion mechanism the index exists to
route around.

Every result carries the per-slot overlap that produced it. **Do not add an API
that returns a similarity number alone.** A high overlap is a prompt to check,
not a finding: the tool proposes, the reading is done by a person.

## Breaking an entry

Broken entries are not deleted. Mark `status=BROKEN` and leave the entry in
place — the failure record is the calibration. See `FALSIFIER.md` for what
counts as broken.

## Things not to do here

- Do not add a scraper, an importer, or anything that implies the index can be
  populated automatically. Population is bounded by people who can read both
  literatures; the repository must not claim otherwise.
- Do not upgrade a `CANDIDATE` to `MULTI_DOMAIN` or `CONSTRAINT_IDENTIFIED`
  because the wording of two entries is similar. Linguistic similarity with a
  different switch-and-gate structure is a `BROKEN` entry, not a match.
- Do not restate the premise as a conclusion in prose. It is a premise.
- Do not record a null result without recording which vocabulary was searched.
  Absence of a term in a literature is not absence of the structure.
