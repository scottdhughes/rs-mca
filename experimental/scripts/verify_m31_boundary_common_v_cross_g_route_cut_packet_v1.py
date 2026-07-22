#!/usr/bin/env python3
"""Verify the M31 boundary common-V, cross-G route-cut packet.

This verifier seals the exact route cuts and residual localization obtained
after the all-weight anchor-exchange reduction.  It deliberately does not
certify the missing common-``V``, full-locator coefficient-incidence bound,
move a v4 ledger atom, or close the M31 LIST row.

The verifier is fail closed under ordinary Python and ``python -O``.  It
checks a closed top-level schema, canonical JSON, fresh source hashes,
internal predecessor payload pins, exact theorem/source anchors, independent
subprocess replays of both arithmetic implementations, and hostile
proof-critical mutations.  ``--print-template`` emits canonical one-line
JSON but never writes the pinned manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Sequence


SCHEMA_ID = "rs-mca-m31-boundary-common-v-cross-g-route-cut-v1"
THEOREM_ID = "M31_BOUNDARY_COMMON_V_CROSS_G_ROUTE_CUT_V1"
ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
ARTIFACT_KIND = "EXACT_BOUNDARY_COMMON_V_CROSS_G_ROUTE_CUT_AND_RESIDUAL_LOCALIZATION"
STATUS = "PROVED_EXACT_ROUTE_CUTS_SHALLOW_COMMON_V_FULL_LOCATOR_RESIDUAL_OPEN"

PARENT_ANCHOR_PAYLOAD = "bf38cbae247269196395c61aeae3e9fa8b72f92ffc0b0af4650e96e98d66eb6e"
PARENT_COMPILER_PAYLOAD = "d8acc7accdb9b6720b109af5ececc8569f0822f6550a35241234d99264acbc4e"
SOURCE_ADAPTER_PAYLOAD = "21b213e2b3dfc7f8f99049aea44542ce5ae06dd59b62c10555f9faf5aaa882ce"
PARTITION_SHA256 = "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"

UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")

P = 2**31 - 1
Q = P**4
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
BUDGET = Q // 2**100
FORBIDDEN_LIST_SIZE = BUDGET + 1
NONANCHOR_CENSUS_TARGET = BUDGET - 1
PARENT_U_PAID = 3_730

WHOLE_LIST_FIRST_DEEP_SLACK = 366_887
WHOLE_LIST_DEEP_CAP = 1_001_282
SHALLOW_NONANCHOR_LOWER = 15_775_933
ROOT_DEFICIT = RADIUS - W

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_boundary_common_v_cross_g_route_cut_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/manifest.json"
PRIMARY_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py"
INDEPENDENT_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1_independent.py"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_boundary_common_v_cross_g_route_cut_v1.md"
README_PATH = ROOT / "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/README.md"
PARENT_ANCHOR_PATH = ROOT / "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json"
PARENT_COMPILER_PATH = ROOT / "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json"
SOURCE_ADAPTER_PATH = ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json"
CAP_FOUNDATION_PATH = ROOT / "tex/cs25_cap_v13_2.tex"
ACTIVE_LEDGER_PATH = ROOT / "experimental/grande_finale.tex"
SCALAR_DESCENT_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_scalar_descent_equivalence.md"
SCALAR_DESCENT_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_scalar_descent_equivalence.py"
PREFIX_COUNTEREXAMPLE_NOTE_PATH = ROOT / "experimental/notes/thresholds/prefix_staircase_extremality_counterexamples.md"
PREFIX_COUNTEREXAMPLE_REPLAY_PATH = ROOT / "experimental/scripts/verify_prefix_staircase_extremality_counterexamples.py"
FIXED_REMAINDER_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut.md"
FIXED_REMAINDER_REPLAY_PATH = ROOT / "experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py"


class VerificationError(RuntimeError):
    """Raised when any exact packet gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("noncanonical JSON value") from exc
    return (encoded + "\n").encode("ascii")


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
    require(not pure.is_absolute(), "source path is relative")
    require(len(pure.parts) > 0, "source path nonempty")
    require("." not in pure.parts and ".." not in pure.parts, "source path canonical")
    resolved = ROOT.joinpath(*pure.parts)
    require(resolved.exists() and resolved.is_file(), f"source exists: {value}")
    require(not resolved.is_symlink(), f"source is not symlink: {value}")
    require(resolved.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return resolved


def strict_payload_pin(path: Path, expected: str, label: str) -> dict[str, Any]:
    data = strict_load(path)
    require(type(data.get("payload_sha256")) is str, f"{label}: payload field")
    require(data["payload_sha256"] == expected, f"{label}: payload pin")
    require(payload_sha256(data) == expected, f"{label}: payload seal")
    return data


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
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema object")
    require(schema.get("additionalProperties") is False, "schema top closed")
    required = {
        "architecture_id",
        "artifact_kind",
        "base_field_route_cut",
        "boundary_coordinate",
        "chebyshev_support_countermodel",
        "dependency_contract",
        "deployed_parameters",
        "fixed_G_bound",
        "ledger_state",
        "nonclaims",
        "payload_sha256",
        "residual_localization",
        "row_contract",
        "schema",
        "singleton_packing",
        "source_bindings",
        "split_support_moment",
        "status",
        "theorem_id",
        "v_equals_1_route_cut",
        "whole_list_deep_cut",
        "wronskian_route_cut",
    }
    require(set(schema.get("required", [])) == required, "schema required keys")
    require(set(schema.get("properties", {})) == required, "schema property keys")


def arithmetic() -> None:
    require(P == 2_147_483_647, "M31 prime")
    require(Q == 21_267_647_892_944_572_736_998_860_269_687_930_881, "quartic field cardinality")
    require(N == 2_097_152 and K == 1_048_576, "deployed n K")
    require(AGREEMENT == 1_116_023, "deployed agreement")
    require(RADIUS == 981_129 and W == 67_447, "deployed radius and shift")
    require(BUDGET == 16_777_215, "deployed list budget")
    require(FORBIDDEN_LIST_SIZE == 16_777_216, "forbidden list size")
    require(NONANCHOR_CENSUS_TARGET == 16_777_214, "nonanchor census target")
    require(ROOT_DEFICIT == 913_682, "root deficit")
    require(BUDGET - WHOLE_LIST_DEEP_CAP == SHALLOW_NONANCHOR_LOWER, "shallow residual arithmetic")
    require(FORBIDDEN_LIST_SIZE < Q, "fresh-symbol field gate inherited")


def replay_python(path: Path, *arguments: str) -> dict[str, Any]:
    require(path.exists() and path.is_file() and not path.is_symlink(), f"replay exists: {path}")
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend((str(path), *arguments))
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=240,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError(f"replay execution failed: {path.name}") from exc
    require(completed.returncode == 0, f"replay exit status: {path.name}")
    require(completed.stderr == b"", f"replay stderr empty: {path.name}")
    return strict_decode(completed.stdout, canonical=True)


def replay_summaries() -> tuple[dict[str, Any], dict[str, Any]]:
    primary = replay_python(PRIMARY_REPLAY_PATH, "--print-template")
    independent = replay_python(INDEPENDENT_REPLAY_PATH, "--print-template")
    crosscheck_replays(primary, independent)
    return primary, independent


def replay_scalar_descent() -> dict[str, str]:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.append(str(SCALAR_DESCENT_REPLAY_PATH))
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError("scalar-descent replay execution failed") from exc
    require(completed.returncode == 0, "scalar-descent replay exit status")
    require(completed.stderr == b"", "scalar-descent replay stderr empty")
    try:
        text = completed.stdout.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("scalar-descent replay non-ASCII output") from exc
    require(text.endswith("\n"), "scalar-descent replay final newline")
    lines = text.splitlines()
    require(lines and lines[-1] == "VERIFIED", "scalar-descent VERIFIED sentinel")
    values: dict[str, str] = {}
    for line in lines[:-1]:
        require(line.count("=") == 1, "scalar-descent key-value output")
        key, value = line.split("=", 1)
        require(key and value and key not in values, "scalar-descent unique nonempty field")
        values[key] = value
    expected = {
        "B_star": "16777215",
        "H_r": "4611686016279904257",
        "L": "16777216",
        "LtH_r": "75911179514902718909260442370048",
        "N_r": "9903520305059670166633185280",
        "a": "1116023",
        "base_commit": "9908454995f3f195cfe748f35a1135211609d066",
        "certificate_id": "m31-scalar-descent-equivalence-v1",
        "forbidden_size": "16777216",
        "g": "67448",
        "gN_r": "667972637535664633399075080765440",
        "k": "1048576",
        "n": "2097152",
        "p": "2147483647",
        "r": "4",
        "semantic_mutations": "8/8",
        "strict_margin": "592061458020761914489814638395392",
        "t": "981129",
        "threshold_equivalence": "PASS",
    }
    deep_exact(values, expected, "scalar_descent_replay")
    return values


def replay_auxiliary_text(path: Path, expected_lines: list[str], label: str) -> str:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.append(str(path))
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VerificationError(f"{label} replay execution failed") from exc
    require(completed.returncode == 0, f"{label} replay exit status")
    require(completed.stderr == b"", f"{label} replay stderr empty")
    try:
        output = completed.stdout.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"{label} replay non-ASCII output") from exc
    require(output.endswith("\n"), f"{label} replay final newline")
    require(output.splitlines() == expected_lines, f"{label} replay exact output")
    return sha256_bytes(completed.stdout)


