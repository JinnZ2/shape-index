# shape-index

> The searchable unit is the shape, not the vocabulary.

**shape-index** is a small, hand-populated index of structural signatures that recur across domains under different names. It is an instrument to be tested and broken, not a thesis or a position under defense.

Keyword search misses cross-domain matches by construction. A provisioning regime in anthropology, seasonal fodder supplementation in zooarchaeology, and variable coupling in resource-allocation models can describe one structure while sharing no terms, citations, or journals. This repository records the structure directly: what flows, what switches, what gates the switch, what remains constant, and how the shape was measured.

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

## Status values

`CANDIDATE` is an entry not yet supported across domains. `MULTI_DOMAIN` records recurrence across more than one domain. `CONSTRAINT_IDENTIFIED` records an entry whose proposed generating constraint has been argued or asserted. `BROKEN` records a failed shape; broken entries stay in the file because failure is calibration.

## Use

The project uses only the Python standard library and parses under Python 3.9. There is no dependency installation, network call, or build step. Run the tests directly:

```sh
python3 -m unittest -v
```

Matching returns ranked candidates together with the slots that matched. **A high signature overlap is a prompt to check, not a finding. The tool proposes; the reading is done by a person.**

The repository cross-references `uninstrumented/coupling_audit` and the cross-model calibration toolkit as reading locations rather than claiming that those materials have already been incorporated.

## Provenance

The shape, the shape-not-vocabulary cut, and the constraint-generates-shape premise are the author’s. The field names, scoring function, and this write-up are model-generated. Instances are cited sources, not authored claims.

## License

Released to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). See `LICENSE`.
