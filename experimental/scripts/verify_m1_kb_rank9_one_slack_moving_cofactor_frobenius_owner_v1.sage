#!/usr/bin/env sage
"""Exact toy controls for the one-slack moving-cofactor owner.

This script works over GF(13^2)/GF(13).  It checks, on one explicit
quadratic primitive pencil, the source Frobenius four-anchor determinant
used by the proposed owner.  It also checks the two oriented quotient
interfaces, a projectively-base fixture, and the degree-at-most-one
degeneracy in which every four-anchor minor vanishes identically.

Everything here is an exact toy-scale algebra control.  It is not a
deployed KoalaBear selector, a census, a proof of the symbolic owner, or a
ledger authorization.
"""

import json
from itertools import combinations


SCHEMA = "rs-mca-m1-kb-rank9-one-slack-moving-cofactor-frobenius-owner-v1-sage"
SCALE = "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_CENSUS_PROOF_OR_LEDGER"


def require(condition, message):
    """Fail closed in ordinary and optimized generated-Python modes."""
    if not condition:
        raise RuntimeError(message)


Base = GF(13)
BZ = PolynomialRing(Base, "z")
z = BZ.gen()
modulus = z^2 + 12*z + 2
require(modulus.is_irreducible(), "quadratic modulus became reducible")
Field = GF(13^2, name="zeta", modulus=modulus)
zeta = Field.gen()
require(zeta.multiplicative_order() == Field.order() - 1,
        "declared extension generator is not primitive")

R = PolynomialRing(Field, "X")
X = R.gen()
K = PolynomialRing(Field, "T")
T = K.gen()
p = ZZ(Base.order())


def is_base(value):
    return value^p == value


def projectively_base(values):
    """Whether a nonzero Field-vector is a scalar multiple of a Base-vector."""
    values = tuple(Field(value) for value in values)
    nonzero = tuple(value for value in values if value != 0)
    if not nonzero:
        return False
    pivot = nonzero[0]
    return all(value == 0 or is_base(value/pivot) for value in values)


def four_column_matrix(values):
    """Columns Mg^p, g^p, Mg, g in the note's displayed order."""
    values = tuple(Field(value) for value in values)
    require(len(values) == len(source_points), "source-vector length drift")
    return matrix(Field, len(source_points), 4, lambda row, column: (
        source_points[row]*(values[row]^p),
        values[row]^p,
        source_points[row]*values[row],
        values[row],
    )[column])


def symbolic_anchor_minor(anchor, left_values, right_values):
    """The four-anchor Frobenius determinant for A+T B."""
    require(len(anchor) == 4 and len(set(anchor)) == 4,
            "anchor must contain four distinct source indices")
    rows = []
    for index in anchor:
        h = source_points[index]
        a = Field(left_values[index])
        b = Field(right_values[index])
        g = K(a) + T*K(b)
        gp = K(a^p) + T^p*K(b^p)
        rows.append([K(h)*gp, gp, K(h)*g, g])
    return matrix(K, rows).det()


# Split the nonzero base field into disjoint source and moving supports.  This
# models the full-outside contract: no selected base root is a source anchor,
# and zero is absent from both sets.
source_points = tuple(Field(value) for value in range(1, 7))
moving_points = tuple(Field(value) for value in range(7, 13))
s = ZZ(len(source_points))
e = ZZ(2)
require(s == 6 and len(moving_points) == 6,
        "source/moving support size drift")
require(all(point != 0 and is_base(point) for point in source_points),
        "source support is not nonzero and Base-rational")
require(all(point != 0 and is_base(point) for point in moving_points),
        "moving support is not nonzero and Base-rational")
require(set(source_points).isdisjoint(set(moving_points)),
        "source and moving supports overlap")
require(set(source_points).union(moving_points)
        == {Field(value) for value in Base if value != 0},
        "source/moving split does not partition the nonzero base field")


# -------------------------------------------------------------------------
# Quadratic primitive pencil and its exact split fibers.
# -------------------------------------------------------------------------

Pbar = -(X^2 + zeta*X)
Qbar = R.one()
require(max(Pbar.degree(), Qbar.degree()) == e,
        "quadratic pencil degree drift")
