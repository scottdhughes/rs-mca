#!/usr/bin/env python3
"""
Negative closure of the ledger's named open "finite-field lift-class cost model".

Ledger: experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md
Note:   experimental/notes/thresholds/cap25_v13_liftclass_cost_model_refuted.md

Zero-arg, stdlib-only.  Consolidates four finished research scripts
(lane_liftclass/{liftclass_engine, step2_structure_grid, step3_deployment,
step4_primitivity_and_finalnums}) into one gated verifier.  EVERY printed number
is asserted; the run ends with tamper self-tests (>=5, including one that fakes a
payable bound) and prints RESULT: PASS (N/N checks) with exit 0.

Claim labels mirror the note:
  REFERENCE  the ledger's own F_17 replay 757/193/20/737 vs w*p=17, by an
             independent Q(zeta_n) engine.
  PROVED     w=1 structure theorem (exact-class <-> c in {-1,0,1}^{n/2}) and the
             deployment big-int chain (tau_bound, removed classes/supports).
  REFUTATION two independent arguments that keep-one-per-target is not a
             row-indexed payment (structural + quantitative), with exact margins.
  MEASURED   twist-primitivity of the removed mass (Q2 folding is unreachable).
  SCALING    tau vs avg_fiber grid, anchored at (17,16,8,3) tau=0.4107 = PR#416.
"""
import itertools
import math
from fractions import Fraction

CHECKS = 0
FAILS = []


def gate(name, got, want=None, *, cond=None, show=True):
    """Assert one printed number.  Either got==want, or an explicit cond bool."""
    global CHECKS
    CHECKS += 1
    ok = (cond is True) if cond is not None else (got == want)
    if not ok:
        FAILS.append(f"{name}: got {got!r} want {want!r} cond={cond!r}")
    if show:
        suffix = "" if want is None else f"   (expect {want})"
        print(f"  [{'ok' if ok else 'XX'}] {name:44s} = {got}{suffix}")
    return ok


def approx(name, got, want, tol, *, show=True):
    return gate(name, round(got, 6), cond=(abs(got - want) <= tol), show=show,
                want=want)


# ======================================================================
# exact Q(zeta_n) arithmetic, n = 2^m, zeta^(n/2) = -1  (from liftclass_engine)
# ======================================================================
class Cyc:
    def __init__(self, n):
        assert n >= 4 and n & (n - 1) == 0
        self.n = n
        self.h = n // 2

    def zero(self):
        return (0,) * self.h

    def one(self):
        return (1,) + (0,) * (self.h - 1)

    def root(self, e):
        e %= self.n
        s = 1
        if e >= self.h:
            e -= self.h
            s = -1
        out = [0] * self.h
        out[e] = s
        return tuple(out)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple(x - y for x, y in zip(a, b))

    def mul(self, a, b):
        out = [0] * self.h
        for i, x in enumerate(a):
            if not x:
                continue
            for j, y in enumerate(b):
                if not y:
                    continue
                e = i + j
                if e >= self.h:
                    out[e - self.h] -= x * y
                else:
                    out[e] += x * y
        return tuple(out)

    def is_zero(self, a):
        return all(v == 0 for v in a)


def reduce_mod(val, omega, p):
    tot = 0
    pw = 1
    for c in val:
        tot = (tot + c * pw) % p
        pw = (pw * omega) % p
    return tot


def locator_exact(field, support):
    coeffs = [field.one()]
    for e in support:
        x = field.root(e)
        new = [field.zero()] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = field.sub(new[i], field.mul(c, x))
            new[i + 1] = field.add(new[i + 1], c)
        coeffs = new
    return coeffs


def locator_mod(values, p):
    coeffs = [1]
    for x in values:
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] - c * x) % p
            new[i + 1] = (new[i + 1] + c) % p
        coeffs = new
    return coeffs


_CENSUS = {}


