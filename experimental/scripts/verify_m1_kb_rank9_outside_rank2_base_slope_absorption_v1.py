#!/usr/bin/env python3
"""Verify the existing-owner absorption of the printed J=166 pencil.

The proof is in the companion note. This checker binds the active-source
template to the earlier global base-slope owner, freezes first-match order,
records zero ledger movement, and fail-closes the genuinely extension-valued
residual. It does not prove a deployed extension-field payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import verify_kb_mca_1116048_base_slope_universe_v2 as base_owner
import verify_m1_kb_rank9_active_source_matroid_reindex_v1 as active


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-outside-rank2-base-slope-absorption-v1"
STATUS = (
    "PROVED_PRINTED_J166_TEMPLATE_EARLIER_OWNED_"
    "BROADER_EXTENSION_RANK2_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates"
    / "m1-kb-rank9-outside-rank2-base-slope-absorption-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_outside_rank2_base_slope_absorption_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_outside_rank2_base_slope_absorption_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-outside-rank2-base-slope-absorption-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1.sage"
)
ACTIVE_NOTE_REL = active.NOTE_REL
ACTIVE_CERT_REL = active.CERT_PATH.relative_to(ROOT)
ACTIVE_SCRIPT_REL = active.SCRIPT_REL
BASE_NOTE_REL = base_owner.NOTE_REL
BASE_CERT_REL = base_owner.CERT_PATH.relative_to(ROOT)
BASE_SCRIPT_REL = base_owner.VERIFIER_REL
FIRST_MATCH_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)

ACTIVE_PAYLOAD = (
    "4fa636866ddb4483ec577a44f3f832d1abaab5febab6c40271360214cfcecf3c"
)
BASE_OWNER_PAYLOAD = (
    "6ea64d19ecd298fb5be1bff9b17e7c41d3239553e0aa9ebfd7c9ff9d17896a56"
)

P = base_owner.P
EXTENSION_DEGREE = base_owner.E
SELECTED_SLOPES = 166
POST_BASE_SELECTED_SLOPES = 0
BASE_OWNER_INDEX = 7
SPARSE_OWNER_INDEX = 8

ContractError = active.ContractError
require = active.require
payload_hash = active.payload_hash


def file_hash(relative: Path) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def source_binding(
    binding_id: str, relative: Path, role: str
) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding(
            "active-note", ACTIVE_NOTE_REL,
            "printed equations (6.9)--(6.11) and predecessor scope",
        ),
        source_binding(
            "active-certificate", ACTIVE_CERT_REL,
            "exact J=166 template and current ledger snapshot",
        ),
        source_binding(
            "active-verifier", ACTIVE_SCRIPT_REL,
            "predecessor certificate semantics",
        ),
        source_binding(
            "base-owner-note", BASE_NOTE_REL,
            "global residual base-slope owner proof",
        ),
        source_binding(
            "base-owner-certificate", BASE_CERT_REL,
            "owner identity, order, and global-once charge",
        ),
        source_binding(
            "base-owner-verifier", BASE_SCRIPT_REL,
            "predecessor owner replay and nonclaims",
        ),
        source_binding(
            "first-match-note", FIRST_MATCH_NOTE_REL,
            "frozen branch order before the v2 owner rename",
        ),
        source_binding("proof-note", NOTE_REL, "proof and scope guards"),
        source_binding("verifier", SCRIPT_REL, "strict exact certificate replay"),
        source_binding("sage-control", SAGE_REL, "exact projective edge controls"),
        source_binding("readme", README_REL, "replay contract"),
    ]


def load_json(path: Path) -> dict[str, Any]:
    return base_owner.load_json(path)


def validate_predecessors() -> tuple[dict[str, Any], dict[str, Any]]:
    active_doc = load_json(ROOT / ACTIVE_CERT_REL)
    base_doc = load_json(ROOT / BASE_CERT_REL)
    active.validate_certificate(active_doc)
    base_owner.validate_certificate(base_doc)
    require(active_doc["payload_sha256"] == ACTIVE_PAYLOAD, "active payload drift")
    require(
        base_doc["payload_sha256"] == BASE_OWNER_PAYLOAD,
        "base-owner payload drift",
    )
    return active_doc, base_doc


def validate_consumed_source_facts(
    active_doc: dict[str, Any], base_doc: dict[str, Any]
) -> None:
    template = active_doc["full_outside_source_subcell"]["moving_root_template"]
    require(template["selected_slope_count"] == SELECTED_SLOPES, "J=166 drift")
    require(template["domain"] == "multiplicative subgroup D of F_p^x", "domain drift")
    require(template["domain_excludes_zero"] is True, "domain zero guard drift")
    require(template["P"] == "L_C*X", "template P drift")
    require(template["Q"] == "-L_C", "template Q drift")
    require(
        template["positive_determinant_mass_constructed"] is False,
        "predecessor scope drift",
    )
    require(
        active_doc["full_outside_source_subcell"]["terminal"]
        == "UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR",
        "predecessor terminal drift",
    )
    owner = base_doc["first_match"]
    require(owner["replacement_index_one_based"] == BASE_OWNER_INDEX, "owner index drift")
    require(owner["replacement_owner"] == "residual_base_slope_universe", "owner id drift")
    require(
        owner["v2_order"][BASE_OWNER_INDEX - 1]
        == "residual_base_slope_universe",
        "base branch order drift",
    )
    require(
        owner["v2_order"][SPARSE_OWNER_INDEX - 1]
        == "sparse_sigma_or_sparse_support",
        "sparse branch order drift",
    )
    theorem = base_doc["theorem"]
    require(theorem["set_inclusion"] == "residual_set subseteq F_p", "owner set drift")
    require(theorem["global_once_bound"] == str(P), "global owner amount drift")
    require(theorem["infinity_included"] is False, "finite-only owner drift")


def expected_certificate() -> dict[str, Any]:
    active_doc, base_doc = validate_predecessors()
    validate_consumed_source_facts(active_doc, base_doc)
    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    require("J_{\\mathrm{post\\text{-}base}}=0" in note_text, "post-owner statement drift")
    require(
        "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2" in note_text,
        "extension terminal drift",
    )
    require(
        "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP" in note_text,
        "lower-gcd terminal drift",
    )
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "n": active.N,
            "k": active.K,
            "agreement_A": active.A,
            "j": active.J,
            "t": active.T,
        },
        "predecessors": {
            "active_source_matroid_reindex": "payload-sha256:" + ACTIVE_PAYLOAD,
            "residual_base_slope_universe": "payload-sha256:" + BASE_OWNER_PAYLOAD,
        },
        "printed_template": {
            "domain_chain": "W subset D subset F_p^x",
            "P": "L_C*X",
            "Q": "-L_C",
            "moving_root_equation": "P+rho*Q=L_C*(X-rho)",
            "slope_identity": "eta_rho=rho",
            "selected_slope_count_before_owner_removal": SELECTED_SLOPES,
            "selected_slope_count_after_base_owner_removal": POST_BASE_SELECTED_SLOPES,
            "new_outlier_records_can_resurrect_deleted_labels": False,
            "positive_determinant_mass_constructed_in_predecessor": False,
        },
        "owner_route": {
            "frozen_order": base_owner.V2_ORDER,
            "base_owner_index_one_based": BASE_OWNER_INDEX,
            "sparse_owner_index_one_based": SPARSE_OWNER_INDEX,
            "base_owner": "residual_base_slope_universe",
            "later_branch": "sparse_sigma_or_sparse_support",
            "assignment_rule": "each printed slope is assigned at or before branch 7",
            "post_owner_selector_rebuild_required": True,
            "corrected_template_terminal": "PAID_BASE_SLOPE_UNIVERSE_BEFORE_SPARSE_SELECTOR",
        },
        "proved_lemmas": {
            "base_defined_moving_root": {
                "hypotheses": "D subset F_p; lambda*P,lambda*Q in F_p[X]; x not a common root",
                "finite_slope_formula": "eta=-P(x)/Q(x)",
                "conclusion": "every finite moving-root slope lies in F_p",
            },
            "maximal_gcd_subline": {
                "hypotheses": "P=G(aX+b), Q=G(cX+d), det([[a,b],[c,d]]) nonzero",
                "classifier": "q_M(X,Z)=det(M*(X,Z)^T,M^(p)*(X,Z)^T)",
                "base_defined_iff": "q_M is identically zero iff M is projectively F_p-defined",
                "nonstandard_intersection_bound": 2,
                "bound_is_absolute": True,
            },
        },
        "edge_guards": {
            "classify_after_gcd_reduction": True,
            "nonbase_coefficients_before_cancellation_are_insufficient": True,
            "cancelled_common_roots_remain_deleted_inputs": True,
            "finite_denominator_zero_is_projective_infinity_not_a_finite_slope": True,
            "determinant_zero_routes_to_rank_at_most_one_degenerate_not_PGL2": True,
            "lower_gcd_reduces_to_subline": False,
        },
        "residual_terminals": [
            "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2",
            "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
            "UNBOUND_ACTIVE_SOURCE_HIT_BASIS_TAIL",
        ],
        "exact_control": {
            "field": "GF(5^6)",
            "base_field": "GF(5)",
            "base_projective_line_size": 6,
            "base_PGL2_classes_checked": 120,
            "nonbase_slice_total": 625,
            "nonbase_slice_invertible": 580,
            "nonbase_slice_singular": 45,
            "nonbase_intersection_histogram": {"0": 0, "1": 80, "2": 500},
            "zero_hit_example_checked": True,
            "pole_common_root_rank_one_zero_guards_checked": True,
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_PAYMENT",
        },
        "ledger": {
            "U_paid": active_doc["ledger"]["U_paid"],
            "B_remaining": active_doc["ledger"]["B_remaining"],
            "ledger_movement": 0,
            "base_owner_charge_already_banked": str(P),
            "historical_base_packet_ledger_replaces_current_stack": False,
            "U_Q": None,
            "U_A": None,
            "row_status": "YELLOW_EXTENSION_AND_SOURCE_LOAD_RESIDUALS_OPEN",
        },
        "scope_guards": {
            "printed_J166_template_closed": True,
            "general_full_outside_rank2_closed": False,
            "extension_slope_payment_proved": False,
            "complete_post_owner_selector_built": False,
            "koalabear_row_safe": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
        },
        "nonclaims": [
            "No new numerator charge is banked by this packet.",
            "The at-most-two theorem counts base intersections, not extension slopes.",
            "Eight outliers may create other slopes and require a rebuilt selector.",
            "Lower-gcd rational maps are not projective sublines in general.",
            "The packet does not determine U_Q or U_A or prove the row safe.",
        ],
        "source_bindings": expected_source_bindings(),
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(document: dict[str, Any]) -> None:
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    strict_match(document, expected_certificate())


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def certificate_mutations() -> list[Mutation]:
    return [
        ("status", lambda d: d.__setitem__("status", "PROVED_GLOBAL_RANK2_PAYMENT")),
        ("p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("active-predecessor", lambda d: d["predecessors"].__setitem__("active_source_matroid_reindex", "payload-sha256:00")),
        ("base-predecessor", lambda d: d["predecessors"].__setitem__("residual_base_slope_universe", "payload-sha256:00")),
        ("domain", lambda d: d["printed_template"].__setitem__("domain_chain", "W subset F_(p^6)")),
        ("P", lambda d: d["printed_template"].__setitem__("P", "L_C*(X+a)")),
        ("Q", lambda d: d["printed_template"].__setitem__("Q", "-a*L_C")),
        ("slope", lambda d: d["printed_template"].__setitem__("slope_identity", "unknown")),
        ("selected", lambda d: d["printed_template"].__setitem__("selected_slope_count_before_owner_removal", 165)),
        ("post-owner", lambda d: d["printed_template"].__setitem__("selected_slope_count_after_base_owner_removal", 1)),
        ("resurrect", lambda d: d["printed_template"].__setitem__("new_outlier_records_can_resurrect_deleted_labels", True)),
        ("base-index", lambda d: d["owner_route"].__setitem__("base_owner_index_one_based", 8)),
        ("sparse-index", lambda d: d["owner_route"].__setitem__("sparse_owner_index_one_based", 7)),
        ("order-swap", lambda d: d["owner_route"].__setitem__("frozen_order", [*base_owner.V2_ORDER[:6], base_owner.V2_ORDER[7], base_owner.V2_ORDER[6], *base_owner.V2_ORDER[8:]])),
        ("owner", lambda d: d["owner_route"].__setitem__("base_owner", "per-chart-base-owner")),
        ("no-rebuild", lambda d: d["owner_route"].__setitem__("post_owner_selector_rebuild_required", False)),
        ("false-unpaid", lambda d: d["owner_route"].__setitem__("corrected_template_terminal", "UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR")),
        ("common-root", lambda d: d["proved_lemmas"]["base_defined_moving_root"].__setitem__("hypotheses", "D subset F_p")),
        ("wrong-formula", lambda d: d["proved_lemmas"]["base_defined_moving_root"].__setitem__("finite_slope_formula", "eta=P(x)/Q(x)")),
        ("intersection-three", lambda d: d["proved_lemmas"]["maximal_gcd_subline"].__setitem__("nonstandard_intersection_bound", 3)),
        ("pre-reduction", lambda d: d["edge_guards"].__setitem__("classify_after_gcd_reduction", False)),
        ("restore-common", lambda d: d["edge_guards"].__setitem__("cancelled_common_roots_remain_deleted_inputs", False)),
        ("finite-pole", lambda d: d["edge_guards"].__setitem__("finite_denominator_zero_is_projective_infinity_not_a_finite_slope", False)),
        ("degenerate-as-PGL2", lambda d: d["edge_guards"].__setitem__("determinant_zero_routes_to_rank_at_most_one_degenerate_not_PGL2", False)),
        ("lower-gcd-subline", lambda d: d["edge_guards"].__setitem__("lower_gcd_reduces_to_subline", True)),
        ("delete-extension-terminal", lambda d: d["residual_terminals"].pop(0)),
        ("toy-histogram", lambda d: d["exact_control"]["nonbase_intersection_histogram"].__setitem__("2", 499)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("scale", "DEPLOYED_PAYMENT")),
        ("ledger", lambda d: d["ledger"].__setitem__("ledger_movement", 1)),
        ("historical-ledger", lambda d: d["ledger"].__setitem__("historical_base_packet_ledger_replaces_current_stack", True)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("general-closure", lambda d: d["scope_guards"].__setitem__("general_full_outside_rank2_closed", True)),
        ("extension-paid", lambda d: d["scope_guards"].__setitem__("extension_slope_payment_proved", True)),
        ("row-safe", lambda d: d["scope_guards"].__setitem__("koalabear_row_safe", True)),
        ("rank10", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "00")),
        ("payload", lambda d: d.__setitem__("payload_sha256", "00")),
    ]


def run_tamper_selftest() -> int:
    expected = expected_certificate()
    rejected = 0
    for name, mutate in certificate_mutations():
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except (ContractError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    require(rejected == len(certificate_mutations()), "mutation count mismatch")
    print(f"M1 outside-rank-two base-slope absorption mutations: {rejected}/{rejected} PASS")
    return 0


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(expected_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.print_certificate:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return 0
    if args.write:
        write_certificate()
        print(CERT_PATH)
        return 0
    document = load_json(CERT_PATH)
    validate_certificate(document)
    print("M1 outside-rank-two base-slope absorption: PASS")
    print("  printed J=166 slopes: all assigned at or before base owner branch 7")
    print("  post-owner printed graph line: J=0 before sparse/rank-nine branch 8")
    print("  maximal-gcd nonstandard subline: at most two base intersections")
    print("  broader extension/lower-gcd residual: YELLOW; ledger movement 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
