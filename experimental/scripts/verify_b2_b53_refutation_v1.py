#!/usr/bin/env python3
"""
Self-contained (stdlib only), deterministic verifier for the packet
"The full-rank target |H_d(v)| <= p^{n/2+2} of PR #662 is false by exact computation at reachable rows".

Checks, all exact integer / rational arithmetic:
  A1. q=1 Littlewood-Offord sign-count |Q_1(0)|/p^3 > 1 at a deployment-matched row (no CHG machinery).
  A2. q=1 COMPONENT grows over finite rows of the deployed ray (p-1)/n ~ 1016 (single stratum, NOT full B53).
  B.  Bridge law + order-two identity at a small row via an INDEPENDENT full-rank oracle (own det/solve mod p)
      and a subset-sum fiber DP:  A_d(v) = p^c*dev(v)*(1+O(1/p))  and  sigma^2 = p^{-w-2c} sum_v |A_d(v)|^2 *(1+O(1/p)).
  C.  (97,96,2,3) cross-validation: DP predicts A_d(0)=p^c*dev(0); stated GPU value agrees to 1+O(1/p).
  D.  HEADLINE (97,32,2,3): asserts |A_d(0)|/p^{c/2+2} = 89.19 (>1 => B53 refuted), cross-checked vs the DP prediction;
      the tamper-selftest mutates THIS headline witness.

Run: python3 verify_b2_b53_refutation_v1.py --check
     python3 verify_b2_b53_refutation_v1.py --tamper-selftest
"""
import sys, argparse
from fractions import Fraction