def replay_v1_sources() -> dict[str, str]:
    prefix_hash = replay_auxiliary_text(
        PREFIX_COUNTEREXAMPLE_REPLAY_PATH,
        [
            "prefix/staircase extremality counterexamples",
            "F7 list=4 prefix=3 MCA=4/1",
            "F23 list=11/8 MCA=11/2",
            "PASS_WITH_PREFIX_STAIRCASE_EXTREMALITY_COUNTEREXAMPLES",
        ],
        "prefix counterexample",
    )
    fixed_hash = replay_auxiliary_text(
        FIXED_REMAINDER_REPLAY_PATH,
        [
            "M31 Chebyshev fixed-remainder C1 boundary-source route cut: PASS",
            "exact source: c=2048 floor=6796405; complete ball boundary-only",
            "route: QR2 fixed-R; removed by/at C1; primitive-Q residual=0",
            "chronology: T46>=6796360; raw cap missed by 6536480",
            "optimizer: b=27 compatible by 69137; every b>=28 incompatible",
            "Forney: b27 p2=70282; b28 p2=67680; b29 p2=65262<67447",
            "route cut: no flat baseline survives source and gains two-row control",
            "scope: C1 numerical payment and variable-R residual OPEN; ledger movement=0",
            "checks=183289",
        ],
        "fixed-remainder source",
    )
    return {
        "prefix_counterexample_output_sha256": prefix_hash,
        "fixed_remainder_output_sha256": fixed_hash,
    }


def crosscheck_replays(primary: dict[str, Any], independent: dict[str, Any]) -> None:
    require(primary.get("schema") == "m31-boundary-common-v-cross-g-route-cut-summary-v1", "primary replay schema")
    require(primary.get("theorem_id") == THEOREM_ID, "primary theorem id")
    require(primary.get("status") == "PROVED_EXACT_ROUTE_CUTS_SHALLOW_COMMON_V_FULL_LOCATOR_RESIDUAL_OPEN", "primary status")
    require(independent.get("schema") == "m31-boundary-cross-g-route-cut-independent-summary-v1", "independent replay schema")

    parameters = primary["deployed_parameters"]
    independent_parameters = independent["parameters"]
    require(parameters == {
        "K": K,
        "R": RADIUS,
        "agreement": AGREEMENT,
        "budget": BUDGET,
        "forbidden": FORBIDDEN_LIST_SIZE,
        "n": N,
        "p": P,
        "w": W,
    }, "primary exact parameters")
    require(independent_parameters == {
        "B": BUDGET,
        "K": K,
        "R": RADIUS,
        "a": AGREEMENT,
        "n": N,
        "w": W,
    }, "independent exact parameters")

    fixed = primary["fixed_G_bound"]
    independent_fixed = independent["fixed_G"]
    require(fixed["s_zero"]["positive_wings"] == independent_fixed["s0"]["intervals"]["positive"], "fixed-G positive wings agree")
    require(fixed["s_zero"]["cap_at_most_3730_wings"] == independent_fixed["s0"]["intervals"]["cap_at_most_3730"], "fixed-G 3730 wings agree")
    require(fixed["s_zero"]["cap_at_most_46_wings"] == independent_fixed["s0"]["intervals"]["cap_at_most_46"], "fixed-G 46 wings agree")
    require(fixed["uniform_positive"]["first_slack"] == independent_fixed["uniform_s"]["first_all_denominators_positive"]["s"] == 177_835, "fixed-G uniform positivity agrees")
    require(fixed["uniform_positive"]["maximum_cap_at_threshold"] == independent_fixed["uniform_s"]["first_all_denominators_positive"]["maximum_cap"] == 327_043, "fixed-G threshold cap agrees")
    for cap, threshold in (("3730", 177_901), ("46", 183_167)):
        require(fixed["uniform_caps"][cap]["first_uniform_slack"] == independent_fixed["uniform_s"]["cap_thresholds"][cap]["first_uniform_s"] == threshold, f"fixed-G cap {cap} threshold agrees")
        require(fixed["uniform_caps"][cap]["threshold_maximum_cap"] == independent_fixed["uniform_s"]["cap_thresholds"][cap]["maximum_cap"], f"fixed-G cap {cap} maximum agrees")
    require(fixed["direct_pair_union"]["N_G_at_most_one_from_m"] == independent_fixed["direct_overlap_threshold"] == ROOT_DEFICIT, "fixed-G singleton threshold agrees")

    whole = primary["whole_list_deep_cut"]
    independent_whole = independent["whole_list_Johnson"]
    require(whole["first_positive_denominator_slack"] == independent_whole["first_positive_s"] == WHOLE_LIST_FIRST_DEEP_SLACK, "whole-list threshold agrees")
    require(whole["threshold_cap"] == independent_whole["deep_cap"] == WHOLE_LIST_DEEP_CAP, "whole-list cap agrees")
    require(whole["forbidden_list_shallow_nonanchors_lower"] == independent_whole["shallow_residual"] == SHALLOW_NONANCHOR_LOWER, "shallow residual agrees")
    require(independent_whole["predecessor_denominator"] == -2_056_119, "whole-list predecessor denominator")
    require(independent_whole["denominator"] == 909_700, "whole-list denominator")
    require(independent_whole["numerator"] == 910_866_513_920, "whole-list numerator")
    rank46 = whole["rank46_cutoff_substitution"]
    independent_rank46 = independent_whole["rank46_cutoff_substitution"]
    require(rank46 == independent_rank46, "rank-46 nonbankability replay agrees")
    require(rank46 == {
        "bankable_replacement": False,
        "high_weight_count": 366_887,
        "parent_baseline": 16_517_335,
        "substituted_baseline": 17_511_197,
        "substituted_baseline_exceeds_budget_by": 733_982,
    }, "rank-46 nonbankability diagnostic")

    moment = primary["split_support_moment"]
    independent_moment = independent["split_support_moment"]
    require(moment["at_366886"] == independent_moment["F_values"]["366886"] == -35_406_814_945_353, "moment left endpoint agrees")
    require(moment["at_366887"] == independent_moment["F_values"]["366887"] == 14_351_365_971_580, "moment right endpoint agrees")
    require(independent_moment["integer_feasible_mu_interval"] == [326_152, 327_601], "moment integer feasible interval")
    require(independent_moment["mu_minimizer"] == "685509315589/2097152", "moment exact minimizer")
    require(independent_moment["sign_gate"] is True, "moment exact sign gate")

    wronskian = primary["wronskian_route_cut"]
    independent_wronskian = independent["Wronskian"]
    require(wronskian["cross_G"]["nonzero_for_distinct_canonical_pairs"] is True, "Wronskian nonzero")
    require(wronskian["cross_G"]["root_deficit_R_minus_w"] == independent_wronskian["H_overlap_only_excess_sum_threshold"] == ROOT_DEFICIT, "Wronskian root threshold agrees")
    require(independent_wronskian["s0_support_overlap_alone_contradicts"] is False, "boundary support overlap does not close")
    require(independent_wronskian["s0_combined_forced_overlap_max_minus_wronskian_allowance"] == -67_446, "combined boundary overlap deficit")

    base = primary["base_field_route_cut"]
    independent_base = independent["base_field_scalarization"]
    require(base["d_range"] == independent_base["d_range"] == [1, ROOT_DEFICIT], "base-field dimension range agrees")
    require(base["dimension_upper_bound_over_Fp"] == "d", "base-field dimension upper bound")
    require(base["V_equals_1_attains_dimension_d"] is True, "base-field sharpness")
    require(base["uniform_minimum_codimension_over_Fp"] == independent_base["true_V_equals_1_codimension_formula"] == "3d", "base-field codimension agrees")
    require(independent_base["fake_3m_independence_deficit"] == 202_341, "base-field fake-gain deficit")
    live_base = base["live_counterexample_reduction"]
    independent_live_base = independent_base["live_counterexample_reduction"]
    require(live_base["scalar_descent_margin"] == independent_live_base["strict_margin"] == 592_061_458_020_761_914_489_814_638_395_392, "scalar-descent strict margin agrees")
    require(live_base["quartic_violation_implies_base_boundary_violation"] is True, "quartic-to-base boundary reduction")
    require(live_base["projected_V_in_base_residue_ring"] is True, "projected V is base-field")
    require(live_base["projected_b_coefficients_in_base_field"] is True, "projected b is base-field")
    require(live_base["fresh_symbol_gate"] == "2^24<p", "base-field fresh-symbol gate")
    require(live_base["scalar_descent_is_ledger_payment"] is False, "scalar descent zero payment")
    require(independent_live_base["left"] == 75_911_179_514_902_718_909_260_442_370_048, "scalar-descent left side")
    require(independent_live_base["right"] == 667_972_637_535_664_633_399_075_080_765_440, "scalar-descent right side")

    v1 = primary["v_equals_1_route_cut"]
    independent_v1 = independent["V_equals_1_route_cut"]
    require(v1["deployed_source_list_floor"] == independent_v1["source_list_floor"] == 6_796_405, "V=1 source list floor agrees")
    require(v1["deployed_source_companion_floor"] == independent_v1["source_companion_floor"] == 6_796_404, "V=1 source companion floor agrees")
    require(v1["deployed_headroom_after_source"] == independent_v1["source_headroom"] == 9_980_810, "V=1 source headroom agrees")
    require(v1["toy_nonextremality"]["maximum_V_equals_1_companions"] == independent_v1["F7_control"]["maximum_V1_companions"] == 2, "F7 V=1 maximum agrees")
    require(v1["toy_nonextremality"]["arbitrary_V_companions"] == independent_v1["F7_control"]["arbitrary_V_companions"] == 3, "F7 arbitrary-V count agrees")
    require(v1["toy_nonextremality"]["arbitrary_V_beats_global_V_equals_1"] is True, "F7 nonextremality primary")
    require(independent_v1["F7_control"]["arbitrary_V_strictly_beats_global_V1"] is True, "F7 nonextremality independent")
    require(v1["general_reduction_to_V_equals_1"] is False and independent_v1["general_V1_reduction"] is False, "general V=1 reduction rejected")

    chebyshev = primary["chebyshev_support_countermodel"]
    independent_chebyshev = independent["Chebyshev_support_countermodel"]
    require(chebyshev["binary_gilbert"]["family_size_strict_lower"] == "2^576447", "Chebyshev Gilbert exponent")
    require(chebyshev["binary_gilbert"]["fixed_nonzero_weight_shell_strict_lower"] == "2^576427", "Chebyshev shell exponent")
    require(independent_chebyshev["greedy_code_size_strictly_exceeds_power_of_two_exponent"] == 576_447, "independent Gilbert exponent")
    require(independent_chebyshev["fixed_weight_shell_strictly_exceeds_power_of_two_exponent"] == 576_427, "independent shell exponent")
    require(chebyshev["chebyshev_support_model"]["support_size"] == independent_chebyshev["support_size"] == AGREEMENT, "Chebyshev support size agrees")
    require(chebyshev["scope_guards"] == {
        "common_V_realized": False,
        "polynomial_G_b_realized": False,
        "same_received_word_RS_list": False,
        "support_only_pairwise_root_budget_control": True,
    }, "Chebyshev countermodel scope")

    singleton = primary["singleton_packing"]
    independent_singleton = independent["Singleton_K_subset"]
    require(singleton["cap_at_n_minus_23"] == independent_singleton["ratio_floors"]["23"] == 8_389_620, "Singleton n-23 cap agrees")
    require(singleton["cap_at_n_minus_24"] == independent_singleton["ratio_floors"]["24"] == 16_779_424, "Singleton n-24 cap agrees")
    require(singleton["closes_boundary_census"] is False and independent_singleton["budget_fitting_transition_reachable_by_nonanchor"] is False, "Singleton route cut agrees")

    require(primary["ledger_state"]["ledger_movement"] == 0, "primary ledger movement zero")
    require(primary["ledger_state"]["row_closed"] is False, "primary row open")
    require(independent["ledger_movement"] == 0 and independent["row_closed"] is False, "independent ledger and row scope")


