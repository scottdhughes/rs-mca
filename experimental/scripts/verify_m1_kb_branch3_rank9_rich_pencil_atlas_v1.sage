#!/usr/bin/env sage
"""Exact rich-pencil atlas replay on the j=20 five-pencil family.

The loaded predecessor constructs the complete declared GF(2^37) selector.
This checker canonically groups every excess rank-eight basis by its affine
graph line and verifies direct excess equals the atlas sum.  It is an exact
generic-local control, not a KoalaBear-domain census.
"""

import hashlib
import json
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SCRIPT_DIR = Path(__file__).resolve().parent
PREDECESSOR = (
    SCRIPT_DIR / "verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.sage"
)
predecessor_stdout = StringIO()
with redirect_stdout(predecessor_stdout):
    load(str(PREDECESSOR))
require('"status": "PASS"' in predecessor_stdout.getvalue(),
        "fixed-basis predecessor did not replay")

require((j, n, k, R, A) == (20, 34, 13, 21, 14),
        "loaded toy row drift")
require(len(slopes) == len(errors) == len(zero_masks) == 105,
        "loaded selector size drift")
require(K0.rank() == 8, "loaded K0 rank drift")

# Normalize the syndrome direction and recover K0 coordinates of every graph
# point e_eta = affine_origin + eta*affine_direction + w_eta.
eta_0 = slopes[0]
eta_1 = slopes[1]
require(eta_0 != eta_1, "anchor slopes collided")
affine_direction = (errors[1] - errors[0]) / (eta_1 - eta_0)
affine_origin = errors[0] - eta_0 * affine_direction
require(H * affine_origin == y_0, "affine origin syndrome drift")
require(H * affine_direction == y_1, "affine direction syndrome drift")

k0_pivots = list(K0.pivots())
require(len(k0_pivots) == 8, "K0 pivot count drift")
K0_square = K0.matrix_from_columns(k0_pivots)
require(K0_square.det() != 0, "K0 pivot square became singular")
K0_square_inverse = K0_square.inverse()


def k0_coordinates(word):
    restricted = vector(F, [word[index] for index in k0_pivots])
    coefficients = restricted * K0_square_inverse
    reconstructed = coefficients * K0
    require(reconstructed == word, "K0 coordinate reconstruction failed")
    return vector(F, coefficients)


graph_coordinates = []
for eta, error in zip(slopes, errors):
    residual = error - affine_origin - eta * affine_direction
    require(H * residual == 0, "graph residual left the RS kernel")
    graph_coordinates.append(k0_coordinates(residual))

# Every pair of graph points determines one affine graph line.  Equal keys
# canonically merge all points on the same line.
line_members = defaultdict(set)
for left, right in combinations(range(len(slopes)), 2):
    denominator = slopes[right] - slopes[left]
    require(denominator != 0, "distinct graph points lost slope separation")
    beta = (
        graph_coordinates[right] - graph_coordinates[left]
    ) / denominator
    alpha = graph_coordinates[left] - slopes[left] * beta
    key = (tuple(alpha), tuple(beta))
    line_members[key].add(left)
    line_members[key].add(right)

rich_lines = [
    (key, tuple(sorted(members)))
    for key, members in line_members.items()
    if len(members) >= 21
]
rich_lines.sort(key=lambda item: item[1][0])
require(len(rich_lines) == 5, "rich graph-line count drift")
require([len(members) for _, members in rich_lines] == [21] * 5,
        "rich graph-line sizes drift")


def linear_combination(coefficients):
    result = vector(F, [0] * n)
    for index, coefficient in enumerate(coefficients):
        result += coefficient * K0.row(index)
    return result


