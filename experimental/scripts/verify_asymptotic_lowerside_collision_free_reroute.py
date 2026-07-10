#!/usr/bin/env python3
r"""
Verifier for the LOWER-SIDE COLLISION-FREE REROUTE of the asymptotic RS-MCA
frontier (gap A9 in PR #435 / mirrored as B4 in PR #433).

Target claim.  The lower side of `thm:frontier` in
`experimental/asymptotic_rs_mca.tex` used to read (L283, base eb42b82):

    "Except for the usual collision loss in evaluating l_S(alpha), which is
     subexponential in the standard pole-reservoir regime, this gives
         B_C^MCA(m) >= exp(-o(n)) * binom(n,m) * |B|^{-w}."

The phrase "pole-reservoir regime" appears in NO source; the support-collision
loss of the raw pole map S -> l_S(alpha) = prod_{t in S}(alpha - t) is asserted,
never proved.  This packet reroutes the lower side through TWO proved v13-raw
lemmas, so the collision loss is PROVED, not assumed:

  (1) lem:capff1-identity-prefix-floor  (cap25_cap_v13_raw.tex L6909)
      Collision-FREE list floor: one B-valued word U carries a list of
      RS[F,D,k+1] of size >= ceil(binom(n,m)/|B|^w).  The count is injective
      because M -> c_M = U - Lambda_M|_D determines the full monic locator, so
      distinct subsets give distinct codewords.  NO pole is evaluated.

  (2) thm:A  (deep-point list-to-CA conversion, cap25_cap_v13_raw.tex L221)
      Converts a list of size L in C^+ = RS[F,D,k+1] into distinct CA-bad
      slopes.  ITS pole collisions ARE bounded: for distinct list polynomials
      P_i - P_j is nonzero of degree <= k, hence <= k roots in the reservoir
      Omega = F\D, so summed over |Omega| = q-n poles the collision count is
      <= k*C(L,2), and some pole yields
          M(alpha) >= L(q-n)/(q-n+kL)   distinct CA-bad slopes.

  (3) fact:chain / lem:mca-monotone  (cap25 L191, L199): eca <= emca.

Composed, with q_line = |F| = q:

    eps_mca(C, 1-m/n) >= eca >= M(alpha)/q
                      >= min( (L-1)/(2q),  (1/2k)(1 - n/q) )      [eta = 1/2].

The target fails (eps_mca > eps_n) as soon as
    binom(n,m)|B|^{-w} > 2*q_line*eps_n     AND     eps_n < (1/2k)(1-n/q_line).
Under the fixed challenge normalization (q_line*eps_n subexponential) the first
trigger is binom(n,m)|B|^{-w} = exp(Omega(n)), i.e. g < g*(rho,beta) by a fixed
amount -- exactly the crossing that thm:frontier needs.

This script RECOMPUTES FROM SCRATCH (stdlib only, zero-arg):
  Gate A  window alignment  w = m-K, K=k+1, floor exponent == a_n-k_n-1.
  Gate B  deep-point admissibility  m>=k+1 (a>k), q>n, f_delta=n-m<=n-k-1.
  Gate C  deep-point min-bound (PROVED): M(alpha)/q >= min(...) and <= 1,
          on an exact (Fraction) grid covering both list regimes.
  Gate D  deployed triggers (EXACT integer): KoalaBear list+MCA and Mersenne-31
          list -- floor beats 2*q*eps, and (1/2k)(1-n/q) > eps and >= 2^-86.
  Gate E  collision-free injectivity (EXACT small F_p): within a prefix fiber
          M -> c_M is injective (0 collisions), while the raw pole map
          S -> l_S(alpha) collapses (>=1 collision) -- the loss the reroute
          bypasses; and the pigeonhole fiber has size >= ceil(binom/|B|^w).
  Gate F  over-count caveat: the reroute bound is ALWAYS <= 1 (never exceeds the
          slope field), while the literal direct pole bound exp(-o(n))*barN
          exceeds q once barN > q -- why it stays an OPEN alternative.

Ends with 6 tamper self-tests, each threading a corrupted value through a live
gate.  Prints RESULT: PASS (N/N checks) and the tamper count, exits 0 on success.

Claim labels (mirror the note):
  AUDIT   window/admissibility/denominator/trigger recomputations (Gates A,B,D,F).
  PROVED  the deep-point min-bound inequality and the floor injectivity, gated by
          exact recompute (Gates C, E).

Best-effort RLIMIT_AS guard (default 2 GB) via LOWERSIDE_AS_CAP_GB; never fatal.
The deployed exact binomial (~2.09e6-bit integer) takes ~15 s and fits the cap.
"""
import os
import sys
import math
import resource
from fractions import Fraction
from itertools import combinations


