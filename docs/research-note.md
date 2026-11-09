# RSI-SYNTH-001: a falsifiable instrument for bounded recursive strategy improvement

**Authors:** Matthew Chenoweth Wright / MillieComplex research program  
**Date:** 2026-11-09  
**Genre:** Technical demonstration note; not peer reviewed  
**Status:** SIMULATED; no independent scientific replication

## Abstract

A recursive self-improvement system is sometimes defined so loosely that any sequence of self-reflections or answer edits is treated as progress. We instead define a stricter operational test: predeclare the evaluation contract; recursively optimize a bounded strategy against development data; compare with ordinary controls; assess unseen cases once; preserve an auditable history; and prevent unapproved promotion. We implement this process in dependency-free Python using a deliberately synthetic evidence-labeling task. The purpose is **instrument calibration and governance**, not a novel cognitive or physical discovery.

## Method

The state contains a small policy for assigning `SUPPORTED`, `CONTRADICTED` or `UNRESOLVED` to claims represented by evidence counts and provenance/bridge flags. A fixed synthetic oracle supplies labels. At each development step, a candidate differs from the current champion in one gene. A strict improvement in development accuracy minus twice wrong-assertion rate is required to update the champion. After 64 proposals, the winner is frozen and evaluated on 384 heldout synthetic cases generated with a new seed and stress distribution. A separate random search receives 64 development proposals. Two conventional fixed policies serve as controls, including one given the artificial truth rule.

## Result: included deterministic demonstration

The original baseline scores **159/384 = 41.41% accuracy** with **205/384 = 53.39% wrong assertive outputs** and **229/384 = 59.64% coverage**. The optimized candidate scores **384/384 = 100% synthetic accuracy**, **0/384 false assertions**, and **44/384 = 11.46% coverage**. The random-search control scores **349/384 = 90.89% accuracy**. The policy explicitly given the synthetic oracle reaches **384/384 = 100%** as well. The nominal gate passes with an accuracy gain of 58.59 percentage points and a paired bootstrap 95% interval of approximately [53.65, 63.54] percentage points. These figures are outputs of the included frozen run, not claims about a foundation model or actual physics problems.

**A crucial diagnostic:** the seemingly impressive 100% score is fully explainable by the artificial oracle; the optimizer has rediscovered a target that a transparent rule-based control already implements. Its very low coverage, and the possibility of an overly easy benchmark, require more attention than the raw accuracy headline. The task is also heavily weighted toward `UNRESOLVED` under the stress distribution.

## Interpretation and next tests

The result supports the narrow claim that a bounded recursive search and evaluation packet can run deterministically and preserve a separated candidate, control and audit trail. It does **not** establish generalizable recursive self-improvement, superiority to appropriate conventional baselines, discovery of new mathematical truths, any EFMW-specific memory process or AGI. The next study must use actual, source-disjoint error-correction data, human adjudication protocols, independently blinded holdouts, multiple controls and reviewers who can reproduce exact commands without access to developer-side tuning.

## Reproduction

See `README.md` and run `python -m rsi replay examples/frozen_demo` in an unchanged checkout. `manifest.json` records checksums; for legitimate independent custody use signed source revisions and signatures supplied by an external reviewer.
