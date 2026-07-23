#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 rank-six closure."""

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
MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank6-generalized-weight-codim1-closure-v1/manifest.json"
)
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank6_generalized_weight_codim1_closure_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank6_generalized_weight_codim1_closure_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank6_generalized_weight_codim1_closure_v1.sage"
)
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank6_generalized_weight_codim_one_closure_v1.md"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-varying-g-first-pivot-basis-route-cut-v1/manifest.json"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"

SCHEMA_ID = "m31-rank6-generalized-weight-codim1-closure-summary-v1"
THEOREM_ID = "M31_RANK6_GENERALIZED_WEIGHT_CODIM_ONE_CLOSURE_V1"
ARCHITECTURE_ID = (
    "M31_BASE_FIELD_BOUNDARY_RANK6_WEIGHT_HIERARCHY_CODIM_ONE_COMPILER_V1"
)
ARTIFACT_KIND = (
    "EXACT_GENERALIZED_WEIGHT_MARKED_LINE_AND_CODIMENSION_ONE_RANK6_CLOSURE"
)
STATUS = "PROVED_BASE_FIELD_BOUNDARY_SHALLOW_RANK6_EXCLUDED_RANK_GE7_OPEN"
TERMINAL = "UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE"
PARENT_PAYLOAD = (
    "28f18608d3552ffe42e6dc8fcb6c03c1338fd349e1d52a0a3f52de6629bcbf6b"
)
PRIMARY_MUTATIONS = 22


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
        return (
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON") from exc


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def payload_hash(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_hash(result)
    return result


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


def run(command: Sequence[str], *, timeout: int = 900) -> bytes:
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
    require(set(payload) == set(properties) == set(required), "schema exact keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const: {key}")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["theorem_id"] == THEOREM_ID, "theorem id")
    require(payload["architecture_id"] == ARCHITECTURE_ID, "architecture id")
    require(payload["artifact_kind"] == ARTIFACT_KIND, "artifact kind")
    require(payload["status"] == STATUS, "status")
    require(payload["terminal"] == TERMINAL, "terminal")


def validate_semantics(payload: dict[str, Any]) -> None:
    require(payload.get("payload_sha256") == payload_hash(payload), "payload seal")
    deployed = payload["deployed_parameters"]
    require(deployed["shallow_size"] == 15_775_933, "shallow size")
    require(deployed["rank6_parent_union_interval"] == [781_458, 1_033_227], "g window")
    require(deployed["affine_line_multiplicity"] == 15, "line multiplicity")

    weights = payload["generalized_weight_refinement"]
    require(weights["q5_ceiling"] == 32_004, "q5 ceiling")
    require(weights["q5_successor_slack"] < 0, "q5 successor rejected")
    require(weights["d5_range"] == [1_048_581, 1_080_585], "d5 range")
    require(weights["union_values_exhausted"] == 251_770, "g sweep count")

    compiler = payload["codimension_one_compiler"]
    require(compiler["support_saturated"] is True, "support saturation")
    require(
        compiler["parameter_map"]["outside_common_mismatch"] == "b_0=eta",
        "b0 orientation",
    )
    require(
        compiler["parameter_map"]["support_layer"] == "Delta=d_6-d_5",
        "support-layer orientation",
    )
    require(
        compiler["profile_interpolation"]["uniform_margin"] == 170_336,
        "profile interpolation margin",
    )
    require(compiler["whole_chart_upper"] == 908_116, "whole-chart upper")
    require(compiler["contradiction_gap"] == 14_867_817, "contradiction gap")

    consequence = payload["rank_consequence"]
    require(consequence["rank_6_excluded_by_this_packet"] is True, "rank six closed")
    require(consequence["minimum_surviving_rank"] == 7, "surviving rank")
    require(consequence["whole_rank6_chart_upper"] == 908_116, "consequence upper")

    ledger = payload["ledger_state"]
    require(ledger["movement_from_this_packet"] == 0, "zero movement")
    require(ledger["row_closed"] is False, "row open")
    require(ledger["rank6_route_closed"] is True, "rank6 route closed")
    require(payload["nonclaims"]["rank7_or_higher_paid"] is False, "rank7 open")
    require(payload["toy_controls"]["deployed_evidence"] is False, "toy not deployed")
    require(
        payload["dependency_contract"]["parent_payload_sha256"] == PARENT_PAYLOAD,
        "parent dependency pin",
    )


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload.get("source_bindings")
    require(type(bindings) is list and len(bindings) == 10, "source binding count")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in bindings:
        require(type(binding) is dict, "source binding object")
        require(
            set(binding)
            == {
                "binding_id",
                "role",
                "path",
                "sha256",
                "internal_payload_sha256",
                "scope",
            },
            "source binding keys",
        )
        binding_id = binding["binding_id"]
        path_text = binding["path"]
        require(type(binding_id) is str and binding_id not in seen_ids, "unique binding id")
        require(type(path_text) is str and not path_text.startswith("/"), "relative source path")
        require(".." not in Path(path_text).parts, "source traversal forbidden")
        require(path_text not in seen_paths, "source path unique")
        seen_ids.add(binding_id)
        seen_paths.add(path_text)
        path = ROOT / path_text
        require(path.is_file(), f"bound source exists: {path_text}")
        require(sha256_bytes(path.read_bytes()) == binding["sha256"], f"fresh hash: {path_text}")
        if binding["role"] == "parent_manifest":
            parent = load(path)
            require(
                binding["internal_payload_sha256"] == parent["payload_sha256"] == PARENT_PAYLOAD,
                "parent internal payload",
            )
        else:
            require(binding["internal_payload_sha256"] is None, "nonmanifest internal pin null")


def validate_note_and_theorem_source() -> None:
    require(NOTE_PATH.is_file(), "theorem note exists")
    note = NOTE_PATH.read_text(encoding="utf-8")
    note_anchors = (
        "sum_i (g+s_i) prod_{j=2}^5 (w+eta+j+q_j+s_i)",
        "q_5 <= 32,004",
        "1,048,581 <= d_5(W_c) <= 1,080,585",
        "outside common mismatch b_0 | eta",
        "4Q-A_profile >= 170,336+3 eta",
        "908,116",
        "15,775,933-908,116=14,867,817",
        TERMINAL,
        "ledger movement=0",
    )
    for anchor in note_anchors:
        require(anchor in note, f"theorem-note anchor: {anchor}")

    require(GRANDE_FINALE_PATH.is_file(), "Grande Finale theorem source exists")
    source = GRANDE_FINALE_PATH.read_text(encoding="utf-8")
    source_anchors = (
        r"\label{thm:codim-one-recursion}",
        r"\label{lem:codim-one-profile-interpolation}",
        r"\label{cor:codim-one-mds-soft}",
        r"\label{lem:weight-minimizer-saturated}",
        r"\frac{d^{\underline j}}{\Pi_0}+",
    )
    for anchor in source_anchors:
        require(anchor in source, f"Grande Finale source anchor: {anchor}")


def validate_sage(manifest: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    raw = run(["/usr/local/bin/sage", str(SAGE_PATH)])
    summary = decode(raw, canonical=False)
    require(summary["status"] == "EXACT_INDEPENDENT_SAGE_CONTROL", "Sage status")
    require(summary["theorem_id"] == THEOREM_ID, "Sage theorem")
    deployed = summary["deployed"]
    weights = manifest["generalized_weight_refinement"]
    compiler = manifest["codimension_one_compiler"]
    require(deployed["union_values_exhausted"] == weights["union_values_exhausted"], "Sage g sweep")
    require(deployed["q5_ceiling"] == weights["q5_ceiling"], "Sage q5")
    require(deployed["q5_cap_slack"] == weights["q5_cap_slack"], "Sage q5 slack")
    require(deployed["q5_successor_slack"] == weights["q5_successor_slack"], "Sage q5 successor")
    require(deployed["d5_range"] == weights["d5_range"], "Sage d5 range")
    require(
        deployed["profile_interpolation_margin"]
        == compiler["profile_interpolation"]["uniform_margin"],
        "Sage interpolation margin",
    )
    require(deployed["old_support_maximum"] == compiler["old_support_maximum"], "Sage old term")
    require(deployed["new_layer_maximum"] == compiler["new_layer_maximum"], "Sage new term")
    require(deployed["mixed_majorant"] == compiler["mixed_majorant"], "Sage mixed term")
    require(deployed["whole_chart_upper"] == compiler["whole_chart_upper"], "Sage chart upper")
    require(deployed["contradiction_gap"] == compiler["contradiction_gap"], "Sage gap")

    toy = summary["toy_GF7"]
    certified_toy = manifest["toy_controls"]
    for key in (
        "whole_list_size",
        "affine_span_rank",
        "d5",
        "d6",
        "support_layer",
        "compiler_old_resource",
        "compiler_new_resource",
        "compiler_bound",
        "marked_line_left",
        "marked_line_right",
        "deployed_evidence",
    ):
        require(toy[key] == certified_toy[key], f"Sage toy {key}")
    require(toy["support_saturated"] is True, "Sage toy saturation")
    require(toy["maximum_affine_line_multiplicity"] == 2, "Sage toy line multiplicity")
    return summary, raw


def parser_hostile_tests() -> list[str]:
    detected: list[str] = []
    cases = (
        ("duplicate-key", b'{"x":1,"x":2}\n', False),
        ("float", b'{"x":1.5}\n', False),
        ("nonfinite", b'{"x":NaN}\n', False),
        ("noncanonical", b'{ "x": 1 }\n', True),
    )
    for name, raw, canonical in cases:
        try:
            decode(raw, canonical=canonical)
        except VerificationError:
            detected.append(name)
    require(len(detected) == len(cases), "all hostile parser cases detected")
    return detected


def tamper_selftest(manifest: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("q5", lambda value: value["generalized_weight_refinement"].__setitem__("q5_ceiling", 32_005)),
        ("d5", lambda value: value["generalized_weight_refinement"]["d5_range"].__setitem__(1, 1_080_586)),
        ("b0", lambda value: value["codimension_one_compiler"]["parameter_map"].__setitem__("outside_common_mismatch", "b_0=0")),
        ("layer", lambda value: value["codimension_one_compiler"]["parameter_map"].__setitem__("support_layer", "Delta=d_5-d_6")),
        ("interpolation", lambda value: value["codimension_one_compiler"]["profile_interpolation"].__setitem__("uniform_margin", 0)),
        ("floor", lambda value: value["codimension_one_compiler"].__setitem__("whole_chart_upper", 908_117)),
        ("rank6", lambda value: value["rank_consequence"].__setitem__("rank_6_excluded_by_this_packet", False)),
        ("rank7", lambda value: value["nonclaims"].__setitem__("rank7_or_higher_paid", True)),
        ("toy", lambda value: value["toy_controls"].__setitem__("deployed_evidence", True)),
        ("ledger", lambda value: value["ledger_state"].__setitem__("movement_from_this_packet", 1)),
        ("row", lambda value: value["ledger_state"].__setitem__("row_closed", True)),
        ("parent", lambda value: value["dependency_contract"].__setitem__("parent_payload_sha256", "0" * 64)),
        ("source", lambda value: value["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("alias", lambda value: value["source_bindings"][1].__setitem__("path", value["source_bindings"][0]["path"])),
        ("seal", lambda value: value.__setitem__("payload_sha256", "0" * 64)),
    ]
    detected: list[str] = []
    for name, mutate in mutations:
        changed = copy.deepcopy(manifest)
        mutate(changed)
        if name != "seal":
            changed = seal(changed)
        try:
            validate_schema(changed)
            validate_semantics(changed)
            validate_sources(changed)
            deep_exact(changed, expected, "tampered")
        except (VerificationError, KeyError, TypeError, IndexError):
            detected.append(name)
    require(len(detected) == len(mutations), "all packet mutations detected")
    parser = parser_hostile_tests()
    return {
        "semantic_count": len(detected),
        "semantic_detected": detected,
        "parser_count": len(parser),
        "parser_detected": parser,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    manifest = load(MANIFEST_PATH)
    validate_schema(manifest)
    validate_semantics(manifest)
    validate_sources(manifest)
    validate_note_and_theorem_source()

    primary_normal_raw = run([sys.executable, str(PRIMARY_PATH)])
    primary_optimized_raw = run([sys.executable, "-O", str(PRIMARY_PATH)])
    require(primary_normal_raw == primary_optimized_raw, "normal equals optimized primary")
    primary = decode(primary_normal_raw, canonical=True)
    deep_exact(primary, manifest, "primary_vs_manifest")

    if args.tamper_selftest:
        result = tamper_selftest(manifest, primary)
        result["status"] = STATUS
        print(json.dumps(result, sort_keys=True, indent=2))
        return

    primary_tamper_raw = run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"])
    primary_tamper_optimized_raw = run(
        [sys.executable, "-O", str(PRIMARY_PATH), "--tamper-selftest"]
    )
    require(
        primary_tamper_raw == primary_tamper_optimized_raw,
        "normal equals optimized primary tamper replay",
    )
    primary_tamper = decode(primary_tamper_raw, canonical=False)
    require(primary_tamper["count"] == PRIMARY_MUTATIONS, "primary mutation count")
    require(len(primary_tamper["detected"]) == PRIMARY_MUTATIONS, "primary mutations detected")

    sage_summary, sage_raw = validate_sage(manifest)

    parent = load(PARENT_MANIFEST_PATH)
    require(parent["payload_sha256"] == PARENT_PAYLOAD, "parent manifest pin")
    parent_raw = run([sys.executable, str(PARENT_PACKET_PATH)])

    summary = {
        "schema": "m31-rank6-generalized-weight-codim1-closure-packet-replay-v1",
        "status": STATUS,
        "terminal": TERMINAL,
        "payload_sha256": manifest["payload_sha256"],
        "whole_chart_upper": manifest["codimension_one_compiler"]["whole_chart_upper"],
        "contradiction_gap": manifest["codimension_one_compiler"]["contradiction_gap"],
        "primary_normal_equals_optimized": True,
        "primary_output_sha256": sha256_bytes(primary_normal_raw),
        "primary_mutations_detected": PRIMARY_MUTATIONS,
        "primary_tamper_normal_equals_optimized": True,
        "sage_output_sha256": sha256_bytes(sage_raw),
        "sage_checks": sage_summary["checks"],
        "parent_output_sha256": sha256_bytes(parent_raw),
        "source_bindings": len(manifest["source_bindings"]),
        "ledger_movement": 0,
        "row_closed": False,
        "checks": CHECKS,
    }
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
