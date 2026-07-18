#!/usr/bin/env sage
"""Exact core-source coordinate-cover census for the n=36, k=14 t=2 toy row.

The dynamic program exhausts every 12-root core product state and every
13-root nonzero-locator product state in B=D\{a,b,c}.  For each core-derived
source line it computes the full post-deep slope envelope and the exact
single-coordinate availability intersection

    A_eta = union {S : |S|=13 and S is compatible at slope eta}.

A nonempty intersection over eta proves the existing low-carrier alternative.
An empty intersection proves high carrier only for the full post-deep toy
envelope; it is deliberately reported as UNRESOLVED_SOURCE_MAP because the
earlier first-match owner projections are not source-bound.
"""

import hashlib
import json
from collections import Counter

import numpy as np


SCHEMA = "rs-mca-m1-kb-branch3-t2-core-source-coordinate-cover-v1-sage"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def histogram(values):
    return {
        str(key): int(count)
        for key, count in sorted(Counter(int(value) for value in values).items())
    }


def field_coordinates(value):
    coefficients = list(value)
    require(len(coefficients) <= 2, "quadratic coordinate overflow")
    coefficients += [0] * (2 - len(coefficients))
    return [int(coefficient) for coefficient in coefficients]


def build_multiplication_table(p, u2_constant, u2_linear):
    q = p * p
    values = np.arange(q, dtype=np.int64)
    left = values[:, None]
    right = values[None, :]
    a = left % p
    b = left // p
    c = right % p
    d = right // p
    return (
        (a * c + u2_constant * b * d) % p
        + p * ((a * d + b * c + u2_linear * b * d) % p)
    ).astype(np.int16)


