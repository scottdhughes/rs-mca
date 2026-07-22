#!/usr/bin/env python3
"""Verify the source-bound M31 Grande Finale v4 LIST global compiler.

The verifier migrates the live machine contract to five codeword-valued LIST
atoms, binds the integrated source/route-cut graph, recomputes the exact
signed occupancy target, and proves the boundary-only insufficiency
countermodel at the compiler level.  It fails closed: four atoms remain null
and it never reports row closure.

All assertions remain active under ``python -O``.  ``--print-template`` emits
canonical JSON to stdout; this script never writes the certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-m31-list-v4-global-completion-compiler-v2"
COMPILER_ID = "M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V2"
SOURCE_ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
ARCHITECTURE_ID = SOURCE_ARCHITECTURE_ID
ARTIFACT_KIND = "EXACT_SOURCE_BOUND_COMPLETION_COMPILER_AND_ROUTE_CUT"
SOURCE_PARTITION_SHA256 = "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"
STATUS = "PROVED_V4_GLOBAL_COMPLETION_CONTRACT_CURRENT_INPUTS_ROUTE_CUT_ROW_OPEN"
TERMINAL = "CURRENT_ARTIFACT_SET_ROUTE_CUT_CROSS_WEIGHT_THEOREM_REQUIRED"
GLOBAL_RESIDUAL = "UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER"
BOUNDARY_HEAVY = "UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP"
BOUNDARY_DISPERSED = "UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE"
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
QUANTIFIER = "UNIFORM_OVER_ALL_RECEIVED_WORDS"
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")

P = 2**31 - 1
Q = P**4
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
SHIFT = AGREEMENT - K
BUDGET = Q // 2**100
FORBIDDEN = BUDGET + 1

J0 = 614_160
LOW_CAP = 3_730
FREE_BASELINE = 45
HIGH_LAYERS = RADIUS - J0
INTERIOR_HIGH_LAYERS = HIGH_LAYERS - 1
HIGH_BASELINE = FREE_BASELINE * HIGH_LAYERS
BASE_MASS = LOW_CAP + HIGH_BASELINE
SAFE_XI = BUDGET - BASE_MASS
FORBIDDEN_XI = FORBIDDEN - BASE_MASS
HIGH_ALLOWANCE = BUDGET - LOW_CAP

BOUNDARY_FREE_EXTRA = FORBIDDEN - LOW_CAP - FREE_BASELINE * INTERIOR_HIGH_LAYERS
BOUNDARY_FREE_CREDITS = FREE_BASELINE
BOUNDARY_FREE_XI = BOUNDARY_FREE_EXTRA - BOUNDARY_FREE_CREDITS
SAFE_46_END = J0 + SAFE_XI + BOUNDARY_FREE_CREDITS
FORBIDDEN_46_END = SAFE_46_END + 1

IDENTITY_PREFIX_BOUNDARY_FLOOR = 1_993_678
IDENTITY_PREFIX_T46_FLOOR = IDENTITY_PREFIX_BOUNDARY_FLOOR - FREE_BASELINE
IDENTITY_PREFIX_MARGIN = IDENTITY_PREFIX_T46_FLOOR - SAFE_XI
EXPECTED_TRANSITIVE_SOURCE_BINDINGS = 172
EXPECTED_INTERNAL_PAYLOAD_PINS = 29

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_list_v4_global_completion_compiler_v2.schema.json"
VERIFIER_PATH = ROOT / "experimental/scripts/verify_m31_list_v4_global_completion_compiler.py"
INDEPENDENT_PATH = ROOT / "experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_list_v4_global_completion_compiler.md"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json"

SOURCE_ADAPTER = ROOT / "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json"
HISTORICAL_COMPILER = ROOT / "experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json"
GRANDE_FINALE = ROOT / "experimental/grande_finale.tex"


SOURCE_GRAPH = (
    (
        "global_source_adapter",
        "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json",
        "21b213e2b3dfc7f8f99049aea44542ce5ae06dd59b62c10555f9faf5aaa882ce",
        "OPEN_ROUTE_CUT_UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL",
        "UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL",
        3_730,
    ),
    (
        "canonical_masked_pade",
        "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json",
        "b23186b09c7017fc80e836b70eea042077a30db22706763d33a98c053a44b0c3",
        "PROVED_DEPLOYED_SYMBOLIC_BRIDGE_TOY_COALESCENCE_ROUTE_CUT_ROW_OPEN",
        "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
        0,
    ),
    (
        "full_span_forced_collision",
        "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json",
        "5b139aaea139cc0d0440927d7df04e267b6e13a1775dc48c79acb1abc8bbc5d3",
        "PROVED_ANNIHILATOR_CRITERION_EXACT_FULL_SPAN_ROUTE_CUT_ROW_OPEN",
        GLOBAL_RESIDUAL,
        0,
    ),
    (
        "fixed_remainder_boundary_source",
        "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json",
        "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7",
        "PROVED_FIXED_REMAINDER_EXACT_C1_BOUNDARY_SOURCE_RAW_ROUTE_CUT_ROW_OPEN",
        "M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL",
        0,
    ),
    (
        "boundary_occupancy_30carrier",
        "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json",
        "c312bd2c108634af51cd351a004cdb2942bc10a145eca3e49dbcfe8fe8873a7c",
        "PROVED_BOUNDARY_OCCUPANCY_ATLAS_AND_30CARRIER_REDUCTION_ROW_OPEN",
        "M31_C2048_BIDEEP_30COLUMN_OWNER",
        0,
    ),
    (
        "boundary_multiprefix_activation",
        "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json",
        "dacb9136f5818a5f86d9ca8987fbe4d361a57a70ebb490eac50dfc3822e062e4",
        "PROVED_MULTIPREFIX_ROUTE_CUT_AND_30CARRIER_ACTIVATION_ROW_OPEN",
        "M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER",
        0,
    ),
    (
        "boundary_65column_route_cut",
        "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json",
        "1474cf06d7a058a010462ca06758df0576de9464441fa9245ddaf1b8e7d23245",
        "PROVED_65COLUMN_FIXED_ANCHOR_AND_COLLISION_ROUTE_CUT_ROW_OPEN",
        "M31_C2048_65COLUMN_FIXED_ANCHOR_OWNER",
        0,
    ),
    (
        "fixed_template_interleaved_quotient",
        "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json",
        "99febb07f517aac958e55eeba466e268a4ada793ef7960a189374603ea4a3ec9",
        "PROVED_FIXED_TEMPLATE_BOUND_AND_TARGET_ROUTE_CUT_GLOBAL_SUM_OPEN",
        "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER",
        0,
    ),
    (
        "fixed_template_module_rank",
        "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json",
        "c164f24810e0ed5015b3e538607e8867c7f634d5797de645c455447a08aaa303",
        "PROVED_FIXED_TEMPLATE_MODULE_RANK_DICHOTOMY_GLOBAL_OWNERS_OPEN",
        BOUNDARY_HEAVY,
        0,
    ),
    (
        "guarded_support_flat_separator",
        "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json",
        "d0aa51bd3811ad5e93269f7174afc249fc2865715cb484e41cd233bcab775960",
        "PROVED_EXACT_GLOBAL_SEPARATOR_INTERFACE_VT_OPEN",
        "UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER",
        0,
    ),
    (
        "vt_multitemplate_global_rank",
        "experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1/manifest.json",
        "34fe14e21ebcb7a3932cc44e73d19c7f39a154fcb7581821c538ab2c751bc1d8",
        "PROVED_GLOBAL_STRATIFICATION_BOTH_BRANCHES_UNPAID",
        BOUNDARY_DISPERSED,
        0,
    ),
)

TERMINAL_PATHS = {
    "global_source_adapter": ("closure_state", "unpaid_global_residual", "terminal"),
    "canonical_masked_pade": ("route_cut", "deployed_terminal"),
    "full_span_forced_collision": ("deployed_context", "successor_terminal"),
    "fixed_remainder_boundary_source": ("chronology_specialization", "route_terminal"),
    "boundary_occupancy_30carrier": ("carrier_reduction", "route_terminal"),
    "boundary_multiprefix_activation": ("chronology", "boundary_diagnostic_subterminal"),
    "boundary_65column_route_cut": ("chronology", "successor_terminal"),
    "fixed_template_interleaved_quotient": ("chronology", "successor_terminal"),
    "fixed_template_module_rank": ("chronology", "nested_diagnostic_subterminal"),
    "guarded_support_flat_separator": ("chronology", "boundary_subterminal"),
    "vt_multitemplate_global_rank": ("chronology", "diagnostic"),
}


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


def legacy_payload_sha256(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


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


def strict_load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 64 * 1024 * 1024, f"file size: {path}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII JSON: {path}") from exc
    value = json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON object: {path}")
    if canonical:
        require(raw == canonical_json(value), f"canonical bytes: {path}")
    return value


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
    require(value.isascii(), "source path ASCII")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), "source path relative")
    require(".." not in pure.parts and "." not in pure.parts, "source path canonical")
    resolved = ROOT.joinpath(*pure.parts)
    require(resolved.exists() and resolved.is_file(), f"source exists: {value}")
    require(not resolved.is_symlink(), f"source not symlink: {value}")
    require(resolved.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return resolved


def strict_decimal(value: Any, *, max_digits: int = 256) -> int:
    require(type(value) is str and value.isascii(), "decimal ASCII string")
    require(1 <= len(value) <= max_digits, "decimal length")
    require(all("0" <= char <= "9" for char in value), "decimal digits")
    require(value == "0" or value[0] != "0", "decimal no leading zero")
    return int(value)


def source_binding(path: str, role: str) -> dict[str, Any]:
    resolved = canonical_repo_path(path)
    return {"path": path, "role": role, "sha256": sha256_path(resolved)}


def nested_values(value: Any, key: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key == key:
                found.append(child)
            found.extend(nested_values(child, key))
    elif isinstance(value, list):
        for child in value:
            found.extend(nested_values(child, key))
    return found


def at_path(value: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = value
    for key in path:
        require(type(current) is dict and key in current, f"source terminal path: {'.'.join(path)}")
        current = current[key]
    return current


def verify_embedded_source_bindings(data: dict[str, Any], *, role: str) -> tuple[int, int]:
    bindings = data.get("source_bindings")
    require(type(bindings) is list and len(bindings) > 0, f"{role}: source bindings")
    internal_pin_count = 0
    for index, binding in enumerate(bindings):
        require(type(binding) is dict, f"{role}: binding object {index}")
        require(type(binding.get("path")) is str, f"{role}: binding path {index}")
        path = canonical_repo_path(binding["path"])
        require(binding.get("sha256") == sha256_path(path), f"{role}: fresh source {index}")
        internal = binding.get("internal_payload_sha256")
        if internal is not None:
            internal_pin_count += 1
            require(type(internal) is str and len(internal) == 64, f"{role}: internal pin type {index}")
            source = strict_load(path, canonical=False)
            require(source.get("payload_sha256") == internal or source.get("certificate_sha256") == internal, f"{role}: internal payload pin {index}")
    return len(bindings), internal_pin_count


def verify_predecessors() -> tuple[list[dict[str, Any]], int, int]:
    rows: list[dict[str, Any]] = []
    transitive_source_bindings = 0
    internal_payload_pins = 0
    for role, path_text, expected_payload, expected_status, terminal, movement in SOURCE_GRAPH:
        path = canonical_repo_path(path_text)
        data = strict_load(path)
        require(data.get("payload_sha256") == expected_payload, f"{role}: payload pin")
        require(payload_sha256(data) == expected_payload, f"{role}: payload seal")
        require(data.get("status") == expected_status, f"{role}: status")
        require(at_path(data, TERMINAL_PATHS[role]) == terminal, f"{role}: terminal")
        binding_count, internal_pin_count = verify_embedded_source_bindings(data, role=role)
        transitive_source_bindings += binding_count
        internal_payload_pins += internal_pin_count
        movements = nested_values(data, "ledger_movement") + nested_values(data, "high_residual_payment_movement")
        if movement == 0 and movements:
            require(all(value == 0 for value in movements), f"{role}: zero movement")
        rows.append(
            {
                "bankable": movement > 0,
                "import_mode": "SOURCE_CONTRACT_AND_LOW_PAYMENT" if movement > 0 else "ROUTE_CUT_ONLY",
                "internal_payload_pin_count": internal_pin_count,
                "ledger_movement": movement,
                "path": path_text,
                "payload_sha256": expected_payload,
                "role": role,
                "status": expected_status,
                "source_binding_count": binding_count,
                "terminal_or_scope": terminal,
            }
        )
    require(transitive_source_bindings == EXPECTED_TRANSITIVE_SOURCE_BINDINGS, "transitive source binding census")
    require(internal_payload_pins == EXPECTED_INTERNAL_PAYLOAD_PINS, "internal payload pin census")
    return rows, transitive_source_bindings, internal_payload_pins


def verify_source_adapter() -> dict[str, Any]:
    data = strict_load(SOURCE_ADAPTER)
    require(data["architecture_id"] == SOURCE_ARCHITECTURE_ID, "source architecture")
    require(data["partition"]["partition_sha256"] == SOURCE_PARTITION_SHA256, "source partition digest")
    require(data["partition"]["atom_order"] == list(ATOM_ORDER), "source atom order")
    require(data["partition"]["unit"] == UNIT, "source unit")
    require(data["partition"]["quantifier"] == QUANTIFIER, "source quantifier")
    atoms = data["atoms"]
    require([row["atom_id"] for row in atoms] == list(ATOM_ORDER), "source atom rows")
    require(atoms[0]["value"] == LOW_CAP and atoms[0]["bankable"] is True, "banked low cap")
    require(all(row["value"] is None and row["bankable"] is False for row in atoms[1:]), "four null atoms")
    require(data["closure_state"]["known_sum"] == LOW_CAP, "source known sum")
    require(data["closure_state"]["row_closed"] is False, "source row open")
    require(data["source_universe"]["occupancy_identity"]["safe_signed_occupancy_max"] == SAFE_XI, "source Xi cap")
    return data


def verify_historical_mismatch() -> dict[str, Any]:
    old = strict_load(HISTORICAL_COMPILER, canonical=False)
    row = next(item for item in old["rows"] if item["row_id"] == "m31_list")
    ledger = old["active_ledger_contract"]
    require(old["payload_sha256"] == "8e1811e91f2b58f2c7497e419047c3e260ef20cdcfef448dc8df0109704797b0", "old payload")
    require(legacy_payload_sha256(old) == old["payload_sha256"], "old payload seal")
    require(row["active_architecture_id"] == "GRANDE_FINALE_V3_EXACT_COMPLETION", "old v3 architecture")
    require(row["active_completion"]["required_atoms"] == ["U_paid", "U_Q", "U_list_int", "U_new"], "old four atoms")
    require(ledger["LIST"] == "U_total=U_paid+U_Q+U_list_int+U_new", "old four-atom formula")
    require(ledger["unit"] == "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE", "old slope unit")
    require(ledger["quantifier"] == "UNIFORM_OVER_ALL_ADMISSIBLE_RECEIVED_LINES", "old line quantifier")
    require("UNPAID_EXTENSION_SUBCELLS" in row["active_completion"]["unresolved_cells"], "old missing extension atom")
    pinned = old["source_bindings"]["experimental/grande_finale.tex"]
    current = sha256_path(GRANDE_FINALE)
    require(pinned == "f419d3307bf0292c855a9cb5602ea55d101a9c20bdb88f5af8bcbca56a8be986", "old spine pin")
    require(current == "34618918de8fc1c1aac5642393f49019c60ff7041a9efeacbf0b8ea01eb3d8cd", "current spine hash")
    require(pinned != current, "historical pin stale")
    return {
        "active_authority": False,
        "architecture_id": row["active_architecture_id"],
        "current_spine_sha256": current,
        "failure_mode": "V3_FOUR_ATOM_SLOPE_UNIT_CONTRACT_AND_STALE_ACTIVE_SPINE_PIN",
        "historical_spine_sha256": pinned,
        "legacy_LIST_formula": ledger["LIST"],
        "legacy_payload_sha256": old["payload_sha256"],
        "legacy_quantifier": ledger["quantifier"],
        "legacy_unit": ledger["unit"],
        "path": "experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json",
        "required_atoms": row["active_completion"]["required_atoms"],
        "superseded_as_live_authority_not_refuted": True,
    }


def arithmetic() -> None:
    require(P == 2_147_483_647, "p")
    require(N == 2_097_152 and K == 1_048_576, "n K")
    require(RADIUS == 981_129 and SHIFT == 67_447, "R w")
    require(BUDGET == 16_777_215 and FORBIDDEN == 16_777_216, "budget")
    require(HIGH_LAYERS == 366_969 and INTERIOR_HIGH_LAYERS == 366_968, "layer counts")
    require(HIGH_BASELINE == 16_513_605, "high baseline")
    require(BASE_MASS == 16_517_335, "base mass")
    require(SAFE_XI == 259_880 and FORBIDDEN_XI == 259_881, "Xi thresholds")
    require(HIGH_ALLOWANCE == 16_773_485, "high allowance")
    require(BOUNDARY_FREE_EXTRA == 259_926, "boundary-free extra")
    require(BOUNDARY_FREE_XI == FORBIDDEN_XI, "boundary-free Xi")
    require(SAFE_46_END == 874_085 and FORBIDDEN_46_END == 874_086, "RLE endpoints")
    require(LOW_CAP + FREE_BASELINE * INTERIOR_HIGH_LAYERS + BOUNDARY_FREE_EXTRA == FORBIDDEN, "boundary-free total")
    require(IDENTITY_PREFIX_T46_FLOOR == 1_993_633, "identity T46")
    require(IDENTITY_PREFIX_MARGIN == 1_733_753, "identity raw margin")


def occupancy_fixture(*, forbidden: bool) -> dict[str, Any]:
    end_46 = FORBIDDEN_46_END if forbidden else SAFE_46_END
    start_45 = end_46 + 1
    count_46 = end_46 - (J0 + 1) + 1
    count_45 = (RADIUS - 1) - start_45 + 1
    total = LOW_CAP + 46 * count_46 + 45 * count_45
    t46 = count_46
    credit_sum = FREE_BASELINE
    xi46 = t46 - credit_sum
    return {
        "boundary_multiplicity": 0,
        "boundary_weight": RADIUS,
        "compiler_countermodel_only": True,
        "credits_C_low": 0,
        "credits_C_r_sum": credit_sum,
        "H_1_through_45": INTERIOR_HIGH_LAYERS,
        "H_46": count_46,
        "received_word_constructed": False,
        "source_realized": False,
        "T46": t46,
        "total_mass": total,
        "weight_blocks": [
            {"end": J0, "multiplicity": LOW_CAP, "start": J0},
            {"end": end_46, "multiplicity": 46, "start": J0 + 1},
            {"end": RADIUS - 1, "multiplicity": 45, "start": start_45},
            {"end": RADIUS, "multiplicity": 0, "start": RADIUS},
        ],
        "Xi46": xi46,
    }


def verify_occupancy_fixture(fixture: dict[str, Any], *, forbidden: bool) -> None:
    blocks = fixture["weight_blocks"]
    require(len(blocks) == 4, "fixture four maximal blocks")
    require(blocks[0]["start"] == J0 and blocks[-1]["end"] == RADIUS, "fixture support range")
    previous_end = J0 - 1
    previous_multiplicity: int | None = None
    n_low = 0
    total = 0
    t46 = 0
    high_counts = [0] * (FREE_BASELINE + 1)
    for index, block in enumerate(blocks):
        start = block["start"]
        end = block["end"]
        multiplicity = block["multiplicity"]
        require(type(start) is int and type(end) is int and type(multiplicity) is int, "fixture integer block")
        require(start == previous_end + 1 and start <= end, "fixture contiguous blocks")
        require(previous_multiplicity is None or multiplicity != previous_multiplicity, "fixture maximal RLE")
        width = end - start + 1
        if multiplicity == 0:
            require(index == len(blocks) - 1 and start == end == RADIUS, "only boundary singleton may be zero")
        else:
            require(multiplicity > 0, "fixture nonnegative multiplicity")
        if start <= J0:
            require(end <= J0, "fixture cutoff aligned")
            n_low += width * multiplicity
        else:
            t46 += width * max(0, multiplicity - FREE_BASELINE)
            for level in range(1, FREE_BASELINE + 1):
                if multiplicity >= level:
                    high_counts[level] += width
        total += width * multiplicity
        previous_end = end
        previous_multiplicity = multiplicity

    c_low = LOW_CAP - n_low
    c_levels = sum(HIGH_LAYERS - high_counts[level] for level in range(1, FREE_BASELINE + 1))
    xi46 = t46 - c_low - c_levels
    expected_total = FORBIDDEN if forbidden else BUDGET
    expected_xi = FORBIDDEN_XI if forbidden else SAFE_XI
    expected_t46 = 259_926 if forbidden else 259_925
    require(n_low == LOW_CAP and c_low == 0, "fixture low cap")
    require(high_counts[1:] == [INTERIOR_HIGH_LAYERS] * FREE_BASELINE, "fixture missing boundary credits")
    require(c_levels == FREE_BASELINE, "fixture level credits")
    require(t46 == expected_t46 and xi46 == expected_xi, "fixture signed occupancy")
    require(total == expected_total, "fixture total")
    require(fixture["boundary_multiplicity"] == 0, "fixture boundary empty")
    require(fixture["source_realized"] is False and fixture["received_word_constructed"] is False, "fixture nonrealization")
    require(fixture == occupancy_fixture(forbidden=forbidden), "fixture exact contract")


def build_template() -> dict[str, Any]:
    arithmetic()
    source = verify_source_adapter()
    graph, transitive_source_bindings, internal_payload_pins = verify_predecessors()
    historical = verify_historical_mismatch()

    bindings = [
        source_binding("experimental/grande_finale.tex", "v4_five_atom_ledger"),
        source_binding("experimental/notes/thresholds/m31_list_v4_global_completion_compiler.md", "compiler_note"),
        source_binding("experimental/scripts/verify_m31_list_v4_global_completion_compiler.py", "primary_verifier"),
        source_binding("experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py", "independent_verifier"),
        source_binding("experimental/data/schemas/m31_list_v4_global_completion_compiler_v2.schema.json", "schema"),
        source_binding("experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/README.md", "certificate_readme"),
    ]
    bindings.extend(source_binding(row[1], f"predecessor::{row[0]}") for row in SOURCE_GRAPH)
    bindings.append(source_binding(historical["path"], "historical_v3_compiler"))

    atoms = []
    for atom in ATOM_ORDER:
        if atom == "U_paid":
            atoms.append(
                {
                    "atom_id": atom,
                    "bankable": True,
                    "owner_ids": ["LOW_EXACT_WEIGHT_PACKING"],
                    "status": "BANKED_SOURCE_BOUND_EXACT_UPPER",
                    "unit": UNIT,
                    "value": LOW_CAP,
                }
            )
        else:
            atoms.append(
                {
                    "atom_id": atom,
                    "bankable": False,
                    "owner_ids": [],
                    "status": "OPEN_UNPAID",
                    "unit": UNIT,
                    "value": None,
                }
            )

    payload: dict[str, Any] = {
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "atom_state": {
            "atom_order": list(ATOM_ORDER),
            "atoms": atoms,
            "available_high_allowance": HIGH_ALLOWANCE,
            "known_sum": LOW_CAP,
            "null_atoms": list(ATOM_ORDER[1:]),
            "row_closed": False,
        },
        "boundary_free_extremizers": {
            "consequence": "BOUNDARY_ONLY_HYPOTHESES_CANNOT_CLOSE_CURRENT_GLOBAL_COMPILER",
            "first_forbidden": occupancy_fixture(forbidden=True),
            "safe_sharp": occupancy_fixture(forbidden=False),
        },
        "candidate_interface": {
            "accepted_completion_modes": [
                "FIVE_EXACT_NONNEGATIVE_SOURCE_PARTITION_ATOMS",
                "DIRECT_SIGNED_HISTOGRAM_BOUND",
            ],
            "additive_mode_requires_all_five_atoms_nonnull": True,
            "direct_mode_does_not_fabricate_atom_values": True,
            "direct_mode_target": "Xi46<=259880",
            "exact_partition_digest_required": SOURCE_PARTITION_SHA256,
            "negative_refund_atom_interface_available": False,
            "quantifier_required": QUANTIFIER,
            "residual_empty_required": True,
            "unit_required": UNIT,
        },
        "closure_contract": {
            "complete_list_upper_required": BUDGET,
            "exact_equivalence": "list_mass=3730+45*(R-J0)+Xi46",
            "exact_signed_expression": "Xi46=T46_interior+T46_boundary-C_low-sum_{r=1}^{45}C_r",
            "forbidden_Xi46_lower": FORBIDDEN_XI,
            "global_residual": GLOBAL_RESIDUAL,
            "no_unresolved_cells_required": True,
            "signed_Xi46_upper_required": SAFE_XI,
            "signed_comparator": "<=",
            "sufficient_high_mass_upper_with_low_cap": HIGH_ALLOWANCE,
            "T46_decomposition_required": True,
            "raw_T46_upper_259880_required": False,
            "terminal": TERMINAL,
        },
        "current_artifact_graph": graph,
        "compiler_id": COMPILER_ID,
        "historical_compiler": historical,
        "identity_prefix_raw_tail_cut": {
            "actual_deployed_source": True,
            "boundary_layer_floor": IDENTITY_PREFIX_BOUNDARY_FLOOR,
            "complete_list_budget_status": "UNKNOWN",
            "raw_T46_cap_259880_false": True,
            "T46_floor": IDENTITY_PREFIX_T46_FLOOR,
            "T46_margin_over_signed_allowance": IDENTITY_PREFIX_MARGIN,
            "signed_credits_required": True,
        },
        "open_pr_admissibility": {
            "proof_dependency": False,
            "pr_1047": {
                "admissible_payment": False,
                "head_at_audit": "0e735999acf24a7779b2271553deb26207396cda",
                "reason": "SLOPES_PER_RECEIVED_LINE_WITHOUT_UNIFORM_CODEWORD_PROJECTION_OR_ADDBACK",
                "role": "INFORMATIVE_LOCAL_THEOREM_ONLY",
            },
            "pr_1048": {
                "admissible_payment": False,
                "head_at_audit": "6487b234334e4c6d601732b2b587cde2c7bc342d",
                "reason": "EXISTENTIAL_PINNED_SUPPORT_COUNTEREXAMPLE_WITHOUT_RECEIVED_WORD_OR_OWNER_PROJECTION",
                "role": "ROUTE_CUT_INTERCEPTS_3_TO_5_REJECTED_INTERCEPT_6_UNPROVED",
            },
            "pr_1051": {
                "admissible_payment": False,
                "head_at_audit": "0b339ebb0c92c1e7703c1e765f0ad9f819c3b9f7",
                "prior_formula_artifact": "experimental/scripts/verify_quotient_cell_prefix_fiber_floor.py",
                "reason": "DIFFERENT_N_K_AGREEMENT_AND_MULTIPLICATIVE_COSET_DOMAIN_EXISTENTIAL_LOWER_CONSTRUCTION",
                "role": "SELF_CONTAINED_PROMOTION_AND_HARDENING_OF_PRIOR_LOWER_FLOOR_NOT_M31_PAYMENT",
            },
        },
        "partition": {
            "atom_order": list(ATOM_ORDER),
            "owner_order": source["partition"]["owner_order"],
            "partition_sha256": SOURCE_PARTITION_SHA256,
            "quantifier": QUANTIFIER,
            "source_architecture_id": SOURCE_ARCHITECTURE_ID,
            "source_manifest_sha256": sha256_path(SOURCE_ADAPTER),
            "source_payload_sha256": source["payload_sha256"],
            "source_codeword_partition_exhaustive": True,
            "unit": UNIT,
        },
        "payload_sha256": "",
        "row_contract": {
            "B_star": BUDGET,
            "K": K,
            "agreement": AGREEMENT,
            "base_prime": P,
            "code_field_cardinality": str(Q),
            "n": N,
            "object": "LIST",
            "quantifier": QUANTIFIER,
            "radius": RADIUS,
            "shift": SHIFT,
            "target_epsilon": "2^-100",
            "unit": UNIT,
        },
        "schema": SCHEMA_ID,
        "scope_guards": {
            "arithmetic_extremizer_source_realized": False,
            "boundary_histogram_is_received_word": False,
            "boundary_only_closure_sufficient": False,
            "boundary_support_is_automatically_U_Q": False,
            "five_atom_additive_ledger_complete": False,
            "high_residual_payment_movement": 0,
            "marked_key_is_owner": False,
            "negative_refund_interface_proved": False,
            "official_row_movement": 0,
            "open_pr_1047_banked": False,
            "open_pr_1047_slope_profile_is_LIST_payment": False,
            "open_pr_1048_banked": False,
            "open_pr_1048_support_witness_is_U_Q_payment": False,
            "open_pr_1051_banked": False,
            "raw_T46_cap_claimed": False,
            "route_cut_registry_contains_payment": False,
            "scalar_descent_is_U_ext_zero": False,
            "signed_Xi46_bound_proved": False,
            "stable_paper_modified": False,
        },
        "source_graph_freshness": {
            "direct_predecessor_count": len(SOURCE_GRAPH),
            "every_embedded_path_and_sha256_fresh": True,
            "internal_payload_pins_checked_when_present": True,
            "internal_payload_pin_count": internal_payload_pins,
            "transitive_source_binding_count": transitive_source_bindings,
        },
        "source_bindings": bindings,
        "status": STATUS,
        "unpaid_boundary_branches": [BOUNDARY_HEAVY, BOUNDARY_DISPERSED],
    }
    return seal(payload)


def validate_schema() -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft")
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("additionalProperties") is False, "schema top closed")


def validate(payload: dict[str, Any]) -> None:
    arithmetic()
    require(payload.get("schema") == SCHEMA_ID, "schema")
    require(payload.get("compiler_id") == COMPILER_ID, "compiler")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "architecture")
    require(payload.get("status") == STATUS, "status")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")
    require(strict_decimal(payload["row_contract"]["code_field_cardinality"]) == Q, "field cardinality")
    require(payload["partition"]["partition_sha256"] == SOURCE_PARTITION_SHA256, "partition")
    require(payload["partition"]["atom_order"] == list(ATOM_ORDER), "atom order")
    require(payload["partition"]["unit"] == UNIT, "unit")
    require(payload["partition"]["quantifier"] == QUANTIFIER, "quantifier")
    require(payload["partition"]["source_manifest_sha256"] == sha256_path(SOURCE_ADAPTER), "adapter file hash")
    require(payload["partition"]["source_payload_sha256"] == SOURCE_GRAPH[0][2], "adapter payload")
    require(payload["atom_state"]["known_sum"] == LOW_CAP, "known sum")
    require(payload["atom_state"]["null_atoms"] == list(ATOM_ORDER[1:]), "null atoms")
    require(payload["atom_state"]["row_closed"] is False, "row open")
    require(payload["closure_contract"]["signed_Xi46_upper_required"] == SAFE_XI, "Xi cap")
    require(payload["closure_contract"]["global_residual"] == GLOBAL_RESIDUAL, "global residual")
    require(payload["closure_contract"]["exact_signed_expression"] == "Xi46=T46_interior+T46_boundary-C_low-sum_{r=1}^{45}C_r", "signed expression")
    require(payload["closure_contract"]["signed_comparator"] == "<=", "signed comparator")
    require(payload["closure_contract"]["raw_T46_upper_259880_required"] is False, "raw target rejected")
    require(payload["candidate_interface"]["accepted_completion_modes"] == ["FIVE_EXACT_NONNEGATIVE_SOURCE_PARTITION_ATOMS", "DIRECT_SIGNED_HISTOGRAM_BOUND"], "completion modes")
    require(payload["candidate_interface"]["direct_mode_does_not_fabricate_atom_values"] is True, "direct mode no fake atoms")
    require(payload["candidate_interface"]["negative_refund_atom_interface_available"] is False, "no negative atom")
    verify_occupancy_fixture(payload["boundary_free_extremizers"]["safe_sharp"], forbidden=False)
    verify_occupancy_fixture(payload["boundary_free_extremizers"]["first_forbidden"], forbidden=True)
    require(payload["identity_prefix_raw_tail_cut"]["raw_T46_cap_259880_false"] is True, "raw cut")
    require(payload["identity_prefix_raw_tail_cut"]["complete_list_budget_status"] == "UNKNOWN", "identity status")
    require(payload["scope_guards"]["high_residual_payment_movement"] == 0, "zero movement")
    require(payload["scope_guards"]["official_row_movement"] == 0, "zero official movement")
    require(payload["scope_guards"]["signed_Xi46_bound_proved"] is False, "signed theorem open")
    require(payload["scope_guards"]["five_atom_additive_ledger_complete"] is False, "five atom open")
    require(payload["scope_guards"]["route_cut_registry_contains_payment"] is False, "route cuts pay zero")
    require(payload["source_graph_freshness"]["transitive_source_binding_count"] == EXPECTED_TRANSITIVE_SOURCE_BINDINGS, "freshness census")
    require(payload["source_graph_freshness"]["internal_payload_pin_count"] == EXPECTED_INTERNAL_PAYLOAD_PINS, "internal pin census")
    require(payload["open_pr_admissibility"]["proof_dependency"] is False, "open PR not proof source")
    require(payload["open_pr_admissibility"]["pr_1047"]["admissible_payment"] is False, "1047 rejected")
    require(payload["open_pr_admissibility"]["pr_1048"]["admissible_payment"] is False, "1048 rejected")
    require(payload["open_pr_admissibility"]["pr_1051"]["admissible_payment"] is False, "1051 rejected")
    require(payload["unpaid_boundary_branches"] == [BOUNDARY_HEAVY, BOUNDARY_DISPERSED], "boundary branches")
    for binding in payload["source_bindings"]:
        path = canonical_repo_path(binding["path"])
        require(binding["sha256"] == sha256_path(path), f"source hash: {binding['role']}")
    deep_exact(payload, build_template())


def mutate(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
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

    def stale_seal(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        out["row_contract"]["agreement"] -= 1
        return out

    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutate(("schema",), "rs-mca-m31-list-v4-global-completion-compiler-v1")),
        ("status", mutate(("status",), "SAFE")),
        ("unknown top property", add_unknown),
        ("stale payload seal", stale_seal),
        ("compiler", mutate(("compiler_id",), "M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V1")),
        ("artifact kind", mutate(("artifact_kind",), "THEOREM")),
        ("v3 architecture", mutate(("architecture_id",), "GRANDE_FINALE_V3_EXACT_COMPLETION")),
        ("slope unit", mutate(("row_contract", "unit"), "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE")),
        ("received line", mutate(("row_contract", "quantifier"), "UNIFORM_OVER_ALL_RECEIVED_LINES")),
        ("four atoms", mutate(("partition", "atom_order"), ["U_paid", "U_Q", "U_list_int", "U_new"])),
        ("partition digest", mutate(("partition", "partition_sha256"), "0" * 64)),
        ("owner order", mutate(("partition", "owner_order"), list(reversed(["LOW_EXACT_WEIGHT_PACKING", "HIGH_BOUNDARY_EXACT_CODEWORD", "HIGH_INTERIOR_EXACT_CODEWORD"])))),
        ("adapter file hash", mutate(("partition", "source_manifest_sha256"), "0" * 64)),
        ("adapter payload", mutate(("partition", "source_payload_sha256"), "0" * 64)),
        ("low cap", mutate(("atom_state", "known_sum"), LOW_CAP - 1)),
        ("low atom", mutate(("atom_state", "atoms", 0, "value"), LOW_CAP - 1)),
        ("U Q zero", mutate(("atom_state", "atoms", 1, "value"), 0)),
        ("U list zero", mutate(("atom_state", "atoms", 2, "value"), 0)),
        ("U ext zero", mutate(("atom_state", "atoms", 3, "value"), 0)),
        ("U new zero", mutate(("atom_state", "atoms", 4, "value"), 0)),
        ("row closed", mutate(("atom_state", "row_closed"), True)),
        ("field leading zero", mutate(("row_contract", "code_field_cardinality"), "0" + str(Q))),
        ("field unicode digit", mutate(("row_contract", "code_field_cardinality"), "١" + str(Q)[1:])),
        ("field oversized", mutate(("row_contract", "code_field_cardinality"), "9" * 257)),
        ("Xi off by one", mutate(("closure_contract", "signed_Xi46_upper_required"), SAFE_XI + 1)),
        ("forbidden Xi", mutate(("closure_contract", "forbidden_Xi46_lower"), SAFE_XI)),
        ("unsigned sufficient cap", mutate(("closure_contract", "sufficient_high_mass_upper_with_low_cap"), HIGH_ALLOWANCE + 1)),
        ("Xi comparator", mutate(("closure_contract", "signed_comparator"), "<")),
        ("Xi sign", mutate(("closure_contract", "exact_signed_expression"), "Xi46=T46_interior+T46_boundary+C_low+sum_C_r")),
        ("raw target required", mutate(("closure_contract", "raw_T46_upper_259880_required"), True)),
        ("drop direct mode", mutate(("candidate_interface", "accepted_completion_modes"), ["FIVE_EXACT_NONNEGATIVE_SOURCE_PARTITION_ATOMS"])),
        ("fabricate direct atoms", mutate(("candidate_interface", "direct_mode_does_not_fabricate_atom_values"), False)),
        ("negative refund atom", mutate(("candidate_interface", "negative_refund_atom_interface_available"), True)),
        ("safe equality", mutate(("boundary_free_extremizers", "safe_sharp", "Xi46"), SAFE_XI - 1)),
        ("safe boundary nonzero", mutate(("boundary_free_extremizers", "safe_sharp", "boundary_multiplicity"), 1)),
        ("safe endpoint", mutate(("boundary_free_extremizers", "safe_sharp", "weight_blocks", 1, "end"), SAFE_46_END - 1)),
        ("safe source witness", mutate(("boundary_free_extremizers", "safe_sharp", "source_realized"), True)),
        ("forbidden Xi", mutate(("boundary_free_extremizers", "first_forbidden", "Xi46"), SAFE_XI)),
        ("forbidden total", mutate(("boundary_free_extremizers", "first_forbidden", "total_mass"), BUDGET)),
        ("forbidden boundary", mutate(("boundary_free_extremizers", "first_forbidden", "weight_blocks", 3, "multiplicity"), 1)),
        ("forbidden credits", mutate(("boundary_free_extremizers", "first_forbidden", "credits_C_r_sum"), 44)),
        ("raw cap true", mutate(("identity_prefix_raw_tail_cut", "raw_T46_cap_259880_false"), False)),
        ("identity counterexample", mutate(("identity_prefix_raw_tail_cut", "complete_list_budget_status"), "OVER_BUDGET")),
        ("1047 payment", mutate(("scope_guards", "open_pr_1047_slope_profile_is_LIST_payment"), True)),
        ("1047 banked", mutate(("scope_guards", "open_pr_1047_banked"), True)),
        ("1047 admissible", mutate(("open_pr_admissibility", "pr_1047", "admissible_payment"), True)),
        ("1048 payment", mutate(("scope_guards", "open_pr_1048_support_witness_is_U_Q_payment"), True)),
        ("1048 banked", mutate(("scope_guards", "open_pr_1048_banked"), True)),
        ("1048 admissible", mutate(("open_pr_admissibility", "pr_1048", "admissible_payment"), True)),
        ("1051 banked", mutate(("scope_guards", "open_pr_1051_banked"), True)),
        ("1051 admissible", mutate(("open_pr_admissibility", "pr_1051", "admissible_payment"), True)),
        ("scalar Uext", mutate(("scope_guards", "scalar_descent_is_U_ext_zero"), True)),
        ("boundary auto Q", mutate(("scope_guards", "boundary_support_is_automatically_U_Q"), True)),
        ("key owner", mutate(("scope_guards", "marked_key_is_owner"), True)),
        ("ledger movement", mutate(("scope_guards", "high_residual_payment_movement"), 1)),
        ("official movement", mutate(("scope_guards", "official_row_movement"), 1)),
        ("signed theorem", mutate(("scope_guards", "signed_Xi46_bound_proved"), True)),
        ("five atoms complete", mutate(("scope_guards", "five_atom_additive_ledger_complete"), True)),
        ("route cut payment", mutate(("scope_guards", "route_cut_registry_contains_payment"), True)),
        ("global residual paid", mutate(("closure_contract", "global_residual"), "PAID")),
        ("heavy branch paid", mutate(("unpaid_boundary_branches", 0), "PAID")),
        ("dispersed branch paid", mutate(("unpaid_boundary_branches", 1), "PAID")),
        ("historical authority", mutate(("historical_compiler", "active_authority"), True)),
        ("historical formula", mutate(("historical_compiler", "legacy_LIST_formula"), "U_total=U_paid+U_Q+U_list_int+U_ext+U_new")),
        ("predecessor movement", mutate(("current_artifact_graph", 2, "ledger_movement"), 1)),
        ("source hash", mutate(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source traversal", mutate(("source_bindings", 0, "path"), "../grande_finale.tex")),
        ("transitive source census", mutate(("source_graph_freshness", "transitive_source_binding_count"), EXPECTED_TRANSITIVE_SOURCE_BINDINGS - 1)),
        ("internal pin census", mutate(("source_graph_freshness", "internal_payload_pin_count"), EXPECTED_INTERNAL_PAYLOAD_PINS - 1)),
    ]
    for index, (role, _path, _payload, _status, _terminal, movement) in enumerate(SOURCE_GRAPH):
        mutations.extend(
            [
                (f"{role} payload", mutate(("current_artifact_graph", index, "payload_sha256"), "0" * 64)),
                (f"{role} mode", mutate(("current_artifact_graph", index, "import_mode"), "PAYMENT")),
                (f"{role} movement", mutate(("current_artifact_graph", index, "ledger_movement"), movement + 1)),
                (f"{role} bankable", mutate(("current_artifact_graph", index, "bankable"), movement == 0)),
                (f"{role} source count", mutate(("current_artifact_graph", index, "source_binding_count"), 0)),
                (f"{role} internal pin count", mutate(("current_artifact_graph", index, "internal_payload_pin_count"), -1)),
            ]
        )
    rejected = 0
    for label, fn in mutations:
        candidate = fn(expected)
        try:
            validate(candidate)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    malformed = ('{"a":1,"a":2}', '{"a":1.5}', '{"a":NaN}', '{"a":Infinity}')
    for text in malformed:
        try:
            json.loads(text, object_pairs_hook=unique_object, parse_float=reject_float, parse_constant=reject_constant)
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
    validate_schema()
    expected = build_template()
    validate(expected)
    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
    if args.check:
        actual = strict_load(args.manifest)
        validate(actual)
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"M31 LIST v4 global compiler mutations: {count}/{count} rejected PASS")
    if not args.print_template:
        print("M31 LIST v4 global completion compiler v2: PASS")
        print("contract: five codeword atoms / source partition 816f0702... PASS")
        print("atoms: U_paid=3730 BANKED; U_Q/U_list_int/U_ext/U_new=null")
        print("signed target: Xi46<=259880; forbidden threshold=259881 PASS")
        print("boundary-free safe/first-forbidden sharp RLE fixtures: PASS (not received words)")
        print("raw T46<=259880: REFUTED by actual identity-prefix boundary source")
        print(f"terminal: {TERMINAL}; row OPEN; ledger movement beyond U_paid=0")
        print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
