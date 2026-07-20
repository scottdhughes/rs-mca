#!/usr/bin/env python3
"""Verify the exact rho=9 ADE architecture wall for the M31 list row.

The packet has two deliberately separate conclusions.

1.  At the first row not covered by the component-sensitive rho<9 theorem,
    every abstract common-height ADE/rank hypothesis used by that theorem is
    simultaneously feasible.  The witness is a connected 8-edge deletion
    from the positive roots of a 9 by q complete bipartite graph in A_{v-1}.
2.  The canonical witness cannot itself be an actual binary support family.
    A complete 9 by (q-1) subrectangle would violate an exact binary-
    rectangle dimension bound.

This is a sharp route cut, not a construction of an RS list and not a row
payment.  All arithmetic is exact and standard-library-only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import resource
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "rs-mca-m31-ade-rho9-architecture-wall-v1"
STATUS = "PROVED_SHARP_ADE_ROUTE_CUT_AND_BINARY_RECTANGLE_OBSTRUCTION"
CAP_BYTES = 256 * 1024**2
BASE_COMMIT = "a6e6232b7e935736c0b3cf33ba4cd39da55e2a6a"

NOTE_PATH = Path(
    "experimental/notes/thresholds/m31_ade_rho9_architecture_wall.md"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_ade_rho9_architecture_wall.py"
)
SAGE_PATH = Path(
    "experimental/scripts/verify_m31_ade_rho9_architecture_wall.sage"
)
README_PATH = Path(
    "experimental/data/certificates/m31-ade-rho9-architecture-wall/README.md"
)
ARTIFACT_PATH = Path(
    "experimental/data/certificates/m31-ade-rho9-architecture-wall/"
    "m31_ade_rho9_architecture_wall.json"
)
PARENT_NOTE_PATH = Path(
    "experimental/notes/thresholds/m31_ade_component_sensitive_refinement.md"
)
PARENT_VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_ade_component_sensitive_refinement.py"
)
PARENT_CERTIFICATE_PATH = Path(
    "experimental/data/certificates/m31-ade-component-sensitive/"
    "m31_ade_component_sensitive_refinement.json"
)

SOURCE_PATHS = (
    NOTE_PATH,
    VERIFIER_PATH,
    SAGE_PATH,
    README_PATH,
    PARENT_NOTE_PATH,
    PARENT_VERIFIER_PATH,
    PARENT_CERTIFICATE_PATH,
)

P = 2**31 - 1
N = 2**21
M = 981_129
W = 67_447
D0 = N - W
L = 2**24
T = 276_415
T_PROVED = 276_416
R = M * (N - M)
A = 9


class CheckFailure(AssertionError):
    """Raised when an exact packet invariant fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def impose_cap() -> int | None:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    try:
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
            soft = cap
    except (OSError, ValueError):
        # macOS reports a sentinel RLIMIT_AS but refuses to lower it.  The
        # checker is formula-only and never materializes the large graph.
        return None
    return int(soft)


def ceil_div(x: int, y: int) -> int:
    return -(-x // y)


def frac_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(obj)
    result.pop("payload_sha256", None)
    return result


def payload_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(without_hash(obj))).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        require((root / NOTE_PATH).is_file(), "explicit repository root")
        return root
    here = Path(__file__).resolve()
    for root in here.parents:
        if (root / NOTE_PATH).is_file() and (root / "experimental").is_dir():
            return root
    raise CheckFailure("repository root not found")


def load_parent_payload(root: Path) -> str:
    parent = json.loads((root / PARENT_CERTIFICATE_PATH).read_text())
    require(
        parent.get("schema") == "m31_ade_component_sensitive_refinement.v1",
        "parent schema",
    )
    require(parent.get("payload_sha256") == payload_hash(parent), "parent self-hash")
    return str(parent["payload_sha256"])


