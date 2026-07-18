p = 5
B = GF(p)
F.<z> = GF(p^6)
assert z^p != z

base_values = [F(i) for i in B]
base_points = [(x, F.one()) for x in base_values] + [(F.one(), F.zero())]


def normalize(point):
    u, v = point
    if u == 0 and v == 0:
        return None
    if v != 0:
        return (u / v, F.one())
    return (F.one(), F.zero())


def action(M, point):
    a, b, c, d = M
    x, y = point
    return normalize((a*x + b*y, c*x + d*y))


def det(M):
    a, b, c, d = M
    return a*d - b*c


def is_base_element(x):
    return x^p == x


def is_base_point(point):
    if point is None:
        return False
    u, v = point
    return v == 0 or is_base_element(u/v)


def projectively_base(M):
    pivot = next((x for x in M if x != 0), None)
    if pivot is None:
        return False
    return all(is_base_element(x/pivot) for x in M)


def projective_key(M):
    pivot = next(x for x in M if x != 0)
    return tuple(x/pivot for x in M)


def image_record(M):
    images = [action(M, point) for point in base_points]
    defined = [point for point in images if point is not None]
    distinct = set(defined)
    base_image = {point for point in distinct if is_base_point(point)}
    return {
        "images": images,
        "defined_count": len(defined),
        "distinct_count": len(distinct),
        "base_intersection_count": len(base_image),
        "base_intersection": base_image,
        "undefined_inputs": [
            base_points[i] for i, point in enumerate(images) if point is None
        ],
    }


R.<X,Y> = PolynomialRing(F, 2)


def frobenius_quadratic(M):
    a, b, c, d = M
    u = a*X+b*Y
    v = c*X+d*Y
    us = a^p*X+b^p*Y
    vs = c^p*X+d^p*Y
    return u*vs-v*us


# Exhaust every PGL_2(F_5) class.
base_classes = {}
for a, b, c, d in cartesian_product([B]*4):
    M = tuple(F(x) for x in (a, b, c, d))
    if det(M) == 0:
        continue
    base_classes[projective_key(M)] = M
assert len(base_classes) == p*(p^2-1) == 120
for M in base_classes.values():
    rec = image_record(M)
    assert projectively_base(M)
    assert rec["distinct_count"] == p+1
    assert rec["base_intersection_count"] == p+1
    assert frobenius_quadratic(M) == 0


# A transparent exact-two example and a 625-matrix coefficient slice.
M_two = (z, F.one(), F.zero(), F.one())
rec_two = image_record(M_two)
Q_two = frobenius_quadratic(M_two)
assert det(M_two) != 0 and not projectively_base(M_two)
assert rec_two["base_intersection_count"] == 2
assert rec_two["base_intersection"] == {
    (F.one(), F.one()), (F.one(), F.zero())
}
assert Q_two == (z-z^p)*X*Y

hist = {0: 0, 1: 0, 2: 0}
invertible_slice = 0
singular_slice = 0
for aa, bb, cc, dd in cartesian_product([B]*4):
    M = (z+F(aa), F(bb), F(cc), F(dd))
    if det(M) == 0:
        singular_slice += 1
        continue
    invertible_slice += 1
    assert not projectively_base(M)
    rec = image_record(M)
    q = frobenius_quadratic(M)
    assert q != 0
    roots = sum(q(F(x), F.one()) == 0 for x in B)
    roots += q(F.one(), F.zero()) == 0
    assert roots == rec["base_intersection_count"]
    assert roots <= 2
    hist[ZZ(roots)] += 1
assert invertible_slice == 580
assert singular_slice == 45
assert hist == {0: 0, 1: 80, 2: 500}

# A zero-hit nonstandard subline exists outside that slice.
M_zero_hit = (F.one(), z, z, z^2+1)
assert det(M_zero_hit) != 0
assert not projectively_base(M_zero_hit)
assert image_record(M_zero_hit)["base_intersection_count"] == 0


# A base pole maps to projective infinity, but finite-only slopes omit it.
M_pole = (z, F.one(), F.one(), F.one())
rec_pole = image_record(M_pole)
pole_input = (F(-1), F.one())
assert det(M_pole) != 0
assert action(M_pole, pole_input) == (F.one(), F.zero())
projective_hits_pole = rec_pole["base_intersection_count"]
finite_hits_pole = sum(
    action(M_pole, point) is not None
    and action(M_pole, point)[1] != 0
    and is_base_point(action(M_pole, point))
    for point in base_points if point != pole_input
)
assert projective_hits_pole == 2
assert finite_hits_pole == 1


# Common factors are cancelled only after their roots leave the domain.
r = F(2)
S.<T> = PolynomialRing(F)
N = (T-r)*(z*T+1)
D = (T-r)*(T+1)
assert N.gcd(D) == T-r
assert N(r) == D(r) == 0
assert N // (T-r) == z*T+1
assert D // (T-r) == T+1
assert action(M_pole, (r, F.one())) is not None

r_pole = F(-1)
N_pole_common = (T-r_pole)*(z*T+1)
D_pole_common = (T-r_pole)*(T+1)
assert N_pole_common(r_pole) == D_pole_common(r_pole) == 0
assert N_pole_common.gcd(D_pole_common) == T-r_pole
assert action(M_pole, (r_pole, F.one())) == (F.one(), F.zero())

# Nonbase coefficients before gcd cancellation do not imply a nonbase map.
N_nonbase_gcd = (T-z)*T
D_nonbase_gcd = T-z
assert N_nonbase_gcd.gcd(D_nonbase_gcd) == T-z
assert N_nonbase_gcd // (T-z) == T
assert D_nonbase_gcd // (T-z) == 1
M_reduced_identity = (F.one(), F.zero(), F.zero(), F.one())
assert projectively_base(M_reduced_identity)
assert image_record(M_reduced_identity)["base_intersection_count"] == p+1


# Nonzero determinant-zero matrices have rank one; the zero matrix has rank
# zero. Neither is in PGL_2, and both need separate handling.
M_rank1_base = (F.one(), F.zero(), F(2), F.zero())
rec_rank1_base = image_record(M_rank1_base)
assert det(M_rank1_base) == 0
assert rec_rank1_base["defined_count"] == p
assert rec_rank1_base["distinct_count"] == 1
assert rec_rank1_base["base_intersection_count"] == 1
assert rec_rank1_base["undefined_inputs"] == [(F.zero(), F.one())]

M_rank1_nonbase = (z, F.zero(), F.one(), F.zero())
rec_rank1_nonbase = image_record(M_rank1_nonbase)
assert det(M_rank1_nonbase) == 0
assert rec_rank1_nonbase["defined_count"] == p
assert rec_rank1_nonbase["distinct_count"] == 1
assert rec_rank1_nonbase["base_intersection_count"] == 0
assert rec_rank1_nonbase["undefined_inputs"] == [(F.zero(), F.one())]

M_zero = (F.zero(),)*4
rec_zero = image_record(M_zero)
assert rec_zero["defined_count"] == 0
assert len(rec_zero["undefined_inputs"]) == p+1

print("M1 outside-rank-two base-slope absorption Sage control: PASS")
print("  field: GF(5^6); base P1 size: 6; base PGL2 classes: 120")
print("  slice: 580 genuinely nonbase invertible, 45 singular, histogram %s" % hist)
print("  exact intersection examples: 0 and 2; pole/common-root guards: PASS")
