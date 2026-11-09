# Research roadmap: RSI from reproducible toy to serious evaluation

## Phase 0 — Instrument and falsify the pipeline (implemented)

Freeze a tiny synthetic policy task; measure a recursive hill climb, strong references and random-search null; archive all test artifacts; implement replay, source checks and review attestation. Criterion: same inputs regenerate exactly the same bytes; false promotion is blocked. Current `examples/frozen_demo` is an internal simulated demonstration.

## Phase 1 — Real error-correction tasks (proposed)

Collect a licensed, externally sourced corpus of claim-evidence conflicts from multiple domains. Split by source and time, not merely by random row. Register adjudication standards, inter-rater disagreement and abstention cost. Establish rule-based, retrieval-plus-validator, structured Bayesian, calibration and conventional sequential-learning baselines. Before evaluation, compute data requirements, expected false-alert tolerance and cost budget. **No existing Devs 2.0 approved benchmark may be silently replaced by this corpus.**

## Phase 2 — Recursive process improvement (proposed)

Separate (a) improving the answer, (b) improving the policy, (c) changing the search algorithm, (d) changing the evaluator. Test each level independently. Require versioned, typed edits and restrict code execution to isolated sandboxes. Evaluate changes against never-before-seen error families. Insert matched budget random search, simple conventional optimization and a **no-recursion** control.

## Phase 3 — Coherence and EFMW-specific hypotheses (proposed)

Predefine competing operational variables: contradiction rate, evidence custody violations, signed/squared-error histories, and multiscale predictors. Test whether a proposed EFMW memory/coherence monitor produces measurable incremental value **after controlling these ordinary mechanisms**. Keep the physical interpretation of EFMW explicitly unresolved.

## Phase 4 — Independent replication and governance (proposed)

Give an independent reviewer protocol hashes and a sealed dataset; have another group execute exact commits, report both positive and negative cases, evaluate drift, and test resource constraints. Allow only explicitly approved deployment with rollback and continuous monitoring. Publish a transparent package with a signed custody ledger, review comments and protocol amendments.

## Hard go/no-go gates

At each phase require: named owner, rights to data, independent labels, frozen design, baseline selection, heldout custody, resource authorization, safe stopping rules, reproducible raw outputs and external review. Unmet conditions mean **UNRESOLVED**, not "ready".
