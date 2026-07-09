#!/usr/bin/env python3
"""KB-MCA Route-D v73: free-1 high fibre packing m_h <= floor(t/e).

Board-facing corollary of disjoint multipads (v69).

Proved:
  (1) Fibre packing. Fix ambient t-set (e.g. GP prefix I_t) and free-1 high h.
      Let F_h = { e-subsets U : high(U)=h }. For any distinct U,V in F_h, (U,V) is
      a free-1 multipad, hence U cap V = empty (v69). Therefore the members of
      F_h are pairwise disjoint e-subsets of a t-set, so
        m_h := |F_h|  <=  floor(t/e).
  (2) Threshold recovery. If t < 2e then floor(t/e)=1, so m_h <= 1 for all h,
      i.e. free-1 high is injective, coll=0, |T|=0 (v68-v69).
  (3) Collision bound. With C = binom(t,e) = sum_h m_h and K = floor(t/e),
        coll = sum_h m_h(m_h-1)  <=  (K-1) sum_h m_h  = (K-1) C,
      since m_h-1 <= K-1 whenever m_h <= K.
  (4) Deployed pack. K = floor(n'/e) = 17, so coll <= 16 C (still >> H2; does
      not close residual alone). Marks the packing ceiling on the board.

CAS:
  (5) All fibres respect m_h <= floor(t/e) on tested rows.
  (6) t < 2e: all m_h <= 1.
  (7) Observed max m_h often < pack bound; coll <= (K-1)C holds.

OPEN:
  Deployed multipad ban / SoftB for |T|<=H2 (packing alone insufficient).

Does NOT claim |T|<=H2 or A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v73.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v73"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v73.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v73.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v73.report.md"
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
FLOOR_NP = N_PRIME // E  # = 17
B_STAR = math.sqrt(2 * H2)


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_fibre_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_fibre_packing",
        "statement": (
            "For any free-1 high h on e-subsets of a t-set: "
            "m_h = |{U : high(U)=h}| <= floor(t/e)."
        ),
        "proof": [
            "Distinct U,V with high(U)=high(V) are multipads => U cap V = empty (v69).",
            "Pairwise disjoint e-subsets of a t-set: at most floor(t/e) of them.",
        ],
    }


def lemma_threshold_recovery() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "packing_recovers_t_lt_2e_injectivity",
        "statement": (
            "t < 2e => floor(t/e)=1 => m_h <= 1 for all h => injective => |T|=0."
        ),
        "proof": ["Special case of fibre packing + v68."],
    }


def lemma_coll_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coll_le_pack_minus_one_times_C",
        "statement": (
            "With K=floor(t/e) and C=binom(t,e): coll = sum m(m-1) <= (K-1)C."
        ),
        "proof": [
            "m_h <= K => m_h(m_h-1) <= (K-1) m_h.",
            "Sum over h: coll <= (K-1) sum m_h = (K-1)C.",
        ],
    }


def lemma_deployed_pack() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "deployed_pack_ceiling_17",
        "statement": (
            f"At deployed n'={N_PRIME}, e={E}: K=floor(n'/e)={FLOOR_NP}, "
            f"hence m_h <= {FLOOR_NP} and coll <= {FLOOR_NP - 1} C."
        ),
        "proof": ["Arithmetic: n'//e = 17."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_deployed_multipad_ban_or_SoftB",
        "statement": (
            "Packing coll <= 16 C is far above 2 H2; still need multipad ban or SoftB."
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
    buckets: dict[tuple[int, ...], list[set[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        h = free1_X(monic_X(roots, p), e)
        buckets[h].append(set(idxs))

    C = math.comb(t, e)
    K = t // e
    ms = [len(v) for v in buckets.values()]
    max_m = max(ms) if ms else 0
    coll = sum(m * (m - 1) for m in ms)
    # verify pairwise disjoint inside each fibre
    disjoint_ok = True
    for v in buckets.values():
        if len(v) < 2:
            continue
        for A, B in itertools.combinations(v, 2):
            if A & B:
                disjoint_ok = False
                break
        if not disjoint_ok:
            break

    pack_ok = all(m <= K for m in ms)
    coll_bound = (K - 1) * C if K >= 1 else 0
    coll_ok = coll <= coll_bound

    return {
        "p": p,
        "t": t,
        "e": e,
        "C": int(C),
        "K_floor_t_over_e": int(K),
        "max_m": int(max_m),
        "coll": int(coll),
        "coll_bound_Km1_C": int(coll_bound),
        "pack_ok": bool(pack_ok),
        "coll_ok": bool(coll_ok),
        "disjoint_ok": bool(disjoint_ok),
        "injective": bool(max_m <= 1),
        "t_lt_2e": bool(t < 2 * e),
        "n_highs": len(buckets),
        "n_multipad_highs": sum(1 for m in ms if m >= 2),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "pack deployed")
    ensure(N_PRIME // E == 17, "n'/e")

    rows = []
    # threshold regime
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [3, 4, 5]:
            for t in [e + 1, 2 * e - 1]:
                if t > n or math.comb(t, e) > 20000:
                    continue
                r = census(p, n, t, e)
                ensure(r["t_lt_2e"], " thr")
                ensure(r["pack_ok"], "pack")
                ensure(r["injective"], "inj")
                ensure(r["disjoint_ok"], "disj")
                ensure(r["coll"] == 0, "coll0")
                rows.append(r)

    # multipad regime
    for p, n, t, e in [
        (61, 60, 13, 3),
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (61, 60, 30, 3),
        (101, 100, 9, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 16, 3),
        (127, 126, 21, 4),
        (61, 60, 16, 4),
        (61, 60, 21, 4),
    ]:
        if t > n or math.comb(t, e) > 40000:
            continue
        r = census(p, n, t, e)
        ensure(r["pack_ok"], f"pack {p},{t},{e} max_m={r['max_m']} K={r['K_floor_t_over_e']}")
        ensure(r["coll_ok"], "coll bound")
        ensure(r["disjoint_ok"], "disj")
        rows.append(r)

    ensure(any(r["n_multipad_highs"] > 0 for r in rows), "some multipads")
    ensure(all(r["pack_ok"] for r in rows), "all pack")

    # deployed arithmetic
    K = FLOOR_NP
    # cannot compute C = binom(n',e) fully; use log
    # coll bound (K-1)C vs 2 H2: still open that coll is small
    deployed = {
        "n_prime": N_PRIME,
        "e": E,
        "K": K,
        "coll_bound_factor_Km1": K - 1,
        "H2": H2,
        "B_star": float(B_STAR),
        "packing_closes_residual_alone": False,
        "note": f"m_h <= {K}; coll <= {K-1} C (insufficient alone for H2)",
    }

    return {
        "status": "PASS",
        "rows": rows,
        "summary": {
            "n_rows": len(rows),
            "n_with_multipads": sum(1 for r in rows if r["n_multipad_highs"] > 0),
            "all_pack_ok": True,
            "all_coll_bound_ok": True,
            "all_disjoint_ok": True,
            "max_observed_max_m": max(r["max_m"] for r in rows),
            "deployed_K": K,
        },
        "deployed": deployed,
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v73",
        "title": "Free-1 high fibre packing m_h <= floor(t/e)",
        "status": "FIBRE_PACKING_PROVED_RESIDUAL_STILL_OPEN",
        "claims": {
            "proves_fibre_packing_m_le_floor_t_over_e": True,
            "proves_packing_recovers_t_lt_2e": True,
            "proves_coll_le_Km1_C": True,
            "proves_deployed_pack_K_17": True,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "fibre_packing": lemma_fibre_packing(),
            "threshold_recovery": lemma_threshold_recovery(),
            "coll_bound": lemma_coll_bound(),
            "deployed_pack": lemma_deployed_pack(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "fibre census on GP arcs"},
        "impact_on_program": {
            "closed": (
                "BOARD: m_h <= floor(t/e); coll <= (K-1)C; unifies t<2e injectivity"
            ),
            "wall": "K=17 pack bound too weak alone; need multipad ban or SoftB",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    lines = []
    for r in cert["toy_suite"]["rows"]:
        lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['K_floor_t_over_e']} | "
            f"{r['max_m']} | {r['coll']} | {r['coll_bound_Km1_C']} | "
            f"{r['n_multipad_highs']} | {'Y' if r['pack_ok'] else 'n'} |"
        )
    tbl = "\n".join(lines)
    return f"""# KB-MCA Route-D v73: fibre packing `m_h ≤ ⌊t/e⌋`

