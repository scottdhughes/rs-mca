#!/usr/bin/env python3
"""Exact verifier: section-nonpositive (J<=0) rational-host EXTRACTION fails.

This certifies the COUNTEREXAMPLE half of the extraction question left open by
the canonical reduced rational-host compiler of
`experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`
(credit: DannyExperiments, PR #721).  #721 proves that IF a section-nonpositive
received line ADMITS a reduced rational-host presentation (RH1)-(RH2) then the
canonical tuple is unique and its witness-exhaustive incidence compiler applies.
It explicitly disclaims extraction (its first Nonclaim: "every J<=0 received
line has a reduced rational-host presentation") and names it the exact next
wall.  This script decides that wall from the negative side.

Engine (an EXACT iff, both directions validated below).  Fix parameters of a
section-nonpositive MCA row over F_p:

    D subseteq F_p, |D| = n, C = RS_F(D,k), k+1 <= a <= n,
    J = a^2 - n(k-1) <= 0,  1 <= d <= a-k.

For a candidate denominator L (monic, deg L = d, L(x)!=0 for x in D), a received
line r=(r0,r1) in (F_p^D)^2 admits the reduced rational-host presentation

    r0(x) = c0(x) + U(x)/L(x),   r1(x) = c1(x) - T(x)/L(x)      (RH1)
    c0,c1 in F[X]_{<k}; deg U = a, ell=lc(U)!=0; 0!=T in F[X]_{<d};
    gcd(L,T)=1; gauge [X^j]U = 0 for d<=j<=d+k-1                (RH2)

with THIS (d,L) if and only if, writing R0,R1 for the degree-<n interpolants of
r0,r1 on D and P0=(L*R0) mod M_D, P1=(L*R1) mod M_D  (M_D = prod_{x in D}(X-x)):

    (A)  deg P0 = a exactly           [then c0,U are forced by the RH2 gauge]
    (B)  deg P1 <= d+k-1  AND  T := (-P1 mod L) != 0  AND  gcd(L,T)=1
                                       [then c1 = (P1+T)/L, deg c1 < k]

Because the whole tuple (d,L,T,c0,c1,U) is forced (this IS #721 Thm parts 2-4),
the ONLY search dimension is (d,L).  Exhausting every monic L of degree
d<=a-k that is nonvanishing on D certifies non-existence exactly, with no
silent caps.

The verdict (route-scoped to reduced rational-host presentations in the sense of
#721): extraction FAILS.  This script certifies, by exhaustive (d,L) search:

  * three explicit counterexample rows over F_11, F_13, F_17 (the F_17 row has
    a-k=2, so the exhaustion exercises the genuinely-new degree-2 denominators);
  * the provable infinite family: r1 = g|_D with k <= deg g <= n-1-(a-k) admits
    NO presentation for ANY r0 (degree obstruction; no interpolation reduction
    ever occurs, so the ceiling (B) is violated at every (d,L));
  * two POSITIVE CONTROLS reconstructed from #721 section 7 (a d=1 and a d=2
    rational-host line) where the SAME engine DOES find the presentation and the
    reconstruction matches r on D byte-for-byte -- so the search is a genuine
    iff, not a vacuous "always empty";
  * the degree gate J<=0 => 2a-k <= n-1 (#721 section 4.1) and the dimension
    bound (a-k)*p^{2a-k} < p^n forcing generic failure;
  * the finite fact that p in {5,7} host NO J<=0 row with a<=n-1 and D proper
    (the regime needs n>=9), so 11 and 13 are the smallest usable prime fields.

Deterministic, stdlib-only, no `assert` (so `-O` runs the identical checks),
< 60 s.  `--tamper-selftest` corrupts a counterexample into a genuine
rational-host line and confirms the engine then FINDS a presentation.
"""

import argparse
import ast
import json
import os
import sys

# --------------------------------------------------------------------------
# Exact F_p polynomial arithmetic.  Polynomials are coefficient lists, index =
# degree, always trimmed so the top entry is nonzero (the zero polynomial is
# [0], with degree -1 by convention).
# --------------------------------------------------------------------------