require(gcd(Pbar, Qbar).degree() == 0,
        "quadratic pencil is not primitive")
require(not all(is_base(coefficient) for coefficient in Pbar.list()),
        "quadratic pencil unexpectedly descended to the base field")

Avec = vector(Field, [Pbar(point) for point in source_points])
Bvec = vector(Field, [Qbar(point) for point in source_points])
M = diagonal_matrix(Field, source_points)
MAvec = M*Avec
MBvec = M*Bvec
span_matrix = matrix(Field, len(source_points), 4, lambda row, column: (
    Avec[row], Bvec[row], MAvec[row], MBvec[row]
)[column])
require(span_matrix.rank() == 4,
        "span(A,B,MA,MB) did not have dimension four")

selected_records = []
selected_slopes = []
interface_orientation_checks = 0
for y in moving_points:
    eta = y^2 + zeta*y
    other = -zeta-y
    member = Pbar + eta*Qbar
    expected = -(X-y)*(X-other)
    require(member == expected, "quadratic split identity drift")
    roots = tuple(root for root in Field if member(root) == 0)
    require(set(roots) == {y, other} and len(roots) == 2,
            "selected fiber did not have exactly the declared roots")
    require(is_base(y) and not is_base(other),
            "selected fiber lost its one-base/one-nonbase orientation")
    require(not is_base(eta), "selected slope fell back into the base field")

    source_combination = Avec + eta*Bvec
    support = tuple(index for index, value in enumerate(source_combination)
                    if value != 0)
    require(len(support) == s and len(support) >= s-e,
            "selected full-outside source combination acquired a zero")
    require(tuple(index for index, value in enumerate(source_combination)
                  if value == 0) == (),
            "selected moving root entered the source anchors")

    U_y, rem_y = member.quo_rem(X-y)
    V_z, rem_z = member.quo_rem(X-other)
    require(rem_y == 0 and rem_z == 0,
            "oriented quotient interface division failed")
    require(U_y == -(X-other) and V_z == -(X-y),
            "oriented quotient interface polynomial drift")
    require(U_y != V_z and not is_base(other) and is_base(y),
            "the U_y and V_z interfaces collapsed")
    U_values = vector(Field, [U_y(point) for point in source_points])
    V_values = vector(Field, [V_z(point) for point in source_points])
    require(not projectively_base(U_values),
            "base-root quotient U_y unexpectedly became projectively Base")
    require(projectively_base(V_values),
            "nonbase-root quotient V_z lost its projectively-Base image")
    interface_orientation_checks += 1

    relation_matrix = four_column_matrix(source_combination)
    require(relation_matrix.rank() == 3,
            "selected Frobenius four-column rank was not three")
    relation_kernel = relation_matrix.right_kernel()
    require(relation_kernel.dimension() == 1,
            "selected Frobenius relation was not unique")
    a, b, c, d = relation_kernel.basis()[0]
    relation_det = a*d-b*c
    require(relation_det != 0,
            "selected base/nonbase split acquired a singular relation")

    selected_slopes.append(eta)
    selected_records.append({
        "base_root": int(Base(y)),
        "base_root_count": int(sum(is_base(root) for root in roots)),
        "four_column_rank": int(relation_matrix.rank()),
        "nonbase_root_count": int(sum(not is_base(root) for root in roots)),
        "nonbase_root_trace": int(Base(other + other^p)),
        "outside_base_slope": bool(not is_base(eta)),
        "relation_nonsingular": bool(relation_det != 0),
        "source_support": int(len(support)),
    })

require(len(set(selected_slopes)) == s,
        "selected slopes collided")
require(all(not is_base(eta) for eta in selected_slopes),
        "selected slopes are not all outside the base field")


