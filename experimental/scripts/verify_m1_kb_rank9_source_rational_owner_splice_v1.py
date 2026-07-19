#!/usr/bin/env python3
r"""Verify the adaptive pair-global source--rational owner splice.

The companion note widens the #962 source--Mobius owner to every qualifying
full-outside rank-two record whose full-gcd-reduced rational map has degree at
most floor((|Sigma|-1)/2).  Projective rational-map rigidity synchronizes all
such records across selectors.  Their finite slopes remain in one image of
D\Sigma, so the predecessor cap is unchanged and the incremental ledger
movement is zero.

The packet also freezes the sharp residual consequences

    |Sigma| >= 36,836,
    reduced degree >= 18,418,
    full gcd degree <= 1,030,157.

It does not pay the remaining high-degree or non-full-outside cells, determine
U_Q or U_A, close rank nine, or close the KoalaBear row.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_active_source_matroid_reindex_v1 as active_source
import verify_m1_kb_rank9_projective_source_load_v1 as source_load
import verify_m1_kb_rank9_source_mobius_owner_splice_v1 as source_mobius


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-source-rational-owner-splice-v1"
ARTIFACT_KIND = "M1_KB_RANK9_PAIR_GLOBAL_SOURCE_RATIONAL_OWNER_SPLICE"
STATUS = (
    "PROVED_ADAPTIVE_PAIR_GLOBAL_SOURCE_RATIONAL_OWNER_"
    "ZERO_MOVEMENT_SPLICE_HIGH_DEGREE_RESIDUAL_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-source-rational-owner-splice-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_source_rational_owner_splice_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_source_rational_owner_splice_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-source-rational-owner-splice-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.sage"
)

SOURCE_MOBIUS_PAYLOAD = (
    "239ca25b91ef6a4f98af31aef9d5b5ddd970204043abe2153223eab5d39629e1"
)
SOURCE_LOAD_PAYLOAD = (
    "68ada825d2e16544298ccc94dc390e3266ab175b375ab118de73f8e0e8040e0f"
)
ACTIVE_SOURCE_PAYLOAD = (
    "4fa636866ddb4483ec577a44f3f832d1abaab5febab6c40271360214cfcecf3c"
)

tangent = source_mobius.tangent
P = source_mobius.P
N = source_mobius.N
K = source_mobius.K
A = source_mobius.A
J = source_mobius.J
T = source_mobius.T
RICH_X_MAX = source_mobius.RICH_X_MAX
SIGMA_FLOOR = source_mobius.SIGMA_FLOOR


class ContractError(RuntimeError):
    """Raised for parser, source, semantic, or exact-arithmetic drift."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def adaptive_degree_cap(source_size: int) -> int:
    """Largest degree for which source_size anchors force equality."""

    require(type(source_size) is int, "source size is not an exact integer")
    require(source_size >= 1, "source size must be positive")
    return (source_size - 1) // 2


def survivor_degree_floor(source_size: int) -> int:
    """First degree not covered by the adaptive rigidity owner."""

    require(type(source_size) is int, "source size is not an exact integer")
    require(source_size >= 1, "source size must be positive")
    return adaptive_degree_cap(source_size) + 1


DEPLOYED_DEGREE_CAP = adaptive_degree_cap(SIGMA_FLOOR)
UNIFORM_HIGH_GCD_FLOOR = K - 1 - DEPLOYED_DEGREE_CAP

# A survivor satisfies ceil(s/2) <= e <= s+x-t-1.  Equivalently,
# floor(s/2) >= t+1-x.  The weakest constraint uses x=RICH_X_MAX.
SURVIVOR_HALF_FLOOR = T + 1 - RICH_X_MAX
SURVIVOR_SIGMA_FLOOR = 2 * SURVIVOR_HALF_FLOOR
SURVIVOR_DEGREE_FLOOR = survivor_degree_floor(SURVIVOR_SIGMA_FLOOR)
SURVIVOR_GCD_CEILING = K - 1 - SURVIVOR_DEGREE_FLOOR
ADAPTIVELY_CLOSED_GCD_FLOOR = SURVIVOR_GCD_CEILING + 1
ADAPTIVELY_CLOSED_GCD_COUNT = (K - 2) - ADAPTIVELY_CLOSED_GCD_FLOOR + 1

SOURCE_RATIONAL_CAP = N - SIGMA_FLOOR
PREDECESSOR_OWNER_CAP = source_mobius.SOURCE_MOBIUS_CAP
PREDECESSOR_JOINT_CAP = source_mobius.NEW_JOINT_CAP
NEW_JOINT_CAP = PREDECESSOR_JOINT_CAP
LEDGER_MOVEMENT = 0
U_PAID_BEFORE = source_mobius.U_PAID_AFTER
U_PAID_AFTER = U_PAID_BEFORE
B_REMAINING_BEFORE = source_mobius.B_REMAINING_AFTER
B_REMAINING_AFTER = B_REMAINING_BEFORE

OLD_OWNER_ID = source_mobius.SOURCE_OWNER_ID
SOURCE_OWNER_ID = "source_rational_full_outside_bounded_degree"
PAID_TERMINAL = "PAID_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL"
HIGH_DEGREE_TERMINAL = (
    "UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418"
)
SOURCE_LOAD_TERMINAL = "UNBOUND_POST_TANGENT_SOURCE_LOAD"

FIRST_MATCH_ORDER = list(source_mobius.FIRST_MATCH_ORDER)
_OWNER_INDEX = FIRST_MATCH_ORDER.index(OLD_OWNER_ID)
FIRST_MATCH_ORDER[_OWNER_INDEX] = SOURCE_OWNER_ID

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "counted_object_contract",
    "pair_global_source_contract",
    "adaptive_rational_rigidity",
    "source_rational_owner",
    "cross_selector_containment",
    "adaptive_residual",
    "first_match_partition",
    "joint_owner_theorem",
    "selector_restart",
    "exact_control",
    "ledger",
    "rank9_gate",
    "residual_route_cuts",
    "scope_guards",
    "nonclaims",
    "source_bindings",
    "payload_sha256",
}