def modinv(a, p): return pow(a % p, p - 2, p)
def legendre(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def primitive_root(p):
    for g in range(2, p):
        seen = set(); x = 1
        for _ in range(p - 1):
            x = x * g % p; seen.add(x)
        if len(seen) == p - 1: return g
def order_n_root(p, n):
    return pow(primitive_root(p), (p - 1) // n, p)

# ---------- A. q=1 Littlewood-Offord sign-count (WLS-false witness), pure stdlib ----------
def q1_ratio(p, n):
    """|Q_1(0)|/p^3 for w=1,c=2 via exact integer sign-count over Z/p (63.. two-shift convolutions)."""
    z = order_n_root(p, n)
    assert pow(z, n, p) == 1 and pow(z, n // 2, p) != 1
    inv = lambda a: pow(a, p - 2, p)
    cs = [(pow(z, j, p) - 1) * inv(n // 2) % p for j in range(1, n)]   # c_{Z,a}, T = mu_n \ {1}
    A = [0] * p; A[0] = 1
    for cj in cs:
        B = [0] * p
        for r in range(p):
            a = A[r]
            if a:
                B[(r + cj) % p] += a; B[(r - cj) % p] += a
        A = B
    assert sum(A) == 2 ** (n - 1)
    t = n - 1; r_main = (-8 * inv(n)) % p
    Dm = Fraction(p * A[r_main] - 2 ** t, p); Dz = Fraction(p * A[0] - 2 ** t, p)
    Q1 = n * (p * Dm + Fraction(1, 2) * Dz)
    return abs(Q1) / Fraction(p ** 3), Q1

# ---------- B. independent full-rank CHG oracle (own arithmetic) ----------
def det_solve_modp(A, b, p):
    """return (det, x) with A x = b mod p, via fraction-free-ish Gaussian elim; det=0 -> (0,None)."""
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]; det = 1
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % p), None)
        if piv is None: return 0, None
        if piv != c: M[c], M[piv] = M[piv], M[c]; det = (-det) % p
        det = det * M[c][c] % p; invp = modinv(M[c][c], p)
        M[c] = [(x * invp) % p for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]; M[r] = [(M[r][k] - f * M[c][k]) % p for k in range(n + 1)]
    return det, [M[i][n] % p for i in range(n)]

def Td_oracle(p, n, w, m):
    """Exact T_d(v)=U(v)-mean for all v in F_p^w, full-rank CHG aggregate. Returns dict v->int."""
    d = n - w - 1; ninv = modinv(n, p); inv4 = modinv(4, p)
    z = order_n_root(p, n); H = [pow(z, k, p) for k in range(n)]; Hinv = [modinv(a, p) for a in H]
    g2 = legendre(-1, p) * p                 # g^2 = chi(-1) p
    gd = (g2 ** (d // 2)) if d % 2 == 0 else None
    assert d % 2 == 0, "this stdlib oracle handles even d (rational T_d); use even-d rows"
    import itertools
    Us = {}
    for v in itertools.product(range(p), repeat=w):
        hv = [(2 * (ninv * ((m + sum(v[j - 1] * pow(Hinv[k], j, p) for j in range(1, w + 1))) % p) % p) - 1) % p for k in range(n)]
        counts = [0] * p                     # histogram of chi * zeta^phase
        for lam in itertools.product(range(p), repeat=n):
            Ms = [sum(lam[k] * pow(H[k], s, p) for k in range(n)) % p for s in range(0, 2 * d + 1)]
            Amat = [[Ms[(i + 1) + (j + 1)] for j in range(d)] for i in range(d)]
            ell = [sum(lam[k] * pow(H[k], i + 1, p) * hv[k] for k in range(n)) % p for i in range(d)]
            det, x = det_solve_modp(Amat, ell, p)
            if det == 0: continue
            quad = sum(ell[i] * x[i] for i in range(d)) % p
            gam = (sum(lam[k] * hv[k] * hv[k] for k in range(n)) - sum(lam[k] for k in range(n))) % p
            phase = ((gam - quad) * inv4) % p
            counts[phase] += legendre(det, p)
        # U(v) = gd * sum_k counts[k] zeta_p^k ; reduce mod Phi_p (must be rational at these rows)
        base = counts[p - 1]
        assert all(counts[k] == base for k in range(1, p - 1)), "oracle U(v) not rational (unexpected)"
        Us[v] = gd * (counts[0] - base)
    mean = Fraction(sum(Us.values()), p ** w)
    return {v: Us[v] - mean for v in Us}, d

def fiber_counts(p, n, w, m):
    """N(v) = #{S subset mu_n, |S|=m, power-sums_j = v_j} via subset-sum DP. dict v->int."""
    import itertools
    z = order_n_root(p, n); H = [pow(z, k, p) for k in range(n)]
    pows = [tuple(pow(a, j, p) for j in range(1, w + 1)) for a in H]
    dp = {0: {tuple([0] * w): 1}}
    for pw in pows:
        for k in range(min(m, n), 0, -1):
            prev = dp.get(k - 1);
            if not prev: continue
            cur = dp.setdefault(k, {})
            for s, ct in prev.items():
                key = tuple((s[j] + pw[j]) % p for j in range(w))
                cur[key] = cur.get(key, 0) + ct
    return dp.get(m, {})

# ---------- checks ----------
def run_checks(verbose=True):
    ok = True
    def say(s):
        if verbose: print(s)
    # A1: q=1 counterexample
    r, Q1 = q1_ratio(65089, 64)
    a1 = (abs(float(r) - 2.16693644) < 1e-6) and (r > 1)
    say(f"[A1] q=1 (65089,64): |Q1(0)|/p^3 = {float(r):.8f} > 1  Q1={Q1}   {'PASS' if a1 else 'FAIL'}")
    ok &= a1
    # A2: q=1 COMPONENT grows steeply along the deployment ray (finite rows; NOT the full aggregate)
    ray = [(64, 65089), (128, 130817)]
    vals = []
    for n, p in ray:
        rr, _ = q1_ratio(p, n); vals.append(float(rr))
    a2 = vals[0] > 1 and vals[1] > 1e4 and vals[1] > vals[0] * 100
    say(f"[A2] deployment-ray q=1 COMPONENT q1/p^3: n=64(p=65089)->{vals[0]:.3g}, n=128(p=130817)->{vals[1]:.3g} "
        f"(finite-row growth; component only, not full B53)   {'PASS' if a2 else 'FAIL'}")
    ok &= a2
    # B: bridge + order-two identity at (7,6,1,2)  [even d=4]
    p, n, w, m = 7, 6, 1, 1; c = w + 1
    Td, d = Td_oracle(p, n, w, m)
    N = fiber_counts(p, n, w, m); total = sum(N.values()); mean = Fraction(total, p ** w)
    Ad = {v: Fraction(Td[v], p ** d) for v in Td}
    dev = {v: Fraction(N.get(v, 0)) - mean for v in Td}
    b_oracle = (Td[(0,)] == -95256)
    worst = max(abs(float(Ad[v] / (p ** c * dev[v])) - 1) for v in Td if dev[v] != 0)
    s2_dev = Fraction(sum(dev[v] ** 2 for v in Td), p ** w)
    s2_Ad = Fraction(sum(Ad[v] ** 2 for v in Td), p ** w) / p ** (2 * c)
    bb = b_oracle and worst < 0.15 and abs(float(s2_Ad / s2_dev) - 1) < 0.15   # p=7 => O(1/p)~0.14
    say(f"[B ] (7,6,1,2): oracle T_d(0)={Td[(0,)]} (expect -95256); bridge max|ratio-1|={worst:.3f}; "
        f"sigma^2 ident ratio={float(s2_Ad/s2_dev):.3f}   {'PASS' if bb else 'FAIL'}")
    ok &= bb
    # C: (97,96,2,3) cross-validation (DP prediction vs stated GPU value)
    p, n, w, c = 97, 96, 2, 3; m = n // 2 - c
    N96 = fiber_counts(p, n, w, m); tot = sum(N96.values()); mean96 = Fraction(tot, p ** w)
    dev0 = Fraction(N96.get((0, 0), 0)) - mean96
    pred = p ** c * dev0
    gpu = Fraction(-2804335939511319360, 912673)     # stated GPU A_d(0) at (97,96,2,3)
    ratio = float(gpu / pred)
    cc = abs(ratio - 1) < 0.02
    say(f"[C ] (97,96,2,3): DP pred A_d(0)=p^c*dev0={float(pred):.4e}; stated GPU={float(gpu):.4e}; "
        f"GPU/pred={ratio:.4f} (~1+O(1/p))   {'PASS' if cc else 'FAIL'}")
    ok &= cc
    # D: the HEADLINE witness (97,32,2,3) -- assert the stated GPU A_d(0), its ratio 89.19, and the DP cross-check
    p, n, w, c = 97, 32, 2, 3; m = n // 2 - c
    N32 = fiber_counts(p, n, w, m); tot = sum(N32.values()); mean32 = Fraction(tot, p ** w)
    dev0 = Fraction(N32.get((0, 0), 0)) - mean32
    pred = p ** c * dev0
    gpu = Fraction(-731704492880832, 912673)          # stated GPU A_d(0) at (97,32,2,3) [the headline]
    tgt = Fraction(p) ** Fraction(c, 2) * p ** 2
    ratio_headline = float(abs(gpu) / tgt); cross = float(gpu / pred)
    dd = (abs(ratio_headline - 89.1906746519) < 1e-6) and (abs(cross - 1) < 0.02) and (ratio_headline > 1)
    say(f"[D ] (97,32,2,3) HEADLINE: |A_d(0)|/p^(c/2+2) = {ratio_headline:.6f} (>1 => B53 refuted); "
        f"DP cross-check GPU/pred={cross:.4f}   {'PASS' if dd else 'FAIL'}")
    ok &= dd
    return ok

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true")
    ap.add_argument("--tamper-selftest", action="store_true"); a = ap.parse_args()
    if a.tamper_selftest:
        # flip one stated GPU digit; check C must FAIL
        import re
        global Td_oracle
        print("tamper self-test: perturbing the HEADLINE (97,32) GPU value by ~14%; check D must FAIL...")
        src = open(__file__).read().replace("-731704492880832", "-831704492880832")
        ns = {}; exec(compile(src, "tampered", "exec"), ns)
        bad = ns["run_checks"](verbose=False)
        print("tamper self-test:", "PASS (tamper caught)" if not bad else "FAIL (tamper NOT caught)")
        sys.exit(0 if not bad else 1)
    if not a.check:
        print("use --check or --tamper-selftest"); sys.exit(2)
    ok = run_checks()
    print("\nTOTAL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
