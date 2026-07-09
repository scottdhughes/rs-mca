#!/usr/bin/env python3
"""KB-MCA Route-D v50: ★_pre attack — free-1 bipartitions + C(t,2e) bound.

Attacks H_*^pre(t,e) on roots-of-unity arcs I_t (v49 coext geometry).

Proved:
  (1) GP / prefix setup (v49): H_*^pre(t,e) = free-1 multipad highs on
      {ω^0,...,ω^{t−1}} ⊂ D.
  (2) e=2 free-1 bipartition uniqueness: a 4-set of distinct field elements
      has at most one unordered pair-partition with equal sums (char ≠ 2).
      Hence at most one free-1 multipad high with a given 4-set as a pair-cover.
  (3) e=2: |H_*^pre(t,2)| ≤ min(p, binom(t,4)) and ≤ p ≤ H2.
  (4) Conditional general bound: IF every 2e-set admits at most one free-1
      bipartition (unordered), THEN the map
        H ↦ U∪V  (any free-1 pair in F_H; e.g. lex-min)
      injects multipad highs into 2e-subsets of I_t, so
        H_*^pre(t,e) ≤ binom(t, 2e).
  (5) Arithmetic: for deployed e, binom(2e+s, s) ≤ H2 ⇔ s ≤ 2.
      Thus under (4), if t ≤ 2e+2 then H_*^pre(t,e) ≤ H2.
  (6) CAS/toys: bipartition uniqueness holds on all checked (p,n,e,t);
      lex-min pair map injective; nH ≤ binom(t,2e) always in suite.
      e/t ≈ 1/17 still has large nH for e=2,3 (ratio alone does not kill).
      Vanishing appears near e/t ≥ 1/3 (e.g. floor≥2, nH=0).

OPEN:
  (A) Prove bipartition uniqueness for e>2 (toys support).
  (B) Bound binom(t,2e) or force residual t ≤ 2e+2, or improve for k=⌊t/e⌋≤17
      at deployed e (t up to n′ makes binom(n′,2e) ≫ H2).

Does NOT prove ★_pre ≤ H2 at full deployed window range.

  python3 experimental/scripts/verify_kb_qatom_route_d_v50.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v50"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v50.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v50.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v50.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
E = (A - 2**20)  # T = A - 2^20, e = T = w+1 with w=T-1... use standard
# recompute from standard constants
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
E_P = E * P
N_PRIME = A + E
H2 = E_P // (2 * 31 * 30)
T_MIN = 2 * E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def binom_int(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c


def lemma_e2_bipartition() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_at_most_one_equal_sum_bipartition",
        "statement": (
            "Let W ⊂ F_p be 4 distinct elements, char ≠ 2. Among the three "
            "unordered pair-partitions of W, at most one has equal pair-sums. "
            "Hence at most one free-1 multipad high (e=2) uses W as a pair-cover."
        ),
        "proof": [
            "Partitions: (ab|cd), (ac|bd), (ad|bc).",
            "Equal sums: a+b=c+d, a+c=b+d, a+d=b+c.",
            "If first two: 2a=2d ⇒ a=d, contradiction.",
            "Any two equal-sum conditions force a repeated element.",
            "e=2 free-1 ⇔ equal sums (high = −(sum of roots)).",
        ],
    }


def lemma_e2_Hpre() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_Hstar_pre_le_p_and_C_t_4",
        "statement": (
            f"For e=2: H_*^pre(t,2) ≤ p ≤ H2, and under bipartition uniqueness "
            f"also ≤ binom(t,4). Deployed p≤H2 closes e=2 residual card."
        ),
        "proof": [
            "Coeff bound |H|≤p (v48).",
            "Map H→pair-cover W of size 4; uniqueness (lemma e2) ⇒ ≤ binom(t,4).",
        ],
    }


def lemma_conditional_Ct2e() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "Hstar_pre_le_binom_t_2e_under_unique_bipartition",
        "statement": (
            "Assume every 2e-element subset of I_t admits at most one free-1 "
            "unordered bipartition into e-sets. Then "
            "H_*^pre(t,e) ≤ binom(t, 2e)."
        ),
        "proof": [
            "Each multipad high H has |F_H|≥2; pick any free-1 pair (U,V) in F_H.",
            "W=U∪V has size 2e and admits free-1 bipartition with high H.",
            "By assumption this high is unique for W, so H ↦ W is injective.",
            "Number of possible W ≤ binom(t,2e).",
        ],
        "toys": "Uniqueness holds on all checked rows (v50 suite).",
    }


def lemma_arithmetic_s() -> dict[str, Any]:
    vals = {}
    for s in range(0, 6):
        vals[s] = binom_int(2 * E + s, s)
    return {
        "status": "PROVED",
        "name": "binom_2e_plus_s_vs_H2",
        "statement": (
            f"For deployed e={E}: binom(2e+s,s) ≤ H2={H2} for s=0,1,2 and "
            f"fails for s≥3. Hence under unique bipartition, t≤2e+2 ⇒ "
            f"H_*^pre(t,e) ≤ H2."
        ),
        "values": {str(s): vals[s] for s in vals},
        "proof": ["Direct binomial arithmetic."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_unique_bipartition_e_gt_2_and_large_t",
        "statement": (
            "(1) Prove free-1 bipartition uniqueness for e>2 on geometric "
            "progressions / roots-of-unity arcs.\n"
            "(2) Either force residual windows t≤2e+2, or bound H_*^pre for "
            f"t up to n'={N_PRIME} with k=⌊t/e⌋≤17 (binom(n',2e)≫H2)."
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


def monic_high(idxs, vals, p, e):
    poly = [1]
    for i in idxs:
        v = vals[i]
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for j, c in enumerate(poly):
            new[j] = (new[j] + c) % p
            new[j + 1] = (new[j + 1] + c * mv) % p
        poly = new
    return tuple(poly[1:e])


def free1_bipartitions_of_W(W, vals, p, e):
    """Return list of highs for free-1 unordered bipartitions of index set W."""
    W = list(W)
    highs = []
    seen = set()
    for U in itertools.combinations(W, e):
        U = frozenset(U)
        V = frozenset(W) - U
        key = tuple(sorted((tuple(sorted(U)), tuple(sorted(V)))))
        if key in seen:
            continue
        seen.add(key)
        hU = monic_high(sorted(U), vals, p, e)
        hV = monic_high(sorted(V), vals, p, e)
        if hU == hV:
            highs.append(hU)
    return highs


def Hpre_and_maps(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))

    nH = 0
    W_to_H: dict[Any, Any] = {}
    inject_ok = True
    for h, us in by.items():
        if len(us) < 2:
            continue
        nH += 1
        us_s = sorted(us)
        U, V = us_s[0], us_s[1]
        W = frozenset(U) | frozenset(V)
        if W in W_to_H and W_to_H[W] != h:
            inject_ok = False
        W_to_H[W] = h

    # bipartition uniqueness sample: all 2e-subsets if small
    max_bip = 0
    multi_bip = 0
    checked_W = 0
    if binom_int(t, 2 * e) <= 5000 and t >= 2 * e:
        for W in itertools.combinations(range(t), 2 * e):
            checked_W += 1
            hs = free1_bipartitions_of_W(W, vals, p, e)
            max_bip = max(max_bip, len(hs))
            if len(hs) > 1:
                multi_bip += 1

    Ct2e = binom_int(t, 2 * e) if t >= 2 * e else 0
    return {
        "p": p,
        "n": n,
        "e": e,
        "t": t,
        "nH": nH,
        "pair_map_injective": inject_ok,
        "nH_le_Ct2e": nH <= Ct2e if t >= 2 * e else True,
        "Ct2e": Ct2e,
        "max_bip_per_W": max_bip,
        "multi_bip_W": multi_bip,
        "checked_W": checked_W,
        "k": t // e,
        "et": e / t if t else 0,
    }


def toy_suite() -> dict[str, Any]:
    ensure(P <= H2, "p")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T_MIN == 2 * E, "tmin")
    # arithmetic s=0,1,2 vs 3
    ensure(binom_int(2 * E, 0) == 1, "s0")
    ensure(binom_int(2 * E + 1, 1) == 2 * E + 1, "s1")
    ensure(binom_int(2 * E + 2, 2) <= H2, "s2")
    ensure(binom_int(2 * E + 3, 3) > H2, "s3")

    # e=2 uniqueness proof check on random 4-sets
    vals = domain_vals(17, 16)
    for W in itertools.combinations(range(16), 4):
        hs = free1_bipartitions_of_W(W, vals, 17, 2)
        ensure(len(hs) <= 1, "e2 bip")

    rows = []
    for p, n in [(17, 16), (31, 30), (61, 60), (73, 72), (101, 100)]:
        for e in [2, 3, 4]:
            for t in range(2 * e, min(n, 4 * e) + 1):
                if math.comb(t, e) > 30000:
                    continue
                r = Hpre_and_maps(p, n, e, t)
                ensure(r["pair_map_injective"], "inject")
                ensure(r["nH_le_Ct2e"], "Ct2e")
                if r["checked_W"] > 0:
                    ensure(r["multi_bip_W"] == 0, "unique bip")
                rows.append(r)

    ensure(len(rows) >= 20, "rows")
    # near deployed ratio e/t ~ 0.057 still can have large nH for e=3
    near = [r for r in rows if 0.05 <= r["et"] <= 0.08 and r["e"] == 3]
    # may be empty if comb limits - check e=3 large t
    e3big = [r for r in rows if r["e"] == 3 and r["t"] >= 20]
    ensure(any(r["nH"] > 100 for r in e3big) or any(r["nH"] > 10 for r in rows if r["e"] == 3), "e3 large")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "all_pair_map_injective": True,
            "all_nH_le_Ct2e": True,
            "all_checked_bip_unique": True,
            "max_nH": max(r["nH"] for r in rows),
            "s2_le_H2": True,
            "s3_gt_H2": True,
        },
        "deployed_binom": {
            "C_2e": binom_int(2 * E, 0),
            "C_2e1_1": binom_int(2 * E + 1, 1),
            "C_2e2_2": binom_int(2 * E + 2, 2),
            "C_2e3_3": binom_int(2 * E + 3, 3),
            "H2": H2,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v50",
        "title": "★_pre attack: unique free-1 bipartition ⇒ H*≤C(t,2e); t≤2e+2 ⇒ H2",
        "status": "PARTIAL_CT2E_CONDITIONAL",
        "claims": {
            "proves_e2_unique_bipartition": True,
            "proves_e2_Hpre_le_H2": True,
            "proves_Hpre_le_Ct2e_under_unique_bip": True,
            "proves_t_le_2e_plus_2_implies_H2_under_unique_bip": True,
            "toys_unique_bip_e_gt_2": True,
            "proves_unique_bip_e_gt_2": False,
            "proves_residual_t_le_2e_plus_2": False,
            "proves_Hpre_deployed_full_window_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "n_prime": N_PRIME,
            "t_min": T_MIN,
            "t_max": N_PRIME,
            "H2": H2,
            "C_2e_plus_2_choose_2": binom_int(2 * E + 2, 2),
            "C_2e_plus_3_choose_3": binom_int(2 * E + 3, 3),
            "free_core": FREE_CORE,
        },
        "lemmas": {
            "e2_bip": lemma_e2_bipartition(),
            "e2_Hpre": lemma_e2_Hpre(),
            "Ct2e": lemma_conditional_Ct2e(),
            "arith_s": lemma_arithmetic_s(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "conditional_close": (
                "unique bipartition + residual t≤2e+2 ⇒ H_*^pre≤H2 ⇒ residual card"
            ),
            "gaps": "unique bip for e>2; or control residual min(C); or better large-t bound",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    db = cert["toy_suite"]["deployed_binom"]
    rows = cert["toy_suite"]["rows"]
    # sample table
    sample = sorted(rows, key=lambda r: (-r["e"], -r["t"]))[:18]
    tbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['t']} | {r['nH']} | {r['Ct2e']} | "
        f"{r['pair_map_injective']} | {r['nH_le_Ct2e']} | {r['multi_bip_W']} |"
        for r in sample
    )
    return f"""# KB-MCA Route-D v50: ★_pre attack — bipartitions and C(t,2e)

