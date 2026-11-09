import unittest
import random

from rsi.core import Case, Label, Policy, generate_cases, mutate, oracle, predict, score


class CoreTests(unittest.TestCase):
    def test_oracle_requires_provenance_and_bridge(self):
        self.assertEqual(oracle(2, 0, False, True), Label.UNRESOLVED)
        self.assertEqual(oracle(2, 0, True, False), Label.UNRESOLVED)
        self.assertEqual(oracle(1, 0, True, True), Label.SUPPORTED)
        self.assertEqual(oracle(0, 1, True, True), Label.CONTRADICTED)
        self.assertEqual(oracle(1, 1, True, True), Label.UNRESOLVED)

    def test_explicit_justification(self):
        case = Case("x", 2, 0, False, True, "UNRESOLVED")
        p = Policy(require_provenance=True)
        label, rationale = predict(p, case)
        self.assertEqual(label, "UNRESOLVED")
        self.assertIn("provenance", rationale)

    def test_policy_validation(self):
        with self.assertRaises(ValueError):
            Policy(support_threshold=0).validate()
        with self.assertRaises(ValueError):
            Policy.from_dict({"require_bridge": True})
        with self.assertRaises(ValueError):
            Policy(conflict_handling="arbitrary").validate()

    def test_generator_determinism_and_partition(self):
        a = generate_cases(256, 7, "dev", "uniform")
        b = generate_cases(256, 7, "dev", "uniform")
        c = generate_cases(256, 8, "holdout", "stress")
        self.assertEqual(a, b)
        self.assertFalse(set(x.case_id for x in a) & set(x.case_id for x in c))

    def test_score_false_assertions(self):
        case = Case("x", 2, 0, False, True, "UNRESOLVED")
        p = Policy(support_threshold=2, contradiction_threshold=2,
                   require_provenance=False, require_bridge=False,
                   conflict_handling="prefer_support")
        metric = score(p, [case])
        self.assertEqual(metric["accuracy"], 0.0)
        self.assertEqual(metric["false_assertion_rate"], 1.0)

    def test_mutations_respect_constraints_and_change_one_gene(self):
        seed = random.Random(123)
        p = Policy()
        for _ in range(200):
            q = mutate(p, seed)
            q.validate()
            changed = [key for key, value in p.as_dict().items()
                       if value != q.as_dict()[key]]
            self.assertEqual(len(changed), 1)
            p = q
