# Independent reviewer checklist

Reviewer should run from a fresh checkout with a recorded Git commit, Python version, OS and machine architecture.

- [ ] Confirm `configs/protocol-v1.json` was frozen before evaluating the study and its hash is recorded.
- [ ] Read `rsi/core.py` and confirm the synthetic target rule is not being marketed as real-world discovery.
- [ ] Run `python -m unittest discover -s tests -v` and record result and exact command.
- [ ] Run `python -m rsi verify examples/frozen_demo --check-source`.
- [ ] Run `python -m rsi replay examples/frozen_demo`; check exact byte-level equality.
- [ ] Re-execute a fresh run from the protocol into a new empty folder.
- [ ] Compare baseline, conservative policy, oracle-aware reference, candidate and random null, including denominators, coverage and wrong assertions.
- [ ] Check that candidate optimization has no path to holdout-case data before selection.
- [ ] Check the null arm's equal proposal budget and state distribution caveat.
- [ ] Confirm heldout ablations are labeled exploratory.
- [ ] Verify integrity hashes; explain why unsigned manifests do not prove chain of custody.
- [ ] Confirm `attest` has no automatic external promotion side effect.
- [ ] Keep real-world transfer, EFMW mechanism, autonomy and AGI assertions UNRESOLVED.

Suggested report fields: reviewer name and organization (if authorized), date, code SHA, OS/Python, commands, artifact digest, discrepancy list, source changes, PASS/FAIL/UNRESOLVED per claim, conflicts of interest and consent for public attribution.
