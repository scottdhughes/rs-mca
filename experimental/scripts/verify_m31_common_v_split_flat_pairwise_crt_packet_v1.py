#!/usr/bin/env python3
"""Verify the M31 common-V split-flat/pairwise-CRT packet.

The packet certifies an exact fixed-``H`` affine atlas and an exact criterion
for realizing full gcd locators by one common unit modulo ``L0``.  It is a
route cut: it does not prove the remaining global split rational-function
incidence bound, move a Grande Finale v4 atom, or close the M31 LIST row.

All gates use explicit exceptions and remain active under ``python -O``.
The verifier checks canonical JSON, a closed top-level schema, fresh source
hashes, internal predecessor payload pins, theorem-note anchors, independent
normal/optimized/tamper replays of the standard-library verifier, a Sage
finite-field replay, predecessor replays, and hostile packet mutations.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Sequence


SCHEMA_DOC_ID = "rs-mca-m31-common-v-split-flat-pairwise-crt-equivalence-v1"
SCHEMA_ID = "m31-common-v-pairwise-crt-equivalence-summary-v1"
THEOREM_ID = "M31_COMMON_V_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1"
ARTIFACT_KIND = "EXACT_SPLIT_FLAT_ATLAS_AND_PAIRWISE_COMMON_V_CRT_EQUIVALENCE_ROUTE_CUT"
STATUS = "PROVED_PAIRWISE_CRT_EQUIVALENCE_SPLIT_FLAT_ATLAS_GLOBAL_INCIDENCE_OPEN"
TERMINAL = "UNPAID_PAIRWISE_SPLIT_RATIONAL_FUNCTION_DIVISOR_INCIDENCE"

PARENT_PAYLOAD = "fcc630ba68c803bb67378f836a84e6bdbcefe7fd9d5b468ef48fe919bd8307e3"
ANCHOR_EXCHANGE_PAYLOAD = "bf38cbae247269196395c61aeae3e9fa8b72f92ffc0b0af4650e96e98d66eb6e"
PARENT_THEOREM = "M31_BOUNDARY_COMMON_V_CROSS_G_ROUTE_CUT_V1"
PARENT_STATUS = "PROVED_EXACT_ROUTE_CUTS_SHALLOW_COMMON_V_FULL_LOCATOR_RESIDUAL_OPEN"

P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
FORBIDDEN_LIST_SIZE = B_STAR + 1
COMPANION_TARGET = B_STAR - 1
DEEP_EXCESS_START = 366_887
DEEP_CAP = 1_001_282
SHALLOW_LOWER = 15_775_933
SHALLOW_TARGET = 15_775_932
FIELD_MARGIN = P - 1 - B_STAR
SHALLOW_FIELD_MARGIN = P - 1 - SHALLOW_LOWER
U_PAID = 3_730
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_common_v_split_flat_pairwise_crt_equivalence_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json"
README_PATH = ROOT / "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/README.md"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_common_v_split_flat_pairwise_crt_equivalence_v1.md"
PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.sage"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/manifest.json"
PARENT_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_boundary_common_v_cross_g_route_cut_v1.md"
PARENT_PRIMARY_PATH = ROOT / "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py"
SCALAR_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_scalar_descent_equivalence.md"
SCALAR_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_scalar_descent_equivalence.py"
ANCHOR_EXCHANGE_PATH = ROOT / "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json"


class VerificationError(RuntimeError):
    """Raised whenever an exact packet gate fails."""


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
        raise VerificationError("noncanonical JSON value") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise VerificationError("invalid JSON") from exc
    require(type(value) is dict, "top-level JSON object")
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def strict_load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    require(path.exists() and path.is_file(), f"JSON source exists: {path}")
    return strict_decode(path.read_bytes(), canonical=canonical)


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


def canonical_repo_path(value: str) -> Path:
    require(type(value) is str and value.isascii(), "source path ASCII string")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), "source path relative")
    require(len(pure.parts) > 0, "source path nonempty")
    require("." not in pure.parts and ".." not in pure.parts, "source path canonical")
    path = ROOT.joinpath(*pure.parts)
    require(path.exists() and path.is_file(), f"source exists: {value}")
    require(not path.is_symlink(), f"source is not symlink: {value}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return path


def strict_payload_pin(path: Path, expected: str, label: str) -> dict[str, Any]:
    value = strict_load(path)
    require(value.get("payload_sha256") == expected, f"{label}: payload pin")
    require(payload_sha256(value) == expected, f"{label}: payload seal")
    return value


def source_binding(
    binding_id: str,
    path_text: str,
    role: str,
    scope: str,
    *,
    internal_payload_sha256: str | None = None,
) -> dict[str, Any]:
    path = canonical_repo_path(path_text)
    if internal_payload_sha256 is not None:
        strict_payload_pin(path, internal_payload_sha256, binding_id)
    return {
        "binding_id": binding_id,
        "internal_payload_sha256": internal_payload_sha256,
        "path": path_text,
        "role": role,
        "scope": scope,
        "sha256": sha256_path(path),
    }


def validate_schema() -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft")
    require(schema.get("$id") == SCHEMA_DOC_ID, "schema document id")
    require(schema.get("type") == "object", "schema object")
    require(schema.get("additionalProperties") is False, "schema top closed")
    required = {
        "architecture_id",
        "artifact_kind",
        "dependency_contract",
        "deployed_parameters",
        "fixed_h_split_flat_atlas",
        "ledger_state",
        "local_route_cuts",
        "nonclaims",
        "pairwise_crt_equivalence",
        "payload_sha256",
        "residual_localization",
        "row_contract",
        "schema",
        "source_bindings",
        "status",
        "theorem_id",
        "toy_replays",
    }
    require(set(schema.get("required", [])) == required, "schema required keys")
    require(set(schema.get("properties", {})) == required, "schema property keys")


def arithmetic() -> None:
    require(P == 2_147_483_647, "M31 prime")
    require((N, K, A, R, W) == (2_097_152, 1_048_576, 1_116_023, 981_129, 67_447), "deployed code parameters")
    require(B_STAR == 16_777_215 and FORBIDDEN_LIST_SIZE == 16_777_216, "budget and forbidden size")
    require(COMPANION_TARGET == 16_777_214, "companion target")
    require(DEEP_CAP == 1_001_282 and DEEP_EXCESS_START == 366_887, "parent deep cut")
    require(B_STAR - DEEP_CAP == SHALLOW_LOWER, "shallow lower arithmetic")
    require(COMPANION_TARGET - DEEP_CAP == SHALLOW_TARGET, "shallow target arithmetic")
    require(SHALLOW_LOWER == SHALLOW_TARGET + 1, "shallow one-unit gap")
    require(FIELD_MARGIN == 2_130_706_431, "deployed field margin")
    require(SHALLOW_FIELD_MARGIN == 2_131_707_713, "shallow field margin")
    require(B_STAR < P - 1, "strict deployed field-size gate")
    denominator = lambda m: m * m - R * (m - W - 1)
    require(denominator(72_858) == 380_274, "fixed-G left predecessor positive")
    require(denominator(72_859) == -455_138, "fixed-G left endpoint nonpositive")
    require(denominator(908_270) == -455_138, "fixed-G right endpoint nonpositive")
    require(denominator(908_271) == 380_274, "fixed-G right successor positive")


def run_process(
    command: list[str],
    *,
    timeout: int,
    label: str,
    env: dict[str, str] | None = None,
) -> bytes:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError(f"{label}: execution failed") from exc
    require(completed.returncode == 0, f"{label}: exit status")
    require(completed.stderr == b"", f"{label}: stderr empty")
    require(completed.stdout.endswith(b"\n"), f"{label}: final newline")
    return completed.stdout


def verify_primary_summary(summary: dict[str, Any]) -> None:
    require(summary.get("schema") == SCHEMA_ID, "primary schema")
    require(summary.get("theorem_id") == THEOREM_ID, "primary theorem")
    require(summary.get("status") == STATUS, "primary status")
    require(summary.get("terminal") == TERMINAL, "primary terminal")
    params = summary["parameters"]
    require(params["p"] == P and params["B_star"] == B_STAR, "primary deployed p/B_star")
    require(params["field_margin_p_minus_1_minus_B_star"] == FIELD_MARGIN, "primary field margin")
    require(params["shallow_field_margin_p_minus_1_minus_15775933"] == SHALLOW_FIELD_MARGIN, "primary shallow field margin")

    atlas = summary["fixed_H_split_flat_atlas"]
    require(atlas["remainder_map"]["rank"] == "d", "primary injective remainder rank")
    require(atlas["boundary"]["affine_equation"] == "G=H+T_HV(b)", "primary boundary affine equation")
    require(atlas["boundary"]["full_gcd_gate"] == "gcd(L0/H,1-Q_HV(b))=1", "primary boundary quotient orientation")
    require(atlas["boundary"]["rank_drop_components"] == 0, "primary no boundary rank drop")
    require(atlas["interior"]["affine_equation"] == "C_HmV*b=e_0", "primary interior affine equation")
    require(atlas["interior"]["consistent_rank_range"][0] == "1", "primary interior positive rank")
    require(atlas["interior"]["full_gcd_gate"] == "gcd(L0/H,Q_HV(b))=1", "primary interior quotient orientation")

    crt = summary["pairwise_full_gcd_equivalence"]
    require(crt["family_size_hypothesis"] == "|I|<p-1", "primary strict field hypothesis")
    require(crt["available_nonzero_value_margin"] == FIELD_MARGIN, "primary available field margin")
    require("gcd(b_i,H_i)=1" in crt["individual_gates"], "primary individual denominator-unit gate")
    require(crt["pairwise_gates"] == ["J_ij|W_ij", "gcd(Delta_ij,W_ij)=1"], "primary pairwise gates")
    require(crt["higher_CRT_obstruction"] is False, "primary no higher CRT obstruction")
    require(crt["Wronskian_nonzero_for_distinct_canonical_pairs"] is True, "primary reduced-pair Wronskian gate")

    realization = summary["exact_boundary_list_realization"]
    require(realization["degree_gate"] == "deg(c_i)<K", "primary reconstruction degree gate")
    require(realization["projection_unit"] == "distinct nonanchor codewords per received word", "primary reconstruction unit")
    require(realization["maximum_codeword_degree"] == K - 1, "primary reconstruction max degree")

    shallow = summary["shallow_successor"]
    require(shallow["parent_deep_cap"] == DEEP_CAP, "primary deep cap")
    require(shallow["forbidden_family_shallow_needed"] == SHALLOW_LOWER, "primary shallow lower")
    require(shallow["sufficient_shallow_upper_target"] == SHALLOW_TARGET, "primary shallow target")
    require(shallow["exact_gap"] == 1 and shallow["proved"] is False, "primary residual open")

    controls = summary["small_prime_controls"]
    require(controls["GF5"]["family_counts"]["2"]["pairwise_compatible"] == controls["GF5"]["family_counts"]["2"]["exactly_realized"], "GF5 pair equivalence")
    require(controls["GF7"]["family_counts"]["3"]["pairwise_compatible"] == controls["GF7"]["family_counts"]["3"]["exactly_realized"], "GF7 triple equivalence")
    sharp = controls["field_size_sharpness"]
    require(sharp["family_size"] == 4 and sharp["q"] == 5, "sharp field-size control")
    require(sharp["pairwise_H_gates"] == "vacuous" and sharp["common_unit_exists"] is False, "sharp equality failure")

    ledger = summary["ledger"]
    require(ledger["movement"] == 0 and ledger["official_endpoint_movement"] == 0, "primary zero movement")
    require(ledger["row_closed"] is False, "primary row open")
    require(all(ledger[atom] is None for atom in ATOM_ORDER[1:]), "primary null atoms")

    fixed_g = summary["degree_one_route_cuts"]["fixed_G_RS_embedding"]
    require(fixed_g["as_V_varies"] == "r_GV ranges bijectively over all nonzero-valued received words", "primary fixed-G arbitrary-word embedding")
    require(fixed_g["agreement_identity"] == "deg(gcd(L0,G-bV))=agreement_E0(b,r_GV)", "primary fixed-G agreement identity")
    require(fixed_g["additional_filter"] == "gcd(b,G)=1", "primary fixed-G additional filter")
    require(fixed_g["nonpositive_intervals"] == [[72_859, 908_270]], "primary fixed-G Johnson interval")


def replay_primary() -> tuple[dict[str, Any], dict[str, Any]]:
    normal_raw = run_process([sys.executable, str(PRIMARY_PATH)], timeout=300, label="primary normal")
    optimized_raw = run_process([sys.executable, "-O", str(PRIMARY_PATH)], timeout=300, label="primary optimized")
    normal = strict_decode(normal_raw, canonical=True)
    optimized = strict_decode(optimized_raw, canonical=True)
    deep_exact(optimized, normal, "primary optimized replay")
    verify_primary_summary(normal)

    tamper_raw = run_process(
        [sys.executable, str(PRIMARY_PATH), "--tamper-selftest"],
        timeout=300,
        label="primary tamper",
    )
    tamper = strict_decode(tamper_raw, canonical=True)
    require(tamper.get("schema") == SCHEMA_ID, "primary tamper schema")
    require(tamper.get("mutation_selftest") == "PASS", "primary tamper pass")
    require(type(tamper.get("mutations_detected")) is int and tamper["mutations_detected"] >= 27, "primary tamper count")
    require(len(tamper.get("mutation_names", [])) == tamper["mutations_detected"], "primary tamper names")
    require(tamper.get("row_closed") is False, "primary tamper row open")
    return normal, {
        "normal_output_sha256": sha256_bytes(normal_raw),
        "optimized_output_sha256": sha256_bytes(optimized_raw),
        "normal_equals_optimized": normal_raw == optimized_raw,
        "tamper_output_sha256": sha256_bytes(tamper_raw),
        "mutations_detected": tamper["mutations_detected"],
        "mutation_names": tamper["mutation_names"],
    }


def replay_sage() -> dict[str, Any]:
    sage_env = dict(os.environ)
    sage_env["HOME"] = "/tmp/rs-mca-sage-home"
    raw = run_process(
        ["/usr/local/bin/sage", str(SAGE_PATH)],
        timeout=600,
        label="Sage replay",
        env=sage_env,
    )
    summary = strict_decode(raw, canonical=True)
    require(summary.get("schema") == "m31-common-v-pairwise-crt-equivalence-sage-v1", "Sage schema")
    require(summary.get("theorem_id") == THEOREM_ID, "Sage theorem")
    require(summary.get("status") == STATUS, "Sage status")
    require(summary.get("terminal") == TERMINAL, "Sage terminal")
    atlas = summary["atlas_control"]
    require(atlas["chart_cases"] == 768, "Sage atlas cases")
    require(atlas["monic_equivalence_tests"] == 153_600, "Sage monic equivalence tests")
    require(atlas["full_gcd_tests"] == 6_864 and atlas["resultant_tests"] == 6_864, "Sage full-gcd/resultant tests")
    require(atlas["lift_invariance_tests"] == 7_680, "Sage lift-invariance tests")
    require(atlas["observed_nonempty_interior_ranks"] == [1], "Sage interior rank control")
    crt = summary["pairwise_crt_control"]
    require(crt["family_counts"]["2"] == {
        "exactly_realized": 48,
        "pairwise_compatible": 48,
        "pairwise_distinct_reduced_pair_families": 112,
    }, "Sage GF5 pair control")
    require(crt["family_counts"]["3"] == {
        "exactly_realized": 32,
        "pairwise_compatible": 32,
        "pairwise_distinct_reduced_pair_families": 448,
    }, "Sage GF5 triple control")
    require(summary["hostile_singleton_control"]["common_unit_exists"] is False, "Sage individual-unit hostile control")
    require(summary["hostile_singleton_control"]["pairwise_gates"] == "vacuous", "Sage singleton pairwise-vacuous control")
    require(summary["field_size_sharpness"]["family_size"] == 4, "Sage sharp family size")
    require(summary["field_size_sharpness"]["common_unit_exists"] is False, "Sage sharp equality failure")
    require(summary["boundary_reconstruction"]["distinct_codewords"] == 3, "Sage boundary reconstruction distinctness")
    require(summary["boundary_reconstruction"]["exact_supports"] is True, "Sage exact reconstructed supports")
    require(summary["deployed_scope"] == {
        "global_incidence_upper_15775932_proved": False,
        "ledger_movement": 0,
        "row_closed": False,
        "toy_controls_are_deployed_evidence": False,
    }, "Sage zero-ledger scope")
    return {
        "output_sha256": sha256_bytes(raw),
        "summary": summary,
        "independent_finite_field_control": True,
    }


def replay_parent_primary() -> dict[str, Any]:
    raw = run_process(
        [sys.executable, str(PARENT_PRIMARY_PATH), "--print-template"],
        timeout=300,
        label="parent primary replay",
    )
    summary = strict_decode(raw, canonical=True)
    require(summary.get("schema") == "m31-boundary-common-v-cross-g-route-cut-summary-v1", "parent replay schema")
    require(summary.get("theorem_id") == PARENT_THEOREM, "parent replay theorem")
    require(summary["whole_list_deep_cut"]["threshold_cap"] == DEEP_CAP, "parent replay deep cap")
    require(summary["whole_list_deep_cut"]["forbidden_list_shallow_nonanchors_lower"] == SHALLOW_LOWER, "parent replay shallow lower")
    require(summary["ledger_state"]["ledger_movement"] == 0, "parent replay zero movement")
    require(summary["ledger_state"]["row_closed"] is False, "parent replay row open")
    return {"output_sha256": sha256_bytes(raw), "schema": summary["schema"]}


def replay_scalar_descent() -> dict[str, Any]:
    raw = run_process([sys.executable, str(SCALAR_REPLAY_PATH)], timeout=180, label="scalar descent replay")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("scalar replay ASCII") from exc
    lines = text.splitlines()
    require(lines and lines[-1] == "VERIFIED", "scalar descent VERIFIED")
    values: dict[str, str] = {}
    for line in lines[:-1]:
        require(line.count("=") == 1, "scalar descent key-value line")
        key, value = line.split("=", 1)
        require(key and value and key not in values, "scalar descent unique field")
        values[key] = value
    require(values.get("p") == str(P), "scalar descent p")
    require(values.get("B_star") == str(B_STAR), "scalar descent B_star")
    require(values.get("threshold_equivalence") == "PASS", "scalar descent threshold equivalence")
    require(values.get("semantic_mutations") == "8/8", "scalar descent semantic mutations")
    return {"output_sha256": sha256_bytes(raw), "fields": values}


def verify_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    parent = strict_payload_pin(PARENT_MANIFEST_PATH, PARENT_PAYLOAD, "parent packet")
    anchor = strict_payload_pin(ANCHOR_EXCHANGE_PATH, ANCHOR_EXCHANGE_PAYLOAD, "anchor-exchange predecessor")
    require(parent.get("theorem_id") == PARENT_THEOREM, "parent theorem id")
    require(parent.get("status") == PARENT_STATUS, "parent status")
    require(parent["residual_localization"]["any_forbidden_boundary_census_contains_at_least"] == SHALLOW_LOWER, "parent shallow lower")
    require(parent["whole_list_deep_cut"]["threshold_cap"] == DEEP_CAP, "parent deep cap")
    require(parent["ledger_state"]["movement_from_this_packet"] == 0, "parent zero movement")
    require(parent["ledger_state"]["row_closed"] is False, "parent row open")
    require(parent["dependency_contract"]["anchor_exchange_parent"]["payload_sha256"] == ANCHOR_EXCHANGE_PAYLOAD, "parent anchor pin")
    require(anchor.get("theorem_id") == "M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1", "anchor predecessor theorem")
    return parent, anchor


def verify_text_contracts() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 common-V split-flat and pairwise CRT equivalence",
        "### Theorem 2.2: boundary charts",
        "gcd(J,1-Q_(H,V)(b))=1",
        "### Theorem 2.3: interior charts",
        "gcd(J,Q_(H,V)(b))=1",
        "### Theorem 3.1: pairwise CRT equivalence",
        "The CRT elimination itself needs no M31 degree inequality.",
        "pairwise distinct reduced pairs (G_i,b_i)",
        "gcd(b_i,H_i)=1",
        "J_(ij)\\mid W_(ij)",
        "gcd(Delta_(ij),W_(ij))=1",
        "|I|<p-1",
        "This failure is sharp.  Over F_5",
        "p-1-15,775,933",
        "=2,131,707,713",
        "72,859\\le m\\le908,270",
        "UNPROVEN: the global split rational-function/divisor incidence upper",
        "ledger\\ movement=0",
    ):
        require(anchor in note, f"theorem-note anchor: {anchor}")

    parent_note = PARENT_NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 boundary common-V, full-locator route cut",
        "15,775,933",
        "The maximal successor is the exact base-field split-flat incidence theorem.",
    ):
        require(anchor in parent_note, f"parent-note anchor: {anchor}")

    scalar_note = SCALAR_NOTE_PATH.read_text(encoding="utf-8")
    require("# Mersenne-31 scalar-descent equivalence" in scalar_note, "scalar note title")
    require("592,061,458,020,761,914,489,814,638,395,392" in scalar_note, "scalar strict margin anchor")

    readme = README_PATH.read_text(encoding="utf-8")
    for anchor in (
        "gcd(b_i,H_i)=1",
        "72,859 <= m <= 908,270",
        "no hidden triple-or-higher",
        "Ledger movement is zero",
    ):
        require(anchor in readme, f"README anchor: {anchor}")


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding(
            "M31_PAIRWISE_CRT::packet_schema",
            "experimental/data/schemas/m31_common_v_split_flat_pairwise_crt_equivalence_v1.schema.json",
            "packet_schema",
            "Closed top-level schema for the split-flat and pairwise-CRT packet.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::packet_verifier",
            "experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py",
            "packet_verifier",
            "Fail-closed source, replay, payload, predecessor, theorem-anchor, and mutation verifier.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::primary_exact_replay",
            "experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.py",
            "primary_exact_replay",
            "Standard-library deployed arithmetic, exact pairwise criterion, controls, and mutations.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::sage_exact_replay",
            "experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.sage",
            "sage_exact_replay",
            "Independent Sage finite-field split-flat and common-unit controls.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::theorem_note",
            "experimental/notes/thresholds/m31_common_v_split_flat_pairwise_crt_equivalence_v1.md",
            "theorem_note",
            "Proofs, scope audit, exact deployed margins, route cuts, and successor terminal.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::packet_readme",
            "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/README.md",
            "packet_readme",
            "Replay instructions and explicit zero-payment scope.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::parent_manifest",
            "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/manifest.json",
            "parent_manifest",
            "Sealed #1059 boundary common-V residual and direct shallow/deep threshold.",
            internal_payload_sha256=PARENT_PAYLOAD,
        ),
        source_binding(
            "M31_PAIRWISE_CRT::parent_note",
            "experimental/notes/thresholds/m31_boundary_common_v_cross_g_route_cut_v1.md",
            "parent_note",
            "Parent boundary coordinate, route cuts, and full-locator residual localization.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::parent_primary_replay",
            "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py",
            "parent_primary_replay",
            "Parent exact deployed arithmetic and shallow/deep residual replay.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::scalar_descent_note",
            "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
            "scalar_descent_note",
            "Direct-threshold quartic-to-base-field scalar descent theorem.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::scalar_descent_replay",
            "experimental/scripts/verify_m31_scalar_descent_equivalence.py",
            "scalar_descent_replay",
            "Exact scalar-descent field margin and semantic mutations.",
        ),
        source_binding(
            "M31_PAIRWISE_CRT::anchor_exchange_predecessor",
            "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json",
            "anchor_exchange_predecessor",
            "Sealed boundary-anchor divisor/gcd bijection predecessor.",
            internal_payload_sha256=ANCHOR_EXCHANGE_PAYLOAD,
        ),
    ]


def build_template() -> dict[str, Any]:
    arithmetic()
    verify_text_contracts()
    parent, anchor = verify_dependencies()
    primary, primary_replay = replay_primary()
    sage_replay = replay_sage()
    parent_replay = replay_parent_primary()
    scalar_replay = replay_scalar_descent()
    bindings = source_bindings()
    require(len(bindings) == 12, "source binding count")
    require(len({row["binding_id"] for row in bindings}) == len(bindings), "unique source ids")
    require(len({row["path"] for row in bindings}) == len(bindings), "unique source paths")

    pairwise = copy.deepcopy(primary["pairwise_full_gcd_equivalence"])
    pairwise["exact_boundary_list_realization"] = copy.deepcopy(primary["exact_boundary_list_realization"])
    pairwise["abstract_crt_degree_gate"] = "NO_h_ge_m_HYPOTHESIS"
    pairwise["canonical_M31_reconstruction_adds_degree_gates"] = True
    pairwise["input_identity"] = "PAIRWISE_DISTINCT_REDUCED_(G_i,b_i)_DECORATED_WITH_H_i"
    pairwise["individual_denominator_unit_gate_is_independent"] = True

    local_route_cuts = {
        "degree_one": copy.deepcopy(primary["degree_one_route_cuts"]),
        "fixed_G_arbitrary_nonzero_word_embedding": {
            "received_table": "r_(G,V)(x)=G(x)/V(x) on E0",
            "agreement_identity": "deg(gcd(L0,G-bV))=agr_E0(b,r_(G,V))",
            "unit_V_to_nonzero_received_word_bijection": True,
            "additional_filter": "gcd(b,G)=1",
            "ordinary_RS_dimension": "d=m-w",
            "ordinary_RS_agreement_threshold": "m",
            "johnson_denominator": "m^2-R*(m-w-1)",
            "nonpositive_integer_interval": [72_859, 908_270],
            "left_predecessor_value": 380_274,
            "left_endpoint_value": -455_138,
            "right_endpoint_value": -455_138,
            "right_successor_value": 380_274,
            "route_cut": "ANOTHER_FIXED_G_JOHNSON_OR_MOMENT_SUBSTITUTION_CANNOT_CLOSE_THE_BROAD_MIDDLE_RANGE",
        },
    }

    payload: dict[str, Any] = {
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "dependency_contract": {
            "stacked_dependency": True,
            "parent": {
                "path": str(PARENT_MANIFEST_PATH.relative_to(ROOT)),
                "payload_sha256": parent["payload_sha256"],
                "theorem_id": parent["theorem_id"],
                "status": parent["status"],
            },
            "anchor_exchange_predecessor": {
                "path": str(ANCHOR_EXCHANGE_PATH.relative_to(ROOT)),
                "payload_sha256": anchor["payload_sha256"],
                "theorem_id": anchor["theorem_id"],
            },
            "subprocess_replays": {
                "primary_normal": True,
                "primary_optimized": True,
                "primary_normal_equals_optimized": primary_replay["normal_equals_optimized"],
                "primary_normal_output_sha256": primary_replay["normal_output_sha256"],
                "primary_optimized_output_sha256": primary_replay["optimized_output_sha256"],
                "primary_tamper_output_sha256": primary_replay["tamper_output_sha256"],
                "primary_mutations_detected": primary_replay["mutations_detected"],
                "sage": True,
                "sage_output_sha256": sage_replay["output_sha256"],
                "parent_primary_output_sha256": parent_replay["output_sha256"],
                "scalar_descent_output_sha256": scalar_replay["output_sha256"],
            },
        },
        "deployed_parameters": {
            **copy.deepcopy(primary["parameters"]),
            "companion_target": COMPANION_TARGET,
            "deep_excess_start": DEEP_EXCESS_START,
            "deep_cap": DEEP_CAP,
            "shallow_lower": SHALLOW_LOWER,
            "shallow_target": SHALLOW_TARGET,
            "shallow_field_margin_p_minus_1_minus_shallow_lower": SHALLOW_FIELD_MARGIN,
            "target_epsilon": "2^-100",
        },
        "fixed_h_split_flat_atlas": copy.deepcopy(primary["fixed_H_split_flat_atlas"]),
        "ledger_state": {
            "atoms": copy.deepcopy(parent["ledger_state"]["atoms"]),
            "known_parent_sum": U_PAID,
            "movement_from_this_packet": 0,
            "official_endpoint_or_score_movement": 0,
            "null_atoms": list(ATOM_ORDER[1:]),
            "row_closed": False,
            "route_cut_is_not_payment": True,
        },
        "local_route_cuts": local_route_cuts,
        "nonclaims": {
            "abstract_CRT_requires_h_at_least_m": False,
            "all_pairwise_gates_alone_imply_realizability_without_individual_unit_gates": False,
            "complete_M31_list_bound_proved": False,
            "fixed_G_johnson_closes_middle_range": False,
            "global_split_rational_function_incidence_bound_proved": False,
            "ledger_atom_paid_by_this_packet": False,
            "locator_repetition_in_forbidden_family_proved": False,
            "official_endpoint_or_score_changed": False,
            "row_closed": False,
            "small_prime_controls_are_deployed_evidence": False,
            "stable_paper_modified": False,
            "v4_owner_transport_proved": False,
        },
        "pairwise_crt_equivalence": pairwise,
        "payload_sha256": "",
        "residual_localization": {
            "parent_shallow_lower": SHALLOW_LOWER,
            "sufficient_shallow_upper_target": SHALLOW_TARGET,
            "exact_gap": 1,
            "proved": False,
            "terminal": TERMINAL,
            "successor_statement": "EVERY_INDIVIDUAL_UNIT_AND_PAIRWISE_COMPATIBLE_CANONICAL_SPLIT_RATIONAL_FUNCTION_FAMILY_WITH_0_LE_s_LE_366886_HAS_SIZE_AT_MOST_15775932",
            "no_hidden_triple_or_higher_common_V_obstruction": True,
            "common_V_reconstructible_from_individual_AND_pairwise_gates": True,
            "direct_threshold_diagnostic_not_v4_payment": True,
        },
        "row_contract": {
            **copy.deepcopy(primary["row"]),
            "unit": UNIT,
            "forbidden_list_size": FORBIDDEN_LIST_SIZE,
            "companion_target": COMPANION_TARGET,
            "quantifier": "EVERY_BASE_FIELD_BOUNDARY_PARTITION_AND_EVERY_FAMILY_OF_AT_MOST_B_STAR_PAIRWISE_DISTINCT_REDUCED_PAIRS_DECORATED_WITH_H",
            "common_unit": "NONZERO_TABLE_ON_E0_INTERPOLATED_UNIQUELY_MODULO_L0",
        },
        "schema": SCHEMA_ID,
        "source_bindings": bindings,
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "toy_replays": {
            "small_prime_controls": copy.deepcopy(primary["small_prime_controls"]),
            "primary_mutation_names": primary_replay["mutation_names"],
            "sage": sage_replay,
            "parent_primary": parent_replay,
            "scalar_descent": scalar_replay,
        },
    }
    return seal(payload)


def verify_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list and len(bindings) == 12, "source bindings list")
    ids: set[str] = set()
    paths: set[str] = set()
    pins = 0
    for index, binding in enumerate(bindings):
        require(type(binding) is dict, f"binding {index}: object")
        require(set(binding) == {"binding_id", "internal_payload_sha256", "path", "role", "scope", "sha256"}, f"binding {index}: exact keys")
        require(type(binding["binding_id"]) is str and binding["binding_id"].isascii(), f"binding {index}: id")
        require(binding["binding_id"] not in ids, f"binding {index}: unique id")
        ids.add(binding["binding_id"])
        path = canonical_repo_path(binding["path"])
        require(binding["path"] not in paths, f"binding {index}: unique path")
        paths.add(binding["path"])
        require(type(binding["role"]) is str and binding["role"].isascii(), f"binding {index}: role")
        require(type(binding["scope"]) is str and binding["scope"].isascii(), f"binding {index}: scope")
        digest = binding["sha256"]
        require(type(digest) is str and len(digest) == 64 and set(digest) <= set("0123456789abcdef"), f"binding {index}: hash")
        require(digest == sha256_path(path), f"binding {index}: fresh hash")
        pin = binding["internal_payload_sha256"]
        if pin is not None:
            pins += 1
            require(type(pin) is str and len(pin) == 64, f"binding {index}: pin shape")
            strict_payload_pin(path, pin, f"binding {index}")
    require(pins == 2, "two internal predecessor pins")


def validate(payload: dict[str, Any], expected: dict[str, Any] | None = None) -> None:
    arithmetic()
    require(payload.get("schema") == SCHEMA_ID, "payload schema")
    require(payload.get("theorem_id") == THEOREM_ID, "payload theorem")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "payload architecture")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "payload artifact kind")
    require(payload.get("status") == STATUS, "payload status")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")

    params = payload["deployed_parameters"]
    require(params["p"] == P and params["B_star"] == B_STAR, "payload p/B_star")
    require(params["field_margin_p_minus_1_minus_B_star"] == FIELD_MARGIN, "payload field margin")
    require(params["shallow_field_margin_p_minus_1_minus_shallow_lower"] == SHALLOW_FIELD_MARGIN, "payload shallow field margin")
    require(params["deep_cap"] == DEEP_CAP and params["shallow_lower"] == SHALLOW_LOWER, "payload deep/shallow")

    atlas = payload["fixed_h_split_flat_atlas"]
    require(atlas["remainder_map"]["rank"] == "d", "payload atlas full column rank")
    require(atlas["boundary"]["codimension"] == "m-d=w", "payload boundary codimension")
    require(atlas["boundary"]["rank_drop_components"] == 0, "payload no boundary rank drop")
    require(atlas["boundary"]["full_gcd_gate"] == "gcd(L0/H,1-Q_HV(b))=1", "payload boundary sign")
    require(atlas["interior"]["full_gcd_gate"] == "gcd(L0/H,Q_HV(b))=1", "payload interior sign")
    require(atlas["interior"]["consistent_rank_range"][0] == "1", "payload interior rank floor")

    crt = payload["pairwise_crt_equivalence"]
    require(crt["family_size_hypothesis"] == "|I|<p-1", "payload strict field gate")
    require(crt["abstract_crt_degree_gate"] == "NO_h_ge_m_HYPOTHESIS", "payload abstract CRT degree scope")
    require(crt["input_identity"] == "PAIRWISE_DISTINCT_REDUCED_(G_i,b_i)_DECORATED_WITH_H_i", "payload reduced-pair identity")
    require(crt["individual_denominator_unit_gate_is_independent"] is True, "payload individual gate independence")
    require("gcd(b_i,H_i)=1" in crt["individual_gates"], "payload individual denominator-unit gate")
    require(crt["pairwise_gates"] == ["J_ij|W_ij", "gcd(Delta_ij,W_ij)=1"], "payload pairwise gates")
    require(crt["higher_CRT_obstruction"] is False, "payload no higher obstruction")
    require(crt["exact_boundary_list_realization"]["maximum_codeword_degree"] == K - 1, "payload reconstruction degree")

    fixed_g = payload["local_route_cuts"]["fixed_G_arbitrary_nonzero_word_embedding"]
    require(fixed_g["unit_V_to_nonzero_received_word_bijection"] is True, "payload fixed-G word bijection")
    require(fixed_g["nonpositive_integer_interval"] == [72_859, 908_270], "payload fixed-G Johnson interval")
    require((fixed_g["left_predecessor_value"], fixed_g["left_endpoint_value"], fixed_g["right_endpoint_value"], fixed_g["right_successor_value"]) == (380_274, -455_138, -455_138, 380_274), "payload fixed-G endpoint values")

    residual = payload["residual_localization"]
    require(residual["parent_shallow_lower"] == SHALLOW_LOWER, "payload residual lower")
    require(residual["sufficient_shallow_upper_target"] == SHALLOW_TARGET, "payload residual target")
    require(residual["exact_gap"] == 1 and residual["proved"] is False, "payload residual open")
    require(residual["terminal"] == TERMINAL, "payload terminal")
    require(residual["no_hidden_triple_or_higher_common_V_obstruction"] is True, "payload route cut")
    require(residual["common_V_reconstructible_from_individual_AND_pairwise_gates"] is True, "payload complete common-V gates")

    ledger = payload["ledger_state"]
    require([row["atom_id"] for row in ledger["atoms"]] == list(ATOM_ORDER), "payload atom order")
    require(ledger["known_parent_sum"] == U_PAID, "payload parent sum")
    require(ledger["movement_from_this_packet"] == 0, "payload zero movement")
    require(ledger["official_endpoint_or_score_movement"] == 0, "payload zero official movement")
    require(ledger["null_atoms"] == list(ATOM_ORDER[1:]), "payload null atoms")
    require(ledger["row_closed"] is False and ledger["route_cut_is_not_payment"] is True, "payload row open")
    require(all(value is False for value in payload["nonclaims"].values()), "all nonclaims false")

    dependency = payload["dependency_contract"]
    require(dependency["stacked_dependency"] is True, "payload stacked dependency")
    require(dependency["parent"]["payload_sha256"] == PARENT_PAYLOAD, "payload parent pin")
    require(dependency["anchor_exchange_predecessor"]["payload_sha256"] == ANCHOR_EXCHANGE_PAYLOAD, "payload anchor pin")
    replays = dependency["subprocess_replays"]
    require(replays["primary_normal"] is True and replays["primary_optimized"] is True, "payload primary modes")
    require(replays["primary_normal_equals_optimized"] is True, "payload primary optimization equality")
    require(replays["sage"] is True, "payload Sage replay")
    require(replays["primary_mutations_detected"] >= 27, "payload primary mutation floor")

    sharp = payload["toy_replays"]["small_prime_controls"]["field_size_sharpness"]
    require(sharp["family_size"] == sharp["q"] - 1, "payload sharp field family size")
    require(sharp["pairwise_H_gates"] == "vacuous" and sharp["common_unit_exists"] is False, "payload sharp field failure")
    require(payload["toy_replays"]["sage"]["independent_finite_field_control"] is True, "payload Sage independence")
    verify_source_bindings(payload["source_bindings"])

    if expected is not None:
        deep_exact(payload, expected)


def mutate(path: Sequence[Any], value: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def apply(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        cursor: Any = out
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        return seal(out)

    return apply


def tamper_selftest(expected: dict[str, Any]) -> int:
    def drop_source(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"].pop()
        return seal(out)

    def duplicate_source(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"][1]["binding_id"] = out["source_bindings"][0]["binding_id"]
        return seal(out)

    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutate(("schema",), "wrong-schema")),
        ("theorem", mutate(("theorem_id",), "WRONG")),
        ("architecture", mutate(("architecture_id",), "WRONG")),
        ("status", mutate(("status",), "CLOSED")),
        ("p", mutate(("deployed_parameters", "p"), P - 2)),
        ("B_star", mutate(("deployed_parameters", "B_star"), B_STAR + 1)),
        ("field margin", mutate(("deployed_parameters", "field_margin_p_minus_1_minus_B_star"), FIELD_MARGIN - 1)),
        ("shallow field margin", mutate(("deployed_parameters", "shallow_field_margin_p_minus_1_minus_shallow_lower"), SHALLOW_FIELD_MARGIN - 1)),
        ("atlas rank", mutate(("fixed_h_split_flat_atlas", "remainder_map", "rank"), "d-1")),
        ("boundary rank drop", mutate(("fixed_h_split_flat_atlas", "boundary", "rank_drop_components"), 1)),
        ("boundary quotient sign", mutate(("fixed_h_split_flat_atlas", "boundary", "full_gcd_gate"), "gcd(L0/H,Q_HV(b))=1")),
        ("interior quotient sign", mutate(("fixed_h_split_flat_atlas", "interior", "full_gcd_gate"), "gcd(L0/H,1-Q_HV(b))=1")),
        ("interior rank zero", mutate(("fixed_h_split_flat_atlas", "interior", "consistent_rank_range", 0), "0")),
        ("nonstrict field gate", mutate(("pairwise_crt_equivalence", "family_size_hypothesis"), "|I|<=p-1")),
        ("abstract degree gate", mutate(("pairwise_crt_equivalence", "abstract_crt_degree_gate"), "h>=m")),
        ("input identity", mutate(("pairwise_crt_equivalence", "input_identity"), "DISTINCT_TRIPLES")),
        ("individual gate independence", mutate(("pairwise_crt_equivalence", "individual_denominator_unit_gate_is_independent"), False)),
        ("delete individual unit gate", mutate(("pairwise_crt_equivalence", "individual_gates", 3), "gcd(b_i,H_i) unchecked")),
        ("intersection gate", mutate(("pairwise_crt_equivalence", "pairwise_gates", 0), "J_ij does not divide W_ij")),
        ("symmetric difference gate", mutate(("pairwise_crt_equivalence", "pairwise_gates", 1), "Delta_ij|W_ij")),
        ("higher obstruction", mutate(("pairwise_crt_equivalence", "higher_CRT_obstruction"), True)),
        ("reconstruction degree", mutate(("pairwise_crt_equivalence", "exact_boundary_list_realization", "maximum_codeword_degree"), K)),
        ("fixed-G bijection", mutate(("local_route_cuts", "fixed_G_arbitrary_nonzero_word_embedding", "unit_V_to_nonzero_received_word_bijection"), False)),
        ("fixed-G interval", mutate(("local_route_cuts", "fixed_G_arbitrary_nonzero_word_embedding", "nonpositive_integer_interval"), [72_858, 908_270])),
        ("fixed-G left endpoint", mutate(("local_route_cuts", "fixed_G_arbitrary_nonzero_word_embedding", "left_endpoint_value"), 380_274)),
        ("residual lower", mutate(("residual_localization", "parent_shallow_lower"), SHALLOW_LOWER - 1)),
        ("residual target", mutate(("residual_localization", "sufficient_shallow_upper_target"), SHALLOW_TARGET + 1)),
        ("false incidence proof", mutate(("residual_localization", "proved"), True)),
        ("wrong terminal", mutate(("residual_localization", "terminal"), "PAID")),
        ("hide triple obstruction", mutate(("residual_localization", "no_hidden_triple_or_higher_common_V_obstruction"), False)),
        ("omit individual gate from reconstruction", mutate(("residual_localization", "common_V_reconstructible_from_individual_AND_pairwise_gates"), False)),
        ("ledger movement", mutate(("ledger_state", "movement_from_this_packet"), 1)),
        ("official movement", mutate(("ledger_state", "official_endpoint_or_score_movement"), 1)),
        ("false row closure", mutate(("ledger_state", "row_closed"), True)),
        ("route cut payment", mutate(("ledger_state", "route_cut_is_not_payment"), False)),
        ("U_Q value", mutate(("ledger_state", "atoms", 1, "value"), 0)),
        ("false nonclaim", mutate(("nonclaims", "global_split_rational_function_incidence_bound_proved"), True)),
        ("false v4 owner", mutate(("nonclaims", "v4_owner_transport_proved"), True)),
        ("parent pin", mutate(("dependency_contract", "parent", "payload_sha256"), "0" * 64)),
        ("anchor pin", mutate(("dependency_contract", "anchor_exchange_predecessor", "payload_sha256"), "0" * 64)),
        ("unstack", mutate(("dependency_contract", "stacked_dependency"), False)),
        ("skip optimized", mutate(("dependency_contract", "subprocess_replays", "primary_optimized"), False)),
        ("normal optimized mismatch", mutate(("dependency_contract", "subprocess_replays", "primary_normal_equals_optimized"), False)),
        ("skip Sage", mutate(("dependency_contract", "subprocess_replays", "sage"), False)),
        ("replay hash", mutate(("dependency_contract", "subprocess_replays", "primary_normal_output_sha256"), "0" * 64)),
        ("Sage hash", mutate(("dependency_contract", "subprocess_replays", "sage_output_sha256"), "0" * 64)),
        ("sharp equality false positive", mutate(("toy_replays", "small_prime_controls", "field_size_sharpness", "common_unit_exists"), True)),
        ("source hash", mutate(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source traversal", mutate(("source_bindings", 0, "path"), "../schema.json")),
        ("source internal pin", mutate(("source_bindings", 6, "internal_payload_sha256"), "0" * 64)),
        ("drop source", drop_source),
        ("duplicate source", duplicate_source),
    ]
    rejected = 0
    for name, apply in mutations:
        candidate = apply(expected)
        try:
            validate(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise VerificationError(f"mutation escaped: {name}")

    malformed = [
        b'{"a":1,"a":2}\n',
        b'{"x":1.5}\n',
        b'{"x":NaN}\n',
        b'[]\n',
        b'{"x":"\xff"}\n',
        b'{"x":1}',
    ]
    for raw in malformed:
        try:
            strict_decode(raw, canonical=True)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    require(rejected == len(mutations) + len(malformed), "all packet mutations rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.check or args.tamper_selftest or args.print_template):
        args.check = True
    require(sum((args.check, args.tamper_selftest, args.print_template)) == 1, "select exactly one mode")
    validate_schema()
    expected = build_template()
    validate(expected, expected)

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
        return
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"M31 common-V split-flat pairwise-CRT packet mutations: {count}/{count} rejected PASS")
        return

    actual = strict_load(args.manifest)
    validate(actual, expected)
    print("M31 common-V split-flat pairwise-CRT packet v1: PASS")
    print("fixed-H atlas: boundary codimension w; interior codimension at least w+1 PASS")
    print("common unit: individual denominator gates plus pairwise exact-Wronskian gates are equivalent PASS")
    print("field margins: full=2130706431; shallow=2131707713; equality case sharp PASS")
    print("fixed-G nowhere-zero-word embedding: Johnson denominator nonpositive on 72859..908270 ROUTE CUT")
    print("global split rational-function/divisor incidence: OPEN; v4 ledger movement: 0")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
