#!/usr/bin/env python3
"""b2 DENSE-band regime: exact count of non-coset-union w-null blocks vs n^3.

CORRECT object (CAP25 v13, `b2_step0_object_pinned.md`):
  Phi_{m,w}: (mu_n choose m) -> F_q^w,  M |-> (e_1(M), ..., e_w(M)).
  Zero-fiber = "w-null blocks" M: e_1(M)=...=e_w(M)=0
             <=> (Newton, valid when q > w) p_1(M)=...=p_w(M)=0,  p_h(M)=sum_{x in M} x^h.
  m = K + w = rho*n + w  (block size TIED to rate rho and depth w).
  Structured main term (b1) = M that are unions of subgroup cosets (translation-
  invariant index sets); "extras" = w-null M that are NOT coset-unions.
  Conjecture (deployed): #extras <= n^3  (repo 16 n^3).

REGIME (the fix): this probes the DENSE band w > w_0 (past the proved head depth),
NOT the earlier rare-event b~t toy. Dense means mean fiber C(n,m)/q^w >> 1.

Everything exact (integer MITM). Self-checks: Newton e<->p equivalence; MITM == brute
on tiny cases; q PRIME and q>w and n|(q-1) asserted. Mechanism mean|S_m(c)| is a diagnostic.

SCOPE: PRIME field F_p only. The deployed b2 fields (KoalaBear = 2^31-2^27+1, Mersenne-31
= 2^31-1) are prime, so this is the deployed setting. For prime-power F_q the Newton
condition is char(F_q)>w (not q>w) and one needs a real finite-field backend; not handled
here (Codex R1 scope note).
"""
from __future__ import annotations
import argparse, cmath, math, itertools, random
from math import comb
from collections import defaultdict


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _prime_factors(n):
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


def primroot(q):
    """Least primitive root mod prime q, via the standard order test
    (g is primitive iff g^((q-1)/p) != 1 for every prime p | q-1) -- O(w(q-1) log q),
    so it is fast even for 31-bit deployed primes (naive O(q) scan would hang)."""
    facs = _prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // p, q) != 1 for p in facs):
            return g
    raise ValueError(f"no primitive root found mod {q} (is {q} prime?)")


