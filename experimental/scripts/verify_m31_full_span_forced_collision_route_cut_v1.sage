#!/usr/bin/env sage
"""Independent Sage replay for the full-span forced-collision route cut."""

from sage.all import GF, Matrix, PolynomialRing, vector
import hashlib
import itertools
import json
from pathlib import Path


P = 17
K = 7
N = 14
J = 6
DOMAIN = tuple(range(N))
MOMENTS = (4, 0, 1, 3, 4, 10, 8)
RECEIVED = (4, 3, 11, 5, 13, 6, 9, 0, 0, 0, 0, 0, 0, 0)
ANCHOR_COUNT = 45

F = GF(P)
R = PolynomialRing(F, "X")
X = R.gen()
ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json"

checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def locator(points):
    out = R.one()
    for point in points:
        out *= X - F(point)
    return out


def functional(polynomial):
    require(polynomial.degree() < K, "functional degree range")
    return sum(polynomial[degree] * F(MOMENTS[degree]) for degree in range(K))


def exact_support(points):
    polynomial = locator(points)
    return (
        all(functional(X**shift * polynomial) == 0
            for shift in range(K - len(points)))
        and all(functional(polynomial // (X - F(point))) != 0 for point in points)
    )


def support_order_key(points):
    return tuple(1 if point in points else 0 for point in DOMAIN)


def coefficients(polynomial):
    return [int(polynomial[degree]) for degree in range(K)]


def lagrange(samples):
    answer = R.zero()
    for index, (x_value, y_value) in enumerate(samples):
        basis = R.one()
        denominator = F.one()
        for other, (z_value, _) in enumerate(samples):
            if other == index:
                continue
            basis *= X - F(z_value)
            denominator *= F(x_value - z_value)
        answer += F(y_value) * basis / denominator
    return answer


def collision_polynomial(left, right, point):
    return (
        right.derivative()(F(point)) * (left // (X - F(point)))
        - left.derivative()(F(point)) * (right // (X - F(point)))
    )


def exact_set_packing(masks):
    states = {0: (0, ())}
    for index, mask in enumerate(masks):
        require(mask != 0, "nonempty collision mask")
        for used, (count, chosen) in list(states.items()):
            if used & mask:
                continue
            combined = used | mask
            candidate = (count + 1, chosen + (index,))
            if combined not in states or candidate[0] > states[combined][0]:
                states[combined] = candidate
    return max(states.values())


def exact_root_transversals(masks):
    for size in range(N + 1):
        witnesses = []
        for points in itertools.combinations(range(N), size):
            candidate = sum(1 << point for point in points)
            if all(candidate & mask for mask in masks):
                witnesses.append(points)
        if witnesses:
            return size, tuple(witnesses)
    raise RuntimeError("no transversal")


all_supports = tuple(itertools.combinations(DOMAIN, J))
layer = tuple(sorted(
    (support for support in all_supports if exact_support(support)),
    key=support_order_key,
))
require(len(all_supports) == 3003, "support universe")
require(len(layer) == 137, "complete layer size")

locators = {support: locator(support) for support in layer}
locator_matrix = Matrix(F, [coefficients(locators[support]) for support in layer])
require(locator_matrix.rank() == 6 == K - 1, "full syndrome-hyperplane span")
require(all(functional(locators[support]) == 0 for support in layer),
        "locator containment")

codewords = {}
for support in layer:
    agreements = tuple(point for point in DOMAIN if point not in support)
    codeword = lagrange(tuple((point, RECEIVED[point]) for point in agreements[:K]))
    require(all(codeword(F(point)) == F(RECEIVED[point]) for point in agreements),
            "agreement reconstruction")
    require(all(codeword(F(point)) != F(RECEIVED[point]) for point in support),
            "exact error reconstruction")
    codewords[support] = codeword
require(len(set(codewords.values())) == 137, "distinct codewords")

common_count = 0
collisions = []
proper_count = 0
incidence_serial = []
for left_index, left_support in enumerate(layer):
    left = locators[left_support]
    for right_index in range(left_index + 1, len(layer)):
        right_support = layer[right_index]
        right = locators[right_support]
        for point in sorted(set(left_support).intersection(right_support)):
            common_count += 1
            g = collision_polynomial(left, right, point)
            require(g != 0, "nonzero collision form")

            common_locator = left.gcd(right).monic()
            common_without_point = common_locator // (X - F(point))
            left_reduced = left // common_locator
            right_reduced = right // common_locator
            factorized = (
                common_without_point(F(point)) * common_without_point
                * (right_reduced(F(point)) * left_reduced
                   - left_reduced(F(point)) * right_reduced)
            )
            require(g == factorized, "collision factorization")
            require(g % common_locator == 0, "full common locator factor")

            actual = (
                codewords[left_support](F(point))
                == codewords[right_support](F(point))
            )
            require(actual == (functional(g) == 0), "collision functional")
            incidence_serial.append(
                f"{left_index},{right_index},{point},{int(actual)}:"
                + ",".join(map(str, coefficients(g)))
            )
            if actual:
                collisions.append((left_index, right_index, point, g))
            else:
                proper_count += 1

require(common_count == 23813, "common incidence count")
require(len(collisions) == 1326, "collision incidence count")
require(proper_count == 22487, "proper incidence count")

collision_rank = Matrix(F, [coefficients(record[3]) for record in collisions]).rank()
require(collision_rank == 4, "collision polynomial span rank")
require(locator_matrix.stack(Matrix(F, [coefficients(record[3]) for record in collisions])).rank() == 6,
        "all collision polynomials in locator span")
require(len(set(record[3] for record in collisions)) == 1219,
        "distinct collision polynomial count")

collision_lookup = {(left, right, point) for left, right, point, _ in collisions}
anchors = layer[:ANCHOR_COUNT]
extras = layer[ANCHOR_COUNT:]
anchor_locator_rank = Matrix(
    F, [coefficients(locators[support]) for support in anchors]
).rank()
require(anchor_locator_rank == 6 == K - 1,
        "anchor locators span the syndrome hyperplane")
masks = []
key_records = []
marked_key_locator_ranks = []
anchor_extra_incidences = 0
for extra_offset, extra in enumerate(extras):
    extra_index = ANCHOR_COUNT + extra_offset
    key_rank = Matrix(
        F,
        [coefficients(locators[support]) for support in anchors]
        + [coefficients(locators[extra])],
    ).rank()
    require(key_rank == 6 == K - 1,
            "every 46-column marked family spans the syndrome hyperplane")
    marked_key_locator_ranks.append(key_rank)
    mask = 0
    for anchor_index, anchor in enumerate(anchors):
        for point in set(anchor).intersection(extra):
            if (anchor_index, extra_index, point) in collision_lookup:
                anchor_extra_incidences += 1
                mask |= 1 << point
    require(mask != 0, "forced collision on every key")
    masks.append(mask)
    key_records.append({
        "extra_index_one_based": extra_offset + 1,
        "global_index_one_based": extra_index + 1,
        "support": list(extra),
        "forced_collision_roots": [point for point in DOMAIN if mask & (1 << point)],
    })

require(anchor_extra_incidences == 597, "anchor-extra collision count")
require(sum(int(mask).bit_count() for mask in masks) == 357, "deduplicated root mass")

packing, packing_indices = exact_set_packing(masks)
require(packing == 5, "packing optimum")
packing_witness = [key_records[index] for index in packing_indices]
transversal, transversals = exact_root_transversals(masks)
require(transversal == 6 and len(transversals) == 4, "transversal census")

layer_serial = ";".join(",".join(map(str, support)) for support in layer)
forced_serial = ";".join(
    f"{left},{right},{point}:" + ",".join(map(str, coefficients(g)))
    for left, right, point, g in collisions
)
key_serial = ";".join(
    f"{record['global_index_one_based']}:"
    + ",".join(map(str, record["forced_collision_roots"]))
    for record in key_records
)

manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
fixture = manifest["full_span_fixture"]
keys = manifest["forced_key_noncoalescence"]
require(fixture["ordered_layer_sha256"] == hashlib.sha256(layer_serial.encode("ascii")).hexdigest(),
        "layer digest")
require(fixture["incidence_table_sha256"] == hashlib.sha256(";".join(incidence_serial).encode("ascii")).hexdigest(),
        "incidence digest")
require(fixture["forced_collision_table_sha256"] == hashlib.sha256(forced_serial.encode("ascii")).hexdigest(),
        "forced collision digest")
require(keys["forced_key_table_sha256"] == hashlib.sha256(key_serial.encode("ascii")).hexdigest(),
        "key digest")
require(keys["five_union_witness"] == packing_witness, "packing witness")
require(keys["minimum_root_transversals"] == [list(points) for points in transversals],
        "transversal witnesses")
require(keys["anchor_containment_generator_rank"] == anchor_locator_rank == 6,
        "anchor full-span rank")
require(keys["minimum_marked_key_containment_rank"] == min(marked_key_locator_ranks) == 6,
        "minimum marked-key rank")
require(keys["maximum_marked_key_containment_rank"] == max(marked_key_locator_ranks) == 6,
        "maximum marked-key rank")
require(keys["every_marked_key_spans_syndrome_hyperplane"] is True,
        "every marked key full span")
require(manifest["scope"]["deployed_row_closed"] is False, "row remains open")
require(manifest["scope"]["ledger_movement"] == 0, "zero ledger movement")
require(manifest["deployed_context"]["deployed_full_span_is_proved"] is False,
        "toy does not prove deployed full span")

print("M31 full-span forced-collision independent Sage replay: PASS")
print("GF(17): layer=137 locator_rank=6 containment_dim=1")
print("incidences: common=23813 forced=1326 proper=22487 distinct_forced=1219")
print("keys: full_span=92/92 forced=92/92 packing=5 transversal=6")
print("scope: universal route cut only; M31 row OPEN; ledger movement=0")
print(f"checks={checks}")
