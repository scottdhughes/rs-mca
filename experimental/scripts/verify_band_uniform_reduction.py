#!/usr/bin/env python3
r"""Verifier: band-uniform signed death + narrow-band cube certificate on the Sidon-paired class (hard input 2).

Checks, per the note experimental/notes/thresholds/band_uniform_cube_reduction.md:

V1  T1 exact integer ingredients: f_max^2 L < M^2 (even B <= 64); the
    f_max^2 relaxation c^2 sum f^2 h_+^2 <= f_max^2 * c^2 sum h_+^2 at
    B in {6,8} (maximal band, exact integers); the K = 2^{B/2}
    cross-multiplied unsatisfiability on the maximal band (exact integers,
    cross-pinned to the fold-charge packet's 1771440 / 475308288).
V2  T1 band scans (B = 6, BOTH bases; floats under the exact Parseval guard
    sum_j hatf^2 == c * M2 to 1e-6 rel): for each band in a six-family
    battery (top-2 shell, shell-10, full rho=1/10 shell, two dyadic blocks,
    maximal): ||h_A||_2 is the FULL Z_c norm, computed spectrally
    (||h_A||_2^2 = sum_{xi in A} hatf(xi)^2 / c); the projection identity
    <f, h_A> == ||h_A||_2^2 is itself a check (it ties the image table to
    the spectrum); the ell^2 budget sum_sigma f^2 omega^2 <= f_max^2 (the
    multiplicity-free cap); Omega_+ >= ||h_A||_2; and the piece floor
    K_min = Omega_+^2 / budget >= ||h_A||_2^2 / f_max^2 (the T1 chain).
V3  T2 certificate identity (same scans): for every band with |A| <= 200,
    every class at s >= 2, EVERY pattern D subseteq U: the brute sign-cube
    Fourier coefficient of h_A on the class equals
    (1/c) sum_{xi in A} hatf(xi) prod_{i in D}(-i sin theta_i(xi))
    prod_{i in U \ D}(cos theta_i(xi))    (bands exclude 0: no M/c shift).
    Odd-|D| coefficients vanish identically (eps -> -eps symmetry) and that
    vanishing is checked; the substantive identity content is even |D|.
    The maximal band is covered by the fold-charge packet's all-pattern scan
    (h_maximal = f - M/c exactly); here it contributes the flat
    specialization only (V4).
V4  T3 accounting: per class, the cube-Parseval identity
    sum_D hcube_v(D)^2 == 2^{-s} sum_eps h_A(sigma_eps)^2 (every scanned
    band; the floor itself is the triangle inequality, proved in the note,
    with its numerical content carried by this identity and the exactness
    case); maximal band ONLY: the D = empty floor equals the FULL cube
    ell^1 on every class (flatness).
V5  Cross-consistency: brute class/fiber grid == closed forms INCLUDING
    cross-class syndrome disjointness (B in {4,6}, both bases); the base-3
    rho = 1/10 shell census == 42 (resonant-folding pin); M2 pins
    3584 / 97444.

Deterministic, stdlib only.  --tamper-selftest mutates six load-bearing
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


def fmax_of(B):
    return comb(B, B // 2)


def brute_classes(B, base):
    P = sidon_P(B, base)
    c = sidon_c(B, base)
    T = P + [c - p for p in P]
    pairs = [(P[i], c - P[i]) for i in range(B)]
    out = defaultdict(lambda: defaultdict(int))
    for S in combinations(T, B):
        Ss = set(S)
        v = tuple(((pairs[i][0] in Ss) + (pairs[i][1] in Ss)) % 2
                  for i in range(B))
        out[v][sum(S) % c] += 1
    return out


def hatf_scan(B, base):
    c = sidon_c(B, base)
    P = sidon_P(B, base)
    vals = []
    for j in range(c):
        poly = [1.0]
        for A in P:
            th = 2 * pi * ((j * A) % c) / c
            t = 2 * cos(th)
            new = [0.0] * (len(poly) + 2)
            for i, a in enumerate(poly):
                new[i] += a
                new[i + 1] += a * t
                new[i + 2] += a
            poly = new
        vals.append(poly[B])
    return c, P, vals


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

    return {
        "top2": sym(shell[:2]),
        "shell10": sym(shell[:10]),
        "shell_all": sym(shell),
        "dyadic_lo": sym(range(1, 33)),
        "dyadic_mid": sym(range(33, 97)),
        "maximal": sym(range(1, (c + 1) // 2)),
    }


def h_table(Aband, c, hf, costab, image):
    """h_A(sigma) for sigma in image, via direct band sum (floats)."""
    return {sig: sum(hf[xi] * costab[(xi * sig) % c] for xi in Aband) / c
            for sig in image}


def cube_coeff(cube, dbits, s):
    """Normalized sign-cube Fourier coefficient of the dict {bits: value}."""
    return sum(((-1) ** bin(bits & dbits).count("1")) * v
               for bits, v in cube.items()) / 2 ** s


# ------------------------------------------------------------ V1 -- T1 ints

def cLedger_total(B):
    c = 3 ** B
    return sum(comb(B, s) * 2 ** s * fiber_w(B, s)
               * max(0, c * fiber_w(B, s) - closed_M(B))
               for s in range(B % 2, B + 1, 2))


def cSq_total(B):
    c = 3 ** B
    return sum(comb(B, s) * 2 ** s * fiber_w(B, s) ** 2
               * max(0, c * fiber_w(B, s) - closed_M(B)) ** 2
               for s in range(B % 2, B + 1, 2))


def cH2_total(B):
    c = 3 ** B
    return sum(comb(B, s) * 2 ** s
               * max(0, c * fiber_w(B, s) - closed_M(B)) ** 2
               for s in range(B % 2, B + 1, 2))


def v1_integers():
    check("V1 rate ingredient f_max^2 L < M^2, even 4 <= B <= 64",
          all(fmax_of(B) ** 2 * closed_L(B) < closed_M(B) ** 2
              for B in range(4, 65, 2)))
    check("V1 f_max^2 relaxation: c^2 sum f^2 h_+^2 <= f_max^2 c^2 sum h_+^2 (B in {6,8}, exact)",
          all(cSq_total(B) <= fmax_of(B) ** 2 * cH2_total(B) for B in (6, 8)))
    check("V1 maximal-band K = 2^{B/2} unsatisfiable (exact cross-mult, B in {6,8})",
          all(2 ** (B // 2) * cSq_total(B) < cLedger_total(B) ** 2
              for B in (6, 8)))
    check("V1 fold-charge integer cross-pins (1771440 / 475308288)",
          cLedger_total(6) == 1771440 and cLedger_total(8) == 475308288)


# ------------------------------------------- V2/V3/V4 -- band scans (B = 6)

def band_scans(cert=None):
    B = 6
    M = closed_M(B)
    fmax = fmax_of(B)
    for base in (3, 5):
        c, P, hf = hatf_scan(B, base)
        costab = [cos(2 * pi * r / c) for r in range(c)]
        check(f"V2 Parseval guard sum hatf^2 == c*M2 to 1e-6 rel (B=6, base {base})",
              abs(sum(x * x for x in hf) - c * closed_M2(B))
              <= 1e-6 * c * closed_M2(B))
        cls = brute_classes(B, base)
        fib = defaultdict(int)
        for v, d in cls.items():
            for sig, n in d.items():
                fib[sig] += n
        image = sorted(fib)
        bands = band_battery(c, hf, M)
        ok_budget, ok_omega, ok_chain, ok_proj = True, True, True, True
        ok_ident, ok_odd, ok_cpars, maxdev = True, True, True, 0.0
        ok_flat = True
        for name, Ab in bands.items():
            hv = h_table(Ab, c, hf, costab, image)
            l2h = sqrt(sum(hf[xi] ** 2 for xi in Ab) / c)   # FULL Z_c norm
            if l2h <= 0:
                ok_omega = False
                continue
            inner = sum(fib[s] * hv[s] for s in image)      # <f, h_A>
            if abs(inner - l2h ** 2) > 1e-6 * l2h ** 2:
                ok_proj = False
            omega_plus = sum(fib[s] * max(0.0, hv[s]) for s in image) / l2h
            budget = sum((fib[s] * max(0.0, hv[s])) ** 2
                         for s in image) / l2h ** 2
            if budget > fmax * fmax * (1 + 1e-9):
                ok_budget = False
            if omega_plus < l2h * (1 - 1e-9):
                ok_omega = False
            kmin = omega_plus ** 2 / budget
            if kmin < (l2h ** 2 / fmax ** 2) * (1 - 1e-9):
                ok_chain = False
            if cert is not None and base == 3:
                cert["bands_base3"][name] = {
                    "size": len(Ab), "K_min": round(kmin, 2),
                    "budget_over_fmax2": round(budget / fmax ** 2, 4),
                    "R_A_full": round(sqrt(closed_L(B)) * l2h / M, 4)}
            narrow = len(Ab) <= 200
            for v in cls:
                s = sum(v)
                if s < 2:
                    continue
                U = [i for i in range(B) if v[i]]
                sigs = {}
                for bits in range(2 ** s):
                    eps = [1 if (bits >> t) & 1 == 0 else -1
                           for t in range(s)]
                    sigs[bits] = sum(e * P[U[t]]
                                     for t, e in enumerate(eps)) % c
                cube = {bits: hv[sig] for bits, sig in sigs.items()}
                coeffs = {dbits: cube_coeff(cube, dbits, s)
                          for dbits in range(2 ** s)}
                if abs(sum(x * x for x in coeffs.values())
                       - sum(x * x for x in cube.values()) / 2 ** s) \
                        > 1e-8 * M * M:
                    ok_cpars = False
                for dbits, br in coeffs.items():
                    if bin(dbits).count("1") % 2 == 1 and abs(br) > 1e-10 * M:
                        ok_odd = False
                    if narrow:
                        acc = complex(0.0)
                        for xi in Ab:
                            prod = complex(1.0)
                            for t in range(s):
                                th = 2 * pi * ((xi * P[U[t]]) % c) / c
                                prod *= ((-1j * sin(th))
                                         if (dbits >> t) & 1 else cos(th))
                            acc += hf[xi] * prod
                        acc /= c
                        dev = abs(acc - br)
                        maxdev = max(maxdev, dev)
                        if dev > 1e-8 * M:
                            ok_ident = False
                if name == "maximal":
                    l1 = sum(abs(x) for x in cube.values())
                    if abs(2 ** s * abs(coeffs[0]) - l1) > 1e-6 * M:
                        ok_flat = False
        check(f"V2 projection identity <f,h_A> == ||h_A||_2^2 (full norm, spectral) on every band (B=6, base {base})", ok_proj)
        check(f"V2 ell^2 budget <= f_max^2 on every band (B=6, base {base})", ok_budget)
        check(f"V2 Omega_+ >= ||h_A||_2 (full norm) on every band (B=6, base {base})", ok_omega)
        check(f"V2 T1 chain K_min >= ||h||^2/f_max^2 (full norm) on every band (B=6, base {base})", ok_chain)
        check(f"V3 T2 certificate identity, all narrow bands x classes x patterns (B=6, base {base})", ok_ident)
        check(f"V3 odd-|D| cube coefficients vanish (eps -> -eps symmetry), all scanned (B=6, base {base})", ok_odd)
        check(f"V4 cube-Parseval sum_D hcube^2 == 2^-s sum h^2, all scanned classes (B=6, base {base})", ok_cpars)
        check(f"V4 maximal-band flat specialization: D=0 floor == cube ell^1 (B=6, base {base})", ok_flat)
        if cert is not None:
            cert["identity_maxdev"][f"base{base}"] = f"{maxdev:.2e}"


# ------------------------------------------------- V5 -- cross-consistency

def v5_cross():
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
    check("V5 brute class/fiber grid == closed forms (B in {4,6}, both bases)", ok_prof)
    check("V5 cross-class syndrome disjointness (B in {4,6}, both bases)", ok_disj)
    c, _P, hf = hatf_scan(6, 3)
    M = closed_M(6)
    check("V5 base-3 shell census rho=1/10 == 42 (resonant-folding pin)",
          sum(1 for j in range(1, c) if abs(hf[j]) * 10 >= M) == 42)
    check("V5 M2 pins (3584 / 97444)",
          closed_M2(6) == 3584 and closed_M2(8) == 97444)


# ----------------------------------------------------------------- driver

def run_all(quiet=False, cert=None):
    global QUIET, CHECKS
    QUIET = quiet
    CHECKS = []
    if cert is not None:
        cert.update({"bands_base3": {}, "identity_maxdev": {}})
    v1_integers()
    band_scans(cert)
    v5_cross()
    bad = [n for n, ok in CHECKS if not ok]
    if not quiet:
        print(f"RESULT: {'PASS' if not bad else 'FAIL'} "
              f"({len(CHECKS) - len(bad)}/{len(CHECKS)})")
    return not bad


def tamper_selftest():
    """Mutate five load-bearing pieces; each must flip PASS -> FAIL."""
    me = sys.modules[__name__]
    caught = 0
    orig_f = me.fmax_of
    me.fmax_of = lambda B: max(1, orig_f(B) // 2)
    if not run_all(quiet=True):
        caught += 1
    me.fmax_of = orig_f
    orig_h = me.hatf_scan
    def bad_hatf(B, base):
        c, P, vals = orig_h(B, base)
        return c, P, [v * 1.001 for v in vals]
    me.hatf_scan = bad_hatf
    if not run_all(quiet=True):
        caught += 1
    me.hatf_scan = orig_h
    orig_t = me.h_table
    me.h_table = lambda Ab, c, hf, ct, im: {
        s: v * 2 for s, v in orig_t(Ab, c, hf, ct, im).items()}
    if not run_all(quiet=True):
        caught += 1
    me.h_table = orig_t
    orig_l = me.cLedger_total
    me.cLedger_total = lambda B: orig_l(B) + 1
    if not run_all(quiet=True):
        caught += 1
    me.cLedger_total = orig_l
    orig_w = me.fiber_w
    me.fiber_w = lambda B, s: orig_w(B, s) + (1 if s == B else 0)
    if not run_all(quiet=True):
        caught += 1
    me.fiber_w = orig_w
    orig_cc = me.cube_coeff
    me.cube_coeff = lambda cube, dbits, s: sum(
        ((-1) ** bin(bits & dbits).count("1")) * v
        for bits, v in cube.items())          # normalization dropped
    if not run_all(quiet=True):
        caught += 1
    me.cube_coeff = orig_cc
    print(f"tamper-selftest: caught {caught}/6")
    ok = run_all()
    return caught == 6 and ok


def emit_certificate(path):
    import json
    cert = {}
    ok = run_all(quiet=True, cert=cert)
    cert["all_checks_pass"] = ok
    cert["n_checks"] = len(CHECKS)
    cert["float_note"] = ("band scans (V2-V4) use floats under the exact "
                          "Parseval guard; V1/V5 are exact integers")
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
