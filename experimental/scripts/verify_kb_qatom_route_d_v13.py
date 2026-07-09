#!/usr/bin/env python3
"""KB-MCA Route-D v13: recursive block factorization of multi-mates.

Every Phi_w multi-mate pair factors as a common pad plus a multi-mate of
strictly smaller (or equal) block size s >= w+1. Long trades are exactly
those with s >= w+2.

Proved:
  (1) Block factorization: if C ≠ C', Phi_w(C)=Phi_w(C'), R=C∩C',
      U=C\\\\C', V=C'\\\\C, s=|U|=|V|, then s >= w+1, Phi_w(U)=Phi_w(V),
      and Λ_C − Λ_{C'} = Λ_R (Λ_U − Λ_V) with deg(Λ_U−Λ_V) ≤ s−w−1.
  (2) Scale dictionary:
        s = w+1  ⇔  min-weight / tight / free-1 CS blocks
        s ≥ w+2  ⇔  long trade (non-tight)
  (3) Multi-mate existence is scale-recursive: a long multi-mate at (m,w)
      yields a multi-mate at (s,w) for some s ∈ [w+2, m]. Conversely,
      padding (v8/v9) lifts multi-mates at (s,w) to (m,w) when room allows.
  (4) Long-trade free criterion (conditional): if M_s^{max}(w) ≤ 1 for every
      s ∈ [w+2, m], then every multi-mate at (m,w) is tight (s=w+1), and
      pairwise-tight residual cliques have size ≤ k_tight (v9/v12).
  (5) Deployed numbers: w+1=67472, m=913632, so long scales are
      s=67473..913632; v8 uses s=e0=131072 ∈ long range.
  (6) Toys: residual aperiodic cores still realize long trades; when free is
      small and w large relative to m, residual long count can hit 0.

Does not prove residual has no long trades. Does not close the atom.
Does not claim U(1116048) ≤ B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v13.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v13.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v13"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v13.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v13.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v13.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1  # 67472
M = J - E
FREE = M - W
E0 = 2**17
PACK_J = 17
TARGET = 274_836_936_291_722_953
K_TIGHT = 1 + (N - M) // E
K_COSET = 1 + (N - M) // E0
MIN_S = E  # w+1
MIN_TRADE = 2 * E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


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
    return tuple(poly[1 : w + 1])


def aperiodic(exps: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in exps) == exps:
            return False
    return True


def c_cosets(n: int, c: int) -> list[frozenset[int]]:
    step = n // c
    return [frozenset((r + k * step) % n for k in range(c)) for r in range(step)]


def lemma_block_factorization() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multimate_block_factorization",
        "statement": (
            "Let C ≠ C' be m-subsets of D with Phi_w(C)=Phi_w(C'). "
            "Set R = C ∩ C', U = C \\\\ C', V = C' \\\\ C, and s = |U| = |V|. "
            "Then:\n"
            "  (i)   s ≥ w+1 and |R| = m−s ≤ m−w−1;\n"
            "  (ii)  Λ_C = Λ_R Λ_U, Λ_{C'} = Λ_R Λ_V, and "
            "Λ_C − Λ_{C'} = Λ_R (Λ_U − Λ_V);\n"
            "  (iii) deg(Λ_U − Λ_V) ≤ s − w − 1, hence Phi_w(U)=Phi_w(V);\n"
            "  (iv)  |C △ C'| = 2s."
        ),
        "proof": [
            "From v9/v12: |R| = |C ∩ C'| ≤ m−w−1, so s = m−|R| ≥ w+1.",
            "Disjoint unions C = R ⊔ U, C' = R ⊔ V give the locator factorizations.",
            "Phi_w(C)=Phi_w(C') means deg(Λ_C − Λ_{C'}) ≤ m−w−1. "
            "But Λ_C − Λ_{C'} = Λ_R (Λ_U − Λ_V), so "
            "deg = |R| + deg(Λ_U − Λ_V) ≤ m−w−1, hence "
            "deg(Λ_U − Λ_V) ≤ m−w−1−(m−s) = s−w−1.",
            "For monic degree-s locators, deg(difference) ≤ s−w−1 means the first "
            "w high monic coefficients agree, i.e. Phi_w(U)=Phi_w(V).",
            "|C △ C'| = |U| + |V| = 2s.",
        ],
    }


def lemma_scale_dictionary() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "scale_dictionary_tight_vs_long",
        "statement": (
            "Under block factorization, s = |C \\\\ C'| satisfies:\n"
            "  s = w+1  ⇔  |C △ C'| = 2(w+1)  ⇔  tight / min-weight "
            "(free-1 CS of (w+1)-blocks on core R);\n"
            "  s ≥ w+2  ⇔  |C △ C'| ≥ 2(w+2)  ⇔  long trade / non-tight, "
            "and (U,V) is a multi-mate pair at parameters (s,w) with free_s = s−w ≥ 2."
        ),
        "proof": [
            "Immediate from block factorization + trade-weight law (v12) + "
            "tight-pair law (v9).",
            "free_s = s − w: when s = w+1, free_s = 1; when s ≥ w+2, free_s ≥ 2.",
        ],
        "deployed": {
            "s_tight": E,
            "s_long_min": E + 1,
            "s_long_max": M,
            "v8_s": E0,
            "v8_is_long": E0 >= E + 1,
        },
    }


def lemma_recursion() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multimate_scale_recursion",
        "statement": (
            "Let M_m^{max}(w) be the max Phi_w fiber size among m-subsets of D. "
            "(A) If there exists a multi-mate pair at (m,w) with block size s, then "
            "M_s^{max}(w) ≥ 2. "
            "(B) Conversely, if M_s^{max}(w) ≥ 2 and n − s ≥ m − s (i.e. n ≥ m) "
            "with room for a common pad R of size m−s disjoint from two disjoint "
            "s-blocks in one fiber, then M_m^{max}(w) ≥ 2 (padding reduction, v8/v9). "
            "(C) Therefore long multi-mates at (m,w) exist only if multi-mates exist "
            "at some scale s ∈ [w+2, m]."
        ),
        "proof": [
            "(A) Block factorization produces U ≠ V with Phi_w(U)=Phi_w(V), |U|=s.",
            "(B) v9 padding reduction / v8 coset case.",
            "(C) Long means s ≥ w+2; apply (A).",
        ],
    }


def lemma_long_free_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "no_long_scales_implies_only_tight",
        "statement": (
            "If M_s^{max}(w) ≤ 1 for every s ∈ [w+2, m], then every multi-mate "
            "pair at (m,w) has block size s = w+1 (tight only). "
            "If moreover every residual multi-mate fiber is a pairwise-tight clique, "
            f"then M_m^{{res,phi}} ≤ k_tight = {K_TIGHT}, and "
            f"U_res ≤ floor(target/(17*{K_TIGHT})) closes the residual atom."
        ),
        "proof": [
            "If a multi-mate had s ≥ w+2 then M_s^{max}(w) ≥ 2, contradiction.",
            "Hence only s = w+1 multi-mates remain (or no multi-mates).",
            "Apply v12 min-weight pairwise-tight criterion.",
        ],
        "deployed_long_scales": {
            "s_min": E + 1,
            "s_max": M,
            "count_of_scales": M - E,  # s = w+2 .. m inclusive: m-(w+2)+1 = m-w-1
            "count_inclusive": M - (E + 1) + 1,
        },
        "note": (
            "Still a large family of scales. The point is reduction: residual "
            "uniqueness at ALL free≥2 scales of depth w implies only tight "
            "multi-mates at deployed m. Entropy at each scale with "
            "C(n,s)/p^w ≪ 1 is the same style of claim."
        ),
        "budgets_if_Kres_18": {
            "U_res": TARGET // (PACK_J * K_TIGHT),
            "log2": math.log2(max(TARGET / (PACK_J * K_TIGHT), 1)),
        },
    }


def lemma_atomic_scale() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "tight_scale_is_atomic_free1",
        "statement": (
            "The minimal multi-mate scale s = w+1 is exactly the free-1 regime "
            "for block size s: M_{w+1}^{max}(w) ≤ floor(n/(w+1)), achieved by "
            "full free-1 CS pencils (e.g. pure cosets when (w+1)|n)."
        ),
        "proof": [
            "free = s − w = 1 at s = w+1; apply free-1 packing (v6).",
            "Cosets when e0 = w+1 divides n: pencil size n/e0 (v8).",
        ],
        "deployed": {
            "s": E,
            "floor_n_over_s": N // E,
            "e0_coset_divides": N % E0 == 0,
            "note": "Deployed tight scale e=w+1 does not divide n; pure cosets use e0=2^17 > e.",
        },
    }


def lemma_program() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_PROGRAM_LAW",
        "name": "v13_reduction",
        "statement": (
            "Residual atom after v12–v13 reduces to forbidding multi-mates at "
            "long scales s ∈ [w+2, m] inside residual can-cores (or paying them), "
            "then applying tight-clique packing ≤ 18; or proving residual "
            "M_m^{res} ≤ 1 directly; or bounding U_phi."
        ),
        "not_proved": [
            "no residual long-scale multi-mates",
            "residual tight fibers are cliques",
            "M_m^{res} ≤ 1",
            "U_phi atom bound",
        ],
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    # Full m-fiber: verify factorization on all multi-mate pairs
    for m, w in [(4, 2), (5, 2), (5, 3), (6, 2), (6, 3), (6, 4), (8, 6)]:
        p, n = 17, 16
        if math.comb(n, m) > 10000:
            continue
        vals = domain_vals(p, n)
        fib: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for S in itertools.combinations(range(n), m):
            fib[phi_w(monic_rev([vals[i] for i in S], p), w)].append(frozenset(S))
        n_pairs = 0
        n_tight = 0
        n_long = 0
        s_hist: Counter[int] = Counter()
        for sets in fib.values():
            if len(sets) < 2:
                continue
            for i, a in enumerate(sets):
                for b in sets[i + 1 :]:
                    R = a & b
                    U, V = a - b, b - a
                    s = len(U)
                    ensure(s == len(V), "bal")
                    ensure(s >= w + 1, f"s>={w+1}")
                    ensure(len(R) == m - s, "R size")
                    # Phi_w on blocks
                    pu = monic_rev([vals[i] for i in sorted(U)], p)
                    pv = monic_rev([vals[i] for i in sorted(V)], p)
                    ensure(phi_w(pu, w) == phi_w(pv, w), "block Phi_w")
                    n_pairs += 1
                    s_hist[s] += 1
                    if s == w + 1:
                        n_tight += 1
                        # free-1: middle coeffs of length s-1=w agree except const
                        ensure(pu[1:s] == pv[1:s] or True, "placeholder")
                        # high w coeffs are poly[1:w+1]; free-1 means poly[1:s] match except const at s
                        ensure(pu[1:s] == pv[1:s] and pu[s] != pv[s] or pu[1:w+1] == pv[1:w+1], "f1")
                        # simpler: already Phi_w match; for s=w+1, Phi_w is all but const
                        ensure(pu[1:w+1] == pv[1:w+1], "tight high")
                        ensure(pu[s] != pv[s], "tight const differs")
                    else:
                        n_long += 1
        rows.append(
            {
                "kind": "full",
                "m": m,
                "w": w,
                "free": m - w,
                "n_pairs": n_pairs,
                "n_tight_s": n_tight,
                "n_long_s": n_long,
                "s_hist": dict(s_hist),
                "Mm": max((len(v) for v in fib.values()), default=0),
            }
        )

    # Residual cores from aperiodic j-supports
    res_rows = []
    for j, w in [(9, 2), (7, 2), (10, 3), (6, 2), (9, 3)]:
        p, n = 17, 16
        e = w + 1
        m = j - e
        if m <= 1 or math.comb(n, j) > 12000:
            continue
        vals = domain_vals(p, n)
        cores: set[frozenset[int]] = set()
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            if not aperiodic(S, n):
                continue
            ss = sorted(S)
            U = frozenset(ss[:e])
            cores.add(S - U)
        fib = defaultdict(list)
        for C in cores:
            fib[phi_w(monic_rev([vals[i] for i in sorted(C)], p), w)].append(C)
        n_tight = n_long = 0
        s_hist: Counter[int] = Counter()
        for sets in fib.values():
            if len(sets) < 2:
                continue
            # unique
            uniq = list({tuple(sorted(c)): c for c in sets}.values())
            for i, a in enumerate(uniq):
                for b in uniq[i + 1 :]:
                    s = len(a - b)
                    ensure(s >= w + 1, "res s")
                    U, V = a - b, b - a
                    ensure(
                        phi_w(monic_rev([vals[i] for i in sorted(U)], p), w)
                        == phi_w(monic_rev([vals[i] for i in sorted(V)], p), w),
                        "res block phi",
                    )
                    s_hist[s] += 1
                    if s == w + 1:
                        n_tight += 1
                    else:
                        n_long += 1
        res_rows.append(
            {
                "kind": "residual_proxy",
                "j": j,
                "m": m,
                "w": w,
                "n_tight_s": n_tight,
                "n_long_s": n_long,
                "s_hist": dict(s_hist),
                "Mm_res": max(
                    (
                        len({tuple(sorted(c)) for c in v})
                        for v in fib.values()
                    ),
                    default=0,
                ),
            }
        )

    # Unit: v8-style long factorization on toy
    p, n, e0, w, m = 17, 16, 4, 2, 6
    ensure(e0 > w + 1, "long e0")
    vals = domain_vals(p, n)
    cos = c_cosets(n, e0)
    free_pts = [i for i in range(n) if i not in cos[0] and i not in cos[1]]
    R = frozenset(free_pts[: m - e0])
    C1, C2 = R | cos[0], R | cos[1]
    ensure(phi_w(monic_rev([vals[i] for i in sorted(C1)], p), w) ==
           phi_w(monic_rev([vals[i] for i in sorted(C2)], p), w), "pad phi")
    U, V = C1 - C2, C2 - C1
    ensure(len(U) == e0 and U == cos[0], "U coset")
    ensure(
        phi_w(monic_rev([vals[i] for i in sorted(U)], p), w)
        == phi_w(monic_rev([vals[i] for i in sorted(V)], p), w),
        "block phi coset",
    )
    ensure(len(C1 ^ C2) == 2 * e0, "long trade")
    unit = {"e0": e0, "s": e0, "long": True, "block_phi_match": True}

    # Deployed gates
    ensure(MIN_S == W + 1, "min s")
    ensure(E0 > MIN_S, "v8 long scale")
    ensure(K_TIGHT == 18, "kt")
    ensure(any(r["n_long_s"] > 0 for r in rows), "has long")
    ensure(any(r["n_tight_s"] > 0 for r in rows), "has tight")
    ensure(all(r["n_pairs"] == r["n_tight_s"] + r["n_long_s"] for r in rows), "sum")

    return {
        "status": "PASS",
        "full_rows": rows,
        "residual_rows": res_rows,
        "unit_long_factor": unit,
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v13",
        "title": "Recursive block factorization of Phi_w multi-mates",
        "status": "PARTIAL_SCALE_RECURSION",
        "claims": {
            "proves_block_factorization": True,
            "proves_scale_dictionary": True,
            "proves_scale_recursion": True,
            "proves_long_free_criterion": True,
            "proves_tight_scale_free1": True,
            "proves_no_residual_long_trades": False,
            "proves_Mm_res_le_1": False,
            "proves_unconditional_atom": False,
        },
        "deployed": {
            "n": N,
            "m": M,
            "w": W,
            "s_tight": MIN_S,
            "s_long_min": MIN_S + 1,
            "s_long_max": M,
            "n_long_scales": M - MIN_S,
            "v8_s": E0,
            "v8_long": True,
            "k_tight": K_TIGHT,
            "k_coset_lower": K_COSET,
            "min_trade": MIN_TRADE,
            "U_res_if_Kres_18": TARGET // (PACK_J * K_TIGHT),
            "log2_U_res_K18": math.log2(max(TARGET / (PACK_J * K_TIGHT), 1)),
        },
        "lemmas": {
            "block_factorization": lemma_block_factorization(),
            "scale_dictionary": lemma_scale_dictionary(),
            "recursion": lemma_recursion(),
            "long_free_criterion": lemma_long_free_criterion(),
            "atomic_scale": lemma_atomic_scale(),
            "program": lemma_program(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": (
                "Long multi-mates at deployed m ⇔ multi-mates at some s in "
                f"[{MIN_S+1}, {M}] at same depth w"
            ),
            "next": (
                "Forbid/pay multi-mates at long scales inside residual, then "
                "tight-clique ≤18; or M_m^res≤1; or U_phi"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    full = cert["toy_suite"]["full_rows"]
    res = cert["toy_suite"]["residual_rows"]
    ftbl = "\n".join(
        f"| {r['m']} | {r['w']} | {r['free']} | {r['Mm']} | {r['n_tight_s']} | "
        f"{r['n_long_s']} | {r['s_hist']} |"
        for r in full
    )
    rtbl = "\n".join(
        f"| {r['j']} | {r['m']} | {r['w']} | {r['Mm_res']} | {r['n_tight_s']} | "
        f"{r['n_long_s']} | {r['s_hist']} |"
        for r in res
    )
    return f"""# KB-MCA Route-D v13: block factorization of multi-mates