def build_certificate(root: Path) -> dict[str, Any]:
    q = ceil_div(L, A)
    v = A + q
    rank = v - 1
    deleted = A * q - L
    rectangle_b = q - 1
    rho = Fraction(N * T, 2 * N * T - R)
    rho_proved = Fraction(N * T_PROVED, 2 * N * T_PROVED - R)
    z_norm = Fraction(A * q, v)
    rho_gap = rho - z_norm
    h_squared = Fraction(2 * N * T - R, N * T)
    projected_unit_norm_squared = h_squared * z_norm
    binary_minimum = 2 * T + rectangle_b - 1
    eight_part_capacity = 8 * (D0 + 1 - 8)

    source_bindings = [
        {
            "path": str(path),
            "sha256": file_sha256(root / path),
        }
        for path in SOURCE_PATHS
    ]

    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "base_commit": BASE_COMMIT,
        "deployed_row": {
            "field_prime": P,
            "domain_size": N,
            "support_size": M,
            "prefix_depth": W,
            "modular_rank_cap": D0,
            "forbidden_list_size": L,
            "first_unclassified_two_shell_row": {
                "kappa": 2,
                "t": T,
                "e1": T,
                "e2": 2 * T,
            },
            "R=m(N-m)": R,
            "2Nt-R": 2 * N * T - R,
            "rho_t": frac_record(rho),
            "rho_t_greater_than_9": rho > 9,
            "preceding_proved_boundary": {
                "t": T_PROVED,
                "rho_t": frac_record(rho_proved),
                "rho_t_below_9": rho_proved < 9,
                "model_norm_minus_rho_t": frac_record(z_norm - rho_proved),
                "model_is_infeasible_at_proved_boundary": z_norm > rho_proved,
            },
        },
        "abstract_A_type_countercertificate": {
            "lattice": f"A_{rank}",
            "positive_part_size": A,
            "negative_part_size": q,
            "ambient_coordinate_count": v,
            "real_rank": rank,
            "modular_rank": rank,
            "rank_gap_below_d0": D0 - rank,
            "complete_bipartite_root_count": A * q,
            "deleted_edge_count": deleted,
            "canonical_deleted_edges_zero_based": [[i, q - 1] for i in range(deleted)],
            "selected_root_count": L,
            "graph_edge_connectivity_before_deletion": min(A, q),
            "selected_graph_connected": deleted < min(A, q),
            "pairwise_distinct_root_inner_products": [0, 1],
            "dual_vector": {
                "positive_coordinate": frac_record(Fraction(q, v)),
                "negative_coordinate": frac_record(Fraction(-A, v)),
                "coordinate_sum": 0,
                "all_selected_root_heights": 1,
                "squared_norm": frac_record(z_norm),
                "squared_norm_below_9": z_norm < 9,
            },
            "rho_minus_squared_norm": frac_record(rho_gap),
            "field_nondegeneracy": {
                "v_less_than_p": v < P,
                "v_mod_p": v % P,
                "p_does_not_divide_A_discriminant": v % P != 0,
            },
            "centered_euclidean_lift": {
                "h_squared": frac_record(h_squared),
                "h_squared_equals_inverse_rho": h_squared * rho == 1,
                "projected_unit_norm_squared": frac_record(projected_unit_norm_squared),
                "unit_extension_exists": projected_unit_norm_squared < 1,
                "identity": "tQ=YY^T+(2t-R/N)J",
                "shared_endpoint_exchange_distance": T,
                "disjoint_endpoint_exchange_distance": 2 * T,
            },
            "all_frozen_ADE_rank_hypotheses_feasible": True,
        },
        "two_level_A_type_integer_jump": {
            "scope": "connected_single_A_component",
            "largest_capacity_with_smaller_part_at_most_8": eight_part_capacity,
            "capacity_deficit_to_L": L - eight_part_capacity,
            "part_size_8_impossible_under_rank_cap": eight_part_capacity < L,
            "part_size_9_capacity": A * q,
            "part_size_9_is_first_possible": True,
            "minimum_part9_negative_size": q,
            "minimum_part9_squared_norm": frac_record(z_norm),
        },
        "binary_rectangle_lemma": {
            "statement": (
                "If binary vectors x_ij in {0,1}^N have Hamming distance 2t "
                "when exactly one index agrees and 4t when neither agrees, "
                "for a,b>=2 and positive t, then "
                "N>=max(2t,a-1)+max(2t,b-1)."
            ),
            "assumptions": {"a_at_least_2": True, "b_at_least_2": True, "t_positive": T > 0},
            "proof_atoms": {
                "euclidean_rectangle_identity": True,
                "exchange_distance_in_application_is_half_Hamming": True,
                "binary_coordinate_partition": ["constant", "row_only", "column_only"],
                "row_block_distance_lower_bound": 2 * T,
                "row_equidistant_affine_rank": A - 1,
                "column_block_distance_lower_bound": 2 * T,
                "column_equidistant_affine_rank": rectangle_b - 1,
            },
            "canonical_complete_subrectangle": {
                "a": A,
                "b": rectangle_b,
                "root_count": A * rectangle_b,
                "root_count_equals_L_minus_1": A * rectangle_b == L - 1,
            },
            "required_binary_domain_size": binary_minimum,
            "deployed_domain_size": N,
            "contradiction_margin": binary_minimum - N,
            "canonical_countercertificate_is_not_a_binary_support_family": (
                binary_minimum > N
            ),
        },
        "scope_guards": {
            "actual_constant_weight_family_constructed": False,
            "actual_prefix_fiber_constructed": False,
            "first_unclassified_parameter_row_excluded": False,
            "M31_list_row_closed": False,
            "U_Q_determined": False,
            "U_A_determined": False,
            "ledger_movement": 0,
            "ade_rank_architecture_alone_can_cross_rho9": False,
            "next_required_input": (
                "classify dense A-type height-one components using binary "
                "realizability and the full prefix-fiber equations"
            ),
        },
        "parent_binding": {
            "schema": "m31_ade_component_sensitive_refinement.v1",
            "payload_sha256": load_parent_payload(root),
        },
        "source_bindings": source_bindings,
        "resource_limits": {
            "address_space_target_bytes": CAP_BYTES,
            "address_space_cap_best_effort": True,
            "large_root_or_Gram_enumeration": False,
        },
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def validate_semantics(cert: dict[str, Any]) -> None:
    require(cert.get("schema") == SCHEMA, "schema")
    require(cert.get("status") == STATUS, "status")
    row = cert["deployed_row"]
    model = cert["abstract_A_type_countercertificate"]
    jump = cert["two_level_A_type_integer_jump"]
    rectangle = cert["binary_rectangle_lemma"]
    guards = cert["scope_guards"]

    require(row["forbidden_list_size"] == L, "forbidden list size")
    require(row["modular_rank_cap"] == D0, "rank cap")
    require(row["first_unclassified_two_shell_row"]["t"] == T, "boundary t")
    require(row["rho_t_greater_than_9"] is True, "rho exceeds nine")
    require(row["2Nt-R"] > 0, "positive common-height denominator")
    proved_boundary = row["preceding_proved_boundary"]
    require(proved_boundary["t"] == T_PROVED, "proved boundary t")
    require(proved_boundary["rho_t_below_9"] is True, "proved rho below nine")
    require(proved_boundary["model_is_infeasible_at_proved_boundary"] is True,
            "no contradiction with predecessor")

    require(model["selected_root_count"] == L, "selected root count")
    require(model["deleted_edge_count"] == 8, "eight-edge deletion")
    require(model["selected_graph_connected"] is True, "connected root graph")
    require(model["real_rank"] == model["modular_rank"], "real/modular rank")
    require(model["modular_rank"] <= D0, "modular rank cap")
    require(model["dual_vector"]["all_selected_root_heights"] == 1, "common height")
    require(model["dual_vector"]["squared_norm_below_9"] is True, "norm below nine")
    require(model["all_frozen_ADE_rank_hypotheses_feasible"] is True, "ADE feasibility")
    require(model["field_nondegeneracy"]["p_does_not_divide_A_discriminant"] is True,
            "A discriminant nonzero mod p")
    lift = model["centered_euclidean_lift"]
    require(lift["h_squared_equals_inverse_rho"] is True, "h squared inverse rho")
    require(lift["unit_extension_exists"] is True, "centered unit extension")
    require(lift["shared_endpoint_exchange_distance"] == T, "near exchange distance")
    require(lift["disjoint_endpoint_exchange_distance"] == 2 * T,
            "far exchange distance")

    require(jump["scope"] == "connected_single_A_component", "integer-jump scope")
    require(jump["part_size_8_impossible_under_rank_cap"] is True, "part eight impossible")
    require(jump["part_size_9_is_first_possible"] is True, "part nine first")
    require(rectangle["canonical_complete_subrectangle"]["root_count_equals_L_minus_1"] is True,
            "complete subrectangle size")
    require(rectangle["assumptions"]["t_positive"] is True, "positive rectangle distance")
    require(rectangle["contradiction_margin"] == 319_812, "binary contradiction margin")
    require(rectangle["canonical_countercertificate_is_not_a_binary_support_family"] is True,
            "binary support obstruction")

    require(guards["actual_constant_weight_family_constructed"] is False,
            "no actual support family")
    require(guards["first_unclassified_parameter_row_excluded"] is False,
            "row remains unexcluded")
    require(guards["M31_list_row_closed"] is False, "row remains open")
    require(guards["ledger_movement"] == 0, "zero ledger movement")
    require(guards["ade_rank_architecture_alone_can_cross_rho9"] is False,
            "ADE architecture route cut")