Status: **fibre packing PROVED** (board row); residual `|T|≤H2` still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
m_h := #{{ e-subsets with free-1 high h }}  <=  floor(t/e)
```

### Proof

Any two distinct e-sets with the same free-1 high are multipads ⇒ **disjoint** (v69).  
Pairwise disjoint e-subsets of a t-set ⇒ at most `⌊t/e⌋` of them.

### Corollaries (PROVED)

| claim | result |
|---|---|
| `t < 2e` | `⌊t/e⌋=1` ⇒ injective ⇒ `\|T\|=0` (recovers v69) |
| collisions | `coll = Σ m(m-1) ≤ (K-1) C` with `K=⌊t/e⌋`, `C=binom(t,e)` |
| deployed | `K = ⌊n'/e⌋ = 17` ⇒ `m_h ≤ 17`, `coll ≤ 16 C` |

## Deployed

| | |
|---|---:|
| n' | {d['n_prime']} |
| e | {d['e']} |
| K = ⌊n'/e⌋ | **{d['K']}** |
| coll ≤ | `16 · C` |
| closes residual alone? | **no** (still ≫ H2) |

## CAS

| p | e | t | K | max m | coll | (K-1)C | #mp highs | pack ok? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
{tbl}

- all rows: packing + disjointness + coll bound hold  
- max observed `max m` = {s['max_observed_max_m']}

## Link

| item | status |
|---|---|
| multipads disjoint | CLOSED (v69) |
| H gap law | CLOSED (v72) |
| **fibre packing m_h≤⌊t/e⌋** | **CLOSED (v73)** |
| deployed multipad ban / SoftB | OPEN |
| `\|T\|≤H2` | OPEN |

## OPEN

Packing is board-true but not residual-final. Next residual board hit remains:
ban multipads at deployed or SoftB.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v73.py --check
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
        "# kb-qatom-route-d-v73\n\n"
        "Free-1 high fibre packing m_h <= floor(t/e); coll <= (K-1)C.\n"
    )
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    REPORT_PATH.write_text(
        f"# v73 report\n\nstatus: {cert['status']}\n"
        f"fibre packing: PROVED\n"
        f"deployed K={d['K']}\n"
        f"OPEN residual: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  m_h <= floor(t/e): PROVED (pairwise disjoint multipads)")
    print("  recovers t<2e injectivity: PROVED")
    print("  coll <= (K-1)C: PROVED")
    print(f"  deployed K={d['K']}; coll <= {d['coll_bound_factor_Km1']} C (not enough alone)")
    print(
        f"  CAS: rows={s['n_rows']}; multipad rows={s['n_with_multipads']}; "
        f"max max_m={s['max_observed_max_m']}"
    )
    print("  BOARD: packing closed; residual still OPEN")


if __name__ == "__main__":
    main()
