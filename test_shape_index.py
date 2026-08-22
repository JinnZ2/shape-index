# SPDX-License-Identifier: CC0-1.0
# This file is dedicated to the public domain under CC0 1.0.

import ast
import os
import re
import unittest

from shape_index.entries import (
    INDEPENDENCE_CREDITED_VS_JOINT,
    OCCUPIED_SET_VS_SPACE,
    SUPPLY_COUPLED_DRAW,
)
from shape_index.match import (
    MATCH_THRESHOLD,
    STRUCTURAL_WEIGHTS,
    compare,
    compare_signatures,
    explain,
    rank_candidates,
    self_consistency,
)
from shape_index.schema import (
    ClosureMode,
    GateType,
    Instance,
    Provenance,
    ShapeEntry,
    Signature,
    Status,
    SwitchDirection,
    SwitchPeriodicity,
)


ROOT = os.path.dirname(os.path.abspath(__file__))

CC0_HEADER = "SPDX-License-Identifier: CC0-1.0"
DEDICATION = "This file is dedicated to the public domain under CC0 1.0."

STDLIB_ONLY = frozenset(
    ("ast", "dataclasses", "enum", "os", "re", "typing", "unittest")
)

# The package itself is not a dependency; the tests import it by absolute name.
LOCAL = frozenset(("shape_index",))

# Headings that would introduce an author profile or a working-style section.
_PROFILE_HEADING = re.compile(
    r"^#{1,6}\s+.*\b(about\s+(me|the\s+human|the\s+author)|author|"
    r"working\s+style|who\s+i\s+am|profile|bio)\b",
    re.IGNORECASE | re.MULTILINE,
)


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

    def test_no_author_profile_or_working_style_section(self):
        for path in _source_files():
            if not path.endswith(".md"):
                continue
            if os.path.basename(path) == "test_shape_index.py":
                continue
            with open(path, "r") as handle:
                body = handle.read()
            found = _PROFILE_HEADING.findall(body)
            self.assertEqual(found, [], "%s: %s" % (path, found))


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

    def test_uninstrumented_instance_has_no_invented_signature(self):
        by_domain = dict(
            (instance.domain, instance) for instance in SUPPLY_COUPLED_DRAW.instances
        )
        self.assertIsNone(by_domain["resource-allocation models"].signature)
        self.assertEqual(len(SUPPLY_COUPLED_DRAW.instrumented_instances()), 2)


class SelfConsistencyTests(unittest.TestCase):
    """The founding example, run against itself across its own domains.

    A suite that never compares one instance's slot filling to another's does
    not test the thing the repository claims.
    """

    def test_seed_has_a_pair_to_check(self):
        self.assertEqual(len(self_consistency(SUPPLY_COUPLED_DRAW)), 1)

    def test_seed_matches_itself_structurally(self):
        (_, _, result) = self_consistency(SUPPLY_COUPLED_DRAW)[0]
        self.assertGreaterEqual(result.structural_score, MATCH_THRESHOLD)
        self.assertIn("gate_type", result.matched_slots)
        self.assertIn("switch_direction", result.matched_slots)

    def test_seed_does_not_match_itself_lexically(self):
        """Zero shared vocabulary is the case the index exists for."""
        (_, _, result) = self_consistency(SUPPLY_COUPLED_DRAW)[0]
        self.assertLess(result.lexical_score, 0.1)
        for slot in ("flows", "gated_on", "held_constant", "units"):
            self.assertEqual(result.overlap(slot), 0.0, slot)

    def test_structural_layer_beats_lexical_layer_on_the_seed(self):
        (_, _, result) = self_consistency(SUPPLY_COUPLED_DRAW)[0]
        self.assertGreater(result.structural_score, result.lexical_score * 5)

    def test_periodicity_disagreement_is_surfaced_not_hidden(self):
        (_, _, result) = self_consistency(SUPPLY_COUPLED_DRAW)[0]
        self.assertEqual(result.overlap("switch_periodicity"), 0.0)
        self.assertNotIn("switch_periodicity", result.matched_slots)


