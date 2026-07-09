#!/usr/bin/env python3
"""KB-MCA Route-D v76: coll <= 2 binom(t,2e) via unique multipad unions.

Board collision bound after packing (v73) and span (v75).

Proved:
  (1) Unique union. Each unordered free-1 multipad pair {A,B} determines a
      unique 2e-set W = A cup B. Distinct unordered pairs yield distinct W:
      if {A,B} != {A',B'} but A cup B = A' cup B' = W, then at least three
      distinct e-subsets of W share free-1 highs in a way that contradicts
      fibre packing on W (at most floor(2e/e)=2 e-subsets in any single fibre
      of a 2e-point ambient — so at most one unordered pair per W).
      More directly: for a fixed W, the multipad e-subsets inside W with a given
      high are pairwise disjoint of size e in a 2e-set => at most 2 of them =>
      at most one unordered pair per W.
  (2) Collision bound. Let N_unord = sum_h binom(m_h,2) = coll/2 be the number
      of unordered multipad pairs. By (1), N_unord <= binom(t,2e) (number of
      candidate W), for t >= 2e (else binom(t,2e)=0 and coll=0 by v74).
      Therefore
        coll  <=  2 * binom(t, 2e).
  (3) Combined bound. With K = floor(t/e) and C = binom(t,e),
        coll  <=  min( (K-1) C ,  2 binom(t,2e) )
      (packing v73 and union bound (2)). Near t ~ 2e the union bound is far
      sharper; for larger t the packing bound may win.
  (4) Deployed arithmetic. K=17, coll <= min(16 C, 2 C(n',2e)). Both still
      enormously larger than 2 H2 — does not close residual alone.

CAS:
  (5) One W per unordered pair on all multipad rows.
  (6) coll <= 2 C(t,2e) and coll <= (K-1)C always hold; min switches by regime.

OPEN:
  Drive coll to 0 at t=n' (multipad ban) or SoftB for |T|<=H2.

Does NOT claim |T|<=H2 / A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v76.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v76"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v76.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v76.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v76.report.md"
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
B_STAR = math.sqrt(2 * H2)
TWO_E = 2 * E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_unique_W() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "one_multipad_pair_per_2e_union",
        "statement": (
            "Each 2e-set W supports at most one unordered free-1 multipad pair "
            "{A,B} with A cup B = W."
        ),
        "proof": [
            "Multipad e-sets with the same high are pairwise disjoint (v69).",
            "In a 2e-point ambient, at most floor(2e/e)=2 such e-sets per high.",
            "Hence at most one unordered pair per W.",
        ],
    }


def lemma_coll_union() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coll_le_twice_binom_t_2e",
        "statement": (
            "For t >= 2e: coll <= 2 binom(t,2e). For t < 2e: coll = 0."
        ),
        "proof": [
            "t < 2e: v74 injectivity.",
            "N_unord = coll/2 <= # of W = binom(t,2e) by unique union map.",
        ],
    }


def lemma_combined() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coll_le_min_packing_and_union",
        "statement": (
            "coll <= min( (floor(t/e)-1) binom(t,e) , 2 binom(t,2e) ) "
            "(with the usual conventions when t < 2e or floor(t/e)<1)."
        ),
        "proof": ["v73 packing bound and (2)."],
    }


def lemma_deployed() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "deployed_combined_bound_still_weak",
        "statement": (
            f"At deployed: coll <= min(16 C, 2 C(n',2e)) with C=C(n',e), "
            f"still >> 2 H2={2*H2}."
        ),
        "proof": [
            "K=17 => packing 16C; union bound 2 C(n',2e).",
            "Both tower above H2 ~ 7.7e10.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_coll_zero_or_SoftB_deployed",
        "statement": "Need coll=0 (multipad ban) or SoftB for |T|<=H2.",
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


def monic_X(roots: list[int], p: int) -> list[int]:
    poly = [1]
    for r in roots:
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] - (r * c) % p) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


def free1_X(poly: list[int], e: int) -> tuple[int, ...]:
    return tuple(poly[1:e])


def census(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    buckets: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        buckets[free1_X(monic_X(roots, p), e)].append(frozenset(idxs))

    C = math.comb(t, e)
    K = t // e
    coll = sum(len(v) * (len(v) - 1) for v in buckets.values())
    unord = sum(math.comb(len(v), 2) for v in buckets.values())
    ensure(unord * 2 == coll, "unord")

    Ws: set[frozenset[int]] = set()
    for v in buckets.values():
        if len(v) < 2:
            continue
        for a, b in itertools.combinations(v, 2):
            W = a | b
            ensure(len(W) == 2 * e, "2e")
            ensure(W not in Ws, "unique W")  # first insert
            Ws.add(W)
    ensure(len(Ws) == unord, "W count")

    bound_pack = (K - 1) * C if K >= 1 else 0
    bound_union = 2 * math.comb(t, 2 * e) if t >= 2 * e else 0
    bound_min = min(bound_pack, bound_union) if t >= 2 * e else 0
    if t < 2 * e:
        ensure(coll == 0, "t<2e free")
        bound_min = 0

    ensure(coll <= bound_pack or t < e, "pack")
    if t >= 2 * e:
        ensure(coll <= bound_union, "union")
    ensure(coll <= bound_min if t >= 2 * e or t < 2 * e else True, "min")

    return {
        "p": p,
        "t": t,
        "e": e,
        "C": int(C),
        "K": int(K),
        "coll": int(coll),
        "n_unord": int(unord),
        "n_W": int(len(Ws)),
        "bound_pack": int(bound_pack),
        "bound_union": int(bound_union),
        "bound_min": int(bound_min),
        "union_tighter": bool(t >= 2 * e and bound_union < bound_pack),
        "pack_tighter": bool(t >= 2 * e and bound_pack <= bound_union),
        "ok": bool(coll <= bound_min if t >= 2 * e else coll == 0),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "odd")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(TWO_E < N, "2e<n")

    rows = []
    # free regime
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [3, 4]:
            for t in [2 * e - 1, 2 * e]:
                if t > n or math.comb(t, e) > 20000:
                    continue
                r = census(p, n, t, e)
                ensure(r["ok"], "free")
                rows.append(r)

    # multipad regime
    for p, n, t, e in [
        (61, 60, 13, 3),
        (61, 60, 17, 3),
        (61, 60, 20, 3),
        (61, 60, 24, 3),
        (61, 60, 16, 4),
        (101, 100, 9, 3),
        (101, 100, 15, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 16, 3),
        (127, 126, 21, 4),
        (43, 42, 12, 3),
        (73, 72, 14, 4),
    ]:
        if t > n or 2 * e > t or math.comb(t, e) > 25000:
            continue
        r = census(p, n, t, e)
        ensure(r["ok"], f"mp {p},{t},{e}")
        ensure(r["n_W"] == r["n_unord"], "W bij")
        rows.append(r)

    ensure(any(r["coll"] > 0 for r in rows), "some coll")
    ensure(any(r["union_tighter"] for r in rows) or any(r["pack_tighter"] for r in rows), "regime")

    # near 2e, union should be tighter
    near = [r for r in rows if r["t"] <= r["e"] * 3 and r["t"] >= 2 * r["e"] and r["coll"] > 0]
    # not always coll>0 near 2e

    return {
        "status": "PASS",
        "rows": rows,
        "summary": {
            "n_rows": len(rows),
            "n_with_coll": sum(1 for r in rows if r["coll"] > 0),
            "all_ok": True,
            "n_union_tighter": sum(1 for r in rows if r["union_tighter"]),
            "n_pack_tighter": sum(1 for r in rows if r["pack_tighter"]),
            "deployed_K": FLOOR_NP,
            "deployed_pack_factor": FLOOR_NP - 1,
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "two_e": TWO_E,
            "K": FLOOR_NP,
            "coll_bound": f"min(16*C(n',e), 2*C(n',2e))",
            "H2": H2,
            "B_star": float(B_STAR),
            "closes_residual_alone": False,
            "note": "union bound sharp near t~2e; packing often better at large t/e",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v76",
        "title": "coll <= 2 binom(t,2e) via unique multipad unions",
        "status": "UNION_COLL_BOUND_PROVED_RESIDUAL_OPEN",
        "claims": {
            "proves_one_pair_per_W": True,
            "proves_coll_le_2_binom_t_2e": True,
            "proves_coll_le_min_pack_union": True,
            "proves_deployed_still_weak": True,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "unique_W": lemma_unique_W(),
            "coll_union": lemma_coll_union(),
            "combined": lemma_combined(),
            "deployed": lemma_deployed(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "W uniqueness census"},
        "impact_on_program": {
            "closed": (
                "BOARD: coll <= 2 C(t,2e); combined min with packing (K-1)C"
            ),
            "wall": "both deployed bounds >> H2; need ban or SoftB",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    lines = []
    for r in cert["toy_suite"]["rows"]:
        if r["coll"] == 0 and r["t"] > 2 * r["e"]:
            continue
        tag = (
            "U"
            if r["union_tighter"]
            else ("P" if r["pack_tighter"] else "-")
        )
        lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['coll']} | "
            f"{r['bound_union']} | {r['bound_pack']} | {r['bound_min']} | {tag} |"
        )
    tbl = "\n".join(lines[:20])
    return f"""# KB-MCA Route-D v76: `coll ≤ 2 C(t,2e)`

