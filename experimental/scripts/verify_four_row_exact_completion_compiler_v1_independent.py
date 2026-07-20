#!/usr/bin/env python3
"""Independent checker for the four-row exact-completion compiler.

This file deliberately does not import the generator.  It replays the row
arithmetic, effective moved endpoints, source hashes, architecture separation,
and direct-extension dimension cuts through a separate implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(2_500_000)

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/"
    "four_row_exact_completion_compiler_v1.json"
)
ACTIVE = "GRANDE_FINALE_V3_EXACT_COMPLETION"
LEGACY = "LEGACY_KB_M1_FIRST_MATCH_V2"
TERMINAL = "ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET"
SCHEMA = "rs-mca-four-row-exact-completion-compiler-v1"
ARTIFACT_KIND = "FOUR_ROW_EXACT_COMPLETION_COMPILER"
STATUS = "PROVED_EXACT_COMPILER_CURRENT_ARTIFACT_ARCHITECTURE_ROUTE_CUT_ROWS_OPEN"
BASE_COMMIT = "4106fc84b7d78d72f68a61398cd04ea260f53df4"
UNIT = "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE"

N = 2_097_152
K = 1_048_576
P_KB = 2_130_706_433
P_M31 = 2_147_483_647

ROWS = [
    ("kb_mca", "MCA", P_KB, 6, 128, K + 1, 1_116_047, 1_116_048, 67_471, 57_198_030_366, 274_980_728_111_395_087, 4_807_520, "kb_mca_v1.packet.json"),
    ("kb_list", "LIST", P_KB, 6, 128, K, 1_116_046, 1_116_047, 67_471, 65_065_153_468, 274_980_728_111_395_087, 4_226_236, "kb_list_v1.packet.json"),
    ("m31_mca", "MCA", P_M31, 4, 100, K + 1, 1_116_023, 1_116_024, 67_447, 1_752_700, 16_777_215, 9, "m31_mca_v1.packet.json"),
    ("m31_list", "LIST", P_M31, 4, 100, K, 1_116_022, 1_116_023, 67_447, 1_993_678, 16_777_215, 8, "m31_list_v1.packet.json"),
]

PACKET_DIR = ROOT / (
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/"
    "experimental/data/certificates/frontier-adjacent"
)
KB995 = ROOT / (
    "experimental/data/certificates/m1-kb-rank9-full-histogram-incidence-closure-v1/"
    "m1_kb_rank9_full_histogram_incidence_closure_v1.json"
)
EXT = ROOT / (
    "experimental/data/certificates/frontier-extension-fixed-line-audit-v1/"
    "frontier_extension_fixed_line_audit_v1.json"
)
CURRENT_DIMENSION_DEGREE = ROOT / "tex/cs25_cap_v13_2.tex"
ALLOWED_SOURCE_ROOTS = {"archived", "docs", "experimental", "site", "tex"}
EXPECTED_SOURCE_PATHS = {
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/experimental/data/certificates/frontier-adjacent/kb_list_v1.packet.json",
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/experimental/data/certificates/frontier-adjacent/kb_mca_v1.packet.json",
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json",
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json",
    "experimental/data/cap25_v13_m31_chebyshev_entropy_inverse_shells.json",
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/README.md",
    "experimental/data/certificates/frontier-extension-fixed-line-audit-v1/frontier_extension_fixed_line_audit_v1.json",
    "experimental/data/certificates/m1-kb-rank9-full-histogram-incidence-closure-v1/m1_kb_rank9_full_histogram_incidence_closure_v1.json",
    "experimental/data/certificates/upaid-ledger/upaid_ledger.json",
    "experimental/data/schemas/four_row_exact_completion_candidate_v1.schema.json",
    "experimental/grande_finale.tex",
    "experimental/lean/m31_few_shell/M31FewShell/ChebyshevPrefix.lean",
    "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md",
    "experimental/notes/frontier-adjacent/frontier_extension_fixed_line_audit_v1.md",
    "experimental/notes/m1/m1_kb_rank9_full_histogram_incidence_closure_v1.md",
    "experimental/notes/thresholds/cap25_v13_m31_chebyshev_entropy_inverse_shells.md",
    "experimental/scripts/verify_four_row_exact_completion_compiler_v1.py",
    "experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py",
    "tex/cs25_cap_v13_2.tex",
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def need(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def pairs_no_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        need(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def bad_number(token: str) -> Any:
    fail(f"forbidden JSON number: {token}")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=pairs_no_duplicate,
        parse_float=bad_number,
        parse_constant=bad_number,
    )
    need(isinstance(value, dict), f"root is not object: {path}")
    return value


def read_legacy_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=pairs_no_duplicate,
        parse_float=lambda token: token,
        parse_constant=bad_number,
    )
    need(isinstance(value, dict), f"legacy root is not object: {path}")
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload_hash(value: dict[str, Any]) -> str:
    cloned = copy.deepcopy(value)
    cloned["payload_sha256"] = ""
    return hashlib.sha256(canonical(cloned)).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_pair(packet: dict[str, Any], kind: str) -> tuple[int, int]:
    if kind == "MCA":
        moved = packet["v13_raw_moved_pair"]["new_pair"]
        return moved["a0_prime"], moved["a0_prime_plus_1"]
    one = packet["agreement_interval"]["one_step_target"]
    return one["a0"], one["a0_plus_1"]


def extension_dimension_cut(p: int, budget: int) -> tuple[int, int, int]:
    # Independent implementation via repeated exact division, not logarithms.
    dimension = 0
    quotient = budget
    while quotient >= p:
        quotient //= p
        dimension += 1
    max_delta = budget // pow(p, dimension)
    return dimension, max_delta, pow(p, dimension + 1) - budget


def recompute_binomials() -> dict[int, int]:
    targets = sorted({row[7] for row in ROWS})
    base = targets[0]
    value = math.comb(N, base)
    all_values = {base: value}
    for a in range(base + 1, targets[-1] + 1):
        value = value * (N - a + 1) // a
        if a in targets:
            all_values[a] = value
    return all_values


def check() -> None:
    cert = read_json(CERT)
    need(cert.get("schema") == SCHEMA, "schema mismatch")
    need(cert.get("artifact_kind") == ARTIFACT_KIND, "artifact kind mismatch")
    need(cert.get("status") == STATUS, "status mismatch")
    need(cert.get("payload_sha256") == payload_hash(cert), "payload self-hash mismatch")
    need(cert["stack"]["base_commit"] == BASE_COMMIT, "base commit mismatch")
    need(cert["stack"]["active_architecture_id"] == ACTIVE, "active architecture mismatch")
    need(cert["stack"]["legacy_architecture_id"] == LEGACY, "legacy architecture mismatch")
    need(cert["active_ledger_contract"]["unit"] == UNIT, "unit mismatch")

    source_bindings = cert["source_bindings"]
    need(isinstance(source_bindings, dict) and source_bindings, "source bindings missing")
    need(set(source_bindings) == EXPECTED_SOURCE_PATHS, "exact expected source-binding set mismatch")
    seen_resolved: set[Path] = set()
    seen_physical: set[tuple[int, int]] = set()
    for rel, expected_digest in source_bindings.items():
        path = Path(rel)
        need(not path.is_absolute() and rel == path.as_posix(), f"noncanonical source path: {rel}")
        need(path.parts and path.parts[0] in ALLOWED_SOURCE_ROOTS, f"source root not allowlisted: {rel}")
        need(all(part not in {"", ".", ".."} and not part.startswith(".") for part in path.parts), f"hidden/traversing source path: {rel}")
        full = ROOT / path
        need(full.is_file(), f"source missing: {rel}")
        resolved = full.resolve()
        need(resolved == full.absolute(), f"symlinked source path: {rel}")
        need(ROOT.resolve() in resolved.parents, f"source escapes repository: {rel}")
        need(resolved not in seen_resolved, f"duplicate physical source binding: {rel}")
        seen_resolved.add(resolved)
        stat = resolved.stat()
        physical_id = (stat.st_dev, stat.st_ino)
        need(physical_id not in seen_physical, f"hardlinked duplicate source binding: {rel}")
        seen_physical.add(physical_id)
        need(isinstance(expected_digest, str) and len(expected_digest) == 64 and all(ch in "0123456789abcdef" for ch in expected_digest), f"bad source digest: {rel}")
        need(file_hash(resolved) == expected_digest, f"source hash mismatch: {rel}")

    binomials = recompute_binomials()
    records = cert["rows"]
    need(len(records) == len(ROWS), "row count mismatch")
    for record, row in zip(records, ROWS):
        row_id, kind, p, ext_degree, security, prefix_K, a0, a_plus, w, avg_expected, B_expected, mult_expected, packet_name = row
        need(record["row_id"] == row_id, f"{row_id}: row id/order mismatch")
        need(record["object_kind"] == kind, f"{row_id}: kind mismatch")
        params = record["parameters"]
        need(all(type(params[key]) is int for key in ["K", "a0", "a_plus", "w", "p", "extension_degree", "security_bits"]), f"{row_id}: parameter type mismatch")
        need(
            (params["K"], params["a0"], params["a_plus"], params["w"], params["p"], params["extension_degree"], params["security_bits"])
            == (prefix_K, a0, a_plus, w, p, ext_degree, security),
            f"{row_id}: parameter mismatch",
        )
        need(a_plus - prefix_K == w, f"{row_id}: depth identity mismatch")

        packet = read_legacy_json(PACKET_DIR / packet_name)
        need(active_pair(packet, kind) == (a0, a_plus), f"{row_id}: effective packet pair mismatch")
        need(int(packet["target"]["B_star"]["value"]) == B_expected, f"{row_id}: packet B* mismatch")

        choose = binomials[a_plus]
        base_power = pow(p, w)
        average = (choose + base_power - 1) // base_power
        B_star = pow(p, ext_degree) // pow(2, security)
        multiplier = B_star * base_power // choose
        need((average, B_star, multiplier) == (avg_expected, B_expected, mult_expected), f"{row_id}: exact calibration mismatch")
        exact = record["exact_calibration"]
        need(type(exact["full_budget_Q_multiplier_floor"]) is int, f"{row_id}: multiplier type mismatch")
        need((int(exact["average_ceiling"]), int(exact["B_star"]), exact["full_budget_Q_multiplier_floor"]) == (average, B_star, multiplier), f"{row_id}: certificate calibration mismatch")

        max_e, max_delta, excess = extension_dimension_cut(p, B_star)
        ext = record["direct_extension_Delta_p_power_e_route_cut"]
        need(type(ext["max_e_Y"]) is int and type(ext["max_Delta_at_max_e_Y"]) is int, f"{row_id}: extension integer type mismatch")
        need((ext["max_e_Y"], ext["max_Delta_at_max_e_Y"], int(ext["first_forbidden_power_minus_budget"])) == (max_e, max_delta, excess), f"{row_id}: extension cut mismatch")
        need(ext["capacities_are_allocations"] is False, f"{row_id}: extension capacity mislabelled")

        required = ["U_paid", "U_Q", "U_BC" if kind == "MCA" else "U_list_int", "U_new"]
        completion = record["active_completion"]
        need(completion["required_atoms"] == required, f"{row_id}: required atoms mismatch")
        need(all(value is None for value in completion["complete_atom_values"].values()), f"{row_id}: invented current atom")
        need(completion["unresolved_cells"] and completion["closed"] is False, f"{row_id}: false closure")
        need(record["q_contract"]["upper_integer"] is None, f"{row_id}: invented U_Q")

    kb = read_json(KB995)
    need(kb["payload_sha256"] == "62a929dfc3936da808031926b0964ec68a19f5672fb72b2661def1b45da50cc7", "#995 payload mismatch")
    need(kb["ledger"]["U_paid_after"] == "422354730332", "#995 local paid charge mismatch")
    need(kb["ledger"]["B_remaining_after"] == "274980305756664755", "#995 local remainder mismatch")
    need(kb["ledger"]["U_Q"] is None and kb["ledger"]["residual_U_A"] is None, "#995 open values drift")
    need(kb["scope_guards"]["koalabear_row_closed"] is False, "#995 false closure")
    legacy = records[0]["legacy_stack_local_progress"]
    need(legacy["consumed_by_active_ledger"] is False and legacy["active_architecture_mapping"] is None, "legacy charge transplanted")
    need(legacy["packet_scope"] == "FULL_OUTSIDE_COEFFICIENT_RANK_TWO_SUBPROGRAM", "legacy packet scope drift")
    need(legacy["inherited_ledger_scope"] == "LEGACY_FIRST_MATCH_LEDGER_WITH_EARLIER_GLOBAL_OWNERS", "legacy inherited-ledger scope drift")
    need(legacy["received_pair_quantifier"] == "ARBITRARY_FIXED_PAIR_POINTWISE_UNIFORM_CAP", "legacy received-pair scope drift")
    need(legacy["translation_scope"] == "ONE_SP3_NORMALIZATION_PER_ARBITRARY_FIXED_PAIR", "legacy translation scope drift")
    need(legacy["fixed_pair_scope_alone_is_not_route_cut"] is True, "fixed-pair scope mislabelled as route cut")
    need(legacy["union_over_received_pairs_translations_selectors_sources_or_r_forbidden"] is True, "legacy union prohibition erased")
    for record in records[1:]:
        need(record["legacy_stack_local_progress"] is None, "legacy KB charge transferred across row")

    correction = read_json(EXT)
    need(correction["status"] == "COUNTEREXAMPLE_AND_CONTRACT_CORRECTION", "extension correction status mismatch")
    need(correction["supersession_gate"]["historical_acceptance_gate"] is False, "superseded extension packet restored")
    need(correction["corrected_contract"]["chart_terminal_without_source_binding"] == "UNPAID_PRIMITIVE", "extension source-free terminal mismatch")
    current_dimension_text = CURRENT_DIMENSION_DEGREE.read_text()
    need("\\label{thm:extension-line-dimension-degree-ledger}" in current_dimension_text, "current extension theorem missing")
    need("\\Delta_Y |\\B|^{e_Y}" in current_dimension_text, "current extension charge formula missing")
    extension_route = cert["extension_route_cut"]
    need(extension_route["current_dimension_degree_source"] == "tex/cs25_cap_v13_2.tex", "current extension source mismatch")
    need(extension_route["correction_full_python_acceptance_status"] == "STALE_SOURCE_PIN_AFTER_PROMOTION", "stale correction verifier hidden")

    route = cert["architecture_route_cut"]
    need(route["terminal"] == TERMINAL, "route-cut terminal mismatch")
    need(route["active_rows_closed"] == [] and route["all_four_rows_open"] is True, "current artifact set falsely closes a row")
    need(route["legacy_to_active_mapping_certificate"] is None, "invented architecture mapping")
    need(route["future_theorems_cut"] is False, "route cut overclaims future impossibility")
    interface = cert["candidate_interface"]
    need(interface["runtime_schema_shape_enforced"] is True, "candidate schema gate disabled")
    need(interface["canonical_contained_source_paths_required"] is True, "candidate path gate disabled")
    need(interface["typed_partition_atom_q_and_mapping_adapters_required"] is True, "candidate typed-adapter gate disabled")
    need(interface["exact_owner_order_coverage_required"] is True, "candidate owner-order gate disabled")
    need(interface["candidate_payload_identity_required"] is True, "candidate payload gate disabled")
    need(interface["candidate_audit_is_structural_preflight_only"] is True, "candidate preflight scope widened")
    need(interface["candidate_audit_can_close_row"] is False, "candidate preflight can close a row")
    need(interface["reviewed_source_registry_entry_required_for_banking"] is True, "candidate review-registry gate disabled")
    need(type(interface["trusted_review_registry_entries"]) is int and interface["trusted_review_registry_entries"] == 0, "unreviewed candidate source registry entry invented")
    need(interface["mechanical_validation_replaces_proof_review"] is False, "candidate mechanical audit overclaimed")
    need(interface["recognized_legacy_input_requires_explicit_architecture_mapping"] is True, "recognized legacy mapping gate disabled")
    need(interface["provenance_transform_detection_complete"] is False, "heuristic provenance detector overclaimed")

    print("[PASS] independent exact row replay: 4/4")
    print("[PASS] effective moved/list endpoints: 4/4")
    print("[PASS] exact canonical source set and source-bound architecture separation")
    print("[PASS] direct-extension route cuts under the Delta*p^e charge")
    print("[PASS] current terminal is route cut; active rows remain open")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
        return 0
    except (RuntimeError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
