import json
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from rsi.cli import main, ROOT
from rsi.experiment import Protocol, perform
from rsi.io import verify_run, write_run

CONFIG = json.loads((ROOT / "configs/protocol-v1.json").read_text())


class CLITests(unittest.TestCase):
    def test_write_verify_replay_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "trial"
            results = perform(Protocol.from_dict(CONFIG))
            write_run(run, results, ROOT)
            self.assertEqual(verify_run(run, ROOT)["status"], "PASS")
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.assertEqual(main(["replay", str(run)]), 0)
            (run / "candidate_policy.json").write_text("{}")
            self.assertEqual(verify_run(run)["status"], "FAIL")
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.assertEqual(main(["replay", str(run)]), 1)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "trial"
            result = perform(Protocol.from_dict(CONFIG))
            write_run(run, result, ROOT)
            with self.assertRaises(FileExistsError):
                write_run(run, result, ROOT)

    def test_attestation_requires_integrity_and_adequate_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "trial"
            result = perform(Protocol.from_dict(CONFIG))
            write_run(run, result, ROOT)
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                status = main(["attest", str(run), "--reviewer", "Test Reviewer",
                               "--reason", "x"])
            self.assertEqual(status, 2)
            self.assertFalse((run / "human_attestation.json").exists())
