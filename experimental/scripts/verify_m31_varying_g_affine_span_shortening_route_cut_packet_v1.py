#!/usr/bin/env python3
"""Fail-closed packet verifier for the M31 affine-span route cuts.

This verifier independently checks the closed top-level schema, canonical
manifest and payload hash, fresh source hashes, predecessor payload pins,
theorem-note anchors, normal/optimized/tamper primary replays, the independent
Sage arithmetic replay, the exhaustive Sage toy census, and both sealed
predecessor packet verifiers.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Sequence


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/manifest.json"
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_varying_g_affine_span_shortening_route_cut_v1.schema.json"
PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.sage"
TOY_PATH = ROOT / "experimental/scripts/scan_m31_varying_g_shallow_incidence_toy_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_varying_g_affine_span_shortening_route_cut_v1.md"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py"
FIXED_G_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_fixed_g_universal_rs_embedding_packet_v1.py"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json"
FIXED_G_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/manifest.json"

SCHEMA_ID = "m31-varying-g-affine-span-shortening-route-cut-summary-v1"
THEOREM_ID = "M31_VARYING_G_AFFINE_SPAN_SHORTENING_ROUTE_CUT_V1"
STATUS = "PROVED_AFFINE_RANK4_AND_FIXED_G_ENDPOINT_ROUTE_CUTS_HIGH_RANK_OPEN"
TERMINAL = "UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE"
PARENT_PAYLOAD = "006cde59ee0a9fc23f8f13c3dc9955c26732bdee86b4af943f06fffeb5dd572e"
FIXED_G_PAYLOAD = "d28cf777c70a7cbfbf9d79aabe568c33f6efa9485270f41424bcafbea9926be4"


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        return (json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON") from exc


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def payload_hash(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def no_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def no_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        text = raw.decode("ascii")
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=no_float,
            parse_constant=no_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("valid ASCII JSON") from exc
    require(type(value) is dict, "top-level JSON object")
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    require(path.is_file(), f"file exists: {path}")
    return decode(path.read_bytes(), canonical=canonical)


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: value")


def run(command: Sequence[str]) -> bytes:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    require(completed.returncode == 0,
            f"subprocess success: {' '.join(command)}\n{completed.stderr.decode(errors='replace')}")
    return completed.stdout


def validate_schema(payload: dict[str, Any]) -> None:
    schema = load(SCHEMA_PATH, canonical=False)
    require(schema.get("additionalProperties") is False, "closed top-level schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(required) == set(properties), "schema exact top-level keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const: {key}")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["theorem_id"] == THEOREM_ID, "theorem id")
    require(payload["status"] == STATUS, "status")
    require(payload["terminal"] == TERMINAL, "terminal")


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload.get("source_bindings")
    require(type(bindings) is list and len(bindings) == 11, "source binding count")
    seen: set[str] = set()
    for binding in bindings:
        require(type(binding) is dict, "source binding object")
        require(set(binding) == {"binding_id", "role", "path", "sha256"},
                "source binding keys")
        path_text = binding["path"]
        require(type(path_text) is str and not path_text.startswith("/"), "relative source path")
        require(".." not in Path(path_text).parts, "source path traversal forbidden")
        path = ROOT / path_text
        require(path.is_file(), f"bound source exists: {path_text}")
        require(path_text not in seen, "source path unique")
        seen.add(path_text)
        require(hashlib.sha256(path.read_bytes()).hexdigest() == binding["sha256"],
                f"fresh source hash: {path_text}")


def validate_note() -> None:
    text = NOTE_PATH.read_text(encoding="utf-8")
    anchors = (
        "sum_{i\\in I}\\binom{w+s_i+r+e}{r}",
        "\\le \\binom{R+g-e}{r}",
        "\\boxed{r\\ge5}",
        "72,860\\le m\\le 908,269",
        "\\boxed{L\\le2,310,492}",
        "\\boxed{L\\le2,359,100}",
        "UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE",
        "ledger movement is exactly zero",
        "rank eleven",
    )
    for anchor in anchors:
        require(anchor in text, f"theorem-note anchor: {anchor}")


def validate_toy(payload: dict[str, Any]) -> dict[str, Any]:
    raw = run(["sage", str(TOY_PATH), "--summary-only"])
    summary = decode(raw, canonical=True)
    require(summary["checks"] == 40_010, "toy check count")
    require(summary["status"] == "EXACT_TOY_CENSUS_DEPLOYED_INCIDENCE_OPEN", "toy status")
    expected = [(5, 2, 5, 5), (1, 1, 0, 1), (3, 1, 3, 3),
                (3, 1, 3, 3), (14, 2, 14, 14)]
    observed = []
    for cell in summary["cells"]:
        abstract = cell["abstract_pairwise_maxima"]
        realized = cell["realized_nonanchor_codeword_maxima"]
        observed.append((
            abstract["maximum_any"],
            abstract["maximum_fixed_G"],
            abstract["maximum_mixed_G"],
            realized["maximum_any"],
        ))
    require(observed == expected, "toy maxima")
    require(payload["toy_census"]["cells"][-1]["zero_anchor_addback"] == 15,
            "toy add-back pin")
    return summary


def validate_replays(manifest: dict[str, Any]) -> dict[str, Any]:
    normal_raw = run([sys.executable, str(PRIMARY_PATH)])
    optimized_raw = run([sys.executable, "-O", str(PRIMARY_PATH)])
    require(normal_raw == optimized_raw, "normal equals optimized primary")
    primary = decode(normal_raw, canonical=True)
    deep_exact(primary, manifest, "primary_manifest")

    tamper = decode(run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"]), canonical=False)
    require(tamper["count"] == 21 and len(tamper["detected"]) == 21,
            "primary mutations detected")

    sage = decode(run(["sage", str(SAGE_PATH)]), canonical=False)
    require(sage["rank_caps_1_4"] == [31, 966, 30_058, 934_551], "Sage rank caps")
    require(sage["fixed_G_new_interval_m"] == [72_860, 908_269], "Sage interval")
    require(sage["lower_endpoint_cap"] == 2_310_492, "Sage lower endpoint")
    require(sage["upper_endpoint_cap"] == 2_359_100, "Sage upper endpoint")
    require(sage["row_closed"] is False and sage["ledger_movement"] == 0,
            "Sage scope guards")

    toy = validate_toy(manifest)

    run([sys.executable, str(PARENT_PACKET_PATH)])
    run([sys.executable, str(FIXED_G_PACKET_PATH)])
    parent = load(PARENT_MANIFEST_PATH)
    fixed_g = load(FIXED_G_MANIFEST_PATH)
    require(parent["payload_sha256"] == PARENT_PAYLOAD, "parent replay payload")
    require(fixed_g["payload_sha256"] == FIXED_G_PAYLOAD, "fixed-G replay payload")
    return {
        "normal_sha256": sha256_bytes(normal_raw),
        "sage_sha256": sha256_bytes(canonical_json(sage)),
        "toy_sha256": sha256_bytes(canonical_json(toy)),
        "parent_payload": parent["payload_sha256"],
        "fixed_g_payload": fixed_g["payload_sha256"],
        "mutations": tamper["count"],
    }


def validate_local(payload: dict[str, Any], expected: dict[str, Any]) -> None:
    deep_exact(payload, expected)
    require(payload["payload_sha256"] == payload_hash(payload), "payload hash")
    validate_schema(payload)
    validate_sources(payload)
    require(payload["ledger_state"]["movement_from_this_packet"] == 0, "zero movement")
    require(payload["ledger_state"]["row_closed"] is False, "row open")
    require(payload["nonclaims"]["rank_at_least_7_paid"] is False, "high rank open")


def mutation_tests(manifest: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("status", lambda x: x.__setitem__("status", "SAFE")),
        ("terminal", lambda x: x.__setitem__("terminal", "PAID")),
        ("basis", lambda x: x["affine_span_incidence"].__setitem__("basis_inequality", "false")),
        ("rank", lambda x: x["rank_consequences"].__setitem__("rank_1_through_4_excluded", False)),
        ("interval", lambda x: x["fixed_g_endpoint_peeling"].__setitem__("new_unresolved_m_interval", [72_859, 908_270])),
        ("endpoint", lambda x: x["fixed_g_endpoint_peeling"]["upper_endpoint"].__setitem__("total_cap", 2_359_101)),
        ("toy", lambda x: x["toy_census"].__setitem__("deployed_incidence_upper_proved", True)),
        ("ledger", lambda x: x["ledger_state"].__setitem__("movement_from_this_packet", 1)),
        ("closure", lambda x: x["ledger_state"].__setitem__("row_closed", True)),
        ("parent", lambda x: x["dependency_contract"].__setitem__("pairwise_crt_parent_payload_sha256", "0"*64)),
        ("source", lambda x: x["source_bindings"][0].__setitem__("sha256", "0"*64)),
        ("hash", lambda x: x.__setitem__("payload_sha256", "0"*64)),
    ]
    detected: list[str] = []
    for name, mutate in mutations:
        hostile = copy.deepcopy(manifest)
        mutate(hostile)
        if name != "hash":
            hostile["payload_sha256"] = payload_hash(hostile)
        try:
            validate_local(hostile, expected)
        except VerificationError:
            detected.append(name)
        else:
            raise VerificationError(f"packet mutation escaped: {name}")
    require(len(detected) == len(mutations), "all packet mutations detected")
    return detected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    manifest = load(MANIFEST_PATH)
    expected = decode(run([sys.executable, str(PRIMARY_PATH)]), canonical=True)
    validate_local(manifest, expected)
    validate_note()
    if args.tamper_selftest:
        detected = mutation_tests(manifest, expected)
        print(json.dumps({"count": len(detected), "detected": detected}, sort_keys=True))
        return
    replay = validate_replays(manifest)
    require(replay["mutations"] == 21, "replay mutation count")
    sys.stdout.buffer.write(canonical_json(manifest))


try:
    main()
except (VerificationError, OSError, subprocess.SubprocessError) as error:
    print(f"packet verification failed: {error}", file=sys.stderr)
    raise SystemExit(1)