def vector_add(left, right, p):
    left = np.asarray(left, dtype=np.int64)
    right = np.asarray(right, dtype=np.int64)
    return (
        (left % p + right % p) % p
        + p * ((left // p + right // p) % p)
    )


def subset_product_dp(ratio_pairs, q, multiplication, maximum_size):
    """Return exact subset counts and coordinate-union masks by product pair."""

    state_count = q * q
    counts = np.zeros((maximum_size + 1, state_count), dtype=np.int64)
    masks = np.zeros((maximum_size + 1, state_count), dtype=np.uint64)
    one_key = q + 1
    counts[0, one_key] = 1
    keys = np.arange(state_count, dtype=np.int64)
    product_b = keys // q
    product_c = keys % q

    for position, (ratio_b, ratio_c) in enumerate(ratio_pairs):
        destination = (
            multiplication[product_b, ratio_b].astype(np.int64) * q
            + multiplication[product_c, ratio_c].astype(np.int64)
        )
        require(len(np.unique(destination)) == state_count,
                "nonzero ratio multiplication stopped being a permutation")
        upper = min(maximum_size, position + 1)
        bit = np.uint64(1 << position)
        for size in range(upper, 0, -1):
            sources = np.flatnonzero(counts[size - 1])
            destinations = destination[sources]
            require(len(np.unique(destinations)) == len(destinations),
                    "subset transition destination collision")
            counts[size, destinations] += counts[size - 1, sources]
            masks[size, destinations] |= masks[size - 1, sources] | bit

    return counts, masks


def brute_force_crosscheck(ratio_pairs, q, multiplication):
    """Cross-check the DP recurrence on a deterministic six-point fixture."""

    from itertools import combinations

    fixture = ratio_pairs[:6]
    target_size = 3
    counts, masks = subset_product_dp(fixture, q, multiplication, target_size)
    brute_counts = np.zeros(q * q, dtype=np.int64)
    brute_masks = np.zeros(q * q, dtype=np.uint64)
    for subset in combinations(range(len(fixture)), target_size):
        product_b = 1
        product_c = 1
        mask = 0
        for position in subset:
            ratio_b, ratio_c = fixture[position]
            product_b = int(multiplication[product_b, ratio_b])
            product_c = int(multiplication[product_c, ratio_c])
            mask |= 1 << position
        key = product_b * q + product_c
        brute_counts[key] += 1
        brute_masks[key] |= np.uint64(mask)
    require(np.array_equal(counts[target_size], brute_counts),
            "reduced-fixture subset counts disagree with brute force")
    require(np.array_equal(masks[target_size], brute_masks),
            "reduced-fixture availability masks disagree with brute force")
    return {
        "fixture_coordinate_count": len(fixture),
        "fixture_subset_size": target_size,
        "fixture_subset_count": int(sum(brute_counts)),
        "counts_and_masks_match": True,
    }


p = 17
q = p * p
base = GF(p)
polynomial_ring = PolynomialRing(base, "z")
z = polynomial_ring.gen()
modulus = z**2 + 16 * z + 3
require(modulus.is_irreducible(), "quadratic modulus became reducible")
field = GF(q, name="u", modulus=modulus)
u = field.gen()
require(u.multiplicative_order() == q - 1, "u stopped being primitive")

# u^2 = 14 + u in this presentation.
multiplication = build_multiplication_table(p, 14, 1)


def encode(value):
    constant, linear = field_coordinates(value)
    return constant + p * linear


require(int(multiplication[p, p]) == encode(u * u) == 14 + p,
        "manual/Sage quadratic multiplication mismatch")
for left in range(q):
    for right in range(q):
        sage_left = field(left % p) + field(left // p) * u
        sage_right = field(right % p) + field(right // p) * u
        require(int(multiplication[left, right])
                == encode(sage_left * sage_right),
                "manual multiplication table disagrees with Sage")

inverse = np.zeros(q, dtype=np.int16)
for value in range(1, q):
    candidates = np.flatnonzero(multiplication[value] == 1)
    require(len(candidates) == 1, "field inverse ceased to be unique")
    inverse[value] = int(candidates[0])

omega = u**8
require(field_coordinates(omega) == [12, 16]
        and omega.multiplicative_order() == 36,
        "cyclic-domain generator drift")
domain = [omega**index for index in range(36)]
require(len(set(domain)) == 36 and all(domain), "cyclic domain drift")
a, b, c = domain[:3]
B = tuple(range(3, 36))

ratio_pairs = []
for index in B:
    denominator = a - domain[index]
    ratio_b = (b - domain[index]) / denominator
    ratio_c = (c - domain[index]) / denominator
    encoded_b = encode(ratio_b)
    encoded_c = encode(ratio_c)
    require(encoded_b != 0 and encoded_c != 0,
            "source ratio vanished on B")
    ratio_pairs.append((encoded_b, encoded_c))

brute_force_control = brute_force_crosscheck(ratio_pairs, q, multiplication)
counts, masks = subset_product_dp(ratio_pairs, q, multiplication, 13)
require(int(counts[12].sum()) == int(binomial(33, 12)),
        "12-core DP did not exhaust all cores")
require(int(counts[13].sum()) == int(binomial(33, 13)),
        "13-root DP did not exhaust all locator supports")

# Reversing the coordinate order must preserve state counts and must reverse
# the availability-mask bit numbering.  This is an independent recurrence-
# order check, not a mathematical symmetry assumption.
reverse_counts, reverse_masks = subset_product_dp(
    tuple(reversed(ratio_pairs)), q, multiplication, 13
)
require(np.array_equal(counts, reverse_counts),
        "subset-product counts depend on coordinate order")


def reverse_bits(value, width):
    result = 0
    for position in range(width):
        if int(value) >> position & 1:
            result |= 1 << (width - 1 - position)
    return result


for size in (12, 13):
    reversed_back = np.fromiter(
        (reverse_bits(value, len(B)) for value in reverse_masks[size]),
        dtype=np.uint64,
        count=q * q,
    )
    require(np.array_equal(masks[size], reversed_back),
            "availability masks depend on coordinate order")

core_states = np.flatnonzero(counts[12])
witness_states = np.flatnonzero(counts[13])
require(all((core_states // q) != 0) and all((core_states % q) != 0),
        "core product state gained zero coordinate")
require(all((witness_states // q) != 0) and all((witness_states % q) != 0),
        "witness product state gained zero coordinate")
require(len(witness_states) == (q - 1)**2
        and np.all(masks[13, witness_states] == np.uint64((1 << len(B)) - 1)),
        "a nonzero locator product state lacks a coordinate")

# For a 12-root core with products g_b=Q0(b), g_c=Q0(c),
# alpha=g_c*(b-c)/(b-a) and beta=g_c*(c-a)/(g_b*(b-a)).
alpha_factor = encode((b - c) / (b - a))
beta_factor = encode((c - a) / (b - a))
all_B_mask = (1 << len(B)) - 1
etas = np.arange(1, q, dtype=np.int64)

line_records = []
batch_size = 512
for start in range(0, len(core_states), batch_size):
    states = core_states[start:start + batch_size].astype(np.int64)
    product_b = states // q
    product_c = states % q
    alphas = multiplication[product_c, alpha_factor].astype(np.int64)
    ratios = multiplication[product_c, inverse[product_b]].astype(np.int64)
    betas = multiplication[ratios, beta_factor].astype(np.int64)
    require(np.all(alphas != 0) and np.all(betas != 0),
            "core-derived source coefficient vanished")

    beta_eta = multiplication[betas[:, None], etas[None, :]].astype(np.int64)
    targets = vector_add(alphas[:, None], beta_eta, p)
    state_keys = etas[None, :] * q + targets
    reachable = (targets != 0) & (counts[13, state_keys] != 0)
    gamma_counts = reachable.sum(axis=1)
    require(np.all(gamma_counts >= 21),
            "core-derived rich pencil lost one of its 21 slopes")

    availability = masks[13, state_keys].copy()
    availability[~reachable] = np.uint64(all_B_mask)
    common_masks = np.bitwise_and.reduce(availability, axis=1)

    for offset, state in enumerate(states):
        alpha = int(alphas[offset])
        beta = int(betas[offset])
        common_mask = int(common_masks[offset])
        line_records.append([
            alpha,
            beta,
            int(gamma_counts[offset]),
            common_mask,
            int(counts[12, state]),
            int(state),
        ])

line_records.sort(key=lambda record: (record[0], record[1]))
line_ids = [record[0] * q + record[1] for record in line_records]
require(len(line_ids) == len(set(line_ids)) == len(core_states),
        "core product states did not map injectively to source lines")

low_records = [record for record in line_records if record[3] != 0]
high_records = [record for record in line_records if record[3] == 0]
require(len(low_records) + len(high_records) == len(line_records),
        "source-line coordinate-cover partition drift")


def public_line(record):
    alpha, beta, gamma_count, common_mask, core_count, state = record
    common_coordinates = [
        B[position]
        for position in range(len(B))
        if common_mask >> position & 1
    ]
    return {
        "alpha_coordinates": [alpha % p, alpha // p],
        "beta_coordinates": [beta % p, beta // p],
        "post_deep_slope_count": gamma_count,
        "common_available_coordinates": common_coordinates,
        "common_available_coordinate_count": len(common_coordinates),
        "core_subset_count": core_count,
        "core_product_state": [state // q, state % q],
        "classification": (
            "AT_OR_BEFORE_LOW_CARRIER"
            if common_mask
            else "UNRESOLVED_SOURCE_MAP"
        ),
    }


canonical_core = tuple(range(3, 15))
canonical_product_b = 1
canonical_product_c = 1
for index in canonical_core:
    position = index - 3
    canonical_product_b = int(
        multiplication[canonical_product_b, ratio_pairs[position][0]]
    )
    canonical_product_c = int(
        multiplication[canonical_product_c, ratio_pairs[position][1]]
    )
canonical_state = canonical_product_b * q + canonical_product_c
canonical_alpha = int(multiplication[canonical_product_c, alpha_factor])
canonical_ratio = int(
    multiplication[canonical_product_c, inverse[canonical_product_b]]
)
canonical_beta = int(multiplication[canonical_ratio, beta_factor])
require([canonical_alpha % p, canonical_alpha // p] == [13, 7]
        and [canonical_beta % p, canonical_beta // p] == [5, 14],
        "canonical predecessor source coefficients drift")
canonical_record = next(
    record for record in line_records
    if record[0] == canonical_alpha and record[1] == canonical_beta
)
require(canonical_record[5] == canonical_state,
        "canonical line/core product state mismatch")
require(canonical_record[2] == 287 and canonical_record[3] & 1,
        "canonical line lost its full post-deep root-3 cover")

# Replay the predecessor's fixed-root-3 inventory by a different DP shape:
# remove coordinate 3, enumerate all 12-subsets of the other 32 coordinates,
# and divide every target product pair by coordinate 3's ratios.  This must
# reproduce the independent meet-in-the-middle constants from #901.
fixed_root_position = 0
fixed_root_ratio_b, fixed_root_ratio_c = ratio_pairs[fixed_root_position]
fixed_counts, _ = subset_product_dp(
    ratio_pairs[1:], q, multiplication, 12
)
fixed_root_counts = []
for eta in range(1, q):
    target_c = int(vector_add(
        canonical_alpha,
        multiplication[canonical_beta, eta],
        p,
    ))
    if target_c == 0:
        continue
    predecessor_b = int(
        multiplication[eta, inverse[fixed_root_ratio_b]]
    )
    predecessor_c = int(
        multiplication[target_c, inverse[fixed_root_ratio_c]]
    )
    count = int(fixed_counts[12, predecessor_b * q + predecessor_c])
    require(count > 0, "canonical fixed-root cover lost a post-deep slope")
    fixed_root_counts.append(count)
require(len(fixed_root_counts) == 287
        and sum(fixed_root_counts) == 780_907
        and (min(fixed_root_counts), max(fixed_root_counts)) == (2_571, 2_833),
        "canonical fixed-root replay disagrees with #901")

compact_records = [record[:5] for record in line_records]
records_hash = canonical_hash(compact_records)
gamma_counts = [record[2] for record in line_records]
common_counts = [int(record[3]).bit_count() for record in line_records]
core_counts = [record[4] for record in line_records]
core_histogram = histogram(core_counts)
core_histogram_hash = canonical_hash(core_histogram)

require(len(core_states) == len(witness_states) == (q - 1)**2,
        "nonzero product-pair coverage is not complete")
require(len(line_records) == len(low_records) == (q - 1)**2
        and len(high_records) == 0,
        "core-source coordinate-cover census did not close uniformly")
require(set(gamma_counts) == {q - 2},
        "a core-derived line lost a post-deep slope")
require(set(common_counts) == {len(B)},
        "a core-derived line lost a universally available coordinate")
require(records_hash
        == "384b40b21b1cfc07420c14f75a2e3de37096b41b6c31c5cadc0e43a5c513a332",
        "compact source-line record hash drift")
require(core_histogram_hash
        == "b9dea1936974d9e6c0b91f6d9bd4ec006362bcee009c1a33e2bb4c7a4d6e17a8",
        "core multiplicity histogram hash drift")

payload = {
    "schema": SCHEMA,
    "status": "PASS",
    "classification": "EXACT_TOY_CORE_SOURCE_COORDINATE_COVER_CENSUS",
    "field": {
        "characteristic": p,
        "degree": 2,
        "cardinality": q,
        "modulus_coefficients_ascending": [3, 16, 1],
        "primitive_generator_order": int(u.multiplicative_order()),
        "omega_coordinates": field_coordinates(omega),
        "omega_order": int(omega.multiplicative_order()),
    },
    "row": {"n": 36, "k": 14, "R": 22, "j": 20, "A": 16, "t": 2},
    "dynamic_program": {
        "coordinate_count": len(B),
        "core_size": 12,
        "locator_root_size": 13,
        "state_space_size_per_cardinality": q * q,
        "core_subset_count": int(counts[12].sum()),
        "locator_subset_count": int(counts[13].sum()),
        "reachable_core_product_states": len(core_states),
        "reachable_locator_product_states": len(witness_states),
        "availability_mask_bits": len(B),
        "full_witness_universe_enumerated": True,
        "every_nonzero_locator_state_has_full_coordinate_mask": True,
        "coordinate_order_invariant": True,
        "brute_force_control": brute_force_control,
        "canonical_fixed_root_crosscheck": {
            "fixed_coordinate": 3,
            "post_deep_slope_count": len(fixed_root_counts),
            "compatible_support_count": sum(fixed_root_counts),
            "witness_count_min": min(fixed_root_counts),
            "witness_count_max": max(fixed_root_counts),
            "matches_predecessor_mitm": True,
        },
    },
    "source_line_census": {
        "source_line_count": len(line_records),
        "source_line_map_injective_on_product_states": True,
        "post_deep_slope_count_min": min(gamma_counts),
        "post_deep_slope_count_max": max(gamma_counts),
        "post_deep_slope_count_histogram": histogram(gamma_counts),
        "core_multiplicity_min": min(core_counts),
        "core_multiplicity_max": max(core_counts),
        "core_multiplicity_distinct_values": len(core_histogram),
        "core_multiplicity_histogram_sha256": core_histogram_hash,
        "common_available_coordinate_count_histogram": histogram(common_counts),
        "low_carrier_line_count": len(low_records),
        "unresolved_source_map_line_count": len(high_records),
        "compact_line_records_sha256": records_hash,
        "low_examples": [public_line(record) for record in low_records[:3]],
        "unresolved_examples": [
            public_line(record) for record in high_records[:8]
        ],
    },
    "canonical_predecessor_line": public_line(canonical_record),
    "coordinate_cover_lemma": {
        "fixed_gamma_identity": (
            "kappa_star=max(0,k-3-max_selector_common_root_count)"
        ),
        "k14_low_equivalence": (
            "kappa_star<=10 iff intersection_eta A_eta is nonempty"
        ),
        "low_direction_deletion_monotone": True,
        "high_direction_deletion_monotone": False,
        "availability_is_full_for_every_censused_line": True,
    },
    "first_match": {
        "earlier_owner_projections_source_bound": False,
        "literal_first_match_gamma_available": False,
        "low_lines_paid_at_or_before_low_carrier": True,
        "empty_cover_lines_are_only_full_post_deep_toy_candidates": True,
        "empty_cover_line_classification": "UNRESOLVED_SOURCE_MAP",
    },
    "scope_guards": {
        "toy_scale_only": True,
        "deployed_field_instantiated": False,
        "koalabear_rank9_closed": False,
        "rank9_geometry_checked_for_every_source_line": False,
        "ledger_movement": 0,
        "U_Q_determined": False,
        "U_A_determined": False,
        "lean_authorized": False,
    },
}
payload["payload_sha256"] = canonical_hash(payload)
print(json.dumps(payload, sort_keys=True, default=int))