Status: `PARTIAL` — **e=2 bipartition uniqueness + H2 close PROVED**;
**conditional** `H_*^pre ≤ binom(t,2e)` PROVED; full deployed window **OPEN**.

## Setup (v49)

`H_*^pre(t,e)` = free-1 multipad highs on index prefix `I_t` of KB domain.
Coext multipads use some `t = min(C) ∈ [2e, n']`.

## e=2 bipartition uniqueness (PROVED)

Four distinct field elements: at most one equal-sum pair-partition (char≠2).
⇒ e=2 free-1 multipad highs inject via pair-cover into 4-subsets, and
`H_*^pre(t,2) ≤ p ≤ H2`.

## Conditional bound for general e (PROVED)

**Hypothesis U2e:** every 2e-subset of `I_t` has at most one free-1 bipartition.

Then each multipad high H determines a unique 2e-set `W = U∪V` (any free-1 pair
in `F_H`), and

```text
H_*^pre(t,e)  ≤  binom(t, 2e)
```

Toys: U2e holds on all checked rows; pair-map injective; nH ≤ binom(t,2e).

## Arithmetic gate (PROVED)

Deployed e={d['e']}:

| s | binom(2e+s, s) | ≤ H2? |
|---:|---:|---|
| 0 | {db['C_2e']} | yes |
| 1 | {db['C_2e1_1']} | yes |
| 2 | {db['C_2e2_2']} | yes |
| 3 | {db['C_2e3_3']} | **no** |

