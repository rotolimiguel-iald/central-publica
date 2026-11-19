#!/usr/bin/env python3
"""Deterministic K06 extractors. Standard library only; no model calls.

The accepted surface is deliberately strict. Each non-comment content line is:
K06R1|ID|SUBJECT|RELATION|OBJECT|STATUS

Unstructured prose invalidates the whole surface. A malformed structured line only
loses its own assertion. Exact duplicates collapse; conflicting duplicates score
zero for the affected assertion. C4 abstention is explicit, never inferred from
an empty answer.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
DEFAULT_SPEC = ROOT / "especificacao.json"
HEADER = "K06R1"
MAX_CHARS = 1_000_000
MAX_LINES = 10_000
ID_RE = re.compile(r"^[A-Z0-9_]+$")
TOKEN_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")
ZERO = tuple(0 for _ in range(24))
ONE = tuple(1 for _ in range(24))


def load_spec(path: Path | str = DEFAULT_SPEC) -> Dict[str, Any]:
    """Load and validate the frozen 5 x 24 assertion specification."""
    spec_path = Path(path)
    with spec_path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    if spec.get("schema") != "K06_EXTRACTOR_SPEC_V1":
        raise ValueError("unexpected specification schema")
    if set(spec["arms"]) != {"T", "C1", "C2", "C3", "C4"}:
        raise ValueError("the five frozen arms are required")
    all_ids = set()
    for arm, arm_spec in spec["arms"].items():
        assertions = arm_spec["assertions"]
        if len(assertions) != 24 or arm_spec["tau"] != [1] * 24:
            raise ValueError(f"{arm}: expected 24 assertions and tau=(1,...,1)")
        ids = [item["id"] for item in assertions]
        if len(set(ids)) != 24 or all_ids.intersection(ids):
            raise ValueError(f"{arm}: assertion identifiers are not unique")
        all_ids.update(ids)
        for item in assertions:
            fields = [item[key] for key in ("subject", "relation", "object", "status")]
            if not ID_RE.fullmatch(item["id"]) or not all(TOKEN_RE.fullmatch(x) for x in fields):
                raise ValueError(f"{item['id']}: non-canonical specification token")
    return spec


def _expected_tuples(spec: Dict[str, Any], arm: str) -> List[Tuple[str, str, str, str, str, str]]:
    tuples = []
    for item in spec["arms"][arm]["assertions"]:
        tuples.append((HEADER, item["id"], item["subject"], item["relation"], item["object"], item["status"]))
    return tuples


def _issue(code: str, line: int, detail: str = "") -> Dict[str, Any]:
    return {"code": code, "line": line, "detail": detail}


def extract(text: str, arm: str, spec: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return the 24-bit own-arm vector and deterministic diagnostics."""
    if spec is None:
        spec = load_spec()
    if arm not in spec["arms"]:
        raise ValueError(f"unknown arm: {arm}")
    expected = _expected_tuples(spec, arm)
    id_to_arm = {
        item["id"]: other_arm
        for other_arm, other_spec in spec["arms"].items()
        for item in other_spec["assertions"]
    }
    issues: List[Dict[str, Any]] = []
    records: Dict[str, set[Tuple[str, str, str, str, str, str]]] = {}
    all_canonical_records = set()
    unstructured = False
    exact_duplicate_count = 0

    if not isinstance(text, str):
        raise TypeError("extractor input must be text")
    if len(text) > MAX_CHARS or len(text.splitlines()) > MAX_LINES:
        return {
            "arm": arm,
            "vector": list(ZERO),
            "surface_valid": False,
            "issues": [_issue("INPUT_LIMIT", 0, "input exceeds frozen resource limit")],
            "accepted_records": 0,
            "exact_duplicates": 0,
            "conflicting_ids": [],
        }

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line in {"```", "```k06"}:
            continue
        if re.match(r"^K06R1\s*\|", line) is None:
            unstructured = True
            issues.append(_issue("UNSTRUCTURED_LINE", line_number, line[:80]))
            continue
        parts = tuple(part.strip() for part in line.split("|"))
        if len(parts) != 6:
            issues.append(_issue("MALFORMED_RECORD", line_number, "expected six fields"))
            continue
        if parts[0] != HEADER or not ID_RE.fullmatch(parts[1]):
            issues.append(_issue("MALFORMED_RECORD", line_number, "bad header or identifier"))
            continue
        if not all(TOKEN_RE.fullmatch(token) for token in parts[2:]):
            issues.append(_issue("MALFORMED_RECORD", line_number, "non-canonical field token"))
            continue
        record_id = parts[1]
        if record_id not in id_to_arm:
            issues.append(_issue("UNKNOWN_ID", line_number, record_id))
            continue
        if parts in all_canonical_records:
            exact_duplicate_count += 1
            continue
        all_canonical_records.add(parts)
        if id_to_arm[record_id] != arm:
            issues.append(_issue("FOREIGN_RECORD", line_number, record_id))
            continue
        records.setdefault(record_id, set()).add(parts)

    vector = [0] * 24
    conflicts = sorted(record_id for record_id, variants in records.items() if len(variants) > 1)
    accepted_records = 0
    for index, wanted in enumerate(expected):
        variants = records.get(wanted[1], set())
        if len(variants) == 1 and wanted in variants:
            vector[index] = 1
            accepted_records += 1
        elif len(variants) > 1:
            issues.append(_issue("CONFLICTING_RECORDS", 0, wanted[1]))

    if unstructured:
        vector = [0] * 24
        accepted_records = 0
        issues.append(_issue("UNSTRUCTURED_SURFACE", 0, "all assertions zeroed by the strict surface gate"))

    return {
        "arm": arm,
        "vector": vector,
        "surface_valid": not unstructured,
        "issues": issues,
        "accepted_records": accepted_records,
        "exact_duplicates": exact_duplicate_count,
        "conflicting_ids": conflicts,
    }


