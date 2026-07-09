#!/usr/bin/env python3
"""KB-MCA Route-D v64: phase form All=sum f(s)G(beta); CS bound; soft-B budget.

After v63 bilinear factorization, keep structure but apply Cauchy+Plancherel
and compute the deployed coll budget for a soft max|S| bound B_*.

Proved:
  (1) Level-set form. For l1 != 0 and arc value set S subset F_p, |S|=t,
        f(s) = sum_{x in S cap (s-S)} psi(l1 (s x - x^2)),
        beta(s) = -l0 + l1 s,
        G(alpha) = sum_{y in S} psi(alpha y),
      one has
        All = sum_s psi(-l0 s) f(s) G(beta(s)).
      (Recovered from v63 by grouping pairs with vi+vj=s and using
       vi vj = s vi - vi^2.)
  (2) Cauchy + Plancherel. If l1 != 0 then beta is bijective, so
        sum_s |G(beta(s))|^2 = sum_alpha |G(alpha)|^2 = p t
      (Plancherel for the arc indicator). Hence
        |All| <= sqrt( sum_s |f(s)|^2 ) * sqrt(p t).
  (3) Phased energy dominated by additive energy:
        |f(s)| <= r(s) := |S cap (s-S)|,
        sum_s |f(s)|^2 <= sum_s r(s)^2 =: E_+(S)
      (additive energy of S counting ordered sum representations).
      Therefore |All| <= sqrt(E_+(S) p t).
  (4) Soft-B coll budget (v58). If |S(lambda)| <= B for all lambda != 0 then
        coll <= C^2 / p^{e-1} + B^2.
      |T| <= nH <= coll/2, so coll <= 2 H2 forces |T| <= H2.
      Sufficient: B <= B_* with
        B_*^2 = 2 H2 - C^2/p^{e-1}   (when positive).
  (5) Deployed arithmetic (exact log-space):
        log2 C = log2 binom(n',e) ~ 3.73e5,
        log2(C^2 / p^{e-1}) ~ -1.344e6  (term ~ 0 for all practical purposes),
        B_* = sqrt(2 H2) ~ 3.932e5.
      So any proof of max_{lambda != 0} |S(lambda)| <= 3.93e5 at deployed
      (n',e) closes |T|<=H2 via v58 — much weaker than |S|<=sqrt(C)
      (sqrt(C) is astronomically larger than B_* at deployed e).
  (6) e=3 toy scale: CS bound |All| <= sqrt(sum|f|^2) sqrt(p t) is typically
      slightly tighter than v63's sum r2|G|, and often << v62's p t^{3/2}.
      If sum|f|^2 = O(t^2) then |All| = O(t^{3/2} sqrt(p)), still ~sqrt(p)
      short of sqrt(C) ~ t^{3/2} — same qualitative gap as soft envelopes for e=3
      sqrt-cancel, but the *deployed* bar is B_* not sqrt(C).

CAS:
  (7) Identity (1) holds (err ~ 1e-12).
  (8) sum_alpha |G|^2 = p t; CS bound holds; sum|f|^2 <= E_+(S).
  (9) Deployed log2(C^2/p^{e-1}) matches ~ -1.34e6 (v55 entropy scale).
  (10) e=3 toys: max|S|/sqrt(C)=O(1-3); CS/sqrt(C) still >>1.

OPEN:
  (A) Bound sum|f|^2 (phased energy) for GP arcs sharply enough that the CS
      All-bound reaches soft or sqrt targets.
  (B) Lift soft-B: prove max|S| <= B_* ~ 4e5 for free-1 highs at deployed
      (n',e) — the actual residual-close bar.
  (C) e=3 sqrt-cancel remains a method template, not the deployed numerical bar.

Does NOT close |T|<=H2 unconditionally; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v64.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v64"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v64.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v64.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v64.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A_DEP = 1_116_048
J = N - A_DEP
T_ROW = A_DEP - 2**20
Wdeg = T_ROW - 1
E = Wdeg + 1
M_C = J - E
FREE_CORE = M_C - Wdeg
N_PRIME = A_DEP + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


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


def lemma_level_set() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_All_level_set_f_G",
        "statement": (
            "All = sum_s psi(-l0 s) f(s) G(-l0+l1 s) with "
            "f(s)=sum_{x in S cap (s-S)} psi(l1(s x - x^2))."
        ),
        "proof": [
            "Group (i,j) by s=vi+vj; vi vj = s vi - vi^2.",
            "Inner sum over such x=vi in S with s-x in S is f(s).",
            "Factor G(beta(s)) from the third arc index (v63).",
        ],
    }


def lemma_CS() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_All_CS_Plancherel",
        "statement": (
            "For l1!=0: |All| <= sqrt(sum_s |f(s)|^2) * sqrt(p t)."
        ),
        "proof": [
            "Cauchy-Schwarz on sum_s (psi(-l0 s) f(s)) G(beta(s)).",
            "beta bijective => sum_s |G(beta(s))|^2 = sum_a |G(a)|^2 = p t.",
        ],
    }


def lemma_energy_dom() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "phased_energy_le_additive_energy",
        "statement": (
            "sum |f|^2 <= E_+(S) := sum_s r(s)^2, r(s)=|S cap (s-S)|; "
            "hence |All| <= sqrt(E_+(S) p t)."
        ),
        "proof": [
            "|f(s)| <= r(s) termwise (unimodular sum).",
            "E_+(S) is the ordered additive energy of S.",
        ],
    }


def lemma_soft_B() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "soft_B_coll_budget",
        "statement": (
            "If max_{lambda!=0}|S(lambda)| <= B and B^2 + C^2/p^{e-1} <= 2 H2, "
            "then coll <= 2 H2 and |T| <= H2 (via v57-v58)."
        ),
        "proof": [
            "v58: coll <= C^2/p^{e-1} + B^2.",
            "v57: |T| <= nH <= coll/2.",
            "coll/2 <= H2 <=> coll <= 2 H2.",
        ],
    }


def lemma_deployed_Bstar() -> dict[str, Any]:
    log2C = log2_comb(N_PRIME, E)
    log2_term = 2 * log2C - (E - 1) * math.log2(P)
    Bstar = math.sqrt(2 * H2)  # term negligible
    return {
        "status": "PROVED",
        "name": "deployed_Bstar_arithmetic",
        "statement": (
            f"At deployed (n',e,p,H2): log2(C^2/p^{{e-1}}) ~ {log2_term:.1f} "
            f"(<<0), so B_* = sqrt(2 H2) ~ {Bstar:.1f} suffices for soft-B close."
        ),
        "proof": [
            "log2 binom(n',e) by summing log2((n'-i)/(i+1)).",
            "C^2/p^{e-1} = 2^{log2_term} with log2_term ~ -1.34e6 => ~0.",
            "B_*^2 = 2 H2 - C^2/p^{e-1} = 2 H2 for practical purposes.",
        ],
        "numbers": {
            "log2_C": log2C,
            "log2_C2_over_p_em1": log2_term,
            "H2": H2,
            "B_star": Bstar,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_phased_energy_or_soft_B_deployed",
        "statement": (
            "Bound sum|f|^2 for GP arcs (e=3 method), and/or prove "
            f"max|S| <= B_* ~ {math.sqrt(2*H2):.0f} at deployed (n',e)."
        ),
    }


def prim_root(p: int) -> int:
    fac: list[int] = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            fac.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no prim root")


def domain_vals(p: int, n: int) -> list[int]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(n)]


def monic_high3(u: int, v: int, w: int, p: int) -> tuple[int, int]:
    poly = [1]
    for x in (u, v, w):
        new = [0] * (len(poly) + 1)
        mv = (-x) % p
        for j, c in enumerate(poly):
            new[j] = (new[j] + c) % p
            new[j + 1] = (new[j + 1] + c * mv) % p
        poly = new
    return poly[1] % p, poly[2] % p


def G_table(p: int, vals: list[int]) -> list[complex]:
    out: list[complex] = []
    for a in range(p):
        s = 0j
        for x in vals:
            s += np.exp(2j * np.pi * ((a * x) % p) / p)
        out.append(s)
    return out


def row_fG(p: int, n: int, t: int, l0: int, l1: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    Sset = set(vals)

    All = 0j
    Ssum = 0j
    for i in range(t):
        for j in range(t):
            for k in range(t):
                h0, h1 = monic_high3(vals[i], vals[j], vals[k], p)
                All += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)
    for i, j, k in itertools.combinations(range(t), 3):
        h0, h1 = monic_high3(vals[i], vals[j], vals[k], p)
        Ssum += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)

    Gt = G_table(p, vals)
    sum_G2 = sum(abs(g) ** 2 for g in Gt)

    f = np.zeros(p, dtype=np.complex128)
    r = np.zeros(p, dtype=np.float64)
    for s in range(p):
        sm = 0j
        cnt = 0
        for x in vals:
            if (s - x) % p in Sset:
                cnt += 1
                phase = (l1 * ((s * x - x * x) % p)) % p
                sm += np.exp(2j * np.pi * phase / p)
        f[s] = sm
        r[s] = cnt

    All2 = 0j
    sum_Gbeta2 = 0.0
    for s in range(p):
        beta = (-l0 + l1 * s) % p
        All2 += np.exp(2j * np.pi * (((-l0) * s) % p) / p) * f[s] * Gt[beta]
        sum_Gbeta2 += abs(Gt[beta]) ** 2

    sum_f2 = float(np.sum(np.abs(f) ** 2))
    E_plus = float(np.sum(r**2))
    bound_CS = math.sqrt(sum_f2 * sum_Gbeta2)
    bound_E = math.sqrt(E_plus * p * t)
    bound_v62 = p * (t**1.5)
    C = math.comb(t, 3)
    bound_S = (1 / 6) * (bound_CS + 3 * t * (t - 1) + t)

    return {
        "p": p,
        "t": t,
        "l0": l0,
        "l1": l1,
        "abs_All": float(abs(All)),
        "abs_S": float(abs(Ssum)),
        "fact_err": float(abs(All - All2)),
        "sum_G2": float(sum_G2),
        "sum_Gbeta2": float(sum_Gbeta2),
        "p_t": float(p * t),
        "plancherel_ok": bool(abs(sum_G2 - p * t) < 1e-6),
        "beta_plancherel_ok": bool(abs(sum_Gbeta2 - p * t) < 1e-6),
        "sum_f2": float(sum_f2),
        "E_plus": float(E_plus),
        "f2_le_E": bool(sum_f2 <= E_plus + 1e-6),
        "bound_CS": float(bound_CS),
        "bound_E": float(bound_E),
        "bound_v62": float(bound_v62),
        "All_le_CS": bool(abs(All) <= bound_CS + 1e-4),
        "All_le_E": bool(abs(All) <= bound_E + 1e-4),
        "CS_over_v62": float(bound_CS / bound_v62),
        "sum_f2_over_t2": float(sum_f2 / (t * t)),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(abs(Ssum) / math.sqrt(C)),
        "bound_S_over_sqrtC": float(bound_S / math.sqrt(C)),
        "forces_sqrt_cancel": bool(bound_S <= math.sqrt(C) + 1e-9),
    }


def maxS_row(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    for idxs in itertools.combinations(range(t), 3):
        h0, h1 = monic_high3(vals[idxs[0]], vals[idxs[1]], vals[idxs[2]], p)
        freq[h0, h1] += 1
        C += 1
    F = np.fft.fft2(freq)
    a = np.abs(F)
    a[0, 0] = 0
    maxS = float(np.max(a))
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "maxS": float(maxS),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
    }


def deployed_budget() -> dict[str, Any]:
    log2C = log2_comb(N_PRIME, E)
    log2_term = 2 * log2C - (E - 1) * math.log2(P)
    term = 2.0**log2_term  # underflows to 0.0 in float — correct practically
    two_H2 = 2.0 * H2
    # B_*^2 = 2 H2 - term; term ~ 0
    Bstar_sq = two_H2 - term if two_H2 > term else 0.0
    Bstar = math.sqrt(Bstar_sq) if Bstar_sq > 0 else 0.0
    # compare to trivial |S|<=C impossible; soft vs sqrt(C) log
    return {
        "n_prime": N_PRIME,
        "e": E,
        "p": P,
        "H2": H2,
        "log2_C": float(log2C),
        "log2_C2_over_p_em1": float(log2_term),
        "C2_over_p_em1_negligible": bool(log2_term < -100),
        "two_H2": float(two_H2),
        "B_star": float(Bstar),
        "B_star_sq": float(Bstar_sq),
        "sqrt_2H2": float(math.sqrt(two_H2)),
        "note": (
            "Any max|S|<=B_star at deployed closes |T|<=H2 via v58; "
            "sqrt(C) bar is not the deployed numerical target"
        ),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char!=2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    budget = deployed_budget()
    ensure(budget["C2_over_p_em1_negligible"], "term ~0")
    ensure(abs(budget["B_star"] - budget["sqrt_2H2"]) < 1e-3, "B*=sqrt(2H2)")
    # cross-check log2_term ~ -1.34e6
    ensure(budget["log2_C2_over_p_em1"] < -1e6, "log2 term scale")
    ensure(budget["log2_C2_over_p_em1"] > -2e6, "log2 term not crazy")

    fG_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 15),
        (101, 100, 15),
        (101, 100, 20),
        (127, 126, 18),
        (127, 126, 24),
    ]:
        for l0, l1 in [(1, 1), (3, 5)]:
            r = row_fG(p, n, t, l0, l1)
            ensure(r["fact_err"] < 1e-8, "fG fact")
            ensure(r["plancherel_ok"], "G plancherel")
            ensure(r["beta_plancherel_ok"], "beta plancherel")
            ensure(r["f2_le_E"], "f2<=E")
            ensure(r["All_le_CS"], "CS bound")
            ensure(r["All_le_E"], "E bound")
            ensure(not r["forces_sqrt_cancel"], "still weak sqrtC")
            fG_rows.append(r)
    ensure(len(fG_rows) >= 10, "fG rows")

    max_rows = []
    for p, n, t in [
        (61, 60, 15),
        (61, 60, 24),
        (101, 100, 15),
        (101, 100, 24),
        (127, 126, 15),
        (127, 126, 36),
    ]:
        if math.comb(t, 3) > 20000:
            continue
        r = maxS_row(p, n, t)
        ensure(r["S_over_sqrtC"] < 5, "emp")
        max_rows.append(r)

    return {
        "status": "PASS",
        "deployed_budget": budget,
        "fG_rows": fG_rows,
        "max_rows": max_rows,
        "census": {
            "n_fG": len(fG_rows),
            "n_max": len(max_rows),
            "all_identities_ok": True,
            "CS_always_holds": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in max_rows),
            "max_bound_S_over_sqrtC": max(
                r["bound_S_over_sqrtC"] for r in fG_rows
            ),
            "max_CS_over_v62": max(r["CS_over_v62"] for r in fG_rows),
            "min_CS_over_v62": min(r["CS_over_v62"] for r in fG_rows),
            "max_sum_f2_over_t2": max(r["sum_f2_over_t2"] for r in fG_rows),
            "min_sum_f2_over_t2": min(r["sum_f2_over_t2"] for r in fG_rows),
            "max_fact_err": max(r["fact_err"] for r in fG_rows),
            "B_star": budget["B_star"],
            "log2_C2_over_p_em1": budget["log2_C2_over_p_em1"],
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": budget["B_star"],
            "note": "soft-B bar B_*=sqrt(2 H2); C^2/p^{e-1} negligible",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v64",
        "title": "Phase form All=sum f G; CS bound; deployed soft-B budget",
        "status": "PHASE_CS_SOFTB_PROVED_DEPLOYED_BSTAR_OPEN",
        "claims": {
            "proves_All_level_set_f_G": True,
            "proves_All_CS_Plancherel": True,
            "proves_phased_energy_le_Eplus": True,
            "proves_soft_B_coll_budget": True,
            "proves_deployed_Bstar_arithmetic": True,
            "proves_S_le_sqrtC": False,
            "proves_S_le_Bstar_deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "level_set": lemma_level_set(),
            "CS": lemma_CS(),
            "energy_dom": lemma_energy_dom(),
            "soft_B": lemma_soft_B(),
            "deployed_Bstar": lemma_deployed_Bstar(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy": "f,G,CS", "python_nt": "GP + log2_comb"},
        "impact_on_program": {
            "closed": (
                "All=sum f(s)G(beta); CS|All|<=sqrt(sum|f|^2 p t); "
                "deployed soft-B bar B_*=sqrt(2 H2)~3.93e5"
            ),
            "wall": "prove max|S|<=B_* at deployed, or sharp sum|f|^2 on GP",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    bud = cert["toy_suite"]["deployed_budget"]
    d = cert["deployed"]
    fg_lines = []
    for r in cert["toy_suite"]["fG_rows"][:8]:
        fg_lines.append(
            f"| {r['p']} | {r['t']} | {r['l0']},{r['l1']} | {r['abs_All']:.1f} | "
            f"{r['bound_CS']:.1e} | {r['bound_v62']:.1e} | {r['CS_over_v62']:.2f} | "
            f"{r['sum_f2_over_t2']:.2f} |"
        )
    fg_tbl = "\n".join(fg_lines)
    mx_lines = []
    for r in cert["toy_suite"]["max_rows"]:
        mx_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['sqrtC']:.1f} | "
            f"{r['S_over_sqrtC']:.2f} |"
        )
    mx_tbl = "\n".join(mx_lines)
    return f"""# KB-MCA Route-D v64: phase `f·G` form, CS bound, soft-B budget

