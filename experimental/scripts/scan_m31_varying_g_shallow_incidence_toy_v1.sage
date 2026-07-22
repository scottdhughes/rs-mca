#!/usr/bin/env sage
"""Exhaustive tiny-field scanner for the M31 varying-G shallow incidence.

For each declared toy boundary cell this script enumerates every canonical
triple ``(G,b,H)`` with

* ``G`` monic and split on ``S0``;
* ``m = deg(G)``, ``d = m-w``, ``b != 0``, ``deg(b) < d``;
* ``gcd(G,b)=gcd(H,b)=1``;
* ``H`` monic and split on ``E0`` with ``m <= deg(H) <= m+s_max``.

It then computes the exact maximum family satisfying the pairwise Wronskian
intersection/symmetric-difference gates, both with one fixed ``G`` and with
at least two different ``G`` locators.  Separately, it exhausts every unit
table ``V:E0 -> GF(q)^*`` and counts the *actual boundary-row codewords*
whose exact full gcd is ``H=gcd(L0,G-bV)``.  Thus an abstract pairwise clique
is never silently promoted to a realized RS list.

All scans are complete finite enumerations.  They are toy-scale controls and
do not prove the deployed M31 incidence upper or move a ledger atom.
"""

import argparse
import json
import sys
from itertools import combinations, product


SCHEMA = "m31-varying-g-shallow-incidence-toy-v1"
STATUS = "EXACT_TOY_CENSUS_DEPLOYED_INCIDENCE_OPEN"
TERMINAL = "UNPAID_VARYING_G_SHALLOW_INCIDENCE"


CELLS = (
    {
        "name": "gf5_a2_r2_w0_boundary",
        "q": 5,
        "a": 2,
        "R": 2,
        "w": 0,
        "s_max": 0,
    },
    {
        "name": "gf5_a3_r2_w1_boundary",
        "q": 5,
        "a": 3,
        "R": 2,
        "w": 1,
        "s_max": 0,
    },
    {
        "name": "gf7_a3_r3_w1_boundary",
        "q": 7,
        "a": 3,
        "R": 3,
        "w": 1,
        "s_max": 0,
    },
    {
        "name": "gf7_a3_r3_w1_shallow1",
        "q": 7,
        "a": 3,
        "R": 3,
        "w": 1,
        "s_max": 1,
    },
    {
        "name": "gf7_a4_r2_w0_shallow1",
        "q": 7,
        "a": 4,
        "R": 2,
        "w": 0,
        "s_max": 1,
    },
)


class ScanFailure(RuntimeError):
    pass


CHECKS = 0


def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not bool(condition):
        raise ScanFailure(label)


def locator(PR, roots):
    X = PR.gen()
    value = PR.one()
    for root in roots:
        value *= X - root
    return value


def interpolate(PR, points, values):
    F = PR.base_ring()
    X = PR.gen()
    value = PR.zero()
    for i, point in enumerate(points):
        basis = PR.one()
        denominator = F.one()
        for j, other in enumerate(points):
            if i == j:
                continue
            basis *= X - other
            denominator *= point - other
        value += values[i] * basis / denominator
    return value


def polynomial_from_coefficients(PR, coefficients):
    X = PR.gen()
    return sum(
        (PR.base_ring()(coefficient) * X**index
         for index, coefficient in enumerate(coefficients)),
        PR.zero(),
    )


def normalized_gcd(left, right):
    value = left.gcd(right)
    return value.monic() if value != 0 else value


def exact_quotient(numerator, denominator, label):
    quotient, remainder = numerator.quo_rem(denominator)
    require(remainder == 0, label)
    return quotient


def bit_indices(bits):
    while bits:
        bit = bits & -bits
        yield bit.bit_length() - 1
        bits -= bit


def is_clique(vertices, adjacency):
    for position, left in enumerate(vertices):
        required = 0
        for right in vertices[position + 1:]:
            required |= 1 << right
        if required & adjacency[left] != required:
            return False
    return True