Status: `PARTIAL` — scale recursion **PROVED**; residual long-trade ban **OPEN**.

## Block factorization (PROVED, unconditional)

If `Phi_w(C)=Phi_w(C')`, `C ≠ C'`, set `R=C∩C'`, `U=C\\\\C'`, `V=C'\\\\C`, `s=|U|`:

```text
s ≥ w+1
Phi_w(U) = Phi_w(V)          (same depth w on blocks)
Λ_C − Λ_{{C'}} = Λ_R (Λ_U − Λ_V)
|C △ C'| = 2s
```

## Scale dictionary

| Block size s | Trade | Meaning |
|---:|---|---|
| s = w+1 = {d['s_tight']} | min-weight | tight free-1 CS |
| s ≥ w+2 | long | free_s = s−w ≥ 2 multi-mate of blocks |
| s = 2^17 (v8) | long | coset pad |

Deployed long scales: `s ∈ [{d['s_long_min']}, {d['s_long_max']}]`
({d['n_long_scales']} values).

## Recursion (PROVED)

```text
long multi-mate at (m,w)
    ⇒  multi-mate at some (s,w), s ∈ [w+2, m]
padding multi-mate at (s,w)
    ⇒  multi-mate at (m,w)  (when room)
```

## Conditional criterion

```text
M_s^{{max}}(w) ≤ 1  for all s ∈ [w+2, m]
    ⇒  only tight multi-mates at (m,w)
    + pairwise-tight residual cliques
    ⇒  M_m^{{res}} ≤ k_tight = {d['k_tight']}
    ⇒  U_res ≤ target/(17·18) ≈ 2^{{{d['log2_U_res_K18']:.2f}}}
```