def validate_certificate(cert: dict[str, Any], expected: dict[str, Any]) -> None:
    require(cert.get("payload_sha256") == payload_hash(cert), "payload self-hash")
    validate_semantics(cert)
    require(cert == expected, "canonical certificate equality")


def write_artifact(root: Path, cert: dict[str, Any]) -> None:
    path = root / ARTIFACT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def mutate_path(obj: dict[str, Any], path: tuple[Any, ...], value: Any) -> dict[str, Any]:
    result = copy.deepcopy(obj)
    cursor: Any = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    result["payload_sha256"] = payload_hash(result)
    return result


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = [
        ("schema", mutate_path(expected, ("schema",), "wrong-schema")),
        ("status", mutate_path(expected, ("status",), "CLOSED")),
        ("base", mutate_path(expected, ("base_commit",), "0" * 40)),
        ("list-size", mutate_path(expected, ("deployed_row", "forbidden_list_size"), L - 1)),
        ("rank-cap", mutate_path(expected, ("deployed_row", "modular_rank_cap"), D0 + 1)),
        ("boundary", mutate_path(expected, ("deployed_row", "first_unclassified_two_shell_row", "t"), T + 1)),
        ("rho-sign", mutate_path(expected, ("deployed_row", "rho_t_greater_than_9"), False)),
        ("proved-boundary", mutate_path(expected, ("deployed_row", "preceding_proved_boundary", "t"), T)),
        ("predecessor-conflict", mutate_path(expected, ("deployed_row", "preceding_proved_boundary", "model_is_infeasible_at_proved_boundary"), False)),
        ("denominator", mutate_path(expected, ("deployed_row", "2Nt-R"), -1)),
        ("root-count", mutate_path(expected, ("abstract_A_type_countercertificate", "selected_root_count"), L - 1)),
        ("deletions", mutate_path(expected, ("abstract_A_type_countercertificate", "deleted_edge_count"), 9)),
        ("connectivity", mutate_path(expected, ("abstract_A_type_countercertificate", "selected_graph_connected"), False)),
        ("real-rank", mutate_path(expected, ("abstract_A_type_countercertificate", "real_rank"), D0 + 1)),
        ("mod-rank", mutate_path(expected, ("abstract_A_type_countercertificate", "modular_rank"), D0 + 1)),
        ("height", mutate_path(expected, ("abstract_A_type_countercertificate", "dual_vector", "all_selected_root_heights"), 0)),
        ("norm", mutate_path(expected, ("abstract_A_type_countercertificate", "dual_vector", "squared_norm_below_9"), False)),
        ("discriminant", mutate_path(expected, ("abstract_A_type_countercertificate", "field_nondegeneracy", "p_does_not_divide_A_discriminant"), False)),
        ("lift-rho", mutate_path(expected, ("abstract_A_type_countercertificate", "centered_euclidean_lift", "h_squared_equals_inverse_rho"), False)),
        ("lift-unit", mutate_path(expected, ("abstract_A_type_countercertificate", "centered_euclidean_lift", "unit_extension_exists"), False)),
        ("lift-shell", mutate_path(expected, ("abstract_A_type_countercertificate", "centered_euclidean_lift", "disjoint_endpoint_exchange_distance"), 2 * T + 1)),
        ("ADE-feasible", mutate_path(expected, ("abstract_A_type_countercertificate", "all_frozen_ADE_rank_hypotheses_feasible"), False)),
        ("jump-scope", mutate_path(expected, ("two_level_A_type_integer_jump", "scope"), "all_components")),
        ("part8", mutate_path(expected, ("two_level_A_type_integer_jump", "part_size_8_impossible_under_rank_cap"), False)),
        ("part9", mutate_path(expected, ("two_level_A_type_integer_jump", "part_size_9_is_first_possible"), False)),
        ("rectangle-size", mutate_path(expected, ("binary_rectangle_lemma", "canonical_complete_subrectangle", "root_count_equals_L_minus_1"), False)),
        ("rectangle-zero-distance", mutate_path(expected, ("binary_rectangle_lemma", "assumptions", "t_positive"), False)),
        ("binary-margin", mutate_path(expected, ("binary_rectangle_lemma", "contradiction_margin"), 0)),
        ("binary-obstruction", mutate_path(expected, ("binary_rectangle_lemma", "canonical_countercertificate_is_not_a_binary_support_family"), False)),
        ("fake-support", mutate_path(expected, ("scope_guards", "actual_constant_weight_family_constructed"), True)),
        ("fake-row-exclusion", mutate_path(expected, ("scope_guards", "first_unclassified_parameter_row_excluded"), True)),
        ("fake-closure", mutate_path(expected, ("scope_guards", "M31_list_row_closed"), True)),
        ("fake-ledger", mutate_path(expected, ("scope_guards", "ledger_movement"), 1)),
        ("fake-crossing", mutate_path(expected, ("scope_guards", "ade_rank_architecture_alone_can_cross_rho9"), True)),
        ("parent", mutate_path(expected, ("parent_binding", "payload_sha256"), "0" * 64)),
        ("source", mutate_path(expected, ("source_bindings", 0, "sha256"), "0" * 64)),
    ]
    bad_hash = copy.deepcopy(expected)
    bad_hash["payload_sha256"] = "0" * 64
    mutations.append(("self-hash", bad_hash))

    rejected = 0
    for label, candidate in mutations:
        try:
            validate_certificate(candidate, expected)
        except (CheckFailure, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise CheckFailure(f"tamper survived: {label}")
    require(rejected == len(mutations), "all mutations rejected")
    print(f"tamper self-test: {rejected}/{len(mutations)} rejected")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    impose_cap()
    root = locate_repo(args.repo_root)
    expected = build_certificate(root)

    if args.write:
        write_artifact(root, expected)
        print(f"wrote {root / ARTIFACT_PATH}")
        return 0
    if args.tamper_selftest:
        tamper_selftest(expected)
        return 0

    artifact = root / ARTIFACT_PATH
    require(artifact.is_file(), "certificate exists; run --write")
    actual = json.loads(artifact.read_text())
    validate_certificate(actual, expected)
    model = actual["abstract_A_type_countercertificate"]
    rectangle = actual["binary_rectangle_lemma"]
    print("M31 rho=9 ADE architecture wall: PASS")
    print(f"  exact roots: {model['selected_root_count']}")
    print(f"  real/mod-p rank: {model['real_rank']} <= {D0}")
    print(f"  binary rectangle contradiction margin: {rectangle['contradiction_margin']}")
    print("  row closure: false; ledger movement: 0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
