#!/usr/bin/env python3
"""Exact F_97 / mu_16 preflight for general first-interior BC lines.

This is an EXPERIMENT, not a theorem or a certificate for the deployed row.
It extends the two small fixtures from
``verify_bc_l4_interior_chart_to_q.py`` from one planted word to affine lines
of received words.  All arithmetic and enumeration are exact over F_97.

For every m-subset T, restriction to T is interpolated once.  The two excess
conditions (m-K=2 in both fixtures) are affine equations in the line slope z,
so T contributes either no slope, one slope, or every slope (a common
support).  The output then:

* classifies the exact shifted weak-Popov d1 at every finite slope;
* verifies the saturation identity after deduplication to (slope, codeword)
  LineRay pairs;
* recovers degree-omega split locators as A W1 + B W2;
* removes common-support and cyclic-periodic support representatives;
* measures ranks of canonical minimal denominators and deterministic
  locator representatives of the retained LineRay pairs; and
* enumerates every one-locator-per-selected-slope transversal and reports its
  fixed-domain-root GCD, separately from gcd(B,W1).

The fixture-first construction at (K,m)=(5,7) solves exact linear constraints
for three prescribed slopes with three degree-four rational presentations.
The program accepts a candidate only after recomputing weak Popov, checking
that the minimal kernel is one-dimensional, checking pairwise denominator
gcd 1, enumerating every support, and finding no common support.  Since the
toy has q=p, it cannot test the extension/subfield first-match cell.  Thus a
rank >= 2 row is evidence that higher-dimensional minimal-denominator geometry
can occur before first match.  The pinned fixture is then routed through
fixed-root common-GCD cells; it is not an unpaid deployed residual witness.

Stdlib only.  Typical runtime is a few seconds.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import random
from collections import Counter
from dataclasses import dataclass


STATUS = "EXPERIMENTAL / FIXTURE-FIRST PREFLIGHT"
PROBLEM_ID = "balanced-core residual ray compiler; general-line d1=w+2"
P = 97
N = 16
D1_TARGET = 4
W_DEPTH = 2
SEED = 20260715
SELECTED_SLOPES = (0, 1, 2)


# ------------------------------------------------------------------ F_p/poly
def inv(a: int) -> int:
    assert a % P
    return pow(a % P, P - 2, P)


def pnorm(f):
    f = [x % P for x in f]
    while f and f[-1] == 0:
        f.pop()
    return f


def pdeg(f):
    return len(pnorm(f)) - 1


def padd(f, g):
    out = [0] * max(len(f), len(g))
    for i in range(len(out)):
        out[i] = ((f[i] if i < len(f) else 0)
                  + (g[i] if i < len(g) else 0)) % P
    return pnorm(out)


def psub(f, g):
    out = [0] * max(len(f), len(g))
    for i in range(len(out)):
        out[i] = ((f[i] if i < len(f) else 0)
                  - (g[i] if i < len(g) else 0)) % P
    return pnorm(out)


def pscale(f, c):
    return pnorm([(c % P) * x % P for x in f])


def pshift(f, k):
    return ([0] * k + list(f)) if f else []


def pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return pnorm(out)


def pdivmod(f, g):
    f, g = pnorm(f), pnorm(g)
    assert g
    q = [0] * max(0, len(f) - len(g) + 1)
    gi = inv(g[-1])
    while f and len(f) >= len(g):
        c = f[-1] * gi % P
        d = len(f) - len(g)
        q[d] = c
        for j, b in enumerate(g):
            f[d + j] = (f[d + j] - c * b) % P
        f = pnorm(f)
    return pnorm(q), f


def pgcd(f, g):
    f, g = pnorm(f), pnorm(g)
    while g:
        f, g = g, pdivmod(f, g)[1]
    return pscale(f, inv(f[-1])) if f else []


def pgcd_many(polys):
    polys = [list(f) for f in polys]
    assert polys
    out = polys[0]
    for f in polys[1:]:
        out = pgcd(out, f)
    return out


def domain_root_indices(f):
    return tuple(i for i, x in enumerate(D) if peval(f, x) == 0)


def peval(f, x):
    out = 0
    for a in reversed(f):
        out = (out * x + a) % P
    return out


def pfrom_roots(roots):
    out = [1]
    for x in roots:
        out = pmul(out, [(-x) % P, 1])
    return out


def pad(f, length):
    return tuple((f[i] if i < len(f) else 0) for i in range(length))


# -------------------------------------------------------------- domain mu_16
def primitive_root():
    for g in range(2, P):
        if pow(g, 48, P) != 1 and pow(g, 32, P) != 1:
            return g
    raise AssertionError("no primitive root")


GEN = primitive_root()
H = pow(GEN, (P - 1) // N, P)
# Exponent order is intentional: cyclic-periodicity is then an index rotation.
D = tuple(pow(H, j, P) for j in range(N))
assert len(set(D)) == N and all(pow(x, N, P) == 1 for x in D)
LAMBDA = pfrom_roots(D)
assert LAMBDA == [P - 1] + [0] * (N - 1) + [1]


# ----------------------------------------------------------- linear algebra
def rref(mat, ncols=None):
    if ncols is None:
        ncols = len(mat[0]) if mat else 0
    a = [[x % P for x in row] for row in mat]
    pivots = []
    rr = 0
    for col in range(ncols):
        pivot = next((i for i in range(rr, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        scale = inv(a[rr][col])
        a[rr] = [x * scale % P for x in a[rr]]
        for i in range(len(a)):
            if i != rr and a[i][col]:
                c = a[i][col]
                a[i] = [(x - c * y) % P for x, y in zip(a[i], a[rr])]
        pivots.append(col)
        rr += 1
        if rr == len(a):
            break
    return a, pivots


def matrix_rank(mat):
    if not mat:
        return 0
    return len(rref(mat, len(mat[0]))[1])


def nullspace(mat, ncols):
    reduced, pivots = rref(mat, ncols)
    free = [j for j in range(ncols) if j not in pivots]
    out = []
    for fc in free:
        v = [0] * ncols
        v[fc] = 1
        for i, pc in enumerate(pivots):
            v[pc] = (-reduced[i][fc]) % P
        out.append(v)
    return out


def invert_square(mat):
    n = len(mat)
    aug = [list(row) + [1 if i == j else 0 for j in range(n)]
           for i, row in enumerate(mat)]
    red, pivots = rref(aug, n)
    assert pivots == list(range(n))
    return [row[n:] for row in red]


def matvec(mat, vec):
    return [sum(a * b for a, b in zip(row, vec)) % P for row in mat]


def affine_rank(points):
    if len(points) <= 1:
        return 0
    base = points[0]
    return matrix_rank([[(x - y) % P for x, y in zip(pt, base)]
                        for pt in points[1:]])


def projective_dimension(vectors):
    nonzero = [list(v) for v in vectors if any(v)]
    return matrix_rank(nonzero) - 1 if nonzero else -1


# ------------------------------------------------------- interpolation/popov
def interpolate_full(vals):
    out = []
    for i, xi in enumerate(D):
        num, den = [1], 1
        for j, xj in enumerate(D):
            if i == j:
                continue
            num = pmul(num, [(-xj) % P, 1])
            den = den * (xi - xj) % P
        out = padd(out, pscale(num, vals[i] * inv(den)))
    assert [peval(out, x) for x in D] == list(vals)
    return out


def wdeg_pivot(row, K):
    Wp, Np = row
    e1 = pdeg(Wp) if Wp else -10**9
    e2 = pdeg(Np) - (K - 1) if Np else -10**9
    return max(e1, e2), (1 if e2 >= e1 else 0)


def popov_reduce(vals, K):
    Uhat = interpolate_full(vals)
    rows = [([1], Uhat), ([], list(LAMBDA))]
    for _ in range(10000):
        wp0, wp1 = wdeg_pivot(rows[0], K), wdeg_pivot(rows[1], K)
        if wp0[1] != wp1[1]:
            break
        i, j = (0, 1) if wp0[0] <= wp1[0] else (1, 0)
        wi = wdeg_pivot(rows[i], K)[0]
        wj = wdeg_pivot(rows[j], K)[0]
        pivot = wdeg_pivot(rows[i], K)[1]
        c = rows[j][pivot][-1] * inv(rows[i][pivot][-1]) % P
        delta = wj - wi
        rows[j] = (
            psub(rows[j][0], pshift(pscale(rows[i][0], c), delta)),
            psub(rows[j][1], pshift(pscale(rows[i][1], c), delta)),
        )
    else:
        raise AssertionError("weak-Popov reduction did not terminate")
    rows.sort(key=lambda row: wdeg_pivot(row, K)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot(g1, K)[0], wdeg_pivot(g2, K)[0]
    assert wdeg_pivot(g1, K)[1] != wdeg_pivot(g2, K)[1]
    assert d1 + d2 == N - K + 1
    for Wp, Np in rows:
        assert all(peval(Wp, x) * vals[j] % P == peval(Np, x)
                   for j, x in enumerate(D))
    det = psub(pmul(g1[0], g2[1]), pmul(g1[1], g2[0]))
    q, rem = pdivmod(det, LAMBDA)
    assert not rem and pdeg(q) == 0
    assert pdeg(pgcd(g1[0], g2[0])) == 0
    return g1, g2, d1, d2, Uhat


def profile_kernel(vals, K, d):
    """Kernel for deg W<=d, deg N<=d+K-1, evaluated on D."""
    ncols = (d + 1) + (d + K)
    rows = []
    for x, y in zip(D, vals):
        rows.append([(y * pow(x, j, P)) % P for j in range(d + 1)]
                    + [(-pow(x, j, P)) % P for j in range(d + K)])
    return nullspace(rows, ncols)


def canonical_minimal_pair(g1, d1, K):
    Wp, Np = g1
    assert Wp
    # The constructed fixture requires deg W=d1.  Monic W gives a global
    # affine chart in which denominator ranks are meaningful across slopes.
    scale = inv(Wp[-1])
    Wm, Nm = pscale(Wp, scale), pscale(Np, scale)
    return pad(Wm, d1 + 1), pad(Nm, d1 + K)


# ----------------------------------------------------------- support models
@dataclass(frozen=True)
class Row:
    label: str
    K: int
    m: int

    @property
    def omega(self):
        return N - self.m

    @property
    def mprime(self):
        return self.K - 1 + D1_TARGET


@dataclass(frozen=True)
class SupportModel:
    indices: tuple[int, ...]
    head: tuple[int, ...]
    inverse_vandermonde: tuple[tuple[int, ...], ...]
    parity_rows: tuple[tuple[int, ...], ...]
    locator: tuple[int, ...]
    aperiodic: bool


ROWS = (Row("A", 4, 6), Row("B", 5, 7))


def cyclic_aperiodic(indices):
    s = set(indices)
    return all({(i + shift) % N for i in s} != s for shift in range(1, N))


def support_models(row):
    out = []
    for inds in itertools.combinations(range(N), row.m):
        head = inds[:row.K]
        vand = [[pow(D[i], j, P) for j in range(row.K)] for i in head]
        vinv = invert_square(vand)
        parity = []
        for idx in inds[row.K:]:
            # predicted value at idx is weights dot values_on_head
            powers = [pow(D[idx], j, P) for j in range(row.K)]
            weights = [sum(powers[a] * vinv[a][b]
                           for a in range(row.K)) % P
                       for b in range(row.K)]
            h = [0] * N
            h[idx] = 1
            for b, hi in enumerate(head):
                h[hi] = (h[hi] - weights[b]) % P
            parity.append(tuple(h))
        locator = pfrom_roots(D[i] for i in range(N) if i not in set(inds))
        assert pdeg(locator) == row.omega and locator[-1] == 1
        out.append(SupportModel(tuple(inds), tuple(head),
                                tuple(tuple(x) for x in vinv),
                                tuple(parity), pad(locator, row.omega + 1),
                                cyclic_aperiodic(inds)))
    assert len(out) == math.comb(N, row.m)
    return out


def interpolate_head(model, vals, K):
    rhs = [vals[i] for i in model.head]
    return tuple(matvec(model.inverse_vandermonde, rhs))


def dot(row, vals):
    return sum(a * b for a, b in zip(row, vals)) % P


def support_slope(model, u, v):
    equations = [(dot(h, u), dot(h, v)) for h in model.parity_rows]
    if all(a == 0 and b == 0 for a, b in equations):
        return "all", None
    candidates = [(-a * inv(b)) % P for a, b in equations if b]
    if not candidates:
        return "none", None
    z = candidates[0]
    if all((a + z * b) % P == 0 for a, b in equations):
        return "one", z
    return "none", None


def eval_poly(coeffs):
    return tuple(peval(coeffs, x) for x in D)


def add_words(u, v, z):
    return tuple((a + z * b) % P for a, b in zip(u, v))


def line_census(row, models, u, v):
    """Enumerate supports exactly and deduplicate to (z, codeword)."""
    pairs = {}
    common_supports = 0
    for model in models:
        kind, z0 = support_slope(model, u, v)
        if kind == "none":
            continue
        slopes = range(P) if kind == "all" else (z0,)
        if kind == "all":
            common_supports += 1
        cu = interpolate_head(model, u, row.K)
        cv = interpolate_head(model, v, row.K)
        for z in slopes:
            c = tuple((a + z * b) % P for a, b in zip(cu, cv))
            key = (z, c)
            st = pairs.setdefault(key, {"supports": [], "clean": []})
            st["supports"].append(model)
            if kind != "all" and model.aperiodic:
                st["clean"].append(model)

    # Exact LineRay and saturation audit.
    raw_supports = sum(len(st["supports"]) for st in pairs.values())
    saturation = 0
    for (z, c), st in pairs.items():
        word = add_words(u, v, z)
        agree = tuple(i for i, x in enumerate(D)
                      if peval(c, x) == word[i])
        assert all(set(model.indices).issubset(agree) for model in st["supports"])
        want = math.comb(len(agree), row.m)
        assert len(st["supports"]) == want
        saturation += want
        st["agreement"] = agree
    assert saturation == raw_supports
    return {
        "pairs": pairs,
        "raw_supports": raw_supports,
        "common_supports": common_supports,
        "lineray": len(pairs),
        "slopes": len({z for z, _ in pairs}),
    }


def word_lineray_count(row, models, word):
    """Exact ray count for one received word (no artificial slope axis)."""
    rays = {}
    for model in models:
        if any(dot(h, word) for h in model.parity_rows):
            continue
        c = interpolate_head(model, word, row.K)
        rays.setdefault(c, []).append(model)
    for c, representatives in rays.items():
        agreement = tuple(i for i, x in enumerate(D)
                          if peval(c, x) == word[i])
        assert len(representatives) == math.comb(len(agreement), row.m)
    return len(rays)


# ------------------------------------------------------- split-locator chart
def split_solver(g1, g2, d1, d2, omega):
    cap1, cap2 = omega - d1, omega - d2
    assert cap1 >= 0 and cap2 >= 0
    columns = []
    for j in range(cap1 + 1):
        columns.append(list(pad(pshift(g1[0], j), omega + 1)))
    nA = len(columns)
    for j in range(cap2 + 1):
        columns.append(list(pad(pshift(g2[0], j), omega + 1)))
    ncols = len(columns)
    matrix = [[columns[j][i] for j in range(ncols)]
              for i in range(omega + 1)]
    assert matrix_rank(matrix) == ncols
    chosen, chosen_idx = [], []
    for i, row in enumerate(matrix):
        if matrix_rank(chosen + [row]) > len(chosen):
            chosen.append(row)
            chosen_idx.append(i)
        if len(chosen) == ncols:
            break
    inverse = invert_square(chosen)

    def solve(locator):
        rhs = [locator[i] for i in chosen_idx]
        x = matvec(inverse, rhs)
        assert all(sum(matrix[i][j] * x[j] for j in range(ncols)) % P
                   == locator[i] for i in range(omega + 1))
        return tuple(x[:nA]), tuple(x[nA:])

    return solve


def quotient_rank_mod_W1(row, W1, B, gamma, max_v_degree):
    """Rank of V |-> gamma*B*V modulo W1*P_{<K}.

    All polynomials fit in P_{<=m+1}.  Rank in the quotient is computed as
    rank(S + image) - rank(S), where S=W1*P_{<K}; no quotient basis choices
    enter the result.
    """
    ambient = row.m + 2
    subspace = [list(pad(pshift(W1, j), ambient))
                for j in range(row.K)]
    image = [list(pad(pshift(pscale(B, gamma), j), ambient))
             for j in range(max_v_degree + 1)]
    rank_subspace = matrix_rank(subspace)
    assert rank_subspace == row.K
    return matrix_rank(subspace + image) - rank_subspace


def determinant_quotient_diagnostic(row, prof, hit):
    """Replay the fixed-B map attached to one recovered split locator."""
    W1, N1 = prof["g1"]
    W2, N2 = prof["g2"]
    det = psub(pmul(W1, N2), pmul(W2, N1))
    gamma_poly, det_rem = pdivmod(det, LAMBDA)
    assert not det_rem and pdeg(gamma_poly) == 0
    gamma = gamma_poly[0]
    G = list(hit["model"].locator)
    V, rem = pdivmod(LAMBDA, G)
    assert not rem and pdeg(V) == row.m
    B = pnorm(hit["B"])
    # Record the invariant degree alternative, not an implementation-specific
    # weak-Popov tie-break: deg(W1)=d1 may still be a shifted N-column tie.
    pivot = ("denominator-full" if pdeg(W1) == prof["d1"]
             else "numerator-strict")

    if B:
        full_rank = quotient_rank_mod_W1(row, W1, B, gamma, row.m)
        direction_rank = quotient_rank_mod_W1(
            row, W1, B, gamma, row.m - 1)
        gcd_degree = pdeg(pgcd(B, W1))
    else:
        full_rank = direction_rank = 0
        gcd_degree = -1

    lhs = padd(N1, pscale(pmul(B, V), gamma))
    rhs = pmul(W1, hit["c"])
    identity_ok = lhs == rhs
    gluing_lhs = psub(N2, pmul(W2, hit["c"]))
    gluing_rhs = pscale(pmul(hit["A"], V), gamma)
    gluing_identity_ok = gluing_lhs == gluing_rhs
    quotient, membership_rem = pdivmod(lhs, W1)
    membership_ok = (not membership_rem and pdeg(quotient) < row.K
                     and pad(quotient, row.K) == hit["c"])

    expected_direction = (D1_TARGET if pivot == "denominator-full"
                          else W_DEPTH + 1)
    generic_rank_ok = (B and full_rank == D1_TARGET
                       and direction_rank == expected_direction)
    structural_shape_ok = (
        (pivot == "denominator-full" and pdeg(W1) == D1_TARGET)
        or (pivot == "numerator-strict" and pdeg(W1) <= W_DEPTH + 1
            and pdeg(B) == 1)
    )
    return {
        "pivot": pivot,
        "deg_W1": pdeg(W1),
        "deg_B": pdeg(B),
        "gcd_B_W1_degree": gcd_degree,
        "full_rank": full_rank,
        "monic_direction_rank": direction_rank,
        "expected_generic_direction_rank": expected_direction,
        "generic_rank_ok": generic_rank_ok,
        "structural_shape_ok": structural_shape_ok,
        "determinant_gamma": gamma,
        "identity_ok": identity_ok,
        "gluing_identity_ok": gluing_identity_ok,
        "membership_in_W1_PltK": membership_ok,
    }


def analyze_line(row, models, label, u, v, construction=None):
    assert len(u) == len(v) == N and any(v)
    census = line_census(row, models, u, v)

    profiles = {}
    d1_hist = Counter()
    for z in range(P):
        word = add_words(u, v, z)
        g1, g2, d1, d2, uhat = popov_reduce(word, row.K)
        ker = profile_kernel(word, row.K, d1)
        profiles[z] = {"g1": g1, "g2": g2, "d1": d1, "d2": d2,
                       "uhat": uhat, "nullity": len(ker)}
        d1_hist[d1] += 1

    pair_d1_hist = Counter(profiles[z]["d1"] for z, _ in census["pairs"])
    support_d1_hist = Counter()
    for (z, _c), st in census["pairs"].items():
        support_d1_hist[profiles[z]["d1"]] += len(st["supports"])
    retained = []
    for key, st in census["pairs"].items():
        z, c = key
        prof = profiles[z]
        if prof["d1"] != D1_TARGET or not st["clean"]:
            continue
        canonical = min(st["clean"], key=lambda model: model.indices)
        solve = split_solver(prof["g1"], prof["g2"], prof["d1"],
                             prof["d2"], row.omega)
        A, B = solve(canonical.locator)
        # Autodiv: (A N1 + B N2) / G is the deduplicated codeword.
        Ncomb = padd(pmul(A, prof["g1"][1]), pmul(B, prof["g2"][1]))
        q, rem = pdivmod(Ncomb, canonical.locator)
        assert not rem and pad(q, row.K) == c
        Wcan, Ncan = canonical_minimal_pair(prof["g1"], prof["d1"], row.K)
        hit = {
            "z": z, "c": c, "model": canonical, "A": A, "B": B,
            "W": Wcan, "N": Ncan, "nullity": prof["nullity"],
        }
        hit["fixed_B"] = determinant_quotient_diagnostic(row, prof, hit)
        assert hit["fixed_B"]["identity_ok"]
        assert hit["fixed_B"]["gluing_identity_ok"]
        assert hit["fixed_B"]["membership_in_W1_PltK"]
        retained.append(hit)

    # One minimal denominator per retained slope; LineRay may have several
    # codewords at a slope, but d1 and its canonical row belong to the word.
    per_slope = {}
    for hit in retained:
        per_slope.setdefault(hit["z"], hit)
        assert per_slope[hit["z"]]["W"] == hit["W"]
    slope_hits = list(per_slope.values())

    denominator_points = [hit["W"][:-1] for hit in slope_hits
                          if hit["W"][-1] == 1]
    denominator_vectors = [hit["W"] for hit in slope_hits]
    minimal_pair_vectors = [hit["W"] + hit["N"] for hit in slope_hits]
    locator_points = [hit["model"].locator[:-1] for hit in retained]
    locator_vectors = [hit["model"].locator for hit in retained]
    # These coordinates are basis-local across slopes, hence diagnostic only.
    split_vectors = [hit["A"] + hit["B"] for hit in retained]
    width = max((len(x) for x in split_vectors), default=0)
    split_vectors = [tuple(x) + (0,) * (width - len(x)) for x in split_vectors]

    fixed_B = [hit["fixed_B"] for hit in retained]
    pivot_hist = Counter(diag["pivot"] for diag in fixed_B)
    full_rank_hist = Counter(diag["full_rank"] for diag in fixed_B)
    direction_rank_hist = Counter(diag["monic_direction_rank"] for diag in fixed_B)
    gcd_hist = Counter(diag["gcd_B_W1_degree"] for diag in fixed_B)
    fixed_B_exceptions = [
        hit for hit in retained
        if (not hit["fixed_B"]["generic_rank_ok"]
            or not hit["fixed_B"]["structural_shape_ok"]
            or hit["fixed_B"]["gcd_B_W1_degree"] > 0)
    ]

    result = {
        "label": label,
        "u": tuple(u), "v": tuple(v),
        "input_sha256": hashlib.sha256(bytes(u) + bytes(v)).hexdigest(),
        "construction": construction,
        "d1_hist": dict(sorted(d1_hist.items())),
        "pair_d1_hist": dict(sorted(pair_d1_hist.items())),
        "support_d1_hist": dict(sorted(support_d1_hist.items())),
        "raw_supports": census["raw_supports"],
        "common_supports": census["common_supports"],
        "lineray": census["lineray"],
        "slopes": census["slopes"],
        "retained_lineray": len(retained),
        "retained_slopes": len(slope_hits),
        "retained_slope_values": sorted(per_slope),
        "unique_minimal_kernel": all(hit["nullity"] == 1 for hit in slope_hits),
        "denominator_affine_rank": affine_rank(denominator_points),
        "denominator_projective_dim": projective_dimension(denominator_vectors),
        "minimal_pair_projective_dim": projective_dimension(minimal_pair_vectors),
        "locator_section_affine_rank": affine_rank(locator_points),
        "locator_section_projective_dim": projective_dimension(locator_vectors),
        "basis_local_split_affine_rank": affine_rank(split_vectors),
        "pivot_hist": dict(sorted(pivot_hist.items())),
        "fixed_B_full_rank_hist": dict(sorted(full_rank_hist.items())),
        "fixed_B_direction_rank_hist": dict(sorted(direction_rank_hist.items())),
        "gcd_B_W1_degree_hist": dict(sorted(gcd_hist.items())),
        "fixed_B_exception_count": len(fixed_B_exceptions),
        "fixed_B_exceptions": fixed_B_exceptions,
        "retained": retained,
        "profiles": profiles,
    }
    return result


# --------------------------------------------------------------- line makers
def random_value_line(row, seed):
    rng = random.Random(seed)
    u = tuple(rng.randrange(P) for _ in range(N))
    v = tuple(rng.randrange(P) for _ in range(N))
    assert any(v)
    return u, v


def polynomial_line(row, seed):
    """Non-sparse first-interior polynomial control (not the planted word)."""
    rng = random.Random(seed)
    p0 = [rng.randrange(P) for _ in range(row.mprime)] + [rng.randrange(1, P)]
    p1 = [rng.randrange(P) for _ in range(row.mprime)] + [rng.randrange(1, P)]
    return eval_poly(p0), eval_poly(p1), (tuple(p0), tuple(p1))


def random_monic_root_free_degree4(rng):
    while True:
        f = [rng.randrange(P) for _ in range(D1_TARGET)] + [1]
        if all(peval(f, x) for x in D):
            return f


def projectively_equal(f, g):
    f, g = pnorm(f), pnorm(g)
    if not f or not g or len(f) != len(g):
        return False
    c = f[-1] * inv(g[-1]) % P
    return f == pscale(g, c)


def constrained_three_slope_line(row, models, seed, max_attempts):
    """Search exact rational presentations at z=0,1,2.

    Fixed pairwise-coprime monic W_i of degree four are chosen first.  The
    numerators N_i (degree <= K+3) are then solved from
        N_0/W_0 - 2 N_1/W_1 + N_2/W_2 = 0 on all x in D.
    This is linear in the numerator coefficients.  Candidates are accepted
    only after exact profile and full support-census checks.
    """
    rng = random.Random(seed)
    ncoef = row.K + D1_TARGET
    weights = (1, P - 2, 1)
    for attempt in range(1, max_attempts + 1):
        denoms = []
        while len(denoms) < 3:
            Wp = random_monic_root_free_degree4(rng)
            if all(pdeg(pgcd(Wp, old)) == 0 for old in denoms):
                denoms.append(Wp)
        if affine_rank([tuple(Wp[:-1]) for Wp in denoms]) < 2:
            continue

        mat = []
        for x in D:
            row_eq = []
            for a, Wp in zip(weights, denoms):
                factor = a * inv(peval(Wp, x)) % P
                row_eq.extend(factor * pow(x, j, P) % P for j in range(ncoef))
            mat.append(row_eq)
        ker = nullspace(mat, 3 * ncoef)
        if len(ker) <= 2 * row.K:
            # The 2K-dimensional affine-codeword-line kernel is always here.
            continue

        # Random exact combinations explore the non-codeword quotient while
        # allowing arbitrary affine codeword additions.
        for _ in range(80):
            coeff = [rng.randrange(P) for _ in ker]
            if not any(coeff):
                continue
            vector = [sum(coeff[a] * ker[a][j] for a in range(len(ker))) % P
                      for j in range(3 * ncoef)]
            nums = [pnorm(vector[i * ncoef:(i + 1) * ncoef]) for i in range(3)]
            words = [tuple(peval(Np, x) * inv(peval(Wp, x)) % P
                           for x in D)
                     for Np, Wp in zip(nums, denoms)]
            if not all((words[0][j] - 2 * words[1][j] + words[2][j]) % P == 0
                       for j in range(N)):
                raise AssertionError("constructed words are not collinear")
            u = words[0]
            v = tuple((b - a) % P for a, b in zip(words[0], words[1]))
            if not any(v):
                continue

            selected = []
            ok = True
            for i, word in enumerate(words):
                g1, _g2, d1, _d2, _ = popov_reduce(word, row.K)
                if d1 != D1_TARGET or len(profile_kernel(word, row.K, d1)) != 1:
                    ok = False
                    break
                if not projectively_equal(g1[0], denoms[i]):
                    ok = False
                    break
                selected.append((g1, word))
            if not ok:
                continue

            # Cheap exact word census before the full 97-slope analysis.
            ray_counts = [word_lineray_count(row, models, word)
                          for word in words]
            if not all(ray_counts):
                continue

            construction = {
                "attempt": attempt,
                "selected_slopes": SELECTED_SLOPES,
                "denominators": tuple(tuple(x) for x in denoms),
                "numerators": tuple(tuple(x) for x in nums),
                "selected_word_lineray": tuple(ray_counts),
                "kernel_dimension": len(ker),
            }
            result = analyze_line(row, models, "constrained-rational-fixture",
                                  u, v, construction)
            if result["common_supports"]:
                continue
            if not set(SELECTED_SLOPES).issubset(result["retained_slope_values"]):
                continue
            slope_groups = [
                [hit for hit in result["retained"] if hit["z"] == z]
                for z in SELECTED_SLOPES
            ]
            assert all(slope_groups)
            transversals = []
            for hits in itertools.product(*slope_groups):
                locator_gcd = pgcd_many(hit["model"].locator for hit in hits)
                roots = domain_root_indices(locator_gcd)
                transversals.append((pdeg(locator_gcd), roots, hits))
            transversals.sort(
                key=lambda item: (
                    item[0], item[1],
                    tuple(hit["model"].indices for hit in item[2]),
                )
            )
            selected_hits = list(transversals[0][2])
            selected_W = [hit["W"] for hit in selected_hits]
            if affine_rank([Wp[:-1] for Wp in selected_W]) < 2:
                continue
            pairwise_denominator_gcd_degrees = tuple(
                pdeg(pgcd(selected_W[i], selected_W[j]))
                for i in range(3) for j in range(i + 1, 3)
            )
            if any(degree != 0 for degree in pairwise_denominator_gcd_degrees):
                continue
            all_locator_gcd = pgcd_many(
                hit["model"].locator for hit in result["retained"]
            )
            result["construction"]["selected_denominator_affine_rank"] = 2
            result["construction"]["selected_pairwise_gcd_degrees"] = (
                pairwise_denominator_gcd_degrees
            )
            result["construction"]["locator_transversal_gcd_degrees"] = tuple(
                item[0] for item in transversals
            )
            result["construction"]["locator_transversal_gcd_root_indices"] = tuple(
                item[1] for item in transversals
            )
            result["construction"]["locator_transversal_zero_gcd_count"] = sum(
                item[0] == 0 for item in transversals
            )
            result["construction"]["all_retained_locator_gcd_degree"] = pdeg(
                all_locator_gcd
            )
            result["construction"]["all_retained_locator_gcd_root_indices"] = (
                domain_root_indices(all_locator_gcd)
            )
            return result
    return None


# ------------------------------------------------------------------- output
def compact_line(result):
    return (
        f"{result['label']}: sha256={result['input_sha256'][:16]} "
        f"d1(all slopes)={result['d1_hist']} "
        f"supports={result['raw_supports']} LineRay={result['lineray']} "
        f"slopes={result['slopes']} common={result['common_supports']} "
        f"retained(d1=4,noncommon,aperiodic)="
        f"{result['retained_lineray']}/{result['retained_slopes']} "
        f"denom-rank(a/p)={result['denominator_affine_rank']}/"
        f"{result['denominator_projective_dim']} "
        f"locator-rank(a/p)={result['locator_section_affine_rank']}/"
        f"{result['locator_section_projective_dim']}"
    )


def compact_lattice(result):
    return (
        f"  d1=4 census/rays="
        f"{result['support_d1_hist'].get(D1_TARGET, 0)}/"
        f"{result['pair_d1_hist'].get(D1_TARGET, 0)} "
        f"pivot={result['pivot_hist']} "
        f"fixed-B rank(full/direction)="
        f"{result['fixed_B_full_rank_hist']}/"
        f"{result['fixed_B_direction_rank_hist']} "
        f"gcd(B,W1)-degree={result['gcd_B_W1_degree_hist']} "
        f"exceptions={result['fixed_B_exception_count']}"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--max-attempts", type=int, default=240,
                        help="denominator triples for the constrained fixture")
    args = parser.parse_args(argv)

    print("=== BC first-interior general-line experiment ===")
    print(f"status: {STATUS}")
    print(f"problem_id: {PROBLEM_ID}")
    print(f"seed: {args.seed}")
    print(f"field/domain: F_{P}, D=mu_{N}, generator={H}, D={list(D)}")
    print("claim_boundary: exact toy enumeration only; q=p cannot test the "
          "extension/subfield cell; retained means only d1=4 + noncommon + "
          "cyclic-aperiodic support, before common-GCD/tangent first match")

    all_results = []
    models_by_row = {}
    for offset, row in enumerate(ROWS):
        print(f"\nrow {row.label}: (K,m,w,d1,omega)="
              f"({row.K},{row.m},{W_DEPTH},{D1_TARGET},{row.omega})")
        models = support_models(row)
        models_by_row[row.label] = models
        print(f"enumerated supports: C({N},{row.m})={len(models)}; "
              f"aperiodic={sum(model.aperiodic for model in models)}")

        u, v = random_value_line(row, args.seed + 1000 * offset + 11)
        random_result = analyze_line(row, models, "arbitrary-value-control", u, v)
        all_results.append((row, random_result))
        print(compact_line(random_result))
        print(compact_lattice(random_result))

        u, v, polys = polynomial_line(row, args.seed + 1000 * offset + 29)
        poly_result = analyze_line(
            row, models, "non-sparse-polynomial-control", u, v,
            {"coefficient_polynomials": polys},
        )
        all_results.append((row, poly_result))
        print(compact_line(poly_result))
        print(compact_lattice(poly_result))

    # Row B has one more numerator degree of freedom than the unavoidable
    # affine-codeword-line kernel, making the three-denominator construction
    # an efficient deterministic fixture hunt.  Row A remains covered by the
    # arbitrary-value and non-sparse polynomial controls above.
    row_b = next(row for row in ROWS if row.label == "B")
    print("\nsearch: constrained three-slope rational pre-first-match fixture at row B")
    witness = constrained_three_slope_line(
        row_b, models_by_row["B"], args.seed + 7001, args.max_attempts,
    )
    if witness is None:
        print(f"FIXTURE: none in deterministic budget {args.max_attempts}")
        print("RESULT: EXPERIMENT COMPLETED; NO RANK>=2 FIXTURE IN BUDGET")
        return 0

    all_results.append((row_b, witness))
    print(compact_line(witness))
    print(compact_lattice(witness))
    c = witness["construction"]
    print(f"construction: attempt={c['attempt']} kernel_dim={c['kernel_dimension']} "
          f"selected_slopes={list(c['selected_slopes'])} "
          f"selected_word_LineRay={list(c['selected_word_lineray'])}")
    print(f"selected pairwise denominator gcd degrees="
          f"{list(c['selected_pairwise_gcd_degrees'])}")
    print("error-locator transversal common-GCD degrees="
          f"{list(c['locator_transversal_gcd_degrees'])} "
          "root_indices="
          f"{[list(x) for x in c['locator_transversal_gcd_root_indices']]} "
          f"zero_gcd={c['locator_transversal_zero_gcd_count']}")
    print("all retained error-locator common-GCD: "
          f"degree={c['all_retained_locator_gcd_degree']} "
          f"root_indices={list(c['all_retained_locator_gcd_root_indices'])}")
    print(f"selected denominators={list(map(list, c['denominators']))}")
    print(f"fixture line u={list(witness['u'])}")
    print(f"fixture line v={list(witness['v'])}")
    print("retained fixed-B cases:")
    for hit in sorted(witness["retained"], key=lambda item: (item["z"], item["c"])):
        diag = hit["fixed_B"]
        print(
            f"  z={hit['z']:2d} support={list(hit['model'].indices)} "
            f"{diag['pivot']} degW1={diag['deg_W1']} degB={diag['deg_B']} "
            f"gcddeg={diag['gcd_B_W1_degree']} "
            f"rank={diag['full_rank']}/{diag['monic_direction_rank']} "
            f"identity={diag['identity_ok']} "
            f"gluing={diag['gluing_identity_ok']} "
            f"N1+gamma*B*V_in_W1*P_<K="
            f"{diag['membership_in_W1_PltK']}"
        )

    rank2 = witness["denominator_affine_rank"] >= 2
    assert rank2
    assert witness["denominator_projective_dim"] >= 2
    assert witness["common_supports"] == 0
    assert witness["unique_minimal_kernel"]
    assert set(SELECTED_SLOPES).issubset(witness["retained_slope_values"])
    print("FIXTURE: rank>=2 pre-first-match minimal-denominator family FOUND "
          f"(denominator affine rank={witness['denominator_affine_rank']}, "
          f"projective dimension={witness['denominator_projective_dim']}, "
          f"retained LineRay={witness['retained_lineray']})")
    assert c["locator_transversal_zero_gcd_count"] == 0
    print("first_match_routing: every one-locator-per-selected-slope "
          "transversal has a positive fixed-D-root GCD; the fixture is routed "
          "through common-GCD cells")
    print("interpretation: this falsifies only the pre-common-GCD toy-level "
          "assumption that every general first-interior line has a rank-one "
          "minimal-denominator core; it does NOT certify an unpaid residual")
    print("unresolved_first_match_labels: prop:exact-tangent-cell beyond the "
          "common-support proxy; thm:subfield-confinement and "
          "prop:extension-cell-target (q=p toy); witness-exhaustive "
          "first-match atlas / deployed balanced-core residual compiler")
    print("RESULT: EXPERIMENTAL RANK>=2 PRE-FIRST-MATCH FIXTURE; "
          "COMMON-GCD ROUTING PRESENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
