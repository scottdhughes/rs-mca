#!/usr/bin/env sage
"""Sage audit for the M1 non-quotient pairwise-overlap rank gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from numbers import Integral


DATA_PATH = Path("experimental/data/m1_nonquotient_pairwise_overlap_rank_gate.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
TARGET_BITS = 128
SIZE4_COUNT = 271
SIZE5_COUNT = 241


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def sha256_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def all_patterns(size):
    return [tuple(pattern) for pattern in Combinations(range(LIST_SIZE), size)]


def pair_key(i, j):
    return (i, j) if i < j else (j, i)


def pair_label(pair):
    return "%d,%d" % (pair[0], pair[1])


def support_design():
    """Build the same deterministic balanced support design as the parent audit."""
    patterns_by_size = {4: all_patterns(4), 5: all_patterns(5)}
    remaining_by_size = {4: SIZE4_COUNT, 5: SIZE5_COUNT}
    counts = [0 for _ in range(LIST_SIZE)]
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    memberships = []

    for _pos in range(N):
        admissible_sizes = [size for size, remaining in remaining_by_size.items() if remaining]
        best = None
        for size in admissible_sizes:
            for pattern in patterns_by_size[size]:
                if any(counts[idx] >= TARGET_AGREEMENT for idx in pattern):
                    continue
                new_counts = counts[:]
                for idx in pattern:
                    new_counts[idx] += 1
                if any(count > TARGET_AGREEMENT for count in new_counts):
                    continue
                new_pair_counts = dict(pair_counts)
                for a, b in Subsets(pattern, 2):
                    key = pair_key(a, b)
                    new_pair_counts[key] += 1
                max_pair = max(new_pair_counts.values())
                if max_pair > K - 1:
                    continue
                score = (
                    max(abs(TARGET_AGREEMENT - count) for count in new_counts),
                    max_pair,
                    sum((TARGET_AGREEMENT - count) ** 2 for count in new_counts),
                    size,
                    pattern,
                )
                if best is None or score < best[0]:
                    best = (score, size, pattern, new_counts, new_pair_counts)
        if best is None:
            raise RuntimeError("support-design greedy construction failed")
        _score, size, pattern, counts, pair_counts = best
        remaining_by_size[size] -= 1
        memberships.append(list(pattern))

    assert len(memberships) == N
    assert counts == [TARGET_AGREEMENT] * LIST_SIZE
    assert remaining_by_size == {4: 0, 5: 0}
    pair_values = list(pair_counts.values())
    assert max(pair_values) <= K - 1
    return {
        "memberships": memberships,
        "witness_support_sizes": counts,
        "pair_intersection_min": min(pair_values),
        "pair_intersection_max": max(pair_values),
        "pair_intersection_values": sorted(pair_values),
        "pair_intersections": {
            pair_label(pair): pair_counts[pair]
            for pair in sorted(pair_counts)
        },
        "multiplicity_histogram": {
            "4": sum(1 for membership in memberships if len(membership) == 4),
            "5": sum(1 for membership in memberships if len(membership) == 5),
        },
    }


def support_positions(memberships):
    supports = [[] for _ in range(LIST_SIZE)]
    for pos, members in enumerate(memberships):
        for member in members:
            supports[member].append(pos)
    return supports


def intersection_positions(supports):
    intersections = {}
    for i in range(LIST_SIZE):
        set_i = set(supports[i])
        for j in range(i + 1, LIST_SIZE):
            intersections[(i, j)] = sorted(set_i.intersection(supports[j]))
    return intersections


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    return q, F, H


def locator_values(F, H, vanish_positions):
    """Evaluate prod_{a in vanish_positions}(X-a) on all H."""
    values = []
    roots = [H[pos] for pos in vanish_positions]
    for point in H:
        acc = F(1)
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def build_compressed_matrix(F, H, intersections):
    """Build the reduced D_i-D_j system after imposing D_i|S0capSi=0.

    For original witnesses 1..6, D_i is represented as

        D_i(X) = Z_i(X) E_i(X),

    where Z_i vanishes on S_0 cap S_i and deg D_i < 256.  This gives
    dim_i = 256 - |S_0 cap S_i| variables for E_i.  The remaining rows impose
    D_i(h)-D_j(h)=0 on S_i cap S_j for 1 <= i < j <= 6.
    """
    witness_dims = {}
    witness_offsets = {}
    locator_eval = {}
    ambient_dimension = 0

    for witness in range(1, LIST_SIZE):
        vanish = intersections[pair_key(0, witness)]
        dim = K - len(vanish)
        assert dim > 0
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values(F, H, vanish)

    rows = []
    remaining_equations_by_pair = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions = intersections[(i, j)]
            remaining_equations_by_pair[pair_label((i, j))] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = H[pos]
                powers_i = [F(1)]
                for _degree in range(1, dim_i):
                    powers_i.append(powers_i[-1] * point)
                powers_j = [F(1)]
                for _degree in range(1, dim_j):
                    powers_j.append(powers_j[-1] * point)
                row = [F(0) for _ in range(ambient_dimension)]
                scale_i = locator_eval[i][pos]
                scale_j = locator_eval[j][pos]
                for degree, value in enumerate(powers_i):
                    row[off_i + degree] = scale_i * value
                for degree, value in enumerate(powers_j):
                    row[off_j + degree] = -scale_j * value
                rows.append(row)

    return {
        "rows": rows,
        "ambient_dimension": ambient_dimension,
        "witness_dims": witness_dims,
        "witness_offsets": witness_offsets,
        "remaining_equations_by_pair": remaining_equations_by_pair,
    }


def coefficient_vector_from_kernel(kernel_vector, compressed, intersections, H, F):
    coeffs_by_witness = [[F(0) for _ in range(K)] for _ in range(LIST_SIZE)]
    for witness in range(1, LIST_SIZE):
        vanish = intersections[pair_key(0, witness)]
        locator_poly = PolynomialRing(F, "X").gen().parent()(1)
        X = locator_poly.parent().gen()
        for pos in vanish:
            locator_poly *= X - H[pos]
        dim = compressed["witness_dims"][str(witness)]
        off = compressed["witness_offsets"][witness]
        e_poly = sum(kernel_vector[off + degree] * X**degree for degree in range(dim))
        d_poly = locator_poly * e_poly
        coeffs = d_poly.list()
        for degree, coeff in enumerate(coeffs[:K]):
            coeffs_by_witness[witness][degree] = coeff
        assert d_poly.degree() < K or d_poly == 0
    return coeffs_by_witness


def eval_poly(coeffs, point):
    acc = point.parent()(0)
    power = point.parent()(1)
    for coeff in coeffs:
        acc += coeff * power
        power *= point
    return acc


def verify_solution(coeffs_by_witness, memberships, H):
    value_table = []
    for coeffs in coeffs_by_witness:
        value_table.append([eval_poly(coeffs, point) for point in H])

    received = {}
    for pos, members in enumerate(memberships):
        values = [value_table[member][pos] for member in members]
        if any(value != values[0] for value in values[1:]):
            return {"valid": False, "reason": "overlap disagreement"}
        received[pos] = values[0]

    agreement_counts = []
    for witness in range(LIST_SIZE):
        count = 0
        for pos, members in enumerate(memberships):
            if witness in members and value_table[witness][pos] == received[pos]:
                count += 1
        agreement_counts.append(count)

    coeff_tuples = [tuple(coeffs) for coeffs in coeffs_by_witness]
    distinct = len(set(coeff_tuples)) == LIST_SIZE
    nonzero_differences = all(any(coeff != 0 for coeff in coeffs_by_witness[witness]) for witness in range(1, LIST_SIZE))
    return {
        "valid": all(count >= TARGET_AGREEMENT for count in agreement_counts)
        and distinct
        and nonzero_differences,
        "agreement_counts": agreement_counts,
        "distinct_codewords": distinct,
        "nonzero_differences": nonzero_differences,
    }


def rank_gate(run_rank=True, extract_witness=False):
    design = support_design()
    supports = support_positions(design["memberships"])
    intersections = intersection_positions(supports)
    q, F, H = field_context()

    vanish_by_witness = {
        str(witness): len(intersections[pair_key(0, witness)])
        for witness in range(1, LIST_SIZE)
    }
    remaining_equations = sum(
        len(intersections[(i, j)])
        for i in range(1, LIST_SIZE)
        for j in range(i + 1, LIST_SIZE)
    )
    total_pairwise_equations = sum(len(value) for value in intersections.values())

    compressed = build_compressed_matrix(F, H, intersections)
    matrix_hash = sha256_payload(
        {
            "pair_intersections": design["pair_intersections"],
            "vanish_by_witness": vanish_by_witness,
            "witness_dims": compressed["witness_dims"],
            "remaining_equations_by_pair": compressed["remaining_equations_by_pair"],
        }
    )

    result = {
        "field_denominator": str(q),
        "field_denominator_label": "17^32",
        "subgroup_order": len(H),
        "difference_variables": 6 * K,
        "compressed_variables": compressed["ambient_dimension"],
        "diagonal_vanish_equations": sum(vanish_by_witness.values()),
        "remaining_pairwise_equations": remaining_equations,
        "total_pairwise_overlap_equations": total_pairwise_equations,
        "vanish_intersections_with_anchor": vanish_by_witness,
        "compressed_dimensions_by_witness": compressed["witness_dims"],
        "remaining_equations_by_pair": compressed["remaining_equations_by_pair"],
        "matrix_hash": matrix_hash,
        "rank": None,
        "nullity": None,
        "non_diagonal_solution_found": None,
        "explicit_witness_extracted": False,
        "status": "RANK_NOT_RUN",
    }

    if not run_rank:
        return design, result

    M = matrix(F, compressed["rows"])
    rank = M.rank()
    nullity = compressed["ambient_dimension"] - rank
    non_diagonal = nullity > 0
    result.update(
        {
            "rank": rank,
            "nullity": nullity,
            "non_diagonal_solution_found": non_diagonal,
            "status": "RANK_COMPUTED",
        }
    )

    if extract_witness and non_diagonal:
        basis = M.right_kernel().basis()
        kernel_vector = basis[0]
        coeffs_by_witness = coefficient_vector_from_kernel(
            kernel_vector,
            compressed,
            intersections,
            H,
            F,
        )
        verification = verify_solution(coeffs_by_witness, design["memberships"], H)
        result["explicit_witness_extracted"] = bool(verification["valid"])
        result["witness_verification"] = jsonable(verification)
        coeff_hashes = []
        for coeffs in coeffs_by_witness:
            coeff_hashes.append(
                hashlib.sha256(",".join(str(coeff) for coeff in coeffs).encode()).hexdigest()
            )
        result["coefficient_hashes"] = coeff_hashes

    return design, result


def compute(run_rank=True, extract_witness=False):
    design, gate = rank_gate(run_rank=run_rank, extract_witness=extract_witness)
    if gate["status"] == "RANK_NOT_RUN":
        status = "PARTIAL"
        candidate_found = False
        improves_pr_133 = False
    elif gate["non_diagonal_solution_found"]:
        status = "PROOF_RECORD_LOWER_BOUND" if gate["explicit_witness_extracted"] else "CANDIDATE_NULLSPACE"
        candidate_found = bool(gate["explicit_witness_extracted"])
        improves_pr_133 = bool(gate["explicit_witness_extracted"])
    else:
        status = "ROUTE_CUT_SUPPORT_DESIGN"
        candidate_found = False
        improves_pr_133 = False

    return {
        "support_design": {
            "witness_support_sizes": design["witness_support_sizes"],
            "pair_intersection_min": design["pair_intersection_min"],
            "pair_intersection_max": design["pair_intersection_max"],
            "pair_intersection_values": design["pair_intersection_values"],
            "pair_intersections": design["pair_intersections"],
            "multiplicity_histogram": design["multiplicity_histogram"],
        },
        "pairwise_overlap_rank_gate": gate,
        "global_status": {
            "candidate_found": candidate_found,
            "improves_pr_133": improves_pr_133,
            "status": status,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    parser.add_argument("--rank-only", action="store_true")
    parser.add_argument("--sample-nullspace", action="store_true")
    parser.add_argument("--extract-witness", action="store_true")
    parser.add_argument("--no-rank", action="store_true")
    args = parser.parse_args()

    run_rank = not args.no_rank
    extract_witness = args.extract_witness or args.sample_nullspace
    result = jsonable(compute(run_rank=run_rank, extract_witness=extract_witness))

    if args.compute_only or args.rank_only or args.no_rank:
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print("COMPUTED_M1_NONQUOTIENT_PAIRWISE_OVERLAP_RANK_GATE")
            print(json.dumps(result["pairwise_overlap_rank_gate"], sort_keys=True))
        return

    record = json.loads(DATA_PATH.read_text())
    assert record["track"] == "INTERLEAVED_LIST"
    assert Integer(record["field_denominator"]) == Integer(P) ** FIELD_DEGREE
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert result["support_design"] == record["support_design"]
    assert result["pairwise_overlap_rank_gate"] == record["pairwise_overlap_rank_gate"]
    assert result["global_status"] == record["global_status"]
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_NONQUOTIENT_PAIRWISE_OVERLAP_RANK_GATE_OK")


if __name__ == "__main__":
    main()