class DiscriminatorTests(unittest.TestCase):
    """The two entries the free-text discriminator was separating alone."""

    def test_both_entries_type_under_the_representation_gate(self):
        self.assertEqual(OCCUPIED_SET_VS_SPACE.signature.gate_type,
                         GateType.REPRESENTATION)
        self.assertEqual(INDEPENDENCE_CREDITED_VS_JOINT.signature.gate_type,
                         GateType.REPRESENTATION)

    def test_closure_mode_carries_the_separation(self):
        self.assertEqual(OCCUPIED_SET_VS_SPACE.signature.closure_mode,
                         ClosureMode.REPRESENTATIONAL)
        self.assertEqual(INDEPENDENCE_CREDITED_VS_JOINT.signature.closure_mode,
                         ClosureMode.PHYSICAL)

    def test_the_two_entries_no_longer_score_identical(self):
        result = compare(INDEPENDENCE_CREDITED_VS_JOINT, OCCUPIED_SET_VS_SPACE)
        self.assertLess(result.structural_score, 1.0)
        self.assertGreater(result.support("structural"), 1)
        self.assertNotIn("closure_mode", result.matched_slots)
        self.assertIn("gate_type", result.matched_slots)

    def test_closure_mode_is_weighted_like_the_gate(self):
        """The discriminating slot cannot be outvoted by the agreeing ones."""
        self.assertEqual(STRUCTURAL_WEIGHTS["closure_mode"],
                         STRUCTURAL_WEIGHTS["gate_type"])

    def test_closure_mode_alone_can_split_an_otherwise_identical_pair(self):
        base = dict(direction=SwitchDirection.DECREASE,
                    gate=GateType.REPRESENTATION)
        left = _signature("a", "b", "c", "d", "e",
                          closure=ClosureMode.REPRESENTATIONAL, **base)
        right = _signature("a", "b", "c", "d", "e",
                           closure=ClosureMode.PHYSICAL, **base)
        same = _signature("a", "b", "c", "d", "e",
                          closure=ClosureMode.REPRESENTATIONAL, **base)
        self.assertEqual(compare_signatures(left, same).structural_score, 1.0)
        self.assertLess(compare_signatures(left, right).structural_score, 1.0)

    def test_unspecified_closure_stays_incomparable(self):
        left = _signature("a", "b", "c", "d", "e")
        right = _signature("a", "b", "c", "d", "e")
        self.assertEqual(compare_signatures(left, right).layer("structural"), ())


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

    def test_constraint_identified_requires_an_argued_constraint(self):
        """Asserted is not argued; constraint_stated exists to separate them."""
        with self.assertRaises(ValueError):
            ShapeEntry(
                shape_id="asserted_only",
                signature=Signature("flow", "switch", "gate", "constant", "unit"),
                constraint="a rate limit, asserted without argument",
                constraint_stated=False,
                status=Status.CONSTRAINT_IDENTIFIED,
            )

    def test_asserted_constraint_stays_multi_domain(self):
        entry = ShapeEntry(
            shape_id="asserted_only",
            signature=Signature("flow", "switch", "gate", "constant", "unit"),
            constraint="a rate limit, asserted without argument",
            constraint_stated=False,
            status=Status.MULTI_DOMAIN,
        )
        self.assertEqual(entry.status, Status.MULTI_DOMAIN)
        self.assertTrue(entry.constraint)

    def test_argued_constraint_may_be_promoted(self):
        entry = ShapeEntry(
            shape_id="argued",
            signature=Signature("flow", "switch", "gate", "constant", "unit"),
            constraint="a rate limit, argued from the transport equation",
            constraint_stated=True,
            status=Status.CONSTRAINT_IDENTIFIED,
        )
        self.assertEqual(entry.status, Status.CONSTRAINT_IDENTIFIED)


def _signature(flows, switches, gated_on, held_constant, units,
               direction=SwitchDirection.UNSPECIFIED,
               periodicity=SwitchPeriodicity.UNSPECIFIED,
               gate=GateType.UNSPECIFIED,
               closure=ClosureMode.UNSPECIFIED):
    return Signature(
        flows, switches, gated_on, held_constant, units, direction,
        periodicity, gate, closure,
    )