class ExactCliqueSolver:
    """Tomita-style exact maximum clique with a greedy coloring bound."""

    def __init__(self, adjacency, group_ids, require_mixed=False, seed=None):
        self.adjacency = adjacency
        self.group_ids = group_ids
        self.require_mixed = require_mixed
        self.best = list(seed or [])
        if self.best:
            require(is_clique(self.best, adjacency), "clique seed is valid")
            if require_mixed:
                require(
                    len({group_ids[index] for index in self.best}) >= 2,
                    "mixed clique seed uses two G locators",
                )
        self.nodes = 0

    def color_sort(self, vertices):
        uncolored = vertices
        order = []
        bounds = []
        color = 0
        while uncolored:
            color += 1
            available = uncolored
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                uncolored -= bit
                available -= bit
                order.append(vertex)
                bounds.append(color)
                available -= available & self.adjacency[vertex]
        return order, bounds

    def can_be_mixed(self, group_mask, vertices):
        if not self.require_mixed or int(group_mask).bit_count() >= 2:
            return True
        possible = group_mask
        for vertex in bit_indices(vertices):
            possible |= 1 << self.group_ids[vertex]
            if int(possible).bit_count() >= 2:
                return True
        return False

    def expand(self, chosen, vertices, group_mask):
        self.nodes += 1
        if not vertices:
            if (not self.require_mixed or int(group_mask).bit_count() >= 2) \
                    and len(chosen) > len(self.best):
                self.best = list(chosen)
            return
        if not self.can_be_mixed(group_mask, vertices):
            return
        order, color_bounds = self.color_sort(vertices)
        for index in range(len(order) - 1, -1, -1):
            if len(chosen) + color_bounds[index] <= len(self.best):
                return
            vertex = order[index]
            bit = 1 << vertex
            if not vertices & bit:
                continue
            self.expand(
                chosen + [vertex],
                vertices & self.adjacency[vertex],
                group_mask | (1 << self.group_ids[vertex]),
            )
            vertices -= bit

    def solve(self, vertices):
        self.expand([], vertices, 0)
        require(is_clique(self.best, self.adjacency), "solver witness is clique")
        if self.require_mixed and self.best:
            require(
                len({self.group_ids[index] for index in self.best}) >= 2,
                "solver mixed witness classification",
            )
        return list(sorted(self.best)), self.nodes


def candidate_signature(candidate):
    return (
        candidate["G_roots"],
        candidate["b_coefficients"],
        candidate["H_roots"],
    )


def pair_signature(candidate):
    return candidate["G_roots"], candidate["b_coefficients"]


def pair_gate(left, right):
    if pair_signature(left) == pair_signature(right):
        return False
    W = left["G"] * right["b"] - right["G"] * left["b"]
    require(W != 0, "distinct reduced pairs have nonzero Wronskian")
    H_left = set(left["H_values"])
    H_right = set(right["H_values"])
    intersection = H_left.intersection(H_right)
    symmetric_difference = H_left.symmetric_difference(H_right)
    return (
        all(W(root) == 0 for root in intersection)
        and all(W(root) != 0 for root in symmetric_difference)
    )


def enumerate_pairs_and_candidates(cell, PR, s_roots, e_roots):
    F = PR.base_ring()
    q = cell["q"]
    a = cell["a"]
    R = cell["R"]
    w = cell["w"]
    s_max = cell["s_max"]
    pairs = []
    candidates = []
    pair_range_counts = {}
    candidate_range_counts = {}

    for m in range(w + 1, min(a, R) + 1):
        d = m - w
        pair_count_before = len(pairs)
        candidate_count_before = len(candidates)
        for G_values in combinations(s_roots, m):
            G = locator(PR, G_values)
            G_key = tuple(int(value) for value in G_values)
            for coefficients_field in product(list(F), repeat=d):
                if all(coefficient == 0 for coefficient in coefficients_field):
                    continue
                b = polynomial_from_coefficients(PR, coefficients_field)
                if normalized_gcd(G, b) != 1:
                    continue
                coefficients = tuple(int(value) for value in coefficients_field)
                pair = {
                    "m": m,
                    "d": d,
                    "G": G,
                    "G_roots": G_key,
                    "b": b,
                    "b_coefficients": coefficients,
                }
                pairs.append(pair)
                pair_id = len(pairs) - 1
                for h in range(m, min(R, m + s_max) + 1):
                    for H_values in combinations(e_roots, h):
                        H = locator(PR, H_values)
                        if normalized_gcd(H, b) != 1:
                            continue
                        candidate = dict(pair)
                        candidate.update({
                            "pair_id": pair_id,
                            "s": h - m,
                            "h": h,
                            "H": H,
                            "H_values": tuple(H_values),
                            "H_roots": tuple(int(value) for value in H_values),
                        })
                        candidates.append(candidate)
        pair_range_counts[str(m)] = len(pairs) - pair_count_before
        candidate_range_counts[str(m)] = len(candidates) - candidate_count_before

    require(len({pair_signature(pair) for pair in pairs}) == len(pairs),
            "canonical reduced pairs are unique")
    require(len({candidate_signature(item) for item in candidates})
            == len(candidates), "canonical triples are unique")
    require(pairs and candidates, "cell has canonical candidates")
    return pairs, candidates, pair_range_counts, candidate_range_counts


