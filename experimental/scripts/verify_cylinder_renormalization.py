#!/usr/bin/env python3
r"""Verifier: failing bands are wide + cylinder renormalization on the Sidon-paired class (hard input 2).

Checks, per the note experimental/notes/thresholds/cylinder_renormalization.md:

V1  U1 (failing bands are wide): |hatf(xi)| <= M for EVERY xi (full scans,
    B in {6,8} base 3 and B = 6 base 5, floats under the exact Parseval
    guard sum hatf^2 == c * M2); the integer identity c = 2L - 1 on base 3
    (even B <= 64) pinning the width constant c/L -> 2; instantiated width
    chain |A| * M^2 >= sum_{xi in A} hatf(xi)^2 = c ||h_A||_2^2 on the
    six-family band battery.
V2  U3 (subgroup renormalization, base 3): for B in {6,8}, k in {1,2,3},
    ALL m in [0, 3^{B-k}):
        hatf_B(3^k m) == sum_j C(2k, B-j) [z^j] p_{B-k, m}
    to 1e-9 M, where p_{B-k,m} is the scale-(B-k) per-pair product; the
    scale-(B-k) graded weights are themselves Parseval-guarded at their
    own scale ([z^{B-k}] slice: sum_m == c' * M2(B-k)).
V3  U3 twisted (r != 0): for B = 6, k in {1,2,3}, every r in [1, 3^k) and
    ALL m: hatf_B(r + 3^k m) == [z^B](T_r(z) * p^{phi(r)}_{B-k,m}(z)) with
    the top factors T_r at angles 2 pi r 3^{i-1}/3^B (i > B-k) and the low
    factors phase-shifted by phi_i(r) = 2 pi r 3^{i-1}/3^B, to 1e-9 M.
V4  Cube corollary (B = 6, base 3):
    (a) HIERARCHY FLATNESS: on subgroup bands (k in {1,2}) AND twisted
    cosets (k = 1, r in {1,2}), EVERY pattern D != empty has
    hcube_v(D) == 0 (absolute deviation <= 1e-10; the nonzero spectrum is
    exactly the per-class D = empty values -- 31 of 364 coefficients);
    (b) RENORMALIZED VALUES: on the subgroup bands, the direct brute cube
    coefficient (every D, the D = empty values being the live ones) equals
    the scale-(B-k) m-sum with the graded-convolved weight (absolute
    deviation <= 1e-9), and the D = empty values take few distinct values
    per level (pinned counts);
    (c) SLICE STAIRCASE (the flatness mechanism, brute): for EVERY slice
    size j (not only j = B), within-class fiber counts of the j-slice are
    equal (B in {4,6}, both bases) -- every graded slice is class-constant,
    which with the polynomial-level renormalization PROVES subgroup-coset
    flatness; twisted flatness is VERIFIED by (a).
V5  Base-5 COUNTEREXAMPLE pin: the analogous k = 1 identity FAILS on base 5
    (c = (5^B+1)/2 is not a power of the base): the max deviation over m is
    pinned ABOVE 0.05 M (exhibited witness), while base 3 sits below
    1e-9 M -- the renormalization is a base-3 (c = 3^B) phenomenon.
V6  Cross-consistency: brute class/fiber grid == closed forms including
    cross-class syndrome disjointness (B in {4,6}, both bases); shell
    census 42; M2 pins 3584 / 97444.
V7  Hierarchy relevance: disjoint bands are orthogonal, so coset spectral
    masses ADD exactly (B in {6,10}); the per-coset SHARES are pinned
    (.2065/.3968/.3968 at B = 6 and .3164/.3418/.3418 at B = 10, k = 1:
    the subgroup coset is under-weighted at small B, the shares drift
    toward 1/3); and the subgroup band's full-norm failure ratio GROWS
    with B at fixed k (pinned R = 0.4615 / 0.6226 / 0.7834 at
    B = 6/8/10, k = 1, strictly increasing) -- the hierarchy carries a
    growing share of the failure, while the failing maximal band IS the
    depth-k coset union at every k.

Deterministic, stdlib only.  --tamper-selftest mutates five load-bearing
pieces and verifies each is caught.  --emit-certificate PATH writes JSON.
"""
import sys
from math import comb, cos, sin, pi, sqrt
from itertools import combinations
from collections import defaultdict

