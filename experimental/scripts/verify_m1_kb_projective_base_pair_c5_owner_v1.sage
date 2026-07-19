"""Exact C5 guardrail for a projectively base-defined received pair.

The toy starts with a sparse rank-two received pair for the repetition
Reed--Solomon code over GF(5).  Every direction in P^1(GF(5)) has a
two-coordinate support-wise noncontained witness.  A GL_2(GF(5^6)) change of
source coordinates moves those six directions to a nonstandard projective
GF(5)-subline, all of whose points lie in the finite slope chart.  Five of the
six displayed slopes are genuinely degree six.

Nevertheless, the transformed received pair is globally GL_2-equivalent to
the original base pair, and its syndrome plane is defined over GF(5).  Thus
raw extension-valued slopes on a nonstandard subline do not imply full
projective syndrome field; this exact configuration belongs to canonical C5.
"""

p = 5
B = GF(p)
F.<z> = GF(p^6)
theta = z

assert theta.minimal_polynomial().degree() == 6
assert theta^p != theta

# Repetition RS parameters.  The union of the two source supports has size
# j=3, so this is one fixed sparse/SP3 source at agreement A=2.
n = 5
k = 1
A_agreement = 2
j = n - A_agreement

assert (n, k, A_agreement, j) == (5, 1, 2, 3)

# Rows are the two received coordinates at the five evaluation points.  Two
# coordinates are zero; the three nonzero rows are chosen so that the six
# differences among {(0,0),(0,1),(1,0),(2,2)} determine all six directions
# of P^1(GF(5)).
base_rows = [
    (0, 0),
    (0, 0),
    (0, 1),
    (1, 0),
    (2, 2),
]
R_base = matrix(F, [[F(a), F(b)] for a, b in base_rows])
zero_row = vector(F, [0, 0])

assert sum(row != zero_row for row in R_base.rows()) == j

# H is a parity-check matrix for the [5,1,5] repetition RS code.  Its kernel
# is the space of constant evaluation vectors.
H = matrix(
    F,
    n - k,
    n,
    lambda i, ell: 1 if ell == i else (-1 if ell == n - 1 else 0),
)
assert H.rank() == n - k
assert H * vector(F, [1] * n) == 0

Y_base = H * R_base
assert Y_base.rank() == 2

# Let M send the standard projective base line to a nonstandard subline.  Its
# pole is nonbase, so no point of P^1(B) maps to projective infinity.  Set the
# received-pair change of basis to A=M^{-1}; then witness directions transform
# by M and R_ext*M=R_base.
M = matrix(F, [[1, theta], [0, 1]])
A_change = M.inverse()
R_ext = R_base * A_change

assert R_ext * M == R_base
assert sum(row != zero_row for row in R_ext.rows()) == j


def is_base_element(value):
    return value^p == value


def projectively_base(matrix_2_by_2):
    entries = matrix_2_by_2.list()
    pivot = next((value for value in entries if value != 0), None)
    if pivot is None:
        return False
    return all(is_base_element(value / pivot) for value in entries)


assert not projectively_base(M)

# The syndrome plane is unchanged as an F-subspace by the invertible column
# operation.  Its canonical RREF is Frobenius fixed, so its intrinsic minimal
# projective field is B (rank two rules out the zero-syndrome edge case).
Y_ext = H * R_ext
assert Y_ext.rank() == 2
assert Y_ext.column_space() == Y_base.column_space()

syndrome_plane_rref = Y_ext.transpose().echelon_form()
assert all(is_base_element(value) for value in syndrome_plane_rref.list())

# Standard projective directions [1:x], x in B, followed by infinity [0:1].
base_directions = [vector(F, [1, F(x)]) for x in B]
base_directions.append(vector(F, [0, 1]))
assert len(base_directions) == p + 1

finite_slopes = []
witness_pairs = []

