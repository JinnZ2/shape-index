# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

import unittest

from shape_index.entries import SUPPLY_COUPLED_DRAW
from shape_index.match import compare
from shape_index.schema import ShapeEntry, Signature


class ShapeIndexTests(unittest.TestCase):
    def test_seed_is_model_seeded_and_multi_domain(self):
        self.assertEqual(SUPPLY_COUPLED_DRAW.provenance.value, "MODEL_SEEDED")
        self.assertEqual(SUPPLY_COUPLED_DRAW.status.value, "MULTI_DOMAIN")
        self.assertEqual(len(SUPPLY_COUPLED_DRAW.instances), 3)

    def test_match_reports_slots_not_only_a_number(self):
        result = compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW)
        self.assertIn("switches", result.matched_slots)
        self.assertIn("gated_on", result.matched_slots)
        self.assertEqual(result.score, 1.0)

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


if __name__ == "__main__":
    unittest.main()