Status: **identities + deployed B_\\* arithmetic PROVED**;
`max|S|<=B_\\*` at deployed still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Level-set form (PROVED)

```text
f(s) = sum_{{x in S ∩ (s-S)}} psi(l1 (s x - x^2))
All  = sum_s psi(-l0 s) f(s) G(-l0 + l1 s)
```

## Cauchy + Plancherel (PROVED)

```text
l1 != 0  =>  sum_s |G(beta(s))|^2 = p t
|All|    <= sqrt(sum |f|^2) * sqrt(p t)
         <= sqrt(E_+(S) p t)
```

## Soft-B budget (PROVED)

```text
coll <= C^2/p^{{e-1}} + B^2     (v58)
|T|  <= coll/2                 (v57)
want coll <= 2 H2  =>  B <= B_* = sqrt(2 H2 - C^2/p^{{e-1}})
```

## Deployed arithmetic (PROVED)

| quantity | value |
|---|---:|
| n' | {bud['n_prime']} |
| e | {bud['e']} |
| H2 | {bud['H2']} |
| log2 C | {bud['log2_C']:.2f} |
| log2(C²/p^{{e-1}}) | {bud['log2_C2_over_p_em1']:.1f} |
| B_\\* = √(2 H2) | **{bud['B_star']:.1f}** |

