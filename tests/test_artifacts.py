import json
from pathlib import Path
import unittest

from rsi.io import verify_run

ROOT = Path(__file__).resolve().parents[1]


class ArtifactTests(unittest.TestCase):
    def test_frozen_example_replay_integrity(self):
        result = verify_run(ROOT / 'examples/frozen_demo', ROOT)
        self.assertEqual(result['status'], 'PASS', result['problems'])

    def test_evidence_ledger_sources_exist(self):
        data = json.loads((ROOT / 'docs/evidence-ledger.json').read_text())
        allowed = {'PROPOSED','DERIVED','SIMULATED','OBSERVED',
                   'REPLICATED','CONTRADICTED','UNKNOWN'}
        for claim in data['claims']:
            self.assertIn(claim['status'], allowed)
            for path in claim['evidence']:
                self.assertTrue((ROOT / path).is_file(), path)

    def test_known_rule_reference_is_reported_and_not_outperformed(self):
        report = json.loads((ROOT / 'examples/frozen_demo/report.json').read_text())
        heldout = report['heldout']
        self.assertEqual(heldout['oracle_aware_reference']['accuracy'], 1.0)
        self.assertLessEqual(heldout['candidate']['accuracy'], heldout['oracle_aware_reference']['accuracy'])
        self.assertEqual(report['claim_status']['independent_replication'], 'UNRESOLVED')