def exact_int(value: object, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return int(value)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ContractError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise ContractError(f"floating-point JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing source binding: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("proof-note", NOTE_REL, "adaptive rational rigidity and splice"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding("sage-control", SAGE_REL, "exact rigidity and sharpness controls"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding(
            "source-mobius-note",
            source_mobius.NOTE_REL,
            "pair-global predecessor and moving-root bridge",
        ),
        source_binding(
            "source-mobius-certificate",
            source_mobius.CERT_PATH.relative_to(ROOT),
            "immediate predecessor fingerprint",
        ),
        source_binding(
            "source-mobius-verifier",
            source_mobius.SCRIPT_REL,
            "predecessor first-match and ledger semantics",
        ),
        source_binding(
            "source-mobius-sage",
            source_mobius.SAGE_REL,
            "predecessor exact projective controls",
        ),
        source_binding(
            "source-load-note",
            source_load.NOTE_REL,
            "rank-two reduced-degree and source-load facts",
        ),
        source_binding(
            "source-load-certificate",
            source_load.CERT_PATH.relative_to(ROOT),
            "source-load predecessor fingerprint",
        ),
        source_binding(
            "source-load-verifier",
            source_load.SCRIPT_REL,
            "source-load semantic contract",
        ),
        source_binding(
            "active-source-note",
            active_source.NOTE_REL,
            "full-outside source-rank split and floor",
        ),
        source_binding(
            "active-source-certificate",
            active_source.CERT_PATH.relative_to(ROOT),
            "active-source predecessor fingerprint",
        ),
        source_binding(
            "active-source-verifier",
            active_source.SCRIPT_REL,
            "full-outside predecessor semantic contract",
        ),
    ]


def validate_predecessors() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    mobius_doc = load_json(source_mobius.CERT_PATH)
    source_mobius.validate_certificate(mobius_doc)
    require(
        mobius_doc["payload_sha256"] == SOURCE_MOBIUS_PAYLOAD,
        "#962 source-Mobius payload drift",
    )

    source_load_doc = load_json(source_load.CERT_PATH)
    source_load.validate_certificate(source_load_doc)
    require(
        source_load_doc["payload_sha256"] == SOURCE_LOAD_PAYLOAD,
        "projective source-load payload drift",
    )

    active_doc = load_json(active_source.CERT_PATH)
    active_source.validate_certificate(active_doc)
    require(
        active_doc["payload_sha256"] == ACTIVE_SOURCE_PAYLOAD,
        "active-source payload drift",
    )
    return mobius_doc, source_load_doc, active_doc


def validate_consumed_facts(
    mobius_doc: dict[str, Any],
    source_load_doc: dict[str, Any],
    active_doc: dict[str, Any],
) -> None:
    pair = mobius_doc["pair_global_source_contract"]
    require(pair["fixed_received_pair"] is True, "received-pair scope drift")
    require(pair["fixed_sp3_translation"] is True, "SP3 translation drift")
    require(pair["alternative_translation_union_forbidden"] is True, "translation union drift")
    require(pair["source_label_nonzero_on_Sigma"] is True, "source-label drift")
    require(pair["source_anchor_floor"] == SIGMA_FLOOR, "source floor drift")

    old_owner = mobius_doc["source_mobius_owner"]
    require(old_owner["owner_id"] == OLD_OWNER_ID, "predecessor owner drift")
    require(old_owner["domain"] == "D SETMINUS Sigma", "predecessor domain drift")
    require(old_owner["uniform_cap"] == SOURCE_RATIONAL_CAP, "predecessor cap drift")
    require(old_owner["using_all_D_forbidden"] is True, "predecessor D guard drift")

    old_containment = mobius_doc["cross_selector_containment"]
    require(
        old_containment["full_outside_each_selector"]
        == "V_sigma INTERSECT Sigma is empty",
        "predecessor full-outside drift",
    )
    require(old_containment["coefficient_rank_each_line"] == 2, "rank-two drift")
    require(old_containment["contributing_beta_positive"] is True, "beta drift")
    require(old_containment["contributing_J_at_least"] == 21, "J drift")
    require(old_containment["contributing_x_at_most"] == RICH_X_MAX, "x drift")
    require(
        old_containment["moving_root_x_in_W_subset_V_subset_D_minus_Sigma"] is True,
        "moving-root domain drift",
    )
    require(old_containment["moving_root_is_not_common_root"] is True, "common-root drift")

    old_partition = mobius_doc["first_match_partition"]
    require(old_partition["order"] == source_mobius.FIRST_MATCH_ORDER, "owner order drift")
    require(old_partition["incoming_exact_residual_required"] is True, "incoming residual drift")
    require(old_partition["later_owners_receive_exact_set_difference"] is True, "deletion drift")

    old_ledger = mobius_doc["ledger"]
    require(old_ledger["U_paid_after"] == str(U_PAID_BEFORE), "U_paid predecessor drift")
    require(
        old_ledger["B_remaining_after"] == str(B_REMAINING_BEFORE),
        "B_remaining predecessor drift",
    )
    require(old_ledger["U_Q"] is None, "predecessor U_Q drift")
    require(old_ledger["residual_U_A"] is None, "predecessor U_A drift")

    theorem = source_load_doc["theorem_contract"]
    reduced = source_load_doc["rank_two_reduced_root_gate"]
    incidence = source_load_doc["same_selector_incidence"]
    require(
        theorem["rank_split"] == "rank_F span(P_L,Q_L) is exactly 1 or 2",
        "source-load rank split drift",
    )
    require(
        theorem["rank_two"]
        == "after factoring G_L, every projective fiber has size <=d_L^proj=s_L+x_L-t-1",
        "source-load rank-two degree drift",
    )
    require(
        reduced["reduced_degree"] == "k-1-c_L=s_L+x_L-t-1",
        "source-load reduced-degree formula drift",
    )
    require(
        incidence["source_h_outside_V_is_universal_rank_zero_edge_case"] is True,
        "source-load universal edge drift",
    )
    require(
        theorem["current_deployed_terminal"] == SOURCE_LOAD_TERMINAL,
        "source-load terminal drift",
    )

    deployed = active_doc["deployed_row"]
    full_outside = active_doc["full_outside_source_subcell"]
    require(deployed["rich_x_max"] == RICH_X_MAX, "active-source x cap drift")
    require(
        full_outside["hypothesis"] == "Sigma INTERSECT V is empty",
        "active-source full-outside drift",
    )
    require(
        full_outside["rank_one_excluded_by_source_syndrome_rank_two"] is True,
        "active-source rank-one exclusion drift",
    )
    require(
        full_outside["rank_two_source_floor"] == "|Sigma|>=t-x_L+2",
        "active-source rank-two floor drift",
    )
    require(
        active_doc["route_cut"]["encompassing_terminal"] == SOURCE_LOAD_TERMINAL,
        "active-source encompassing terminal drift",
    )