def _entry(shape_id, signature, constraint=None, field_name="unnamed"):
    return ShapeEntry.from_instances(
        shape_id=shape_id,
        signature=signature,
        constraint=constraint,
        constraint_stated=False,
        instances=(
            Instance(
                domain="test",
                field_name=field_name,
                instrument="none",
                units=signature.units,
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
        self.assertIn("gate_type", result.matched_slots)
        self.assertIn("switches", result.matched_slots)
        self.assertIn("gated_on", result.matched_slots)
        self.assertEqual(result.score, 1.0)
        self.assertTrue(result.slots)

    def test_layers_are_reported_separately(self):
        result = compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW)
        self.assertTrue(result.layer("structural"))
        self.assertTrue(result.layer("lexical"))
        self.assertEqual(result.structural_score, 1.0)
        self.assertEqual(result.lexical_score, 1.0)

    def test_partial_overlap_scores_between_zero_and_one(self):
        left = _signature(
            "dietary calories", "draw magnitude", "household surplus availability",
            "protection", "kcal",
        )
        right = _signature(
            "dietary calories", "draw magnitude", "herd surplus availability",
            "territory", "kcal",
        )
        result = compare_signatures(left, right)
        self.assertGreater(result.score, 0.0)
        self.assertLess(result.score, 1.0)
        self.assertIn("switches", result.matched_slots)
        self.assertNotIn("held_constant", result.matched_slots)
        self.assertGreaterEqual(result.overlap("gated_on"), MATCH_THRESHOLD)

    def test_matching_ignores_names_and_ids(self):
        """Different names, same structure, must still match."""
        common = ("dietary calories", "draw magnitude", "supply availability",
                  "shelter", "kcal")
        left = _entry("provisioning_regime", _signature(*common),
                      field_name="provisioning regime")
        right = _entry("seasonal_foddering", _signature(*common),
                       field_name="seasonal fodder supplementation")
        self.assertEqual(compare(left, right).score, 1.0)

    def test_no_shared_vocabulary_still_matches_on_typed_slots(self):
        """The whole point: zero token overlap, same structure."""
        left = _signature(
            "dietary calories", "provisioning intensity", "household surplus",
            "shelter", "n.a.",
            SwitchDirection.BIDIRECTIONAL, SwitchPeriodicity.APERIODIC,
            GateType.AVAILABILITY,
        )
        right = _signature(
            "foddered plant intake", "supplementation rate", "forage abundance",
            "penning", "permil d13C",
            SwitchDirection.BIDIRECTIONAL, SwitchPeriodicity.APERIODIC,
            GateType.AVAILABILITY,
        )
        result = compare_signatures(left, right)
        self.assertEqual(result.structural_score, 1.0)
        self.assertEqual(result.lexical_score, 0.0)

    def test_same_words_different_switch_and_gate_do_not_match(self):
        """Linguistic similarity is not structural similarity."""
        left = _signature(
            "dietary calories", "draw magnitude", "supply availability",
            "shelter", "kcal",
            gate=GateType.AVAILABILITY,
        )
        right = _signature(
            "dietary calories", "supply availability", "draw magnitude",
            "shelter", "kcal",
            gate=GateType.DEMAND,
        )
        result = compare_signatures(left, right)
        self.assertNotIn("gate_type", result.matched_slots)
        self.assertNotIn("switches", result.matched_slots)
        self.assertNotIn("gated_on", result.matched_slots)
        self.assertEqual(result.structural_score, 0.0)

    def test_typed_gate_outweighs_units(self):
        base = _signature("x", "s", "g", "h", "unit", gate=GateType.AVAILABILITY)
        structural = _signature("x", "s", "g", "h", "other", gate=GateType.AVAILABILITY)
        unit_only = _signature("x", "s", "g", "h", "unit", gate=GateType.DEMAND)
        self.assertGreater(
            compare_signatures(base, structural).score,
            compare_signatures(base, unit_only).score,
        )

    def test_one_sided_constraint_costs_score(self):
        signature = _signature("x", "s", "g", "h", "u")
        stated = _entry("stated", signature, constraint="rate limit")
        silent = _entry("silent", signature, constraint=None)
        both_silent = _entry("both_silent", signature, constraint=None)
        self.assertEqual(compare(silent, both_silent).score, 1.0)
        self.assertLess(compare(stated, silent).score, 1.0)

    def test_unspecified_typed_slots_are_not_scored_as_agreement(self):
        left = _signature("x", "s", "g", "h", "u")
        right = _signature("x", "s", "g", "h", "u")
        result = compare_signatures(left, right)
        self.assertEqual(result.layer("structural"), ())
        self.assertEqual(result.structural_score, 0.0)

    def test_rank_candidates_excludes_the_query_itself(self):
        other = _entry("other", _signature("a", "b", "c", "d", "e"))
        ranked = rank_candidates(SUPPLY_COUPLED_DRAW, (SUPPLY_COUPLED_DRAW, other))
        self.assertEqual([result.shape_id for result in ranked], ["other"])

    def test_support_reports_how_many_slots_a_layer_rests_on(self):
        # Two, not three: the seed's entry-level switch_periodicity is
        # deliberately UNSPECIFIED because its own instances disagree on it,
        # and unspecified on both sides is incomparable rather than agreed.
        result = compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW)
        self.assertEqual(result.support("structural"), 2)
        self.assertEqual(
            result.support("lexical"), len(result.layer("lexical")))
        self.assertEqual(result.support("nonexistent"), 0)

    def test_a_one_slot_structural_score_is_flagged_in_explain(self):
        """1.0 on one slot and 1.0 on three slots are not the same evidence."""
        left = _signature("a", "b", "c", "d", "e",
                          direction=SwitchDirection.DECREASE)
        right = _signature("v", "w", "x", "y", "z",
                           direction=SwitchDirection.DECREASE)
        result = compare_signatures(left, right)
        self.assertEqual(result.structural_score, 1.0)
        self.assertEqual(result.support("structural"), 1)
        self.assertIn("ONE slot", explain(result))

    def test_a_multi_slot_structural_score_is_not_flagged(self):
        result = compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW)
        self.assertGreater(result.support("structural"), 1)
        self.assertNotIn("ONE slot", explain(result))

    def test_explain_shows_both_layers_and_the_guard(self):
        text = explain(compare(SUPPLY_COUPLED_DRAW, SUPPLY_COUPLED_DRAW))
        self.assertIn("structural", text)
        self.assertIn("lexical", text)
        self.assertIn("gate_type", text)
        self.assertIn("prompt to check", text)


if __name__ == "__main__":
    unittest.main()
