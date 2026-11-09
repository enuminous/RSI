# Frozen local demonstration

`frozen_demo/` contains the complete output of a local execution of `RSI-SYNTH-001` using Python 3.13. It is a synthetically generated example **not an external or independently reviewed result**. All input cases and their oracle-defined labels are archived; `manifest.json` fingerprints them and the four core implementation files.

Run `python -m rsi replay examples/frozen_demo` from an unchanged checkout to regenerate the result and compare it byte for byte, or `python -m rsi verify examples/frozen_demo --check-source` to check local hashes.

Reported denominator: **384 artificial holdout cases**. The optimized candidate obtains 384/384 correct with 44/384 assertive coverage. The known-rule conventional reference also obtains 384/384 correct. The baseline is intentionally weak and its apparent large gain is not evidence of AGI or scientific mechanism discovery.