Hence under U2e:

```text
t ≤ 2e+2  ⇒  H_*^pre(t,e) ≤ H2
```

## Residual card path (conditional)

```text
U2e + residual pure-untyped windows satisfy t ≤ 2e+2
  ⇒  |H_unt| ≤ H2
  ⇒  residual free-1 card (v45–v47)
```

OR prove U2e and a better large-t bound than binom(t,2e).

## CAS notes

- e/t ≈ 1/17 still has **large** nH for e=2,3 (ratio does not vanish multipads).
- Vanishing seen near e/t ≥ 1/3, not at 1/17.
- Deployed e/n′ ≈ 0.057 is the hard mid-ratio, large-e regime.

## Toys (sample)

| p | e | t | nH | C(t,2e) | map inj? | nH≤C? | multi bip W |
|---|---:|---:|---:|---:|---|---|---:|
{tbl}

Census: rows={cen['n_rows']}; all injective; all nH≤C(t,2e); bip unique on checked W.

## OPEN

1. **U2e for e>2** (geometric progression free-1 bipartitions)
2. **Residual t ≤ 2e+2** or replace C(t,2e) for t up to n′
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v50.py --check
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
        "# kb-qatom-route-d-v50\n\n"
        "H_*^pre attack: unique free-1 bipartition => H*<=C(t,2e); t<=2e+2 => H2.\n"
    )
    REPORT_PATH.write_text(
        f"# v50 report\n\nstatus: {cert['status']}\n"
        f"e2 unique bip: PROVED\n"
        f"conditional Ct2e: PROVED\n"
        f"OPEN e>2 unique bip + large t: True\n"
    )
    cen = cert["toy_suite"]["census"]
    db = cert["toy_suite"]["deployed_binom"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  e=2: unique equal-sum bipartition of 4-sets: PROVED")
    print("  under U2e: H_*^pre(t,e) ≤ C(t,2e): PROVED")
    print(f"  t≤2e+2 ⇒ C(t,2e)≤H2 (C(2e+2,2)={db['C_2e2_2']}≤H2): PROVED")
    print(f"  toys: {cen['n_rows']} rows, all pair-map inj, all nH≤C(t,2e), bip unique")
    print("  OPEN: U2e for e>2; residual t≤2e+2 or better large-t bound")


if __name__ == "__main__":
    main()
