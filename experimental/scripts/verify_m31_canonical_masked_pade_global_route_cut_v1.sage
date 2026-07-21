"""Independent Sage replay of the canonical-masked global route cut.

This file recomputes the exact GF(17) received-word model, including a
nontrivial-padding bridge fixture, without importing the Python verifier.
It is a toy universal-implication falsifier, not an M31 counterexample.
"""

from itertools import combinations
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = (
    ROOT
    / "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json"
)

F = GF(17)
R.<X> = PolynomialRing(F)
K = 7
n = 14
radius = 6
agreement = 8
j = 6
D0 = 1
sigma = 4
domain = tuple(F(a) for a in range(n))
moments = tuple(F(a) for a in (4, 0, 1, 3, 4, 10, 8))


def locator(points):
    return R.prod(X - point for point in points)


def functional(polynomial):
    require(polynomial.degree() < K, "functional moment range")
    return sum(polynomial[degree] * moments[degree] for degree in range(K))


def divided_numerator(polynomial):
    answer = R.zero()
    for degree in range(1, polynomial.degree() + 1):
        for output_degree in range(degree):
            answer += (
                polynomial[degree]
                * moments[degree - 1 - output_degree]
                * X^output_degree
            )
    return answer


def exact_support(points):
    polynomial = locator(points)
    return all(
        functional(X^degree * polynomial) == 0
        for degree in range(K - len(points))
    ) and all(
        functional(polynomial // (X - point)) != 0 for point in points
    )


def incidence_key(points):
    return tuple(1 if point in points else 0 for point in domain)


def coefficient_list(polynomial):
    return [int(polynomial[degree]) for degree in range(polynomial.degree() + 1)]


def joint_relation_matrix(first_row, second_row, multiplier_width):
    output_length = max(
        max(polynomial.degree() + 1 for polynomial in first_row),
        max(polynomial.degree() + 1 for polynomial in second_row),
    ) + multiplier_width - 1
    equations = []
    for polynomial_row in (first_row, second_row):
        for output_degree in range(output_length):
            equation = []
            for polynomial in polynomial_row:
                for shift in range(multiplier_width):
                    degree = output_degree - shift
                    equation.append(
                        polynomial[degree]
                        if 0 <= degree <= polynomial.degree() else F.zero()
                    )
            equations.append(equation)
    return matrix(F, equations)


def joint_kernel_nullity(first_row, second_row, multiplier_width):
    coefficient_map = joint_relation_matrix(
        first_row, second_row, multiplier_width
    )
    return len(first_row) * multiplier_width - coefficient_map.rank()


# Reconstruct one received word realizing the moment functional.
domain_locator = locator(domain)
dual_weights = tuple(F.one() / domain_locator.derivative()(point) for point in domain)
moment_chart = matrix(F, K, K, lambda row, column:
                      dual_weights[column] * domain[column]^row)
require(moment_chart.det() != 0, "received-word moment chart singular")
first_values = moment_chart.solve_right(vector(F, moments))
received = tuple(first_values[index] if index < K else F.zero()
                 for index in range(n))
require(tuple(int(value) for value in received)
        == (4, 3, 11, 5, 13, 6, 9, 0, 0, 0, 0, 0, 0, 0),
        "received-word witness changed")
for degree in range(K):
    require(sum(received[index] * dual_weights[index] * domain[index]^degree
                for index in range(n)) == moments[degree],
            "received word does not realize moment functional")


# Nontrivial-padding bridge: the complete exact weight-five layer has Q != 1.
interior_weight = 5
interior_layer = tuple(
    points for points in combinations(domain, interior_weight)
    if exact_support(points)
)
expected_interior = (
    tuple(F(a) for a in (0, 3, 5, 8, 12)),
    tuple(F(a) for a in (0, 4, 10, 11, 13)),
    tuple(F(a) for a in (1, 2, 5, 6, 13)),
    tuple(F(a) for a in (1, 4, 7, 11, 12)),
)
require(interior_layer == expected_interior,
        "complete nontrivial-padding exact layer changed")

received_polynomial = R.lagrange_polynomial([
    (point, received[int(point)]) for point in domain
])
gamma = F(16)
require(gamma != 0, "collision scalar vanished")
padding_records = []
error_locators = []
padding_locators = []
canonical_locators = []
error_numerators = []
canonical_numerators = []
interpolation_numerators = []
for support in interior_layer:
    agreements = tuple(point for point in domain if point not in support)
    selected = agreements[:agreement]
    discarded = agreements[agreement:]
    require(len(discarded) == 1, "nontrivial padding degree changed")
    L = locator(support)
    Q = locator(discarded)
    W = L * Q
    B_L = divided_numerator(L)
    B_W = divided_numerator(W)
    require(Q != 1, "padding became trivial")
    require(B_W == Q * B_L, "B(LQ)=Q B(L) failed")
    require(W.gcd(B_W).monic() == Q.monic(), "gcd(W,B(W)) != Q")
    require((W // W.gcd(B_W).monic()).monic() == L.monic(),
            "saturation quotient did not recover L")

    outside = tuple(point for point in domain if point not in support)
    codeword = R.lagrange_polynomial([
        (point, received[int(point)]) for point in outside[:K]
    ])
    require(all(codeword(point) == received[int(point)] for point in outside),
            "interior codeword agreement failed")
    domain_over_W, remainder = domain_locator.quo_rem(W)
    require(remainder == 0, "W does not divide Lambda_D")
    reconstructed = received_polynomial + gamma^(-1) * domain_over_W * B_W
    require(reconstructed == codeword,
            "c=Y+gamma^-1(Lambda_D/W)B(W) failed")
    N = codeword * W
    transformed_N = received_polynomial * W + gamma^(-1) * domain_locator * B_W
    require(N == transformed_N,
            "N=YW+gamma^-1 Lambda_D B(W) failed")

    error_locators.append(L)
    padding_locators.append(Q)
    canonical_locators.append(W)
    error_numerators.append(B_L)
    canonical_numerators.append(B_W)
    interpolation_numerators.append(N)
    padding_records.append({
        "support": [int(point) for point in support],
        "selected_agreements": [int(point) for point in selected],
        "discarded_agreements": [int(point) for point in discarded],
        "L_coefficients": coefficient_list(L),
        "Q_coefficients": coefficient_list(Q),
        "W_coefficients": coefficient_list(W),
        "B_L_coefficients": coefficient_list(B_L),
        "B_W_coefficients": coefficient_list(B_W),
        "codeword_coefficients": coefficient_list(codeword),
        "interpolation_numerator_coefficients": coefficient_list(N),
    })

pair_factor_checks = 0
for left, right in combinations(range(len(interior_layer)), 2):
    omega_canonical = (
        canonical_locators[left] * canonical_numerators[right]
        - canonical_locators[right] * canonical_numerators[left]
    )
    omega_error = (
        error_locators[left] * error_numerators[right]
        - error_locators[right] * error_numerators[left]
    )
    require(omega_canonical
            == padding_locators[left] * padding_locators[right] * omega_error,
            "canonical pair minor lost a padding factor")
    pair_factor_checks += 1
require(pair_factor_checks == 6, "canonical pair-factor count")

kernel_replay = []
saturated_error_locators = [
    error_locators[index] * padding_locators[index]
    for index in range(len(error_locators))
]
saturated_error_numerators = [
    error_numerators[index] * padding_locators[index]
    for index in range(len(error_numerators))
]
require(saturated_error_locators == canonical_locators
        and saturated_error_numerators == canonical_numerators,
        "diagonal padding did not recover the canonical masked row")
for width in range(1, 7):
    masked_matrix = joint_relation_matrix(
        canonical_locators, canonical_numerators, width)
    saturated_matrix = joint_relation_matrix(
        saturated_error_locators, saturated_error_numerators, width)
    require(masked_matrix == saturated_matrix,
            "diagonal-saturation relation conditions changed")
    interpolation_matrix = joint_relation_matrix(
        canonical_locators, interpolation_numerators, width)
    masked = len(canonical_locators) * width - masked_matrix.rank()
    interpolation = (
        len(canonical_locators) * width - interpolation_matrix.rank()
    )
    require(masked == interpolation,
            "masked/interpolation right-kernel dimensions differ")
    combined_rank = masked_matrix.stack(interpolation_matrix).rank()
    require(masked_matrix.rank() == interpolation_matrix.rank() == combined_rank,
            "masked/interpolation right-kernel subspaces differ")
    kernel_replay.append({
        "multiplier_width": width,
        "masked_pair_nullity": int(masked),
        "interpolation_pair_nullity": int(interpolation),
        "combined_relation_rank": int(combined_rank),
    })
require([entry["masked_pair_nullity"] for entry in kernel_replay]
        == [0, 2, 4, 6, 8, 10], "right-kernel profile changed")


# Complete boundary exact layer and its canonical first-45/excess keys.
raw_layer = tuple(
    points for points in combinations(domain, j) if exact_support(points)
)
layer = tuple(sorted(raw_layer, key=incidence_key))
require(len(layer) == 137, "full exact boundary layer changed")
core = set(layer[0])
for support in layer[1:]:
    core.intersection_update(support)
require(not core, "full boundary layer acquired a common core")

locators = {support: locator(support) for support in layer}
numerators = {support: divided_numerator(locators[support]) for support in layer}
codewords = {}
for support in layer:
    outside = tuple(point for point in domain if point not in support)
    codeword = R.lagrange_polynomial([
        (point, received[int(point)]) for point in outside[:K]
    ])
    require(codeword.degree() < K, "codeword degree exceeded K")
    require(all(codeword(point) == received[int(point)] for point in outside),
            "eighth agreement failed")
    require(all(codeword(point) != received[int(point)] for point in support),
            "exact support lost an error")
    codewords[support] = codeword
require(len(set(codewords.values())) == len(layer),
        "exact support/codeword projection is not injective")

anchors = layer[:45]
extras = layer[45:]
require(len(extras) == 92, "canonical marked-key count changed")
collision_masks = []
key_records = []
constant_nullities = []
polynomial_pair_checks = 0
collision_point_checks = 0
factor_checks = 0
for extra_index, extra in enumerate(extras):
    packet = anchors + (extra,)
    coefficient_rows = []
    for degree in range(j + 1):
        coefficient_rows.append([locators[support][degree] for support in packet])
    for degree in range(j):
        coefficient_rows.append([numerators[support][degree] for support in packet])
    constant_map = matrix(F, coefficient_rows)
    nullity = 46 - constant_map.rank()
    require(nullity >= 3, "key lost three degree-zero coupled rows")
    constant_nullities.append(int(nullity))

    for left, right in combinations(packet, 2):
        omega = (
            locators[left] * numerators[right]
            - locators[right] * numerators[left]
        )
        require(omega != 0, "pair minor vanished")
        polynomial_pair_checks += 1

    mask = 0
    for anchor in anchors:
        P_i, P_e = locators[anchor], locators[extra]
        B_i, B_e = numerators[anchor], numerators[extra]
        overlap = P_i.gcd(P_e).monic()
        omega = P_i * B_e - P_e * B_i
        quotient, remainder = omega.quo_rem(overlap)
        require(remainder == 0 and quotient != 0,
                "pair collision quotient failed")
        require(quotient.degree() <= sigma - overlap.degree(),
                "collision quotient degree exceeded sigma")
        factor_checks += 1
        for point in set(anchor).intersection(extra):
            rho_i = B_i(point) / P_i.derivative()(point)
            rho_e = B_e(point) / P_e.derivative()(point)
            normalized = (rho_i == rho_e)
            actual = (codewords[anchor](point) == codewords[extra](point))
            require(normalized == actual,
                    "normalized escape does not match actual collision")
            require((quotient(point) == 0) == actual,
                    "collision quotient root mismatch")
            if actual:
                mask |= 1 << int(point)
            collision_point_checks += 1
    require(mask != 0, "fixture key acquired empty collision union")
    roots = [point for point in range(n) if mask & (1 << point)]
    collision_masks.append(mask)
    key_records.append({
        "extra_index_one_based": extra_index + 1,
        "global_index_one_based": 46 + extra_index,
        "support": [int(point) for point in extra],
        "collision_roots": roots,
    })

require(polynomial_pair_checks == 95220, "pair-minor count changed")
require(factor_checks == 4140, "anchor-extra factor count changed")
require(collision_point_checks == 9914, "collision point count changed")
require(min(constant_nullities) == 40, "minimum constant nullity changed")

# Exhaustive set packing on the 14-point collision masks.
states = {0: (0, ())}
for index, mask in enumerate(collision_masks):
    for used, (count, chosen) in list(states.items()):
        if used & mask:
            continue
        combined = used | mask
        candidate = (count + 1, chosen + (index,))
        if combined not in states or candidate[0] > states[combined][0]:
            states[combined] = candidate
optimum, witness_indices = max(states.values())
require(optimum == 5, "exact disjoint-union optimum changed")
witness = [key_records[index] for index in witness_indices]
require([entry["extra_index_one_based"] for entry in witness]
        == [48, 62, 67, 77, 80], "five-union witness changed")
require(all(
    collision_masks[left] & collision_masks[right] == 0
    for left, right in combinations(witness_indices, 2)
), "five witness unions are not pairwise disjoint")

# Exhaustive root-transversal census on the same 14-point family.
minimum_transversals = []
transversal_minimum = None
for size in range(n + 1):
    for points in combinations(range(n), size):
        candidate = sum(1 << point for point in points)
        if all(candidate & mask for mask in collision_masks):
            minimum_transversals.append(tuple(points))
    if minimum_transversals:
        transversal_minimum = size
        break
require(transversal_minimum == 6, "exact root-transversal minimum changed")
require(minimum_transversals == [
    (3, 5, 6, 7, 8, 9),
    (3, 5, 7, 8, 9, 13),
    (3, 6, 7, 8, 9, 12),
    (6, 7, 8, 9, 11, 12),
], "complete minimum root-transversal list changed")

layer_serial = ";".join(
    ",".join(str(int(point)) for point in support) for support in layer
).encode("ascii")
collision_serial = ";".join(
    "{}:{}".format(
        ",".join(str(int(point)) for point in support), mask
    )
    for support, mask in zip(extras, collision_masks)
).encode("ascii")
layer_hash = hashlib.sha256(layer_serial).hexdigest()
collision_hash = hashlib.sha256(collision_serial).hexdigest()
require(layer_hash == "e7affd99b9650add0a334a56cededf48f76338c5dd9209bcb39017aa308c17a8",
        "layer digest changed")
require(collision_hash == "9e0c2f63e5400893c28c8b144ed85dd9b44e4b8f581bb9d9a91581bc591f7aeb",
        "collision digest changed")


# Bind the independent replay to the sealed certificate.
require(MANIFEST_PATH.is_file(), "sealed manifest missing")
manifest = json.loads(MANIFEST_PATH.read_text(encoding="ascii"))
require(manifest["schema"]
        == "rs-mca-m31-canonical-masked-pade-global-route-cut-v1",
        "manifest schema mismatch")
require(manifest["architecture_id"]
        == "M31_CANONICAL_MASKED_PADE_GLOBAL_ROUTE_CUT_V1",
        "manifest architecture mismatch")
require(manifest["scope"]["deployed_symbolic_bridge_proved"] is True
        and manifest["scope"]["toy_falsifier_scale"] is True
        and manifest["scope"]["is_m31_counterexample"] is False
        and manifest["scope"]["ledger_movement"] == 0,
        "manifest scope mismatch")
bridge = manifest["canonical_masked_bridge"]
require(bridge["records"] == padding_records, "manifest padding records mismatch")
require(bridge["kernel_dimension_replay"] == kernel_replay,
        "manifest kernel replay mismatch")
require(bridge["nontrivial_padding"] is True
        and bridge["all_identities_verified"] is True,
        "manifest masked bridge mismatch")
require(bridge["diagonal_saturation_identity"]
        == "ker(H_W)=Delta_Q^-1*ker(H_L) intersect GF(17)[X]^M",
        "manifest diagonal-saturation contract mismatch")
require(manifest["exact_source"]["ordered_exact_supports"]
        == [[int(point) for point in support] for support in layer],
        "manifest full layer mismatch")
require(manifest["exact_source"]["ordered_layer_sha256"] == layer_hash,
        "manifest layer hash mismatch")
require(manifest["coupled_keys"]["key_collision_unions"] == key_records,
        "manifest key collision table mismatch")
require(manifest["coupled_keys"]["collision_table_sha256"] == collision_hash,
        "manifest collision hash mismatch")
require(manifest["noncoalescence"]["five_union_witness"] == witness,
        "manifest five-union witness mismatch")
require(manifest["noncoalescence"]["exact_disjoint_nonempty_union_optimum"] == 5,
        "manifest packing optimum mismatch")
require(manifest["noncoalescence"]["exact_root_transversal_minimum"] == 6,
        "manifest root-transversal minimum mismatch")
require(manifest["noncoalescence"]["minimum_root_transversals"]
        == [list(points) for points in minimum_transversals],
        "manifest minimum root-transversal list mismatch")
require(manifest["noncoalescence"]["no_four_point_root_transversal"] is True,
        "manifest four-point root-transversal scope mismatch")
require(manifest["route_cut"]["payment_status"] == "NONE"
        and manifest["route_cut"]["deployed_terminal"]
        == "UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND",
        "manifest payment/terminal mismatch")

# Deployed arithmetic is exact context only.
require(4 * 62295 == 249180 and 259880 - 249180 == 10700,
        "deployed four-union arithmetic changed")
require(5 * 62295 > 259880, "deployed fifth-union route cut changed")
selected_count = 2^24
deployed_radius = 981129
deployed_sigma = 913681
form_upper = (
    selected_count * deployed_radius
    + binomial(selected_count, 2) * deployed_sigma
)
quartic_field_size = (2^31 - 1)^4
require(form_upper == 128589177894085853184,
        "deployed hyperplane-form count changed")
margin_to_67 = 2^67 - form_upper
require(margin_to_67 == 18984774695590559744,
        "deployed hyperplane margin to 2^67 changed")
require(form_upper < 2^67 < 2^68 < quartic_field_size,
        "deployed target-field hyperplane inequalities failed")
context = manifest["deployed_context"]
require(context["escape_and_collision_form_upper"] == form_upper
        and context["two_to_67"] == 2^67
        and context["two_to_68"] == 2^68
        and context["margin_below_two_to_67"] == margin_to_67
        and context["quartic_field_cardinality"] == quartic_field_size,
        "manifest hyperplane arithmetic mismatch")
require(context["form_upper_below_two_to_67_below_field"] is True,
        "manifest strong hyperplane inequality boolean mismatch")
require(context["hyperplane_dichotomy_is_conditional"] is True
        and context["extra_full_list_supports_may_appear"] is True
        and context["hyperplane_branch_is_row_counterexample_or_payment"] is False,
        "manifest hyperplane scope mismatch")

print("M31_CANONICAL_MASKED_PADE_GLOBAL_ROUTE_CUT_SAGE")
print("padding_bridge=PASS exact_weight5=4 Q_nontrivial=true pair_factors=6")
print("reconstruction=PASS B(LQ)=QB(L) gcd=Q codeword/N transforms=true")
print("right_kernel=PASS widths=1..6 nullities=0,2,4,6,8,10")
print("shared_source=PASS GF17 layer=137 anchors=45 keys=92 core=0")
print("coupled=PASS pair_minors=95220 min_constant_nullity=40")
print("noncoalescence=PASS exact_disjoint_optimum=5 root_transversal_minimum=6")
print("hyperplane=PASS forms=128589177894085853184<2^67<2^68<p^4 conditional=true")
print("scope=DEPLOYED_SYMBOLIC_BRIDGE_PROVED GF17_ROUTE_CUT_TOY "
      "NOT_M31_COUNTEREXAMPLE ledger_movement=0")
print("RESULT=SAGE_REPLAY_PASS")