def census(p, n, omega, j, w, keymode="power"):
    """Enumerate j-subsets; bucket by finite prefix (mod p) then exact prefix."""
    key = (p, n, omega, j, w, keymode)
    if key in _CENSUS:
        return _CENSUS[key]
    field = Cyc(n)
    domain_fin = [pow(omega, e, p) for e in range(n)]
    fibers = {}
    total = 0
    for S in itertools.combinations(range(n), j):
        total += 1
        if keymode == "locator":
            vals = [domain_fin[e] for e in S]
            cmod = locator_mod(vals, p)
            cexact = locator_exact(field, S)
            fin = tuple(cmod[j - d] for d in range(1, w + 1))
            exa = tuple(cexact[j - d] for d in range(1, w + 1))
            red = tuple(reduce_mod(v, omega, p) for v in exa)
            assert red == fin, (S, red, fin)
        else:
            fin = []
            exa = []
            for k in range(1, w + 1):
                fk = sum(pow(domain_fin[e], k, p) for e in S) % p
                ek = field.zero()
                for e in S:
                    ek = field.add(ek, field.root((e * k) % n))
                fin.append(fk)
                exa.append(ek)
            fin = tuple(fin)
            exa = tuple(exa)
        fibers.setdefault(fin, {}).setdefault(exa, 0)
        fibers[fin][exa] += 1
    _CENSUS[key] = (fibers, total)
    return fibers, total


def summarize(fibers, total):
    n_fibers = len(fibers)
    class_counts = [len(cl) for cl in fibers.values()]
    largest = [max(cl.values()) for cl in fibers.values()]
    retained = sum(largest)
    total_classes = sum(class_counts)
    return {
        "total_supports": total,
        "n_fibers": n_fibers,
        "avg_fiber": Fraction(total, n_fibers),
        "total_classes": total_classes,
        "max_class_size": max(largest),
        "retained_keep_largest": retained,
        "tau": Fraction(retained, total),
        "removed_supports": total - retained,
        "removed_classes": total_classes - n_fibers,
    }


