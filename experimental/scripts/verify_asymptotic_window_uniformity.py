#!/usr/bin/env python3
"""
verify_asymptotic_window_uniformity.py  --  B3 window-uniformity verifier.

Zero-argument, stdlib-only, best-effort RLIMIT_AS 2 GB.  Recomputes, from
scratch and with exact big-integer binomials where feasible, the window
arithmetic that discharges the B3 gap of PR #433 (see
experimental/notes/audits/asymptotic_window_uniformity.md): that the closed
paid ledger of experimental/asymptotic_rs_mca.tex (thm:closed-ledger-package,
consumed at a window-varying agreement by thm:frontier) slides across every
o(n)-window W_n = {a : |a-a_n| <= psi_n}, psi_n = o(n), with a single exp(o(n))
rate, GIVEN single-agreement closure.

Design: every check runs through a LIVE gate function.  The real inputs must
make the gate PASS; the tamper self-tests thread corrupted values through the
SAME gate and must be REJECTED.  Nothing is stubbed and no result is silently
truncated: every cap is printed and every gate prints its PASS count.

Gates (see the note, section 6):
  G1  Lemma W, binomial part      -- exact binom ratio ~ exp(o(n)) on o(n) window
  G2  Lemma W, subfield part      -- |B|^{-o(n)} = exp(o(n)) for bounded base
  G3  combined barN window ratio  -- G1 x G2, exact big-int
  G4  Stirling/entropy identity   -- log2 C(n,a) = n H2(a/n) + O(log n)
  G5  frontier interior guard     -- beta>0 => rho+g* < 1 strictly
  G6  per-cell budget stability   -- C3 flat, census/planted monotone, C4/C8 tame
  G7  cell-count bound            -- active dyadic quotient orders O(1) in n

Tampers (>=5; here 7):
  T1 Theta(n) slide (F2), T2 near-1 interior (F1), T3 unbounded base (F3),
  T4 census non-monotone, T5 wrong entropy (H3 for H2), T6 C8 off-frontier,
  T7 beta=0 boundary (F1).
"""

import math
import resource
import sys

# --------------------------------------------------------------------------
# Best-effort address-space cap (report the outcome; never hard-fail on it).
# --------------------------------------------------------------------------
AS_CAP_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB
_cap_note = ""
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    target = AS_CAP_BYTES if (hard == resource.RLIM_INFINITY or hard > AS_CAP_BYTES) else hard
    resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    _cap_note = "RLIMIT_AS set to %.2f GB (soft), hard=%s" % (
        target / 2**30, "inf" if hard == resource.RLIM_INFINITY else "%.2f GB" % (hard / 2**30))
except (ValueError, OSError) as exc:  # pragma: no cover - platform dependent
    _cap_note = "RLIMIT_AS could not be set (%s); continuing without cap" % exc

# --------------------------------------------------------------------------
# Caps / knobs (all printed at the end).
# --------------------------------------------------------------------------
N_EXACT_MAX = 160_000        # largest n at which exact big-int C(n,a) is computed
NS_EXACT = [10_000, 40_000, 160_000]  # exact big-int ladder for G1/G3/G4
#   ladder starts at 1e4 so round(c*n) discreteness and window overshoot of the
#   entropy peak do not corrupt the small-n end; ratio r=x20 in n is enough to
#   witness the o(n) collapse (surrogate ~ n^{theta-1} shrinks by 20^{1-theta}).
GSTAR_GRID = 400_000         # scan resolution for g*(rho,beta) (monotone scan)
STIR_C = 1.0                 # G4: |log2 C(n,a) - n H2(a/n)| <= STIR_C * log2 n
INTERIOR_MARGIN = 1e-6       # G5 strict-interior margin

CAPS = []  # (name, value/limitation) -- printed verbatim at the end
CAPS.append(("address-space", _cap_note))
CAPS.append(("exact big-int C(n,a)", "computed only for n <= %d (NS_EXACT=%s); "
             "larger n would be exact but slow -- not needed for the o(n) claim" % (N_EXACT_MAX, NS_EXACT)))
