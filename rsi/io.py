"""Canonical serialization and local, non-adversarial integrity checks."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def encode(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_run(directory: Path, results: dict[str, Any], source_root: Path) -> dict[str, Any]:
    if directory.exists() and any(directory.iterdir()):
        raise FileExistsError(f"run directory is not empty: {directory}")
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name, value in sorted(results.items()):
        blob = encode(value)
        (directory / name).write_bytes(blob)
        outputs[name] = sha256(blob)
    source_files = ["rsi/core.py", "rsi/experiment.py", "rsi/io.py", "rsi/cli.py"]
    source_hashes = {path: sha256((source_root / path).read_bytes()) for path in source_files}
    manifest = {
        "type": "RSI-SYNTH-001-artifact-digests",
        "algorithm": "SHA-256",
        "artifact_hashes": outputs,
        "source_hashes": source_hashes,
        "note": "Detects accidental changes only; author-controlled hashes are not a digital signature.",
    }
    (directory / "manifest.json").write_bytes(encode(manifest))
    return manifest


def verify_run(directory: Path, source_root: Path | None = None) -> dict[str, Any]:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    problems = []
    for filename, expected in manifest["artifact_hashes"].items():
        target = directory / filename
        if not target.is_file() or sha256(target.read_bytes()) != expected:
            problems.append(f"missing/changed artifact: {filename}")
    if source_root is not None:
        for name, expected in manifest["source_hashes"].items():
            target = source_root / name
            if not target.is_file() or sha256(target.read_bytes()) != expected:
                problems.append(f"missing/changed source: {name}")
    return {"status": "PASS" if not problems else "FAIL", "problems": problems}
