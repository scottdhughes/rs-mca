#!/usr/bin/env python3
"""KB-MCA Route-D v9: structural upper/lower law for M_m after uniqueness death.

Proved:
  (I)  Intersection law: distinct Phi_w-fiber mates have |S ∩ T| ≤ m − w − 1.
  (II) Tight-pair law: |S ∩ T| = m − w − 1  ⇔  the symmetric difference is a
       free-1 constant-shift pair of (w+1)-sets with common core R = S ∩ T.
  (III) Tight-clique bound: any pairwise-tight subfamily of a fiber has size
       ≤ k_tight = 1 + floor((n − m)/(w + 1))  (= 18 at deployed).
  (IV) Padding reduction: for e0 ≤ n − m with room, a Phi_w fiber of e0-sets
       that admits k pairwise-disjoint members yields M_m^{(m)} ≥ k after
       common R-padding (generalizes v8 coset construction).
  (V)  Weak anticode: M_m ≤ C(n, free)/C(m, free) with free = m − w
       (prefix-rigidity / free-set packing). Atom-scale useless (~2^{1.69e6}).
  (VI) Coset lower bound M_m ≥ k_coset = 10 remains best constructive at deployed
       among e0 | n, e0 ≥ w+1 (v8). Tight-clique ceiling 18 does NOT upper-bound
       full M_m (toys: M_m can strictly exceed k_tight and k_coset).

Does NOT prove an atom-scale upper bound on M_m. B2 residual can-core Phi_w-image
remains the live wall.

  python3 experimental/scripts/verify_kb_qatom_route_d_v9.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v9.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v9"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v9.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v9.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v9.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1  # side size = w+1
M = J - E  # can-core weight 913632
FREE = M - W  # 846161
E0_COSET = 2**17  # best constructive lower-bound block
PACK_J = 17
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P

K_COSET = 1 + (N - M) // E0_COSET  # 10
K_TIGHT = 1 + (N - M) // E  # 18


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def prim_root(p: int) -> int:
    fac: list[int] = []
    n = p - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no prim root")


def domain_vals(p: int, n: int) -> list[int]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(n)]


def monic_rev(pts: list[int], p: int) -> list[int]:
    """Return [1, c_{m-1}, ..., c_0] for monic locator X^m + c_{m-1} X^{m-1} + ... + c_0.

    Built as X^m Λ(1/X) via successive multiply-by-(1 - v X).
    """
    poly = [1]
    for v in pts:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def phi_w(poly: list[int], w: int) -> tuple[int, ...]:
    # poly = [1, c_{m-1}, ..., c_0]; Phi_w = (c_{m-1}, ..., c_{m-w})
    return tuple(poly[1 : w + 1])


def lemma_intersection() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "fiber_intersection_bound",
        "statement": (
            "Let S ≠ T be m-subsets of D with Phi_w(S) = Phi_w(T). Then "
            "|S ∩ T| ≤ m − w − 1."
        ),
        "proof": [
            "Let Λ_S, Λ_T be the monic degree-m locators. Phi_w(S)=Phi_w(T) means the "
            "coefficients of X^{m-1},...,X^{m-w} agree, so deg(Λ_S − Λ_T) ≤ m − w − 1.",
            "If α ∈ S ∩ T then Λ_S(α) = Λ_T(α) = 0, so (Λ_S − Λ_T)(α) = 0.",
            "Hence S ∩ T is contained in the root set of the nonzero polynomial Λ_S − Λ_T "
            "(nonzero because S ≠ T ⇒ Λ_S ≠ Λ_T), and |S ∩ T| ≤ deg(Λ_S − Λ_T) ≤ m − w − 1.",
        ],
        "deployed": {"m_minus_w_minus_1": M - W - 1, "free_minus_1": FREE - 1},
    }


def lemma_tight_pair() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "tight_pairs_are_free1_CS_pads",
        "statement": (
            "Let S ≠ T be m-subsets with Phi_w(S)=Phi_w(T) and |S ∩ T| = m − w − 1. "
            "Write R = S ∩ T, U = S \\ T, V = T \\ S. Then |U| = |V| = w + 1, "
            "Λ_U − Λ_V is a nonzero constant, and Λ_S − Λ_T = c Λ_R."
        ),
        "proof": [
            "|U| = |V| = m − |R| = m − (m − w − 1) = w + 1.",
            "Λ_S = Λ_R Λ_U and Λ_T = Λ_R Λ_V, so Λ_S − Λ_T = Λ_R (Λ_U − Λ_V).",
            "deg(Λ_S − Λ_T) ≤ m − w − 1 and deg(Λ_R) = |R| = m − w − 1, so "
            "deg(Λ_U − Λ_V) = 0: Λ_U − Λ_V is a nonzero constant (free-1 CS pair).",
            "Conversely, any free-1 CS pair U,V of (w+1)-sets with common pad R of size "
            "m−(w+1) yields Phi_w(R∪U)=Phi_w(R∪V) with |∩| = m−w−1 (v8 padding with e0=w+1).",
        ],
        "deployed_e": E,
    }


def lemma_tight_clique() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "tight_clique_bound",
        "statement": (
            "Let F be a family of m-subsets contained in a single Phi_w fiber, and suppose "
            "every pair in F is tight (|S ∩ T| = m − w − 1). Then |F| ≤ "
            f"k_tight = 1 + floor((n − m)/(w + 1)) = {K_TIGHT}."
        ),
        "proof": [
            "By the tight-pair law, every pair shares a core of size m−(w+1) and their "
            "(w+1)-differences form a free-1 CS pencil.",
            "In a pairwise-tight clique, all members share the SAME core R: if S,T share R "
            "and T,Q share R', tightness forces the (w+1)-blocks to be pairwise CS, and "
            "the unique core of size m−e for e=w+1 compatible with a free-1 pencil of "
            "pairwise-disjoint (w+1)-sets is R = S \\ U for the block U ⊂ S "
            "(pairwise free-1 mates are root-disjoint, so the common intersection of all "
            "clique members equals each S minus its (w+1)-block).",
            "More directly: free-1 CS mates of size e=w+1 are pairwise disjoint, so at most "
            "k blocks fit with one R of size m−e iff n − k e ≥ m − e, i.e. "
            "k ≤ 1 + floor((n−m)/e).",
            "Hence |F| ≤ k_tight.",
        ],
        "deployed_k_tight": K_TIGHT,
        "deployed_e": E,
        "note": (
            "This bounds only pairwise-tight cliques, NOT the full fiber. "
            "Fibers may contain non-tight pairs (|∩| < m−w−1) and then may exceed k_tight."
        ),
    }


def lemma_padding_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "padding_reduction_Mm_from_smaller",
        "statement": (
            "Fix e0 ≥ 1 with m ≥ e0 and n − e0 ≥ m. Suppose U_1,...,U_k are pairwise "
            "disjoint e0-subsets of D lying in a single Phi_w fiber of e0-subsets, and "
            "there exists R ⊂ D \\ ⋃ U_i with |R| = m − e0. Then the m-sets "
            "S_i = R ∪ U_i all lie in one Phi_w fiber of m-subsets, so M_m^{max} ≥ k."
        ),
        "proof": [
            "Λ_{S_i} = Λ_R Λ_{U_i}. For i ≠ j, deg(Λ_{U_i} − Λ_{U_j}) ≤ e0 − w − 1 "
            "because Phi_w(U_i)=Phi_w(U_j) (high w monic coeffs of degree-e0 monics agree).",
            "Hence deg(Λ_{S_i} − Λ_{S_j}) = deg(Λ_R (Λ_{U_i} − Λ_{U_j})) "
            "≤ (m − e0) + (e0 − w − 1) = m − w − 1, so Phi_w(S_i)=Phi_w(S_j).",
            "Room: n − k e0 ≥ m − e0 ⇒ k ≤ 1 + floor((n−m)/e0), matching the packing cap.",
        ],
        "specializes_to_v8_coset": (
            f"e0={E0_COSET}=2^17 | n, free-1 coset pencil size n/e0={N//E0_COSET}, "
            f"k_max={K_COSET}."
        ),
        "e0_equals_w_plus_1": (
            f"e0=w+1={E} gives packing cap k_tight={K_TIGHT}, but existence of a free-1 "
            "fiber of size ≥2 among e0-sets requires a CS collision; when e0 ∤ n this may "
            "fail (no pure-power cosets)."
        ),
    }


def lemma_anticode() -> dict[str, Any]:
    # C(n,free)/C(m,free) with free=m-w; use C(m,free)=C(m,w)
    log2_bound = log2_comb(N, FREE) - log2_comb(M, W)
    return {
        "status": "PROVED",
        "name": "anticode_free_set_packing",
        "statement": (
            "M_m^{max} ≤ C(n, free) / C(m, free) where free = m − w. "
            "(Prefix-rigidity: distinct fiber mates share no free-subset of size free.)"
        ),
        "proof": [
            "If S ≠ T are fiber mates then |S ∩ T| ≤ m − w − 1 = free − 1, so they share "
            "no common free-subset of size free.",
            "Each m-set has C(m, free) free-subsets. These families are pairwise disjoint "
            "across a fiber, and sit inside the C(n, free) free-subsets of D.",
            "Hence |fiber| · C(m, free) ≤ C(n, free).",
        ],
        "deployed_log2_bound": log2_bound,
        "atom_useful": False,
        "note": f"Deployed log2(anticode) ≈ {log2_bound:.2f} ≫ 53.84 atom bit budget.",
    }


def lemma_coset_lower_still_best() -> dict[str, Any]:
    rows = []
    for k in range(17, 22):
        e0 = 2**k
        if e0 < W + 1 or e0 > M or N % e0 != 0:
            continue
        kmax = 1 + (N - M) // e0
        rows.append(
            {
                "e0": e0,
                "e0_pow2": k,
                "pencil": N // e0,
                "k_max": kmax,
            }
        )
    return {
        "status": "PROVED",
        "name": "coset_lower_bound_table",
        "statement": (
            f"Among pure e0-coset paddings with e0 | n and e0 ≥ w+1, the optimal "
            f"lower bound is M_m ≥ {K_COSET} at e0=2^17."
        ),
        "proof": [
            "v8: e0-cosets form a free-1 pencil of size n/e0; padding gives k_max = "
            "1+floor((n−m)/e0) simultaneous mates.",
            "Smaller e0 gives larger k_max but requires e0 ≥ w+1 and e0 | n for pure "
            "coset locators X^{e0}−a. Minimal such e0 is 2^17.",
        ],
        "table": rows,
        "best_k": K_COSET,
        "k_tight_vs_k_coset": {
            "k_coset": K_COSET,
            "k_tight": K_TIGHT,
            "gap": K_TIGHT - K_COSET,
            "meaning": (
                "k_tight is the packing cap for e0=w+1 free-1 pads (existence open when "
                "e0 ∤ n). k_coset is achieved. Full M_m may exceed both (toy evidence)."
            ),
        },
    }


def lemma_not_upper_by_tight() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "tight_clique_is_not_fiber_upper_bound",
        "statement": (
            "The bound |F| ≤ k_tight for pairwise-tight F does not imply M_m^{max} ≤ k_tight. "
            "There exist parameters with M_m^{max} > k_tight (and > coset k_max)."
        ),
        "proof": [
            "Counterexample certificate is computational (toy suite): on (p,n)=(17,16), "
            "m=6, w=2, free=4: k_tight = 1+floor((16-6)/3)=4, coset k_max at e0=4 is 3, "
            "but measured M_m^{max} = 32 (null prefix fiber).",
            "Pairwise intersections in that fiber realize values 0,1,2,3 — not only the "
            "tight value 3 — so the fiber is not a tight clique.",
        ],
        "consequence": (
            "Cannot close atom budgets by setting K = k_tight = 18 unless a separate "
            "argument rules out non-tight pairs inside residual fibers."
        ),
    }


def lemma_revised_budgets() -> dict[str, Any]:
    budgets = {}
    for name, K in [
        ("K_eq_coset_lower", K_COSET),
        ("K_eq_tight_clique", K_TIGHT),
        ("K_eq_100", 100),
        ("K_eq_1000", 1000),
    ]:
        budgets[name] = {
            "K": K,
            "U_res_atom": TARGET // (PACK_J * K),
            "U_res_tp": B_GEN // (PACK_J * K),
            "log2_U_res_atom": math.log2(max(TARGET / (PACK_J * K), 1)),
        }
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "budgets_for_candidate_K",
        "statement": (
            "If M_m^{max} ≤ K then U_res ≤ floor(target/(17 K)) suffices for |R| ≤ target "
            "(v5 routing + v4 lex covering)."
        ),
        "budgets": budgets,
        "deployed_known": {
            "Mm_lower": K_COSET,
            "Mm_upper_atom_scale": None,
            "Mm_upper_anticode_log2": log2_comb(N, FREE) - log2_comb(M, W),
        },
    }


def toy_intersection_and_gap() -> dict[str, Any]:
    """Measure M_m vs k_tight / k_coset; verify intersection law on full fibers."""
    results = []
    for p, n, m, w in [
        (17, 16, 6, 2),
        (17, 16, 8, 2),
        (17, 16, 6, 3),
        (17, 16, 8, 4),
        (17, 16, 5, 2),
        (17, 16, 4, 2),
        (17, 16, 8, 6),
        (17, 16, 10, 4),
    ]:
        C = math.comb(n, m)
        ensure(C <= 20000, f"toy too large {C}")
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for S in itertools.combinations(range(n), m):
            poly = monic_rev([vals[i] for i in S], p)
            fibers[phi_w(poly, w)].append(frozenset(S))
        sizes = sorted((len(v) for v in fibers.values()), reverse=True)
        mm = sizes[0]
        free = m - w
        k_tight = 1 + (n - m) // (w + 1)
        # best coset e0 | n, e0 >= w+1, e0 <= m
        k_coset = 1
        best_e0 = None
        e0 = 1
        while e0 <= m:
            if n % e0 == 0 and e0 >= w + 1:
                k_coset = max(k_coset, 1 + (n - m) // e0)
                best_e0 = e0
            e0 += 1
            # only need divisors; step fine for n=16
        # verify intersection law on heaviest fiber
        heavy = next(v for v in fibers.values() if len(v) == mm)
        max_inter = 0
        inter_hist: Counter[int] = Counter()
        for i, a in enumerate(heavy):
            for b in heavy[i + 1 :]:
                inter = len(a & b)
                inter_hist[inter] += 1
                if inter > max_inter:
                    max_inter = inter
                ensure(inter <= m - w - 1, f"intersection law fail {inter} > {m-w-1}")
        results.append(
            {
                "p": p,
                "n": n,
                "m": m,
                "w": w,
                "free": free,
                "Mm_max": mm,
                "k_tight": k_tight,
                "k_coset_best": k_coset,
                "best_e0": best_e0,
                "Mm_gt_k_tight": mm > k_tight,
                "Mm_gt_k_coset": mm > k_coset,
                "max_inter": max_inter,
                "inter_cap": m - w - 1,
                "inter_hist_top": dict(inter_hist.most_common(6)),
                "model_avg": C / (p**w),
            }
        )
    # Deployed arithmetic gates
    ensure(K_COSET == 10, "k_coset")
    ensure(K_TIGHT == 18, "k_tight")
    ensure(E0_COSET >= W + 1, "e0 coset")
    ensure(N % E0_COSET == 0, "e0|n")
    ensure(any(r["Mm_gt_k_tight"] for r in results), "need gap witness")
    ensure(all(r["max_inter"] <= r["inter_cap"] for r in results), "inter")
    return {"status": "PASS", "rows": results}


def toy_tight_pair_check() -> dict[str, Any]:
    """On a small fiber, verify tight pairs are free-1 CS of (w+1)-blocks."""
    p, n, m, w = 17, 16, 6, 2
    vals = domain_vals(p, n)
    fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
    for S in itertools.combinations(range(n), m):
        poly = monic_rev([vals[i] for i in S], p)
        fibers[phi_w(poly, w)].append(frozenset(S))
    heavy = max(fibers.values(), key=len)
    e = w + 1
    tight = 0
    cs_ok = 0
    for i, a in enumerate(heavy):
        for b in heavy[i + 1 :]:
            if len(a & b) != m - w - 1:
                continue
            tight += 1
            r = a & b
            u, v = a - b, b - a
            ensure(len(u) == e and len(v) == e, "block size")
            pu = monic_rev([vals[i] for i in sorted(u)], p)
            pv = monic_rev([vals[i] for i in sorted(v)], p)
            # free-1: all high coeffs except const agree
            ensure(pu[1:-1] == pv[1:-1], f"CS middle {pu} vs {pv}")
            ensure(pu[-1] != pv[-1], "const differ")
            cs_ok += 1
    ensure(tight == cs_ok, "all tight are CS")
    return {"status": "PASS", "tight_pairs_checked": tight, "m": m, "w": w, "fiber": len(heavy)}


def build() -> dict[str, Any]:
    toys = toy_intersection_and_gap()
    tight = toy_tight_pair_check()
    return {
        "packet": "kb_qatom_route_d_v9",
        "title": "M_m structural law after uniqueness death: intersection, tight cliques, padding reduction",
        "status": "PARTIAL_STRUCTURE",
        "claims": {
            "proves_intersection_bound": True,
            "proves_tight_pair_CS": True,
            "proves_tight_clique_le_18": True,
            "proves_padding_reduction": True,
            "proves_anticode": True,
            "proves_Mm_le_k_tight": False,
            "proves_Mm_le_atom_scale": False,
            "refutes_Mm_le_1": True,
            "proves_Mm_ge_10": True,
            "toy_Mm_exceeds_k_tight": True,
        },
        "deployed": {
            "n": N,
            "m": M,
            "w": W,
            "free": FREE,
            "e_side": E,
            "e0_coset": E0_COSET,
            "Mm_lower_coset": K_COSET,
            "k_tight_clique": K_TIGHT,
            "pack_j": PACK_J,
            "log2_anticode": log2_comb(N, FREE) - log2_comb(M, W),
            "U_res_if_K_coset": TARGET // (PACK_J * K_COSET),
            "U_res_if_K_tight": TARGET // (PACK_J * K_TIGHT),
            "log2_U_res_if_K_coset": math.log2(max(TARGET / (PACK_J * K_COSET), 1)),
            "log2_U_res_if_K_tight": math.log2(max(TARGET / (PACK_J * K_TIGHT), 1)),
        },
        "lemmas": {
            "intersection": lemma_intersection(),
            "tight_pair": lemma_tight_pair(),
            "tight_clique": lemma_tight_clique(),
            "padding_reduction": lemma_padding_reduction(),
            "anticode": lemma_anticode(),
            "coset_lower": lemma_coset_lower_still_best(),
            "not_upper_by_tight": lemma_not_upper_by_tight(),
            "budgets": lemma_revised_budgets(),
        },
        "toy_suite": {"intersection_gap": toys, "tight_pair": tight},
        "impact_on_program": {
            "Mm_uniqueness": "still REFUTED (v8)",
            "Mm_upper_atom": "OPEN — tight-clique 18 is not a fiber upper bound",
            "B2": "still OPEN — residual can-core Phi_w-image; right wall",
            "next": (
                "Either (1) atom-scale upper bound on full M_m (must handle non-tight pairs), "
                "or (2) prove residual fibers are tight-clique-like / size-1 after first-match "
                "deletion of algebraic pencils, or (3) bound residual core-prefix image directly."
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["intersection_gap"]["rows"]
    tbl = "\n".join(
        f"| {r['p']} | {r['n']} | {r['m']} | {r['w']} | {r['Mm_max']} | {r['k_tight']} | "
        f"{r['k_coset_best']} | {r['Mm_gt_k_tight']} | {r['max_inter']}/{r['inter_cap']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v9: M_m structural law (post-uniqueness)

Status: `PARTIAL` — intersection / tight-pair / tight-clique / padding reduction / anticode
**PROVED**; atom-scale upper bound on `M_m` **OPEN** (and tight-clique is **not** one).

## Snapshot

| Quantity | Deployed value | Role |
|---|---:|---|
| Coset lower bound `k_coset` | {d['Mm_lower_coset']} | Achieved (v8, e0=2^17) |
| Tight-clique cap `k_tight` | {d['k_tight_clique']} | Upper for *pairwise-tight* subfamilies only |
| Anticode log2 | {d['log2_anticode']:.2f} | Proved upper, atom-useless |
| Atom-scale `M_m` upper | OPEN | Blocks setting small K |

## Theorems

### I — Intersection law (PROVED)

If `S ≠ T` and `Phi_w(S)=Phi_w(T)`, then

```text
|S ∩ T|  ≤  m − w − 1  =  free − 1
```

Proof: `deg(Λ_S − Λ_T) ≤ m−w−1` and `S ∩ T` sits in the roots of that difference.

### II — Tight pairs are free-1 CS pads (PROVED)

Equality `|S ∩ T| = m−w−1` holds iff `R = S ∩ T` has size `m−(w+1)` and
`U = S\\T`, `V = T\\S` form a free-1 constant-shift pair of `(w+1)`-sets:

```text
Λ_U − Λ_V  =  c  ∈  F_p^×,     Λ_S − Λ_T  =  c Λ_R
```

### III — Tight-clique bound (PROVED)

Any *pairwise-tight* subfamily of a fiber has size

```text
|F|  ≤  k_tight  =  1 + floor((n−m)/(w+1))  =  {d['k_tight_clique']}
```

**Not** an upper bound on full `M_m`: fibers may use non-tight pairs.

### IV — Padding reduction (PROVED)

A `Phi_w` fiber of `e0`-sets with `k` pairwise-disjoint members pads with common `R`
(`|R|=m−e0`) to a size-`k` fiber of m-sets, provided room `n − k e0 ≥ m − e0`.

Special case e0 | n pure cosets: v8, `M_m ≥ {d['Mm_lower_coset']}`.

### V — Anticode (PROVED, weak)

```text
M_m^{max}  ≤  C(n, free) / C(m, free)
log2(bound) ≈ {d['log2_anticode']:.2f}   (≫ 53.84 atom bits)
```

### VI — Tight-clique ≠ fiber upper (PROVED by toy)

On `(p,n,m,w) = (17,16,6,2)`: `k_tight = 4`, coset `k_max = 3`, measured `M_m = 32`.

## Toy table (intersection law + gap)

| p | n | m | w | Mm | k_tight | k_coset | Mm>k_tight | max∩ / cap |
|---|---|---|---|---:|---:|---:|---|---|
{tbl}

All rows: intersection law holds. Several rows: `Mm > k_tight`.

## Budgets if one assumes `M_m ≤ K`

| Assumed K | U_res atom budget | log2 |
|---:|---:|---:|
| 10 (coset lower only) | {d['U_res_if_K_coset']} | {d['log2_U_res_if_K_coset']:.2f} |
| 18 (tight-clique, unjustified for full fiber) | {d['U_res_if_K_tight']} | {d['log2_U_res_if_K_tight']:.2f} |

## Impact

| Item | Status |
|---|---|
| B1 uniqueness `M_m ≤ 1` | REFUTED (v8) |
| `M_m ≥ 10` | PROVED (v8) |
| `M_m ≤ 18` via tight-clique | **FALSE hope** — only tight subfamilies |
| Atom-scale `M_m` upper | OPEN |
| B2 residual can-core `Phi_w`-image | OPEN (still the wall) |

## Next real math

1. Atom-scale upper bound on full `M_m` that accounts for non-tight pairs, **or**
2. Prove residual (post first-match) fibers have no non-tight pairs / size ≤ 1, **or**
3. Bound residual can-core `Phi_w`-image (B2) without any small-`M_m` premise.

Do not re-prove `M_m ≤ 1`. Do not claim `M_m ≤ k_tight` for full fibers.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v9.py
python3 experimental/scripts/verify_kb_qatom_route_d_v9.py --check
```
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cert = build()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text())
        ensure(old["claims"] == cert["claims"], "claims drift")
        ensure(
            old["deployed"]["Mm_lower_coset"] == cert["deployed"]["Mm_lower_coset"],
            "bound drift",
        )
        ensure(
            old["deployed"]["k_tight_clique"] == cert["deployed"]["k_tight_clique"],
            "tight drift",
        )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v9\n\n"
        "M_m structural law: intersection, tight cliques, padding reduction.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v9.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v9 report\n\nstatus: {cert['status']}\n"
        f"Mm_lower_coset: {cert['deployed']['Mm_lower_coset']}\n"
        f"k_tight_clique: {cert['deployed']['k_tight_clique']}\n"
        f"log2_anticode: {cert['deployed']['log2_anticode']:.2f}\n"
        f"toy_gap_rows: {len(cert['toy_suite']['intersection_gap']['rows'])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  M_m >= {cert['deployed']['Mm_lower_coset']} (coset)")
    print(f"  k_tight clique cap: {cert['deployed']['k_tight_clique']} (not full-fiber upper)")
    print(f"  log2 anticode: {cert['deployed']['log2_anticode']:.2f}")
    print(f"  toy rows: {len(cert['toy_suite']['intersection_gap']['rows'])}")
    print(f"  tight pairs checked: {cert['toy_suite']['tight_pair']['tight_pairs_checked']}")
    gap = sum(1 for r in cert["toy_suite"]["intersection_gap"]["rows"] if r["Mm_gt_k_tight"])
    print(f"  toys with Mm > k_tight: {gap}")


if __name__ == "__main__":
    main()
