# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

import ast
import os
import unittest

from shape_index.entries import SUPPLY_COUPLED_DRAW
from shape_index.match import MATCH_THRESHOLD, compare, explain, rank_candidates
from shape_index.schema import (
    Instance,
    Provenance,
    ShapeEntry,
    Signature,
    Status,
)


ROOT = os.path.dirname(os.path.abspath(__file__))

CC0_HEADER = "SPDX-License-Identifier: CC0-1.0"
DEDICATION = "This file is dedicated to the public domain under CC0 1.0."

STDLIB_ONLY = frozenset(("ast", "dataclasses", "enum", "os", "typing", "unittest"))

# The package itself is not a dependency; the tests import it by absolute name.
LOCAL = frozenset(("shape_index",))


def _source_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)


def _python_files():
    return [path for path in _source_files() if path.endswith(".py")]


class RepositoryConstraintTests(unittest.TestCase):
    """The repository's stated constraints, enforced rather than asserted."""

    def test_every_file_carries_the_cc0_header(self):
        for path in _source_files():
            if os.path.basename(path) == "LICENSE":
                continue
            with open(path, "r") as handle:
                head = handle.read(400)
            self.assertIn(CC0_HEADER, head, path)
            self.assertIn(DEDICATION, head, path)

    def test_header_appears_once_per_file(self):
        for path in _source_files():
            base = os.path.basename(path)
            if base in ("LICENSE", "test_shape_index.py"):
                continue
            with open(path, "r") as handle:
                body = handle.read()
            self.assertEqual(body.count(DEDICATION), 1, path)

    def test_sources_parse_under_python_39(self):
        for path in _python_files():
            with open(path, "r") as handle:
                source = handle.read()
            try:
                ast.parse(source, filename=path, feature_version=(3, 9))
            except SyntaxError as error:  # pragma: no cover - failure path
                self.fail("%s does not parse under Python 3.9: %s" % (path, error))

    def test_imports_are_standard_library_only(self):
        for path in _python_files():
            with open(path, "r") as handle:
                tree = ast.parse(handle.read(), filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        self.assertIn(root, STDLIB_ONLY | LOCAL, path)
                elif isinstance(node, ast.ImportFrom):
                    if node.level:  # relative, inside the package
                        continue
                    root = (node.module or "").split(".")[0]
                    self.assertIn(root, STDLIB_ONLY | LOCAL, path)


class SeedEntryTests(unittest.TestCase):
    def test_seed_is_model_seeded_and_multi_domain(self):
        self.assertEqual(SUPPLY_COUPLED_DRAW.provenance.value, "MODEL_SEEDED")
        self.assertEqual(SUPPLY_COUPLED_DRAW.status.value, "MULTI_DOMAIN")
        self.assertEqual(len(SUPPLY_COUPLED_DRAW.instances), 3)

    def test_seed_instances_share_no_field_name(self):
        names = set(
            instance.field_name for instance in SUPPLY_COUPLED_DRAW.instances
        )
        self.assertEqual(len(names), len(SUPPLY_COUPLED_DRAW.instances))

    def test_seed_records_a_discriminator(self):
        self.assertTrue(SUPPLY_COUPLED_DRAW.discriminator)


class SchemaTests(unittest.TestCase):
    def test_unstated_constraint_is_allowed(self):
        entry = ShapeEntry(
            shape_id="candidate",
            signature=Signature("flow", "switch", "gate", "constant", "unit"),
            constraint=None,
            constraint_stated=False,
        )
        self.assertIsNone(entry.constraint)

    def test_stated_constraint_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            ShapeEntry(
                shape_id="invalid",
                signature=Signature("flow", "switch", "gate", "constant", "unit"),
                constraint=None,
                constraint_stated=True,
            )


def _entry(shape_id, flows, switches, gated_on, held_constant, units,
           constraint=None, field_name="unnamed"):
    return ShapeEntry.from_instances(
        shape_id=shape_id,
        signature=Signature(flows, switches, gated_on, held_constant, units),
        constraint=constraint,
        constraint_stated=False,
        instances=(
            Instance(
                domain="test",
                field_name=field_name,
                instrument="none",
                units=units,
                citation="none",
                scale="test",
            ),
        ),
        scale="test",
        discriminator="none",
        status=Status.CANDIDATE,
        provenance=Provenance.MODEL_SEEDED,
    )


class MatchTests(unittest.TestCase):
    def test_match_reports_slots_not_only_a_number(self):
        result = compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW)
        self.assertIn("switches", result.matched_slots)
        self.assertIn("gated_on", result.matched_slots)
        self.assertEqual(result.score, 1.0)
        self.assertTrue(result.slots)

    def test_partial_overlap_scores_between_zero_and_one(self):
        left = _entry(
            "left", "dietary calories", "draw magnitude",
            "household surplus availability", "protection", "kcal",
        )
        right = _entry(
            "right", "dietary calories", "draw magnitude",
            "herd surplus availability", "territory", "kcal",
        )
        result = compare(left, right)
        self.assertGreater(result.score, 0.0)
        self.assertLess(result.score, 1.0)
        self.assertIn("switches", result.matched_slots)
        self.assertNotIn("held_constant", result.matched_slots)
        self.assertGreaterEqual(result.overlap("gated_on"), MATCH_THRESHOLD)

    def test_matching_ignores_names_and_ids(self):
        """Different names, same structure, must still match."""
        left = _entry(
            "provisioning_regime", "dietary calories", "draw magnitude",
            "supply availability", "shelter", "kcal",
            field_name="provisioning regime",
        )
        right = _entry(
            "seasonal_foddering", "dietary calories", "draw magnitude",
            "supply availability", "shelter", "kcal",
            field_name="seasonal fodder supplementation",
        )
        self.assertEqual(compare(left, right).score, 1.0)

    def test_same_words_different_switch_and_gate_do_not_match(self):
        """Linguistic similarity is not structural similarity."""
        left = _entry(
            "left", "dietary calories", "draw magnitude",
            "supply availability", "shelter", "kcal",
        )
        right = _entry(
            "right", "dietary calories", "supply availability",
            "draw magnitude", "shelter", "kcal",
        )
        result = compare(left, right)
        self.assertNotIn("switches", result.matched_slots)
        self.assertNotIn("gated_on", result.matched_slots)

    def test_switch_and_gate_outweigh_units(self):
        base = _entry("base", "x", "switch alpha", "gate alpha", "held", "unit")
        structural = _entry("structural", "x", "switch alpha", "gate alpha", "held", "other")
        unit_only = _entry("unit_only", "x", "switch beta", "gate beta", "held", "unit")
        self.assertGreater(
            compare(base, structural).score, compare(base, unit_only).score
        )

    def test_one_sided_constraint_costs_score(self):
        stated = _entry("stated", "x", "s", "g", "h", "u", constraint="rate limit")
        silent = _entry("silent", "x", "s", "g", "h", "u", constraint=None)
        both_silent = _entry("both_silent", "x", "s", "g", "h", "u", constraint=None)
        self.assertEqual(compare(silent, both_silent).score, 1.0)
        self.assertLess(compare(stated, silent).score, 1.0)

    def test_rank_candidates_excludes_the_query_itself(self):
        other = _entry("other", "a", "b", "c", "d", "e")
        ranked = rank_candidates(SUPPLY_COUPLED_DRAW, (SUPPLY_COUPLED_DRAW, other))
        self.assertEqual([result.shape_id for result in ranked], ["other"])

    def test_explain_shows_slots_and_the_guard(self):
        text = explain(compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW))
        self.assertIn("gated_on", text)
        self.assertIn("prompt to check", text)


if __name__ == "__main__":
    unittest.main()