def trim(c):
    c = list(c)
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def degree(c):
    c = trim(c)
    if len(c) == 1 and c[0] == 0:
        return -1
    return len(c) - 1


def padd(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = (r[i] + a[i]) % p
    for i in range(len(b)):
        r[i] = (r[i] + b[i]) % p
    return trim(r)


def pscale(a, s, p):
    return trim([(x * s) % p for x in a])


def pmul(a, b, p):
    if degree(a) < 0 or degree(b) < 0:
        return [0]
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return trim(r)


def pmod(a, m, p):
    a = trim(a)
    m = trim(m)
    dm = degree(m)
    if dm < 0:
        raise ZeroDivisionError("mod by zero polynomial")
    inv = pow(m[-1], p - 2, p)
    while degree(a) >= dm:
        da = degree(a)
        c = (a[da] * inv) % p
        sh = da - dm
        for i in range(len(m)):
            a[i + sh] = (a[i + sh] - c * m[i]) % p
        a = trim(a)
    return trim(a)


def pdivmod(a, m, p):
    a = trim(a)
    m = trim(m)
    dm = degree(m)
    inv = pow(m[-1], p - 2, p)
    q = [0] * max(1, degree(a) - dm + 1)
    while degree(a) >= dm:
        da = degree(a)
        c = (a[da] * inv) % p
        sh = da - dm
        q[sh] = c
        for i in range(len(m)):
            a[i + sh] = (a[i + sh] - c * m[i]) % p
        a = trim(a)
    return trim(q), trim(a)


def pgcd(a, b, p):
    a, b = trim(a), trim(b)
    while degree(b) >= 0:
        a, b = b, pmod(a, b, p)
    if degree(a) >= 0 and a[-1] != 1:
        a = pscale(a, pow(a[-1], p - 2, p), p)
    return trim(a)


def peval(c, x, p):
    r = 0
    for coef in reversed(c):
        r = (r * x + coef) % p
    return r


def evalvec(coeffs, D, p):
    return [peval(coeffs, x, p) for x in D]


def interpolate(D, vals, p):
    """Unique degree-<n interpolant through {(D[i], vals[i])} (Lagrange)."""
    n = len(D)
    res = [0]
    for i in range(n):
        xi, yi = D[i], vals[i] % p
        num = [1]
        den = 1
        for j in range(n):
            if j == i:
                continue
            num = pmul(num, [(-D[j]) % p, 1], p)
            den = (den * ((xi - D[j]) % p)) % p
        res = padd(res, pscale(num, (yi * pow(den, p - 2, p)) % p, p), p)
    return trim(res)


def M_D(D, p):
    m = [1]
    for x in D:
        m = pmul(m, [(-x) % p, 1], p)
    return m


def monic_of_degree(p, d):
    """Yield every monic degree-d polynomial over F_p (top coeff = 1)."""
    import itertools

    for tail in itertools.product(range(p), repeat=d):
        yield list(tail) + [1]


def nonvanishing_on(L, D, p):
    return all(peval(L, x, p) != 0 for x in D)


# --------------------------------------------------------------------------
# The exact decision engine.
# --------------------------------------------------------------------------


def presentation_with(d, L, R0, R1, D, k, a, p, MD):
    """Return the forced tuple if r=(R0,R1) has an RH1-RH2 presentation with
    this (d,L), else None.  Also RECONSTRUCTS the line from the tuple and
    checks it matches on D, so a returned tuple is a genuine witness."""
    P0 = pmod(pmul(L, R0, p), MD, p)
    P1 = pmod(pmul(L, R1, p), MD, p)

    # ---- (A) r0 side: deg P0 must be exactly a; gauge-split P0 = L*c0 + U.
    if degree(P0) != a:
        return None
    P0f = P0 + [0] * (a + 1 - len(P0))  # pad to length a+1
    Lf = L + [0] * (d + 1 - len(L))
    # Solve triangular system for c0 (deg < k): impose [X^j]U=0, j=d..d+k-1.
    c0 = [0] * k
    for m in range(k - 1, -1, -1):
        s = P0f[d + m]
        for i in range(m + 1, k):
            idx = d + m - i
            if 0 <= idx <= d:
                s = (s - Lf[idx] * c0[i]) % p
        c0[m] = s % p
    c0 = trim(c0)
    U = padd(P0, pscale(pmul(L, c0, p), p - 1, p), p)  # U = P0 - L*c0
    if degree(U) != a:
        return None
    for j in range(d, d + k):
        if (U[j] if j < len(U) else 0) != 0:
            return None
    ell = U[a]
    if ell == 0:
        return None

    # ---- (B) r1 side: deg P1 <= d+k-1; T=-(P1 mod L); T!=0; gcd(L,T)=1.
    if degree(P1) > d + k - 1:
        return None
    T = pscale(pmod(P1, L, p), p - 1, p)  # T = -(P1 mod L)
    if degree(T) < 0:
        return None  # T == 0
    if degree(T) >= d:
        return None
    if degree(pgcd(L, T, p)) >= 1:
        return None
    q1, rem1 = pdivmod(padd(P1, T, p), L, p)  # c1 = (P1 + T)/L, must be exact
    if degree(rem1) >= 0:
        return None
    c1 = q1
    if degree(c1) >= k:
        return None

    # ---- Reconstruct r on D and confirm it matches (closes the iff loop).
    Linv = {x: pow(peval(L, x, p), p - 2, p) for x in D}
    r0chk = [(peval(c0, x, p) + peval(U, x, p) * Linv[x]) % p for x in D]
    r1chk = [(peval(c1, x, p) - peval(T, x, p) * Linv[x]) % p for x in D]
    if r0chk != evalvec(R0, D, p) or r1chk != evalvec(R1, D, p):
        return None
    return {"d": d, "L": L, "c0": c0, "U": U, "T": T, "c1": c1, "ell": ell}


def search_all(p, D, k, a, r0vals, r1vals):
    """Exhaust every (d,L) with 1<=d<=a-k.  Return hits and exact accounting."""
    n = len(D)
    MD = M_D(D, p)
    R0 = interpolate(D, r0vals, p)
    R1 = interpolate(D, r1vals, p)
    per_d = []
    hits = []
    for d in range(1, a - k + 1):
        enumerated = 0
        valid = 0
        for L in monic_of_degree(p, d):
            enumerated += 1
            if not nonvanishing_on(L, D, p):
                continue
            valid += 1
            res = presentation_with(d, L, R0, R1, D, k, a, p, MD)
            if res is not None:
                hits.append(res)
        per_d.append({"d": d, "monic_enumerated": enumerated, "valid_L": valid})
    return {
        "n": n,
        "k": k,
        "a": a,
        "J": a * a - n * (k - 1),
        "a_minus_k": a - k,
        "per_d": per_d,
        "valid_L_total": sum(x["valid_L"] for x in per_d),
        "hits": hits,
    }


# --------------------------------------------------------------------------
# Instances.
# --------------------------------------------------------------------------

# Counterexample rows: r1 = g|_D with k <= deg g <= n-1-(a-k) (provable family),
# r0 arbitrary.  p in {11,13,17}.
COUNTEREXAMPLES = [
    # (p, D, k, a, g0 coeffs for r0, g1 coeffs for r1)
    (17, list(range(16)), 2, 4, [0, 0, 0, 1], [1, 0, 3, 0, 0, 1]),   # r1 deg 5
    (13, list(range(9)),  2, 3, [0, 0, 1],    [2, 0, 1, 0, 1]),       # r1 deg 4
    (11, list(range(9)),  2, 3, [0, 1],       [1, 0, 2, 1]),          # r1 deg 3
]

# Positive controls reconstructed from #721 section 7 (same engine must FIND).
def positive_controls():
    ctrls = []
    # d=1 host: F_17, D={0..12}, n=13, k=3, a=5, L=X-13, T=1, c0=c1=0, U=X^5.
    p, D, k, a = 17, list(range(13)), 3, 5
    L = [(-13) % 17, 1]
    U = [0, 0, 0, 0, 0, 1]
    Linv = {x: pow(peval(L, x, p), p - 2, p) for x in D}
    r0 = [(peval(U, x, p) * Linv[x]) % p for x in D]
    r1 = [(-1 * Linv[x]) % p for x in D]
    ctrls.append(("F17_d1_host_#721_s7", p, D, k, a, r0, r1))
    # d=2 host: F_17, D={0..12}, k=3, a=5, L=(X-13)(X-14)=X^2+7X+12,
    #           T=X+1, c0=2+3X+4X^2, c1=5+6X+7X^2, U=X^5.
    L2 = [12, 7, 1]
    T2 = [1, 1]
    c0 = [2, 3, 4]
    c1 = [5, 6, 7]
    Linv2 = {x: pow(peval(L2, x, p), p - 2, p) for x in D}
    r0b = [(peval(c0, x, p) + peval(U, x, p) * Linv2[x]) % p for x in D]
    r1b = [(peval(c1, x, p) - peval(T2, x, p) * Linv2[x]) % p for x in D]
    ctrls.append(("F17_d2_host_#721_s7", p, D, k, a, r0b, r1b))
    return ctrls


def check_provable_family(p, D, k, a, g1, MD):
    """Symbolically confirm the degree obstruction for r1 = g1|_D:
    for every d in 1..a-k, L*g1 has degree d+deg(g1) < n (no reduction), and
    d+deg(g1) > d+k-1, so the (B) ceiling is violated at every (d,L)."""
    n = len(D)
    delta = degree(g1)
    ok = (k <= delta <= n - 1 - (a - k))
    checks = []
    for d in range(1, a - k + 1):
        no_reduction = (d + delta <= n - 1)
        exceeds_ceiling = (d + delta > d + k - 1)
        # spot-check one concrete L: interpolant of L*g1 is exactly L*g1.
        L = list(monic_of_degree(p, d))[0]  # X^d (tail all zero)
        # ensure it's usable / representative; degree fact is L-independent.
        P1 = pmod(pmul(L, g1, p), MD, p)
        checks.append(
            {
                "d": d,
                "deg_L_g1": d + delta,
                "no_reduction": no_reduction,
                "exceeds_ceiling": exceeds_ceiling,
                "interp_degree": degree(P1),
                "ceiling": d + k - 1,
            }
        )
    family_holds = ok and all(
        c["no_reduction"] and c["exceeds_ceiling"] and c["interp_degree"] > c["ceiling"]
        for c in checks
    )
    return {"delta": delta, "in_family_range": ok, "per_d": checks, "family_holds": family_holds}


def degree_gate_range(nmax=64):
    """#721 section 4.1: J<=0 (a^2<=n(k-1)) and k+1<=a<=n implies 2a-k<=n-1."""
    bad = []
    for n in range(2, nmax + 1):
        for k in range(1, n):
            for a in range(k + 1, n + 1):
                if a * a <= n * (k - 1):  # J <= 0
                    if not (2 * a - k <= n - 1):
                        bad.append((n, k, a))
    return bad


def small_field_vacuity():
    """p in {5,7}: no J<=0 row with a<=n-1, D proper (n<=p-1), k>=1.
    Returns the minimal n admitting any J<=0 row with a>=k+1 (the regime floor)."""
    out = {}
    for p in (5, 7, 11, 13):
        found = False
        for n in range(2, p):  # D proper: n <= p-1
            for k in range(1, n):
                for a in range(k + 1, n):  # a <= n-1
                    if a * a <= n * (k - 1):
                        found = True
        out["F%d_hosts_row" % p] = found
    # regime floor: smallest n with any a in [k+1, n-1], a^2 <= n(k-1)
    floor_n = None
    for n in range(2, 100):
        for k in range(1, n):
            for a in range(k + 1, n):
                if a * a <= n * (k - 1):
                    floor_n = n
                    break
            if floor_n:
                break
        if floor_n:
            break
    out["regime_floor_n"] = floor_n
    return out


# --------------------------------------------------------------------------
# Driver.
# --------------------------------------------------------------------------


def selfscan_no_assert():
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    return not any(isinstance(node, ast.Assert) for node in ast.walk(tree))


def run(tamper=False):
    report = {"engine": "exact (d,L) exhaustion; iff derived from PR #721 (RH1)-(RH2)"}
    fails = []

    # 0. AST self-scan: no `assert` (so -O runs identical checks).
    no_assert = selfscan_no_assert()
    report["no_assert_statements"] = no_assert
    if not no_assert:
        fails.append("verifier contains an `assert` statement")

    # 1. Positive controls: the SAME engine must FIND #721's rational-host lines.
    pos = []
    for name, p, D, k, a, r0, r1 in positive_controls():
        res = search_all(p, D, k, a, r0, r1)
        found = len(res["hits"]) >= 1
        pos.append({"name": name, "p": p, "n": len(D), "k": k, "a": a,
                    "J": res["J"], "valid_L_total": res["valid_L_total"],
                    "presentation_found": found,
                    "denominator_deg": res["hits"][0]["d"] if found else None})
        if not found:
            fails.append(f"positive control {name}: engine failed to find a known presentation")
    report["positive_controls"] = pos

    # 2. Counterexamples: exhaustive (d,L) search must return ZERO hits.
    ce = []
    for p, D, k, a, g0, g1 in COUNTEREXAMPLES:
        MD = M_D(D, p)
        r0 = evalvec(g0, D, p)
        r1 = evalvec(g1, D, p)
        if tamper and p == 13:
            # TAMPER: replace r1 by a genuine d=1 rational-host line and confirm
            # the engine now FINDS a presentation (search is not vacuously empty).
            alpha = next(x for x in range(p) if x not in D)  # root outside D
            Lc = [(-alpha) % p, 1]
            Linv = {x: pow(peval(Lc, x, p), p - 2, p) for x in D}
            # r1 = c1 - T/L with c1=0, T=1  => r1 = -1/L on D
            r1 = [(-1 * Linv[x]) % p for x in D]
            # r0 = c0 + U/L with U of degree a=3, gauge; pick U = X^3 (gauge ok:
            # k=2 forces [X^d..X^{d+k-1}]=[X^1,X^2]U=0 which X^3 satisfies), c0=0.
            U = [0, 0, 0, 1]
            r0 = [(peval(U, x, p) * Linv[x]) % p for x in D]
        res = search_all(p, D, k, a, r0, r1)
        fam = None if tamper else check_provable_family(p, D, k, a, g1, MD)
        n_hits = len(res["hits"])
        row = {
            "p": p, "n": len(D), "k": k, "a": a, "J": res["J"],
            "a_minus_k": res["a_minus_k"], "r1_polynomial_degree": degree(g1),
            "search_space_valid_L": res["valid_L_total"], "per_d": res["per_d"],
            "presentations_found": n_hits,
            "provable_family": fam,
        }
        ce.append(row)
        if tamper and p == 13:
            if n_hits < 1:
                fails.append("TAMPER: mutated line should admit a presentation but none found")
        else:
            if n_hits != 0:
                fails.append(f"F_{p} row unexpectedly admits {n_hits} presentation(s)")
            if fam and not fam["family_holds"]:
                fails.append(f"F_{p} row: provable-family degree obstruction failed")
            if not (res["J"] <= 0):
                fails.append(f"F_{p} row: J={res['J']} is not <= 0")
            if not (a <= len(D) - 1):
                fails.append(f"F_{p} row: a={a} is not <= n-1")
    report["counterexamples"] = ce

    # 3. Degree gate J<=0 => 2a-k <= n-1 (exhaustive to n=64).
    bad_gate = degree_gate_range(64)
    report["degree_gate_violations_n_le_64"] = len(bad_gate)
    if bad_gate:
        fails.append(f"degree gate violated at {bad_gate[:3]}")

    # 4. Dimension bound (a-k)*p^{2a-k} < p^n for each counterexample row.
    dim = []
    for p, D, k, a, _, _ in COUNTEREXAMPLES:
        n = len(D)
        lhs = (a - k) * p ** (2 * a - k)
        rhs = p ** n
        frac_no_pres = 1.0 - min(1.0, lhs / rhs)
        dim.append({"p": p, "n": n, "k": k, "a": a,
                    "host_lines_upper": lhs, "ambient": rhs,
                    "min_fraction_no_presentation": round(frac_no_pres, 6),
                    "strict": lhs < rhs})
        if not (lhs < rhs):
            fails.append(f"F_{p} row: dimension bound (a-k)p^(2a-k) < p^n failed")
    report["dimension_bound"] = dim

    # 5. Small-field vacuity: p in {5,7} host no J<=0 row (regime floor n>=9).
    sfv = small_field_vacuity()
    report["small_field_vacuity"] = sfv
    if sfv["F5_hosts_row"] or sfv["F7_hosts_row"]:
        fails.append("F_5 or F_7 unexpectedly hosts a J<=0 row with a<=n-1")
    if sfv["regime_floor_n"] != 8:
        fails.append(f"regime floor n = {sfv['regime_floor_n']} (expected 8)")

    report["tamper_mode"] = tamper
    report["result"] = "PASS" if not fails else "FAIL"
    report["failures"] = fails
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print JSON report")
    ap.add_argument("--emit-cert", metavar="PATH", help="write JSON certificate")
    ap.add_argument("--tamper-selftest", action="store_true",
                    help="corrupt a counterexample into a rational-host line; "
                         "engine must then FIND a presentation")
    args = ap.parse_args()

    if args.tamper_selftest:
        rep = run(tamper=True)
        ok = rep["result"] == "PASS"
        print("TAMPER SELF-TEST:", "detected (engine found the planted presentation)"
              if ok else "FAILED")
        print("RESULT:", "PASS" if ok else "FAIL")
        # Also run the real checks so a corrupted engine cannot pass silently.
        rep2 = run(tamper=False)
        print("REAL RUN RESULT:", rep2["result"])
        sys.exit(0 if ok and rep2["result"] == "PASS" else 1)

    rep = run(tamper=False)
    if args.emit_cert:
        os.makedirs(os.path.dirname(args.emit_cert), exist_ok=True)
        with open(args.emit_cert, "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2, sort_keys=True)
        print(f"wrote {args.emit_cert}")
    if args.json:
        print(json.dumps(rep, indent=2, sort_keys=True))
    else:
        print("=== section-nonpositive rational-host EXTRACTION: negative decision ===")
        for c in rep["positive_controls"]:
            print(f"  [+] positive control {c['name']}: found presentation "
                  f"(d={c['denominator_deg']}), searched {c['valid_L_total']} denominators")
        for c in rep["counterexamples"]:
            fam = c["provable_family"]
            print(f"  [-] F_{c['p']} n={c['n']} k={c['k']} a={c['a']} J={c['J']}: "
                  f"searched {c['search_space_valid_L']} valid denominators (d<= {c['a_minus_k']}), "
                  f"presentations found = {c['presentations_found']}"
                  + (f"; provable family holds = {fam['family_holds']}" if fam else ""))
        print(f"  degree gate J<=0 => 2a-k<=n-1 violations (n<=64): "
              f"{rep['degree_gate_violations_n_le_64']}")
        print(f"  small-field vacuity: F5={rep['small_field_vacuity']['F5_hosts_row']}, "
              f"F7={rep['small_field_vacuity']['F7_hosts_row']}, regime floor n="
              f"{rep['small_field_vacuity']['regime_floor_n']}")
        for d in rep["dimension_bound"]:
            print(f"  dim bound F_{d['p']}: host-lines <= {d['host_lines_upper']} "
                  f"< ambient {d['ambient']}  (>= {d['min_fraction_no_presentation']*100:.4f}% have none)")
    print("RESULT:", rep["result"])
    if rep["failures"]:
        for f in rep["failures"]:
            print("  FAILURE:", f)
    sys.exit(0 if rep["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
