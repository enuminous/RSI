"""Standard-library command line interface. No network calls or auto-promotion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .experiment import Protocol, perform
from .io import encode, verify_run, write_run

ROOT = Path(__file__).resolve().parents[1]


def load_protocol(path: Path) -> Protocol:
    return Protocol.from_dict(json.loads(path.read_text(encoding="utf-8")))


def command_run(args: argparse.Namespace) -> int:
    cfg = load_protocol(Path(args.protocol))
    results = perform(cfg)
    out = Path(args.out)
    write_run(out, results, ROOT)
    gate = results["report.json"]["gate"]["status"]
    print(f"Created {out} | synthetic held-out gate: {gate} | promotion: PENDING")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    result = verify_run(Path(args.run), ROOT if args.check_source else None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


def command_replay(args: argparse.Namespace) -> int:
    run_dir = Path(args.run)
    verified = verify_run(run_dir, ROOT)
    if verified["status"] != "PASS":
        print(json.dumps(verified, indent=2))
        return 1
    protocol = load_protocol(run_dir / "protocol.snapshot.json")
    regenerated = perform(protocol)
    mismatches = [
        name for name, value in regenerated.items()
        if encode(value) != (run_dir / name).read_bytes()
    ]
    print(json.dumps({"status": "PASS" if not mismatches else "FAIL",
                      "mismatches": mismatches}, indent=2))
    return 0 if not mismatches else 1


def command_approve(args: argparse.Namespace) -> int:
    directory = Path(args.run)
    integrity = verify_run(directory, ROOT)
    if integrity["status"] != "PASS":
        raise ValueError("run/source integrity failure; cannot attest")
    gate = json.loads((directory / "report.json").read_text(encoding="utf-8"))
    if gate["gate"]["status"] != "PASS":
        raise ValueError("synthetic held-out gate did not pass")
    if not args.reviewer.strip() or len(args.reason.strip()) < 15:
        raise ValueError("reviewer and substantive reason (15+ characters) required")
    target = directory / "human_attestation.json"
    if target.exists():
        raise FileExistsError("an attestation already exists; immutable-by-convention")
    attestation = {
        "reviewer": args.reviewer.strip(),
        "reason": args.reason.strip(),
        "scope": "human-reported review of synthetic run; NOT independent replication",
        "synthetic_gate": "PASS",
        "note": "No model weights or external software are automatically changed.",
    }
    target.write_bytes(encode(attestation))
    print(f"Recorded human attestation at {target}; no auto-promotion performed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rsi", description="MillieComplex RSI research harness")
    subs = parser.add_subparsers(dest="command", required=True)
    run = subs.add_parser("run", help="Generate frozen synthetic experiment and audit packet")
    run.add_argument("--protocol", default=str(ROOT / "configs/protocol-v1.json"))
    run.add_argument("--out", required=True)
    run.set_defaults(func=command_run)
    verify = subs.add_parser("verify", help="Verify artifact digests")
    verify.add_argument("run")
    verify.add_argument("--check-source", action="store_true")
    verify.set_defaults(func=command_verify)
    replay = subs.add_parser("replay", help="Recompute and byte-compare deterministic outputs")
    replay.add_argument("run")
    replay.set_defaults(func=command_replay)
    approve = subs.add_parser("attest", help="Record human attestation; no automatic deployment")
    approve.add_argument("run")
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--reason", required=True)
    approve.set_defaults(func=command_approve)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError, FileExistsError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