def build_compatibility_graph(candidates):
    count = len(candidates)
    adjacency = [0] * count
    edge_count = 0
    for left in range(count):
        for right in range(left + 1, count):
            if pair_gate(candidates[left], candidates[right]):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
                edge_count += 1
    require(all(not (adjacency[index] & (1 << index))
                for index in range(count)), "compatibility graph loop-free")
    return adjacency, edge_count


def group_index(candidates):
    keys = sorted({candidate["G_roots"] for candidate in candidates})
    key_to_group = {key: index for index, key in enumerate(keys)}
    groups = [[] for _key in keys]
    group_ids = []
    for index, candidate in enumerate(candidates):
        group_id = key_to_group[candidate["G_roots"]]
        group_ids.append(group_id)
        groups[group_id].append(index)
    return keys, group_ids, groups


def witness_summary(vertices, candidates):
    if not vertices:
        return {
            "vertex_ids": [],
            "distinct_G": 0,
            "members": [],
        }
    return {
        "vertex_ids": list(vertices),
        "distinct_G": len({candidates[index]["G_roots"] for index in vertices}),
        "members": [
            {
                "m": candidates[index]["m"],
                "d": candidates[index]["d"],
                "s": candidates[index]["s"],
                "G_roots": list(candidates[index]["G_roots"]),
                "b_coefficients": list(candidates[index]["b_coefficients"]),
                "H_roots": list(candidates[index]["H_roots"]),
            }
            for index in vertices
        ],
    }


def sage_clique_number(adjacency, vertices):
    selected = list(bit_indices(vertices))
    graph = Graph()
    graph.add_vertices(selected)
    graph.add_edges(
        (left, right)
        for left in selected
        for right in selected
        if left < right and adjacency[left] & (1 << right)
    )
    return int(graph.clique_number()) if selected else 0


def abstract_clique_census(candidates, adjacency, actual_seeds):
    keys, group_ids, groups = group_index(candidates)
    all_vertices = (1 << len(candidates)) - 1

    any_solver = ExactCliqueSolver(
        adjacency,
        group_ids,
        seed=actual_seeds.get("any", []),
    )
    any_witness, any_nodes = any_solver.solve(all_vertices)
    require(
        len(any_witness) == sage_clique_number(adjacency, all_vertices),
        "independent Sage maximum clique agrees",
    )

    fixed_best = []
    fixed_nodes = 0
    fixed_sage_best = 0
    for group in groups:
        vertices = sum(1 << index for index in group)
        seed = [
            index for index in actual_seeds.get("fixed", [])
            if index in set(group)
        ]
        solver = ExactCliqueSolver(adjacency, group_ids, seed=seed)
        witness, nodes = solver.solve(vertices)
        fixed_nodes += nodes
        if len(witness) > len(fixed_best):
            fixed_best = witness
        fixed_sage_best = max(fixed_sage_best,
                              sage_clique_number(adjacency, vertices))
    require(len(fixed_best) == fixed_sage_best,
            "independent fixed-G clique maximum agrees")

    mixed_seed = actual_seeds.get("mixed", [])
    mixed_solver = ExactCliqueSolver(
        adjacency,
        group_ids,
        require_mixed=True,
        seed=mixed_seed,
    )
    mixed_witness, mixed_nodes = mixed_solver.solve(all_vertices)

    return {
        "G_locator_count": len(keys),
        "maximum_any": len(any_witness),
        "maximum_fixed_G": len(fixed_best),
        "maximum_mixed_G": len(mixed_witness),
        "any_witness": witness_summary(any_witness, candidates),
        "fixed_G_witness": witness_summary(fixed_best, candidates),
        "mixed_G_witness": witness_summary(mixed_witness, candidates),
        "search_nodes": {
            "any": any_nodes,
            "all_fixed_G_slices": fixed_nodes,
            "mixed_G": mixed_nodes,
        },
        "independent_checks": {
            "sage_clique_number_any": len(any_witness),
            "sage_clique_number_fixed_G": len(fixed_best),
            "mixed_witness_validated": True,
        },
    }