def verify_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    anchor = strict_payload_pin(PARENT_ANCHOR_PATH, PARENT_ANCHOR_PAYLOAD, "parent anchor-exchange")
    compiler = strict_payload_pin(PARENT_COMPILER_PATH, PARENT_COMPILER_PAYLOAD, "parent compiler")
    source = strict_payload_pin(SOURCE_ADAPTER_PATH, SOURCE_ADAPTER_PAYLOAD, "source adapter")

    require(anchor.get("theorem_id") == "M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1", "anchor predecessor theorem id")
    require(anchor.get("architecture_id") == ARCHITECTURE_ID, "anchor predecessor architecture")
    require(anchor.get("dependency_contract", {}).get("partition_sha256") == PARTITION_SHA256, "anchor predecessor partition")
    require(anchor.get("m31_specialization", {}).get("reduced_anchor_quantifier") == "j0=R; t=0; V arbitrary unit modulo L0", "anchor boundary quantifier")
    require(anchor.get("m31_specialization", {}).get("missing_uniform_pair_census_target") == NONANCHOR_CENSUS_TARGET, "anchor census target")
    require(anchor.get("ledger_state", {}).get("movement_from_this_packet") == 0, "anchor predecessor zero movement")
    require(anchor.get("ledger_state", {}).get("row_closed") is False, "anchor predecessor row open")

    require(compiler.get("compiler_id") == "M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V2", "parent compiler id")
    require(compiler.get("architecture_id") == ARCHITECTURE_ID, "parent compiler architecture")
    require(compiler.get("partition", {}).get("partition_sha256") == PARTITION_SHA256, "parent compiler partition")
    require(compiler.get("atom_state", {}).get("known_sum") == PARENT_U_PAID, "parent compiler U_paid")
    require(compiler.get("atom_state", {}).get("row_closed") is False, "parent compiler row open")

    require(source.get("architecture_id") == ARCHITECTURE_ID, "source adapter architecture")
    require(source.get("partition", {}).get("partition_sha256") == PARTITION_SHA256, "source adapter partition")
    require(source.get("partition", {}).get("unit") == UNIT, "source adapter unit")
    atoms = source.get("atoms")
    require(type(atoms) is list and [row.get("atom_id") for row in atoms] == list(ATOM_ORDER), "source adapter atom order")
    require(atoms[0].get("value") == PARENT_U_PAID and atoms[0].get("bankable") is True, "source adapter U_paid")
    require(all(row.get("value") is None and row.get("bankable") is False for row in atoms[1:]), "source adapter null atoms")
    return anchor, compiler, source


