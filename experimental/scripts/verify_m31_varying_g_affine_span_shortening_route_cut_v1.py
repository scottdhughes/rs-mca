#!/usr/bin/env python3
"""Verify the M31 varying-G affine-span and fixed-G endpoint route cuts.

This standard-library verifier certifies two exact local theorems for the
Mersenne-31 LIST boundary residual:

* an excess-weighted evaluation-matroid basis inequality for every realized
  varying-G shallow family; and
* agreement-shortening/error-puncturing bounds that close the two endpoints
  of the fixed-G post-Johnson interval.

Neither theorem closes the deployed row or moves a Grande Finale v4 ledger
atom.  All proof-critical gates use explicit exceptions and remain active
under ``python -O``.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from math import comb
from pathlib import Path
from typing import Any, Callable


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
COMPANION_TARGET = B_STAR - 1
FORBIDDEN_LIST_SIZE = B_STAR + 1
DEEP_CAP = 1_001_282
SHALLOW_LOWER = FORBIDDEN_LIST_SIZE - DEEP_CAP - 1
SHALLOW_TARGET = SHALLOW_LOWER - 1
S_MAX = 366_886

SCHEMA_ID = "m31-varying-g-affine-span-shortening-route-cut-summary-v1"
THEOREM_ID = "M31_VARYING_G_AFFINE_SPAN_SHORTENING_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_AFFINE_SPAN_SHORTENING_V1"
ARTIFACT_KIND = "EXACT_AFFINE_SPAN_AND_FIXED_G_ENDPOINT_ROUTE_CUT"
STATUS = "PROVED_AFFINE_RANK4_AND_FIXED_G_ENDPOINT_ROUTE_CUTS_HIGH_RANK_OPEN"
TERMINAL = "UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE"

PARENT_PAYLOAD = "006cde59ee0a9fc23f8f13c3dc9955c26732bdee86b4af943f06fffeb5dd572e"
FIXED_G_PAYLOAD = "d28cf777c70a7cbfbf9d79aabe568c33f6efa9485270f41424bcafbea9926be4"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_varying_g_affine_span_shortening_route_cut_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/manifest.json"
README_PATH = ROOT / "experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/README.md"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_varying_g_affine_span_shortening_route_cut_v1.md"
PRIMARY_PATH = Path(__file__).resolve()
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_v1.sage"
TOY_PATH = ROOT / "experimental/scripts/scan_m31_varying_g_shallow_incidence_toy_v1.sage"
PACKET_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_packet_v1.py"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json"
PARENT_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_common_v_split_flat_pairwise_crt_equivalence_v1.md"
FIXED_G_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/manifest.json"
FIXED_G_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md"


class VerificationError(RuntimeError):
    """Raised whenever an exact certificate gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            indent=2 if pretty else None,
            separators=None if pretty else (",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"JSON exists: {path}")
    try:
        value = json.loads(path.read_text(encoding="ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"valid ASCII JSON: {path}") from exc
    require(type(value) is dict, f"JSON object: {path}")
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


def incidence_cap(universe: int, support: int, intersection: int) -> dict[str, int]:
    require(0 <= intersection < support <= universe, "incidence parameters")
    delta = support * support - universe * intersection
    require(delta > 0, "positive incidence denominator")
    numerator = universe * (support - intersection)
    cap, remainder = divmod(numerator, delta)
    return {
        "universe": universe,
        "support": support,
        "intersection": intersection,
        "delta": delta,
        "numerator": numerator,
        "cap": cap,
        "remainder": remainder,
    }


def uniform_zero_excess_cap(rank: int, union_size: int, common_e: int = 0) -> int:
    require(rank >= 1, "positive affine rank")
    require(0 <= common_e <= R, "legal common E0 zeros")
    require(W + rank <= union_size - common_e <= A, "legal numerator union")
    numerator = comb(R + union_size - common_e, rank)
    denominator = comb(W + rank + common_e, rank)
    return numerator // denominator


def first_union_size_for_rank(rank: int, target: int) -> dict[str, int]:
    lo = W + rank
    hi = A
    require(uniform_zero_excess_cap(rank, hi) >= target, "rank reaches target")
    while lo < hi:
        mid = (lo + hi) // 2
        if uniform_zero_excess_cap(rank, mid) >= target:
            hi = mid
        else:
            lo = mid + 1
    threshold = lo
    return {
        "rank": rank,
        "first_union_size_not_excluded": threshold,
        "predecessor_cap": uniform_zero_excess_cap(rank, threshold - 1),
        "threshold_cap": uniform_zero_excess_cap(rank, threshold),
    }


def convex_excess_ceiling(rank: int) -> dict[str, Any]:
    """Maximize total excess under the worst-case affine-span budget.

    Discrete convexity makes the least-cost allocation at fixed total as
    equal as possible.  Thus the optimizer uses only q and q+1.
    """

    require(rank >= 1, "positive convex rank")
    budget = comb(N, rank)

    def cost(excess: int) -> int:
        return comb(W + excess + rank, rank)

    lo, hi = 0, S_MAX
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if SHALLOW_LOWER * cost(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    q = lo
    if q == S_MAX:
        raised = 0
        total = SHALLOW_LOWER * S_MAX
        cut = False
    else:
        remainder = budget - SHALLOW_LOWER * cost(q)
        marginal = comb(W + q + rank, rank - 1)
        raised = min(SHALLOW_LOWER - 1, remainder // marginal)
        total = SHALLOW_LOWER * q + raised
        cut = total < SHALLOW_LOWER * S_MAX
    return {
        "rank": rank,
        "base_excess_q": q,
        "entries_raised_to_q_plus_1": raised,
        "total_excess_ceiling": total,
        "full_shallow_total": SHALLOW_LOWER * S_MAX,
        "uniform_cut": cut,
    }


def shortening_ceiling(m: int, d: int, selected: int) -> dict[str, int]:
    require(1 <= selected < min(m, d), "legal agreement shortening")
    universe = R - selected
    support = m - selected
    intersection = d - selected - 1
    local = incidence_cap(universe, support, intersection)
    numerator = comb(R, selected) * local["cap"]
    denominator = comb(m, selected)
    cap, remainder = divmod(numerator, denominator)
    return {
        "selected": selected,
        "delta": local["delta"],
        "local_cap": local["cap"],
        "pullback_numerator": numerator,
        "pullback_denominator": denominator,
        "pullback_cap": cap,
        "pullback_remainder": remainder,
    }


def error_puncturing_ceiling(m: int, d: int, selected: int) -> dict[str, int]:
    errors = R - m
    require(1 <= selected <= errors, "legal error puncturing")
    local = incidence_cap(R - selected, m, d - 1)
    numerator = comb(R, selected) * local["cap"]
    denominator = comb(errors, selected)
    cap, remainder = divmod(numerator, denominator)
    return {
        "selected": selected,
        "delta": local["delta"],
        "local_cap": local["cap"],
        "pullback_numerator": numerator,
        "pullback_denominator": denominator,
        "pullback_cap": cap,
        "pullback_remainder": remainder,
    }


def source_bindings() -> list[dict[str, str]]:
    specifications = (
        ("packet_schema", SCHEMA_PATH),
        ("primary_exact_replay", PRIMARY_PATH),
        ("independent_sage_replay", SAGE_PATH),
        ("exhaustive_toy_scanner", TOY_PATH),
        ("packet_verifier", PACKET_PATH),
        ("theorem_note", NOTE_PATH),
        ("packet_readme", README_PATH),
        ("parent_manifest", PARENT_MANIFEST_PATH),
        ("parent_note", PARENT_NOTE_PATH),
        ("fixed_g_manifest", FIXED_G_MANIFEST_PATH),
        ("fixed_g_note", FIXED_G_NOTE_PATH),
    )
    return [
        {
            "binding_id": f"M31_AFFINE_SPAN::{role}",
            "role": role,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_path(path),
        }
        for role, path in specifications
    ]


def build_payload() -> dict[str, Any]:
    require(N == A + R, "domain partition")
    require(W == A - K, "anchor deficit")
    require(SHALLOW_LOWER == 15_775_933, "shallow lower inherited exactly")
    require(SHALLOW_TARGET == 15_775_932, "shallow target inherited exactly")
    require(P - 1 > B_STAR, "strict pairwise CRT field gate")

    parent = load_json(PARENT_MANIFEST_PATH)
    fixed_g = load_json(FIXED_G_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent payload pin")
    require(fixed_g.get("payload_sha256") == FIXED_G_PAYLOAD, "fixed-G payload pin")

    rank_caps = [
        {"rank": rank, "worst_case_zero_excess_cap": uniform_zero_excess_cap(rank, A)}
        for rank in range(1, 5)
    ]
    require([row["worst_case_zero_excess_cap"] for row in rank_caps]
            == [31, 966, 30_058, 934_551], "rank 1--4 caps")

    thresholds = [first_union_size_for_rank(rank, SHALLOW_LOWER) for rank in (5, 6)]
    require(thresholds == [
        {
            "rank": 5,
            "first_union_size_not_excluded": 874_886,
            "predecessor_cap": 15_775_899,
            "threshold_cap": 15_775_941,
        },
        {
            "rank": 6,
            "first_union_size_not_excluded": 87_070,
            "predecessor_cap": 15_775_873,
            "threshold_cap": 15_775_962,
        },
    ], "rank 5--6 union thresholds")

    excess = [convex_excess_ceiling(rank) for rank in range(5, 12)]
    require(
        [row["total_excess_ceiling"] for row in excess[:6]] == [
            138_248_451_290,
            1_025_002_415_798,
            2_035_737_937_266,
            3_103_382_431_039,
            4_182_106_682_358,
            5_242_898_479_007,
        ],
        "rank 5--10 convex excess ceilings",
    )
    require([row["base_excess_q"] for row in excess[:6]]
            == [8_763, 64_972, 129_040, 196_716, 265_094, 332_335],
            "rank 5--10 balanced bases")
    require([row["entries_raised_to_q_plus_1"] for row in excess[:6]]
            == [3_950_411, 8_496_922, 11_542_946, 3_995_011, 1_499_656, 3_785_452],
            "rank 5--10 balanced remainders")
    require(excess[-1]["base_excess_q"] == S_MAX, "rank 11 no uniform excess cut")
    require(not excess[-1]["uniform_cut"], "rank 11 branch remains primitive")

    lower_m, lower_d = 72_859, 5_412
    lower_local = incidence_cap(R - 1, lower_m - 1, lower_d - 2)
    require(lower_local["delta"] == 385_684, "lower endpoint delta")
    require(lower_local["cap"] == 171_578, "lower endpoint local cap")
    require(lower_local["remainder"] == 231_992, "lower endpoint local remainder")
    lower_cap, lower_remainder = divmod(R * lower_local["cap"], lower_m)
    require(lower_cap == 2_310_492, "lower endpoint list cap")

    upper_m, upper_d = 908_270, 840_823
    upper_shell_local = incidence_cap(R - 1, upper_m, upper_d - 1)
    require(upper_shell_local == lower_local | {
        "support": upper_m,
        "intersection": upper_d - 1,
    }, "endpoint local identities")
    shell_cap, shell_remainder = divmod(R * upper_shell_local["cap"], R - upper_m)
    require(shell_cap == 2_310_492, "upper exact shell cap")
    upper_tail = incidence_cap(R, upper_m + 1, upper_d - 1)
    require(upper_tail["delta"] == 1_361_403, "upper tail delta")
    require(upper_tail["cap"] == 48_608, "upper tail cap")
    require(shell_cap + upper_tail["cap"] == 2_359_100, "upper endpoint total")

    adjacent_lower = [shortening_ceiling(72_860, 5_413, selected) for selected in range(2, 7)]
    adjacent_upper = [error_puncturing_ceiling(908_269, 840_822, selected) for selected in range(2, 7)]
    require(adjacent_lower == adjacent_upper, "adjacent endpoints have identical method ceilings")
    require([row["pullback_cap"] for row in adjacent_lower] == [
        30_682_450,
        131_171_396,
        1_049_845_524,
        10_057_621_549,
        105_113_431_231,
    ], "adjacent method ceilings")
    require(all(row["pullback_cap"] > COMPANION_TARGET for row in adjacent_lower),
            "adjacent method misses target")
    require(R > 13 * 72_860, "large-s ratio base exceeds 13")
    require(13**7 > COMPANION_TARGET, "large-s ratio exceeds target")

    payload: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "terminal": TERMINAL,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "agreement": A,
            "budget": B_STAR,
            "companion_nonanchor_target": COMPANION_TARGET,
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": "EVERY_RECONSTRUCTED_BASE_FIELD_BOUNDARY_SHALLOW_FAMILY_AND_EVERY_FIXED_G_ORDINARY_RECEIVED_WORD",
        },
        "deployed_parameters": {
            "p": P,
            "n": N,
            "K": K,
            "a": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "forbidden_list_size": FORBIDDEN_LIST_SIZE,
            "deep_cap": DEEP_CAP,
            "shallow_lower": SHALLOW_LOWER,
            "shallow_target": SHALLOW_TARGET,
            "shallow_excess_range": [0, S_MAX],
        },
        "affine_span_incidence": {
            "rank_definition": "r=dim_Fp span{c_i}",
            "codeword_definition": "c_i=(A0/G_i)b_i",
            "union_definition": "g=|union_i Z(G_i)| on S0",
            "common_error_zero_definition": "e=|E0 intersect intersection_i Z(b_i)|",
            "common_zero_count": "z=a-g+e",
            "common_zero_bound": "z<=K-r",
            "union_gate": "g-e>=w+r",
            "basis_inequality": "sum_i binom(w+s_i+r+e,r)<=binom(R+g-e,r)",
            "projection": "full-rank r-coordinate agreement set determines at most one codeword coefficient vector",
            "support_count_substitution_forbidden": True,
        },
        "rank_consequences": {
            "rank_1_through_4_excluded": True,
            "worst_case_zero_excess_caps": rank_caps,
            "rank_5_6_union_thresholds": thresholds,
            "worst_case_convex_excess_ceilings": excess,
            "rank_at_least_7_not_excluded_by_zero_excess": True,
            "rank_at_least_11_not_uniformly_cut_over_full_shallow_range": True,
        },
        "fixed_g_endpoint_peeling": {
            "old_unresolved_m_interval": [72_859, 908_270],
            "new_unresolved_m_interval": [72_860, 908_269],
            "old_unresolved_d_interval": [5_412, 840_823],
            "new_unresolved_d_interval": [5_413, 840_822],
            "lower_endpoint": {
                "m": lower_m,
                "d": lower_d,
                "operation": "choose one agreement coordinate and shorten",
                "local_incidence": lower_local,
                "double_count_numerator": R * lower_local["cap"],
                "double_count_denominator": lower_m,
                "double_count_remainder": lower_remainder,
                "list_cap": lower_cap,
                "margin_below_companion_target": COMPANION_TARGET - lower_cap,
            },
            "upper_endpoint": {
                "m": upper_m,
                "d": upper_d,
                "operation": "puncture one error on exact shell; Johnson-bound higher-agreement tail",
                "exact_shell_local_incidence": upper_shell_local,
                "exact_shell_double_count_remainder": shell_remainder,
                "exact_shell_cap": shell_cap,
                "higher_agreement_tail_incidence": upper_tail,
                "total_cap": shell_cap + upper_tail["cap"],
                "margin_below_companion_target": COMPANION_TARGET - shell_cap - upper_tail["cap"],
            },
        },
        "adjacent_method_boundary": {
            "lower_row": {"m": 72_860, "d": 5_413},
            "upper_exact_shell_row": {"m": 908_269, "d": 840_822},
            "delta_formula": "-1290548+840821*s",
            "first_positive_selected_count": 2,
            "selected_2_through_6": adjacent_lower,
            "large_s_gate": "for 7<=s<d use a nonempty incidence bucket; for s>=d use coordinate uniqueness; in both cases binom(R,s)/binom(72860,s)>13^s>16777214",
            "conclusion": "STANDARD_SHORTENING_OR_ERROR_PUNCTURING_PLUS_PAIRWISE_INCIDENCE_CANNOT_CLOSE_ADJACENT_ROWS",
        },
        "toy_census": {
            "scope": "EXHAUSTIVE_TINY_FIELDS_ONLY",
            "deployed_incidence_upper_proved": False,
            "cells": [
                {"field": 5, "a": 2, "R": 2, "w": 0, "s_max": 0, "abstract": 5, "fixed_G": 2, "mixed_G": 5, "realized": 5},
                {"field": 5, "a": 3, "R": 2, "w": 1, "s_max": 0, "abstract": 1, "fixed_G": 1, "mixed_G": 0, "realized": 1},
                {"field": 7, "a": 3, "R": 3, "w": 1, "s_max": 0, "abstract": 3, "fixed_G": 1, "mixed_G": 3, "realized": 3},
                {"field": 7, "a": 3, "R": 3, "w": 1, "s_max": 1, "abstract": 3, "fixed_G": 1, "mixed_G": 3, "realized": 3},
                {"field": 7, "a": 4, "R": 2, "w": 0, "s_max": 1, "abstract": 14, "fixed_G": 2, "mixed_G": 14, "realized": 14, "zero_anchor_addback": 15, "distinct_G_in_witness": 10},
            ],
            "conclusion": "FIXED_G_MAXIMUM_IS_NOT_A_GLOBAL_VARYING_G_PROXY",
        },
        "dependency_contract": {
            "stacked_dependency": True,
            "pairwise_crt_parent_payload_sha256": PARENT_PAYLOAD,
            "fixed_g_parent_payload_sha256": FIXED_G_PAYLOAD,
        },
        "ledger_state": {
            "movement_from_this_packet": 0,
            "official_endpoint_or_score_movement": 0,
            "row_closed": False,
            "route_cut_not_payment": True,
        },
        "nonclaims": {
            "complete_M31_list_bound_proved": False,
            "rank_at_least_7_paid": False,
            "uniform_deterministic_RS_middle_bound_proved": False,
            "varying_G_reduced_to_fixed_G": False,
            "toy_cells_are_deployed_evidence": False,
            "ledger_atom_paid": False,
            "stable_paper_modified": False,
        },
        "source_bindings": source_bindings(),
    }
    return seal(payload)


def validate(payload: dict[str, Any]) -> None:
    deep_exact(payload, build_payload())
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload hash")


def mutation_tests(payload: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("schema", lambda x: x.__setitem__("schema", "hostile")),
        ("status", lambda x: x.__setitem__("status", "SAFE")),
        ("terminal", lambda x: x.__setitem__("terminal", "PAID")),
        ("rank-formula", lambda x: x["affine_span_incidence"].__setitem__("basis_inequality", "false")),
        ("rank-cap", lambda x: x["rank_consequences"]["worst_case_zero_excess_caps"][3].__setitem__("worst_case_zero_excess_cap", 934_552)),
        ("rank5-threshold", lambda x: x["rank_consequences"]["rank_5_6_union_thresholds"][0].__setitem__("first_union_size_not_excluded", 874_885)),
        ("rank6-threshold", lambda x: x["rank_consequences"]["rank_5_6_union_thresholds"][1].__setitem__("first_union_size_not_excluded", 87_069)),
        ("excess", lambda x: x["rank_consequences"]["worst_case_convex_excess_ceilings"][0].__setitem__("total_excess_ceiling", 138_248_451_291)),
        ("rank11", lambda x: x["rank_consequences"].__setitem__("rank_at_least_11_not_uniformly_cut_over_full_shallow_range", False)),
        ("lower-delta", lambda x: x["fixed_g_endpoint_peeling"]["lower_endpoint"]["local_incidence"].__setitem__("delta", 385_683)),
        ("lower-cap", lambda x: x["fixed_g_endpoint_peeling"]["lower_endpoint"].__setitem__("list_cap", 2_310_493)),
        ("upper-tail", lambda x: x["fixed_g_endpoint_peeling"]["upper_endpoint"].__setitem__("total_cap", 2_359_099)),
        ("new-interval", lambda x: x["fixed_g_endpoint_peeling"].__setitem__("new_unresolved_m_interval", [72_859, 908_269])),
        ("adjacent", lambda x: x["adjacent_method_boundary"]["selected_2_through_6"][0].__setitem__("pullback_cap", COMPANION_TARGET)),
        ("toy", lambda x: x["toy_census"]["cells"][4].__setitem__("realized", 2)),
        ("ledger", lambda x: x["ledger_state"].__setitem__("movement_from_this_packet", 1)),
        ("closure", lambda x: x["ledger_state"].__setitem__("row_closed", True)),
        ("nonclaim", lambda x: x["nonclaims"].__setitem__("rank_at_least_7_paid", True)),
        ("parent-pin", lambda x: x["dependency_contract"].__setitem__("pairwise_crt_parent_payload_sha256", "0" * 64)),
        ("source-hash", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("payload-hash", lambda x: x.__setitem__("payload_sha256", "0" * 64)),
    ]
    detected: list[str] = []
    for name, mutate in mutations:
        hostile = copy.deepcopy(payload)
        mutate(hostile)
        try:
            validate(hostile)
        except VerificationError:
            detected.append(name)
        else:
            raise VerificationError(f"mutation escaped: {name}")
    require(len(detected) == len(mutations), "all hostile mutations detected")
    return detected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the sealed manifest")
    parser.add_argument("--write-manifest", type=Path, help="write canonical sealed manifest")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    validate(payload)
    if args.tamper_selftest:
        names = mutation_tests(payload)
        print(json.dumps({"detected": names, "count": len(names)}, sort_keys=True))
        return
    if args.write_manifest is not None:
        args.write_manifest.parent.mkdir(parents=True, exist_ok=True)
        args.write_manifest.write_bytes(canonical_json(payload))
    if args.check:
        manifest = load_json(DEFAULT_MANIFEST)
        validate(manifest)
    sys.stdout.buffer.write(canonical_json(payload, pretty=args.pretty))


try:
    main()
except VerificationError as error:
    print(f"verification failed: {error}", file=sys.stderr)
    raise SystemExit(1)
