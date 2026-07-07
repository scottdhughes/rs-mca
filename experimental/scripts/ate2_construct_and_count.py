#!/usr/bin/env python3
"""Construct-and-count probe for the A_te-2 deeper-pin question.

For RS[F_q, D, k] with |D|=n, a received "line" is a pair (f,g): D -> F_q, with
line words w_z = f + z*g for finite slopes z in F_q.  A slope z is a
support-wise-noncontained BAD slope at agreement A iff there is a support S,
|S|=A, with w_z|_S a codeword restriction (deg < k) while g|_S does NOT extend
to a codeword restriction (so (f,g) is not jointly a code-line on S).

LD_sw(C, A) = max over lines (f,g) of the number of bad slopes.  Tangent floor
= n-A+1 (a425 moving-root witness).  We probe whether any line beats:
  - R3+2 at A_te-1 = n-R3-1  (would refute the two-core closure -- a sanity check)
  - R3+3 at A_te-2 = n-R3-2  (would CAP the pin at A_te-1; else pin may extend)
where R3 = floor((n-k)/3).

When A > (n+k)/2 (unique-decoding radius) each w_z has at most one codeword
within radius n-A, so counting is cheap (Berlekamp-Welch per slope).
"""
from __future__ import annotations
import argparse, random
from itertools import product


def make_field(q):
    inv = [0] * q
    for a in range(1, q):
        inv[a] = pow(a, q - 2, q)
    return inv


def rs_extends(vals, xs, k, q):
    """Does the partial function {xs[i] -> vals[i]} extend to a deg<k poly?
    True iff interpolating on the first k points reproduces all points."""
    S = list(zip(xs, vals))
    if len(S) <= k:
        return True                      # <=k points always extend
    # Lagrange interpolation on first k points, then check the rest.
    pts = S[:k]
    def interp(x):
        tot = 0
        for i, (xi, yi) in enumerate(pts):
            num = yi % q
            den = 1
            for j, (xj, _) in enumerate(pts):
                if j == i:
                    continue
                num = (num * ((x - xj) % q)) % q
                den = (den * ((xi - xj) % q)) % q
            tot = (tot + num * pow(den, q - 2, q)) % q
        return tot
    return all(interp(x) == y for x, y in S[k:])


def bw_decode_agreement(w, D, k, q, A):
    """Berlekamp-Welch: return (codeword_vals over D) of the unique deg<k poly
    agreeing with w on >= A positions, or None. Requires A > (n+k)/2."""
    n = len(D)
    e = n - A                              # max errors
    # Solve for E (deg<=e, monic-ish) and N (deg < k+e): N(xi) = w_i E(xi).
    # Unknowns: E has e coeffs (E = x^e + sum_{j<e} a_j x^j) OR treat generally.
    # Use the standard homogeneous system with E deg<=e, N deg<=k+e-1, nonzero E.
    import itertools
    # Build matrix rows: for each i, sum_j E_j xi^j * (-w_i) ... arrange columns
    # E_0..E_e (e+1), N_0..N_{k+e-1} (k+e) unknowns; eqn: N(xi) - w_i E(xi) = 0.
    ncolsE = e + 1
    ncolsN = k + e
    rows = []
    for xi, wi in zip(D, w):
        row = [0] * (ncolsE + ncolsN)
        xp = 1
        for j in range(ncolsN):
            row[ncolsE + j] = xp
            xp = (xp * xi) % q
        xp = 1
        for j in range(ncolsE):
            row[j] = (-wi * xp) % q
            xp = (xp * xi) % q
        rows.append(row)
    sol = nullspace_vec(rows, q)
    if sol is None:
        return None
    Ecoe = sol[:ncolsE]
    Ncoe = sol[ncolsE:]
    if all(c == 0 for c in Ecoe):
        return None
    # codeword = N/E if E divides N; evaluate at each xi where E(xi)!=0 must match.
    cw = []
    for xi in D:
        Ev = polyval(Ecoe, xi, q)
        Nv = polyval(Ncoe, xi, q)
        if Ev == 0:
            cw.append(None)               # root of E: fill via interpolation later
        else:
            cw.append((Nv * pow(Ev, q - 2, q)) % q)
    # Reconstruct the deg<k poly from k non-None points and evaluate everywhere.
    known = [(x, c) for x, c in zip(D, cw) if c is not None]
    if len(known) < k:
        return None
    pts = known[:k]
    def interp(x):
        tot = 0
        for i, (xi, yi) in enumerate(pts):
            num = yi; den = 1
            for j, (xj, _) in enumerate(pts):
                if j == i: continue
                num = (num * ((x - xj) % q)) % q
                den = (den * ((xi - xj) % q)) % q
            tot = (tot + num * pow(den, q - 2, q)) % q
        return tot
    cwful = [interp(x) for x in D]
    agree = sum(1 for a, b in zip(cwful, w) if a == b)
    return cwful if agree >= A else None


def polyval(coe, x, q):
    v = 0
    for c in reversed(coe):
        v = (v * x + c) % q
    return v


