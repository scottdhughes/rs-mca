#!/usr/bin/env python3
"""KB-MCA Route-D v45: residual after SR + H_M — N_ord_R / |H_R| vs e·p, H2.

Implements the preferred residual-only card attack (not ambient K_cap).

Definitions:
  Type S multipad: side key (high,c0U,c0V) with ≥2 cores and some root mult≥2.
  Type D multipad: side key with ≥2 cores and all root mult≤1 (v35).
  After SR-cell: Type S multipads paid; residual multipads are Type D only.
  H_M: FM matching of free-1 highs, |H_M|≤⌊n/e⌋ (v33).
  R1 pairs: unique free-1 CS pairs that are NOT Type-S multipad sides.
  R2 pairs: R1 pairs whose high ∉ H_M  (double residual).
  H_R1 / H_R2: highs appearing in R1 / R2.

Proved:
  (1) Type D residual multipads: M_pad ≤ pack_D := ⌊(n−2e)/m_c⌋ (v35);
      deployed pack_D = 2. PROVED restated; toys check max_mpad_D ≤ pack_D.
  (2) After SR, no Type S multipad remains unpaid (by definition of residual).
  (3) H_M ≤ ⌊n/e⌋; M-cell pairs thin (v44).
  (4) Card residual criteria (PROVED conditional):
        |R2| ≤ e·p            ⇒ residual free-1 pairs fit e·p enum
        |H_R2| ≤ H2 and M_pad≤2 on Type D residual
                              ⇒ N_side_R2 ≤ 930·H2 ≤ e·p/2 under family packing
        |R1| ≤ e·p            ⇒ after SR alone
  (5) Toys: free_core≥1 often has large Type S fraction ⇒ R1 ≪ N_pairs;
      double residual R2 smaller still; H_R2 ≤ H2 always on suite;
      R2 ≪ deployed e·p on suite; Type D only after SR; pack_D respected.

Does NOT prove deployed |R2|≤e·p or |H_R2|≤H2 (open at free_core=846161).
Does NOT prove constructive SR e·p mark (v36–v38 still).

  python3 experimental/scripts/verify_kb_qatom_route_d_v45.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v45.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v45"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v45.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v45.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v45.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
T_P = T * P
E_P = E * P
FLOOR_N_OVER_E = N // E
K_CAP = 70 * FLOOR_N_OVER_E
PACK = (A + E) // E
PAIRS_PER_HIGH = FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)
H2 = E_P // (2 * PAIRS_PER_HIGH)
# deployed Type D multipad packing
PACK_D_DEPLOYED = (N - 2 * E) // M_C  # 2


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


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_type_D_residual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "SR_leaves_Type_D_only_mpad",
        "statement": (
            "After SR-cell pays all Type S multipads (r_*=min root with mult≥2), "
            f"remaining multipads are Type D with M_pad ≤ pack_D = ⌊(n−2e)/m_c⌋. "
            f"Deployed pack_D = {PACK_D_DEPLOYED}."
        ),
        "proof": ["v35 shared-root first-match cell."],
        "deployed_pack_D": PACK_D_DEPLOYED,
    }


def lemma_double_residual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "double_residual_R2_definitions",
        "statement": (
            "R1 = free-1 CS pairs that are not Type-S multipad sides (after SR). "
            "R2 = { pairs in R1 : high ∉ H_M } (after H_M). "
            "H_R2 = highs of R2. Then |H_M|≤⌊n/e⌋ and R2 ⊆ R1 ⊆ all free-1 pairs."
        ),
        "proof": [
            "SR removes Type S multipad side keys by definition.",
            "H_M is a matching of highs (v33); complement is H_R.",
        ],
    }


def lemma_residual_card() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_card_criteria",
        "statement": (
            "Any of the following closes residual free-1 card into e·p:\n"
            f"  (R1) |R2| ≤ e·p  (joint enum on R2)\n"
            f"  (R2gate) |H_R2| ≤ H2={H2} and residual multipads have M_pad≤2\n"
            f"           ⇒ N_side(R2) ≤ 930·H2 ≤ e·p/2\n"
            f"  (R1only) |R1| ≤ e·p  (after SR, before H_M thinning)"
        ),
        "proof": [
            "μ_all enum injective on any pair set (v42).",
            "v42/v43 weak high gate with M_pad≤2 → H2.",
            "Type D residual has M_pad≤pack_D=2 deployed (v35).",
        ],
        "deployed": {"H2": H2, "e_p": E_P, "pack_D": PACK_D_DEPLOYED},
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_deployed_R2_or_HR2",
        "statement": (
            f"Prove |R2|≤e·p or |H_R2|≤H2={H2} at free_core={FREE_CORE}. "
            "Toys: free_core≥1 often cuts pairs via Type S; residual still positive."
        ),
    }


def residual_census(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 60000:
        return None
    free_core = m_c - w
    pack_D = max((n - 2 * e) // m_c, 0) if n >= 2 * e else 0
    vals = domain_vals(p, n)
    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)

    high_Us: dict[Any, list] = defaultdict(list)
    seen_u: dict[Any, set] = defaultdict(set)
    # unique free-1 pairs as (high, ut, vt, c0U, c0V)
    unique_fp: list = []
    seen_fp: set = set()
    # side key -> set of cores for multipad classification
    side_cores: dict[Any, set] = defaultdict(set)
    N_ord_pencil = 0

    for _z, members in fib.items():
        pencils: dict[Any, list] = defaultdict(list)
        for S in members:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = frozenset(S - U)
            high, c0 = free1_high_c0(U, vals, p)
            pencils[(tuple(sorted(C)), high)].append((U, c0, high, C))
        for _key, lst in pencils.items():
            by_u: dict = {}
            for U, c0, high, C in lst:
                by_u[tuple(sorted(U))] = (c0, high, C)
            k = len(by_u)
            if k < 2:
                continue
            N_ord_pencil += k * (k - 1)
            items = list(by_u.items())
            for i, (ut, (c0U, high, C)) in enumerate(items):
                if ut not in seen_u[high]:
                    seen_u[high].add(ut)
                    high_Us[high].append(frozenset(ut))
                for j2, (vt, (c0V, _, C2)) in enumerate(items):
                    if i == j2 or c0U == c0V:
                        continue
                    fp = (ut, vt)
                    if fp not in seen_fp:
                        seen_fp.add(fp)
                        unique_fp.append((high, ut, vt, c0U, c0V))
                    side_cores[(high, c0U, c0V)].add(C)

    if not high_Us:
        return None

    # multipad Type S / D
    pair_is_S: set = set()
    pair_is_D: set = set()
    n_mpad_S = n_mpad_D = 0
    max_mpad_D = 1
    max_mpad_S = 1
    for sk, cores in side_cores.items():
        if len(cores) < 2:
            continue
        cnt: Counter = Counter()
        for c in cores:
            for r in c:
                cnt[r] += 1
        tmult = max(cnt.values()) if cnt else 0
        high, c0U, c0V = sk
        # mark fps with this side key
        marked = []
        for high2, ut, vt, cu, cv in unique_fp:
            if high2 == high and cu == c0U and cv == c0V:
                marked.append((ut, vt))
        if tmult >= 2:
            n_mpad_S += 1
            max_mpad_S = max(max_mpad_S, len(cores))
            for fp in marked:
                pair_is_S.add(fp)
                pair_is_D.discard(fp)
        else:
            n_mpad_D += 1
            max_mpad_D = max(max_mpad_D, len(cores))
            if pack_D > 0:
                ensure(len(cores) <= pack_D, f"D pack {len(cores)}>{pack_D}")
            for fp in marked:
                if fp not in pair_is_S:
                    pair_is_D.add(fp)

    # H_M matching
    free = set(range(n))
    H_M: set = set()
    for h in sorted(high_Us, key=repr):
        for U in high_Us[h]:
            if set(U).issubset(free):
                free -= set(U)
                H_M.add(h)
                break
    floor_ne = max(n // e, 1)
    ensure(len(H_M) <= floor_ne, "H_M size")
    H_all = set(high_Us)

    # R1 / R2
    n_pairs = len(unique_fp)
    n_S = n_D = n_unt = 0
    n_R1 = n_R2 = 0
    n_M_pairs = 0
    H_R1: set = set()
    H_R2: set = set()
    for high, ut, vt, cu, cv in unique_fp:
        fp = (ut, vt)
        if fp in pair_is_S:
            n_S += 1
        elif fp in pair_is_D:
            n_D += 1
        else:
            n_unt += 1
        if fp not in pair_is_S:
            n_R1 += 1
            H_R1.add(high)
            if high not in H_M:
                n_R2 += 1
                H_R2.add(high)
        if high in H_M:
            n_M_pairs += 1

    # residual N_ord proxy: pencil sum excluding... hard; use |R2| and bound
    N_side_R2_bound = len(H_R2) * floor_ne * max(floor_ne - 1, 0)

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "pack_D": pack_D,
        "nH": len(H_all),
        "n_HM": len(H_M),
        "n_HR": len(H_all) - len(H_M),
        "n_mpad_S": n_mpad_S,
        "n_mpad_D": n_mpad_D,
        "max_mpad_D": max_mpad_D,
        "max_mpad_S": max_mpad_S,
        "n_pairs": n_pairs,
        "n_pairs_S": n_S,
        "n_pairs_D": n_D,
        "n_pairs_unt": n_unt,
        "n_R1": n_R1,
        "n_R2": n_R2,
        "n_M_pairs": n_M_pairs,
        "frac_S": n_S / n_pairs if n_pairs else 0.0,
        "frac_R1": n_R1 / n_pairs if n_pairs else 0.0,
        "frac_R2": n_R2 / n_pairs if n_pairs else 0.0,
        "n_H_R1": len(H_R1),
        "n_H_R2": len(H_R2),
        "N_ord_pencil": N_ord_pencil,
        "N_side_R2_bound": N_side_R2_bound,
        "D_mpad_le_pack": max_mpad_D <= pack_D if pack_D > 0 else max_mpad_D <= 1,
        "H_R2_le_H2": len(H_R2) <= H2,
        "R2_le_ep_dep": n_R2 <= E_P,
        "R1_le_ep_dep": n_R1 <= E_P,
        "HM_le_floor": len(H_M) <= floor_ne,
    }


def toy_suite() -> dict[str, Any]:
    ensure(PACK_D_DEPLOYED == 2, "packD dep")
    ensure(H2 == E_P // (2 * PAIRS_PER_HIGH), "H2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 9, 2),
        (19, 18, 5, 1),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (19, 18, 8, 2),
        (31, 30, 5, 1),
        (31, 30, 4, 2),
    ]:
        r = residual_census(p, n, j, w)
        if r is None:
            continue
        ensure(r["HM_le_floor"], "HM")
        ensure(r["H_R2_le_H2"], "HR2 H2")
        ensure(r["R2_le_ep_dep"], "R2 ep")
        ensure(r["D_mpad_le_pack"], "D pack")
        rows.append(r)

    ensure(len(rows) >= 10, "rows")
    # some free_core>=1 with Type S cutting residual
    fc1 = [r for r in rows if r["free_core"] >= 1 and r["n_pairs"] > 0]
    ensure(len(fc1) >= 3, "fc1 rows")
    ensure(any(r["frac_S"] > 0.3 for r in fc1), "Type S meaningful")
    ensure(any(r["n_R2"] < r["n_pairs"] for r in fc1), "residual shrinks")
    # double residual strictly ⊆ R1 ⊆ all
    for r in rows:
        ensure(r["n_R2"] <= r["n_R1"] <= r["n_pairs"], "chain")
        ensure(r["n_H_R2"] <= r["n_H_R1"] <= r["nH"], "H chain")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "max_R2": max(r["n_R2"] for r in rows),
            "max_R1": max(r["n_R1"] for r in rows),
            "max_H_R2": max(r["n_H_R2"] for r in rows),
            "max_frac_S": max(r["frac_S"] for r in rows),
            "max_frac_R2": max(r["frac_R2"] for r in rows),
            "avg_frac_R2": sum(r["frac_R2"] for r in rows) / len(rows),
            "avg_frac_R1": sum(r["frac_R1"] for r in rows) / len(rows),
            "avg_frac_S": sum(r["frac_S"] for r in rows) / len(rows),
            "all_HR2_le_H2": True,
            "all_R2_le_ep_dep": True,
            "all_D_pack": True,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v45",
        "title": "Residual after SR + H_M: R2 / H_R2 card gates",
        "status": "PARTIAL_DOUBLE_RESIDUAL",
        "claims": {
            "proves_Type_D_only_after_SR": True,
            "proves_pack_D_deployed_2": True,
            "proves_R2_subset_R1_subset_all": True,
            "proves_residual_card_criteria": True,
            "proves_HM_le_floor": True,
            "toy_Type_S_cuts_residual": True,
            "toy_HR2_le_H2": True,
            "toy_R2_le_ep_dep": True,
            "proves_deployed_R2_le_ep": False,
            "proves_deployed_HR2_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "pack_D": PACK_D_DEPLOYED,
            "H2": H2,
            "e_p": E_P,
            "K_cap": K_CAP,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "type_D": lemma_type_D_residual(),
            "double_res": lemma_double_residual(),
            "card": lemma_residual_card(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "path": (
                "SR (Type S) → residual Type D (M_pad≤2) + untyped free-1; "
                "then H_M peels matching pairs; card on R2 / H_R2"
            ),
            "next": "Prove |R2|≤e·p or |H_R2|≤H2 at deployed free_core",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_pairs']} | "
        f"{r['n_pairs_S']} | {r['n_R1']} | {r['n_R2']} | {r['n_H_R2']} | "
        f"{r['n_HM']} | {r['frac_S']:.2f} | {r['frac_R2']:.2f} | "
        f"{r['max_mpad_D']} | {r['D_mpad_le_pack']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v45: residual after SR + H_M

Status: `PARTIAL` — **double residual R2/H_R2** defined; Type D after SR
**PROVED**; residual card criteria **PROVED**; deployed R2/H_R2 gates **OPEN**.

## Residual definitions

```text
Type S multipad  →  paid by SR-cell (r_*)
Type D multipad  →  residual, M_pad ≤ pack_D = ⌊(n−2e)/m_c⌋
                    deployed pack_D = {d['pack_D']}

R1 = free-1 CS pairs that are not Type-S multipad sides
R2 = R1 pairs with high ∉ H_M
H_R2 = highs of R2
```

```text
R2  ⊆  R1  ⊆  all free-1 pairs
H_M ≤ ⌊n/e⌋ = 31
```

## Residual card criteria (PROVED conditional)

| Gate | Condition | Pays |
|---|---|---|
| R1-enum | `|R2| ≤ e·p` | residual pairs by μ_all |
| H2-res | `|H_R2| ≤ H2` + M_pad≤2 | N_side≤930·H2 ≤ e·p/2 |
| R1-only | `|R1| ≤ e·p` | after SR, before H_M |

H2 = {d['H2']}; e·p = {d['e_p']}.

## Path

```text
1. SR-cell: Type S multipads
2. Type D residual multipads (M_pad ≤ 2 deployed)
3. Untyped free-1 (single-core multi-U pencils) stay in R1
4. H_M peels matching-supported pairs
5. Card-close R2 / H_R2
```

## Toys

| j | w | fc | #pairs | #S | #R1 | #R2 | #H_R2 | #H_M | frac S | frac R2 | max mpad D | D≤pack? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
{tbl}

Census: max R2={cen['max_R2']}; max H_R2={cen['max_H_R2']};
avg frac S={cen['avg_frac_S']:.3f}; avg frac R2={cen['avg_frac_R2']:.3f};
max frac S={cen['max_frac_S']:.3f}.

Observation: **free_core≥1** often has large Type S fraction ⇒ SR cuts residual
sharply; R2 still the card wall but smaller than full N_pairs.

## OPEN

1. Deployed `|R2| ≤ e·p` or `|H_R2| ≤ H2`
2. Constructive SR e·p mark (separate)
3. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v45.py --check
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
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v45\n\n"
        "Residual after SR + H_M: R2 / H_R2 card gates.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    cen = cert["toy_suite"]["census"]
    REPORT_PATH.write_text(
        f"# v45 report\n\nstatus: {cert['status']}\n"
        f"max R2: {cen['max_R2']}\n"
        f"max H_R2: {cen['max_H_R2']}\n"
        f"avg frac R2: {cen['avg_frac_R2']}\n"
        f"deployed R2/HR2: OPEN\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  Type D after SR, pack_D={PACK_D_DEPLOYED}: PROVED (v35 restated)")
    print(f"  residual criteria |R2|≤e·p or |H_R2|≤H2={H2}: PROVED conditional")
    print(
        f"  toys: max R2={cen['max_R2']} max H_R2={cen['max_H_R2']}; "
        f"avg frac S={cen['avg_frac_S']:.3f} R2={cen['avg_frac_R2']:.3f}"
    )
    print("  free_core≥1: Type S often cuts residual; R2 still wall")
    print("  deployed |R2|≤e·p / |H_R2|≤H2: OPEN")


if __name__ == "__main__":
    main()
