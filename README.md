# RSI — MillieComplex Recursive Self-Improvement

[![Reproducibility checks](https://github.com/enuminous/RSI/actions/workflows/ci.yml/badge.svg)](https://github.com/enuminous/RSI/actions/workflows/ci.yml)

**Status: research prototype / synthetic demonstration / no AGI claim**  
**Maintainer:** Matthew Chenoweth Wright · Monolithic LLC  
**Intended GitHub repository:** `enuminous/RSI` (not automatically published by this ZIP)

> A change is not an improvement merely because it is recursive. It is an improvement only when its independently evaluated consequences survive a frozen test.

RSI develops **MillieComplex** as an *evidence-gated, human–AI recursive strategy improvement architecture*. A bounded system proposes changes to its *decision procedure*, evaluates them on development examples, freezes the best candidate, tests it once on a separate synthetic holdout, records PASS/FAIL/UNRESOLVED status and waits for human review. It is designed to make **the distinction between recursion and validated improvement inspectable**.

It does **not** update foundation-model weights, implement self-directed autonomous research, demonstrate EFMW-specific physics, or establish artificial general intelligence. The first benchmark is intentionally small and synthetic so the *evaluation machinery* can be tested before it is applied to consequential research.

## Quick start (Python 3.10+, zero runtime dependencies)

Run from this repository's root:

```bash
python -m unittest discover -s tests -v
python -m rsi run --out runs/first
python -m rsi verify runs/first --check-source
python -m rsi replay runs/first
python -m rsi verify examples/frozen_demo
python -m rsi replay examples/frozen_demo
```

Optional installation as a command:

```bash
python -m pip install -e .
rsi run --out runs/second
```

To document an **explicit human attestation** after studying an internally passing run:

```bash
python -m rsi attest runs/first \
  --reviewer "Your name" \
  --reason "I reviewed the protocol, trace, evaluation, and limitations."
```

Attestation **does not deploy or promote a model**. It is a human-reported record, *not* a verified independent replication. The run directory must be unmodified and the original local source checksums must still match. The CLI never calls external APIs or writes outside the requested run directory.

## What is inside?

| Component | Purpose | Evidence status |
|---|---|---|
| `rsi/core.py` | Evidence cases, label oracle, parameterized policy, explanations | Executable synthetic model |
| `rsi/experiment.py` | Recursive one-gene proposals, matched-budget random search, frozen holdout, bootstrap gate, ablations | Executable research harness |
| `rsi/io.py`, `rsi/cli.py` | Canonical outputs, SHA-256 artifact hashes, replay, attestation | Executable local controls |
| `configs/protocol-v1.json` | Frozen seed, dataset sizes, baseline, search budget and pass criteria | Frozen *within this repo version* |
| `examples/frozen_demo/` | Complete example evidence packet and digest manifest | Locally reproduced; not independent |
| `tests/` | Determinism, boundary rules, artifact integrity and acceptance behavior | Tests runnable in CI |
| `docs/` | Mathematical model, protocol, threats, claims ledger, review checklist and future phases | Proposed/annotated design |
| `index.html` | Static, GitHub Pages-compatible evidence explorer | Renders archived simulated outputs |
| `.github/workflows/ci.yml` | Replays sample and executes fresh run on Python 3.10/3.12 | CI configuration, not a current badge claim |

## MillieComplex formalization

Let the research-system state be

\[
M_t=(K_t,P_t,H_t,V_t,A_t),
\]

where \(K_t\) contains evidence, \(P_t\) the bounded policy or strategy, \(H_t\) immutable-by-convention history, \(V_t\) fixed verification conditions, and \(A_t\) human authorizations.

\[
\widetilde M_{t+1}=\mathcal R(M_t,E_t,F_t), \qquad
M_{t+1}=\mathcal G(\widetilde M_{t+1},V_t,A_t).
\]

The proposal operator \(\mathcal R\) **does not** establish improvement. The gate \(\mathcal G\) evaluates an unexposed holdout with a declared baseline and a precommitted failure budget; rejected candidates cannot replace the accepted state. In the current demonstration \(\mathcal G\) **only writes a report**: a passing gate never autonomously changes a production system.

The evaluation condition is

\[
\Delta Q=Q(P_{candidate},D_{holdout})-Q(P_{baseline},D_{holdout}),
\]

with explicit non-inferiority on wrong assertions and paired uncertainty bounds. The metric and requirements are in `docs/protocol.md`.

## The three decisions

- **PASS:** The *internal synthetic* predeclared acceptance checks were met; **not** a universal success claim.
- **FAIL:** One or more predeclared checks were not met; retain the baseline.
- **UNRESOLVED:** No reliable test, missing provenance, independent replication not done, or evidence insufficient to adjudicate a broader claim. Specific research questions remain UNRESOLVED even if a synthetic gate passes.

## Hard boundary

The current toy oracle generates labels from the **same publicly known logic the optimizer can eventually learn**. This is useful for testing reproducibility and governance, but it is not evidence of transfer learning, novel theory discovery, EFMW-specific effects, or an autonomous intelligence explosion. The heldout seed is visible in source; it is separated in code, *not blind to a sophisticated researcher*. See `docs/limitations.md` and `docs/threat_model.md`.

## Repo structure and reading order

1. `docs/architecture.md` — state, feedback loop, gates.
2. `docs/protocol.md` — exact frozen example and evaluation contract.
3. `docs/evidence-ledger.md` — what's shown, proposed and unknown.
4. `docs/reviewer-checklist.md` — independent audit route.
5. `docs/roadmap.md` — real task datasets, controls, adversarial review and replication.

## Attribution, reuse and responsible publication

© 2026 Matthew Chenoweth Wright. MIT license for the repository code. `CITATION.cff` provides authorship metadata; the scientific claims must be attributed only to evidence that actually exists. No prior historical MillieComplex publication, discovery date, or unique cognitive mechanism is asserted here without independently inspected source records.

To publish this flat ZIP as a GitHub repository, create `RSI` and extract **its contents** into the repository root. For the optional public observatory, enable GitHub Pages from the repository root (`/`) on the intended branch; `index.html` reads its local archived JSON via relative paths. Do not treat the target URL or CI badge above as proof the repository is already online.
