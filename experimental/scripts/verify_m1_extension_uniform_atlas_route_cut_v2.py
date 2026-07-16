#!/usr/bin/env python3
"""Verify the M1 A4 fixed-pair and coarse-uniform route cuts.

This packet proves one narrowly scoped negative implication and replays one
inherited budget wall for the deployed KoalaBear MCA row at A=1,116,048:

1. a chart computation for one fixed or sampled received pair cannot be
   promoted to the row-uniform U_A supremum without an all-pairs bridge; and
2. the unrefined fixed-deficiency complete-absorption envelope is already
   larger than the entire row budget, as proved previously at the same
   binomial index; the exact new translation is that its compiler-range
   effective deficiency must fall to at most one before the bare envelope can
   fit.

It does not claim that the actual residual numerator exceeds the budget and it
does not cut a genuinely uniform pair-dependent atlas with a row-sharp bound.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from math import comb
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-extension-uniform-atlas-route-cut-v2"
    / "m1_extension_uniform_atlas_route_cut_v2.json"
)
PREDECESSOR = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-a4-spi-atlas-manifest-v1"
    / "kb_mca_a1116048_base_generated_family.json"
)
CURRENT_LEDGER = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "kb-mca-1116048-base-slope-universe-v2"
    / "kb_mca_1116048_base_slope_universe_v2.json"
)

P = 2_130_706_433
E = 6
N = 2_097_152
K = 1_048_576
A = 1_116_048
J = N - A
T_SYNDROME = A - K
W = T_SYNDROME - 1
KERNEL_LOWER = J + 1 - T_SYNDROME
TAU_ERROR = N - A
DEFICIENCY = N + K - 2 * A
Q = P**E
B_STAR = Q // (2**128)
U_PAID = 2_602_153_473
B_REMAINING = B_STAR - U_PAID
LOWER_INDEX = 3
COARSE_LOWER = comb(N, LOWER_INDEX)

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "first-match-uniform-contract": {
        "path": "experimental/grande_finale.tex",
        "sha256": "4e3c3f6a898969e5fad70cd09bf354c6a2a12d54bf94525fb62f457dd17ddbc8",
        "anchors": [
            r"\label{lem:first-match-ledger}",
            "If every received line admits a first-match upper ledger",
            "Taking the maximum over received lines gives",
        ],
    },
    "capf-a4-and-active-contracts": {
        "path": "experimental/cap25_cap_v13_raw.tex",
        "sha256": "d0a9a766c4218b3faa355fd4da9ebb4937dcd3c9bbf7b94cecc273c5e502d746",
        "anchors": [
            r"\label{thm:capf-spi}",
            "and assume $t=j$",
            r"\sup_{f,g}\bigl|\Bad_{\rm ap}^{\rm M1}(f,g;a_0+1)\bigr|",
            "A4. Finite SPI atlas route.",
            "The theorem does not classify higher-deficiency SPI charts",
            r"\label{prob:capg-active-BC}",
            "Prove, for every line at band agreements",
        ],
    },
    "paper-d-chart-status": {
        "path": "tex/cs25_cap_v12.tex",
        "sha256": "8b988dd2091b46ab37b5c8c78735369e3e7849a8f89fb6739480b7b0d4859dc5",
        "anchors": [
            "It does not claim",
            "Assume that the chart families $\\mathfrak R_A$, for $A\\ge a$, cover every",
            "for this row, uniformly in the received line",
            "It does not prove the aperiodic upper input",
            "What separates the sandwich from a one-step determination is precisely Open Problem",
        ],
    },
    "fixed-deficiency-theorem": {
        "path": "experimental/notes/thresholds/fixed_deficiency_complete_absorption.md",
        "sha256": "d096a7f5e6399a51132d404347bbb4e8ab992fce53387c1dd407e4dd263b8403",
        "anchors": [
            "|P|<=binom(N,d+1)",
            "B_C^MCA(a)<=binom(N,d+1)",
            "d=2t-R=n+K-2a",
            "survives arbitrary first-match",
            "When `d` grows linearly",
        ],
    },
    "fixed-deficiency-verifier": {
        "path": "experimental/scripts/verify_fixed_deficiency_complete_absorption.py",
        "sha256": "d8893de74f9a05eab38e8f5c2ae3bd6390236ad61eb0e76007a3adc4efbba616",
        "anchors": [
            "complete_all_pair_bound",
            "mca_ca_numerator_bound",
            "tamper-selftest",
        ],
    },
    "fixed-deficiency-certificate": {
        "path": "experimental/data/certificates/fixed-deficiency-complete-absorption/fixed_deficiency_complete_absorption.json",
        "sha256": "85ae5257bb861e31b9ec4f197df13476cd56b29e068c806c37cac40c4914c3e9",
        "anchors": [
            '"complete_all_pair_bound": "|P|<=binom(N,d+1)"',
            '"mca_ca_numerator_bound": "B_MCA,B_CA<=binom(N,d+1)"',
        ],
    },
    "current-base-slope-ledger-note": {
        "path": "experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md",
        "sha256": "265d2fcfc5a55dc7c0e7e6bed5f0f32b6b2ab86638441dbed09b2641cec6b14c",
        "anchors": [
            "corrected proved paid baseline",
            "p + 471447040 = 2602153473",
            "B_rem             = 274980725509241614",
        ],
    },
    "current-base-slope-ledger-verifier": {
        "path": "experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py",
        "sha256": "a860cbd3bd48466ae1ce61e3668ac8aaf2b4453f89731c6c6ab5e5de41ebb579",
        "anchors": [
            "OLD_U_PAID",
            '"new_U_paid"',
            '"B_rem"',
        ],
    },
    "current-base-slope-ledger-certificate": {
        "path": "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/kb_mca_1116048_base_slope_universe_v2.json",
        "sha256": "ffefb3aa56645d06fa14c805c9d8e9b503359fe2e094566b5fb209e8cbe8bece",
        "anchors": [
            '"new_U_paid": "2602153473"',
            '"B_rem": "274980725509241614"',
            '"U_A": null',
        ],
    },
    "prior-saturated-bc-budget-note": {
        "path": "experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md",
        "sha256": "bfb53b596c44ee867b7ab77454c784ef7db412980675c613ee8133ea6a56e4d4",
        "anchors": [
            "fits iff `d<=2`",
            "`C(n,omega-w)`",
            "`2^2072017.7` does not fit",
            "only the interior `d1 >= w+2` growing-deficiency class",
        ],
    },
    "prior-saturated-bc-budget-verifier": {
        "path": "experimental/scripts/verify_saturated_bc_budget_fit.py",
        "sha256": "c005d381514ef328977ac6de8a9fd6efff5bd27ea44c2c4bd994acdece355544",
        "anchors": [
            "math.comb(2^21, 913633)",
            "gate ii -- P2 fixed-deficiency arithmetic + growing-deficiency miss",
            "log2_fixeddim=2072017.7",
        ],
    },
    "prior-saturated-bc-budget-certificate": {
        "path": "experimental/data/certificates/frontier-adjacent/saturated_bc_budget_fit_v1.json",
        "sha256": "f6b1cec423f18c05651eb4a2e057e2d660b0a6f1374e59243477b714b380c036",
        "anchors": [
            '"thm:capf-fixeddim (raw L6735)": "C(n, omega-w)"',
            '"dim_W": 913634, "log2_fixeddim_bound": 2072017.7',
            '"miss_fixeddim_bits": 2072018',
        ],
    },
    "route-cut-human-note": {
        "path": "experimental/notes/m1/m1_extension_uniform_atlas_route_cut_v2.md",
        "sha256": "0684ce6302f4e56eb7968bff772cf66994bcc9ad03baed750c64ef9f74ab793e",
        "anchors": [
            r"U_{\mathrm{paid}}=2{,}602{,}153{,}473",
            "=274{,}980{,}725{,}509{,}241{,}614.",
            r"1\le d_{\mathrm{eff}}<\tau=981{,}104<\frac n2=1{,}048{,}576,",
            "INHERITED_ROUTE_CUT_UNREFINED_COMPLETE_ABSORPTION_ENVELOPE_AT_LINEAR_DEFICIENCY.",
        ],
    },
}

EXPECTED_EDGE_CASES = [
    "A common pair-independent atlas is sufficient but not necessary; pair-dependent atlases with one uniform maximum are allowed.",
    "A first-match deletion may make the actual residual much smaller than the complete-absorption envelope.",
    "The two symbols called t in the SPI and fixed-deficiency sources are separated here as syndrome_depth_t and error_budget_tau.",
    "The d_eff<=1 conclusion is restricted to 1<=d_eff<tau=981104<n/2, where the relevant binomial indices are increasing.",
    "Extension-valued slopes and raw support coverage remain outside the predecessor manifest.",
]
EXPECTED_REMAINING_RISKS = [
    "The fixed-deficiency theorem is consumed at its repository status PROVED / AUDIT and remains subject to independent proof review.",
    "A row-sharp exact root union or effective-deficiency theorem could revive the atlas route without contradicting this cut.",
    "The quotient term U_Q is still null, so closing U_A alone would not finish the adjacent row.",
]
EXPECTED_NONCLAIMS = [
    "The abstract two-pair countermodel is not a Reed-Solomon counterexample.",
    "The coarse budget miss is inherited from the prior saturated-BC packet and is not claimed as new here.",
    "The packet does not prove that the actual KoalaBear residual numerator exceeds B_star.",
    "The packet does not cut a complete pair-dependent atlas with a proved row-uniform maximum.",
    "The packet does not prove an effective-deficiency collapse or a base-field-normalized split-pencil census.",
    "The packet does not assign a numeric U_A, change the ledger, close the row, or improve the public frontier.",
    "The GF(19) atlas remains machinery control only.",
]


class CertificateError(AssertionError):
    """Raised for any fail-closed certificate violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def require_int(value: Any, label: str) -> None:
    require(type(value) is int, f"{label} is not an exact JSON integer")


