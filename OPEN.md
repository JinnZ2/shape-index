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