for base_direction in base_directions:
    moved_direction = M * base_direction

    # The chosen subline misses projective infinity, hence all p+1 directions
    # occur in the source finite-slope chart [1:gamma].
    assert moved_direction[0] != 0
    gamma = moved_direction[1] / moved_direction[0]
    finite_slopes.append(gamma)

    # R_ext*(M*d)=R_base*d.  After finite-chart normalization this changes by
    # only a nonzero scalar, so equality collisions are preserved.
    normalized_values = list(R_ext * vector(F, [1, gamma]))
    witness = None
    for right in range(n):
        for left in range(right):
            if (
                normalized_values[left] == normalized_values[right]
                and R_ext[left] != R_ext[right]
            ):
                witness = (left, right)
                break
        if witness is not None:
            break

    # Equal combined values give a repetition-code explanation on this
    # two-point support.  Distinct received rows mean that the two individual
    # source coordinates are not both repetition-code explainable there.
    assert witness is not None
    assert len(set(witness)) == A_agreement
    witness_pairs.append(witness)

assert len(finite_slopes) == p + 1
assert len(set(finite_slopes)) == p + 1
assert len(witness_pairs) == p + 1

base_slope_count = sum(is_base_element(gamma) for gamma in finite_slopes)
extension_slope_count = (p + 1) - base_slope_count
slope_degrees = sorted(
    gamma.minimal_polynomial().degree() for gamma in finite_slopes
)

assert base_slope_count == 1
assert extension_slope_count == p
assert slope_degrees == [1] + [6] * p

# Scope guard: degree gcd(P,Q)=k-2 does not itself force base descent.
# Here G has the maximal degree k-2 but its root is nonbase and off-domain.
B2 = GF(11)
F2.<xi> = GF(11^2)
S.<T> = PolynomialRing(F2)
D2 = [F2(i) for i in range(1, 10)]
n2 = len(D2)
k2 = 3
agreement2 = 4
j2 = n2 - agreement2
Sigma2 = set(D2[:3])

G2 = T - xi
P2 = G2*T
Q2 = -G2
assert G2.degree() == k2 - 2
assert all(G2(x) != 0 for x in D2)
assert any(not (coefficient^11 == coefficient) for coefficient in G2.list())

# A base-defined parity check for RS(D2,k2).
V2 = matrix(F2, k2, n2, lambda i, ell: D2[ell]^i)
H2 = V2.right_kernel().basis_matrix()
assert H2.nrows() == n2-k2
assert H2.rank() == n2-k2
assert H2*V2.transpose() == 0
assert all(value^11 == value for value in H2.list())

R_nonsplit = matrix(
    F2,
    n2,
    2,
    lambda row, col: (
        [P2(D2[row]), Q2(D2[row])][col]
        if D2[row] in Sigma2
        else F2.zero()
    ),
)
Y_nonsplit = H2*R_nonsplit
assert Y_nonsplit.rank() == 2
nonsplit_rref = Y_nonsplit.transpose().echelon_form()
assert any(value^11 != value for value in nonsplit_rref.list())

nonsplit_witnesses = 0
for rho in D2[3:]:
    h = P2 + rho*Q2
    assert h.degree() < k2
    combined = R_nonsplit*vector(F2, [1, rho])
    agreement_indices = [
        index
        for index, x in enumerate(D2)
        if combined[index] == h(x)
    ]
    expected_indices = [0, 1, 2, D2.index(rho)]
    assert agreement_indices == expected_indices
    assert len(agreement_indices) == agreement2

    # The three source points force the individual interpolants P2 and Q2;
    # neither matches the zero source value at rho.
    assert P2(rho) != 0
    assert Q2(rho) != 0
    nonsplit_witnesses += 1

assert nonsplit_witnesses == len(D2)-len(Sigma2) == 6
assert j2 == 5

print("M1 projective-base-pair C5 owner Sage control: PASS")
print("  field=GF(5^6); code=[5,1,5]; agreement=2; sparse_source_union=3")
print("  source_syndrome_rank=2; intrinsic_F_proj=GF(5)")
print("  nonstandard_subline_finite_slopes=6; base=1; degree6=5")
print("  exact_two_point_noncontained_witnesses=6/6")
print("  GL2_normalization_to_base_pair=PASS; canonical_C5_route=PASS")
print("  nonsplit guard=GF(11^2), RS[9,3,7], deg(gcd)=k-2 but c_L=0")
print("  nonsplit source_syndrome_rank=2; intrinsic_F_proj=GF(11^2)")
print("  nonsplit exact witnesses=6/6; general maximal-gcd C5 route=OPEN")