def extract_own(text: str, arm: str, spec: Dict[str, Any] | None = None) -> List[int]:
    """Public E_j interface."""
    return extract(text, arm, spec)["vector"]


def extract_tgl(text: str, spec: Dict[str, Any] | None = None) -> List[int]:
    """Public E_TGL interface; intentionally identical to E_T."""
    return extract(text, "T", spec)["vector"]


def canonical_text_sha256(text: str) -> str:
    """Hash raw UTF-8 text for exact cross-reading duplication checks."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_record_sha256(text: str, spec: Dict[str, Any] | None = None) -> str:
    """Hash layout-insensitive valid records for near-duplicate auditing.

    The digest is not a semantic similarity measure. It only removes whitespace,
    comments, fences, foreign/unknown identifiers and exact duplicate records.
    """
    if spec is None:
        spec = load_spec()
    known_ids = {
        item["id"]
        for arm_spec in spec["arms"].values()
        for item in arm_spec["assertions"]
    }
    records = set()
    unstructured = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line in {"```", "```k06"}:
            continue
        if re.match(r"^K06R1\s*\|", line) is None:
            unstructured = True
            continue
        parts = tuple(part.strip() for part in line.split("|"))
        if len(parts) != 6 or parts[1] not in known_ids:
            continue
        if not all(TOKEN_RE.fullmatch(token) for token in parts[2:]):
            continue
        records.add("|".join(parts))
    payload = json.dumps(
        {"surface_valid": not unstructured, "records": sorted(records)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def own_distance(vector: Sequence[int], target: Sequence[int] = ONE) -> float:
    """Normalized own-target distance on the 24-bit cube."""
    if len(vector) != 24 or len(target) != 24:
        raise ValueError("24 components required")
    return sum(abs(a - b) for a, b in zip(vector, target)) / 24.0


def a8_from_vectors(vectors: Sequence[Sequence[int]], target: Sequence[int] = ONE) -> Dict[str, Any]:
    """Compute R2 A8 exactly; its non-null final block spans reads 5 through 8."""
    if len(vectors) != 8:
        raise ValueError("A8 requires eight readings")
    distances = [own_distance(vector, target) for vector in vectors]
    changes = [0.0] + [own_distance(vectors[k], vectors[k - 1]) for k in range(1, 8)]
    original_predicate = (
        distances[5] == distances[6] == distances[7] == 0.0
        and changes[5] == changes[6] == changes[7] == 0.0
    )
    return {
        "A8": int(original_predicate),
        "distances": distances,
        "changes": changes,
        "effective_perfect_readings": [5, 6, 7, 8],
        "assertion_reading_cells": 24 * 4,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Apply a deterministic K06 extractor to a UTF-8 text file.")
    parser.add_argument("text_file", type=Path)
    parser.add_argument("--arm", choices=["T", "C1", "C2", "C3", "C4"])
    parser.add_argument("--cross-tgl", action="store_true")
    args = parser.parse_args()
    content = args.text_file.read_text(encoding="utf-8")
    arm = "T" if args.cross_tgl else args.arm
    if arm is None:
        parser.error("choose --arm or --cross-tgl")
    print(json.dumps(extract(content, arm), ensure_ascii=False, indent=2, sort_keys=True))
