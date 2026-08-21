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
