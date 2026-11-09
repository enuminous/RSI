"""Frozen-protocol experiment, improvement proposals, null arm and held-out gate."""
from __future__ import annotations

from dataclasses import dataclass
import json
import random
from typing import Any

from .core import Case, Label, Policy, generate_cases, mutate, predict, random_policy, score


@dataclass(frozen=True)
class Protocol:
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Protocol":
        if not isinstance(raw, dict):
            raise ValueError("protocol must be an object")
        if raw.get("protocol_id") != "RSI-SYNTH-001" or raw.get("version") != "1.0.0":
            raise ValueError("unsupported protocol identifier/version")
        if raw.get("status") != "FROZEN":
            raise ValueError("protocol must be FROZEN")
        data, search, gate = (raw.get(k) for k in ("dataset", "search", "gate"))
        if not all(isinstance(k, dict) for k in (data, search, gate)):
            raise ValueError("dataset, search, gate objects required")
        if not isinstance(raw.get("baseline_policy"), dict):
            raise ValueError("baseline_policy object required")
        Policy.from_dict(raw["baseline_policy"])
        for key in ("development_size", "holdout_size", "development_seed", "holdout_seed"):
            if type(data.get(key)) is not int or data[key] < 0:
                raise ValueError(f"invalid dataset.{key}")
        if data["development_size"] < 128 or data["holdout_size"] < 128:
            raise ValueError("both dataset sizes must be >= 128")
        if data["development_seed"] == data["holdout_seed"]:
            raise ValueError("development and holdout seeds must differ")
        if data.get("development_distribution") != "uniform":
            raise ValueError("unsupported development distribution")
        if data.get("holdout_distribution") != "stress":
            raise ValueError("unsupported holdout distribution")
        if type(search.get("budget")) is not int or not 1 <= search["budget"] <= 10000:
            raise ValueError("search.budget must be 1..10000")
        if type(search.get("seed")) is not int or search["seed"] < 0:
            raise ValueError("invalid search.seed")
        if search.get("algorithm") != "one_gene_hillclimb":
            raise ValueError("unsupported algorithm")
        if search.get("null_arm") != "uniform_random_search_same_budget":
            raise ValueError("unsupported null arm")
        for key in ("minimum_accuracy_gain", "maximum_false_assertion_increase", "minimum_ci_lower"):
            val = gate.get(key)
            if type(val) not in (float, int) or not -1 <= val <= 1:
                raise ValueError(f"invalid gate.{key}")
        if type(gate.get("bootstrap_repetitions")) is not int or not 100 <= gate["bootstrap_repetitions"] <= 10000:
            raise ValueError("bootstrap repetitions must be 100..10000")
        if type(gate.get("bootstrap_seed")) is not int or gate["bootstrap_seed"] < 0:
            raise ValueError("invalid bootstrap_seed")
        return cls(raw)


def objective(metrics: dict[str, Any]) -> float:
    """Frozen on development: correct-rate minus twice wrong-assertion rate."""
    return metrics["accuracy"] - 2.0 * metrics["false_assertion_rate"]


def hillclimb(initial: Policy, dev: list[Case], budget: int, seed: int):
    rng = random.Random(seed)
    best = initial
    best_score = objective(score(best, dev))
    trace: list[dict[str, Any]] = []
    for step in range(1, budget + 1):
        proposal = mutate(best, rng)
        metrics = score(proposal, dev)
        value = objective(metrics)
        accepted = value > best_score + 1e-12
        if accepted:
            best, best_score = proposal, value
        trace.append({"step": step, "proposal": proposal.as_dict(),
                      "dev_objective": value, "accepted": accepted})
    return best, trace


def null_search(dev: list[Case], budget: int, seed: int):
    # Budget matched on number of development-set proposals; not independent
    # scientific replication and not a matched hypothesis class in complexity.
    rng = random.Random(seed)
    champion = None
    best_score = float("-inf")
    trace: list[dict[str, Any]] = []
    for step in range(1, budget + 1):
        proposal = random_policy(rng)
        value = objective(score(proposal, dev))
        accepted = value > best_score + 1e-12
        if accepted:
            champion, best_score = proposal, value
        trace.append({"step": step, "proposal": proposal.as_dict(),
                      "dev_objective": value, "accepted": accepted})
    assert champion is not None
    return champion, trace