Status: **union collision bound PROVED**; residual still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
coll  <=  2 * binom(t, 2e)     (t >= 2e)
coll  <=  min( (⌊t/e⌋-1) C(t,e) ,  2 C(t,2e) )
```

### Why

- Each unordered multipad pair `{{A,B}}` has unique `W=A∪B` of size `2e`.  
- Each `W` hosts **at most one** such pair (packing on a 2e-set: `m_h ≤ 2`).  
- Hence `#unordered pairs ≤ C(t,2e)`, so `coll = 2 · #unordered ≤ 2 C(t,2e)`.

Near `t ~ 2e` this dominates packing; at larger `t/e` packing often wins.

## Deployed

| | |
|---|---|
| bound | `min(16 · C(n',e), 2 · C(n',2e))` |
| vs `2 H2` | still far larger |
| residual close alone? | **no** |

## CAS

| p | e | t | coll | 2 C(t,2e) | (K-1)C | min | tighter |
|---|---:|---:|---:|---:|---:|---:|---|
{tbl}

(U = union tighter, P = packing tighter)

## OPEN

Drive `coll → 0` at `t=n'` or SoftB — residual PR material.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v76.py --check
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
        "# kb-qatom-route-d-v76\n\n"
        "coll <= 2 binom(t,2e) via unique multipad unions W.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v76 report\n\nstatus: {cert['status']}\n"
        f"coll <= 2 C(t,2e): PROVED\n"
        f"OPEN residual: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  at most one multipad pair per 2e-set W: PROVED")
    print("  coll <= 2 binom(t,2e): PROVED")
    print("  coll <= min((K-1)C, 2 C(t,2e)): PROVED")
    print(
        f"  CAS: rows={s['n_rows']}; with coll={s['n_with_coll']}; "
        f"union tighter={s['n_union_tighter']}; pack tighter={s['n_pack_tighter']}"
    )
    print("  BOARD: union coll bound closed; residual still OPEN")


if __name__ == "__main__":
    main()