def nullspace_vec(rows, q):
    """Return one nonzero vector in the null space of the matrix (mod q prime), or None."""
    M = [row[:] for row in rows]
    R = len(M); C = len(M[0])
    piv = []
    r = 0
    for c in range(C):
        pr = None
        for i in range(r, R):
            if M[i][c] % q != 0:
                pr = i; break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        invp = pow(M[r][c], q - 2, q)
        M[r] = [(v * invp) % q for v in M[r]]
        for i in range(R):
            if i != r and M[i][c] % q != 0:
                f = M[i][c]
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == R:
            break
    free = [c for c in range(C) if c not in piv]
    if not free:
        return None
    fc = free[0]
    x = [0] * C
    x[fc] = 1
    for i, c in enumerate(piv):
        x[c] = (-M[i][fc]) % q
    return x


def count_bad_slopes(f, g, D, k, q, A):
    n = len(D)
    bad = 0
    for z in range(q):
        w = [(f[i] + z * g[i]) % q for i in range(n)]
        cw = bw_decode_agreement(w, D, k, q, A)
        if cw is None:
            continue
        S = [i for i in range(n) if w[i] == cw[i]]     # agreement set (>=A)
        # z is bad iff g does NOT extend on some size-A subset of S; since A>=k+1
        # and non-extension is witnessed within A pts, check g on all of S.
        if not rs_extends([g[i] for i in S], [D[i] for i in S], k, q):
            bad += 1
    return bad


def a425_witness(D, k, q, A):
    """Tangent moving-root witness: zero core of size A-1, one moving outside
    coord per slope. Gives exactly n-A+1 bad slopes at agreement A."""
    n = len(D)
    core = A - 1
    f = [0] * n; g = [0] * n
    for idx in range(core, n):             # outside coords core..n-1
        lam = (idx - core) % q             # distinct labels (need n-core <= q)
        g[idx] = 1
        f[idx] = (-lam) % q
    return f, g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--trials", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    q, n, k = args.q, args.n, args.k
    assert n <= q, "need n <= q for a distinct domain"
    D = list(range(n))
    m = n - k; R3 = m // 3
    A1 = n - R3 - 1; A2 = n - R3 - 2
    uniq = (n + k) / 2
    print(f"RS[F_{q}, |D|={n}, k={k}]  m={m} R3={R3}  A_te-1={A1} A_te-2={A2}  unique-radius={uniq:.1f}")
    print(f"tangent floors: A_te-1 -> {n-A1+1}=R3+2, A_te-2 -> {n-A2+1}=R3+3")
    # baseline: a425 witness
    for label, A in [("A_te-1", A1), ("A_te-2", A2)]:
        f, g = a425_witness(D, k, q, A)
        b = count_bad_slopes(f, g, D, k, q, A)
        print(f"  a425 witness @ {label} (A={A}): {b} bad slopes  (expect tangent {n-A+1})")
    # search: random lines
    rng = random.Random(args.seed)
    best = {A1: 0, A2: 0}
    bestline = {A1: None, A2: None}
    for t in range(args.trials):
        f = [rng.randrange(q) for _ in range(n)]
        g = [rng.randrange(q) for _ in range(n)]
        for A in (A1, A2):
            b = count_bad_slopes(f, g, D, k, q, A)
            if b > best[A]:
                best[A] = b; bestline[A] = (f[:], g[:])
    print(f"  random search ({args.trials} lines):")
    print(f"    max bad @ A_te-1 = {best[A1]}   (two-core says R3+2 = {n-A1+1}; > that would REFUTE two-core)")
    print(f"    max bad @ A_te-2 = {best[A2]}   (tangent R3+3 = {n-A2+1}; > that CAPS the pin at A_te-1)")


if __name__ == "__main__":
    main()


def structured_search(q, n, k, restarts=30, steps=60, seed=11):
    """a425 witness + low-overlap construction + hill-climb; report max bad-slope
    count at A_te-1 and A_te-2 vs their tangent floors. Reproduces the note table."""
    D = list(range(n)); m = n - k; R3 = m // 3
    A1 = n - R3 - 1; A2 = n - R3 - 2
    rng = random.Random(seed)
    best = {A1: count_bad_slopes(*a425_witness(D, k, q, A1), D, k, q, A1),
            A2: count_bad_slopes(*a425_witness(D, k, q, A2), D, k, q, A2)}
    for A in (A2, A1):
        for _ in range(restarts):
            f, g = a425_witness(D, k, q, A)
            for _ in range(rng.randrange(0, 5)):            # aggressive restart perturb
                i = rng.randrange(n); f[i] = rng.randrange(q); g[i] = rng.randrange(q)
            cur = count_bad_slopes(f, g, D, k, q, A)
            for _ in range(steps):
                i = rng.randrange(n); w = rng.randrange(2); old = (f[i], g[i])
                if w == 0: f[i] = rng.randrange(q)
                else: g[i] = rng.randrange(q)
                nb = count_bad_slopes(f, g, D, k, q, A)
                if nb >= cur:
                    cur = nb; best[A] = max(best[A], nb)
                else:
                    f[i], g[i] = old
    return {"A_te-1": (best[A1], n - A1 + 1), "A_te-2": (best[A2], n - A2 + 1)}
