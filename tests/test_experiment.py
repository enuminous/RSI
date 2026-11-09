import copy
import json
from pathlib import Path
import unittest

from rsi.core import Policy, generate_cases, score
from rsi.experiment import Protocol, hillclimb, null_search, perform


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "configs/protocol-v1.json").read_text())


class ExperimentTests(unittest.TestCase):
    def test_default_protocol_and_budgets(self):
        p = Protocol.from_dict(CONFIG)
        result = perform(p)
        self.assertEqual(len(result["search_trace.json"]["candidate"]), CONFIG["search"]["budget"])
        self.assertEqual(len(result["search_trace.json"]["random_search_null"]), CONFIG["search"]["budget"])
        self.assertEqual(result["report.json"]["claim_status"]["agi"], "NOT_ESTABLISHED")
        self.assertEqual(result["report.json"]["promotion"], "NOT_AUTOMATIC; independent signoff not included")

    def test_deterministic_result(self):
        p = Protocol.from_dict(CONFIG)
        self.assertEqual(perform(p), perform(p))

    def test_frozen_inputs_are_validated(self):
        broken = copy.deepcopy(CONFIG)
        broken["dataset"]["holdout_seed"] = broken["dataset"]["development_seed"]
        with self.assertRaises(ValueError):
            Protocol.from_dict(broken)
        broken = copy.deepcopy(CONFIG)
        broken["status"] = "PROPOSED"
        with self.assertRaises(ValueError):
            Protocol.from_dict(broken)

    def test_hillclimb_never_reduces_development_objective(self):
        cases = generate_cases(128, 12, "dev", "uniform")
        initial = Policy()
        winner, trace = hillclimb(initial, cases, budget=50, seed=123)
        self.assertEqual(len(trace), 50)
        from rsi.experiment import objective
        self.assertGreaterEqual(objective(score(winner, cases)), objective(score(initial, cases)))

    def test_null_budget_is_matched(self):
        cases = generate_cases(128, 12, "dev", "uniform")
        winner, trace = null_search(cases, budget=21, seed=9)
        self.assertEqual(len(trace), 21)
        winner.validate()