`C²/p^{{e-1}}` is ~ `2^{{-1.34e6}}` (negligible).  
**Closing bar at deployed is `max|S| ≤ ~3.93×10^5`, not `|S|≤√C`.**

e=3 `|S|≤√C` remains a clean *method* template; the residual card only needs soft-B.

## CAS

### f·G / CS rows

| p | t | (l0,l1) | |All| | CS bound | v62 | CS/v62 | (sum|f|²)/t² |
|---|---:|---|---:|---:|---:|---:|---:|
{fg_tbl}

### max|S| (e=3)

| p | t | max|S| | √C | S/√C |
|---|---:|---:|---:|---:|
{mx_tbl}

- fact err max = {cen['max_fact_err']:.1e}
- CS/v62 in [{cen['min_CS_over_v62']:.2f}, {cen['max_CS_over_v62']:.2f}]
- (sum|f|²)/t² in [{cen['min_sum_f2_over_t2']:.2f}, {cen['max_sum_f2_over_t2']:.2f}]
- max S/√C = {cen['max_S_over_sqrtC']:.2f}
- CS still does not force e=3 √-cancel (bound_S/√C max {cen['max_bound_S_over_sqrtC']:.1e})

## Link

v58 + soft-B: prove `|S|≤B_\\*~{d['B_star']:.0f}` at deployed `(n',e)` ⇒ `|T|≤H2`.  
v64 isolates that numerical bar and gives CS handle on e=3 via phased energy `sum|f|²`.