def validate_exact_arithmetic() -> None:
    require(SIGMA_FLOOR == 18_419, "deployed source floor drift")
    require(DEPLOYED_DEGREE_CAP == 9_209, "deployed rational degree cap drift")
    require(2 * DEPLOYED_DEGREE_CAP < SIGMA_FLOOR, "rigidity strictness failed")
    require(
        2 * (DEPLOYED_DEGREE_CAP + 1) >= SIGMA_FLOOR,
        "degree cap is not maximal",
    )
    require(UNIFORM_HIGH_GCD_FLOOR == 1_039_366, "uniform gcd floor drift")
    require(SURVIVOR_HALF_FLOOR == 18_418, "survivor half-floor drift")
    require(SURVIVOR_SIGMA_FLOOR == 36_836, "survivor Sigma floor drift")
    require(SURVIVOR_DEGREE_FLOOR == 18_418, "survivor degree floor drift")
    require(SURVIVOR_GCD_CEILING == 1_030_157, "survivor gcd ceiling drift")
    require(ADAPTIVELY_CLOSED_GCD_FLOOR == 1_030_158, "closed gcd floor drift")
    require(ADAPTIVELY_CLOSED_GCD_COUNT == 18_417, "closed gcd count drift")
    require(SOURCE_RATIONAL_CAP == 2_078_733, "source-rational cap drift")
    require(SOURCE_RATIONAL_CAP == PREDECESSOR_OWNER_CAP, "owner cap changed")
    require(NEW_JOINT_CAP == PREDECESSOR_JOINT_CAP, "joint cap changed")
    require(LEDGER_MOVEMENT == 0, "ledger movement is not zero")
    require(U_PAID_AFTER == U_PAID_BEFORE, "U_paid changed")
    require(B_REMAINING_AFTER == B_REMAINING_BEFORE, "B_remaining changed")

    # Exhaust the deployed integer range used in the implication.  This is an
    # arithmetic audit, not a finite-field census.
    first_survivor = None
    for source_size in range(SIGMA_FLOOR, SURVIVOR_SIGMA_FLOOR + 1):
        lower = survivor_degree_floor(source_size)
        upper = source_size + RICH_X_MAX - T - 1
        if lower <= upper:
            first_survivor = source_size
            break
    require(first_survivor == SURVIVOR_SIGMA_FLOOR, "first survivor source size drift")


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    mobius_doc, source_load_doc, active_doc = validate_predecessors()
    validate_consumed_facts(mobius_doc, source_load_doc, active_doc)
    validate_exact_arithmetic()

    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        PAID_TERMINAL,
        HIGH_DEGREE_TERMINAL,
        SOURCE_LOAD_TERMINAL,
        "Corollary 4.2 (subset stability and post-restart exclusion)",
    ):
        require(token in note_text, f"proof-note terminal missing: {token}")

    sage_text = (ROOT / SAGE_REL).read_text(encoding="utf-8")
    require("def require(condition, message):" in sage_text, "Sage fail-closed helper missing")
    require(
        all(not line.lstrip().startswith("assert ") for line in sage_text.splitlines()),
        "bare Sage assert is unsafe under optimized Python",
    )

    stale_fields = list(mobius_doc["selector_restart"]["stale_selector_fields_forbidden"])
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": tangent.EXTENSION_DEGREE,
            "q_line": str(P**tangent.EXTENSION_DEGREE),
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "rich_uniform_cap": tangent.UNIFORM_CAP,
        },
        "predecessors": {
            "source_mobius_owner_splice": "payload-sha256:" + SOURCE_MOBIUS_PAYLOAD,
            "projective_source_load": "payload-sha256:" + SOURCE_LOAD_PAYLOAD,
            "active_source_matroid_reindex": "payload-sha256:" + ACTIVE_SOURCE_PAYLOAD,
        },
        "counted_object_contract": {
            "object": "distinct support-wise MCA-bad finite slopes of one received pair",
            "charge_scope": "FIRST_MATCH_GLOBAL_ONCE_PER_RECEIVED_PAIR",
            "cross_received_pair_union_required": False,
            "selectors_are_unioned_only_at_slope_set_level": True,
            "per_selector_charge_forbidden": True,
            "determinant_atlas_mass_cross_selector_mixing_forbidden": True,
            "witness_support_line_chart_and_basis_counts_forbidden": True,
            "projective_infinity_is_not_a_finite_slope": True,
            "new_owner_replaces_not_supplements_source_mobius_owner": True,
        },
        "pair_global_source_contract": {
            "fixed_received_pair": True,
            "fixed_sp3_translation": True,
            "alternative_translation_union_forbidden": True,
            "source_pair": "(epsilon_0,epsilon_1)",
            "Sigma": "supp(epsilon_0) UNION supp(epsilon_1) subseteq D",
            "source_size_symbol": "s=|Sigma|",
            "source_label": "lambda(h)=[-epsilon_0(h):epsilon_1(h)]",
            "source_label_nonzero_on_Sigma": True,
            "source_anchor_floor_formula": "t-floor(j/20)+2",
            "rich_x_max": RICH_X_MAX,
            "source_anchor_floor": SIGMA_FLOOR,
            "pair_global_fields_survive_selector_restart": [
                "epsilon_0",
                "epsilon_1",
                "Sigma",
                "s",
            ],
        },
        "adaptive_rational_rigidity": {
            "full_monic_gcd": "H_L=gcd(P_L,Q_L)",
            "forced_locator_in_place_of_full_gcd_forbidden": True,
            "reduced_pair": "(A_L,B_L)=(P_L/H_L,Q_L/H_L)",
            "reduced_pair_coprime": True,
            "map": "psi_L=[-A_L:B_L]",
            "reduced_degree": "e_L=max(deg A_L,deg B_L)",
            "adaptive_degree_cap": "E(s)=floor((s-1)/2)",
            "cross_polynomial": "A_L*B_Lprime-A_Lprime*B_L",
            "cross_polynomial_degree_bound": "at most e_L+e_Lprime<=2E(s)<s",
            "all_source_anchors_are_roots": True,
            "cross_polynomial_identically_zero": True,
            "coprime_pairs_define_same_projective_rational_map": True,
            "uniqueness_only_among_maps_of_degree_at_most_E_s": True,
            "global_uniqueness_among_arbitrary_degree_maps_claimed": False,
            "affine_division_at_source_anchors_forbidden": True,
            "infinity_source_labels_allowed": True,
            "poles_on_D_minus_Sigma_allowed": True,
            "injectivity_required": False,
            "deployed_source_floor": SIGMA_FLOOR,
            "deployed_uniform_degree_cap": DEPLOYED_DEGREE_CAP,
            "strict_degree_check": f"2*{DEPLOYED_DEGREE_CAP}={2*DEPLOYED_DEGREE_CAP}<{SIGMA_FLOOR}",
            "next_degree_not_uniformly_rigid": 2 * (DEPLOYED_DEGREE_CAP + 1) >= SIGMA_FLOOR,
        },
        "source_rational_owner": {
            "owner_id": SOURCE_OWNER_ID,
            "owner_is_intrinsic_not_chosen_from_selector": True,
            "compatibility_condition": (
                "there exists a coprime projective rational map psi of degree at most E(s) "
                "matching lambda(h) for every h in Sigma"
            ),
            "compatible_map_unique_within_printed_degree_range": True,
            "incompatible_source_data_owner_is_empty": True,
            "nonempty_owner_without_compatible_map_forbidden": True,
            "domain": "D SETMINUS Sigma",
            "using_all_D_forbidden": True,
            "finite_image": (
                "R={eta in F:[eta:1]=psi([x:1]) for some x in D SETMINUS Sigma}"
            ),
            "projective_infinity_deleted_from_finite_owner": True,
            "assigned_cell": "Z_SRat=Gamma_in INTERSECT R",
            "outgoing_cell": "Gamma_out=Gamma_in SETMINUS Z_SRat",
            "actual_cap_formula": "|R|<=|D SETMINUS Sigma|=n-s",
            "uniform_cap_formula": "n-18419",
            "uniform_cap": SOURCE_RATIONAL_CAP,
            "collisions_only_reduce_image_size": True,
            "absorbs_predecessor_source_mobius_owner": True,
            "predecessor_owner_id_replaced": OLD_OWNER_ID,
            "separate_source_mobius_charge": 0,
            "earlier_overlap_removed": True,
            "later_overlap_deleted_exactly": True,
        },
        "cross_selector_containment": {
            "quantifier": (
                "every Gamma subseteq Gamma_in, all source-bound complete selectors "
                "on Gamma, and all qualifying lines"
            ),
            "subset_stable_for_every_Gamma_subset_Gamma_in": True,
            "post_restart_application_to_Gamma_out": True,
            "same_carrier_across_selectors_required": False,
            "full_outside_each_selector": "V_sigma INTERSECT Sigma is empty",
            "coefficient_rank_each_line": 2,
            "contributing_beta_positive": True,
            "contributing_J_at_least": 21,
            "contributing_x_at_most": RICH_X_MAX,
            "full_monic_gcd_used_each_line": True,
            "source_rank_two_floor_each_line": "s>=t-x_L+2",
            "anchor_equality_each_line": (
                "psi_sigma_L([h:1])=[-epsilon_0(h):epsilon_1(h)] for every h in Sigma"
            ),
            "qualifying_degree_each_line": "e_sigma_L<=E(s)",
            "adaptive_rigidity_across_selectors": True,
            "all_qualifying_maps_common": True,
            "moving_root_x_in_W_subset_V_subset_D_minus_Sigma": True,
            "moving_root_is_not_common_root": True,
            "selected_finite_slope_equals_common_psi_of_x": True,
            "union_containment": (
                "UNION_sigma UNION_L Gamma_sigma_L_fin subseteq R(epsilon_0,epsilon_1)"
            ),
            "no_qualifying_record_if_compatibility_fails": True,
            "selector_inventory_or_Route_S_U_C_required": False,
            "determinant_weights_transferred_across_selectors": False,
        },
        "adaptive_residual": {
            "survivor_degree_condition": "e_L>=E(s)+1=ceil(s/2)",
            "rank_two_reduced_degree_upper_bound": "e_L<=s+x_L-t-1",
            "rich_x_upper_bound": RICH_X_MAX,
            "combined_half_floor": "floor(s/2)>=t+1-x_L>=18418",
            "survivor_source_floor": SURVIVOR_SIGMA_FLOOR,
            "survivor_reduced_degree_floor": SURVIVOR_DEGREE_FLOOR,
            "full_gcd_degree_relation": "deg(H_L)+e_L<=k-1",
            "survivor_full_gcd_degree_ceiling": SURVIVOR_GCD_CEILING,
            "adaptively_closed_full_gcd_degree_floor": ADAPTIVELY_CLOSED_GCD_FLOOR,
            "adaptively_closed_full_gcd_degree_ceiling": K - 2,
            "adaptively_closed_full_gcd_degree_count": ADAPTIVELY_CLOSED_GCD_COUNT,
            "uniform_degree_cap_at_source_floor": DEPLOYED_DEGREE_CAP,
            "uniform_sufficient_full_gcd_degree_floor": UNIFORM_HIGH_GCD_FLOOR,
            "boundary_source_size_exhaustion_checked": True,
            "terminal": HIGH_DEGREE_TERMINAL,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "projective_base_pair_C5_index_one_based": FIRST_MATCH_ORDER.index(
                "projective_base_pair_C5"
            )
            + 1,
            "source_rational_index_one_based": FIRST_MATCH_ORDER.index(SOURCE_OWNER_ID) + 1,
            "residual_extension_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_extension_valued_strata"
            )
            + 1,
            "residual_base_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_base_slope_universe"
            )
            + 1,
            "source_mobius_owner_removed_from_order": OLD_OWNER_ID not in FIRST_MATCH_ORDER,
            "incoming_exact_residual_required": True,
            "earlier_owner_intersection_removed": True,
            "later_owners_receive_exact_set_difference": True,
            "owner_may_delete_bounded_slopes_without_qualifying_record": True,
            "later_uniform_caps_valid_on_smaller_residual": True,
        },
        "joint_owner_theorem": {
            "rank_zero_noncontained_exact_witness_residual_empty": True,
            "positive_rank_cases_exhaustive": True,
            "base_projective_case_condition": "rank(Y_R)>0 and F_proj(R)=F_p",
            "base_projective_case_C5_owns_all_post5_slopes": True,
            "base_projective_case_later_cells_empty": True,
            "base_projective_case_cap": str(source_mobius.C5_BASE_CASE_CAP),
            "nonbase_case_condition": "rank(Y_R)>0 and F_proj(R)!=F_p",
            "nonbase_case_C5_cell_empty": True,
            "nonbase_source_rational_cap": str(SOURCE_RATIONAL_CAP),
            "nonbase_later_residual_base_cap": str(P),
            "source_and_later_base_disjoint_by_exact_deletion": True,
            "nonbase_case_cap": str(source_mobius.NONBASE_SOURCE_BASE_CASE_CAP),
            "case_combination": "MAXIMUM_NOT_SUM",
            "joint_cap_formula": "max(p+1,p+n-18419)=p+n-18419",
            "joint_uniform_cap": str(NEW_JOINT_CAP),
            "predecessor_joint_cap": str(PREDECESSOR_JOINT_CAP),
            "replaces_existing_joint_block": True,
            "adds_independent_joint_block": False,
        },
        "selector_restart": {
            "complete_selector_restriction_certifies_nonempty_new_universe": True,
            "old_rank9_selector_restricts_to_rank_at_most_9": True,
            "rank_at_least_10_can_be_new_minimum": False,
            "later_pair_global_owner_cells_applied_to_exact_outgoing_set": True,
            "complete_selector_universe_must_be_rebuilt": True,
            "restart_order": list(tangent.RESTART_ORDER),
            "global_carrier_gate_must_be_rerun": True,
            "small_family_gate_must_be_rerun": True,
            "affine_rank_minimizer_must_be_recomputed": True,
            "stale_selector_fields_forbidden": stale_fields,
            "same_sp3_translation_required_downstream": True,
            "source_fields_preserved_downstream": ["epsilon_0", "epsilon_1", "Sigma", "s"],
            "rank_caps_are_alternatives_not_sum": True,
            "rank9_coarse_gate_must_be_replayed": True,
        },
        "exact_control": {
            "status": "PASS",
            "field_order": 13,
            "owner": SOURCE_OWNER_ID,
            "residual": HIGH_DEGREE_TERMINAL,
            "selector_count": 2,
            "common_reduced_degree": 2,
            "distinct_full_gcds": True,
            "anchor_count": 5,
            "anchor_matrix_rank": 5,
            "anchor_kernel_dimension": 1,
            "sharp_agreement_count": 4,
            "sharp_anchor_kernel_dimension": 2,
            "outside_domain_count": 8,
            "outside_projective_image_count": 7,
            "finite_outside_image_count": 6,
            "moving_roots": [6, 8],
            "collision_pair": [6, 7],
            "pole": 0,
            "mutation_count": 4,
            "mutation_rejections": 4,
            "fail_closed_explicit_checks": True,
            "normal_optimized_transcript_parity_required": True,
            "generated_sage_python_is_temporary_build_product": True,
            "mutations": {
                "basepoint": True,
                "common_factor": True,
                "incompatible_labels": True,
                "insufficient_anchors": True,
            },
            "toy_only": True,
            "complete_selector_witness_assignment_constructed": False,
            "rich_beta_J_predicates_constructed": False,
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_CENSUS_OR_PROOF",
        },
        "ledger": {
            "B_star": str(tangent.B_STAR),
            "predecessor_joint_C5_source_mobius_base_cap": str(PREDECESSOR_JOINT_CAP),
            "new_joint_C5_source_rational_base_cap": str(NEW_JOINT_CAP),
            "replacement_not_addition": True,
            "source_rational_uniform_cap": str(SOURCE_RATIONAL_CAP),
            "source_mobius_separate_charge": "0",
            "incremental_ledger_movement": str(LEDGER_MOVEMENT),
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "bounded_degree_full_outside_cell_deleted_before_residual_U_A": True,
            "U_Q": None,
            "residual_U_A": None,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "rank9_gate": {
            "unchanged_from_source_mobius_predecessor": True,
            "predecessor_rank9_updated_gate": copy.deepcopy(mobius_doc["rank9_updated_gate"]),
        },
        "residual_route_cuts": [
            {
                "terminal": HIGH_DEGREE_TERMINAL,
                "condition": (
                    "qualifying full-outside rank-two record survives source-rational owner"
                ),
                "reason": (
                    "e_L>=ceil(s/2), hence s>=36836, e_L>=18418, "
                    "and deg(H_L)<=1030157"
                ),
            },
            {
                "terminal": SOURCE_LOAD_TERMINAL,
                "condition": "non-full-outside and other source-load cells",
                "reason": "the source-rational theorem requires V_sigma INTERSECT Sigma empty",
            },
        ],
        "scope_guards": {
            "adaptive_pair_global_source_rational_owner_proved": True,
            "cross_selector_bounded_degree_slope_union_proved": True,
            "first_match_replacement_splice_proved": True,
            "source_mobius_owner_absorbed": True,
            "full_outside_reduced_degree_below_18418_excluded_from_residual": True,
            "full_outside_survivor_gcd_above_1030157_excluded": True,
            "complete_selector_inventory_required_for_this_cell": False,
            "all_lower_gcd_rational_maps_paid": False,
            "high_reduced_degree_rational_maps_paid": False,
            "non_full_outside_source_load_paid": False,
            "determinant_weighted_incidence_paid": False,
            "U_Q_determined": False,
            "residual_U_A_determined": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": [
            "No alternative SP3 translations or received pairs are unioned.",
            "No per-selector charge is taken and no determinant mass is mixed across selectors.",
            "No pair-global base-field descent is asserted; the common map is over the line field.",
            "No uniqueness among arbitrary-degree rational maps is asserted.",
            "No injectivity of the common rational map is asserted or needed.",
            "No forced locator is substituted for the full monic gcd.",
            "No selector, support, line, chart, basis, witness, or coordinate multiplicity is counted.",
            "No complete-selector inventory or deployed terminal census is invented.",
            "No high-degree or non-full-outside source-load cell is paid.",
            "No exact toy control is promoted to deployed-field evidence or theorem proof.",
            "No new ledger charge is added and no value is assigned to U_Q or residual U_A.",
            "The KoalaBear row remains open.",
            "Rank at least ten, Lean, and stable-paper promotion remain unauthorized.",
        ],
        "source_bindings": expected_source_bindings(),
        "payload_sha256": "",
    }
    result["payload_sha256"] = payload_hash(result)
    _EXPECTED_CACHE = copy.deepcopy(result)
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
    require(set(document) == TOP_KEYS, "top-level key set drift")
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    strict_match(document, expected_certificate())


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("status", lambda d: d.__setitem__("status", "ROW_CLOSED")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("row-k", lambda d: d["row"].__setitem__("k", K - 1)),
        ("predecessor-962", lambda d: d["predecessors"].__setitem__("source_mobius_owner_splice", "payload-sha256:" + "0" * 64)),
        ("predecessor-source-load", lambda d: d["predecessors"].__setitem__("projective_source_load", "payload-sha256:" + "0" * 64)),
        ("predecessor-active-source", lambda d: d["predecessors"].__setitem__("active_source_matroid_reindex", "payload-sha256:" + "0" * 64)),
        ("per-selector-charge", lambda d: d["counted_object_contract"].__setitem__("per_selector_charge_forbidden", False)),
        ("mix-determinant-mass", lambda d: d["counted_object_contract"].__setitem__("determinant_atlas_mass_cross_selector_mixing_forbidden", False)),
        ("infinity-finite", lambda d: d["counted_object_contract"].__setitem__("projective_infinity_is_not_a_finite_slope", False)),
        ("supplement-owner", lambda d: d["counted_object_contract"].__setitem__("new_owner_replaces_not_supplements_source_mobius_owner", False)),
        ("alternative-translation", lambda d: d["pair_global_source_contract"].__setitem__("alternative_translation_union_forbidden", False)),
        ("source-label-zero", lambda d: d["pair_global_source_contract"].__setitem__("source_label_nonzero_on_Sigma", False)),
        ("source-floor", lambda d: d["pair_global_source_contract"].__setitem__("source_anchor_floor", SIGMA_FLOOR - 1)),
        ("vary-source-size", lambda d: d["pair_global_source_contract"].__setitem__("source_size_symbol", "s_L")),
        ("forced-locator", lambda d: d["adaptive_rational_rigidity"].__setitem__("forced_locator_in_place_of_full_gcd_forbidden", False)),
        ("not-coprime", lambda d: d["adaptive_rational_rigidity"].__setitem__("reduced_pair_coprime", False)),
        ("degree-cap-off-one", lambda d: d["adaptive_rational_rigidity"].__setitem__("adaptive_degree_cap", "E(s)=floor(s/2)")),
        ("cross-degree", lambda d: d["adaptive_rational_rigidity"].__setitem__("cross_polynomial_degree_bound", "at most E(s)")),
        ("not-all-anchors", lambda d: d["adaptive_rational_rigidity"].__setitem__("all_source_anchors_are_roots", False)),
        ("cross-not-zero", lambda d: d["adaptive_rational_rigidity"].__setitem__("cross_polynomial_identically_zero", False)),
        ("arbitrary-unique", lambda d: d["adaptive_rational_rigidity"].__setitem__("global_uniqueness_among_arbitrary_degree_maps_claimed", True)),
        ("affine-divide", lambda d: d["adaptive_rational_rigidity"].__setitem__("affine_division_at_source_anchors_forbidden", False)),
        ("no-infinity-label", lambda d: d["adaptive_rational_rigidity"].__setitem__("infinity_source_labels_allowed", False)),
        ("require-injective", lambda d: d["adaptive_rational_rigidity"].__setitem__("injectivity_required", True)),
        ("degree-cap", lambda d: d["adaptive_rational_rigidity"].__setitem__("deployed_uniform_degree_cap", DEPLOYED_DEGREE_CAP + 1)),
        ("next-degree-rigid", lambda d: d["adaptive_rational_rigidity"].__setitem__("next_degree_not_uniformly_rigid", False)),
        ("chosen-selector-map", lambda d: d["source_rational_owner"].__setitem__("owner_is_intrinsic_not_chosen_from_selector", False)),
        ("unqualified-unique", lambda d: d["source_rational_owner"].__setitem__("compatible_map_unique_within_printed_degree_range", False)),
        ("nonempty-incompatible", lambda d: d["source_rational_owner"].__setitem__("nonempty_owner_without_compatible_map_forbidden", False)),
        ("use-all-D", lambda d: d["source_rational_owner"].__setitem__("domain", "D")),
        ("keep-infinity", lambda d: d["source_rational_owner"].__setitem__("projective_infinity_deleted_from_finite_owner", False)),
        ("wrong-owner-cap", lambda d: d["source_rational_owner"].__setitem__("uniform_cap", SOURCE_RATIONAL_CAP + 1)),
        ("no-residual-intersection", lambda d: d["source_rational_owner"].__setitem__("assigned_cell", "Z_SRat=R")),
        ("injective-cap", lambda d: d["source_rational_owner"].__setitem__("collisions_only_reduce_image_size", False)),
        ("no-absorption", lambda d: d["source_rational_owner"].__setitem__("absorbs_predecessor_source_mobius_owner", False)),
        ("second-mobius-charge", lambda d: d["source_rational_owner"].__setitem__("separate_source_mobius_charge", 1)),
        ("no-exact-delete", lambda d: d["source_rational_owner"].__setitem__("later_overlap_deleted_exactly", False)),
        ("same-carrier-required", lambda d: d["cross_selector_containment"].__setitem__("same_carrier_across_selectors_required", True)),
        ("not-full-outside", lambda d: d["cross_selector_containment"].__setitem__("full_outside_each_selector", "V_sigma INTERSECT Sigma nonempty")),
        ("rank-one", lambda d: d["cross_selector_containment"].__setitem__("coefficient_rank_each_line", 1)),
        ("beta-zero", lambda d: d["cross_selector_containment"].__setitem__("contributing_beta_positive", False)),
        ("x-too-large", lambda d: d["cross_selector_containment"].__setitem__("contributing_x_at_most", RICH_X_MAX + 1)),
        ("not-full-gcd", lambda d: d["cross_selector_containment"].__setitem__("full_monic_gcd_used_each_line", False)),
        ("wrong-source-floor", lambda d: d["cross_selector_containment"].__setitem__("source_rank_two_floor_each_line", "s>=t-x_L+1")),
        ("wrong-qualifying-degree", lambda d: d["cross_selector_containment"].__setitem__("qualifying_degree_each_line", "e<=s")),
        ("maps-not-common", lambda d: d["cross_selector_containment"].__setitem__("all_qualifying_maps_common", False)),
        ("root-in-Sigma", lambda d: d["cross_selector_containment"].__setitem__("moving_root_x_in_W_subset_V_subset_D_minus_Sigma", False)),
        ("common-root", lambda d: d["cross_selector_containment"].__setitem__("moving_root_is_not_common_root", False)),
        ("selector-inventory", lambda d: d["cross_selector_containment"].__setitem__("selector_inventory_or_Route_S_U_C_required", True)),
        ("mix-weights", lambda d: d["cross_selector_containment"].__setitem__("determinant_weights_transferred_across_selectors", True)),
        ("no-subset-stability", lambda d: d["cross_selector_containment"].__setitem__("subset_stable_for_every_Gamma_subset_Gamma_in", False)),
        ("no-post-restart-application", lambda d: d["cross_selector_containment"].__setitem__("post_restart_application_to_Gamma_out", False)),
        ("survivor-threshold", lambda d: d["adaptive_residual"].__setitem__("survivor_degree_condition", "e_L>=E(s)")),
        ("degree-upper", lambda d: d["adaptive_residual"].__setitem__("rank_two_reduced_degree_upper_bound", "e_L<=k-1")),
        ("survivor-s", lambda d: d["adaptive_residual"].__setitem__("survivor_source_floor", SURVIVOR_SIGMA_FLOOR - 1)),
        ("survivor-e", lambda d: d["adaptive_residual"].__setitem__("survivor_reduced_degree_floor", SURVIVOR_DEGREE_FLOOR - 1)),
        ("survivor-gcd", lambda d: d["adaptive_residual"].__setitem__("survivor_full_gcd_degree_ceiling", SURVIVOR_GCD_CEILING + 1)),
        ("closed-count", lambda d: d["adaptive_residual"].__setitem__("adaptively_closed_full_gcd_degree_count", ADAPTIVELY_CLOSED_GCD_COUNT - 1)),
        ("residual-terminal", lambda d: d["adaptive_residual"].__setitem__("terminal", "PAID")),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("old-owner-retained", lambda d: d["first_match_partition"].__setitem__("source_mobius_owner_removed_from_order", False)),
        ("owner-index", lambda d: d["first_match_partition"].__setitem__("source_rational_index_one_based", 9)),
        ("later-not-difference", lambda d: d["first_match_partition"].__setitem__("later_owners_receive_exact_set_difference", False)),
        ("sum-cases", lambda d: d["joint_owner_theorem"].__setitem__("case_combination", "SUM")),
        ("rank-zero-nonempty", lambda d: d["joint_owner_theorem"].__setitem__("rank_zero_noncontained_exact_witness_residual_empty", False)),
        ("C5-not-empty", lambda d: d["joint_owner_theorem"].__setitem__("nonbase_case_C5_cell_empty", False)),
        ("source-base-overlap", lambda d: d["joint_owner_theorem"].__setitem__("source_and_later_base_disjoint_by_exact_deletion", False)),
        ("wrong-joint-cap", lambda d: d["joint_owner_theorem"].__setitem__("joint_uniform_cap", str(NEW_JOINT_CAP + 1))),
        ("add-block", lambda d: d["joint_owner_theorem"].__setitem__("adds_independent_joint_block", True)),
        ("not-replacement", lambda d: d["joint_owner_theorem"].__setitem__("replaces_existing_joint_block", False)),
        ("no-selector-restart", lambda d: d["selector_restart"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("stale-selector-fields", lambda d: d["selector_restart"].__setitem__("stale_selector_fields_forbidden", [])),
        ("translation-recomputed", lambda d: d["selector_restart"].__setitem__("same_sp3_translation_required_downstream", False)),
        ("source-not-preserved", lambda d: d["selector_restart"].__setitem__("source_fields_preserved_downstream", [])),
        ("rank10-minimum", lambda d: d["selector_restart"].__setitem__("rank_at_least_10_can_be_new_minimum", True)),
        ("rank-sum", lambda d: d["selector_restart"].__setitem__("rank_caps_are_alternatives_not_sum", False)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("scale", "DEPLOYED_PROOF")),
        ("toy-complete-selector", lambda d: d["exact_control"].__setitem__("complete_selector_witness_assignment_constructed", True)),
        ("toy-four-anchors-rigid", lambda d: d["exact_control"].__setitem__("sharp_anchor_kernel_dimension", 1)),
        ("toy-no-pole", lambda d: d["exact_control"].__setitem__("pole", 1)),
        ("toy-no-collision", lambda d: d["exact_control"].__setitem__("collision_pair", [6, 8])),
        ("toy-mutation", lambda d: d["exact_control"]["mutations"].__setitem__("basepoint", False)),
        ("sage-asserts", lambda d: d["exact_control"].__setitem__("fail_closed_explicit_checks", False)),
        ("sage-no-opt-parity", lambda d: d["exact_control"].__setitem__("normal_optimized_transcript_parity_required", False)),
        ("sage-generated-in-tree", lambda d: d["exact_control"].__setitem__("generated_sage_python_is_temporary_build_product", False)),
        ("ledger-addition", lambda d: d["ledger"].__setitem__("replacement_not_addition", False)),
        ("mobius-charge", lambda d: d["ledger"].__setitem__("source_mobius_separate_charge", "1")),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("incremental_ledger_movement", "1")),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-remaining", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER - 1))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("UA-zero", lambda d: d["ledger"].__setitem__("residual_U_A", 0)),
        ("rank9-gate-changed", lambda d: d["rank9_gate"].__setitem__("unchanged_from_source_mobius_predecessor", False)),
        ("route-paid", lambda d: d["residual_route_cuts"][0].__setitem__("terminal", "PAID")),
        ("all-lower-gcd-paid", lambda d: d["scope_guards"].__setitem__("all_lower_gcd_rational_maps_paid", True)),
        ("high-degree-paid", lambda d: d["scope_guards"].__setitem__("high_reduced_degree_rational_maps_paid", True)),
        ("non-full-outside-paid", lambda d: d["scope_guards"].__setitem__("non_full_outside_source_load_paid", True)),
        ("rank9-closed", lambda d: d["scope_guards"].__setitem__("complete_rank9_payment_proved", True)),
        ("row-closed", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("rank10", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("source-path", lambda d: d["source_bindings"][0].__setitem__("path", d["source_bindings"][1]["path"])),
        ("duplicate-binding", lambda d: d["source_bindings"][1].__setitem__("binding_id", d["source_bindings"][0]["binding_id"])),
        ("payload", lambda d: d.__setitem__("payload_sha256", "1" * 64)),
    ]


def run_parser_tamper_selftest() -> int:
    rejected = 0
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1.5}'):
        try:
            json.loads(
                payload,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_constant,
                parse_float=reject_float,
            )
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"parser mutation survived: {payload}")
    require(rejected == 3, "parser mutation count drift")
    return rejected


def run_tamper_selftest() -> int:
    baseline = expected_certificate()
    validate_certificate(baseline)
    rejected = 0
    for name, mutate in mutation_cases():
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except (ContractError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    parser_rejected = run_parser_tamper_selftest()
    total = rejected + parser_rejected
    require(rejected == len(mutation_cases()), "semantic mutation count drift")
    print(f"M1 source-rational owner mutations: {total}/{total} PASS")
    return 0


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(expected_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_check() -> int:
    document = load_json(CERT_PATH)
    validate_certificate(document)
    print("M1 adaptive source-rational owner splice: PASS")
    print(
        "  adaptive degree cap: E(s)=floor((s-1)/2); "
        f"E({SIGMA_FLOOR:,})={DEPLOYED_DEGREE_CAP:,}"
    )
    print(f"  pair-global finite-image cap unchanged: {SOURCE_RATIONAL_CAP:,}")
    print(f"  joint C5/source/base cap unchanged: {NEW_JOINT_CAP:,}")
    print(f"  incremental ledger movement: {LEDGER_MOVEMENT}")
    print(f"  U_paid unchanged: {U_PAID_AFTER:,}")
    print(f"  B_remaining unchanged: {B_REMAINING_AFTER:,}")
    print(
        "  survivor: "
        f"s>={SURVIVOR_SIGMA_FLOOR:,}, e>={SURVIVOR_DEGREE_FLOOR:,}, "
        f"deg(H)<={SURVIVOR_GCD_CEILING:,}"
    )
    print(f"  terminal paid: {PAID_TERMINAL}")
    print(f"  route cut: {HIGH_DEGREE_TERMINAL}")
    print("  non-full-outside/U_Q/U_A remain open; row YELLOW")
    return 0


def sage_transcript_lines(output: str) -> str:
    prefixes = (
        "SOURCE_RATIONAL_OWNER_CONTROL=",
        "SOURCE_RATIONAL_OWNER_MUTATIONS=",
        "SCALE=",
    )
    lines = [line for line in output.splitlines() if line.startswith(prefixes)]
    require(len(lines) == 3, "Sage replay did not emit exactly three control lines")
    return "\n".join(lines) + "\n"


def expected_sage_transcript(document: dict[str, Any]) -> str:
    exact = document["exact_control"]
    control_keys = (
        "anchor_count",
        "anchor_kernel_dimension",
        "anchor_matrix_rank",
        "collision_pair",
        "common_reduced_degree",
        "distinct_full_gcds",
        "field_order",
        "finite_outside_image_count",
        "moving_roots",
        "mutation_count",
        "mutation_rejections",
        "outside_domain_count",
        "outside_projective_image_count",
        "owner",
        "pole",
        "residual",
        "selector_count",
        "sharp_agreement_count",
        "sharp_anchor_kernel_dimension",
        "status",
        "toy_only",
    )
    control = {key: exact[key] for key in control_keys}
    return (
        "SOURCE_RATIONAL_OWNER_CONTROL="
        + json.dumps(control, sort_keys=True, separators=(",", ":"))
        + "\nSOURCE_RATIONAL_OWNER_MUTATIONS="
        + json.dumps(exact["mutations"], sort_keys=True, separators=(",", ":"))
        + "\nSCALE="
        + exact["scale"]
        + "\n"
    )


def run_sage_parity_check() -> int:
    document = load_json(CERT_PATH)
    validate_certificate(document)
    expected = expected_sage_transcript(document)
    sage_executable = Path("/usr/local/bin/sage")
    require(sage_executable.is_file(), f"missing Sage executable: {sage_executable}")

    with tempfile.TemporaryDirectory(prefix="rs-mca-source-rational-sage-") as tmp:
        temporary_sage = Path(tmp) / SAGE_REL.name
        shutil.copyfile(ROOT / SAGE_REL, temporary_sage)
        env = dict(os.environ)
        env["HOME"] = str(Path(tmp) / "home")
        Path(env["HOME"]).mkdir()

        normal = subprocess.run(
            [str(sage_executable), str(temporary_sage)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        require(normal.returncode == 0, "ordinary Sage replay failed: " + normal.stderr)

        generated_python = temporary_sage.with_name(temporary_sage.name + ".py")
        require(
            generated_python.is_file(),
            "Sage did not emit its temporary Python build product",
        )
        optimized = subprocess.run(
            [str(sage_executable), "-python", "-O", str(generated_python)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        require(
            optimized.returncode == 0,
            "optimized Sage/Python replay failed: " + optimized.stderr,
        )

        normal_transcript = sage_transcript_lines(normal.stdout)
        optimized_transcript = sage_transcript_lines(optimized.stdout)
        require(normal_transcript == expected, "ordinary Sage transcript drift")
        require(optimized_transcript == expected, "optimized Sage transcript drift")
        require(normal_transcript == optimized_transcript, "Sage mode transcript mismatch")

    print("M1 source-rational Sage parity: PASS (ordinary == optimized)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--sage-parity-check", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.sage_parity_check:
        return run_sage_parity_check()
    if args.print_certificate:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return 0
    if args.write:
        write_certificate()
        print(CERT_PATH)
        return 0
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