def verify_text_contracts() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 boundary common-V, full-locator route cut",
        "### Theorem 2.1",
        "W_ij = G_i b_j - G_j b_i.",
        "F(366,886) = -35,406,814,945,353 < 0",
        "N_deep(366,887)",
        "15,775,933",
        "The V=1 equality shows that no larger codimension can be",
        "### 6.3 The V=1 slice is a prefix fiber but is not extremal",
        "max_(S,V)#X_S(V) >= 3 > 2 = max_S #X_S(1)",
        "This section is an impossibility result for one enumerated proof interface.",
        "The row-closing bound #X(V)<=16777214 remains unproved",
        "ledger movement = 0",
    ):
        require(anchor in note, f"theorem-note anchor: {anchor}")

    readme = README_PATH.read_text(encoding="utf-8")
    for anchor in (
        "M31 boundary common-V cross-G route-cut packet",
        "verify_m31_boundary_cross_g_route_cut_v1.py",
        "verify_m31_boundary_cross_g_route_cut_v1_independent.py",
        "verify_m31_boundary_common_v_cross_g_route_cut_packet_v1.py",
        "Ledger movement is zero.",
        "base-field common-(V), cross-(G) coefficient-incidence",
    ):
        require(anchor in readme, f"README anchor: {anchor}")

    foundation = CAP_FOUNDATION_PATH.read_text(encoding="utf-8")
    require("\\label{lem:cheb-fibers}" in foundation, "CAP exact Chebyshev fibre lemma anchor")
    require("Mersenne-$31" in foundation, "CAP M31 deployment anchor")
    require("n=2^{21}" in foundation, "CAP deployed length anchor")

    ledger = ACTIVE_LEDGER_PATH.read_text(encoding="utf-8")
    require("U_{\\rm paid}+U_Q+U_{\\rm list-int}+U_{\\rm ext}+U_{\\rm new}" in ledger, "active five-atom chronology anchor")

    scalar_note = SCALAR_DESCENT_NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# Mersenne-31 scalar-descent equivalence",
        "L t H_r < g N_r",
        "margin  = 592,061,458,020,761,914,489,814,638,395,392",
        "B_F_p(1,116,023) <= 16,777,215",
        "It makes no ledger payment",
    ):
        require(anchor in scalar_note, f"scalar-descent note anchor: {anchor}")

    prefix_note = PREFIX_COUNTEREXAMPLE_NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# Counterexamples to Global Prefix/Staircase Extremality",
        "Counterexample 1: cross-prefix gluing over `F_7`",
        "|List_3(y)| = 4 > 3 = max_z |Fib_1(z)|",
    ):
        require(anchor in prefix_note, f"prefix-counterexample note anchor: {anchor}")

    fixed_note = FIXED_REMAINDER_NOTE_PATH.read_text(encoding="utf-8")
    for anchor in (
        "# M31 Chebyshev fixed-remainder exact C1 boundary source and raw route cut",
        "\\ge6{,}796{,}405.",
        "full depth-\\((A-K)\\) prefix fiber",
    ):
        require(anchor in fixed_note, f"fixed-remainder note anchor: {anchor}")


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding(
            "M31_CROSS_G_CUT::packet_schema",
            "experimental/data/schemas/m31_boundary_common_v_cross_g_route_cut_v1.schema.json",
            "packet_schema",
            "Closed top-level schema for the exact route cuts and residual localization.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::packet_verifier",
            "experimental/scripts/verify_m31_boundary_common_v_cross_g_route_cut_packet_v1.py",
            "packet_verifier",
            "Fail-closed payload, source, replay, theorem-anchor, and mutation verifier.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::primary_exact_replay",
            "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py",
            "primary_exact_replay",
            "Primary stdlib exact endpoint scans, route cuts, summary, and mutations.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::independent_exact_replay",
            "experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1_independent.py",
            "independent_exact_replay",
            "Independent stdlib derivation of every load-bearing arithmetic threshold.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::theorem_note",
            "experimental/notes/thresholds/m31_boundary_common_v_cross_g_route_cut_v1.md",
            "theorem_note",
            "Proofs, exact endpoints, interface countermodel, and terminal residual.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::packet_readme",
            "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/README.md",
            "packet_readme",
            "Replay instructions and explicit zero-payment scope.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::anchor_exchange_parent",
            "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json",
            "anchor_exchange_parent_manifest",
            "Sealed boundary-anchor divisor and gcd census predecessor.",
            internal_payload_sha256=PARENT_ANCHOR_PAYLOAD,
        ),
        source_binding(
            "M31_CROSS_G_CUT::global_compiler_parent",
            "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json",
            "global_compiler_parent_manifest",
            "Sealed v4 five-atom completion chronology and row target.",
            internal_payload_sha256=PARENT_COMPILER_PAYLOAD,
        ),
        source_binding(
            "M31_CROSS_G_CUT::source_adapter_parent",
            "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
            "source_adapter_parent_manifest",
            "Sealed codeword-valued partition and currently banked low atom.",
            internal_payload_sha256=SOURCE_ADAPTER_PAYLOAD,
        ),
        source_binding(
            "M31_CROSS_G_CUT::anchor_exchange_parent_note",
            "experimental/notes/thresholds/m31_all_weight_anchor_exchange_pade_bijection_v1.md",
            "anchor_exchange_parent_note",
            "Exact boundary forcing and arbitrary-unit-V census statement.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::scalar_descent_note",
            "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
            "scalar_descent_note",
            "Proved quartic-to-base-field list-threshold equivalence at forbidden size.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::scalar_descent_replay",
            "experimental/scripts/verify_m31_scalar_descent_equivalence.py",
            "scalar_descent_replay",
            "Exact projective-functional incidence margin and semantic mutations.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::prefix_counterexample_note",
            "experimental/notes/thresholds/prefix_staircase_extremality_counterexamples.md",
            "prefix_counterexample_note",
            "Exact F7 counterexample to global V=1 or one-prefix extremality.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::prefix_counterexample_replay",
            "experimental/scripts/verify_prefix_staircase_extremality_counterexamples.py",
            "prefix_counterexample_replay",
            "Exhaustive F7 list and prefix-fibre enumeration.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::fixed_remainder_source_note",
            "experimental/notes/thresholds/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut.md",
            "fixed_remainder_source_note",
            "Proved deployed V=1 locator-prefix source floor.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::fixed_remainder_source_replay",
            "experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py",
            "fixed_remainder_source_replay",
            "Exact deployed fixed-remainder source-floor arithmetic and mutations.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::cap_foundation",
            "tex/cs25_cap_v13_2.tex",
            "cap_foundation",
            "Deployed M31 parameters and exact Chebyshev fibre tower.",
        ),
        source_binding(
            "M31_CROSS_G_CUT::active_v4_ledger",
            "experimental/grande_finale.tex",
            "active_v4_ledger",
            "Active LIST owner chronology and null-atom semantics.",
        ),
    ]


