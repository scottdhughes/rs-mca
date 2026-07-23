#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 rank-seven route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-truncated-weight-flag-route-cut-v1/manifest.json"
)
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank7_truncated_weight_flag_route_cut_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_truncated_weight_flag_route_cut_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_truncated_weight_flag_route_cut_v1.sage"
)
PACKET_PATH = Path(__file__).resolve()
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_truncated_weight_flag_route_cut_v1.md"
)
README_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-truncated-weight-flag-route-cut-v1/README.md"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank6-generalized-weight-codim1-closure-v1/manifest.json"
)
PARENT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank6_generalized_weight_codim_one_closure_v1.md"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank6_generalized_weight_codim1_closure_packet_v1.py"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"
ENDPOINT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_varying_g_affine_span_shortening_route_cut_v1.md"
)
FIXED_G_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_fixed_g_universal_rs_embedding_v1.md"
)

SCHEMA_ID = "m31-rank7-truncated-weight-flag-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_TRUNCATED_WEIGHT_FLAG_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_TRUNCATED_WEIGHT_FLAG_V1"
STATUS = "PROVED_RANK7_TWO_FLANK_ROUTE_CUT_MIDDLE_OPEN"
PARENT_PAYLOAD = (
    "3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9"
)
SOURCE_PREFIX = "M31_RANK7_ROUTE_CUT::"


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
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_hash(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_hash(result)
    return result


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
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
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def run(command: Sequence[str], *, timeout: int = 1200) -> bytes:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    sage_home = Path(environment.get("RS_MCA_SAGE_HOME", "/tmp/rs-mca-sage-home"))
    sage_home.mkdir(parents=True, exist_ok=True)
    environment["HOME"] = str(sage_home)
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    require(
        completed.returncode == 0,
        f"subprocess success: {' '.join(command)}\n"
        f"{completed.stderr.decode(errors='replace')}",
    )
    return completed.stdout


def source_specifications() -> list[tuple[str, Path, str | None, str]]:
    return [
        ("packet_schema", SCHEMA_PATH, None, "Closed packet schema."),
        ("primary_exact_replay", PRIMARY_PATH, None, "Exact Python rank-seven exhaustion."),
        ("independent_sage_replay", SAGE_PATH, None, "Independent arithmetic and GF(11) sharpness control."),
        ("packet_verifier", PACKET_PATH, None, "Fail-closed packet and mutation replay."),
        ("theorem_note", NOTE_PATH, None, "Proof and exact source-bound residual statement."),
        ("packet_readme", README_PATH, None, "Replay and nonclaim instructions."),
        ("parent_manifest", PARENT_MANIFEST_PATH, PARENT_PAYLOAD, "Sealed rank-six closure dependency."),
        ("parent_note", PARENT_NOTE_PATH, None, "Immediate parent theorem and source definitions."),
        ("parent_packet_verifier", PARENT_PACKET_PATH, None, "Fail-closed predecessor replay."),
        ("grande_finale_compilers", GRANDE_FINALE_PATH, None, "Affine-fiber, Johnson, saturation, and codimension-one sources."),
        ("fixed_g_endpoint_source", ENDPOINT_NOTE_PATH, None, "Fixed-G Johnson wings and endpoint peeling."),
        ("fixed_g_embedding_source", FIXED_G_NOTE_PATH, None, "Universal deterministic ordinary-RS obstruction."),
    ]


def source_bindings() -> list[dict[str, Any]]:
    bindings = []
    for role, path, internal, scope in source_specifications():
        relative = path.relative_to(ROOT).as_posix()
        bindings.append(
            {
                "binding_id": SOURCE_PREFIX + role,
                "internal_payload_sha256": internal,
                "path": relative,
                "role": role,
                "scope": scope,
                "sha256": sha256_path(path),
            }
        )
    return bindings


def build_expected() -> tuple[dict[str, Any], bytes, bytes]:
    normal = run([sys.executable, str(PRIMARY_PATH), "--check"])
    optimized = run([sys.executable, "-O", str(PRIMARY_PATH), "--check"])
    require(normal == optimized, "primary normal/optimized parity")
    primary = decode(normal, canonical=True)
    primary.pop("payload_sha256", None)
    primary["source_bindings"] = source_bindings()
    return seal(primary), normal, optimized


def validate_schema(payload: dict[str, Any]) -> None:
    schema = load(SCHEMA_PATH, canonical=False)
    require(schema.get("additionalProperties") is False, "closed top-level schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(properties) == set(required), "schema exact keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const: {key}")


def validate_semantics(payload: dict[str, Any]) -> None:
    require(payload["payload_sha256"] == payload_hash(payload), "payload seal")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["theorem_id"] == THEOREM_ID, "theorem id")
    require(payload["architecture"] == ARCHITECTURE_ID, "architecture id")
    require(payload["status"] == STATUS, "status")
    require(payload["parent_payload_sha256"] == PARENT_PAYLOAD, "parent pin")

    weights = payload["truncated_weight_compiler"]
    require(weights["maximum_q6"] == 242_225, "q6 maximum")
    require(weights["maximum_d6"] == 1_290_807, "d6 maximum")
    require(weights["maximum_q6_unions"] == [309_679, 309_680, 309_681], "q6 plateau")
    require(weights["minimum_profile_interpolation_margin"] == 27_562, "interpolation margin")
    require(weights["rank7_union_values_exhausted"] == 1_048_570, "union sweep")

    flanks = payload["rank7_flanks"]
    require(flanks["common_zero_johnson_paid_range"] == [67_454, 72_427], "Johnson flank")
    require(flanks["codimension_one_paid_range"] == [354_999, 1_116_023], "codim flank")
    require(flanks["primitive_rank7_union_range"] == [72_428, 354_998], "primitive interval")
    require(flanks["primitive_union_count"] == 282_571, "primitive count")
    require(flanks["last_codim_failure"] == 15_776_141, "last failure")
    require(flanks["first_codim_payment"] == 15_775_924, "first payment")

    owners = payload["owner_partition"]
    require(owners["low_mixed_g_sliver"] == [72_428, 72_859], "mixed sliver")
    require(owners["minimum_distinct_G_floors"] == {"72428": 86_208, "72858": 91, "72859": 7}, "locator floors")
    require(owners["ordinary_rs_middle_overlap"]["union_range"] == [72_860, 354_998], "ordinary RS overlap")

    impact = payload["impact"]
    require(impact == {"ledger_movement": 0, "official_endpoint_movement": 0, "rank7_closed": False, "rank8_and_above_closed": False, "row_closed": False}, "honest impact")


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload["source_bindings"]
    require(type(bindings) is list and len(bindings) == 12, "source count")
    expected = source_bindings()
    deep_exact(bindings, expected, "source_bindings")
    parent = load(PARENT_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent internal payload")


def validate_sage(raw: bytes) -> dict[str, Any]:
    sage = decode(raw, canonical=True)
    require(sage["deployed"]["maximum_q6"] == 242_225, "Sage q6")
    require(sage["deployed"]["last_johnson_paid"] == [72_427, 4_735_771], "Sage Johnson")
    require(sage["deployed"]["last_codim_unpaid"] == [354_998, 15_776_141], "Sage failure")
    require(sage["deployed"]["first_codim_paid"] == [354_999, 15_775_924], "Sage payment")
    require(sage["toy_gf11"]["list_size"] == 330, "Sage toy list")
    require(sage["toy_gf11"]["span_rank"] == 7, "Sage toy rank")
    require(sage["toy_gf11"]["truncated_equalities"] == 7, "Sage toy sharpness")
    require(sage["impact"]["rank7_closed"] is False, "Sage honest scope")
    return sage


def verify_full() -> dict[str, Any]:
    expected, normal, optimized = build_expected()
    manifest = load(MANIFEST_PATH)
    deep_exact(manifest, expected)
    validate_schema(manifest)
    validate_semantics(manifest)
    validate_sources(manifest)

    tamper_normal = run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"])
    tamper_optimized = run([sys.executable, "-O", str(PRIMARY_PATH), "--tamper-selftest"])
    require(tamper_normal == tamper_optimized, "primary tamper parity")
    tamper = decode(tamper_normal, canonical=True)
    require(tamper["mutations"] == tamper["detected"] == 15, "primary mutations")

    sage_raw = run(["sage", str(SAGE_PATH)])
    sage = validate_sage(sage_raw)
    run([sys.executable, str(PARENT_PACKET_PATH)])

    return {
        "schema": "m31-rank7-truncated-weight-flag-packet-replay-v1",
        "checks": CHECKS + 1,
        "payload_sha256": manifest["payload_sha256"],
        "primary_sha256": sha256_bytes(normal),
        "primary_normal_equals_optimized": normal == optimized,
        "primary_mutations_detected": tamper["detected"],
        "primary_tamper_normal_equals_optimized": tamper_normal == tamper_optimized,
        "sage_checks": sage["checks"],
        "sage_sha256": sha256_bytes(sage_raw),
        "source_bindings": len(manifest["source_bindings"]),
        "parent_payload_sha256": PARENT_PAYLOAD,
        "rank7_closed": False,
        "row_closed": False,
        "ledger_movement": 0,
    }


def packet_tamper_selftest() -> dict[str, Any]:
    expected, _, _ = build_expected()
    semantic_mutations = [
        (("row", "shallow_size"), 15_775_934),
        (("truncated_weight_compiler", "maximum_q6"), 242_226),
        (("rank7_flanks", "primitive_union_count"), 282_570),
        (("rank7_flanks", "last_codim_failure"), 15_776_140),
        (("rank7_flanks", "first_codim_payment"), 15_775_925),
        (("owner_partition", "low_mixed_g_sliver"), [72_429, 72_859]),
        (("owner_partition", "fixed_g_endpoint_peeling_cap"), 2_310_491),
        (("owner_partition", "minimum_distinct_G_floors", "72428"), 86_207),
        (("impact", "rank7_closed"), True),
        (("impact", "ledger_movement"), 1),
        (("parent_payload_sha256",), "0" * 64),
        (("payload_sha256",), "0" * 64),
    ]
    detected = 0
    for path, value in semantic_mutations:
        mutant = copy.deepcopy(expected)
        cursor: Any = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        try:
            deep_exact(mutant, expected)
        except VerificationError:
            detected += 1
        else:
            raise VerificationError(f"semantic mutation escaped: {path}")

    hostile = [
        b'{"a":1,"a":2}\n',
        b'{"a":1.5}\n',
        b'{"a":NaN}\n',
        b'{ "a":1}\n',
    ]
    hostile_detected = 0
    for raw in hostile:
        try:
            decode(raw, canonical=True)
        except VerificationError:
            hostile_detected += 1
        else:
            raise VerificationError("hostile parser mutation escaped")
    require(detected == len(semantic_mutations), "packet semantic mutations")
    require(hostile_detected == len(hostile), "packet hostile mutations")
    return {
        "schema": "m31-rank7-truncated-weight-flag-packet-tamper-v1",
        "semantic_mutations": len(semantic_mutations),
        "semantic_detected": detected,
        "hostile_mutations": len(hostile),
        "hostile_detected": hostile_detected,
        "all_detected": True,
        "base_payload_sha256": expected["payload_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write_manifest:
            expected, _, _ = build_expected()
            MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST_PATH.write_bytes(canonical_json(expected))
            print(expected["payload_sha256"])
            return 0
        result = packet_tamper_selftest() if args.tamper_selftest else verify_full()
        sys.stdout.buffer.write(canonical_json(result))
        return 0
    except (VerificationError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