CHECKS = []
QUIET = False


def check(name, ok):
    CHECKS.append((name, bool(ok)))
    if not ok and not QUIET:
        print(f"FAIL: {name}")
    return ok


# ---------------------------------------------------------------- class data

def sidon_P(B, base):
    return [base ** i for i in range(B)]


def sidon_c(B, base):
    return 2 * sum(sidon_P(B, base)) + 1


def fiber_w(B, s):
    return comb(B - s, (B - s) // 2)


def closed_M(B):
    return comb(2 * B, B)


def closed_M2(B):
    return sum(comb(B, s) * 2 ** s * fiber_w(B, s) ** 2
               for s in range(B % 2, B + 1, 2))


def closed_L(B):
    return (3 ** B + 1) // 2 if B % 2 == 0 else (3 ** B - 1) // 2


def factors_poly(angles):
    """prod_i (1 + z^2 + 2 z cos(angle_i)) as a coefficient list."""
    poly = [1.0]
    for th in angles:
        t = 2 * cos(th)
        new = [0.0] * (len(poly) + 2)
        for i, a in enumerate(poly):
            new[i] += a
            new[i + 1] += a * t
            new[i + 2] += a
        poly = new
    return poly


def conv_coeff(k, B, p):
    """[z^B] (1+z)^{2k} * p(z) = sum_j C(2k, B-j) p_j."""
    return sum(comb(2 * k, B - j) * p[j]
               for j in range(max(0, B - 2 * k), min(len(p) - 1, B) + 1))


def cube_coeff(cube, dbits, s):
    """Normalized sign-cube Fourier coefficient of the dict {bits: value}."""
    return sum(((-1) ** bin(bits & dbits).count("1")) * v
               for bits, v in cube.items()) / 2 ** s


def hatf_scan(B, base):
    c = sidon_c(B, base)
    vals = [factors_poly([2 * pi * ((j * base ** i) % c) / c
                          for i in range(B)])[B] for j in range(c)]
    return c, vals


def brute_classes(B, base):
    P = sidon_P(B, base)
    c = sidon_c(B, base)
    T = P + [p_ for p_ in (c - p for p in P)]
    pairs = [(P[i], c - P[i]) for i in range(B)]
    out = defaultdict(lambda: defaultdict(int))
    for S in combinations(T, B):
        Ss = set(S)
        v = tuple(((pairs[i][0] in Ss) + (pairs[i][1] in Ss)) % 2
                  for i in range(B))
        out[v][sum(S) % c] += 1
    return out


def band_battery(c, hf, M):
    shell = sorted((j for j in range(1, c) if abs(hf[j]) * 10 >= M),
                   key=lambda j: -abs(hf[j]))

    def sym(idxs):
        A = set()
        for j in idxs:
            A.add(j % c)
            A.add((-j) % c)
        A.discard(0)
        return sorted(A)

    return {"top2": sym(shell[:2]), "shell10": sym(shell[:10]),
            "shell_all": sym(shell), "dyadic_lo": sym(range(1, 33)),
            "dyadic_mid": sym(range(33, 97)),
            "maximal": sym(range(1, (c + 1) // 2))}


# ------------------------------------------------------------ V1 -- width

def v1_width(cert=None):
    check("V1 base-3 integer identity c == 2L - 1, even B <= 64",
          all(3 ** B == 2 * closed_L(B) - 1 for B in range(4, 65, 2)))
    for B, base in ((6, 3), (8, 3), (6, 5)):
        c, hf = hatf_scan(B, base)
        M = closed_M(B)
        check(f"V1 Parseval guard sum hatf^2 == c*M2 to 1e-6 rel (B={B}, base {base})",
              abs(sum(x * x for x in hf) - c * closed_M2(B))
              <= 1e-6 * c * closed_M2(B))
        check(f"V1 |hatf(xi)| <= M for EVERY xi (B={B}, base {base})",
              all(abs(x) <= M * (1 + 1e-9) for x in hf))
        if B == 6:
            ok_chain = True
            for name, Ab in band_battery(c, hf, M).items():
                lhs = len(Ab) * M * M
                rhs = sum(hf[xi] ** 2 for xi in Ab)
                if lhs < rhs * (1 - 1e-9):
                    ok_chain = False
            check(f"V1 width chain |A| M^2 >= sum_A hatf^2 (arithmetic consistency of U1's two halves) (B=6, base {base})",
                  ok_chain)


# --------------------------------------------- V2 -- subgroup renormalization

def v2_renormalization(cert=None):
    for B in (6, 8):
        c = 3 ** B
        M = closed_M(B)
        _c, hf = hatf_scan(B, 3)
        for k in (1, 2, 3):
            Bs = B - k
            cs = 3 ** Bs
            worst = 0.0
            slice_sum = 0.0
            for m in range(cs):
                p = factors_poly([2 * pi * ((m * 3 ** i) % cs) / cs
                                  for i in range(Bs)])
                worst = max(worst, abs(hf[(3 ** k * m) % c]
                                       - conv_coeff(k, B, p)))
                slice_sum += p[Bs] ** 2
            check(f"V2 subgroup renormalization hatf_B(3^k m) == C(2k,B-j)-conv, ALL m (B={B}, k={k})",
                  worst <= 1e-9 * M)
            check(f"V2 scale-(B-k) Parseval guard at its own scale (B={B}, k={k})",
                  abs(slice_sum - cs * closed_M2(Bs))
                  <= 1e-6 * cs * closed_M2(Bs))
            if cert is not None:
                cert["renorm_maxdev"][f"B{B}_k{k}"] = f"{worst:.2e}"


# ------------------------------------------------------- V3 -- twisted form

def v3_twisted(cert=None):
    B = 6
    c = 3 ** B
    M = closed_M(B)
    _c, hf = hatf_scan(B, 3)
    for k in (1, 2, 3):
        Bs = B - k
        cs = 3 ** Bs
        worst = 0.0
        for r in range(1, 3 ** k):
            top = factors_poly([2 * pi * (r * 3 ** (i - 1) % c) / c
                                for i in range(Bs + 1, B + 1)])
            for m in range(cs):
                low = factors_poly([2 * pi * ((m * 3 ** i) % cs) / cs
                                    + 2 * pi * (r * 3 ** i % c) / c
                                    for i in range(Bs)])
                full = [0.0] * (2 * B + 1)
                for a, va in enumerate(top):
                    if va:
                        for b_, vb in enumerate(low):
                            if a + b_ <= 2 * B:
                                full[a + b_] += va * vb
                worst = max(worst, abs(hf[(r + 3 ** k * m) % c] - full[B]))
        check(f"V3 twisted renormalization, all r in [1,3^k), ALL m (B=6, k={k})",
              worst <= 1e-9 * M)
        if cert is not None:
            cert["twisted_maxdev"][f"k{k}"] = f"{worst:.2e}"


# ------------------------------------------------------ V4 -- cube corollary

def coset_band(c, k, r):
    return sorted({(r + 3 ** k * m) % c for m in range(3 ** 6 // 3 ** k)}
                  - {0})


def v4_cube_corollary(cert=None):
    B, base = 6, 3
    c = 3 ** B
    M = closed_M(B)
    P = sidon_P(B, base)
    _c, hf = hatf_scan(B, base)
    costab = [cos(2 * pi * r / c) for r in range(c)]
    cls = brute_classes(B, base)

    def cube_data(Ab):
        """{class: {dbits: coefficient}} for the band, brute."""
        hv = {}
        out = {}
        for v in cls:
            s = sum(v)
            if s < 2:
                continue
            U = [i for i in range(B) if v[i]]
            sigs = {}
            for bits in range(2 ** s):
                eps = [1 if (bits >> t) & 1 == 0 else -1 for t in range(s)]
                sigs[bits] = sum(e * P[U[t]] for t, e in enumerate(eps)) % c
            for sig in sigs.values():
                if sig not in hv:
                    hv[sig] = sum(hf[xi] * costab[(xi * sig) % c]
                                  for xi in Ab) / c
            cube = {bits: hv[sigs[bits]] for bits in sigs}
            out[v] = {dbits: cube_coeff(cube, dbits, s)
                      for dbits in range(2 ** s)}
        return out

    # (a) hierarchy flatness: subgroup AND twisted cosets
    for k, r in ((1, 0), (2, 0), (1, 1), (1, 2)):
        band = coset_band(c, k, r) if r else sorted(
            {(3 ** k * m) % c for m in range(1, 3 ** (B - k))})
        data = cube_data(band)
        ok_flat, nonzero = True, 0
        for v, coeffs in data.items():
            for dbits, x in coeffs.items():
                if dbits != 0:
                    if abs(x) > 1e-10:
                        ok_flat = False
                elif abs(x) > 1e-12:
                    nonzero += 1
        check(f"V4a hierarchy flatness: all D != empty vanish (B=6, k={k}, r={r})",
              ok_flat)
        if (k, r) == (1, 0):
            check("V4a nonzero cube spectrum == the 31 per-class D=empty values (B=6, k=1, r=0)",
                  nonzero == 31)

    # (b) subgroup renormalized values + distinct-value pins
    for k in (1, 2):
        Bs = B - k
        cs = 3 ** Bs
        band = sorted({(3 ** k * m) % c for m in range(1, cs)})
        data = cube_data(band)
        conv = {m: conv_coeff(k, B, factors_poly(
            [2 * pi * ((m * 3 ** i) % cs) / cs for i in range(Bs)]))
            for m in range(cs)}
        ok_renorm, wdev = True, 0.0
        level_vals = defaultdict(set)
        for v, coeffs in data.items():
            s = sum(v)
            U = [i for i in range(B) if v[i]]
            level_vals[s].add(round(coeffs[0], 9))
            for dbits, br in coeffs.items():
                if any(U[t] >= Bs for t in range(s) if (dbits >> t) & 1):
                    continue
                acc = complex(0.0)
                for m in range(1, cs):
                    prod = complex(1.0)
                    for t in range(s):
                        i = U[t]
                        if i >= Bs:
                            continue
                        th = 2 * pi * ((m * 3 ** i) % cs) / cs
                        prod *= ((-1j * sin(th))
                                 if (dbits >> t) & 1 else cos(th))
                    acc += conv[m] * prod
                acc /= c
                dev = abs(acc - br)
                wdev = max(wdev, dev)
                if dev > 1e-9:
                    ok_renorm = False
        check(f"V4b cube values renormalize to the graded-convolved scale-(B-k) sum (B=6, k={k})",
              ok_renorm)
        check(f"V4b D=empty values take <= 3 distinct values per level (B=6, k={k})",
              all(len(vals) <= 3 for vals in level_vals.values()))
        if cert is not None:
            cert["cube_renorm_maxdev"][f"k{k}"] = f"{wdev:.2e}"

    # (c) slice staircase: every graded slice is class-constant (brute)
    ok_slice = True
    for base2 in (3, 5):
        for B2 in (4, 6):
            P2 = sidon_P(B2, base2)
            c2 = sidon_c(B2, base2)
            T2 = P2 + [c2 - p for p in P2]
            pairs = [(P2[i], c2 - P2[i]) for i in range(B2)]
            for j in range(0, 2 * B2 + 1):
                sl = defaultdict(lambda: defaultdict(int))
                for S in combinations(T2, j):
                    Ss = set(S)
                    v = tuple(((pairs[i][0] in Ss) + (pairs[i][1] in Ss)) % 2
                              for i in range(B2))
                    sl[v][sum(S) % c2] += 1
                for v, fibs in sl.items():
                    if len(set(fibs.values())) != 1:
                        ok_slice = False
    check("V4c slice staircase: EVERY slice size j is class-constant (B in {4,6}, both bases)",
          ok_slice)


# ------------------------------------------------- V5 -- base-5 counterexample

def v5_base5_counterexample(cert=None):
    B, base, k = 6, 5, 1
    c = sidon_c(B, base)
    M = closed_M(B)
    _c, hf = hatf_scan(B, base)
    Bs = B - k
    cs = sidon_c(Bs, base)
    worst = 0.0
    for m in range(cs):
        p = factors_poly([2 * pi * ((m * base ** i) % cs) / cs
                          for i in range(Bs)])
        worst = max(worst, abs(hf[(base ** k * m) % c] - conv_coeff(k, B, p)))
    check("V5 base-5 COUNTEREXAMPLE: the k=1 renormalization FAILS (max dev > 0.05 M)",
          worst > 0.05 * M)
    if cert is not None:
        cert["base5_maxdev_over_M"] = round(worst / M, 4)


# ------------------------------------------------- V6 -- cross-consistency

def v6_cross():
    ok_prof, ok_disj = True, True
    for base in (3, 5):
        for B in (4, 6):
            cls = brute_classes(B, base)
            n_syn, union = 0, set()
            for v, d in cls.items():
                s = sum(v)
                if len(d) != 2 ** s or set(d.values()) != {fiber_w(B, s)}:
                    ok_prof = False
                n_syn += len(d)
                union.update(d)
            if len(union) != n_syn:
                ok_disj = False
    check("V6 brute class/fiber grid == closed forms (B in {4,6}, both bases)", ok_prof)
    check("V6 cross-class syndrome disjointness (B in {4,6}, both bases)", ok_disj)
    c, hf = hatf_scan(6, 3)
    check("V6 base-3 shell census rho=1/10 == 42",
          sum(1 for j in range(1, c) if abs(hf[j]) * 10 >= closed_M(6)) == 42)
    check("V6 M2 pins (3584 / 97444)",
          closed_M2(6) == 3584 and closed_M2(8) == 97444)


# ---------------------------------------------- V7 -- hierarchy relevance

def v7_relevance(cert=None):
    share_pins = {6: (0.2065, 0.3968, 0.3968), 10: (0.3164, 0.3418, 0.3418)}
    ok_add, ok_shares = True, True
    for B in (6, 10):
        c, hf = hatf_scan(B, 3)
        tot = sum(hf[xi] ** 2 for xi in range(1, c))
        parts = [sum(hf[xi] ** 2 for xi in range(1, c) if xi % 3 == r)
                 for r in (0, 1, 2)]
        if abs(sum(parts) - tot) > 1e-9 * tot:
            ok_add = False
        for p, pin in zip(parts, share_pins[B]):
            if abs(p / tot - pin) > 5e-4:
                ok_shares = False
        if cert is not None:
            cert["coset_shares"][str(B)] = [round(p / tot, 4) for p in parts]
    check("V7 coset mass bookkeeping (partition arithmetic; the pinned SHARES below are the content) (B in {6,10})",
          ok_add)
    check("V7 coset share pins (.2065/.3968/.3968 at B=6; .3164/.3418/.3418 at B=10): subgroup coset under-weighted, shares drifting toward 1/3",
          ok_shares)
    Rs = []
    for B in (6, 8, 10):
        cB, hfB = hatf_scan(B, 3)
        M, L = closed_M(B), closed_L(B)
        mass = sum(hfB[xi] ** 2 for xi in range(1, cB) if xi % 3 == 0)
        Rs.append(sqrt(L * mass / cB) / M)
    check("V7 subgroup-band R_A grows with B at k=1 (pins .4615/.6226/.7834)",
          Rs[0] < Rs[1] < Rs[2]
          and abs(Rs[0] - 0.4615) < 5e-4 and abs(Rs[1] - 0.6226) < 5e-4
          and abs(Rs[2] - 0.7834) < 5e-4)
    if cert is not None:
        cert["subgroup_R_k1"] = [round(r, 4) for r in Rs]


# ----------------------------------------------------------------- driver

def run_all(quiet=False, cert=None):
    global QUIET, CHECKS
    QUIET = quiet
    CHECKS = []
    if cert is not None:
        cert.update({"renorm_maxdev": {}, "twisted_maxdev": {},
                     "cube_renorm_maxdev": {}, "coset_shares": {}})
    v1_width(cert)
    v2_renormalization(cert)
    v3_twisted(cert)
    v4_cube_corollary(cert)
    v5_base5_counterexample(cert)
    v6_cross()
    v7_relevance(cert)
    bad = [n for n, ok in CHECKS if not ok]
    if not quiet:
        print(f"RESULT: {'PASS' if not bad else 'FAIL'} "
              f"({len(CHECKS) - len(bad)}/{len(CHECKS)})")
    return not bad


def tamper_selftest():
    """Mutate five load-bearing pieces; each must flip PASS -> FAIL."""
    me = sys.modules[__name__]
    caught = 0
    orig_cv = me.conv_coeff
    me.conv_coeff = lambda k, B, p: sum(
        comb(2 * k, B - j + 1) * p[j]
        for j in range(max(0, B - 2 * k), min(len(p) - 1, B) + 1)
        if 0 <= B - j + 1 <= 2 * k)
    if not run_all(quiet=True):
        caught += 1
    me.conv_coeff = orig_cv
    orig_fp = me.factors_poly
    def bad_fp(angles):
        p = orig_fp(angles)
        return [x * 1.0005 for x in p]
    me.factors_poly = bad_fp
    if not run_all(quiet=True):
        caught += 1
    me.factors_poly = orig_fp
    orig_m2 = me.closed_M2
    me.closed_M2 = lambda B: orig_m2(B) + 1
    if not run_all(quiet=True):
        caught += 1
    me.closed_M2 = orig_m2
    orig_L = me.closed_L
    me.closed_L = lambda B: orig_L(B) + 1
    if not run_all(quiet=True):
        caught += 1
    me.closed_L = orig_L
    orig_w = me.fiber_w
    me.fiber_w = lambda B, s: orig_w(B, s) + (1 if s == B else 0)
    if not run_all(quiet=True):
        caught += 1
    me.fiber_w = orig_w
    print(f"tamper-selftest: caught {caught}/5")
    ok = run_all()
    return caught == 5 and ok


def emit_certificate(path):
    import json
    cert = {}
    ok = run_all(quiet=True, cert=cert)
    cert["all_checks_pass"] = ok
    cert["n_checks"] = len(CHECKS)
    cert["float_note"] = ("all trigonometric scans are floats under exact "
                          "Parseval guards at BOTH scales; V1 integer "
                          "identity and V6 pins are exact")
    with open(path, "w") as fh:
        json.dump(cert, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"certificate written: {path}")


if __name__ == "__main__":
    if "--tamper-selftest" in sys.argv:
        sys.exit(0 if tamper_selftest() else 1)
    if "--emit-certificate" in sys.argv:
        emit_certificate(sys.argv[sys.argv.index("--emit-certificate") + 1])
        sys.exit(0)
    sys.exit(0 if run_all() else 1)