def build_template() -> dict[str, Any]:
    arithmetic()
    verify_text_contracts()
    anchor, compiler, source = verify_dependencies()
    primary, independent = replay_summaries()
    scalar_descent = replay_scalar_descent()
    v1_source_replays = replay_v1_sources()
    bindings = source_bindings()
    require(len(bindings) == 18, "source binding count")
    require(len({row["binding_id"] for row in bindings}) == len(bindings), "unique binding ids")
    require(len({row["path"] for row in bindings}) == len(bindings), "unique binding paths")

    fixed = copy.deepcopy(primary["fixed_G_bound"])
    fixed["independent_endpoint_replay"] = {
        "boundary_values": copy.deepcopy(independent["fixed_G"]["s0"]["boundary_values"]),
        "uniform_s": copy.deepcopy(independent["fixed_G"]["uniform_s"]),
    }

    wronskian = copy.deepcopy(primary["wronskian_route_cut"])
    wronskian["independent_support_overlap_replay"] = copy.deepcopy(independent["Wronskian"])

    moment = copy.deepcopy(primary["split_support_moment"])
    moment["independent_exact_feasible_region"] = copy.deepcopy(independent["split_support_moment"])
    moment["scope"] = "SELECTED_FULL_B_STAR_NONANCHOR_FAMILY_NOT_THE_SHALLOW_SUBFAMILY"

    whole = copy.deepcopy(primary["whole_list_deep_cut"])
    whole["exact_denominator_at_threshold"] = independent["whole_list_Johnson"]["denominator"]
    whole["exact_numerator_at_threshold"] = independent["whole_list_Johnson"]["numerator"]
    whole["exact_predecessor_denominator"] = independent["whole_list_Johnson"]["predecessor_denominator"]
    whole["direct_list_diagnostic_not_ledger_payment"] = True

    base = copy.deepcopy(primary["base_field_route_cut"])
    base["independent_exact_replay"] = copy.deepcopy(independent["base_field_scalarization"])

    v1 = copy.deepcopy(primary["v_equals_1_route_cut"])
    v1["independent_exact_replay"] = copy.deepcopy(independent["V_equals_1_route_cut"])

    chebyshev = copy.deepcopy(primary["chebyshev_support_countermodel"])
    chebyshev["independent_exact_replay"] = copy.deepcopy(independent["Chebyshev_support_countermodel"])

    singleton = copy.deepcopy(primary["singleton_packing"])
    singleton["independent_exact_replay"] = copy.deepcopy(independent["Singleton_K_subset"])

    payload: dict[str, Any] = {
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "base_field_route_cut": base,
        "boundary_coordinate": {
            "anchor": {
                "E0_size": RADIUS,
                "S0_size": AGREEMENT,
                "anchor_slack_t": 0,
                "anchor_weight": RADIUS,
                "V_quantifier": "ARBITRARY_UNIT_MODULO_L0",
            },
            "canonical_nonanchor_pair": {
                "G_gate": "G monic; G divides A0; w+1<=m=deg(G)<=R",
                "H_definition": "H=monic_gcd(L0,G-bV)",
                "b_gate": "b nonzero; deg(b)<m-w; gcd(b,G)=1",
                "excess": "s=deg(H)-m>=0",
                "exact_agreement": "a+s",
                "exact_error_weight": "R-s",
                "support": "T=(S0 minus Z(G)) disjoint-union Z(H)",
            },
            "pair_support_inequality": "|Z(G_i) intersect Z(G_j)|+|Z(H_i) intersect Z(H_j)|<=m_i+m_j-w-1",
            "pair_support_inequality_retains_common_V": False,
            "uniqueness_unit": UNIT,
        },
        "chebyshev_support_countermodel": chebyshev,
        "dependency_contract": {
            "anchor_exchange_parent": {
                "path": str(PARENT_ANCHOR_PATH.relative_to(ROOT)),
                "payload_sha256": anchor["payload_sha256"],
                "theorem_id": anchor["theorem_id"],
            },
            "global_compiler_parent": {
                "compiler_id": compiler["compiler_id"],
                "path": str(PARENT_COMPILER_PATH.relative_to(ROOT)),
                "payload_sha256": compiler["payload_sha256"],
            },
            "source_adapter_parent": {
                "path": str(SOURCE_ADAPTER_PATH.relative_to(ROOT)),
                "payload_sha256": source["payload_sha256"],
            },
            "partition_sha256": PARTITION_SHA256,
            "stacked_dependency": True,
            "exact_replays": {
                "independent_summary_sha256": sha256_bytes(canonical_json(independent)),
                "primary_summary_sha256": sha256_bytes(canonical_json(primary)),
                "scalar_descent_output_sha256": sha256_bytes(canonical_json(scalar_descent)),
                **v1_source_replays,
                "share_implementation_code": False,
                "subprocess_replayed_by_packet": True,
            },
        },
        "deployed_parameters": {
            **copy.deepcopy(primary["deployed_parameters"]),
            "code_field_cardinality": str(Q),
            "nonanchor_census_target": NONANCHOR_CENSUS_TARGET,
            "parent_U_paid": PARENT_U_PAID,
            "root_deficit_R_minus_w": ROOT_DEFICIT,
            "target_epsilon": "2^-100",
        },
        "fixed_G_bound": fixed,
        "ledger_state": {
            "atoms": [
                {
                    "atom_id": "U_paid",
                    "bankable": True,
                    "status": "BANKED_BY_PARENT_NOT_THIS_PACKET",
                    "value": PARENT_U_PAID,
                },
                *[
                    {
                        "atom_id": atom,
                        "bankable": False,
                        "status": "OPEN_UNPAID",
                        "value": None,
                    }
                    for atom in ATOM_ORDER[1:]
                ],
            ],
            "deep_cut_is_direct_diagnostic_not_payment": True,
            "known_parent_sum": PARENT_U_PAID,
            "movement_from_this_packet": 0,
            "null_atoms": list(ATOM_ORDER[1:]),
            "official_endpoint_or_score_movement": 0,
            "row_closed": False,
        },
        "nonclaims": {
            "chebyshev_countermodel_is_a_received_word_list": False,
            "chebyshev_countermodel_realizes_common_V": False,
            "coefficient_incidence_bound_proved": False,
            "complete_M31_list_bound_proved": False,
            "deep_cut_is_a_v4_atom_payment": False,
            "fixed_G_caps_sum_over_G": False,
            "full_locator_family_has_multiple_distinct_G_proved": False,
            "ledger_atom_paid_by_this_packet": False,
            "locators_are_proved_distinct": False,
            "official_endpoint_or_score_changed": False,
            "pairwise_support_bounds_close_global_census": False,
            "row_closed": False,
            "scalar_descent_closes_prime_field_row": False,
            "scalarization_alone_counts_full_census": False,
            "singleton_packing_reaches_live_radius": False,
            "stable_paper_modified": False,
        },
        "payload_sha256": "",
        "residual_localization": {
            "any_forbidden_boundary_census_contains_at_least": SHALLOW_NONANCHOR_LOWER,
            "anchor_coordinate_field_scope": "VALID_UNIFORMLY_FOR_ARBITRARY_QUARTIC_UNIT_V",
            "common_V_required": True,
            "full_locator_census": True,
            "live_sufficient_counterexample_field": "F_p",
            "live_sufficient_pair_coefficients": "V_AND_b_IN_F_p[X]",
            "locator_range": "G_i ranges over all monic divisors of A0; repetitions allowed",
            "multiple_distinct_G_not_proved": True,
            "pair_conditions": [
                "G_i divides A0 and 67448<=deg(G_i)<=981129",
                "b_i nonzero; deg(b_i)<deg(G_i)-67447; gcd(b_i,G_i)=1",
                "H_i=gcd(L0,G_i-b_i*V)",
                "deg(G_i)<=deg(H_i)<=deg(G_i)+366886",
            ],
            "remaining_exact_census": "sum_G #admissible_b<=16777214",
            "remaining_exact_census_proved": False,
            "quartic_violation_implies_base_field_boundary_violation": True,
            "scalar_descent_is_ledger_payment": False,
            "scalar_descent_strict_margin": 592_061_458_020_761_914_489_814_638_395_392,
            "shallow_excess_range": [0, 366_886],
            "successor": "BASE_FIELD_SPLIT_FLAT_FULL_GCD_INCIDENCE_WITH_ONE_COMMON_ARBITRARY_V",
            "terminal": "UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE",
        },
        "row_contract": {
            "agreement": AGREEMENT,
            "complete_list_budget": BUDGET,
            "object": "LIST",
            "partition_sha256": PARTITION_SHA256,
            "quantifier": "EVERY_BOUNDARY_ANCHOR_M31_TRIPLE_A0_L0_V_WITH_V_ARBITRARY_UNIT",
            "row": "Mersenne-31 list at 2^-100",
            "target_epsilon": "2^-100",
            "unit": UNIT,
            "workboard_item": "M1/L",
        },
        "schema": SCHEMA_ID,
        "singleton_packing": singleton,
        "source_bindings": bindings,
        "split_support_moment": moment,
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "v_equals_1_route_cut": v1,
        "whole_list_deep_cut": whole,
        "wronskian_route_cut": wronskian,
    }
    return seal(payload)


def verify_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list and len(bindings) == 18, "source binding list")
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
        require(type(binding["sha256"]) is str and len(binding["sha256"]) == 64, f"binding {index}: hash shape")
        require(set(binding["sha256"]) <= set("0123456789abcdef"), f"binding {index}: lowercase hex hash")
        require(binding["sha256"] == sha256_path(path), f"binding {index}: fresh hash")
        internal = binding["internal_payload_sha256"]
        if internal is not None:
            pins += 1
            require(type(internal) is str and len(internal) == 64, f"binding {index}: pin shape")
            strict_payload_pin(path, internal, f"binding {index}")
    require(pins == 3, "three internal payload pins")


