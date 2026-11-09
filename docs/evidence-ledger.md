# Claims, decisions and evidentiary status

This file summarizes the machine-readable `docs/evidence-ledger.json` record. The record distinguishes **epistemic** statuses from **benchmark decisions**:

- `PROPOSED`: architecture or hypothesis awaiting implementation or measurement.
- `DERIVED`: follows from stated definitions or inspected executable logic, without external measurement.
- `SIMULATED`: computed under an artificial data-generating process.
- `OBSERVED`: measured in actual collected data, with custody and controls disclosed.
- `REPLICATED`: reproduced by an independent party under declared constraints.
- `CONTRADICTED`: a particular asserted behavior is inconsistent with the evidence.
- `UNKNOWN`: no adequate evidence or verification yet.

The verdicts `PASS`, `FAIL`, and `UNRESOLVED` are **test decisions**. In this repository `PASS` refers to the synthetic gate only. The `UNKNOWN` entries for external replication, EFMW specificity and real-world generalization remain open even if this gate passes.

In the included demonstration, the modified policy recovers the artificial ground-truth mapping. It **matches**, not exceeds, the explicit oracle-aware reference. The latter is a conventional rule-based solution, so a broad breakthrough interpretation is unwarranted.

A stronger future experiment must test distinct real-world errors, independently constructed labels and alternatives such as ordinary rule-based systems, calibration, retrieval, Bayesian filtering, conventional reinforcement learning and other deterministic coherence monitors.