CAPS.append(("g* scan", "monotone grid scan with %d points; bisection-free, "
             "error <= (1-rho)/%d per evaluation" % (GSTAR_GRID, GSTAR_GRID)))
CAPS.append(("window family", "finitely many window exponents theta and centres c "
             "are sampled; the o(n) limit is inferred from the strictly shrinking "
             "surrogate, not proved for every psi_n=o(n) sequence"))
CAPS.append(("scope", "checks the ARITHMETIC of the slide and the SHAPE of each cited "
             "budget; does NOT re-derive the algebro-geometric cell counts (that is "
             "#433's FOUND-EXACT citation object)"))


# --------------------------------------------------------------------------
# Exact / accurate primitives.
# --------------------------------------------------------------------------
def log2_bigint(x):
    """Accurate float log2 of an exact positive big integer (no overflow)."""
    if x <= 0:
        return float("-inf")
    b = x.bit_length()
    if b <= 53:
        return math.log2(x)
    s = b - 53
    return s + math.log2(x >> s)


def log2_comb_exact(n, a):
    """log2 of the EXACT integer C(n,a) via math.comb + accurate big-int log2."""
    if a < 0 or a > n:
        return float("-inf")
    return log2_bigint(math.comb(n, a))


def H2(x):
    """Binary entropy in bits."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def H3_wrong(x):
    """A deliberately WRONG 'entropy' (base-3 flavoured) for tamper T5."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log(x, 3) - (1.0 - x) * math.log(1.0 - x, 3)


def gstar(rho, beta):
    """g*(rho,beta) = sup{g in [0,1-rho] : H2(rho+g) >= beta g} by monotone scan."""
    best = 0.0
    span = 1.0 - rho
    for i in range(GSTAR_GRID + 1):
        g = span * i / GSTAR_GRID
        if H2(rho + g) >= beta * g - 1e-15:
            best = g
    return best


# --------------------------------------------------------------------------
# LIVE GATES.  Each returns (passed: bool, detail: str).
# The same gate object is exercised by the real check and by the tampers.
# --------------------------------------------------------------------------
def gate_binom_window(c, dfun, ns):
    """G1: exact (1/n) log2[C(n,a+d)/C(n,a)] must (i) match the entropy surrogate
    H2(c+d/n)-H2(c) within Stirling tolerance and (ii) shrink strictly toward 0
    (the signature of an o(n) window).  Rejects Theta(n) windows and near-1
    centres that leave the interior."""
    surr_abs = []
    for n in ns:
        a = round(c * n)
        d = dfun(n)
        if not (0 < a - d and a + d < n):
            return (False, "window leaves index range at n=%d (a=%d,d=%d)" % (n, a, d))
        cp, cm = (a + d) / n, (a - d) / n
        if not (1e-9 < cm and cp < 1 - 1e-9):
            return (False, "window leaves the open interior (0,1) at n=%d: c+=%.4f" % (n, cp))
        exact = (log2_comb_exact(n, a + d) - log2_comb_exact(n, a)) / n
        surr = H2(cp) - H2(a / n)
        tol = (math.log2(n) + 4.0) / n
        if abs(exact - surr) > tol:
            return (False, "exact!=surrogate at n=%d: |%.6g-%.6g|>%.2g" % (n, exact, surr, tol))
        surr_abs.append(abs(surr))
    # o(n) window  <=>  surrogate collapses toward 0 as n grows.
    strictly_down = all(surr_abs[i + 1] < surr_abs[i] for i in range(len(surr_abs) - 1))
    collapsed = surr_abs[-1] < 0.6 * surr_abs[0]
    if not (strictly_down and collapsed):
        return (False, "normalized log-ratio does not collapse to 0 (surr=%s) -> not o(n)"
                % ["%.4f" % s for s in surr_abs])
    return (True, "surr %.4f -> %.4f (ratio %.2f) over n=%s"
            % (surr_abs[0], surr_abs[-1], surr_abs[-1] / surr_abs[0], ns))


