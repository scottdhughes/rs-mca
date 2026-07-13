#!/usr/bin/env python3
"""
verify_staircase_concentration_sidon_paired.py

Recomputes every number in
  experimental/notes/thresholds/staircase_concentration_sidon_paired.md

DECIDES the CONCENTRATION clause -- the last open clause of avdeevvadim's #716
charge-preserving semantic-or-signed dichotomy (Sec 6) on the Sidon-paired
depth-1 class -- flagged by #732 Theorem B as its residual "max-fiber /
staircase-concentration" hypothesis.

Route-scoped class (#735 Thm 2 / #732 / #728 / #717 Sec 7):
  P     a distinct-subset-sum (dissociated) set over Z, |P| = B
  c     an integer with c > 2*sum(P)      (large-c / no-wraparound regime)
  T     = P  u  (c - P),  |T| = 2B        (twin pairs {A_i, c - A_i})
  a     = B                                (balanced subset size)
  Phi   = subset sum over Z,  Phi(S) = sum_{t in S} t
  M     = C(2B, B),  L = |Phi(Omega^0)|,  fiber = Phi^{-1}(sigma)

Exact combinatorics established here (stdlib only, deterministic, exact ints):

  BLOCK A  EXACT FIBER-SIZE CLASSIFICATION (2-superincreasing / B[+-2] base).
     |Phi^{-1}(sigma)| = C(B - s, (B - s)/2),  s = #unpaired pairs of the support,
     with EXACTLY C(B, s) 2^s syndromes at unpaired-count s (s == B mod 2).
     Recovers L = (3^B + 1)/2 and M = C(2B, B) (#717 Sec 7 / #728).  Verified
     against brute force for P = 3^i, 5^i.

  BLOCK B  ROBUST LOWER BOUND (any distinct-subset-sum P, incl. non-B[+-2]).
     For every R subset [B], |R| = s == B (mod 2), the syndrome
     sigma_R = ((B - s)/2) c + sum_{i in R} A_i has  |Phi^{-1}(sigma_R)| >=
     C(B - s, (B - s)/2), and the C(B, s) syndromes {sigma_R} are DISTINCT.
     Verified for the non-superincreasing Conway-Guy sets {3,5,6,7},
     {11,17,20,22,23,24}, and base 2^i (all distinct-subset-sum, none B[+-2]).
     The central fiber is C(B, B/2) for ALL of them (re-verifies #735 Thm 2).

  BLOCK C  CONCENTRATION IS DECIDED FALSE.  From the exact formula, for every
     fixed eta in (0, ln(3/2)/2),
        #{sigma : |Phi^{-1}(sigma)| >= e^{eta N} M / L}  =  e^{Theta(N)}
     and   min_{T_h} ( #{fiber >= T_h} + max{fiber < T_h} )  =  e^{Theta(N)},
     N = |T| = 2B.  Tabulated to B = 256: log2(#heavy)/B and log2(minPieces)/B
     stay bounded BELOW by a positive constant -- so neither is e^{o(N)}.
     This is #732 Prop 3.1's cardinality obstruction, realized by the actual
     atlas family (not an adversarial synthetic profile).

  BLOCK D  a != B BOUNDARY.  The classification changes; the profile stays a
     non-concentrated staircase on the a = B +- 2 cases checked (reported, not
     claimed in general).

Interfaces: avdeevvadim's #716 (the dichotomy + concentration residual);
  #717 (Johnson depth-R prefix chart, Sec 7 superincreasing witness);
  #729 (density criterion q_+ = 1/(3/2 - logM/logL), layer-cake piece-split);
  #732 (Theorem B: split is #716's decomposition IFF staircase-concentrated;
        Prop 3.1 cardinality obstruction); #735 (Thm 2: central fiber = twin
        unions on any Sidon P).

Usage:
  python3 verify_staircase_concentration_sidon_paired.py            # RESULT: PASS (n/n)
  python3 verify_staircase_concentration_sidon_paired.py --tamper-selftest
  python3 verify_staircase_concentration_sidon_paired.py --json out.json
"""
import sys
import json
from math import comb, lgamma, log, log2
from itertools import combinations
from collections import Counter

LN2 = log(2.0)
LN3 = log(3.0)

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def is_distinct_subset_sum(P):
    """All 2^|P| subset sums distinct (dissociated over {0,1})."""
    sums = set()
    for r in range(len(P) + 1):
        for S in combinations(P, r):
            s = sum(S)
            if s in sums:
                return False
            sums.add(s)
    return True

