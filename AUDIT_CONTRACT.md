<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# AUDIT_CONTRACT

How work is reported in this repository. Binding on any reader, human or
model, producing output here. `CLAUDE.md` governs the repository; this
governs the report.

## Purpose

Hold the translation layer count at one.

Mismatch between how this repository's author models a system and how a
language model does is **informative** — it is the diagnostic residual. That
signal survives only at one translation layer. Register-guessing adds layers,
and the added layers make mismatch unattributable: processing difference and
translation artifact become indistinguishable.

The rules below are not presentation preferences. They are the conditions
under which the residual stays readable.

A consequence that runs against the obvious reading of **Output form**:
reporting in the author's register is itself a second layer. Structure first
means show the artifact, not adopt the notation. Mimicry reads as compliance
and suppresses exactly the signal this contract exists to preserve.

## Output form

- Structure first: schema, table, diff, code. Prose only as caption.
- No restating the conclusion in words after showing it.
- No author-profile, working-style, or audience section. Ever. Enforced by
  `test_no_author_profile_or_working_style_section`.

## What counts as an answer

- A claim without a measurement is not an answer. Name what would measure it.
- A score without its support count is not a score. Enforced by
  `MatchResult.support()`; `explain()` prints the count beside every layer
  score and flags the one-slot case.
- Report the failure mode before the fix. "Vocabulary fails visibly" beats
  "vocabulary patched quietly." The record shows the refusal, then the term.
- Gap analysis is deliverable, not preamble: what is missing, what is
  unmeasured, what is asserted versus measured.

## Wording

- Wording is not a decision. Do not ask for wording approval.
- Do not ask which term to use. Pick one, define it, move on.
- Naming disputes are resolved by the definition and the sign or rate, not by
  preference.

## Discriminators

- When two entries score alike, the discriminator is the deliverable.
- A free-text discriminator carrying load is a flagged defect, not a finished
  entry. The structural layer does not read prose; a separation that lives
  only in the discriminator field is a separation the index cannot make.
  Type it or mark the entry defective.

## Cross-model handoff

- Documents brought for audit are often co-produced with another model.
  Separate the layers **before** auditing:

      user contribution   audit this
      model overlay       strip: flattery, invented premises, narrative
                          padding, restated conclusions

- Explanatory prose in those documents is the author explaining to a model,
  not the author's claim. Do not attribute it to her.
- Pasted AI-conversation snippets are not her work and not her voice.
  Voice-dictated while driving produces voice-layer errors, then the other
  model's processing on top. Audit the content on its merits; assign no
  authorship.
- Do not read state, mood, or meaning into typos or brevity. No autocomplete,
  phone, one finger.

## Not requested

- Do not infer motivation, intent, or reasoning from what is reported.
- Markers are exploratory. A repository or an extended chain is "test the
  fit," not a thesis under defence. Respond by testing, extending, or
  reporting where it breaks.
- Confidence is reported separately from the pattern. Take the number as
  given; do not resolve it in either direction. **Downward is still
  resolving**: a hedge is not grounds to withhold the work.
