# Threat model and governance boundary

## Protected assets

- Frozen protocol, source revision and evaluation thresholds.
- Identity, source and chain of custody for development and heldout datasets.
- Authenticity of independent review.
- Distinction between evidence and speculative interpretation.
- No unauthorized model promotion, external writes or private-data access.

## Attacker / failure modes

| Failure mode | Current mitigation | Remaining risk |
|---|---|---|
| Search overfits the development distribution | Separate holdout seed and stress distribution | Same synthetic oracle and public code |
| Researcher repeatedly tunes after seeing heldout | Versioned protocol and amendment rule | No external custodian; cannot enforce outside repository |
| Candidate fabricates a PASS | Candidate is only a constrained dataclass | Source and manifest could be edited together |
| Unsafe automatic production promotion | `attest` only records a review, no deployment | Social pressure may cause human overclaiming |
| Benchmark gaming via abstention | Report accuracy, false assertions and coverage | Measures may still misrepresent external utility |
| Conflicting or unverified input | UNRESOLVED output in candidate policy | Other policies may bypass safeguards |
| Prompt injection / malicious external docs | No document ingestion or LLM tool execution | Future connectors would require separate sandboxing |
| Loss of provenance | Source hashes, artifact hashes and replay | Hashes are not signatures and do not establish authorship |
| Self-modifying unsafe code | No code mutation or executable payloads | Future extensions must obtain separate review |
| Personal or proprietary data leakage | Only generator-created cases | Future dataset integrations need contracts and privacy review |

## Required for live systems

Sandbox with no unrestricted tool/network permissions; human approval for each mutation surface; bounded resource budgets; independently held secrets; immutable signed logs; explicit kill switch; predeclared stopping rules; privacy authorization; independent red-team; reviewer-selected random samples; multiple baselines; out-of-distribution testing and rollback plan. None is fully implemented here.