# The two plane families in the nondegeneracy proof are checked on every
# toy-field parameter, not merely on the six selected slopes.  The
# support floor is likewise the universal source-combination floor used in
# the symbolic argument.
source_supports = {}
U_plane_keys = {}
V_plane_keys = {}
for parameter in Field:
    source_combination = Avec + parameter*Bvec
    conjugate_combination = vector(Field, [
        value^p for value in Avec
    ]) + parameter*vector(Field, [value^p for value in Bvec])
    source_supports[parameter] = source_combination.hamming_weight()
    require(source_supports[parameter] >= s-e,
            "universal source-combination support floor failed")

    U_basis = matrix(Field, [source_combination,
                             M*source_combination]).row_space().basis_matrix()
    V_basis = matrix(Field, [conjugate_combination,
                             M*conjugate_combination]).row_space().basis_matrix()
    require(U_basis.nrows() == 2 and V_basis.nrows() == 2,
            "a U_y or V_z interface failed to have dimension two")
    U_plane_keys[parameter] = tuple(tuple(value for value in row)
                                    for row in U_basis.rows())
    V_plane_keys[parameter] = tuple(tuple(value for value in row)
                                    for row in V_basis.rows())

require(len(set(U_plane_keys.values())) == Field.order(),
        "the U_y interfaces were not pairwise distinct")
require(len(set(V_plane_keys.values())) == Field.order(),
        "the V_z interfaces were not pairwise distinct")


# -------------------------------------------------------------------------
# Universal four-anchor determinant and its exact root containment.
# -------------------------------------------------------------------------

anchors = tuple(combinations(range(s), 4))
require(len(anchors) == binomial(s, 4) == 15,
        "four-anchor inventory size drift")
anchor_minors = tuple(
    symbolic_anchor_minor(anchor, Avec, Bvec) for anchor in anchors
)
require(all(minor.degree() <= 2*p+2 for minor in anchor_minors if minor != 0),
        "four-anchor determinant exceeded degree 2p+2")
require(all(minor(eta) == 0
            for eta in selected_slopes for minor in anchor_minors),
        "a selected slope did not annihilate every four-anchor determinant")

nonzero_anchors = tuple(
    (anchor, minor) for anchor, minor in zip(anchors, anchor_minors)
    if minor != 0
)
require(nonzero_anchors, "all quadratic four-anchor determinants vanished")
first_anchor, first_minor = nonzero_anchors[0]
require(first_anchor == min(anchor for anchor, minor in nonzero_anchors),
        "first nonzero anchor is not lexicographically first")
require(first_minor.degree() <= 2*p+2,
        "first nonzero determinant exceeded the owner degree")
first_minor_roots = tuple(eta for eta in Field if first_minor(eta) == 0)
require(set(selected_slopes).issubset(set(first_minor_roots)),
        "first determinant root set lost a selected slope")
require(len(first_minor_roots) <= first_minor.degree(),
        "first determinant violated its exact field root bound")


# A projectively-Base vector gives zero four-anchor determinants for the
# elementary reason g^p is proportional to g.  The values are deliberately
# nonzero so this is not a support-zero artifact.
projective_base_values = vector(Field, [
    zeta*(point^2 + Field(2)) for point in source_points
])
require(all(value != 0 for value in projective_base_values),
        "projectively-Base fixture acquired a zero coordinate")
require(projectively_base(projective_base_values),
        "projectively-Base fixture classification failed")
require(four_column_matrix(projective_base_values).rank() == 2,
        "projectively-Base fixture four-column rank drift")
require(all(four_column_matrix(projective_base_values)[list(anchor), :].det() == 0
            for anchor in anchors),
        "projectively-Base fixture has a nonzero four-anchor determinant")


# Degree-at-most-one pencils are a necessary fail-closed degeneracy: the
# columns are evaluations of polynomials of degree at most two in the source
# coordinate, so every four-anchor minor is identically zero.
Pdeg1 = -(zeta*X + Field(2))
Qdeg1 = R.one()
Adeg1 = vector(Field, [Pdeg1(point) for point in source_points])
Bdeg1 = vector(Field, [Qdeg1(point) for point in source_points])
degenerate_minors = tuple(
    symbolic_anchor_minor(anchor, Adeg1, Bdeg1) for anchor in anchors
)
degenerate_span = matrix(Field, len(source_points), 4,
                         lambda row, column: (
                             Adeg1[row],
                             Bdeg1[row],
                             source_points[row]*Adeg1[row],
                             source_points[row]*Bdeg1[row],
                         )[column])
require(max(Pdeg1.degree(), Qdeg1.degree()) <= 1,
        "degenerate fixture left degree at most one")
require(degenerate_span.rank() <= 3,
        "degree-at-most-one span unexpectedly had dimension four")