def verify_actual_boundary_family(
        family, candidates, PR, A0, L0, s_roots, e_roots, V):
    gcd_value, H0, _cofactor = V.xgcd(L0)
    require(gcd_value == 1, "unit V has inverse modulo L0")
    H0 %= L0
    require((V * H0) % L0 == 1, "inverse representative is correct")
    U = A0 * H0
    anchor_support = {
        int(point) for point in s_roots + e_roots if U(point) == 0
    }
    require(anchor_support == {int(point) for point in s_roots},
            "zero boundary anchor has exact support S0")
    codeword_keys = set()
    for index in family:
        candidate = candidates[index]
        G = candidate["G"]
        b = candidate["b"]
        H = candidate["H"]
        require(normalized_gcd(L0, G - b * V) == H,
                "realized candidate has exact full gcd")
        codeword = exact_quotient(A0, G, "G divides A0") * b
        require(codeword.degree() < len(s_roots) - (
            candidate["m"] - candidate["d"]),
            "actual boundary codeword lies in toy RS dimension")
        actual_support = {
            int(point) for point in s_roots + e_roots
            if U(point) == codeword(point)
        }
        expected_support = (
            {int(point) for point in s_roots
             if int(point) not in candidate["G_roots"]}
            | set(candidate["H_roots"])
        )
        require(actual_support == expected_support,
                "actual row agreement support equals locator support")
        require(len(actual_support) == len(s_roots) + candidate["s"],
                "actual agreement is a+s")
        codeword_key = tuple(int(coefficient)
                             for coefficient in codeword.list())
        require(codeword_key not in codeword_keys,
                "canonical realized pairs give distinct codewords")
        codeword_keys.add(codeword_key)
    return len(codeword_keys)