line_records = []
rich_basis_owner = {}
for line_index, (key, members) in enumerate(rich_lines):
    alpha = vector(F, key[0])
    beta = vector(F, key[1])
    a_line = affine_origin + linear_combination(alpha)
    b_line = affine_direction + linear_combination(beta)

    require(all(errors[index] == a_line + slopes[index] * b_line
                for index in members), "line word identity failed")
    require(a_line[0] == a_line[1] == b_line[0] == b_line[1] == 0,
            "toy line gained sparse-coordinate support")

    common_zero = tuple(
        index for index in range(B_size)
        if a_line[2 + index] == 0 and b_line[2 + index] == 0
    )
    moving_support = tuple(
        index for index in range(B_size) if index not in set(common_zero)
    )
    M_line = ZZ(len(moving_support))
    x_line = M_line - j
    require((len(common_zero), M_line, x_line) == (11, 21, 1),
            "toy line support tuple drift")

    moving_zero_sets = []
    deficits = []
    for index in members:
        moving_zeros = frozenset(
            coordinate for coordinate in moving_support
            if a_line[2 + coordinate]
               + slopes[index] * b_line[2 + coordinate] == 0
        )
        moving_zero_sets.append(moving_zeros)
        deficits.append(ZZ(j - errors[index].hamming_weight()))
    require(all(len(zeros) == 1 for zeros in moving_zero_sets),
            "toy moving-zero size drift")
    require(len(set().union(*moving_zero_sets)) == M_line,
            "toy moving zeros no longer partition line support")
    require(sum(len(zeros) for zeros in moving_zero_sets) == M_line,
            "toy moving-zero sets overlap")
    require(deficits == [0] * 21, "toy line gained a deficit")

    independent_bases = []
    for basis in combinations(common_zero, 8):
        rank = K0_carrier.matrix_from_columns(list(basis)).rank()
        if rank == 8:
            independent_bases.append(tuple(basis))
            require(basis not in rich_basis_owner,
                    "one rich basis acquired two graph-line owners")
            rich_basis_owner[tuple(basis)] = line_index
    beta_line = ZZ(len(independent_bases))

    first = members[0]
    second = members[1]
    polynomial_direction = (
        code_polynomials[second] - code_polynomials[first]
    ) / (slopes[second] - slopes[first])
    polynomial_origin = (
        code_polynomials[first]
        - slopes[first] * polynomial_direction
    )
    require(all(
        code_polynomials[index]
        == polynomial_origin + slopes[index] * polynomial_direction
        for index in members
    ), "codeword pencil identity failed")
    require(polynomial_origin.degree() <= k - 1
            and polynomial_direction.degree() <= k - 1,
            "codeword pencil degree drift")
    common_gcd = gcd(polynomial_origin, polynomial_direction)
    gcd_degree = ZZ(common_gcd.degree())

    sparse_plant = ZZ(sum(
        a_line[index] == 0 and b_line[index] == 0
        for index in [0, 1]
    ))
    require((gcd_degree, sparse_plant) == (11, 2),
            "toy GCD/plant tuple drift")

    line_records.append({
        "line_index": ZZ(line_index),
        "first_member": ZZ(members[0]),
        "J": ZZ(len(members)),
        "M": M_line,
        "x": x_line,
        "delta_histogram": {"0": ZZ(len(members))},
        "common_zero_size_in_carrier": ZZ(len(common_zero)),
        "beta": beta_line,
        "gcd_degree": gcd_degree,
        "sparse_plant_size": sparse_plant,
        "contribution": beta_line * (ZZ(len(members)) - 20),
    })

require([record["beta"] for record in line_records]
        == [161, 165, 165, 161, 165],
        "rich-line beta profile drift")

# Directly enumerate only bases appearing in one of the 105 size-12 masks.
# This is 105*C(12,8)=51,975 incidences, not C(32,8).
basis_multiplicity = defaultdict(ZZ)
candidate_mask_basis_incidences = ZZ(0)
valid_mask_basis_incidences = ZZ(0)
for mask in zero_masks:
    require(len(mask) == 12, "complete carrier mask size drift")
    for basis in combinations(mask, 8):
        candidate_mask_basis_incidences += 1
        if K0_carrier.matrix_from_columns(list(basis)).rank() == 8:
            basis_multiplicity[tuple(basis)] += 1
            valid_mask_basis_incidences += 1

direct_excess = ZZ(sum(
    max(ZZ(0), multiplicity - 20)
    for multiplicity in basis_multiplicity.values()
))
atlas_excess = ZZ(sum(record["contribution"] for record in line_records))
maximum_multiplicity = max(basis_multiplicity.values())

require(candidate_mask_basis_incidences == 51_975,
        "candidate incidence count drift")
require(valid_mask_basis_incidences == 51_765,
        "valid incidence count drift")
require(len(basis_multiplicity) == 35_238,
        "distinct valid basis count drift")
require(maximum_multiplicity == 21, "maximum basis multiplicity drift")
require(direct_excess == atlas_excess == 817,
        "direct and atlas excess diverged")

for basis, multiplicity in basis_multiplicity.items():
    if multiplicity >= 21:
        require(basis in rich_basis_owner,
                "rich direct basis has no graph-line owner")
        line_index = rich_basis_owner[basis]
        require(multiplicity == line_records[line_index]["J"],
                "direct multiplicity differs from graph-line size")
require(len(rich_basis_owner) == 817,
        "rich basis owner count drift")

payload = {
    "schema": "rs-mca-m1-kb-branch3-rank9-rich-pencil-atlas-v1-sage",
    "status": "PASS",
    "classification": "EXACT_GENERIC_LOCAL_RICH_PENCIL_ATLAS_CONTROL",
    "field": {
        "cardinality": ZZ(F.cardinality()),
        "degree": degree,
    },
    "row": {"n": n, "k": k, "R": R, "j": j, "A": A},
    "selector": {
        "declared_slope_count": ZZ(len(slopes)),
        "affine_difference_rank": ZZ(affine_rank),
        "raw_witness_rank": ZZ(raw_rank),
        "carrier_excess": nu,
        "all_deficits_zero": True,
    },
    "atlas": {
        "rich_line_count": ZZ(len(line_records)),
        "line_records": line_records,
        "candidate_mask_basis_incidences": candidate_mask_basis_incidences,
        "valid_mask_basis_incidences": valid_mask_basis_incidences,
        "distinct_valid_bases": ZZ(len(basis_multiplicity)),
        "maximum_basis_multiplicity": ZZ(maximum_multiplicity),
        "direct_excess": direct_excess,
        "atlas_excess": atlas_excess,
        "identity_verified": direct_excess == atlas_excess,
    },
    "scope_guards": {
        "generic_local_control": True,
        "koalabear_domain_instantiated": False,
        "full_bad_set_exhausted": False,
        "deployed_aggregate_gate_proved": False,
        "ledger_movement": 0,
    },
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       default=int)
payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
print(json.dumps(payload, sort_keys=True, default=int))
