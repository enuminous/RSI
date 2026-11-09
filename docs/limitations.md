# Limitations — read before quoting the output

1. **Synthetic, tautological in the relevant sense.** The benchmark's oracle and optimal policy exist within the same transparent codebase. Finding the optimal policy demonstrates the search tool, not scientific discovery.
2. **Ceiling control.** The oracle-aware conventional reference already scores 100%. The candidate cannot show a superiority margin over it.
3. **Deliberately weak starting policy.** The nominal initial baseline skips provenance and bridge requirements. Large gains versus that starting point should not be generalized.
4. **Finite policy search.** There are only 108 possible policies; improving this parameter vector is not recursive redesign of the underlying learning architecture.
5. **Public holdout.** The split is separated programmatically, but there is no independent dataset custodian or adversarial blinding. Source inspection exposes the target rule.
6. **Search distribution and null control.** Equal proposal count is not full equality of search complexity or discovery probability. One random null run is insufficient for a statistical superiority claim.
7. **Post-selection ablations.** Same holdout is used to inspect component removal after selection. These are exploratory and may be optimistically biased.
8. **No real-world labels.** No Monolithic customer, Boardy, Devs 2.0, Unity or EFMW physics data is used. No consent or usage right for those data is implied.
9. **Incomplete security and audit custody.** SHA-256 digests are unsigned; a party can rewrite both artifacts and manifest. GitHub CI is controlled by repository owners.
10. **No AGI, continuous memory or sentience claim.** The program has no persistent cognitive life, self-directed planning, network use, weights access or automatic code execution.
11. **No Lean kernel verification.** The source is exercised with ordinary Python unit tests; mathematical proof obligations in documentation are not Lean-certified.
12. **No third-party review yet.** Repeatable local execution is not external independent replication.

## Claim discipline

A graph or screenshot showing 100% must be accompanied by the exact phrase **"accuracy on a synthetic oracle-defined task"**, the 384-case denominator and the oracle-aware reference result. Report false-assertion counts together with denominators and abstention coverage, rather than accuracy alone.
