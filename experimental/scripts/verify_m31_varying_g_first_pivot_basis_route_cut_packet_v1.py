#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 first-pivot basis route cut.

The packet independently checks the canonical manifest and closed schema,
fresh source hashes, theorem-note anchors, normal/optimized/tamper primary
replays, the Sage arithmetic and finite-field control, and the sealed parent
packet.  It proves no global M31 LIST bound and moves no v4 ledger atom.
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
MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-varying-g-first-pivot-basis-route-cut-v1/manifest.json"
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_varying_g_first_pivot_basis_route_cut_v1.schema.json"
PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_varying_g_first_pivot_basis_route_cut_v1.md"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_packet_v1.py"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/manifest.json"

SCHEMA_ID = "m31-varying-g-first-pivot-basis-route-cut-summary-v1"
THEOREM_ID = "M31_VARYING_G_FIRST_PIVOT_BASIS_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_FIRST_PIVOT_BASIS_V1"
ARTIFACT_KIND = "EXACT_MARKED_BASIS_AND_AGGREGATE_ROUTE_CUT"
STATUS = "PROVED_MARKED_BASIS_RANK5_CUT_RANK6_WINDOW_OPEN"
TERMINAL = "UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE"
PARENT_PAYLOAD = "78a6b51d69736b574d258df9e20d84155b8be86e51db942bc6c02a710ee7866d"
TOY_SHA256 = "2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9"


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
        value = json.loads(
            raw.decode("ascii"),
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


def run(command: Sequence[str], *, timeout: int = 600) -> bytes:
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


def validate_schema(payload: dict[str, Any]) -> None:
    schema = load(SCHEMA_PATH, canonical=False)
    require(schema.get("additionalProperties") is False, "closed top-level schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(properties) == set(required), "schema exact top-level keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const: {key}")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["theorem_id"] == THEOREM_ID, "theorem id")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "architecture id")
    require(payload["artifact_kind"] == ARTIFACT_KIND, "artifact kind")
    require(payload["status"] == STATUS, "status")
    require(payload["terminal"] == TERMINAL, "terminal")


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload.get("source_bindings")
    require(type(bindings) is list and len(bindings) == 8, "source binding count")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in bindings:
        require(type(binding) is dict, "source binding object")
        require(set(binding) == {"binding_id", "role", "path", "sha256"},
                "source binding keys")
        binding_id = binding["binding_id"]
        path_text = binding["path"]
        require(type(binding_id) is str and binding_id not in seen_ids,
                "source binding id unique")
        require(type(path_text) is str and not path_text.startswith("/"),
                "relative source path")
        require(".." not in Path(path_text).parts, "source traversal forbidden")
        require(path_text not in seen_paths, "source path unique")
        seen_ids.add(binding_id)
        seen_paths.add(path_text)
        path = ROOT / path_text
        require(path.is_file(), f"bound source exists: {path_text}")
        require(sha256_bytes(path.read_bytes()) == binding["sha256"],
                f"fresh source hash: {path_text}")


def validate_note() -> None:
    require(NOTE_PATH.is_file(), "theorem note exists")
    text = NOTE_PATH.read_text(encoding="utf-8")
    anchors = (
        r"sum_{i\in I}(g+s_i)",
        r"(w+s_i+r+e-1)_{\underline{r-1}}",
        r"\boxed{r\ge6}",
        r"781,458\le g\le1,033,227",
        "96,161,189,784",
        "UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE",
        "2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9",
        "ledger movement}=0",
        "not a row closure",
    )
    for anchor in anchors:
        require(anchor in text, f"theorem-note anchor: {anchor}")


def validate_sage(manifest: dict[str, Any]) -> dict[str, Any]:
    summary = decode(run(["/usr/local/bin/sage", str(SAGE_PATH)]), canonical=False)
    require(summary["status"] == "EXACT_INDEPENDENT_SAGE_CONTROL", "Sage status")
    thresholds = summary["deployed_thresholds"]
    consequences = manifest["rank_consequences"]
    require(summary["rank_caps_1_5"] == [15, 241, 3_757, 58_410, 1_756_141],
            "Sage rank caps")
    deep_exact(thresholds["rank_1_through_5"],
               consequences["worst_case_zero_excess_caps"],
               "sage.rank_1_through_5")
    deep_exact(thresholds["rank6_first_pivot"],
               consequences["rank6_first_pivot_threshold"],
               "sage.rank6_first_pivot")
    deep_exact(thresholds["rank6_affine_line"],
               consequences["rank6_affine_line_threshold"],
               "sage.rank6_affine_line")
    deep_exact(thresholds["rank6_cross_block"],
               consequences["rank6_cross_block_threshold"],
               "sage.rank6_cross_block")
    require(summary["rank6_surviving_union_interval"] == [781_458, 1_033_227],
            "Sage rank6 interval")
    require(summary["rank6_combined_excess"] == 96_161_189_784,
            "Sage rank6 excess")
    sage_excess = summary["deployed_excess_sweeps"]
    rank6 = sage_excess["rank6_combined"]
    certified_rank6 = consequences["rank6_combined_excess"]
    require(rank6["total_excess_ceiling"] == certified_rank6["total_excess_ceiling"],
            "Sage rank6 total")
    require(rank6["maximizing_union"] == certified_rank6["maximizing_union"],
            "Sage rank6 maximizing union")
    require(rank6["line_ceiling"] == certified_rank6["line_ceiling"],
            "Sage rank6 line ceiling")
    require(rank6["cross_ceiling"] == certified_rank6["cross_ceiling"],
            "Sage rank6 cross ceiling")
    require(rank6["line_base_excess"] == certified_rank6["base_excess_q"]
            == rank6["cross_base_excess"], "Sage rank6 balanced bases")
    require(rank6["line_entries_raised"] == certified_rank6["line_entries_raised"],
            "Sage rank6 line histogram")
    require(rank6["cross_entries_raised"] == certified_rank6["cross_entries_raised"],
            "Sage rank6 cross histogram")
    require(rank6["union_values_exhausted"] == 251_770,
            "Sage rank6 exhaustive union count")
    require(rank6["cross_endpoint"] == "m=R-s", "Sage exact cross endpoint")

    sage_high = sage_excess["rank7_through_12"]
    certified_high = consequences["rank7_through_12_first_pivot_excess"]
    require(len(sage_high) == len(certified_high) == 6, "Sage high-rank row count")
    high_keys = (
        "rank", "total_excess_ceiling", "maximizing_union", "base_excess_q",
        "entries_raised_to_q_plus_1", "uniform_cut",
        "first_union_permitting_full_shallow_ceiling",
    )
    for sage_row, certified_row in zip(sage_high, certified_high, strict=True):
        for key in high_keys:
            require(sage_row[key] == certified_row[key],
                    f"Sage rank {sage_row['rank']} field {key}")
        require(sage_row["union_values_exhausted"]
                == 1_116_023 - (67_447 + sage_row["rank"]) + 1,
                f"Sage rank {sage_row['rank']} exhaustive union count")
    deep_exact(sage_excess["rank12_adjacent_full_caps"],
               consequences["rank12_adjacent_full_caps"],
               "sage.rank12_adjacent_full_caps")

    deep_exact(summary["aggregate_route_cut"], manifest["aggregate_route_cut"],
               "sage.aggregate_route_cut")
    toy = summary["toy_sharpness"]
    require(toy["field"] == 17 and toy["family_size"] == 90, "Sage toy size")
    require(toy["rank"] == 12 and toy["g"] == 12 and toy["e"] == 0,
            "Sage toy rank data")
    require(toy["distinct_G"] == 78 and toy["max_fixed_G"] == 2,
            "Sage toy locator data")
    require(toy["Wronskian_pairs"] == 4_005, "Sage Wronskian census")
    require(toy["basis_capacity"] == 91, "Sage toy basis capacity")
    require(toy["first_pivot_slack"] == 479_001_600, "Sage first-pivot slack")
    require(toy["marked_E_slack"] == 0, "Sage marked-E equality")
    require(toy["canonical_family_sha256"] == TOY_SHA256, "Sage family digest")
    require(toy["bad_ratio_removed"] == 13, "Sage bad-ratio mutation")
    require(toy["received_tables_exhausted"] == 256, "Sage received-table census")
    require(toy["received_table_size_histogram"] == {"77": 192, "90": 64},
            "Sage received-table histogram")
    require(toy["inequalities"]["basis"] == {"lhs": 90, "rhs": 91, "slack": 1},
            "Sage predecessor basis sharpness")
    require(toy["inequalities"]["cross_block"]
            == {"lhs": 1_584, "rhs": 1_584, "slack": 0},
            "Sage cross-block equality")
    require(manifest["toy_sharpness"]["canonical_family_sha256"] == TOY_SHA256,
            "manifest toy digest")
    require(summary["row_closed"] is False and summary["ledger_movement"] == 0,
            "Sage scope guards")
    require(summary["scope"]["toy_family_is_deployed_evidence"] is False,
            "Sage toy scope")
    require(summary["scope"]["deployed_union_ranges_exhausted"] is True,
            "Sage exhaustive scope")
    return summary


def validate_local(payload: dict[str, Any], expected: dict[str, Any]) -> None:
    deep_exact(payload, expected)
    require(payload["payload_sha256"] == payload_hash(payload), "payload hash")
    validate_schema(payload)
    validate_sources(payload)
    require(payload["rank_consequences"]["rank_1_through_5_excluded"] is True,
            "rank one through five excluded")
    require(payload["rank_consequences"]["rank6_surviving_union_interval"]
            == [781_458, 1_033_227], "rank6 interval")
    require(payload["rank_consequences"]["rank6_combined_excess"]
            ["total_excess_ceiling"] == 96_161_189_784, "rank6 excess")
    require(payload["aggregate_route_cut"]["realized_polynomial_family"] is False,
            "scalar profile is not realized")
    require(payload["ledger_state"]["movement_from_this_packet"] == 0,
            "zero ledger movement")
    require(payload["ledger_state"]["row_closed"] is False, "row remains open")
    require(payload["nonclaims"]["rank6_paid"] is False, "rank6 remains unpaid")


def validate_replays(manifest: dict[str, Any]) -> dict[str, Any]:
    normal_raw = run([sys.executable, str(PRIMARY_PATH)])
    optimized_raw = run([sys.executable, "-O", str(PRIMARY_PATH)])
    require(normal_raw == optimized_raw, "normal equals optimized primary")
    primary = decode(normal_raw, canonical=True)
    deep_exact(primary, manifest, "primary_manifest")

    tamper = decode(
        run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"]),
        canonical=False,
    )
    require(tamper["count"] == 19 and len(tamper["detected"]) == 19,
            "primary mutations detected")

    sage = validate_sage(manifest)
    run([sys.executable, str(PARENT_PACKET_PATH)])
    parent = load(PARENT_MANIFEST_PATH)
    require(parent["payload_sha256"] == PARENT_PAYLOAD, "parent replay payload")
    require(manifest["dependency_contract"]["parent_payload_sha256"] == PARENT_PAYLOAD,
            "manifest parent payload")
    return {
        "normal_sha256": sha256_bytes(normal_raw),
        "sage_sha256": sha256_bytes(canonical_json(sage)),
        "parent_payload": parent["payload_sha256"],
        "primary_mutations": tamper["count"],
    }


def mutation_tests(manifest: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("status", lambda x: x.__setitem__("status", "SAFE")),
        ("terminal", lambda x: x.__setitem__("terminal", "PAID")),
        ("rank5", lambda x: x["rank_consequences"].__setitem__(
            "rank_1_through_5_excluded", False)),
        ("rank6-low", lambda x: x["rank_consequences"]
         ["rank6_surviving_union_interval"].__setitem__(0, 781_457)),
        ("rank6-high", lambda x: x["rank_consequences"]
         ["rank6_surviving_union_interval"].__setitem__(1, 1_033_228)),
        ("excess", lambda x: x["rank_consequences"]["rank6_combined_excess"]
         .__setitem__("total_excess_ceiling", 96_161_189_785)),
        ("line", lambda x: x["marked_basis_theorem"].__setitem__(
            "affine_line_multiplicity", 16)),
        ("scalar", lambda x: x["aggregate_route_cut"].__setitem__(
            "realized_polynomial_family", True)),
        ("toy", lambda x: x["toy_sharpness"].__setitem__(
            "deployed_bound_proved", True)),
        ("ledger", lambda x: x["ledger_state"].__setitem__(
            "movement_from_this_packet", 1)),
        ("closure", lambda x: x["ledger_state"].__setitem__("row_closed", True)),
        ("parent", lambda x: x["dependency_contract"].__setitem__(
            "parent_payload_sha256", "0" * 64)),
        ("source", lambda x: x["source_bindings"][0].__setitem__(
            "sha256", "0" * 64)),
        ("hash", lambda x: x.__setitem__("payload_sha256", "0" * 64)),
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
    require(replay["primary_mutations"] == 19, "primary mutation count")
    sys.stdout.buffer.write(canonical_json(manifest))


try:
    main()
except (VerificationError, OSError, subprocess.SubprocessError) as error:
    print(f"packet verification failed: {error}", file=sys.stderr)
    raise SystemExit(1)
