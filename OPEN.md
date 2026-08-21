<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# Open questions

Most candidate shapes have no identified constraint. The schema permits `None`; this is honest rather than provisional.

Scale and resolution are untested fields. The claim that holographic, fractal, and branching descriptions are one shape at different sampling resolutions is unverified and remains a question.

Matching currently operates over a hand-populated index of approximately ten entries in the intended future form. This seed repository makes no claim about recall.

Absence of a term in a literature is not absence of the structure. Every null result should record which vocabulary was searched.

The matching threshold is uncalibrated. Slot overlap is scored by token
intersection over union, and the cutoff above which a slot is reported as matched
is a reporting convenience chosen without evidence. Token overlap also rewards
shared phrasing, which is the failure mode the index is supposed to avoid: two
entries written by the same hand will score higher than two entries describing the
same structure in unrelated words. Until entries are written by different people,
the score is measuring the indexer as much as the shape.
