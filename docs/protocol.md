# Frozen demonstration protocol — RSI-SYNTH-001 v1.0.0

**Protocol source:** `configs/protocol-v1.json`; archive copies this into every run's `protocol.snapshot.json`.

## Hypothesis and counterhypotheses

**H1 (narrow):** A fixed-budget one-gene recursive strategy search improves the defined synthetic evidence-labeling policy versus a deliberately non-optimal baseline, without increasing wrong assertive outputs.

**H0:** It fails one or more of the frozen thresholds.

**Not tested:** Improvement relative to the oracle-aware reference, generalization to real research, EFMW-specific explanatory power, autonomous model self-modification, consciousness or AGI.

## Inputs

| Input | Frozen value |
|---|---|
| Development cases | 384, seed 4301, uniform distribution |
| Holdout cases | 384, seed 8707, stress distribution |
| Candidate proposals | 64, seed 991 |
| Random-search null proposals | 64, seed 992 |
| Paired bootstrap | 1,000 resamples, seed 515 |
| Selected outcome | Accuracy gain vs baseline, wrong-assertion-rate change, CI lower bound |
| Missing-evidence output | UNRESOLVED |

Truth generator: unless **both** provenance and bridge are verified, the label is `UNRESOLVED`. Otherwise, evidence only for support means `SUPPORTED`; only for contradiction means `CONTRADICTED`; conflict or no evidence means `UNRESOLVED`. This rule is written in `rsi/core.py`, which intentionally makes the problem *solvable by ordinary explicit rules*.

Each of two search arms receives **exactly 64 proposals on the development set**. Recursive search mutates one parameter of its current development champion; random search samples policies from the same 108-policy space. They are not guaranteed identical in initial state, proposal distribution or chance of discovering the target; the second arm is a descriptive control, not a matched statistical experiment.

## Metrics

`accuracy` = correct decisions / all cases. `false_assertion_rate` = incorrect `SUPPORTED` or `CONTRADICTED` decisions / **all cases**. `coverage` = non-UNRESOLVED decisions / all cases. These have distinct denominators and must not be quietly interchanged.

The development-only objective is:

\[
J(P) = \frac{\#\text{correct}}{n} - 2\frac{\#\text{wrong assertive}}{n}.
\]

The holdout gate is `PASS` iff all of these apply:

1. Accuracy improvement over the predefined initial baseline ≥ **0.05** (five percentage points).
2. Change in false-assertion rate ≤ **0** (no increase).
3. The 2.5th percentile of the predeclared *paired case-bootstrap* distribution of accuracy gains is strictly greater than **0**.

The paired bootstrap interval is a descriptive uncertainty summary conditional on the synthetic data generator; it is not a guarantee of external validity. Failure of any test sets `FAIL` for this gate. `UNRESOLVED` is a **separate claim status** used when no corresponding real-world experiment has occurred.

## Strong reference controls

- **Conservative baseline:** requires provenance and bridge, but requires two units of unopposed evidence before making assertive decisions.
- **Oracle-aware reference:** explicitly implements the known synthetic labeling rule with thresholds of one and conflict abstention. Its ceiling performance is expected. It is a necessary check against advertising a rediscovered hard-coded rule as novel intelligence.
- **Random-search null:** same development proposal budget, chosen by best development score.

These controls are reported beside candidate performance, not hidden in footnotes.

## Analysis and contamination controls

Candidate-selection functions receive development cases only. Holdout data are generated from a different seed and distribution and scored after selection. However, **the oracle, generator, seeds and policy class are all public**; this is not blinded evidence of generalization beyond the programmed task. The heldout set is reused for descriptive post-selection ablations and appears in the run archive; these ablations must not be presented as confirmatory.

Fresh confirmatory work must use a sealed dataset prepared by an independent custodian, a frozen protocol hash, independent scorers and a new experimental identifier. Repeat runs under the same visible synthetic seeds are technical replay, **not independent replication**.

## Required outputs

`protocol.snapshot.json`, the two case sets, baseline/controls/candidate/null policy JSON, step-by-step search traces, `report.json`, and `manifest.json`. Each output has a SHA-256 hash. `python -m rsi replay <run>` recomputes all deterministic data, and `--check-source` detects divergence from the local code used to generate the archive.

## Amendment rule

Do not change this benchmark in place. Copy the protocol, increment version and identifier, write a protocol amendment before looking at the new test set, and retain the original report unmodified. See `protocol-amendment-template.md`.