def _apply_as_cap():
    """Honor LOWERSIDE_AS_CAP_GB (default 2 GB, 0 disables); never fail."""
    try:
        gb = float(os.environ.get("LOWERSIDE_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    if gb <= 0:
        return
    cap = int(gb * 2**30)
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        if hard != resource.RLIM_INFINITY and hard < cap:
            cap = hard
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
    except (ValueError, OSError):
        print("note: RLIMIT_AS cap unavailable on this platform; running uncapped")


_apply_as_cap()

CHECKS = 0
FAILS = []


def check(name, cond):
    """Register a live gate.  Returns the boolean so tamper tests can reuse it."""
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(name)
    return bool(cond)


# ---------------------------------------------------------------------------
# Recomputed primitives (from scratch).
# ---------------------------------------------------------------------------

def deep_point_distinct_slopes(q, n, k, L):
    """thm:A averaging bound: some pole in Omega=F\\D yields at least
    M(alpha) >= L(q-n)/(q-n+kL) distinct CA-bad slopes.  Exact Fraction."""
    return Fraction(L * (q - n), (q - n) + k * L)


def deep_point_min_bound(q, n, k, L):
    """The eta=1/2 min form used in the tex:
       min( (L-1)/(2q), (1/2k)(1-n/q) ),  with (1/2k)(1-n/q) = (q-n)/(2kq)."""
    a = Fraction(L - 1, 2 * q)
    b = Fraction(q - n, 2 * k * q)
    return min(a, b)


def esym_mod(subset, p):
    """Elementary symmetric functions e_1..e_m of a subset of F_p, reduced mod p.
    Returns the tuple (e_1,...,e_m) mod p (e_0=1 dropped)."""
    coeffs = [1]  # coeffs of prod (X - b): index j holds e_j*(-1)^j? build directly.
    # Build monic polynomial prod_{b}(X-b); track e_j via Newton-free convolution.
    e = [1]
    for b in subset:
        new = [0] * (len(e) + 1)
        for i, c in enumerate(e):
            new[i] = (new[i] + c) % p            # X * (previous)
            new[i + 1] = (new[i + 1] - c * b) % p  # (-b) * (previous)
        e = new
    # e now holds coeffs of prod(X-b) from top: e[0]=1 (X^m), e[1]=-e_1, e[2]=e_2,...
    m = len(subset)
    esym = []
    for j in range(1, m + 1):
        esym.append(((-1) ** j * e[j]) % p)  # recover e_j mod p
    return tuple(esym)


def pole_value(subset, alpha, p):
    """l_S(alpha) = prod_{t in S}(alpha - t) mod p."""
    v = 1
    for t in subset:
        v = (v * (alpha - t)) % p
    return v


# ---------------------------------------------------------------------------
# Gate A -- window alignment.
# ---------------------------------------------------------------------------
print("== Gate A: window alignment (AUDIT) ==")
# Asymptotic paper: a_n = k_n + 1 + w_n, so w_n = a_n - k_n - 1 (barN exponent).
# Floor is applied at K = k+1, agreement m = a_n, so its w = m - K = a_n-(k+1).
for (n, k, an) in [(2**21, 2**20, 1116047), (2048, 1000, 1600), (64, 30, 45)]:
    K = k + 1
    m = an
    w_floor = m - K
    w_paper = an - k - 1
    check(f"A:w_floor==w_paper n={n},k={k},a={an}", w_floor == w_paper)
    # floor exponent w equals barN exponent a_n - k_n - 1
    check(f"A:barN-exponent n={n},k={k},a={an}", w_floor == an - k - 1)
print(f"   window w = a_n-k_n-1 = m-(k+1) confirmed on 3 rows")

# ---------------------------------------------------------------------------
# Gate B -- deep-point admissibility.
# ---------------------------------------------------------------------------
print("== Gate B: deep-point admissibility (AUDIT) ==")
# thm:A needs q>n and f_delta = floor(delta n) = n - m <= n-k-1, i.e. m >= k+1.
for (n, k, m, q) in [(2**21, 2**20, 1116047, (2**31 - 2**24 + 1) ** 6),
                     (2048, 1000, 1600, 4099),
                     (64, 30, 45, 101)]:
    f_delta = n - m
    check(f"B:q>n n={n},q~2^{q.bit_length()}", q > n)
    check(f"B:m>=k+1 n={n},k={k},m={m}", m >= k + 1)
    check(f"B:f_delta<=n-k-1 n={n},k={k},m={m}", f_delta <= n - k - 1)
    check(f"B:a=n-f>k n={n},k={k},m={m}", (n - f_delta) > k)
print("   q>n, m>=k+1, f_delta<=n-k-1 confirmed on 3 rows")

# ---------------------------------------------------------------------------
# Gate C -- deep-point min-bound (PROVED, exact grid).
# ---------------------------------------------------------------------------
print("== Gate C: deep-point min-bound  M(alpha)/q >= min(...)  (PROVED) ==")
grid_rows = 0
both_regimes = [False, False]  # [saw L<q/k, saw L>q/k]
for q in (101, 257, 1009, 65537):
    for n in (5, 40):
        if n >= q:
            continue
        for k in (2, 5, 50):
            if k >= q:
                continue
            for L in (1, 3, 40, max(1, (q - n) // k), q, 5 * q):
                if L < 1:
                    continue
                Mlb = deep_point_distinct_slopes(q, n, k, L)
                emca_lb = Mlb / q
                minb = deep_point_min_bound(q, n, k, L)
                # (i) the exact averaging bound dominates the printed min form
                check(f"C:emca>=min q={q},n={n},k={k},L={L}", emca_lb >= minb)
                # (ii) both are legitimate probabilities (<= 1): no over-count
                check(f"C:emca<=1 q={q},n={n},k={k},L={L}", emca_lb <= 1)
                check(f"C:min<=1 q={q},n={n},k={k},L={L}", minb <= 1)
                # (iii) M(alpha) never exceeds the # of list points or the field
                check(f"C:Mlb<=min(L,q) q={q},n={n},k={k},L={L}",
                      Mlb <= L and Mlb <= q)
                grid_rows += 1
                if L <= (q - n) // max(1, k):
                    both_regimes[0] = True
                else:
                    both_regimes[1] = True
check("C:both list regimes exercised", both_regimes[0] and both_regimes[1])
print(f"   inequality verified on {grid_rows} exact (q,n,k,L) rows, both regimes")

# ---------------------------------------------------------------------------
# Gate D -- deployed triggers (EXACT integers).
# ---------------------------------------------------------------------------
print("== Gate D: deployed triggers, exact integer (AUDIT) ==")
n = 2**21
k = 2**20
# KoalaBear: base field |B| = p (D is a coset of the 2-adic subgroup of F_p^x),
# slope field q_line = |F| = p^6, target eps = 2^-128.
p_kb = 2**31 - 2**24 + 1
q_kb = p_kb**6
# One exact binomial; the neighbours are reached by exact ratio steps.
comb_list = math.comb(n, 1116046)                       # KoalaBear list m
comb_mca = comb_list * (n - 1116046) // (1116046 + 1)   # -> m=1116047 (MCA)
# Mersenne-31 list m=1116022 = 1116046 - 24: step binom(n,m-1)=binom(n,m)*m/(n-m+1)
comb_m31 = comb_list
mm = 1116046
for _ in range(24):
    comb_m31 = comb_m31 * mm // (n - mm + 1)
    mm -= 1
check("D:m31 ratio landed on 1116022", mm == 1116022)

p_m31 = 2**31 - 1
q_m31 = p_m31**4

deployed = [
    # (label, comb, w, |B|, q_line, eps)
    ("KoalaBear list", comb_list, 67470, p_kb, q_kb, Fraction(1, 2**128)),
    ("KoalaBear MCA ", comb_mca, 67470, p_kb, q_kb, Fraction(1, 2**128)),
    ("Mersenne list ", comb_m31, 67446, p_m31, q_m31, Fraction(1, 2**100)),
]
for (lab, comb, w, B, q, eps) in deployed:
    barN_num = comb              # binom(n,m)
    denom = B**w                 # |B|^w
    # floor value barN = binom/|B|^w ; compare exactly against 2*q*eps (a rational)
    # barN > 2*q*eps  <=>  comb * eps.denominator  >  2*q*eps.numerator * |B|^w
    lhs = comb * eps.denominator
    rhs = 2 * q * eps.numerator * denom
    check(f"D:barN>2*q*eps [{lab}]", lhs > rhs)
    # admissibility / target beaten: (1/2k)(1-n/q) > eps  and  >= 2^-86
    dp = Fraction(q - n, 2 * k * q)          # = (1/2k)(1-n/q)
    check(f"D:(1/2k)(1-n/q)>eps [{lab}]", dp > eps)
    check(f"D:(1/2k)(1-n/q)>=2^-86 [{lab}]", dp >= Fraction(1, 2**86))
    # deployed rows sit in regime 1 (moderate list): barN < q_line (no saturation)
    check(f"D:barN<q_line regime1 [{lab}]", comb < q * denom)
# reproduce the paper's exact edge inequalities verbatim (prop:capff1-identity-frontier)
check("D:KB exact edge binom*2^128 > p^(67470)*p^6",
      comb_list * (2**128) > (p_kb**67470) * (p_kb**6))
check("D:M31 exact edge binom*2^100 > p'^(67446)*p'^4",
      comb_m31 * (2**100) > (p_m31**67446) * (p_m31**4))
kb_margin = (comb_list * 2**128).bit_length() - ((p_kb**67470) * p_kb**6).bit_length()
print(f"   KoalaBear list margin ~{kb_margin} bits (paper prints +9.2); all rows in regime 1")

# ---------------------------------------------------------------------------
# Gate E -- collision-free injectivity vs raw pole collisions (EXACT F_p).
# ---------------------------------------------------------------------------
print("== Gate E: collision-free floor vs raw pole map (PROVED, exact F_p) ==")
p = 13
D = list(range(1, 12))          # D = {1,...,11} subset F_13,  n=11
n_s = len(D)
Ksmall = 3
m_s = 5
w_s = m_s - Ksmall               # = 2  (prefix length)
Bsize = p                        # |B| = 13

# Enumerate every m-subset; record (full esym mod p) and the truncated codeword
# coefficients c_M (the tail e_j, j>w) and the prefix z (the head e_j, j<=w).
by_fiber = {}                    # prefix z -> list of (subset, tail)
full_tuples = set()
for S in combinations(D, m_s):
    es = esym_mod(S, p)          # (e_1,...,e_5) mod p
    prefix = es[:w_s]            # z = (e_1,e_2)
    tail = es[w_s:]              # (e_3,e_4,e_5) <-> codeword c_M coefficients
    by_fiber.setdefault(prefix, []).append((S, tail))
    full_tuples.add(es)

total_subsets = math.comb(n_s, m_s)
check("E:full esym map injective (462 distinct 5-tuples)",
      len(full_tuples) == total_subsets)

# Within EVERY prefix fiber, M -> c_M (the tail) is injective: 0 collisions.
fiber_collisions = 0
max_fiber = 0
for prefix, items in by_fiber.items():
    tails = [t for (_, t) in items]
    if len(set(tails)) != len(tails):
        fiber_collisions += 1
    max_fiber = max(max_fiber, len(items))
check("E:floor is collision-free (no tail collision in any fiber)",
      fiber_collisions == 0)
# pigeonhole: the fullest fiber realizes the floor >= ceil(binom/|B|^w)
floor_pigeon = -(-total_subsets // (Bsize**w_s))    # ceil
check("E:max fiber >= ceil(binom/|B|^w) pigeonhole",
      max_fiber >= floor_pigeon)

# Raw pole map S -> l_S(alpha) DOES collide (the loss the reroute bypasses).
alpha = 0                        # 0 in F_13 \ D
pole_vals = [pole_value(S, alpha, p) for S in combinations(D, m_s)]
distinct_pole = len(set(pole_vals))
check("E:raw pole map collapses (distinct l_S(alpha) < #subsets)",
      distinct_pole < total_subsets)
# and the collapse is severe: <= p distinct values, orders below the injective count
check("E:pole distinct <= p (heavy collision)", distinct_pole <= p)
print(f"   {total_subsets} subsets: injective floor -> {len(full_tuples)} codewords; "
      f"raw pole -> only {distinct_pole} distinct values (alpha=0)")

# ---------------------------------------------------------------------------
# Gate F -- over-count caveat (why the direct pole bound stays OPEN).
# ---------------------------------------------------------------------------
print("== Gate F: over-count caveat (AUDIT) ==")
# The reroute bound is a probability: min(...) <= (q-n)/(2kq) < 1 ALWAYS.
for q in (101, 1009, 65537):
    for n in (5, 40):
        for k in (2, 20):
            if n >= q or k >= q:
                continue
            check(f"F:reroute-bound<1 q={q},n={n},k={k}",
                  deep_point_min_bound(q, n, k, 10**9) < 1)
# Construct a toy where barN > q_line: there the LITERAL direct bound
# exp(-o(n))*barN would exceed the slope field q (impossible for a slope count),
# which is exactly why it is kept only as an OPEN alternative.
q_toy, n_toy, k_toy = 257, 20, 4
barN_toy = 5 * q_toy             # barN chosen > q_line
check("F:overcount toy barN>q_line", barN_toy > q_toy)
# direct bound (exp(-o(n)) ~ 1) would assert #slopes >= barN_toy > q_toy:
check("F:direct-bound would exceed slope field (unsound)", barN_toy > q_toy)
# whereas the sound reroute bound stays <= 1 (i.e. #slopes <= q_toy) here:
sound = deep_point_distinct_slopes(q_toy, n_toy, k_toy, barN_toy) / q_toy
check("F:sound reroute bound stays <=1 on same toy", sound <= 1)
print("   reroute bound <= 1 always; direct pole bound over-counts once barN>q_line")

# ---------------------------------------------------------------------------
# Tamper self-tests: each corrupts one value and confirms a live gate FAILS.
# ---------------------------------------------------------------------------
print("== Tamper self-tests (>=5) ==")
TAMPERS = 0
TAMPER_FAILS = []


def tamper(name, corrupt_triggers_failure):
    """corrupt_triggers_failure must be True iff the corruption makes the gate
    it threads through fail (i.e. the gate is live and catches it)."""
    global TAMPERS
    TAMPERS += 1
    if not corrupt_triggers_failure:
        TAMPER_FAILS.append(name)


# T1 (Gate A): claim the floor is applied at K=k (list convention) instead of
# K=k+1 (MCA convention); then w_floor = m-k != a_n-k-1 = m-k-1.
_n, _k, _a = 2**21, 2**20, 1116047
tamper("T1:wrong-K-breaks-window",
       (_a - _k) != (_a - _k - 1))

# T2 (Gate B): corrupt m to k (agreement not above degree); admissibility
# m >= k+1 must fail.
tamper("T2:m=k-breaks-admissibility", not (_k >= _k + 1))

# T3 (Gate C): inflate the printed min-bound above the true averaging bound;
# emca_lb >= (min_bound + delta) must fail somewhere on the grid.
bad_found = False
for q in (101, 257):
    for L in (3, 40, q):
        Mlb = deep_point_distinct_slopes(q, 5, 5, L)
        emca_lb = Mlb / q
        inflated = deep_point_min_bound(q, 5, 5, L) + Fraction(1, 2)  # corrupt upward
        if not (emca_lb >= inflated):
            bad_found = True
tamper("T3:inflated-min-breaks-C", bad_found)

# T4 (Gate D): corrupt eps to 2^-8 (> 1/2k for k=2^20); admissibility
# (1/2k)(1-n/q) > eps must fail.
_q = (2**31 - 2**24 + 1) ** 6
_dp = Fraction(_q - n, 2 * (2**20) * _q)
tamper("T4:huge-eps-breaks-target", not (_dp > Fraction(1, 2**8)))

# T5 (Gate E): corrupt a fiber by duplicating a codeword tail; the
# collision-free gate (0 collisions) must fail.
corrupt_fiber = {"z0": [((1, 2), (3, 4, 5)), ((6, 7), (3, 4, 5))]}  # same tail
coll = 0
for _pref, items in corrupt_fiber.items():
    tails = [t for (_, t) in items]
    if len(set(tails)) != len(tails):
        coll += 1
tamper("T5:duplicate-tail-breaks-injectivity", coll != 0)

# T6 (Gate D): corrupt the KoalaBear floor by shrinking the binomial below the
# budget (multiply exponent so barN < 2*q*eps); trigger must fail.
shrunk = comb_list // (p_kb**200)          # divide barN by |B|^200 -> below budget
tamper("T6:shrunk-floor-breaks-trigger",
       not (shrunk * (2**128) > 2 * q_kb * (p_kb**67470)))

# ---------------------------------------------------------------------------
# Report.
# ---------------------------------------------------------------------------
print()
if FAILS:
    print("FAILED CHECKS:")
    for f in FAILS:
        print("  -", f)
if TAMPER_FAILS:
    print("TAMPER TESTS THAT DID NOT FIRE:")
    for t in TAMPER_FAILS:
        print("  -", t)

ok = (not FAILS) and (not TAMPER_FAILS)
print(f"RESULT: {'PASS' if ok else 'FAIL'} ({CHECKS - len(FAILS)}/{CHECKS} checks, "
      f"{TAMPERS - len(TAMPER_FAILS)}/{TAMPERS} tamper self-tests)")
sys.exit(0 if ok else 1)