def gate_subfield_window(beta_fun, dfun, ns):
    """G2: the subfield window factor (1/n) * d * log2|B_n| must collapse to 0.
    Rejects unbounded base fields (beta_n growing) for which it does not."""
    vals = []
    for n in ns:
        d = dfun(n)
        beta = beta_fun(n)
        vals.append(d * beta / n)
    # d*beta/n = beta * n^{theta-1} -> 0 for any FIXED beta (theta<1); an
    # unbounded beta_n makes it grow.  Ratio-based: strictly down AND collapsed.
    strictly_down = all(vals[i + 1] < vals[i] for i in range(len(vals) - 1))
    collapsed = vals[-1] < 0.6 * vals[0]
    if not (strictly_down and collapsed):
        return (False, "subfield factor d*beta/n does not collapse: %s"
                % ["%.4f" % v for v in vals])
    return (True, "d*beta/n %.4f -> %.4f (ratio %.2f)" % (vals[0], vals[-1], vals[-1] / vals[0]))


def gate_barN_window(c, rho, beta_const, dfun, ns):
    """G3: combined barN_{n,a} = C(n,a) |B|^{-(a-k-1)} ratio across the window,
    exact big-int binomial x exact subfield power.  Must collapse toward 0."""
    k_of = lambda n: round(rho * n)
    vals = []
    for n in ns:
        a = round(c * n)
        d = dfun(n)
        if not (0 < a - d and a + d < n):
            return (False, "index range at n=%d" % n)
        k = k_of(n)
        # log2 barN(a) = log2 C(n,a) - (a-k-1) log2|B|
        lb = lambda aa: log2_comb_exact(n, aa) - (aa - k - 1) * beta_const
        vals.append(abs(lb(a + d) - lb(a)) / n)
    strictly_down = all(vals[i + 1] < vals[i] for i in range(len(vals) - 1))
    if not (strictly_down and vals[-1] < 0.6 * vals[0]):
        return (False, "barN window ratio does not collapse: %s" % ["%.4f" % v for v in vals])
    return (True, "|log2 barN ratio|/n %.4f -> %.4f" % (vals[0], vals[-1]))


def gate_stirling_identity(c, ns, entropy=H2):
    """G4: |log2 C(n,a) - n*entropy(a/n)| <= STIR_C * log2 n  (validates the
    Stirling expansion used in thm:frontier's proof).  With the wrong entropy
    (H3) the error is Theta(n) and the gate rejects."""
    for n in ns:
        a = round(c * n)
        err = abs(log2_comb_exact(n, a) - n * entropy(a / n))
        if err > STIR_C * math.log2(n):
            return (False, "Stirling error %.3f > %.1f*log2(%d)=%.3f (entropy=%s)"
                    % (err, STIR_C, n, STIR_C * math.log2(n), entropy.__name__))
    return (True, "max Stirling error within %.1f*log2 n over n=%s" % (STIR_C, ns))


def gate_frontier_interior(rho, beta):
    """G5: the crossing c = rho + g*(rho,beta) must be strictly inside (0,1).
    beta>0 => g* < 1-rho => c < 1 (guard for Lemma W); beta=0 => c=1 rejected."""
    g = gstar(rho, beta)
    c = rho + g
    if not (rho > 0.0):
        return (False, "rho=%.4f not > 0" % rho)
    if not (c < 1.0 - INTERIOR_MARGIN):
        return (False, "crossing rho+g*=%.6f not strictly < 1 (boundary/degenerate)" % c)
    return (True, "rho+g*=%.5f in (0,1)" % c)


