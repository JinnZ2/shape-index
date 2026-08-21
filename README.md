<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# shape-index

> The searchable unit is the shape, not the vocabulary.

**shape-index** is a small, hand-populated index of structural signatures that recur across domains under different names. It is an instrument to be tested and broken, not a thesis or a position under defense.

Keyword search misses cross-domain matches by construction. A provisioning regime in anthropology, seasonal fodder supplementation in zooarchaeology, and variable coupling in resource-allocation models can describe one structure while sharing no terms, citations, or journals. This repository records the structure directly: what flows, what switches, what the switch is gated on, what remains constant, and how the shape was measured. The switch-and-gate pair is recorded in controlled terms rather than free text, because free text reintroduces the vocabulary problem one level down.

The generating premise is stated as a premise, not a conclusion: where domains are downstream of the same physical constraint—such as conservation, a gradient, a rate limit, or a boundary condition—the admissible geometry may recur even when field vocabulary diverges. The constraint is therefore a first-class field. An unidentified constraint is permitted and remains visibly weaker evidence.

## Contents

| File | Purpose |
| --- | --- |
| `shape_index/schema.py` | Entry, instance, signature, status, and provenance records. |
| `shape_index/match.py` | Explainable field-wise matching; it does not match name strings. |
| `shape_index/entries.py` | One `MODEL_SEEDED` entry: `supply_coupled_draw`. |
| `CANDIDATES.md` | Paths to probable entries awaiting hand-populated write-up. |
| `FALSIFIER.md` | Conditions that break an entry without deleting its failure record. |
| `OPEN.md` | Explicit limits and unanswered questions. |
| `LOG.md` | Dated provenance of the repository opening. |
| `CLAUDE.md` | Working constraints for anyone, human or model, editing this repository. |

## Status values

`CANDIDATE` is an entry not yet supported across domains. `MULTI_DOMAIN` records recurrence across more than one domain. `CONSTRAINT_IDENTIFIED` records an entry whose generating constraint has been **argued**, and the schema enforces that: it requires `constraint_stated=True`. A constraint that is asserted but not argued is recorded on the entry and the entry stays `MULTI_DOMAIN`, unpromoted — `constraint_stated` exists to hold that difference, and folding assertion and argument into one status would discard the field. `BROKEN` records a failed shape; broken entries stay in the file because failure is calibration.

## Use

The project uses only the Python standard library and parses under Python 3.9. There is no dependency installation, network call, or build step. Run the tests directly:

```sh
python3 -m unittest -v
```

Matching scores two layers and reports them separately, never blended into one headline number.

The **structural** layer compares the typed switch-and-gate slots — `gate_type` (`AVAILABILITY`, `DEMAND`, `THRESHOLD`, `PHASE`, `STATE`), `switch_direction` (`INCREASE`, `DECREASE`, `BIDIRECTIONAL`), and `switch_periodicity` (`PERIODIC`, `APERIODIC`) — drawn from a controlled vocabulary, so they are identical or they are not.

The **lexical** layer compares the free-text slots by token overlap. Token overlap inside a slot is still a vocabulary operation: it escapes matching what the fields call the shape and starts matching what the indexer calls the slots. It is scored, labelled as vocabulary, and kept out of the structural claim.

The seed entry is checked against itself across its own domains, and the two layers come apart exactly as the premise predicts:

```
anthropology vs zooarchaeology
  structural=0.7500  lexical=0.0417
  [structural]
    gate_type           match overlap=1.00 shared=AVAILABILITY
    switch_direction    match overlap=1.00 shared=BIDIRECTIONAL
    switch_periodicity        overlap=0.00 left=APERIODIC right=PERIODIC
  [lexical]
    flows                     overlap=0.00 left=calories, dietary
                                           right=foddered, intake, plant
    held_constant             overlap=0.00 left=protection, shelter right=penning
```

Nothing matches on words. The structure matches, and the one structural disagreement — aperiodic household surplus against periodic foddering — is surfaced rather than averaged away. Matching never compares shape ids, field names, citations, or domain labels. `explain()` renders a result slot by slot so a match can be rejected on sight. **A high overlap is a prompt to check, not a finding. The tool proposes; the reading is done by a person.**

The repository cross-references `uninstrumented/coupling_audit` and the cross-model calibration toolkit as reading locations rather than claiming that those materials have already been incorporated.

## Provenance

The shape, the shape-not-vocabulary cut, and the constraint-generates-shape premise are the author’s. The field names, scoring function, and this write-up are model-generated. Instances are cited sources, not authored claims.

## License

Released to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). See `LICENSE`.