def require_string(value: Any, label: str) -> None:
    require(type(value) is str, f"{label} is not a JSON string")


def reject_constant(value: str) -> None:
    raise CertificateError(f"nonstandard JSON constant: {value}")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path.relative_to(REPO)}")
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    require(isinstance(value, dict), "top-level JSON value is not an object")
    return value


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    require(set(value) == expected, f"{label} keys drift: {sorted(set(value) ^ expected)}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def payload_sha256(certificate: dict[str, Any]) -> str:
    payload = copy.deepcopy(certificate)
    payload.pop("payload_sha256", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_sources(certificate: dict[str, Any]) -> None:
    bindings = certificate["source_bindings"]
    require(isinstance(bindings, list), "source_bindings is not a list")
    by_id: dict[str, dict[str, Any]] = {}
    for binding in bindings:
        require(isinstance(binding, dict), "source binding is not an object")
        exact_keys(binding, {"binding_id", "path", "sha256", "anchors"}, "source binding")
        binding_id = binding["binding_id"]
        require(isinstance(binding_id, str), "source binding id is not a string")
        require(binding_id not in by_id, f"duplicate source binding: {binding_id}")
        by_id[binding_id] = binding

    require(set(by_id) == set(SOURCE_SPECS), "source binding set drift")
    for binding_id, expected in SOURCE_SPECS.items():
        binding = by_id[binding_id]
        require(binding["path"] == expected["path"], f"{binding_id}: path drift")
        require(binding["sha256"] == expected["sha256"], f"{binding_id}: declared hash drift")
        require(binding["anchors"] == expected["anchors"], f"{binding_id}: anchor list drift")
        path = REPO / binding["path"]
        require(path.is_file(), f"{binding_id}: missing source")
        require(sha256_file(path) == binding["sha256"], f"{binding_id}: live source hash drift")
        text = path.read_text(encoding="utf-8")
        for anchor in binding["anchors"]:
            require(anchor in text, f"{binding_id}: missing source anchor {anchor!r}")


def validate_row(row: dict[str, Any]) -> None:
    exact_keys(
        row,
        {
            "row_id",
            "p",
            "extension_degree",
            "q",
            "n",
            "k",
            "agreement_A",
            "error_count_j",
            "syndrome_depth_t",
            "prefix_depth_w",
            "kernel_dimension_lower_bound",
            "B_star",
            "U_paid",
            "B_remaining",
        },
        "row",
    )
    for key in (
        "p",
        "extension_degree",
        "n",
        "k",
        "agreement_A",
        "error_count_j",
        "syndrome_depth_t",
        "prefix_depth_w",
        "kernel_dimension_lower_bound",
    ):
        require_int(row[key], f"row.{key}")
    for key in ("row_id", "q", "B_star", "U_paid", "B_remaining"):
        require_string(row[key], f"row.{key}")
    require(row["row_id"] == "koalabear-mca-A1116048", "row id drift")
    require(row["p"] == P and row["extension_degree"] == E, "field parameters drift")
    require(int(row["q"]) == Q, "extension-field size drift")
    require(row["n"] == N and row["k"] == K and row["agreement_A"] == A, "row arithmetic drift")
    require(row["error_count_j"] == N - A == J, "j arithmetic drift")
    require(row["syndrome_depth_t"] == A - K == T_SYNDROME, "syndrome t arithmetic drift")
    require(row["prefix_depth_w"] == T_SYNDROME - 1 == W, "w arithmetic drift")
    require(
        row["kernel_dimension_lower_bound"] == J + 1 - T_SYNDROME == KERNEL_LOWER,
        "kernel lower bound drift",
    )
    require(int(row["B_star"]) == B_STAR, "B_star drift")
    require(int(row["U_paid"]) == U_PAID, "U_paid drift")
    require(int(row["B_remaining"]) == B_STAR - U_PAID == B_REMAINING, "remaining budget drift")


def validate_predecessor(guard: dict[str, Any]) -> None:
    exact_keys(
        guard,
        {
            "path",
            "sha256",
            "artifact_kind",
            "status",
            "represented_units",
            "row_complete",
            "uniformity",
            "excluded_scope_count",
            "historical_U_paid",
            "paid_baseline_status",
            "U_Q",
            "U_A",
        },
        "predecessor_guard",
    )
    expected_path = str(PREDECESSOR.relative_to(REPO))
    require_int(guard["represented_units"], "predecessor_guard.represented_units")
    require_int(guard["excluded_scope_count"], "predecessor_guard.excluded_scope_count")
    require(guard["path"] == expected_path, "predecessor path drift")
    require(guard["sha256"] == sha256_file(PREDECESSOR), "predecessor hash drift")
    predecessor = load_json(PREDECESSOR)
    require(guard["artifact_kind"] == predecessor["artifact_kind"] == "DEPLOYED_PARTIAL_MANIFEST", "predecessor kind drift")
    require(guard["status"] == predecessor["status"] == "PARTIAL", "predecessor status drift")
    require(guard["represented_units"] == predecessor["coverage"]["represented_units"] == 0, "predecessor represented charts drift")
    require(guard["row_complete"] is predecessor["coverage"]["row_complete"] is False, "predecessor completion drift")
    require(guard["uniformity"] == predecessor["quantifier_scope"]["uniformity"], "predecessor uniformity drift")
    require(
        guard["excluded_scope_count"] == len(predecessor["quantifier_scope"]["excluded_scopes"]) == 3,
        "predecessor excluded-scope count drift",
    )
    require(guard["historical_U_paid"] == predecessor["ledger"]["U_paid"] == "143763495894416", "historical predecessor baseline drift")
    require(guard["paid_baseline_status"] == "SUPERSEDED_BY_KB_BASE_SLOPE_UNIVERSE_V2", "historical baseline not marked superseded")
    require(guard["U_Q"] is predecessor["ledger"]["U_Q"] is None, "predecessor U_Q overclaim")
    require(guard["U_A"] is predecessor["ledger"]["U_A"] is None, "predecessor U_A overclaim")


def validate_current_ledger(guard: dict[str, Any]) -> None:
    exact_keys(
        guard,
        {"path", "sha256", "status", "new_U_paid", "B_rem", "U_Q", "U_A", "inequality_status"},
        "current_ledger_guard",
    )
    expected_path = str(CURRENT_LEDGER.relative_to(REPO))
    require(guard["path"] == expected_path, "current ledger path drift")
    require(guard["sha256"] == sha256_file(CURRENT_LEDGER), "current ledger hash drift")
    current = load_json(CURRENT_LEDGER)
    arithmetic = current["arithmetic"]
    require(guard["status"] == current["status"] == "PROVED_UPPER_NUMERATOR_REPLACEMENT", "current ledger status drift")
    require(guard["new_U_paid"] == arithmetic["new_U_paid"] == str(U_PAID), "current U_paid drift")
    require(guard["B_rem"] == arithmetic["B_rem"] == str(B_REMAINING), "current B_rem drift")
    require(guard["U_Q"] is arithmetic["U_Q"] is None, "current U_Q overclaim")
    require(guard["U_A"] is arithmetic["U_A"] is None, "current U_A overclaim")
    require(guard["inequality_status"] == arithmetic["inequality_status"] == "UNDECIDED_OPEN_COMPONENTS", "current inequality status drift")


def validate_quantifier_cut(cut: dict[str, Any]) -> None:
    exact_keys(
        cut,
        {
            "row_contract",
            "local_atlas_scope",
            "within_pair_aggregation",
            "across_pair_aggregation",
            "bridge_kind",
            "bridge_status",
            "bridge_theorem_binding_id",
            "all_pairs_covered",
            "all_supports_covered",
            "base_and_extension_slopes_covered",
            "earlier_owner_complement_preserved",
            "first_match_disjointness_preserved",
            "uniform_bound",
            "bankable_as_U_A",
            "logical_countermodel",
            "sufficient_bridge_alternatives",
            "decision",
        },
        "quantifier_cut",
    )
    require(cut["row_contract"] == "SUPREMUM_OVER_ALL_ADMISSIBLE_RECEIVED_PAIRS", "row quantifier drift")
    require(cut["local_atlas_scope"] == "ONE_FIXED_OR_FINITE_SAMPLED_PAIR_SET", "local scope overclaim")
    require(cut["within_pair_aggregation"] == "DISJOINT_FIRST_MATCH_SUM_OR_EXACT_ROOT_UNION", "within-pair aggregation drift")
    require(cut["across_pair_aggregation"] == "SUPREMUM_OR_MAXIMUM", "across-pair aggregation drift")
    require(cut["bridge_kind"] == "ABSENT", "current packet invents a quantifier bridge")
    require(cut["bridge_status"] == "NOT_SUPPLIED_IN_AUDITED_SOURCES", "bridge status drift")
    require(cut["bridge_theorem_binding_id"] is None, "absent bridge has provenance")
    require(cut["all_pairs_covered"] is False, "fixed-pair packet claims all-pair coverage")
    require(cut["all_supports_covered"] is False, "fixed-pair packet claims all-support coverage")
    require(cut["base_and_extension_slopes_covered"] is False, "fixed-pair packet claims extension coverage")
    require(cut["earlier_owner_complement_preserved"] is False, "fixed-pair packet claims owner-complement proof")
    require(cut["first_match_disjointness_preserved"] is False, "fixed-pair packet claims first-match proof")
    require(cut["uniform_bound"] is None and cut["bankable_as_U_A"] is False, "fixed-pair charge banked")

    model = cut["logical_countermodel"]
    exact_keys(
        model,
        {
            "degree_bound_D",
            "sampled_pair_bad_set",
            "unseen_pair_bad_set",
            "sampled_bound_holds",
            "row_supremum",
            "row_bound_conclusion_holds",
            "semantics",
        },
        "logical_countermodel",
    )
    require_int(model["degree_bound_D"], "logical_countermodel.degree_bound_D")
    require(model["degree_bound_D"] == 1, "countermodel D drift")
    sampled = model["sampled_pair_bad_set"]
    unseen = model["unseen_pair_bad_set"]
    require(isinstance(sampled, list) and all(type(value) is int for value in sampled), "sampled countermodel set is not an integer list")
    require(isinstance(unseen, list) and all(type(value) is int for value in unseen), "unseen countermodel set is not an integer list")
    require_int(model["row_supremum"], "logical_countermodel.row_supremum")
    require(sampled == [0] and unseen == [0, 1], "countermodel sets drift")
    require(len(sampled) <= model["degree_bound_D"], "countermodel sampled premise false")
    require(model["sampled_bound_holds"] is True, "countermodel premise flag drift")
    require(model["row_supremum"] == max(len(sampled), len(unseen)) == 2, "countermodel supremum drift")
    require(model["row_bound_conclusion_holds"] is False, "countermodel conclusion overclaim")
    require(model["semantics"] == "ABSTRACT_QUANTIFIER_COUNTERMODEL_NOT_AN_RS_COUNTEREXAMPLE", "countermodel semantics drift")
    require(
        cut["sufficient_bridge_alternatives"]
        == [
            "UNIFORM_BOUND_FOR_A_COMPLETE_PAIR_DEPENDENT_ATLAS_FOR_EVERY_PAIR",
            "EXHAUSTIVE_CANONICAL_REDUCTION_WITH_MAXIMUM_TYPE_BOUND",
        ],
        "sufficient bridge alternatives drift",
    )
    require(cut["decision"] == "ROUTE_CUT_FIXED_OR_SAMPLED_PAIR_AS_U_A_CERTIFICATE", "quantifier decision drift")


def validate_shape_cut(cut: dict[str, Any]) -> None:
    exact_keys(
        cut,
        {
            "capf_spi_shape_assumption",
            "deployed_matrix_rows",
            "deployed_matrix_columns",
            "deployed_generic_kernel_lower_bound",
            "direct_capf_spi_applicable",
            "higher_deficiency_adapter_binding_id",
            "deep_uniform_condition",
            "deep_uniform_lhs",
            "deep_uniform_rhs",
            "deep_uniform_applicable",
            "decision",
        },
        "shape_cut",
    )
    for key in (
        "deployed_matrix_rows",
        "deployed_matrix_columns",
        "deployed_generic_kernel_lower_bound",
        "deep_uniform_lhs",
        "deep_uniform_rhs",
    ):
        require_int(cut[key], f"shape_cut.{key}")
    require(cut["capf_spi_shape_assumption"] == "t_equals_j_DEFICIENCY_ONE", "SPI hypothesis drift")
    require(cut["deployed_matrix_rows"] == T_SYNDROME, "deployed row count drift")
    require(cut["deployed_matrix_columns"] == J + 1, "deployed column count drift")
    require(cut["deployed_generic_kernel_lower_bound"] == KERNEL_LOWER, "deployed kernel dimension drift")
    require(cut["direct_capf_spi_applicable"] is (T_SYNDROME == J) is False, "direct SPI applicability overclaim")
    require(cut["higher_deficiency_adapter_binding_id"] is None, "invented high-deficiency adapter")
    require(cut["deep_uniform_condition"] == "3(n-A)_less_than_or_equal_to_n-k", "deep condition drift")
    require(cut["deep_uniform_lhs"] == 3 * (N - A), "deep lhs drift")
    require(cut["deep_uniform_rhs"] == N - K, "deep rhs drift")
    require(cut["deep_uniform_applicable"] is ((3 * (N - A)) <= (N - K)) is False, "deep theorem applicability overclaim")
    require(cut["decision"] == "DIRECT_DEFICIENCY_ONE_AND_DEEP_UNIFORM_IMPORTS_INAPPLICABLE", "shape decision drift")


def validate_coarse_uniform_cut(cut: dict[str, Any]) -> None:
    exact_keys(
        cut,
        {
            "source_status",
            "all_line_all_field_bound",
            "survives_arbitrary_first_match_deletion",
            "error_budget_tau",
            "deficiency_d",
            "binomial_index_d_plus_1",
            "compiler_hypotheses_hold",
            "unimodality_lower_index",
            "unimodality_lower_bound",
            "binom_n_2",
            "binom_n_2_fits_remaining_budget",
            "B_star",
            "B_remaining_after_U_paid",
            "lower_bound_excess_over_B_star",
            "unrefined_bound_fits_B_star",
            "unrefined_bound_fits_remaining_budget",
            "effective_deficiency_range",
            "tau_strictly_below_n_over_2",
            "binom_n_2_le_B_remaining_lt_binom_n_3",
            "max_unrefined_effective_deficiency_in_compiler_range_that_can_fit",
            "required_effective_deficiency_collapse",
            "prior_budget_wall_binding_ids",
            "index_translation",
            "novelty_scope",
            "decision",
            "live_refinements",
        },
        "coarse_uniform_cut",
    )
    for key in (
        "error_budget_tau",
        "deficiency_d",
        "binomial_index_d_plus_1",
        "unimodality_lower_index",
        "max_unrefined_effective_deficiency_in_compiler_range_that_can_fit",
    ):
        require_int(cut[key], f"coarse_uniform_cut.{key}")
    require(cut["source_status"] == "CONSUMED_AT_REPOSITORY_STATUS_PROVED_AUDIT", "fixed-deficiency theorem status drift")
    require(cut["all_line_all_field_bound"] == "B_MCA(A)_less_than_or_equal_to_binom(n,d+1)", "coarse theorem statement drift")
    require(cut["survives_arbitrary_first_match_deletion"] is True, "first-match stability drift")
    require(cut["error_budget_tau"] == TAU_ERROR, "error budget drift")
    require(cut["deficiency_d"] == DEFICIENCY, "fixed-deficiency d drift")
    require(cut["binomial_index_d_plus_1"] == DEFICIENCY + 1, "binomial index drift")
    hypotheses = K + 1 <= A <= (N + K - 1) // 2 and 1 <= DEFICIENCY < TAU_ERROR
    require(cut["compiler_hypotheses_hold"] is hypotheses is True, "compiler hypotheses drift")
    index = cut["binomial_index_d_plus_1"]
    require(LOWER_INDEX <= index <= N - LOWER_INDEX, "unimodality range fails")
    require(cut["unimodality_lower_index"] == LOWER_INDEX, "unimodality lower index drift")
    require(cut["unimodality_lower_bound"] == str(COARSE_LOWER), "coarse lower bound drift")
    require(int(cut["binom_n_2"]) == comb(N, 2), "binom(n,2) drift")
    require(cut["binom_n_2_fits_remaining_budget"] is (comb(N, 2) <= B_REMAINING) is True, "binom(n,2) fit drift")
    require(int(cut["B_star"]) == B_STAR, "coarse B_star drift")
    require(int(cut["B_remaining_after_U_paid"]) == B_REMAINING, "coarse remaining budget drift")
    require(
        int(cut["lower_bound_excess_over_B_star"]) == COARSE_LOWER - B_STAR > 0,
        "coarse budget excess drift",
    )
    require(COARSE_LOWER > B_STAR > B_REMAINING >= 0, "coarse route-cut inequalities fail")
    require(cut["unrefined_bound_fits_B_star"] is False, "unrefined bound falsely fits full budget")
    require(cut["unrefined_bound_fits_remaining_budget"] is False, "unrefined bound falsely fits remaining budget")
    require(cut["effective_deficiency_range"] == "1_le_d_eff_lt_tau_equals_981104_lt_n_over_2", "effective-deficiency range drift")
    require(cut["tau_strictly_below_n_over_2"] is (TAU_ERROR < N // 2) is True, "tau half-range gate drift")
    require(cut["binom_n_2_le_B_remaining_lt_binom_n_3"] is (comb(N, 2) <= B_REMAINING < COARSE_LOWER) is True, "binomial threshold gate drift")
    require(cut["max_unrefined_effective_deficiency_in_compiler_range_that_can_fit"] == 1, "effective-deficiency wall drift")
    require(cut["required_effective_deficiency_collapse"] == "913632_to_at_most_1", "required collapse drift")
    require(
        cut["prior_budget_wall_binding_ids"]
        == [
            "prior-saturated-bc-budget-note",
            "prior-saturated-bc-budget-verifier",
            "prior-saturated-bc-budget-certificate",
        ],
        "prior budget-wall provenance drift",
    )
    require(cut["index_translation"] == "complete_absorption_d_plus_1_equals_prior_BC_omega_minus_w_equals_913633", "budget-wall index translation drift")
    require(cut["novelty_scope"] == "INHERITED_BUDGET_MISS_WITH_EXACT_D_EFF_LE_1_COROLLARY", "budget-wall novelty overclaim")
    require(
        cut["decision"] == "INHERITED_ROUTE_CUT_UNREFINED_COMPLETE_ABSORPTION_ENVELOPE_AT_LINEAR_DEFICIENCY",
        "coarse route decision drift",
    )
    require(
        cut["live_refinements"]
        == [
            "PROVE_FIRST_MATCH_EFFECTIVE_DEFICIENCY_COLLAPSE",
            "COMPUTE_A_SOURCE_PROVED_EXACT_ROOT_UNION_SMALLER_THAN_THE_BINOMIAL_ENVELOPE",
            "PROVE_THE_ACTIVE_BASE_FIELD_NORMALIZED_SPLIT_PENCIL_CENSUS",
        ],
        "live refinement list drift",
    )


def validate_route_decision(decision: dict[str, Any]) -> None:
    exact_keys(
        decision,
        {
            "route_status",
            "full_A4_status",
            "closure_status",
            "U_A",
            "row_complete",
            "ledger_consequence",
            "next_attack",
            "pr_worthy_if_independently_reviewed",
        },
        "route_decision",
    )
    require(decision["route_status"] == "PROVED_QUANTIFIER_ROUTE_CUT_PLUS_INHERITED_BUDGET_WALL", "route status drift")
    require(decision["full_A4_status"] == "OPEN_ONLY_WITH_A_ROW_UNIFORM_STRUCTURAL_REFINEMENT", "full A4 overclaim")
    require(decision["closure_status"] == "ROW_OPEN", "row closure overclaim")
    require(decision["U_A"] is None, "route cut invents U_A")
    require(decision["row_complete"] is False, "route cut claims row completeness")
    require(decision["ledger_consequence"] is False, "route cut changes the ledger")
    require(
        decision["next_attack"]
        == "EFFECTIVE_DEFICIENCY_OR_OWNER_COLLAPSE_THEN_UNIFORM_MAX_BOUND",
        "next attack drift",
    )
    require(decision["pr_worthy_if_independently_reviewed"] is True, "route-cut PR status drift")


def validate_audit_sections(sections: dict[str, Any]) -> None:
    exact_keys(
        sections,
        {
            "parameter_dependence",
            "layer_cake_dyadic_summability",
            "moment_markov_chebyshev",
            "edge_cases",
            "numerical_evidence",
            "remaining_risks",
        },
        "audit_sections",
    )
    require(sections["parameter_dependence"] == "QUANTIFIER_CUT_PARAMETER_FREE_COARSE_CUT_ROW_SPECIFIC", "parameter dependence drift")
    require(sections["layer_cake_dyadic_summability"] == "NOT_APPLICABLE", "layer-cake status drift")
    require(sections["moment_markov_chebyshev"] == "NOT_APPLICABLE", "moment status drift")
    require(sections["numerical_evidence"] == "NONE_EXACT_INTEGER_AND_LOGICAL_CHECKS_ONLY", "evidence status drift")
    require(sections["edge_cases"] == EXPECTED_EDGE_CASES, "edge-case caveats drift")
    require(sections["remaining_risks"] == EXPECTED_REMAINING_RISKS, "remaining-risk caveats drift")
    require(all(type(item) is str for item in sections["edge_cases"]), "edge cases contain a non-string")
    require(all(type(item) is str for item in sections["remaining_risks"]), "remaining risks contain a non-string")


def validate(certificate: dict[str, Any], *, check_payload: bool = True) -> None:
    exact_keys(
        certificate,
        {
            "schema_version",
            "artifact_kind",
            "status",
            "statement_audited",
            "row",
            "source_bindings",
            "predecessor_guard",
            "current_ledger_guard",
            "quantifier_cut",
            "shape_cut",
            "coarse_uniform_cut",
            "route_decision",
            "audit_sections",
            "nonclaims",
            "payload_sha256",
        },
        "certificate",
    )
    require_int(certificate["schema_version"], "schema_version")
    require(certificate["schema_version"] == 2, "schema version drift")
    require(certificate["artifact_kind"] == "M1_EXTENSION_UNIFORM_ATLAS_ROUTE_CUT_V2", "artifact kind drift")
    require(certificate["status"] == "PROVED_ROUTE_CUT_ROW_OPEN", "status drift")
    require(
        certificate["statement_audited"]
        == "FIXED_OR_SAMPLED_PAIR_ATLAS_AND_UNREFINED_COMPLETE_ABSORPTION_AS_DEPLOYED_U_A_CERTIFICATES",
        "audited statement drift",
    )
    validate_row(certificate["row"])
    validate_sources(certificate)
    validate_predecessor(certificate["predecessor_guard"])
    validate_current_ledger(certificate["current_ledger_guard"])
    validate_quantifier_cut(certificate["quantifier_cut"])
    validate_shape_cut(certificate["shape_cut"])
    validate_coarse_uniform_cut(certificate["coarse_uniform_cut"])
    validate_route_decision(certificate["route_decision"])
    validate_audit_sections(certificate["audit_sections"])
    require(certificate["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims drift")
    require(all(type(item) is str for item in certificate["nonclaims"]), "nonclaims contain a non-string")
    if check_payload:
        require(certificate["payload_sha256"] == payload_sha256(certificate), "payload hash drift")


def expect_reject(name: str, candidate: dict[str, Any]) -> None:
    try:
        validate(candidate)
    except (CertificateError, KeyError, TypeError, ValueError):
        return
    raise CertificateError(f"tamper accepted: {name}")


def run_tamper_selftest(certificate: dict[str, Any]) -> int:
    cases: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(certificate)
        target: Any = candidate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        candidate["payload_sha256"] = payload_sha256(candidate)
        cases.append((name, candidate))

    mutate("fixed-to-uniform-without-bridge", ("quantifier_cut", "local_atlas_scope"), "ALL_RECEIVED_PAIRS")
    mutate("sample-marked-all-pairs", ("quantifier_cut", "all_pairs_covered"), True)
    mutate("absent-bridge-promoted", ("quantifier_cut", "bridge_kind"), "UNIFORM_PER_PAIR_BOUND")
    mutate("invented-bridge-source", ("quantifier_cut", "bridge_theorem_binding_id"), "capf-a4-and-active-contracts")
    mutate("local-bound-banked", ("quantifier_cut", "uniform_bound"), "1")
    mutate("bankable-fixed-pair", ("quantifier_cut", "bankable_as_U_A"), True)
    mutate("average-across-pairs", ("quantifier_cut", "across_pair_aggregation"), "AVERAGE")
    mutate("nondisjoint-within-pair", ("quantifier_cut", "within_pair_aggregation"), "RAW_OVERLAPPING_SUM")
    mutate("extension-coverage-invented", ("quantifier_cut", "base_and_extension_slopes_covered"), True)
    mutate("countermodel-supremum", ("quantifier_cut", "logical_countermodel", "row_supremum"), 1)
    mutate("countermodel-bool-bound", ("quantifier_cut", "logical_countermodel", "degree_bound_D"), True)
    mutate("countermodel-bool-sets", ("quantifier_cut", "logical_countermodel", "sampled_pair_bad_set"), [False])
    mutate("deficiency-one-overclaim", ("shape_cut", "direct_capf_spi_applicable"), True)
    mutate("invented-high-deficiency-adapter", ("shape_cut", "higher_deficiency_adapter_binding_id"), "capf-a4-and-active-contracts")
    mutate("deep-import-overclaim", ("shape_cut", "deep_uniform_applicable"), True)
    mutate("coarse-bound-fits", ("coarse_uniform_cut", "unrefined_bound_fits_B_star"), True)
    mutate("coarse-lower-bound-drift", ("coarse_uniform_cut", "unimodality_lower_bound"), str(COARSE_LOWER - 1))
    mutate("effective-deficiency-wall-drift", ("coarse_uniform_cut", "max_unrefined_effective_deficiency_in_compiler_range_that_can_fit"), 2)
    mutate("budget-wall-novelty-overclaim", ("coarse_uniform_cut", "novelty_scope"), "NEW_BUDGET_WALL")
    mutate("U_A-null-to-zero", ("route_decision", "U_A"), "0")
    mutate("row-complete-overclaim", ("route_decision", "row_complete"), True)
    mutate("ledger-consequence-overclaim", ("route_decision", "ledger_consequence"), True)
    mutate("source-hash-drift", ("source_bindings", 0, "sha256"), "0" * 64)
    mutate("human-note-binding-drift", ("source_bindings", len(SOURCE_SPECS) - 1, "sha256"), "0" * 64)
    mutate("predecessor-uniformity-overclaim", ("predecessor_guard", "uniformity"), "PROVED_ROW_UNIFORM")
    mutate("predecessor-bool-represented", ("predecessor_guard", "represented_units"), False)
    mutate("current-ledger-U-paid-drift", ("current_ledger_guard", "new_U_paid"), str(U_PAID + 1))
    mutate("effective-deficiency-bool", ("coarse_uniform_cut", "max_unrefined_effective_deficiency_in_compiler_range_that_can_fit"), True)
    mutate("erase-edge-caveats", ("audit_sections", "edge_cases"), ["none", "none", "none", "none"])
    mutate("erase-risk-caveats", ("audit_sections", "remaining_risks"), ["none", "none", "none"])
    mutate("erase-nonclaims", ("nonclaims",), ["none"] * 6)

    unknown = copy.deepcopy(certificate)
    unknown["unknown_field"] = True
    unknown["payload_sha256"] = payload_sha256(unknown)
    cases.append(("unknown-key", unknown))

    bad_payload = copy.deepcopy(certificate)
    bad_payload["payload_sha256"] = "0" * 64
    cases.append(("payload-hash", bad_payload))

    bool_as_int = copy.deepcopy(certificate)
    bool_as_int["row"]["agreement_A"] = True
    bool_as_int["payload_sha256"] = payload_sha256(bool_as_int)
    cases.append(("bool-as-integer", bool_as_int))

    for name, candidate in cases:
        expect_reject(name, candidate)

    duplicate_text = '{"schema_version":2,"schema_version":2}'
    try:
        json.loads(duplicate_text, object_pairs_hook=strict_object, parse_constant=reject_constant)
    except CertificateError:
        pass
    else:
        raise CertificateError("tamper accepted: duplicate-key")

    try:
        json.loads('{"x":NaN}', object_pairs_hook=strict_object, parse_constant=reject_constant)
    except CertificateError:
        pass
    else:
        raise CertificateError("tamper accepted: nonstandard-constant")

    return len(cases) + 2


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    certificate = load_json(CERTIFICATE)
    validate(certificate)
    if args.tamper_selftest:
        rejected = run_tamper_selftest(certificate)
        print(f"M1_EXTENSION_UNIFORM_ATLAS_ROUTE_CUT_V2_TAMPER_PASS rejected={rejected}/{rejected}")
    else:
        print("M1_EXTENSION_UNIFORM_ATLAS_ROUTE_CUT_V2_VERIFY_PASS")
        print(
            "row: A=%d j=%d syndrome_t=%d kernel_lower=%d d=%d"
            % (A, J, T_SYNDROME, KERNEL_LOWER, DEFICIENCY)
        )
        print(
            "coarse lower: C(n,3)=%d B_star=%d ratio>5; U_A remains null"
            % (COARSE_LOWER, B_STAR)
        )
        print("decision: fixed/sample-pair promotion cut; unrefined uniform binomial envelope cut")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