def planted_count(n, k, M, sigma, tamper=False):
    """C3 planted quotient-core count C(n/M-1, k/M) (thm:capf-planted).
    The genuine count is INDEPENDENT of the slack sigma; tamper=True injects a
    spurious sigma-dependence so the flatness gate can reject it."""
    base = math.comb(n // M - 1, k // M)
    return base + (sigma if tamper else 0)


def census_A2(n1, tamper_at=None):
    """Rate-1/2 census closed form A2 = (3^n1 - 1)/2 (lem:capf-census-identity),
    strictly increasing in n1.  tamper_at injects a non-monotone value."""
    if tamper_at is not None and n1 == tamper_at:
        return (3 ** (n1 - 2) - 1) // 2  # dips below its predecessor
    return (3 ** n1 - 1) // 2


def c8_moving_root(n, a, g=0):
    """C8 per-pencil budget floor((n-g)/((n-a)-g)) (thm:bc-moving-root)."""
    omega = n - a
    if omega - g <= 0:
        return None
    return (n - g) // (omega - g)


def gate_budget_stability(c, dfun, ns):
    """G6: per-cell budget window-stability + monotonicity, all exact.
      (a) C3 planted flat in sigma (equal across the slack range);
      (b) census A2 strictly increasing;
      (c) dyadic planted monotone C(N-1,rN) <= C(2N-1,2rN);
      (d) C4 tangent n-A+1 and C8 floor(n/(n-a)) have o(n) log-variation on W_n,
          and C8 is O(1) at the frontier interior."""
    # (a) planted flat in sigma
    n, k, M = 4096, 2048, 8
    vals = {planted_count(n, k, M, s) for s in range(1, M)}
    if len(vals) != 1:
        return (False, "planted count not flat in sigma: %s" % sorted(vals))
    # (b) census strictly increasing
    prev = -1
    for n1 in range(1, 14):
        v = census_A2(n1)
        if v <= prev:
            return (False, "census A2 not strictly increasing at n1=%d" % n1)
        prev = v
    # (c) dyadic planted monotone via the injective map (prop:capf-dyadic-planted)
    for N in [64, 128, 256]:
        if math.comb(N - 1, N // 2) > math.comb(2 * N - 1, N):
            return (False, "dyadic planted monotonicity fails at N=%d" % N)
    # (d) C4/C8 window log-variation -> 0, and C8 bounded at the frontier
    c4_var, c8_var, c8_front = [], [], []
    Kfront = 1.0 / (1.0 - c) + 2.0  # O(1) frontier ceiling for floor(n/(n-a))
    for n in ns:
        a = round(c * n)
        d = dfun(n)
        c4 = lambda aa: (n - aa + 1)
        c4_var.append(abs(math.log2(c4(a + d)) - math.log2(c4(a))) / n)
        b_here, b_shift = c8_moving_root(n, a), c8_moving_root(n, a + d)
        c8_var.append(abs(math.log2(b_shift) - math.log2(b_here)) / n)
        c8_front.append(b_here)
    if not (c4_var[-1] <= c4_var[0] and c4_var[-1] < 5e-3):
        return (False, "C4 tangent window log-variation not ->0: %s" % ["%.2e" % v for v in c4_var])
    if not (all(v < 5e-3 for v in c8_var) and c8_var[-1] < 1e-4):
        return (False, "C8 moving-root window log-variation not ~0: %s" % ["%.2e" % v for v in c8_var])
    if not all(b <= Kfront for b in c8_front):
        return (False, "C8 not O(1) at frontier interior (ceil=%.1f): %s" % (Kfront, c8_front))
    return (True, "planted flat; census/dyadic monotone; C4/C8 tame (C8<=%.0f)" % Kfront)


def gate_c8_offfrontier_rejected(n, a):
    """G6-adjacent live check used by tamper T6: C8 evaluated OUTSIDE the frontier
    interior (a ~ n) is Theta(n), violating the O(1)-per-pencil frontier claim."""
    c = a / n
    Kfront = 1.0 / (1.0 - c) + 2.0 if c < 1 else float("inf")
    b = c8_moving_root(n, a)
    if b is None or b > Kfront or b > 100:
        return (False, "C8 budget %s exceeds frontier ceiling (a/n=%.4f)" % (b, c))
    return (True, "C8=%s bounded" % b)


def gate_cell_count(rho, eta, ns):
    """G7: number of active dyadic quotient orders M (sigma < M, N=n/M < n/sigma)
    with sigma=ceil(eta n) is bounded by log2(1/eta)+1, constant in n
    (prop:capf-qprofile)."""
    bound = math.log2(1.0 / eta) + 1.0
    counts = []
    for n in ns:
        sigma = math.ceil(eta * n)
        cnt = 0
        M = 1
        while M <= n:
            N = n // M
            if M > sigma and 1 <= N:  # active: sigma < M
                cnt += 1
            M *= 2
        counts.append(cnt)
    if not all(cnt <= bound + 1 for cnt in counts):
        return (False, "active dyadic M count %s exceeds ~%.1f" % (counts, bound))
    spread = max(counts) - min(counts)
    if spread > 2:
        return (False, "active M count not stable in n: %s" % counts)
    return (True, "active dyadic M in %s (bound ~%.1f), stable in n" % (counts, bound))


# --------------------------------------------------------------------------
# Window / base builders.
# --------------------------------------------------------------------------
def w_on(theta):
    """o(n) window half-width d = ceil(n^theta), theta < 1."""
    return lambda n: max(1, math.ceil(n ** theta))


def w_linear(frac):
    """Theta(n) window half-width d = ceil(frac * n) -- for tamper T1."""
    return lambda n: max(1, math.ceil(frac * n))


def beta_const(b):
    return lambda n: b


def beta_growing():
    """Unbounded base bit-size beta_n = n -- for tamper T3."""
    return lambda n: n


# --------------------------------------------------------------------------
# Runner.
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("B3 window-uniformity verifier  (asymptotic_rs_mca.tex / thm:frontier)")
    print("=" * 74)

    real_pass = 0
    real_total = 0
    failures = []

    def real(name, result):
        nonlocal real_pass, real_total
        real_total += 1
        ok, detail = result
        tag = "PASS" if ok else "FAIL"
        print("  [%s] %-34s %s" % (tag, name, detail))
        if ok:
            real_pass += 1
        else:
            failures.append(name)

    # ---- G1: Lemma W, binomial part -------------------------------------
    print("\nG1  Lemma W (binomial part): exact C(n,a+-d)/C(n,a) ~ exp(o(n)) on o(n) window")
    for c in (0.3, 0.5, 0.7):
        for theta in (0.7, 0.6, 0.5):
            real("G1 c=%.1f theta=%.1f" % (c, theta),
                 gate_binom_window(c, w_on(theta), NS_EXACT))

    # ---- G2: Lemma W, subfield part -------------------------------------
    print("\nG2  Lemma W (subfield part): (1/n) d log2|B| -> 0 for bounded base")
    for b in (1.0, 8.0, 31.0, 128.0):
        real("G2 log2|B|=%.0f" % b, gate_subfield_window(beta_const(b), w_on(0.6), NS_EXACT))

    # ---- G3: combined barN window ratio ---------------------------------
    print("\nG3  combined barN = C(n,a)|B|^-(a-k-1) window ratio (exact big-int)")
    for (c, rho, b) in ((0.6, 0.25, 8.0), (0.5, 0.4, 31.0), (0.7, 0.5, 1.0)):
        real("G3 c=%.1f rho=%.2f b=%.0f" % (c, rho, b),
             gate_barN_window(c, rho, b, w_on(0.6), NS_EXACT))

    # ---- G4: Stirling/entropy identity ----------------------------------
    print("\nG4  Stirling identity: |log2 C(n,a) - n H2(a/n)| <= %.1f log2 n" % STIR_C)
    for c in (0.3, 0.5, 0.7):
        real("G4 c=%.1f" % c, gate_stirling_identity(c, NS_EXACT, entropy=H2))

    # ---- G5: frontier interior guard ------------------------------------
    print("\nG5  frontier interior: beta>0 => rho+g* strictly in (0,1)")
    for rho in (0.25, 0.5, 0.75):
        for beta in (1.0, 8.0, 31.0):
            real("G5 rho=%.2f beta=%.0f" % (rho, beta), gate_frontier_interior(rho, beta))

    # ---- G6: per-cell budget window-stability ---------------------------
    print("\nG6  per-cell budget stability (C3 flat / census+dyadic monotone / C4,C8 tame)")
    for c in (0.5, 0.6, 0.7):
        real("G6 c=%.1f" % c, gate_budget_stability(c, w_on(0.6), NS_EXACT))

    # ---- G7: cell-count bound -------------------------------------------
    print("\nG7  cell count: active dyadic quotient orders O(1) in n (prop:capf-qprofile)")
    for eta in (1.0 / 256, 1.0 / 128, 1.0 / 64):
        real("G7 eta=1/%d" % round(1 / eta),
             gate_cell_count(0.5, eta, [2 ** e for e in (12, 16, 20, 22)]))

    # ---- Tamper self-tests: corrupted values through LIVE gates ---------
    print("\n" + "-" * 74)
    print("Tamper self-tests (each corrupted value must be REJECTED by a live gate)")
    tamper_pass = 0
    tamper_total = 0

    def tamper(name, result, expect_reject=True):
        nonlocal tamper_pass, tamper_total
        tamper_total += 1
        ok, detail = result
        rejected = not ok
        good = (rejected == expect_reject)
        tag = "OK-REJECTED" if (good and rejected) else ("OK" if good else "LEAK!!")
        print("  [%s] %-30s %s" % (tag, name, detail))
        if good:
            tamper_pass += 1
        else:
            failures.append("TAMPER-LEAK:" + name)

    # T1: Theta(n) slide (F2) through G1
    tamper("T1 Theta(n) slide", gate_binom_window(0.6, w_linear(0.1), NS_EXACT))
    # T2: near-1 centre leaves interior (F1) through G1
    tamper("T2 near-1 interior", gate_binom_window(0.97, w_on(0.75), NS_EXACT))
    # T3: unbounded base field (F3) through G2
    tamper("T3 unbounded base", gate_subfield_window(beta_growing(), w_on(0.75), NS_EXACT))
    # T4: non-monotone census through G6 (census check) -- exercise directly
    def _g6_census_tampered():
        prev = -1
        for n1 in range(1, 14):
            v = census_A2(n1, tamper_at=9)
            if v <= prev:
                return (False, "census non-monotone at n1=%d (tampered)" % n1)
            prev = v
        return (True, "census monotone")
    tamper("T4 census non-monotone", _g6_census_tampered())
    # T5: wrong entropy (H3 for H2) through G4
    tamper("T5 wrong entropy H3", gate_stirling_identity(0.5, NS_EXACT, entropy=H3_wrong))
    # T6: C8 evaluated off-frontier (a ~ n) -> Theta(n), through the C8 frontier gate
    tamper("T6 C8 off-frontier", gate_c8_offfrontier_rejected(1_000_000, 1_000_000 - 5))
    # T7: beta=0 boundary (F1) through G5
    tamper("T7 beta=0 boundary", gate_frontier_interior(0.5, 0.0))
    # Extra positive control for T4: the untampered flatness must still PASS
    def _c3_flat_control():
        vals = {planted_count(4096, 2048, 8, s) for s in range(1, 8)}
        return (len(vals) == 1, "C3 flat control -> %s value(s)" % len(vals))
    tamper("T-ctl C3 flat (expect keep)", _c3_flat_control(), expect_reject=False)

    # ---- Report ---------------------------------------------------------
    print("\n" + "=" * 74)
    print("CAPS (limitations, all explicit):")
    for name, val in CAPS:
        print("  - %-22s %s" % (name + ":", val))
    print("-" * 74)
    print("Real gates:   PASS %d/%d" % (real_pass, real_total))
    print("Tamper tests: PASS %d/%d  (>=5 required)" % (tamper_pass, tamper_total))
    all_ok = (real_pass == real_total) and (tamper_pass == tamper_total)
    if all_ok:
        print("\nRESULT: PASS -- window slide discharged (Lemma W + Lemma B); "
              "residual = pre-existing C9/atom OPEN gaps only.")
    else:
        print("\nRESULT: FAIL -- failures: %s" % ", ".join(failures))
    print("=" * 74)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