def validate(payload: dict[str, Any], expected: dict[str, Any] | None = None) -> None:
    arithmetic()
    require(payload.get("schema") == SCHEMA_ID, "payload schema")
    require(payload.get("theorem_id") == THEOREM_ID, "theorem id")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "architecture id")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    require(payload.get("status") == STATUS, "status")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")

    boundary = payload["boundary_coordinate"]
    require(boundary["anchor"] == {
        "E0_size": RADIUS,
        "S0_size": AGREEMENT,
        "anchor_slack_t": 0,
        "anchor_weight": RADIUS,
        "V_quantifier": "ARBITRARY_UNIT_MODULO_L0",
    }, "boundary anchor coordinate")
    require(boundary["canonical_nonanchor_pair"]["H_definition"] == "H=monic_gcd(L0,G-bV)", "boundary full gcd")
    require(boundary["canonical_nonanchor_pair"]["excess"] == "s=deg(H)-m>=0", "boundary excess")
    require(boundary["pair_support_inequality_retains_common_V"] is False, "pair support loses common V")
    require(boundary["uniqueness_unit"] == UNIT, "boundary codeword unit")

    fixed = payload["fixed_G_bound"]
    require(fixed["s_zero"]["positive_wings"] == [[67_448, 72_858], [908_271, 981_129]], "fixed-G positivity wings")
    require(fixed["s_zero"]["cap_at_most_3730_wings"] == [[67_448, 72_837], [908_292, 981_129]], "fixed-G 3730 wings")
    require(fixed["s_zero"]["cap_at_most_46_wings"] == [[67_448, 71_176], [909_953, 981_129]], "fixed-G 46 wings")
    require(fixed["uniform_positive"]["first_slack"] == 177_835, "fixed-G positive threshold")
    require(fixed["uniform_caps"]["3730"]["first_uniform_slack"] == 177_901, "fixed-G uniform 3730")
    require(fixed["uniform_caps"]["46"]["first_uniform_slack"] == 183_167, "fixed-G uniform 46")
    require(fixed["direct_pair_union"]["N_G_at_most_one_from_m"] == ROOT_DEFICIT, "fixed-G singleton threshold")

    whole = payload["whole_list_deep_cut"]
    require(whole["first_positive_denominator_slack"] == WHOLE_LIST_FIRST_DEEP_SLACK, "whole-list deep threshold")
    require(whole["threshold_cap"] == WHOLE_LIST_DEEP_CAP, "whole-list deep cap")
    require(whole["forbidden_list_shallow_nonanchors_lower"] == SHALLOW_NONANCHOR_LOWER, "whole-list shallow residue")
    require(whole["exact_predecessor_denominator"] == -2_056_119, "whole-list predecessor denominator")
    require(whole["exact_denominator_at_threshold"] == 909_700, "whole-list threshold denominator")
    require(whole["exact_numerator_at_threshold"] == 910_866_513_920, "whole-list threshold numerator")
    require(whole["direct_list_diagnostic_not_ledger_payment"] is True, "whole-list cut is not payment")
    require(whole["rank46_cutoff_substitution"] == {
        "bankable_replacement": False,
        "high_weight_count": 366_887,
        "parent_baseline": 16_517_335,
        "substituted_baseline": 17_511_197,
        "substituted_baseline_exceeds_budget_by": 733_982,
    }, "rank-46 cutoff substitution is nonbankable")

    moment = payload["split_support_moment"]
    require(moment["at_366886"] == -35_406_814_945_353, "moment left value")
    require(moment["at_366887"] == 14_351_365_971_580, "moment right value")
    require(moment["unique_root_in_open_interval"] == [366_886, 366_887], "moment root interval")
    require(moment["independent_exact_feasible_region"]["integer_feasible_mu_interval"] == [326_152, 327_601], "moment feasible integer mu")
    require(moment["scope"] == "SELECTED_FULL_B_STAR_NONANCHOR_FAMILY_NOT_THE_SHALLOW_SUBFAMILY", "moment scope")

    wronskian = payload["wronskian_route_cut"]
    require(wronskian["cross_G"]["polynomial"] == "W_12=G_1*b_2-G_2*b_1", "Wronskian polynomial")
    require(wronskian["cross_G"]["nonzero_for_distinct_canonical_pairs"] is True, "Wronskian nonzero")
    require(wronskian["cross_G"]["root_deficit_R_minus_w"] == ROOT_DEFICIT, "Wronskian threshold")
    require(wronskian["independent_support_overlap_replay"]["s0_support_overlap_alone_contradicts"] is False, "Wronskian boundary route cut")

    base = payload["base_field_route_cut"]
    require(base["d_range"] == [1, ROOT_DEFICIT], "base-field d range")
    require(base["dimension_upper_bound_over_Fp"] == "d", "base-field dimension")
    require(base["uniform_minimum_codimension_over_Fp"] == "3d", "base-field codimension")
    require(base["general_unit_V_forced_to_1"] is False, "base-field arbitrary V guard")
    require(base["dimension_count_is_a_census"] is False, "base-field noncensus guard")
    live_base = base["live_counterexample_reduction"]
    require(live_base["quartic_violation_implies_base_boundary_violation"] is True, "live quartic-to-base reduction")
    require(live_base["projected_V_in_base_residue_ring"] is True, "live V base-field")
    require(live_base["projected_b_coefficients_in_base_field"] is True, "live b base-field")
    require(live_base["scalar_descent_margin"] == 592_061_458_020_761_914_489_814_638_395_392, "live scalar-descent margin")
    require(live_base["scalar_descent_is_ledger_payment"] is False, "scalar descent not a payment")

    v1 = payload["v_equals_1_route_cut"]
    require(v1["exact_identity"] == "#X_S(1)=|Fib_w(prefix_w(L_S))|-1", "V=1 prefix identity")
    require(v1["all_pairs_are_boundary"] is True, "V=1 boundary layer")
    require(v1["deployed_source_list_floor"] == 6_796_405, "V=1 deployed list floor")
    require(v1["deployed_source_companion_floor"] == 6_796_404, "V=1 deployed companion floor")
    require(v1["deployed_headroom_after_source"] == 9_980_810, "V=1 deployed headroom")
    require(v1["source_floor_is_uniform_over_anchors"] is False, "V=1 nonuniform source guard")
    toy_v1 = v1["toy_nonextremality"]
    require(toy_v1["depth_one_prefix_fibre_sizes"] == [3, 3, 3, 2, 3, 3, 3], "F7 prefix fibres")
    require(toy_v1["maximum_V_equals_1_companions"] == 2, "F7 V=1 maximum")
    require(toy_v1["arbitrary_V_companions"] == 3, "F7 arbitrary-V companions")
    require(toy_v1["H0_table_on_E0"] == [6, 4, 1], "F7 H0 table")
    require(toy_v1["V_table_on_E0"] == [6, 2, 1], "F7 V table")
    require(toy_v1["arbitrary_V_beats_global_V_equals_1"] is True, "F7 V=1 nonextremality")
    require(v1["general_reduction_to_V_equals_1"] is False, "general V=1 reduction rejected")
    require(v1["deployed_domain_comparison_proved"] is False, "deployed V=1 comparison remains open")
    require(v1["ledger_payment"] is False, "V=1 route cut zero payment")
    require(v1["independent_exact_replay"]["source_companion_floor"] == 6_796_404, "V=1 independent source floor")
    require(v1["independent_exact_replay"]["F7_control"]["arbitrary_V_strictly_beats_global_V1"] is True, "V=1 independent nonextremality")

    chebyshev = payload["chebyshev_support_countermodel"]
    require(chebyshev["binary_gilbert"]["family_size_strict_lower"] == "2^576447", "Chebyshev family size")
    require(chebyshev["binary_gilbert"]["fixed_nonzero_weight_shell_strict_lower"] == "2^576427", "Chebyshev shell size")
    require(chebyshev["chebyshev_support_model"]["full_T2_count"] == W, "Chebyshev T2 count")
    require(chebyshev["chebyshev_support_model"]["full_T4_count"] == 0, "Chebyshev T4 count")
    require(chebyshev["scope_guards"]["same_received_word_RS_list"] is False, "Chebyshev received-word guard")
    require(chebyshev["scope_guards"]["common_V_realized"] is False, "Chebyshev common-V guard")
    require(chebyshev["scope_guards"]["polynomial_G_b_realized"] is False, "Chebyshev polynomial guard")

    singleton = payload["singleton_packing"]
    require(singleton["cap_at_n_minus_23"] == 8_389_620, "Singleton n-23")
    require(singleton["cap_at_n_minus_24"] == 16_779_424, "Singleton n-24")
    require(singleton["maximum_nonanchor_agreement"] == 2_029_704, "Singleton nonanchor agreement")
    require(singleton["closes_boundary_census"] is False, "Singleton route cut")

    residual = payload["residual_localization"]
    require(residual["any_forbidden_boundary_census_contains_at_least"] == SHALLOW_NONANCHOR_LOWER, "residual shallow mass")
    require(residual["shallow_excess_range"] == [0, 366_886], "residual shallow range")
    require(residual["common_V_required"] is True, "residual common V")
    require(residual["full_locator_census"] is True, "residual full locator")
    require(residual["multiple_distinct_G_not_proved"] is True, "locator-distinctness guard")
    require(residual["remaining_exact_census_proved"] is False, "residual theorem open")
    require(residual["anchor_coordinate_field_scope"] == "VALID_UNIFORMLY_FOR_ARBITRARY_QUARTIC_UNIT_V", "universal anchor coordinate scope")
    require(residual["live_sufficient_counterexample_field"] == "F_p", "live residual base field")
    require(residual["live_sufficient_pair_coefficients"] == "V_AND_b_IN_F_p[X]", "live residual V and b field")
    require(residual["quartic_violation_implies_base_field_boundary_violation"] is True, "residual scalar descent")
    require(residual["scalar_descent_is_ledger_payment"] is False, "residual scalar descent not payment")
    require(residual["scalar_descent_strict_margin"] == 592_061_458_020_761_914_489_814_638_395_392, "residual scalar-descent margin")
    require(residual["terminal"] == "UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE", "residual terminal")

    ledger = payload["ledger_state"]
    require(ledger["movement_from_this_packet"] == 0, "zero ledger movement")
    require(ledger["official_endpoint_or_score_movement"] == 0, "zero official movement")
    require(ledger["known_parent_sum"] == PARENT_U_PAID, "parent U_paid")
    require(ledger["null_atoms"] == list(ATOM_ORDER[1:]), "four null atoms")
    require(ledger["row_closed"] is False, "row open")
    require(ledger["deep_cut_is_direct_diagnostic_not_payment"] is True, "deep cut not a payment")
    require([row["atom_id"] for row in ledger["atoms"]] == list(ATOM_ORDER), "ledger atom order")
    require(all(row["value"] is None and row["bankable"] is False for row in ledger["atoms"][1:]), "ledger null values")
    require(all(value is False for value in payload["nonclaims"].values()), "all nonclaims false")

    dependency = payload["dependency_contract"]
    require(dependency["anchor_exchange_parent"]["payload_sha256"] == PARENT_ANCHOR_PAYLOAD, "anchor predecessor pin")
    require(dependency["global_compiler_parent"]["payload_sha256"] == PARENT_COMPILER_PAYLOAD, "compiler predecessor pin")
    require(dependency["source_adapter_parent"]["payload_sha256"] == SOURCE_ADAPTER_PAYLOAD, "source-adapter predecessor pin")
    require(dependency["partition_sha256"] == PARTITION_SHA256, "partition digest")
    require(dependency["stacked_dependency"] is True, "stacked dependency")
    require(dependency["exact_replays"]["share_implementation_code"] is False, "independent replay implementations")
    require(dependency["exact_replays"]["subprocess_replayed_by_packet"] is True, "subprocess replay contract")
    require(type(dependency["exact_replays"]["scalar_descent_output_sha256"]) is str and len(dependency["exact_replays"]["scalar_descent_output_sha256"]) == 64, "scalar-descent replay hash")
    require(type(dependency["exact_replays"]["prefix_counterexample_output_sha256"]) is str and len(dependency["exact_replays"]["prefix_counterexample_output_sha256"]) == 64, "prefix-counterexample replay hash")
    require(type(dependency["exact_replays"]["fixed_remainder_output_sha256"]) is str and len(dependency["exact_replays"]["fixed_remainder_output_sha256"]) == 64, "fixed-remainder replay hash")

    row = payload["row_contract"]
    require(row["object"] == "LIST" and row["unit"] == UNIT, "row object and unit")
    require(row["agreement"] == AGREEMENT and row["complete_list_budget"] == BUDGET, "row endpoint")
    require(row["partition_sha256"] == PARTITION_SHA256, "row partition")
    verify_source_bindings(payload["source_bindings"])

    if expected is None:
        expected = build_template()
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
    def add_unknown(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["unknown"] = 1
        return seal(out)

    def delete_key(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        del out["whole_list_deep_cut"]
        return seal(out)

    def stale_seal(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["deployed_parameters"]["agreement"] -= 1
        return out

    def delete_binding(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"].pop()
        return seal(out)

    def duplicate_binding(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["source_bindings"][1]["binding_id"] = out["source_bindings"][0]["binding_id"]
        return seal(out)

    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutate(("schema",), "rs-mca-m31-boundary-common-v-cross-g-route-cut-v0")),
        ("theorem id", mutate(("theorem_id",), "M31_CROSS_G_ROUTE_CUT_V0")),
        ("architecture", mutate(("architecture_id",), "GRANDE_FINALE_V3")),
        ("artifact kind", mutate(("artifact_kind",), "LIST_BOUND")),
        ("false status closure", mutate(("status",), "ROW_CLOSED")),
        ("unknown top key", add_unknown),
        ("missing top key", delete_key),
        ("stale payload seal", stale_seal),
        ("anchor S0", mutate(("boundary_coordinate", "anchor", "S0_size"), AGREEMENT - 1)),
        ("anchor E0", mutate(("boundary_coordinate", "anchor", "E0_size"), RADIUS - 1)),
        ("anchor nonboundary", mutate(("boundary_coordinate", "anchor", "anchor_slack_t"), 1)),
        ("anchor V structured", mutate(("boundary_coordinate", "anchor", "V_quantifier"), "LOW_DEGREE")),
        ("H arbitrary divisor", mutate(("boundary_coordinate", "canonical_nonanchor_pair", "H_definition"), "H divides gcd(L0,G-bV)")),
        ("wrong excess sign", mutate(("boundary_coordinate", "canonical_nonanchor_pair", "excess"), "s=m-deg(H)>=0")),
        ("support retains V", mutate(("boundary_coordinate", "pair_support_inequality_retains_common_V"), True)),
        ("wrong unit", mutate(("boundary_coordinate", "uniqueness_unit"), "PAIRS")),
        ("parameter p", mutate(("deployed_parameters", "p"), P - 1)),
        ("parameter n", mutate(("deployed_parameters", "n"), N - 1)),
        ("parameter K", mutate(("deployed_parameters", "K"), K - 1)),
        ("parameter agreement", mutate(("deployed_parameters", "agreement"), AGREEMENT - 1)),
        ("parameter radius", mutate(("deployed_parameters", "R"), RADIUS - 1)),
        ("parameter w", mutate(("deployed_parameters", "w"), W - 1)),
        ("parameter budget", mutate(("deployed_parameters", "budget"), BUDGET - 1)),
        ("parameter census target", mutate(("deployed_parameters", "nonanchor_census_target"), BUDGET)),
        ("parameter root deficit", mutate(("deployed_parameters", "root_deficit_R_minus_w"), ROOT_DEFICIT - 1)),
        ("fixed positive wing", mutate(("fixed_G_bound", "s_zero", "positive_wings", 0, 1), 72_859)),
        ("fixed 3730 wing", mutate(("fixed_G_bound", "s_zero", "cap_at_most_3730_wings", 1, 0), 908_291)),
        ("fixed 46 wing", mutate(("fixed_G_bound", "s_zero", "cap_at_most_46_wings", 0, 1), 71_177)),
        ("fixed positive slack", mutate(("fixed_G_bound", "uniform_positive", "first_slack"), 177_834)),
        ("fixed positive cap", mutate(("fixed_G_bound", "uniform_positive", "maximum_cap_at_threshold"), 327_044)),
        ("fixed 3730 slack", mutate(("fixed_G_bound", "uniform_caps", "3730", "first_uniform_slack"), 177_900)),
        ("fixed 3730 predecessor", mutate(("fixed_G_bound", "uniform_caps", "3730", "predecessor_maximum_cap"), 3_730)),
        ("fixed 46 slack", mutate(("fixed_G_bound", "uniform_caps", "46", "first_uniform_slack"), 183_166)),
        ("fixed singleton", mutate(("fixed_G_bound", "direct_pair_union", "N_G_at_most_one_from_m"), ROOT_DEFICIT - 1)),
        ("fixed independent boundary", mutate(("fixed_G_bound", "independent_endpoint_replay", "boundary_values", "72858", "cap"), 174_020)),
        ("Wronskian zero", mutate(("wronskian_route_cut", "cross_G", "nonzero_for_distinct_canonical_pairs"), False)),
        ("Wronskian sign", mutate(("wronskian_route_cut", "cross_G", "polynomial"), "G_1*b_2+G_2*b_1")),
        ("Wronskian degree", mutate(("wronskian_route_cut", "cross_G", "degree_bound"), "deg(W_12)<=m_1+m_2-w")),
        ("Wronskian root threshold", mutate(("wronskian_route_cut", "cross_G", "root_deficit_R_minus_w"), ROOT_DEFICIT - 1)),
        ("Wronskian false boundary contradiction", mutate(("wronskian_route_cut", "independent_support_overlap_replay", "s0_support_overlap_alone_contradicts"), True)),
        ("moment left sign", mutate(("split_support_moment", "at_366886"), 1)),
        ("moment right sign", mutate(("split_support_moment", "at_366887"), -1)),
        ("moment root endpoint", mutate(("split_support_moment", "unique_root_in_open_interval", 1), 366_888)),
        ("moment list size", mutate(("split_support_moment", "list_size"), BUDGET - 1)),
        ("moment mu interval", mutate(("split_support_moment", "independent_exact_feasible_region", "integer_feasible_mu_interval", 0), 326_151)),
        ("moment minimizer", mutate(("split_support_moment", "independent_exact_feasible_region", "mu_minimizer"), "0")),
        ("moment wrong scope", mutate(("split_support_moment", "scope"), "SHALLOW_SUBFAMILY")),
        ("deep threshold", mutate(("whole_list_deep_cut", "first_positive_denominator_slack"), 366_886)),
        ("deep cap", mutate(("whole_list_deep_cut", "threshold_cap"), WHOLE_LIST_DEEP_CAP + 1)),
        ("deep predecessor fits", mutate(("whole_list_deep_cut", "predecessor_fits_budget"), True)),
        ("deep predecessor denominator", mutate(("whole_list_deep_cut", "exact_predecessor_denominator"), -2_056_118)),
        ("deep denominator", mutate(("whole_list_deep_cut", "exact_denominator_at_threshold"), 909_699)),
        ("deep numerator", mutate(("whole_list_deep_cut", "exact_numerator_at_threshold"), 910_866_513_919)),
        ("shallow mass", mutate(("whole_list_deep_cut", "forbidden_list_shallow_nonanchors_lower"), SHALLOW_NONANCHOR_LOWER - 1)),
        ("deep called payment", mutate(("whole_list_deep_cut", "direct_list_diagnostic_not_ledger_payment"), False)),
        ("rank46 false payment", mutate(("whole_list_deep_cut", "rank46_cutoff_substitution", "bankable_replacement"), True)),
        ("rank46 substituted baseline", mutate(("whole_list_deep_cut", "rank46_cutoff_substitution", "substituted_baseline"), 17_511_196)),
        ("rank46 excess", mutate(("whole_list_deep_cut", "rank46_cutoff_substitution", "substituted_baseline_exceeds_budget_by"), 733_981)),
        ("base d range", mutate(("base_field_route_cut", "d_range", 1), ROOT_DEFICIT - 1)),
        ("base dimension", mutate(("base_field_route_cut", "dimension_upper_bound_over_Fp"), "3d")),
        ("base codimension", mutate(("base_field_route_cut", "uniform_minimum_codimension_over_Fp"), "3m")),
        ("base force V1", mutate(("base_field_route_cut", "general_unit_V_forced_to_1"), True)),
        ("base false census", mutate(("base_field_route_cut", "dimension_count_is_a_census"), True)),
        ("base fake deficit", mutate(("base_field_route_cut", "independent_exact_replay", "fake_3m_independence_deficit"), 202_340)),
        ("scalar descent margin", mutate(("base_field_route_cut", "live_counterexample_reduction", "scalar_descent_margin"), 1)),
        ("scalar descent no projection", mutate(("base_field_route_cut", "live_counterexample_reduction", "quartic_violation_implies_base_boundary_violation"), False)),
        ("scalar descent nonbase b", mutate(("base_field_route_cut", "live_counterexample_reduction", "projected_b_coefficients_in_base_field"), False)),
        ("scalar descent false payment", mutate(("base_field_route_cut", "live_counterexample_reduction", "scalar_descent_is_ledger_payment"), True)),
        ("V1 prefix identity", mutate(("v_equals_1_route_cut", "exact_identity"), "#X_S(1)=0")),
        ("V1 source floor", mutate(("v_equals_1_route_cut", "deployed_source_companion_floor"), 6_796_403)),
        ("V1 toy prefix", mutate(("v_equals_1_route_cut", "toy_nonextremality", "maximum_V_equals_1_companions"), 3)),
        ("V1 toy arbitrary", mutate(("v_equals_1_route_cut", "toy_nonextremality", "arbitrary_V_companions"), 2)),
        ("V1 false extremality", mutate(("v_equals_1_route_cut", "toy_nonextremality", "arbitrary_V_beats_global_V_equals_1"), False)),
        ("V1 false reduction", mutate(("v_equals_1_route_cut", "general_reduction_to_V_equals_1"), True)),
        ("V1 false payment", mutate(("v_equals_1_route_cut", "ledger_payment"), True)),
        ("Chebyshev family exponent", mutate(("chebyshev_support_countermodel", "binary_gilbert", "family_size_strict_lower"), "2^576446")),
        ("Chebyshev shell exponent", mutate(("chebyshev_support_countermodel", "binary_gilbert", "fixed_nonzero_weight_shell_strict_lower"), "2^576426")),
        ("Chebyshev T2 count", mutate(("chebyshev_support_countermodel", "chebyshev_support_model", "full_T2_count"), W + 1)),
        ("Chebyshev full T4", mutate(("chebyshev_support_countermodel", "chebyshev_support_model", "full_T4_count"), 1)),
        ("Chebyshev false list", mutate(("chebyshev_support_countermodel", "scope_guards", "same_received_word_RS_list"), True)),
        ("Chebyshev false common V", mutate(("chebyshev_support_countermodel", "scope_guards", "common_V_realized"), True)),
        ("Chebyshev false polynomials", mutate(("chebyshev_support_countermodel", "scope_guards", "polynomial_G_b_realized"), True)),
        ("Chebyshev independent gate", mutate(("chebyshev_support_countermodel", "independent_exact_replay", "rational_volume_gate"), False)),
        ("Singleton n-23", mutate(("singleton_packing", "cap_at_n_minus_23"), 8_389_621)),
        ("Singleton n-24", mutate(("singleton_packing", "cap_at_n_minus_24"), BUDGET)),
        ("Singleton max agreement", mutate(("singleton_packing", "maximum_nonanchor_agreement"), 2_029_705)),
        ("Singleton false close", mutate(("singleton_packing", "closes_boundary_census"), True)),
        ("residual mass", mutate(("residual_localization", "any_forbidden_boundary_census_contains_at_least"), SHALLOW_NONANCHOR_LOWER - 1)),
        ("residual slack range", mutate(("residual_localization", "shallow_excess_range", 1), 366_887)),
        ("residual no common V", mutate(("residual_localization", "common_V_required"), False)),
        ("residual frozen locator", mutate(("residual_localization", "full_locator_census"), False)),
        ("residual claims distinct G", mutate(("residual_localization", "multiple_distinct_G_not_proved"), False)),
        ("residual false theorem", mutate(("residual_localization", "remaining_exact_census_proved"), True)),
        ("residual safe terminal", mutate(("residual_localization", "terminal"), "PAID")),
        ("residual loses universal anchor scope", mutate(("residual_localization", "anchor_coordinate_field_scope"), "F_p_ONLY")),
        ("residual wrong live field", mutate(("residual_localization", "live_sufficient_counterexample_field"), "F_(p^4)")),
        ("residual nonbase coefficients", mutate(("residual_localization", "live_sufficient_pair_coefficients"), "V_AND_b_IN_F_(p^4)[X]")),
        ("residual no scalar implication", mutate(("residual_localization", "quartic_violation_implies_base_field_boundary_violation"), False)),
        ("residual scalar payment", mutate(("residual_localization", "scalar_descent_is_ledger_payment"), True)),
        ("residual scalar margin", mutate(("residual_localization", "scalar_descent_strict_margin"), 1)),
        ("false list proof", mutate(("nonclaims", "complete_M31_list_bound_proved"), True)),
        ("false coefficient theorem", mutate(("nonclaims", "coefficient_incidence_bound_proved"), True)),
        ("false locator distinctness", mutate(("nonclaims", "locators_are_proved_distinct"), True)),
        ("false support closure", mutate(("nonclaims", "pairwise_support_bounds_close_global_census"), True)),
        ("false payment nonclaim", mutate(("nonclaims", "deep_cut_is_a_v4_atom_payment"), True)),
        ("ledger movement", mutate(("ledger_state", "movement_from_this_packet"), 1)),
        ("official movement", mutate(("ledger_state", "official_endpoint_or_score_movement"), 1)),
        ("ledger deep payment", mutate(("ledger_state", "deep_cut_is_direct_diagnostic_not_payment"), False)),
        ("ledger UQ zero", mutate(("ledger_state", "atoms", 1, "value"), 0)),
        ("ledger false closure", mutate(("ledger_state", "row_closed"), True)),
        ("parent anchor pin", mutate(("dependency_contract", "anchor_exchange_parent", "payload_sha256"), "0" * 64)),
        ("parent compiler pin", mutate(("dependency_contract", "global_compiler_parent", "payload_sha256"), "0" * 64)),
        ("source adapter pin", mutate(("dependency_contract", "source_adapter_parent", "payload_sha256"), "0" * 64)),
        ("partition digest", mutate(("dependency_contract", "partition_sha256"), "0" * 64)),
        ("unstack dependency", mutate(("dependency_contract", "stacked_dependency"), False)),
        ("shared replay implementation", mutate(("dependency_contract", "exact_replays", "share_implementation_code"), True)),
        ("no subprocess replay", mutate(("dependency_contract", "exact_replays", "subprocess_replayed_by_packet"), False)),
        ("primary replay hash", mutate(("dependency_contract", "exact_replays", "primary_summary_sha256"), "0" * 64)),
        ("independent replay hash", mutate(("dependency_contract", "exact_replays", "independent_summary_sha256"), "0" * 64)),
        ("scalar replay hash", mutate(("dependency_contract", "exact_replays", "scalar_descent_output_sha256"), "0" * 64)),
        ("prefix replay hash", mutate(("dependency_contract", "exact_replays", "prefix_counterexample_output_sha256"), "0" * 64)),
        ("fixed source replay hash", mutate(("dependency_contract", "exact_replays", "fixed_remainder_output_sha256"), "0" * 64)),
        ("source hash", mutate(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source traversal", mutate(("source_bindings", 0, "path"), "../schema.json")),
        ("source pin", mutate(("source_bindings", 6, "internal_payload_sha256"), "0" * 64)),
        ("delete source binding", delete_binding),
        ("duplicate source binding", duplicate_binding),
    ]

    require(len(mutations) >= 50, "at least fifty hostile mutations")
    rejected = 0
    for label, operation in mutations:
        candidate = operation(expected)
        try:
            validate(candidate, expected)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")

    malformed = (
        b'{"a":1,"a":2}',
        b'{"a":1.5}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b'[1,2,3]',
        "{\"\u00e9\":1}".encode("utf-8"),
    )
    for raw in malformed:
        try:
            strict_decode(raw, canonical=False)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("malformed JSON accepted")
    require(rejected == len(mutations) + len(malformed), "all mutations rejected")
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
        print(f"M31 boundary common-V cross-G packet mutations: {count}/{count} rejected PASS")
        return

    actual = strict_load(args.manifest)
    validate(actual, expected)
    print("M31 boundary common-V cross-G route-cut packet v1: PASS")
    print("fixed-G endpoints and pairwise Wronskian: exact route cuts PASS")
    print("whole-list deep cut: 1001282; shallow residual: 15775933 PASS")
    print("support/base-field/Singleton interfaces: insufficient without common-V cross-G incidence PASS")
    print("v4 ledger movement: 0; M31 LIST row: OPEN")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