def mu_n(q, n):
    """The n-th roots of unity in F_q^*, as residues; requires n | q-1."""
    assert (q - 1) % n == 0, f"n={n} must divide q-1={q-1}"
    g = primroot(q)
    zeta = pow(g, (q - 1) // n, q)
    return [pow(zeta, k, q) for k in range(n)]


def power_key(idxs, pts, q, w):
    """(p_1,...,p_w) mod q for the subset {pts[k] : k in idxs}."""
    acc = [0] * w
    for k in idxs:
        x = pts[k]
        xr = x
        for h in range(w):
            acc[h] = (acc[h] + xr) % q
            xr = xr * x % q
    return tuple(acc)


# ---- Newton self-check: e_1..e_w = 0  <=>  p_1..p_w = 0  (needs q > w) ----
def newton_equiv_ok(pts, q, w, subset):
    """Check e_h==0 for h<=w iff p_h==0 for h<=w on this subset, via both routes."""
    xs = [pts[k] for k in subset]
    # power sums
    p = [sum(pow(x, h, q) for x in xs) % q for h in range(1, w + 1)]
    # elementary symmetric via product prod(X - x): coeff of X^{|xs|-h} is (-1)^h e_h
    coeff = [1]
    for x in xs:
        new = [0] * (len(coeff) + 1)
        for i, c in enumerate(coeff):
            new[i] = (new[i] + c) % q
            new[i + 1] = (new[i + 1] - c * x) % q
        coeff = new
    d = len(xs)
    e = [((-1) ** h) * coeff[h] % q for h in range(1, min(w, d) + 1)]
    e += [0] * (w - len(e))  # e_h = 0 for h > |subset|
    return (all(v == 0 for v in p[:w])) == (all(v == 0 for v in e[:w]))


# ---- exact MITM count of w-null m-subsets of mu_n ----
def count_wnull_mitm(pts, q, n, w, m):
    A, B = list(range(n // 2)), list(range(n // 2, n))
    tableB = defaultdict(int)          # (size, key) -> count
    for r in range(len(B) + 1):
        for comb_b in itertools.combinations(B, r):
            tableB[(r, power_key(comb_b, pts, q, w))] += 1
    total = 0
    for ra in range(len(A) + 1):
        rb = m - ra
        if rb < 0 or rb > len(B):
            continue
        for comb_a in itertools.combinations(A, ra):
            ka = power_key(comb_a, pts, q, w)
            need = tuple((-v) % q for v in ka)   # p_h(A-part) + p_h(B-part) == 0
            total += tableB.get((rb, need), 0)
    return total


# ---- exact structured (coset-union) w-null count: index set invariant under +s, s|n, s<n ----
def count_wnull_structured(pts, q, n, w, m):
    seen = set()
    for s in range(1, n):
        if n % s:
            continue
        reps = n // s
        # M = {p + i*s : p in P, i} for P subset of {0..s-1}; |M| = |P|*reps == m
        if m % reps:
            continue
        pcount = m // reps
        if pcount > s:
            continue
        for P in itertools.combinations(range(s), pcount):
            M = frozenset((p + i * s) % n for p in P for i in range(reps))
            if len(M) != m or M in seen:
                continue
            if all(power_key(tuple(M), pts, q, w)[h] == 0 for h in range(w)):
                seen.add(M)
    return len(seen)


# ---- brute-force ground truth (tiny n only) ----
def count_wnull_brute(pts, q, n, w, m):
    tot = 0
    for M in itertools.combinations(range(n), m):
        if all(v == 0 for v in power_key(M, pts, q, w)):
            tot += 1
    return tot


# ---- mechanism diagnostic: mean/max |S_m(c)|, S_m(c)=[z^m] prod_x(1+z e_q(sum_r c_r x^r)) ----
def mechanism(pts, q, n, w, m, sample_cap=20000):
    eq = [cmath.exp(2j * math.pi * u / q) for u in range(q)]
    PV = [[pow(x, r, q) for r in range(1, w + 1)] for x in pts]
    cs, tot, mx = 0, 0.0, 0.0
    space = q ** w
    rng = random.Random(0xB2)          # seeded uniform sample when space is too big (Codex R1)
    it = (itertools.product(range(q), repeat=w) if space <= sample_cap
          else (tuple(rng.randrange(q) for _ in range(w)) for _ in range(sample_cap)))
    for c in it:
        coeff = [0j] * (n + 1)
        coeff[0] = 1 + 0j
        for k in range(n):
            s = sum(c[r] * PV[k][r] for r in range(w)) % q
            y = eq[s]
            for i in range(n, 0, -1):
                coeff[i] += coeff[i - 1] * y
        val = abs(coeff[m])
        tot += val
        mx = max(mx, val)
        cs += 1
    return tot / cs, mx, (space <= sample_cap)


def run(q, n, rho_num, rho_den, w, do_brute, do_mech):
    assert is_prime(q), f"prime-field (F_p) scope only; q={q} not prime (Codex R1)"
    assert q > w, f"Newton requires q>w over F_p; got q={q}, w={w}"
    pts = mu_n(q, n)
    K = rho_num * n // rho_den
    m = K + w
    assert 0 < m <= n, f"m=rho*n+w={m} out of range for n={n}"
    # Newton self-check on a few subsets
    for M in [tuple(range(m)), tuple(range(0, 2 * m, 2))[:m]]:
        if max(M) < n:
            assert newton_equiv_ok(pts, q, w, M), "Newton e<->p equivalence FAILED"
    total = count_wnull_mitm(pts, q, n, w, m)
    struct = count_wnull_structured(pts, q, n, w, m)
    extras = total - struct
    n3 = n ** 3
    # log2 mean fiber = log2 C(n,m) - w log2 q  (overflow-safe; Codex R1)
    log2_fiber = ((math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1)) / math.log(2)
                  - w * math.log2(q))
    fm = 2.0 ** log2_fiber if log2_fiber < 900 else float("inf")
    row = {
        "q": q, "n": n, "rho": f"{rho_num}/{rho_den}", "K": K, "w": w, "m": m,
        "mean_fiber_C(n,m)/q^w": fm, "log2_fiber": round(log2_fiber, 3), "dense(>1)": log2_fiber > 0,
        "total_wnull": total, "structured": struct, "extras": extras,
        "n^3": n3, "extras<=n^3": extras <= n3,
    }
    if do_brute and comb(n, m) <= 3_000_000:
        b = count_wnull_brute(pts, q, n, w, m)
        row["brute_total"] = b
        row["MITM==brute"] = (b == total)
        assert b == total, f"MITM {total} != brute {b}"
    if do_mech:
        mean_s, max_s, exact = mechanism(pts, q, n, w, m)
        row["mean|S_m(c)|"] = round(mean_s, 2)
        row["max|S_m(c)|"] = round(max_s, 2)
        row["mech_exact_over_c"] = exact
        row["extras<=mean|S|(L1bound)"] = extras <= mean_s
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--q", type=int, default=97)
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--rho", default="1/2", help="rate rho = num/den")
    ap.add_argument("--w", type=int, default=3, help="prefix depth (vanishing power sums)")
    ap.add_argument("--wsweep", default=None, help="e.g. 2:6 to sweep w over [2,6]")
    ap.add_argument("--no-brute", action="store_true")
    ap.add_argument("--mech", action="store_true", help="compute mean|S_m(c)| diagnostic")
    args = ap.parse_args(argv)
    rn, rd = (int(x) for x in args.rho.split("/"))
    ws = ([args.w] if not args.wsweep
          else list(range(*(lambda a, b: (a, b + 1))(*map(int, args.wsweep.split(":"))))))
    for w in ws:
        row = run(args.q, args.n, rn, rd, w, not args.no_brute, args.mech)
        flag = "OK " if row["extras<=n^3"] else "!!!"
        chk = row.get("MITM==brute", "n/a")
        print(f"[{flag}] q={row['q']} n={row['n']} rho={row['rho']} w={w} m={row['m']}: "
              f"total={row['total_wnull']} struct={row['structured']} extras={row['extras']} "
              f"vs n^3={row['n^3']} | dense={row['dense(>1)']} (fiber={row['mean_fiber_C(n,m)/q^w']:.3g}) "
              f"| MITM==brute={chk}"
              + (f" | mean|S|={row.get('mean|S_m(c)|')}" if args.mech else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