def is_two_superincreasing(P):
    """A_i > 2 * sum_{j<i} A_j  (=> B[+-2]-dissociated => exact fiber formula)."""
    s = 0
    for x in sorted(P):
        if x <= 2 * s:
            return False
        s += x
    return True

def brute_profile(P, c, a):
    """Exact fiber-size multiset of the subset-sum chart on T = P u (c-P)."""
    T = list(P) + [c - x for x in P]
    fib = Counter()
    for S in combinations(T, a):
        fib[sum(S)] += 1
    return fib  # syndrome -> fiber size

def predicted_size_multiplicity(B):
    """B[+-2] prediction: fiber phi(s)=C(B-s,(B-s)/2) with mult C(B,s)2^s, s==B(2)."""
    p = {}
    for s in range(B + 1):
        if (s - B) % 2 == 0:
            phi = comb(B - s, (B - s) // 2)
            p[phi] = p.get(phi, 0) + comb(B, s) * (2 ** s)
    return p

def log2_comb(n, k):
    """log2 C(n,k) via lgamma (safe for large n)."""
    if k < 0 or k > n:
        return float("-inf")
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / LN2

def log2_M_over_L(B):
    """log2( C(2B,B) / ((3^B+1)/2) ) without building 3^B as float."""
    # log2 C(2B,B) - [ B*log2(3) + log2(1 + 3^-B) - 1 ]
    return log2_comb(2 * B, B) - (B * (LN3 / LN2) + log2(1.0 + 3.0 ** (-B)) - 1.0)

# ---------------------------------------------------------------------------
# concentration counts from the EXACT formula (fast, large B)
# ---------------------------------------------------------------------------
def heavy_count_formula(B, eta):
    """#{sigma : fiber >= e^{eta N} M/L}, N = 2B, via the exact B[+-2] profile.
    Compared in log2 space so no astronomically large float is formed."""
    N = 2 * B
    thr_log2 = (eta * N) / LN2 + log2_M_over_L(B)   # log2 threshold
    total = 0
    for s in range(B + 1):
        if (s - B) % 2 == 0:
            if log2_comb(B - s, (B - s) // 2) >= thr_log2 - 1e-9:
                total += comb(B, s) * (2 ** s)
    return total  # exact int

def min_piece_count_formula(B):
    """min over thresholds T_h of ( #{fiber >= T_h} + max{fiber < T_h} ).
    Fiber size is strictly decreasing in unpaired-count s, so a threshold is a
    cut at some level s0: heavy = {s <= s0}, light-max = phi(s0+2)."""
    levels = [(s, comb(B - s, (B - s) // 2), comb(B, s) * (2 ** s))
              for s in range(B + 1) if (s - B) % 2 == 0]
    levels.sort()  # by s ascending (fiber descending)
    best = None
    cum = 0
    for i, (s, phi, mult) in enumerate(levels):
        cum += mult
        max_light = levels[i + 1][1] if i + 1 < len(levels) else 0
        pieces = cum + max_light
        if best is None or pieces < best:
            best = pieces
    return best  # exact int

# ---------------------------------------------------------------------------
# verification blocks
# ---------------------------------------------------------------------------
class Checker:
    def __init__(self, tamper=False):
        self.passed = 0
        self.total = 0
        self.tamper = tamper
        self.tamper_hits = 0
        self.tamper_seen = 0

    def check(self, name, got, want, tamper_key=None):
        self.total += 1
        if self.tamper and tamper_key is not None:
            self.tamper_seen += 1
            want = want + 1 if isinstance(want, int) else (not want)  # corrupt expectation
        ok = (got == want)
        if self.tamper and tamper_key is not None:
            if not ok:
                self.tamper_hits += 1
            self.passed += 1  # a caught tamper counts as pass of the self-test
            return
        if ok:
            self.passed += 1
        else:
            print(f"  FAIL [{name}]: got {got!r}, want {want!r}")

    def check_true(self, name, cond, tamper_key=None):
        self.check(name, bool(cond), True, tamper_key=tamper_key)


def run(checker, cert):
    B_BRUTE = [2, 4, 6, 8]
    # --- BLOCK A: exact fiber-size classification (B[+-2] base) ---
    cert["blockA_exact_formula"] = {}
    for name, gen in [("3^i", lambda B: [3 ** i for i in range(B)]),
                      ("5^i", lambda B: [5 ** i for i in range(B)])]:
        rows = []
        for B in B_BRUTE:
            P = gen(B)
            checker.check_true(f"A:{name}:B={B}:dss", is_distinct_subset_sum(P))
            checker.check_true(f"A:{name}:B={B}:2si", is_two_superincreasing(P))
            c = 2 * sum(P) + 1
            fib = brute_profile(P, c, B)
            sizes = dict(sorted(Counter(fib.values()).items()))
            pred = dict(sorted(predicted_size_multiplicity(B).items()))
            checker.check(f"A:{name}:B={B}:profile", sizes, pred,
                          tamper_key=(True if (name=="3^i" and B==6) else None))
            checker.check(f"A:{name}:B={B}:L", len(fib), (3 ** B + 1) // 2)
            checker.check(f"A:{name}:B={B}:M", sum(fib.values()), comb(2 * B, B))
            central = (B // 2) * c
            checker.check(f"A:{name}:B={B}:central", fib[central], comb(B, B // 2))
            rows.append({"B": B, "L": len(fib), "M": sum(fib.values()),
                         "central_fiber": fib[central], "size_mult": sizes})
        cert["blockA_exact_formula"][name] = rows

    # --- BLOCK B: robust lower bound, ANY distinct-subset-sum P ---
    cert["blockB_robust_lower_bound"] = {}
    families = [
        ("2^i", [2 ** i for i in range(6)]),                 # dss, NOT B[+-2]
        ("CG-{3,5,6,7}", [3, 5, 6, 7]),                      # Conway-Guy, B=4
        ("CG-{11,17,20,22,23,24}", [11, 17, 20, 22, 23, 24]),  # Conway-Guy, B=6
    ]
    for name, P in families:
        B = len(P)
        checker.check_true(f"B:{name}:dss", is_distinct_subset_sum(P))
        checker.check_true(f"B:{name}:not-2si", not is_two_superincreasing(P))
        c = 2 * sum(P) + 1
        fib = brute_profile(P, c, B)
        central = (B // 2) * c
        checker.check(f"B:{name}:central=C(B,B/2)", fib[central], comb(B, B // 2))
        # sigma_R lower bound + distinctness, all s
        lb_ok = True
        sig_set = {}
        distinct_ok = True
        for s in range(B + 1):
            if (s - B) % 2:
                continue
            seen = set()
            for R in combinations(range(B), s):
                sig = ((B - s) // 2) * c + sum(P[i] for i in R)
                if fib.get(sig, 0) < comb(B - s, (B - s) // 2):
                    lb_ok = False
                if sig in seen:
                    distinct_ok = False
                seen.add(sig)
        checker.check_true(f"B:{name}:sigmaR>=C(B-s,(B-s)/2)", lb_ok,
                           tamper_key=(True if name=="CG-{3,5,6,7}" else None))
        checker.check_true(f"B:{name}:sigmaR-distinct", distinct_ok)
        # non-B[+-2] sets carry EXTRA (>=1) fibers above the clean staircase
        clean_sizes = set(predicted_size_multiplicity(B).keys())
        actual_sizes = set(fib.values())
        checker.check_true(f"B:{name}:has-intermediate-fibers",
                           len(actual_sizes - clean_sizes) > 0)
        cert["blockB_robust_lower_bound"][name] = {
            "B": B, "central_fiber": fib[central], "L": len(fib),
            "size_mult": dict(sorted(Counter(fib.values()).items())),
            "lower_bound_holds": lb_ok, "sigmaR_distinct": distinct_ok}

    # --- BLOCK C: concentration DECIDED FALSE (exact formula, large B) ---
    cert["blockC_concentration"] = {"eta_table": [], "rate_table": []}
    # C1: brute vs formula agreement for #heavy at small B (consistency)
    for B in [4, 6, 8]:
        P = [5 ** i for i in range(B)]
        c = 2 * sum(P) + 1
        fib = brute_profile(P, c, B)
        M, L = sum(fib.values()), len(fib)
        for eta in [0.05, 0.10]:
            import math
            thr = math.exp(eta * 2 * B) * M / L
            brute_heavy = sum(1 for v in fib.values() if v >= thr)
            form_heavy = heavy_count_formula(B, eta)
            checker.check(f"C:consistency:B={B}:eta={eta}", brute_heavy, form_heavy)
    # C2: eta-table -- heavy count grows exponentially
    for B in [8, 16, 32, 64, 128, 256]:
        row = {"B": B, "N": 2 * B, "log2_M_over_L": round(log2_M_over_L(B), 4)}
        for eta in [0.02, 0.05, 0.10]:
            h = heavy_count_formula(B, eta)
            row[f"heavy_eta{eta}_log2"] = (h.bit_length() - 1) if h > 0 else -1
            row[f"heavy_eta{eta}_rate"] = round((h.bit_length() - 1) / B, 4) if h > 0 else 0.0
        mp = min_piece_count_formula(B)
        row["minPieces_log2"] = mp.bit_length() - 1
        row["minPieces_rate"] = round((mp.bit_length() - 1) / B, 4)
        cert["blockC_concentration"]["eta_table"].append(row)
    # C3: certified NOT-e^{o(N)} -- rates bounded below by a positive constant
    # min-piece-count rate log2(minPieces)/B >= 0.30 for all B >= 8
    for B in [8, 16, 32, 64, 128, 256]:
        mp = min_piece_count_formula(B)
        checker.check_true(f"C:minPieces-superpoly:B={B}",
                           (mp.bit_length() - 1) >= 0.30 * B,
                           tamper_key=(True if B==64 else None))
        # heavy count at eta=0.05 also exponential for B >= 8
        h = heavy_count_formula(B, 0.05)
        checker.check_true(f"C:heavy-exp:B={B}", (h.bit_length() - 1) >= 0.30 * B)
    # explicit super-polynomial witness at B=256 (log2 ~ 210 and ~358 resp.),
    # each exceeds the degree-20 polynomial bound B^20 = 2^160.
    mp256 = min_piece_count_formula(256)
    checker.check_true("C:minPieces(256)>256^20", mp256 > 256 ** 20)
    h256 = heavy_count_formula(256, 0.05)
    checker.check_true("C:heavy(256,0.05)>256^20", h256 > 256 ** 20)
    cert["blockC_concentration"]["decision"] = "NOT_STAIRCASE_CONCENTRATED"
    cert["blockC_concentration"]["minPieces_256_log2"] = mp256.bit_length() - 1
    cert["blockC_concentration"]["heavy_256_eta0.05_log2"] = h256.bit_length() - 1
    cert["blockC_concentration"]["poly_bound_256^20_log2"] = (256 ** 20).bit_length() - 1

    # --- BLOCK D: a != B boundary (report; profile stays non-concentrated) ---
    cert["blockD_a_neq_B"] = []
    for B, a in [(6, 4), (6, 8)]:
        P = [3 ** i for i in range(B)]
        c = 2 * sum(P) + 1
        fib = brute_profile(P, c, a)
        M, L = sum(fib.values()), len(fib)
        sizes = dict(sorted(Counter(fib.values()).items()))
        # min piece count of the ACTUAL (brute) profile
        fs = sorted(set(fib.values()), reverse=True)
        vals = sorted(fib.values(), reverse=True)
        cnt = Counter(fib.values())
        best = None
        cum = 0
        for th in fs:  # threshold at each distinct fiber size
            cum = sum(m for v, m in cnt.items() if v >= th)
            below = [v for v in cnt if v < th]
            max_below = max(below) if below else 0
            pieces = cum + max_below
            if best is None or pieces < best:
                best = pieces
        checker.check(f"D:B={B},a={a}:M", M, comb(2 * B, a))
        cert["blockD_a_neq_B"].append(
            {"B": B, "a": a, "M": M, "L": L, "size_mult": sizes,
             "min_pieces_actual_profile": best})

    return checker


def main():
    args = sys.argv[1:]
    tamper = "--tamper-selftest" in args
    json_path = None
    if "--json" in args:
        json_path = args[args.index("--json") + 1]

    if tamper:
        c = Checker(tamper=True)
        cert = {}
        run(c, cert)
        print(f"tamper-selftest: caught {c.tamper_hits}/{c.tamper_seen}")
        if c.tamper_hits != c.tamper_seen:
            print("RESULT: FAIL (tamper self-test did not catch every corruption)")
            sys.exit(1)
        # then a clean run
        c2 = Checker(tamper=False)
        cert2 = {}
        run(c2, cert2)
        print(f"RESULT: {'PASS' if c2.passed == c2.total else 'FAIL'} ({c2.passed}/{c2.total})")
        sys.exit(0 if c2.passed == c2.total else 1)

    checker = Checker(tamper=False)
    cert = {
        "packet": "staircase_concentration_sidon_paired",
        "class": "T = P u (c-P), P distinct-subset-sum, |P|=B, a=B, c>2 sum P, "
                 "Phi = subset sum over Z",
        "verdict": "CONCENTRATION DECIDED FALSE (route-cut): the Sidon-paired "
                   "depth-1 fiber profile is an exponential staircase; #732's "
                   "staircase-concentration hypothesis fails on this class.",
        "N_convention": "N = |T| = 2B",
    }
    run(checker, cert)
    cert["result"] = {"passed": checker.passed, "total": checker.total}
    ok = checker.passed == checker.total
    if json_path:
        with open(json_path, "w") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
        print(f"wrote {json_path}")
    print(f"RESULT: {'PASS' if ok else 'FAIL'} ({checker.passed}/{checker.total})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
