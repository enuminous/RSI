# Formal obligations — target for future Lean 4 modeling

**These are specification goals, not currently machine-checked theorems.** No Lean source or kernel compilation is represented as executed.

1. **Policy validity:** every generated proposal remains in the finite authorized policy type.
2. **Development-only selection:** the candidate selection operator cannot read heldout examples or their labels.
3. **Monotonic development score:** a new champion is chosen only for strictly higher frozen development objective.
4. **No automatic deployment:** a synthetic gate outcome cannot write to a production policy store.
5. **Guarded attestation:** an attestation cannot be recorded unless artifact/source integrity and the synthetic gate pass.
6. **Frozen evaluation:** comparisons share the same metric implementation and exactly the same holdout case IDs.
7. **Provenance:** each published empirical claim points to a source revision, run, raw data, protocol and status.
8. **Uncertainty preservation:** `UNRESOLVED` is not silently coerced into `SUPPORTED` by missing-bridge or missing-source conditions.

Recommended progression: state a small Lean model with an abstract `Policy`, `Case`, `Decision` and an uninterpreted scoring function; prove type preservation, bounded transition and no-promotion invariants. Then independently audit whether the Python implementation refines those assumptions. A Lean proof of the *model* would not validate the physical or empirical meaning of the inputs.