require(all(minor == 0 for minor in degenerate_minors),
        "degree-at-most-one fixture has a nonzero four-anchor minor")


# The determinant roots are enumerated independently of the first eliminant.
# For diagnostic separation, we also count slopes whose unique rank-three
# relation has singular coefficient matrix; the selected split fibers have
# nonsingular relations.
singular_relation_slopes = []
common_determinant_roots = []
for eta in Field:
    values = Avec + eta*Bvec
    columns = four_column_matrix(values)
    if columns.rank() <= 3:
        common_determinant_roots.append(eta)
        kernel = columns.right_kernel()
        if kernel.dimension() != 1:
            singular_relation_slopes.append(eta)
        else:
            a, b, c, d = kernel.basis()[0]
            if a*d-b*c == 0:
                singular_relation_slopes.append(eta)

require(set(selected_slopes).issubset(set(common_determinant_roots)),
        "common determinant-root census lost a selected slope")

# Opposite-ruling lines in the proof have the form
# (r I + q M) E_0, with [r:q] projective.  Since the source coordinates are
# distinct and nonzero, exactly one projective parameter [-a:1] is singular
# for each a in the source.  This is the promised at-most-s count.
projective_parameters = tuple((value, Field.one()) for value in Field) + (
    (Field.one(), Field.zero()),
)
require(len(projective_parameters) == Field.order()+1,
        "projective parameter inventory drift")
singular_opposite_line_parameters = tuple(
    (r, q) for r, q in projective_parameters
    if (r*identity_matrix(Field, s) + q*M).det() == 0
)
require(len(singular_opposite_line_parameters) == s,
        "singular opposite-line parameter count did not equal source size")
require({(-point, Field.one()) for point in source_points}
        == set(singular_opposite_line_parameters),
        "singular opposite-line parameters were not exactly [-a:1]")
require(len(singular_opposite_line_parameters) <= s,
        "singular opposite-line parameter count exceeded the source size")


# Every Boolean is derived from an exact object above.  Flipping each one is
# a fail-closed interface mutation; no Python assert is used anywhere.
interface_claims = {
    "all_anchor_degree_bound": all(
        minor.degree() <= 2*p+2 for minor in anchor_minors if minor != 0
    ),
    "all_selected_fibers_split": all(
        record["base_root_count"] == 1
        and record["nonbase_root_count"] == 1
        for record in selected_records
    ),
    "all_selected_slopes_outside_base": all(
        not is_base(eta) for eta in selected_slopes
    ),
    "anchor_inventory_complete": len(anchors) == binomial(s, 4),
    "base_field_order": p == 13,
    "common_roots_contain_selected": set(selected_slopes).issubset(
        set(common_determinant_roots)
    ),
    "degenerate_all_minors_zero": all(minor == 0 for minor in degenerate_minors),
    "degenerate_degree_at_most_one": max(Pdeg1.degree(), Qdeg1.degree()) <= 1,
    "degenerate_span_at_most_three": degenerate_span.rank() <= 3,
    "extension_degree_two": Field.degree() == 2,
    "extension_larger_than_source": Field.order() > s,
    "first_anchor_lexicographic": first_anchor == min(
        anchor for anchor, minor in nonzero_anchors
    ),
    "first_determinant_exists": first_minor != 0,
    "first_determinant_owner_degree": first_minor.degree() <= 2*p+2,
    "first_roots_contain_selected": set(selected_slopes).issubset(
        set(first_minor_roots)
    ),
    "four_column_selected_rank_three": all(
        record["four_column_rank"] == 3 for record in selected_records
    ),
    "interfaces_distinct": (
        len(set(U_plane_keys.values())) == Field.order()
        and len(set(V_plane_keys.values())) == Field.order()
    ),
    "nonzero_source_points": all(point != 0 for point in source_points),
    "nonzero_source_pairs": all(
        Avec[index] != 0 or Bvec[index] != 0 for index in range(s)
    ),
    "odd_characteristic": p > 2,
    "primitive_pencil": gcd(Pbar, Qbar).degree() == 0,
    "projective_base_fixture": projectively_base(projective_base_values),
    "projective_base_minors_zero": all(
        four_column_matrix(projective_base_values)[list(anchor), :].det() == 0
        for anchor in anchors
    ),
    "quadratic_pencil": max(Pbar.degree(), Qbar.degree()) == 2,
    "relation_determinants_nonsingular": all(
        record["relation_nonsingular"] for record in selected_records
    ),
    "selected_annihilate_all_minors": all(
        minor(eta) == 0
        for eta in selected_slopes for minor in anchor_minors
    ),
    "selected_slopes_distinct": len(set(selected_slopes)) == s,
    "selected_slope_flags": all(
        record["outside_base_slope"] for record in selected_records
    ),
    "selected_source_combinations_full_outside": all(
        record["source_support"] == s for record in selected_records
    ),
    "singular_opposite_line_cap": len(singular_opposite_line_parameters) <= s,
    "source_moving_disjoint": set(source_points).isdisjoint(set(moving_points)),
    "source_moving_partition_nonzero_base": (
        set(source_points).union(moving_points)
        == {Field(value) for value in Base if value != 0}
    ),
    "source_field_base": all(is_base(point) for point in source_points),
    "source_size": s == 6,
    "source_span_dimension_four": span_matrix.rank() == 4,
    "source_support_floor": min(source_supports.values()) >= s-e,
    "toy_only_label": SCALE.endswith("NOT_DEPLOYED_SELECTOR_CENSUS_PROOF_OR_LEDGER"),
    "two_oriented_interfaces": interface_orientation_checks == s,
    "U_y_interfaces_pairwise_distinct": (
        len(set(U_plane_keys.values())) == Field.order()
    ),
    "V_z_interfaces_pairwise_distinct": (
        len(set(V_plane_keys.values())) == Field.order()
    ),
}
require(len(interface_claims) >= 20,
        "interface mutation inventory is too small")