def actual_unit_census(
        cell, PR, pairs, candidates, adjacency, s_roots, e_roots):
    F = PR.base_ring()
    A0 = locator(PR, s_roots)
    L0 = locator(PR, e_roots)
    lookup = {
        candidate_signature(candidate): index
        for index, candidate in enumerate(candidates)
    }
    all_nonzero_values = [value for value in F if value != 0]
    maximum_any = []
    maximum_fixed = []
    maximum_mixed = []
    witness_values = {"any": None, "fixed": None, "mixed": None}
    seen_vertices = 0
    co_realized_edges = [0] * len(candidates)
    total_family_memberships = 0
    unit_tables = 0

    for values in product(all_nonzero_values, repeat=len(e_roots)):
        unit_tables += 1
        V = interpolate(PR, e_roots, values)
        require(normalized_gcd(V, L0) == 1, "enumerated V is a unit")
        family = []
        for pair in pairs:
            H_values = tuple(
                point for point in e_roots
                if pair["G"](point) - pair["b"](point) * V(point) == 0
            )
            h = len(H_values)
            if not (pair["m"] <= h <= min(
                    cell["R"], pair["m"] + cell["s_max"])):
                continue
            key = (
                pair["G_roots"],
                pair["b_coefficients"],
                tuple(int(value) for value in H_values),
            )
            require(key in lookup, "realized full gcd has canonical triple")
            family.append(lookup[key])

        require(len(family) == len(set(family)),
                "one exact H per canonical reduced pair")
        require(is_clique(family, adjacency),
                "every common-unit family is pairwise compatible")
        total_family_memberships += len(family)
        for index in family:
            seen_vertices |= 1 << index
        for position, left in enumerate(family):
            for right in family[position + 1:]:
                co_realized_edges[left] |= 1 << right
                co_realized_edges[right] |= 1 << left

        by_G = {}
        for index in family:
            by_G.setdefault(candidates[index]["G_roots"], []).append(index)
        fixed = max(by_G.values(), key=len) if by_G else []
        if len(family) > len(maximum_any):
            maximum_any = list(family)
            witness_values["any"] = tuple(int(value) for value in values)
        if len(fixed) > len(maximum_fixed):
            maximum_fixed = list(fixed)
            witness_values["fixed"] = tuple(int(value) for value in values)
        if len(by_G) >= 2 and len(family) > len(maximum_mixed):
            maximum_mixed = list(family)
            witness_values["mixed"] = tuple(int(value) for value in values)

        require(
            verify_actual_boundary_family(
                family, candidates, PR, A0, L0, s_roots, e_roots, V)
            == len(family),
            "realized family size equals distinct nonanchor codeword count",
        )

    all_vertices = (1 << len(candidates)) - 1
    require(seen_vertices == all_vertices,
            "every canonical triple is individually realizable")
    require(co_realized_edges == adjacency,
            "every abstract compatible pair is co-realized by a unit table")
    require(unit_tables == (cell["q"] - 1) ** cell["R"],
            "all unit tables exhausted")
    return {
        "unit_tables_exhausted": unit_tables,
        "total_family_memberships": total_family_memberships,
        "maximum_any": len(maximum_any),
        "maximum_fixed_G": len(maximum_fixed),
        "maximum_mixed_G": len(maximum_mixed),
        "maximum_list_size_after_zero_anchor_addback": len(maximum_any) + 1,
        "counts_exclude_zero_anchor": True,
        "zero_anchor_addback": 1,
        "any_witness": witness_summary(maximum_any, candidates),
        "fixed_G_witness": witness_summary(maximum_fixed, candidates),
        "mixed_G_witness": witness_summary(maximum_mixed, candidates),
        "witness_unit_values": {
            key: list(value) if value is not None else None
            for key, value in witness_values.items()
        },
        "actual_row_checks": {
            "every_triple_individually_realized": True,
            "every_compatible_pair_co_realized": True,
            "all_families_are_compatibility_cliques": True,
            "exact_full_gcds_checked": True,
            "exact_agreement_supports_checked": True,
            "zero_anchor_exact_support_checked": True,
            "distinct_RS_codewords_checked": True,
        },
        "seeds": {
            "any": maximum_any,
            "fixed": maximum_fixed,
            "mixed": maximum_mixed,
        },
    }