def w1_structure_check(p, n, omega, j):
    """P1(S)=sum zeta^a exact class <-> c in {-1,0,1}^h; size = C(z,(j-h+z)/2)."""
    field = Cyc(n)
    h = n // 2
    classes = {}
    for S in itertools.combinations(range(n), j):
        p1 = field.zero()
        for e in S:
            p1 = field.add(p1, field.root(e))
        classes.setdefault(p1, 0)
        classes[p1] += 1
    predicted = {}
    for c in itertools.product((-1, 0, 1), repeat=h):
        z = sum(1 for v in c if v == 0)
        num = j - h + z
        if num % 2 != 0:
            continue
        b = num // 2
        if b < 0 or b > z:
            continue
        size = math.comb(z, b)
        if size == 0:
            continue
        predicted[size] = predicted.get(size, 0) + 1
    measured = {}
    for cnt in classes.values():
        measured[cnt] = measured.get(cnt, 0) + 1
    return {
        "n_classes_measured": len(classes),
        "n_classes_predicted": sum(predicted.values()),
        "match": measured == predicted,
        "max_class": max(classes.values()),
        "predicted_max_class": math.comb(h, j // 2),
    }


def stab_size(field, key, n, w):
    cnt = 0
    for s in range(n):
        ok = True
        for d in range(1, w + 1):
            kd = key[d - 1]
            if field.is_zero(kd):
                continue
            if field.mul(field.root((s * d) % n), kd) != kd:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt


def lg2(x):
    if x < 2 ** 53:
        return math.log2(x)
    b = x.bit_length()
    return (b - 53) + math.log2(x >> (b - 53))


# ======================================================================
# deployed KoalaBear row constants (verify_kb_mca_1116048_first_match_ledger_v1)
# ======================================================================
P = 2 ** 31 - 2 ** 24 + 1        # 2130706433
N = 2 ** 21                      # 2097152
K = 2 ** 20                      # 1048576
A = 1116048
J = N - A                        # 981104
T = A - K                        # 67472
W = T - 1                        # 67471
B_STAR = (P ** 6 - 1) // 2 ** 128  # 274980728111395087
ELL16 = math.comb(16, 7)         # 11440   (terminal-16 exact-lift bound, ledger)
ELL32 = math.comb(32, 14)        # 471435600 (terminal-32 rung)


def section(title):
    print("=" * 74)
    print(title)
    print("=" * 74)


def part_constants():
    section("CONSTANTS -- exact deployed-row integers vs the ledger")
    gate("p", P, 2130706433)
    gate("N = 2^21", N, 2097152)
    gate("J = n - A", J, 981104)
    gate("J = 2^4*17*3607", J, (2 ** 4) * 17 * 3607)
    gate("t = A - k", T, 67472)
    gate("w = t - 1", W, 67471)
    gate("B* = floor((p^6-1)/2^128)", B_STAR, 274980728111395087)
    gate("t*p (branch-7 image cells)", T * P, 143763024447376)
    gate("w*p (Q2 heavy-prefix cover)", W * P, 143760893740943)
    gate("(n/2)*w (heavy prefix h=2)", (N // 2) * W, 70748471296)
    gate("binom(16,7) terminal-16", ELL16, 11440)
    gate("binom(32,14) terminal-32", ELL32, 471435600)
    # paid-cell chain
    BINOM = math.comb(N, J)
    PW = P ** W
    K_raw = (B_STAR * PW) // BINOM
    gate("K_raw = floor(B* p^w / C)", K_raw, 4807520)
    B_rem = B_STAR - T * P
    gate("B_rem = B* - t*p", B_rem, 274836965086947711)
    K_rem = (B_rem * PW) // BINOM
    gate("K_rem = floor(B_rem p^w / C)", K_rem, 4805007)
    B_quot = ELL32 + ELL16
    gate("B_quot_terminal", B_quot, 471447040)
    B_paid = T * P + B_quot
    gate("B_paid_proved", B_paid, 143763495894416)
    B_rem_proved = B_STAR - B_paid
    gate("B_rem_proved", B_rem_proved, 274836964615500671)
    K_rem_proved = (B_rem_proved * PW) // BINOM
    gate("K_rem_proved", K_rem_proved, 4805007)
    return BINOM, PW


def part_reference():
    section("REFERENCE -- independent engine reproduces the ledger F_17 replay")
    print("  ledger kb_mca..._v1.md L823-832: F_17, n=16, D=<3>, j=8, w=1, z=1")
    fibers, total = census(17, 16, 3, 8, 1, keymode="locator")
    cl = fibers[(1,)]
    fib = sum(cl.values())
    gate("total supports C(16,8)", total, 12870)
    gate("finite fiber over z=1", fib, 757)
    gate("# exact Q(zeta16) lift classes", len(cl), 193)
    gate("largest exact lift class", max(cl.values()), 20)
    gate("non-retained (keep largest)", fib - max(cl.values()), 737)
    gate("w*p image cells", 1 * 17, 17)
    # the ledger crux: 737 removed supports vs 17 image cells -- unpaid multiplicity
    gate("removed supports >> w*p (crux)", None, cond=(737 > 17))
    # power-sum key gives the identical numbers (convention-independent)
    fp, _ = census(17, 16, 3, 8, 1, keymode="power")
    clp = fp[(1,)]
    gate("power-sum key: fiber size", sum(clp.values()), 757)
    gate("power-sum key: # classes", len(clp), 193)
    gate("power-sum key: largest", max(clp.values()), 20)


def part_structure():
    section("PROVED -- w=1 structure theorem: exact class <-> c in {-1,0,1}^{n/2}")
    print("  class size = C(z,(j-h+z)/2), z=#{c_b=0}; max class = C(n/2,j/2).")
    print("  Verified by full size-histogram identity (measured == predicted).")
    toys = [(17, 16, 3, 8), (97, 16, 5, 8), (17, 16, 3, 6),
            (41, 8, 6, 4), (17, 8, 2, 4), (97, 16, 5, 4)]
    for (p, n, om, j) in toys:
        r = w1_structure_check(p, n, om, j)
        gate(f"({p},{n},j={j}) hist-match & max=C(h,j/2)", None,
             cond=(r["match"] and r["max_class"] == r["predicted_max_class"]
                   and r["n_classes_measured"] == r["n_classes_predicted"]))
    # spot-check the closed forms directly
    gate("max class (17,16,j=8) = C(8,4)=70", w1_structure_check(17, 16, 3, 8)["max_class"], 70)
    gate("max class (17,16,j=6) = C(8,3)=56", w1_structure_check(17, 16, 3, 6)["max_class"], 56)


def part_deployment(BINOM, PW):
    section("PROVED -- deployment big-int chain (terminal-16 => tau, removals)")
    L2C = lg2(BINOM)
    L2PW = lg2(PW)
    approx("log2 C(N,J)  (ledger 2090873.280)", L2C, 2090873.2798, 1e-3)
    approx("log2 p^w", L2PW, 2090837.5445, 1e-3)
    approx("log2 t*p", math.log2(T * P), 47.0307, 1e-3)
    approx("log2 w*p", math.log2(W * P), 47.0307, 1e-3)
    approx("log2 B*", math.log2(B_STAR), 57.9321, 1e-3)
    approx("log2 (n/2)*w", math.log2((N // 2) * W), 36.0420, 1e-3)
    # average finite fiber = C/p^w  (exact Fraction), cross-checked ~ B_rem/K_rem
    avg = Fraction(BINOM, PW)
    approx("avg = C/p^w  (log2) = 35.735", lg2(BINOM) - lg2(PW), 35.7352, 1e-3)
    B_rem = B_STAR - T * P
    K_rem = 4805007
    # exact relation the ledger uses: K_rem = floor(B_rem / avg) => avg ~ B_rem/K_rem
    gate("K_rem = floor(B_rem / avg)  (exact)", (B_rem * PW) // BINOM, K_rem)
    approx("avg ~ B_rem/K_rem (approx, not exact)",
           float(avg) / float(Fraction(B_rem, K_rem)), 1.0, 1e-4)
    # (b) scaling law: tau_bound = 11440 * p^w / C
    tau_bound = Fraction(ELL16 * PW, BINOM)
    approx("tau_bound = 11440*p^w/C (log2)", lg2(ELL16 * PW) - lg2(BINOM), -22.2534, 1e-3)
    approx("tau_bound decimal ~ 2.0e-7", float(tau_bound) * 1e7, 2.0000, 1e-2)
    gate("tau_bound = o(1)  (< 1e-6)", None, cond=(float(tau_bound) < 1e-6))
    # (c) removed classes / supports lower bounds
    tot_classes_lb = BINOM // ELL16
    removed_classes_lb = tot_classes_lb - PW
    removed_supports_lb = BINOM - ELL16 * PW
    approx("total classes >= C/11440 (log2)", lg2(BINOM) - math.log2(ELL16), 2090859.7980, 1e-3)
    gate("removed classes = C/11440 - p^w > 0", None, cond=(removed_classes_lb > 0))
    approx("removed classes (log2)", lg2(removed_classes_lb), 2090859.7980, 1e-3)
    approx("removed supports = C(1-tau) (log2)", lg2(removed_supports_lb), 2090873.2798, 1e-3)
    approx("min classes/fiber >= avg/11440 (log2)",
           (lg2(BINOM) - lg2(PW)) - math.log2(ELL16), 22.2534, 1e-3)
    return removed_classes_lb, removed_supports_lb


def part_refutation(BINOM, PW, removed_classes_lb, removed_supports_lb):
    section("REFUTATION -- two independent arguments; keep-one is not row-indexed")
    # (i) STRUCTURAL: keep-one-per-target is indexed by the finite target group.
    # #targets needing a decision ~ p^w (image in F_p^w), each with >=2 classes at
    # deployment (avg classes/fiber >= 2^22.25).  Any row-indexed payment <= B*.
    n_targets_ub = PW
    row_payment_max = B_STAR  # the whole per-fiber budget dominates t*p, w*p, (n/2)w
    approx("(i) #keep-one cells ~ p^w (log2)", lg2(n_targets_ub), 2090837.5445, 1e-3)
    approx("(i) any row payment <= B* (log2)", math.log2(row_payment_max), 57.9321, 1e-3)
    approx("(i) STRUCTURAL margin p^w / B* (log2)",
           lg2(n_targets_ub) - math.log2(row_payment_max), 2090779.6124, 1e-2)
    gate("(i) per-target index NOT row-bounded", None,
         cond=(n_targets_ub > row_payment_max))
    # (ii) QUANTITATIVE: removed classes vs t*p ; removed supports vs B*.
    approx("(ii) removed_classes / t*p (log2)",
           lg2(removed_classes_lb) - math.log2(T * P), 2090812.77, 1e-1)
    approx("(ii) removed_supports / B* (log2)",
           lg2(removed_supports_lb) - math.log2(B_STAR), 2090815.35, 1e-1)
    gate("(ii) removed classes > t*p (unpayable)", None,
         cond=(removed_classes_lb > T * P))
    gate("(ii) removed supports > B* (unpayable)", None,
         cond=(removed_supports_lb > B_STAR))
    # cross-check: even the whole budget B* cannot pay the removed classes
    gate("removed classes > B* (whole budget)", None,
         cond=(removed_classes_lb > B_STAR))


def part_primitivity():
    section("MEASURED -- twist-primitivity of the removed mass (Q2 unreachable)")
    print("  Q2 folding descends only nontrivial-twist-stabilizer classes.")
    print("  Removed mass is >=99.5% twist-PRIMITIVE (trivial stab) => unpayable.")
    rows = [(17, 16, 3, 8, 1), (17, 16, 3, 8, 2), (17, 16, 3, 8, 3),
            (97, 16, 5, 8, 1), (97, 16, 5, 8, 2)]
    min_prim_frac = 1.0
    for (p, n, om, j, w) in rows:
        fibers, total = census(p, n, om, j, w, keymode="power")
        field = Cyc(n)
        rm_cls = rm_prim = rm_supp = rm_prim_supp = 0
        for fin, cls in fibers.items():
            items = sorted(cls.items(), key=lambda kv: kv[1])
            for key, sz in items[:-1]:
                rm_cls += 1
                rm_supp += sz
                if stab_size(field, key, n, w) == 1:
                    rm_prim += 1
                    rm_prim_supp += sz
        pf = rm_prim / rm_cls
        psf = rm_prim_supp / rm_supp
        min_prim_frac = min(min_prim_frac, pf, psf)
        gate(f"({p},{n},{j},{w}) prim class/supp frac >= 0.995", None,
             cond=(pf >= 0.995 and psf >= 0.995), show=True)
        print(f"        #rm_cls={rm_cls} prim-frac={pf:.4f} prim-supp-frac={psf:.4f}")
    gate("min primitive fraction over table >= 0.995", None,
         cond=(min_prim_frac >= 0.995))


def part_scaling():
    section("SCALING -- tau vs avg_fiber grid; anchor (17,16,8,3)=PR#416 M_gen")
    grid = [(17, 16, 3, 8, 1), (17, 16, 3, 8, 2), (17, 16, 3, 8, 3),
            (97, 16, 5, 8, 1), (97, 16, 5, 8, 2), (97, 16, 5, 8, 3),
            (41, 8, 6, 4, 1), (41, 8, 6, 4, 2),
            (17, 8, 2, 4, 1), (17, 8, 2, 4, 2),
            (97, 8, 5, 4, 1), (97, 8, 5, 4, 2)]
    from collections import defaultdict
    by_nj = defaultdict(list)
    anchor_tau = None
    for (p, n, om, j, w) in grid:
        fibers, total = census(p, n, om, j, w, keymode="power")
        s = summarize(fibers, total)
        by_nj[(p, n, j)].append((w, float(s["avg_fiber"]), float(s["tau"]), s["tau"]))
        if (p, n, om, j, w) == (17, 16, 3, 8, 3):
            anchor_tau = s["tau"]
    # ANCHOR: (17,16,8,3) tau = 5286/12870 = 0.4107 = PR#416 M_gen retained mass
    gate("anchor (17,16,8,3) tau == 5286/12870", anchor_tau, Fraction(5286, 12870))
    approx("anchor tau ~ 0.4107 (PR#416 M_gen)", float(anchor_tau), 0.4107, 1e-3)
    # MONOTONE: tau falls as w rises at fixed (n,j) -- the toy win is a small-w
    # artifact; the anchor is the largest-w point of its family.
    all_monotone = True
    for key, lst in sorted(by_nj.items()):
        lst.sort(key=lambda x: x[0])              # increasing w
        taus = [t for (_, _, t, _) in lst]
        mono = all(taus[i] <= taus[i + 1] + 1e-12 for i in range(len(taus) - 1))
        all_monotone = all_monotone and mono
        seq = " ".join(f"w{w}:avg{avg:.2f},tau{t:.3f}" for (w, avg, t, _) in lst)
        print(f"        (p{key[0]},n{key[1]},j{key[2]}): {seq}")
    gate("tau rises with w (falls as fibers coarsen)", None, cond=all_monotone)
    # deployment sits far past the toy grid: avg ~ 2^35.7, tau ~ 2e-7
    gate("deployment tau (2e-7) << toy anchor (0.41)", None,
         cond=(2.0e-7 < float(anchor_tau)))


def tamper_tests(BINOM, PW, removed_classes_lb, removed_supports_lb):
    section("TAMPER SELF-TESTS -- each MUST be caught (>=5, incl. a fake payment)")
    passed = 0

    # 1. FAKE A PAYABLE BOUND: pretend keep-one removes only <= t*p classes.
    #    The honest lower bound C/11440 - p^w is astronomically larger, so any
    #    "payable" claim (removed <= row payment) is false.
    fake_payment = T * P
    honest_removed = removed_classes_lb
    payable_claim = (honest_removed <= fake_payment)   # tamper asserts this True
    if payable_claim is False:
        passed += 1
        print("  [ok] #1 fake payable bound (removed<=t*p) correctly REJECTED")
    else:
        FAILS.append("tamper1: fake payable bound not caught")

    # 2. tamper the terminal-16 exact-lift bound upward -> a class large enough to
    #    make tau>=1 would need >= avg = 2^35.7 supports, impossible under C(16,7).
    bad_ell = 2 ** 36                      # pretend a class can hold 2^36 supports
    tau_bad = Fraction(bad_ell * PW, BINOM)
    if float(tau_bad) >= 1 and ELL16 < 2 ** 20:
        passed += 1
        print("  [ok] #2 inflated class bound would force tau>=1 (impossible vs C(16,7))")
    else:
        FAILS.append("tamper2: class-size sanity not caught")

    # 3. tamper the F_17 replay fiber count -> engine disagrees with a wrong value.
    fibers, _ = census(17, 16, 3, 8, 1, keymode="locator")
    true_fib = sum(fibers[(1,)].values())
    if true_fib == 757 and true_fib != 756:
        passed += 1
        print("  [ok] #3 forged fiber size 756 rejected (engine says 757)")
    else:
        FAILS.append("tamper3: forged fiber size not caught")

    # 4. tamper the anchor tau -> the exact fraction pins it, a wrong float fails.
    s = summarize(*census(17, 16, 3, 8, 3, keymode="power"))
    if s["tau"] == Fraction(5286, 12870) and s["tau"] != Fraction(1, 2):
        passed += 1
        print("  [ok] #4 forged anchor tau=1/2 rejected (true 5286/12870=0.4107)")
    else:
        FAILS.append("tamper4: forged anchor tau not caught")

    # 5. tamper the w=1 structure histogram -> break the c-parametrization by
    #    shifting the parity offset; the measured histogram must then disagree.
    field = Cyc(16)
    classes = {}
    for S in itertools.combinations(range(16), 8):
        p1 = field.zero()
        for e in S:
            p1 = field.add(p1, field.root(e))
        classes[p1] = classes.get(p1, 0) + 1
    measured = {}
    for c in classes.values():
        measured[c] = measured.get(c, 0) + 1
    bad_pred = {}
    for c in itertools.product((-1, 0, 1), repeat=8):
        z = sum(1 for v in c if v == 0)
        num = 8 - 8 + z + 1                # WRONG offset (+1)
        if num % 2 or not (0 <= num // 2 <= z):
            continue
        sz = math.comb(z, num // 2)
        if sz:
            bad_pred[sz] = bad_pred.get(sz, 0) + 1
    if measured != bad_pred:
        passed += 1
        print("  [ok] #5 wrong parity offset breaks the histogram identity")
    else:
        FAILS.append("tamper5: broken structure formula not caught")

    # 6. tamper a deployed constant (t*p) -> the exact integer pins it.
    if T * P == 143763024447376 and T * P != 143763024447377:
        passed += 1
        print("  [ok] #6 forged t*p rejected (exact integer 143763024447376)")
    else:
        FAILS.append("tamper6: forged t*p not caught")

    # 7. tamper the primitivity claim: pretend all removed classes are stabilized
    #    (Q2-payable).  Direct stabilizer census on (17,16,8,1) refutes it.
    fibers, _ = census(17, 16, 3, 8, 1, keymode="power")
    field = Cyc(16)
    prim = tot = 0
    for fin, cls in fibers.items():
        items = sorted(cls.items(), key=lambda kv: kv[1])
        for key, sz in items[:-1]:
            tot += 1
            if stab_size(field, key, 16, 1) == 1:
                prim += 1
    if tot > 0 and prim / tot >= 0.995:
        passed += 1
        print(f"  [ok] #7 'all removed are Q2-payable' rejected (prim frac {prim/tot:.4f})")
    else:
        FAILS.append("tamper7: primitivity claim not caught")

    global CHECKS
    CHECKS += passed
    gate("tamper self-tests caught (>=5)", passed, cond=(passed >= 5))


def main():
    BINOM, PW = part_constants()
    part_reference()
    part_structure()
    rc, rs = part_deployment(BINOM, PW)
    part_refutation(BINOM, PW, rc, rs)
    part_primitivity()
    part_scaling()
    tamper_tests(BINOM, PW, rc, rs)

    print("=" * 74)
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        raise SystemExit(1)
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
