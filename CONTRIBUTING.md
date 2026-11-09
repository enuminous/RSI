# Contributing to RSI

Before proposing a scientific claim, add a source reference, exact revision, runnable command, machine-readable output and status (PROPOSED/DERIVED/SIMULATED/OBSERVED/REPLICATED/CONTRADICTED/UNKNOWN).

Do not retroactively edit `configs/protocol-v1.json` or a frozen experiment and describe it as unchanged. New thresholds, data, tasks or seeds require a new protocol version. Document all exploratory runs and report negative outcomes. Never promote candidates based only on development data.

No API keys, personal data, private communications or production telemetry should enter this public repository. External reviews require consent and provenance. Tests run with `python -m unittest discover -s tests -v`.