## OPEN

1. **Primary:** `max_{{λ≠0}} |S(λ)| ≤ B_\\*` at deployed `(n',e)` (free-1 highs on GP arc).  
2. Bound `sum|f|²` for GP arcs (e=3 laboratory).  
3. Alternate `|R2|≤e·p` if exp-sums stall.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v64.py --check
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
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    NOTE_PATH.write_text(render_note(cert))
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v64\n\n"
        "Phase form All=sum f G; CS bound; deployed soft-B budget B_*=sqrt(2 H2).\n"
    )
    REPORT_PATH.write_text(
        f"# v64 report\n\nstatus: {cert['status']}\n"
        f"level-set f·G: PROVED\n"
        f"CS+Plancherel All bound: PROVED\n"
        f"deployed B_*=sqrt(2 H2): PROVED arithmetic\n"
        f"OPEN max|S|<=B_* at deployed: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  All = sum_s psi(-l0 s) f(s) G(beta(s)): PROVED")
    print("  |All| <= sqrt(sum|f|^2) sqrt(p t): PROVED")
    print("  soft-B: B^2 + C^2/p^{e-1} <= 2 H2 => |T|<=H2: PROVED")
    print(
        f"  deployed: log2(C^2/p^{{e-1}})={cen['log2_C2_over_p_em1']:.1f}; "
        f"B_*={cen['B_star']:.1f}"
    )
    print(
        f"  CAS: fG={cen['n_fG']}; max S/sqrtC={cen['max_S_over_sqrtC']:.2f}; "
        f"CS/v62 in [{cen['min_CS_over_v62']:.2f},{cen['max_CS_over_v62']:.2f}]; "
        f"(sum|f|^2)/t^2 in [{cen['min_sum_f2_over_t2']:.2f},"
        f"{cen['max_sum_f2_over_t2']:.2f}]"
    )
    print("  OPEN: max|S|<=B_* at deployed (or sharp sum|f|^2 on GP)")


if __name__ == "__main__":
    main()