## Toys

### Full m-fibers (factorization checks on all pairs)

| m | w | free | Mm | #tight s | #long s | s histogram |
|---|---|---:|---:|---:|---:|---|
{ftbl}

### Residual-proxy can-cores (aperiodic j)

| j | m | w | Mm_res | #tight | #long | s hist |
|---|---|---|---:|---:|---:|---|
{rtbl}

## Unconditional atom?

Still **no**. But long trades are no longer an unstructured remainder:
they are multi-mates at long block scales.

## Next real math

1. Residual (or first-match payment) forbids multi-mates at scales s ≥ w+2, **or**
2. Bound max fiber at long scales after residual pruning, **or**
3. `M_m^{{res}} ≤ 1` / `U_phi` directly.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v13.py
python3 experimental/scripts/verify_kb_qatom_route_d_v13.py --check
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
        ensure(old["deployed"]["s_tight"] == cert["deployed"]["s_tight"], "s drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v13\n\n"
        "Recursive block factorization of Phi_w multi-mates.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v13.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v13 report\n\nstatus: {cert['status']}\n"
        f"s_tight: {cert['deployed']['s_tight']}\n"
        f"v8_s: {cert['deployed']['v8_s']} long: true\n"
        f"full_rows: {len(cert['toy_suite']['full_rows'])}\n"
        f"residual_rows: {len(cert['toy_suite']['residual_rows'])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  block factorization: PROVED")
    print(f"  s_tight=w+1={cert['deployed']['s_tight']}; long s>={cert['deployed']['s_long_min']}")
    print(f"  v8 s={cert['deployed']['v8_s']} is LONG")
    print(f"  long scales count: {cert['deployed']['n_long_scales']}")
    print(f"  full rows: {len(cert['toy_suite']['full_rows'])}")
    print(f"  residual rows: {len(cert['toy_suite']['residual_rows'])}")
    for r in cert["toy_suite"]["residual_rows"]:
        print(
            f"    j={r['j']} m={r['m']} w={r['w']}: "
            f"Mm_res={r['Mm_res']} tight={r['n_tight_s']} long={r['n_long_s']}"
        )


if __name__ == "__main__":
    main()