require(all(interface_claims.values()), "Sage interface control failed")


def accepts_interface_claims(candidate):
    return set(candidate) == set(interface_claims) and all(candidate.values())


mutation_results = {}
for name in sorted(interface_claims):
    mutated = dict(interface_claims)
    mutated[name] = False
    mutation_results[name] = not accepts_interface_claims(mutated)
require(all(mutation_results.values()),
        "Sage interface mutation suite failed")


control = {
    "anchor_count": int(len(anchors)),
    "base_field_order": int(Base.order()),
    "common_determinant_root_count": int(len(common_determinant_roots)),
    "degenerate_all_minors_zero": True,
    "degenerate_span_dimension": int(degenerate_span.rank()),
    "extension_field_order": int(Field.order()),
    "first_nonzero_anchor": [int(index) for index in first_anchor],
    "first_nonzero_determinant_degree": int(first_minor.degree()),
    "first_nonzero_determinant_root_count": int(len(first_minor_roots)),
    "mutation_count": int(len(mutation_results)),
    "mutation_rejections": int(sum(mutation_results.values())),
    "moving_points": [int(Base(point)) for point in moving_points],
    "moving_support_size": int(len(moving_points)),
    "projectively_base_fixture_rank": int(
        four_column_matrix(projective_base_values).rank()
    ),
    "scale": SCALE,
    "schema": SCHEMA,
    "selected_fiber_count": int(len(selected_records)),
    "selected_records": selected_records,
    "singular_relation_slope_count": int(len(singular_relation_slopes)),
    "singular_opposite_line_parameter_count": int(
        len(singular_opposite_line_parameters)
    ),
    "source_degree": int(e),
    "source_points": [int(Base(point)) for point in source_points],
    "selected_source_support_minimum": int(min(
        record["source_support"] for record in selected_records
    )),
    "source_support_minimum_all_parameters": int(min(source_supports.values())),
    "source_size": int(s),
    "span_A_B_MA_MB_dimension": int(span_matrix.rank()),
    "toy_only": True,
}

print("MOVING_COFACTOR_FROBENIUS_OWNER_CONTROL=" + json.dumps(
    control, sort_keys=True, separators=(",", ":")
))
print("MOVING_COFACTOR_FROBENIUS_OWNER_MUTATIONS=" + json.dumps(
    mutation_results, sort_keys=True, separators=(",", ":")
))
print("SCALE=" + SCALE)