def scan_cell(cell):
    q = cell["q"]
    require(q.is_prime(), "scanner cells use prime fields")
    require(cell["a"] + cell["R"] <= q,
            "split toy domains fit in the field")
    require(0 <= cell["w"] < min(cell["a"], cell["R"]),
            "legal toy agreement excess")
    require(0 <= cell["s_max"] <= cell["R"],
            "legal shallow excess range")

    F = GF(q)
    PR = PolynomialRing(F, "X")
    s_roots = [F(value) for value in range(cell["a"])]
    e_roots = [F(value) for value in range(
        cell["a"], cell["a"] + cell["R"])]
    require(not set(s_roots).intersection(e_roots),
            "S0 and E0 are disjoint")

    pairs, candidates, pair_range_counts, candidate_range_counts = (
        enumerate_pairs_and_candidates(cell, PR, s_roots, e_roots)
    )
    adjacency, edge_count = build_compatibility_graph(candidates)
    actual = actual_unit_census(
        cell, PR, pairs, candidates, adjacency, s_roots, e_roots)
    abstract = abstract_clique_census(
        candidates, adjacency, actual["seeds"])

    for classification in ("any", "fixed_G", "mixed_G"):
        abstract_value = abstract["maximum_" + classification]
        actual_value = actual["maximum_" + classification]
        require(actual_value <= abstract_value,
                "realized family is bounded by abstract clique maximum")
        if abstract_value < q - 1:
            require(actual_value == abstract_value,
                    "below field gate pairwise equivalence forces realization")

    del actual["seeds"]
    return {
        "name": cell["name"],
        "parameters": {
            "field": "GF(%d)" % q,
            "q": q,
            "n": cell["a"] + cell["R"],
            "a": cell["a"],
            "R": cell["R"],
            "K": cell["a"] - cell["w"],
            "w": cell["w"],
            "s_range": [0, cell["s_max"]],
            "m_range": [cell["w"] + 1,
                        min(cell["a"], cell["R"])],
            "d_rule": "d=m-w",
            "S0": [int(value) for value in s_roots],
            "E0": [int(value) for value in e_roots],
            "field_gate_for_pairwise_CRT": "family_size<q-1",
        },
        "enumeration": {
            "canonical_reduced_pairs": len(pairs),
            "canonical_shallow_triples": len(candidates),
            "pair_counts_by_m": pair_range_counts,
            "triple_counts_by_m": candidate_range_counts,
            "all_b_coefficient_vectors_exhausted": True,
            "all_split_G_root_subsets_exhausted": True,
            "all_split_H_root_subsets_exhausted": True,
            "compatibility_graph_edges": edge_count,
            "compatibility_graph_possible_edges": (
                len(candidates) * (len(candidates) - 1) // 2),
        },
        "abstract_pairwise_compatibility": abstract,
        "realized_boundary_row_nonanchor_codewords": actual,
        "comparison": {
            "gap_any": abstract["maximum_any"] - actual["maximum_any"],
            "gap_fixed_G": (
                abstract["maximum_fixed_G"] - actual["maximum_fixed_G"]),
            "gap_mixed_G": (
                abstract["maximum_mixed_G"] - actual["maximum_mixed_G"]),
            "abstract_maximum_below_field_gate": (
                abstract["maximum_any"] < q - 1),
            "toy_only_not_deployed_evidence": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cell",
        action="append",
        choices=[cell["name"] for cell in CELLS],
        help="run only the named cell; repeat for more than one",
    )
    parser.add_argument("--list-cells", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="omit full witnesses while retaining ranges and exact maxima",
    )
    args = parser.parse_args()

    if args.list_cells:
        for cell in CELLS:
            print(cell["name"])
        return

    selected = [
        cell for cell in CELLS
        if args.cell is None or cell["name"] in set(args.cell)
    ]
    require(selected, "at least one cell selected")
    results = [scan_cell(cell) for cell in selected]
    summary = {
        "schema": SCHEMA,
        "status": STATUS,
        "terminal": TERMINAL,
        "scope": {
            "enumeration": "complete for every printed toy cell",
            "sampling": False,
            "exact_finite_fields": True,
            "abstract_pairwise_families_are_not_row_codewords": True,
            "deployed_M31_incidence_upper_proved": False,
            "ledger_movement": 0,
        },
        "cells": results,
        "checks": CHECKS,
    }
    if args.summary_only:
        summary["cells"] = [
            {
                "name": result["name"],
                "parameters": result["parameters"],
                "enumeration": {
                    "canonical_reduced_pairs": result["enumeration"][
                        "canonical_reduced_pairs"],
                    "canonical_shallow_triples": result["enumeration"][
                        "canonical_shallow_triples"],
                    "compatibility_graph_edges": result["enumeration"][
                        "compatibility_graph_edges"],
                    "pair_counts_by_m": result["enumeration"][
                        "pair_counts_by_m"],
                    "triple_counts_by_m": result["enumeration"][
                        "triple_counts_by_m"],
                },
                "abstract_pairwise_maxima": {
                    key: result["abstract_pairwise_compatibility"][key]
                    for key in (
                        "maximum_any", "maximum_fixed_G", "maximum_mixed_G")
                },
                "realized_nonanchor_codeword_maxima": {
                    key: result[
                        "realized_boundary_row_nonanchor_codewords"][key]
                    for key in (
                        "maximum_any",
                        "maximum_fixed_G",
                        "maximum_mixed_G",
                        "maximum_list_size_after_zero_anchor_addback",
                        "unit_tables_exhausted",
                    )
                },
                "comparison": result["comparison"],
            }
            for result in results
        ]
    print(json.dumps(
        summary,
        sort_keys=True,
        indent=2 if args.pretty else None,
        separators=None if args.pretty else (",", ":"),
        allow_nan=False,
        default=int,
    ))


try:
    main()
except ScanFailure as error:
    print("scan failed: %s" % error, file=sys.stderr)
    raise SystemExit(1)