def paired_bootstrap_interval(initial: Policy, candidate: Policy, holdout: list[Case],
                              reps: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    per_case = [
        int(predict(candidate, c)[0] == c.truth) - int(predict(initial, c)[0] == c.truth)
        for c in holdout
    ]
    n = len(per_case)
    samples = []
    for _ in range(reps):
        samples.append(sum(per_case[rng.randrange(n)] for _ in range(n)) / n)
    samples.sort()
    lo = samples[int(0.025 * (reps - 1))]
    hi = samples[int(0.975 * (reps - 1))]
    return lo, hi


def ablated(policy: Policy, change: str) -> Policy:
    state = policy.as_dict()
    if change == "remove_provenance_gate":
        state["require_provenance"] = False
    elif change == "remove_bridge_gate":
        state["require_bridge"] = False
    elif change == "force_support_on_conflict":
        state["conflict_handling"] = "prefer_support"
    else:
        raise ValueError("unknown ablation")
    return Policy.from_dict(state)


def perform(protocol: Protocol) -> dict[str, Any]:
    cfg = protocol.raw
    data, search, gate = cfg["dataset"], cfg["search"], cfg["gate"]
    initial = Policy.from_dict(cfg["baseline_policy"])
    conservative = Policy(2, 2, True, True, "abstain")
    oracle_reference = Policy(1, 1, True, True, "abstain")
    dev = generate_cases(data["development_size"], data["development_seed"],
                         "dev", data["development_distribution"])
    # This is generated before search but *never passed* to the search routines.
    # The local source and seeds are visible: NOT a cryptographically sealed holdout.
    holdout = generate_cases(data["holdout_size"], data["holdout_seed"],
                             "holdout", data["holdout_distribution"])
    candidate, trace = hillclimb(initial, dev, search["budget"], search["seed"])
    null, null_trace = null_search(dev, search["budget"], search["seed"] + 1)
    baseline_h, conservative_h, reference_h, candidate_h, null_h = [
        score(p, holdout) for p in (initial, conservative, oracle_reference, candidate, null)
    ]
    baseline_d, conservative_d, reference_d, candidate_d, null_d = [
        score(p, dev) for p in (initial, conservative, oracle_reference, candidate, null)
    ]
    ci_low, ci_high = paired_bootstrap_interval(initial, candidate, holdout,
                                                 gate["bootstrap_repetitions"], gate["bootstrap_seed"])
    gain = candidate_h["accuracy"] - baseline_h["accuracy"]
    false_delta = (candidate_h["false_assertion_rate"] - baseline_h["false_assertion_rate"])
    rules = {
        "minimum_accuracy_gain": gain >= gate["minimum_accuracy_gain"],
        "maximum_false_assertion_increase": false_delta <= gate["maximum_false_assertion_increase"] + 1e-12,
        "minimum_ci_lower": ci_low > gate["minimum_ci_lower"],
    }
    status = "PASS" if all(rules.values()) else "FAIL"
    ablation_metrics = {
        name: score(ablated(candidate, name), holdout)
        for name in ("remove_provenance_gate", "remove_bridge_gate", "force_support_on_conflict")
    }
    report = {
        "experiment_id": cfg["protocol_id"],
        "protocol_version": cfg["version"],
        "scope": "synthetic finite-policy optimization; internal demonstration only",
        "claim_status": {
            "synthetic_holdout_gate": status,
            "independent_replication": "UNRESOLVED",
            "real_world_transfer": "UNRESOLVED",
            "efmw_specific_mechanism": "UNRESOLVED",
            "autonomous_model_weight_updates": "NOT_IMPLEMENTED",
            "agi": "NOT_ESTABLISHED",
        },
        "development": {"baseline": baseline_d, "conservative_baseline": conservative_d,
                        "oracle_aware_reference": reference_d, "candidate": candidate_d,
                        "random_search_null": null_d},
        "heldout": {"baseline": baseline_h, "conservative_baseline": conservative_h,
                    "oracle_aware_reference": reference_h, "candidate": candidate_h,
                    "random_search_null": null_h},
        "effect": {"accuracy_gain": gain, "false_assertion_rate_change": false_delta,
                   "paired_bootstrap_95pct_accuracy_gain_interval": [ci_low, ci_high]},
        "gate": {"status": status, "checks": rules, "thresholds": gate},
        "search": {"algorithm": search["algorithm"], "proposal_budget": search["budget"],
                   "null_algorithm": search["null_arm"], "null_proposal_budget": search["budget"]},
        "ablations": {"classification": "EXPLORATORY_NOT_PREREGISTERED_AS_GATE",
                      "holdout_results": ablation_metrics},
        "limitations": [
            "Synthetic ground truth is written into the code and is not externally measured.",
            "An explicitly oracle-aware reference policy achieves the benchmark ceiling; the candidate does not outperform it.",
            "The finite policy search is not self-modification of AI model weights.",
            "Development and holdout have separate seeds but share the same synthetic oracle.",
            "Holdout seeds and implementation are public; there is no secure blinding.",
            "A single internal run is not independent replication or evidence of AGI.",
            "Ablations are descriptive post-selection analyses and not confirmatory tests.",
        ],
        "promotion": "NOT_AUTOMATIC; independent signoff not included",
    }
    return {
        "protocol.snapshot.json": cfg,
        "development_cases.json": [c.as_dict() for c in dev],
        "holdout_cases.json": [c.as_dict() for c in holdout],
        "baseline_policy.json": initial.as_dict(),
        "control_policies.json": {"conservative_baseline": conservative.as_dict(),
                                  "oracle_aware_reference": oracle_reference.as_dict()},
        "candidate_policy.json": candidate.as_dict(),
        "null_policy.json": null.as_dict(),
        "search_trace.json": {"candidate": trace, "random_search_null": null_trace},
        "report.json": report,
    }
