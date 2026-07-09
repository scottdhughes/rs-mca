#!/usr/bin/env python3
"""KB-MCA Route-D v14: residual mass atom re-anchor (on-track).

After v8–v13 multi-mate geometry (banked), return to the north-star residual
mass bound for ledger residual R(z) at KB-MCA a+=1116048.

Proved:
  (1) Residual mass criteria (exact arithmetic): pack / p-cover / t*p / n*p
      sufficient conditions for residual flatness or E1-style D_prim budgets.
  (2) Lex dual on residual: R(z) injects into C_res(z) × F_p via
      S |-> (C_can(S), c_U(S)); hence |R| ≤ p · N_can_prim and N_can_prim ≤ |R|.
  (3) Routing dual (imported v5/v11): N_can_prim ≤ U_res · M_m^{res,side}
      and N_can_prim ≤ U_phi · M_m^{res,phi}.
  (4) Bridge: any injection of residual can-cores into a label set of size ≤ B
      yields N_can_prim ≤ B; B ≤ target/17 closes pack residual atom;
      B ≤ t yields |R| ≤ t·p via p-cover.
  (5) Bridge: any injection of residual supports into a set of size ≤ n·p
      (E5) or ≤ t·p (E2) yields |R| ≤ that size, hence residual flatness
      (both fit under target_floor).
  (6) Toy bank: naive residual can-core maps into D×F_p (min, b1), (min, c0),
      (min, Phi_w) are NOT injective on aperiodic residual-proxy cores in general
      (collisions exist). min_b nearly injective on some toys (max fiber 2) but
      not a proof. S |-> (min S, c_U) fails badly.

Does NOT prove residual injection or atom close.
Does not claim U(1116048) ≤ B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v14.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v14.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v14"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v14.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v14.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v14.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
K_DIM = 2**20
T = A - K_DIM  # 67472
W = T - 1
E = W + 1
M = J - E
PACK = 17
B_STAR = (P**6 - 1) // 2**128
B_GEN = T * P
B_QUOT_TERM = math.comb(32, 14) + math.comb(16, 7)
B_PAID = B_GEN + B_QUOT_TERM
B_REM = B_STAR - B_PAID
K_REM = 4_805_007
TARGET = 274_836_936_291_722_953  # K_rem residual floor used across Route-D
N_P = N * P
T_P = T * P
TARGET_OVER_PACK = TARGET // PACK
T_P_OVER_PACK = T_P // PACK


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_int(x: int) -> float:
    return math.log2(x) if x > 0 else float("-inf")


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


def lemma_north_star() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_PROGRAM_LAW",
        "name": "residual_mass_north_star",
        "statement": (
            "The Route-D north star is residual mass for ledger residual R(z) at "
            "KB-MCA a+=1116048 (first-match residual of j-supports), not global "
            "multi-mate taxonomy. Sufficient forms include:\n"
            "  (K_rem) max_z |R(z)| ≤ TARGET (residual flatness / pack atom);\n"
            "  (E1)    |G_gen_support| + |D_full_rank_prim| ≤ t·p;\n"
            "  (E2)    residual supports inject into a set of size ≤ t·p;\n"
            "  (E5)    residual supports inject into D × F_p (size n·p).\n"
            "Covering+routing reduce (K_rem) to bounds on N_can_prim, U_res, "
            "M_m^{res}, or U_phi (v4–v11). Multi-mate geometry (v8–v13) only "
            "constrains M_m / M_m^{res} structure; it does not replace mass."
        ),
        "deployed_TARGET": TARGET,
        "deployed_t_p": T_P,
        "deployed_n_p": N_P,
        "source_ledger": (
            "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
        ),
        "source_v1_forms": "experimental/notes/thresholds/kb_qatom_route_d_v1.md E1–E5",
    }


def lemma_mass_arithmetic() -> dict[str, Any]:
    # Exact gates
    ensure(PACK == 17, "pack")
    ensure(TARGET_OVER_PACK == TARGET // PACK, "div")
    ensure(N_P == N * P, "np")
    ensure(T_P == T * P, "tp")
    ensure(PACK * N_P <= TARGET, "17*n*p fits target")
    ensure(PACK * T_P <= TARGET, "17*t*p fits target")
    ensure(N_P <= TARGET_OVER_PACK, "n*p <= target/17")
    ensure(T_P <= TARGET_OVER_PACK, "t*p <= target/17")
    ensure(T_P + 11440 < TARGET, "v1 slack form")
    return {
        "status": "PROVED_BY_EXACT_INTEGER_ARITHMETIC",
        "name": "residual_mass_sufficient_budgets",
        "statement": (
            "With pack_ceil=17 and TARGET the Route-D residual floor:\n"
            "  (P1) If max N_can_prim ≤ floor(TARGET/17), then max |R| ≤ TARGET "
            "by residual lex covering (v4).\n"
            "  (P2) If max N_can_prim ≤ n·p, then max |R| ≤ 17·n·p ≤ TARGET "
            f"(17·n·p = {PACK * N_P}).\n"
            "  (P3) If max N_can_prim ≤ t·p, then max |R| ≤ 17·t·p ≤ TARGET.\n"
            "  (P4) If max N_can_prim ≤ t, then max |R| ≤ p·N_can_prim ≤ t·p "
            "by the p-covering |R| ≤ p·N_can (v3), which is the E1/E2 scale "
            "for residual mass alone (before adding G_gen).\n"
            "  (P5) If residual supports inject into a set of size ≤ n·p (E5) or "
            "≤ t·p (E2), then |R| ≤ that size ≤ TARGET."
        ),
        "proof": [
            "v4: |R| ≤ pack · N_can_prim with pack=17.",
            "v3: |R| ≤ p · N_can_prim via S |-> (C_can, c_U).",
            "Direct comparison of integers PACK*N_P, PACK*T_P, N_P, T_P, TARGET.",
            "v1 retained lift 11440 only needed for additive E1 with G_gen; "
            "pure residual mass |R|≤t·p already fits TARGET with large slack.",
        ],
        "numbers": {
            "TARGET": TARGET,
            "TARGET_over_pack": TARGET_OVER_PACK,
            "n_p": N_P,
            "t_p": T_P,
            "pack_n_p": PACK * N_P,
            "pack_t_p": PACK * T_P,
            "log2_TARGET_over_pack": log2_int(TARGET_OVER_PACK),
            "log2_n_p": log2_int(N_P),
            "log2_t_p": log2_int(T_P),
            "slack_TARGET_minus_pack_n_p": TARGET - PACK * N_P,
            "slack_bits_pack_n_p": log2_int(TARGET) - log2_int(PACK * N_P),
        },
    }


def lemma_lex_dual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_lex_dual_mass",
        "statement": (
            "On any residual family R(z) ⊆ Fib_w^{(j)}(z), the map "
            "φ: S ↦ (C_can(S), c_U(S)) is injective (v3/v4). Therefore "
            "|R(z)| ≤ p · N_can_prim(z) and N_can_prim(z) ≤ |R(z)|. "
            "Equivalently residual supports inject into C_res(z) × F_p."
        ),
        "proof": [
            "v3 lex-split injection depends only on shared prefix z and the "
            "core-pencil theorem, not on exhausting the full fiber; v4 applies "
            "it to residual.",
            "Image of φ lands in C_res × F_p; injectivity gives |R| ≤ p·|C_res|.",
            "C_can surjects onto C_res by definition, so N_can_prim ≤ |R|.",
        ],
    }


def lemma_routing_dual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_routing_mass_dual",
        "statement": (
            "N_can_prim(z) ≤ U_res(z) · M_m^{res,side}(z) and "
            "N_can_prim(z) ≤ U_phi(z) · M_m^{res,phi}(z) (v5/v10/v11). "
            "Hence residual mass is controlled by either a residual uniqueness "
            "bound on M_m^{res,*} or a residual image bound on U_res / U_phi, "
            "or both."
        ),
        "proof": ["Imported residual routing from v5/v11; residual-restricted."],
        "primary_open": [
            "M_m^{res,side} ≤ 1 (or small K_res)",
            "U_phi ≤ floor(TARGET/17) (B2 residual can-core Phi_w-image)",
            "residual support injection |R| ≤ t·p or n·p (E2/E5)",
            "residual can-core injection N_can ≤ n·p or t (core E5/E2)",
        ],
    }


def lemma_injection_bridges() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "injection_bridges_to_mass",
        "statement": (
            "Bridge A (supports): If there is an injection "
            "ι: R(z) → L with |L| ≤ B for every z, then max |R| ≤ B. "
            "Taking B = t·p recovers E2-scale residual mass; B = n·p recovers E5.\n"
            "Bridge B (cores): If there is an injection "
            "κ: C_res(z) → L with |L| ≤ B, then N_can_prim ≤ B. "
            "With B ≤ floor(TARGET/17), pack residual atom closes (P1). "
            "With B ≤ t, p-cover gives |R| ≤ t·p (P4).\n"
            "Bridge C (routing): If M_m^{res,phi} ≤ 1 then N_can_prim = U_phi, "
            "so a U_phi ≤ floor(TARGET/17) bound is equivalent to pack atom."
        ),
        "proof": [
            "Cardinality of domain ≤ cardinality of codomain under injection.",
            "Combine with lemma_mass_arithmetic (P1)/(P4) and routing dual.",
        ],
        "note": (
            "These bridges are the correct attack surface. v8–v13 constrain "
            "possible multi-mate structure inside fibers of κ or inside M_m^{res}; "
            "they are not themselves mass bounds."
        ),
    }


def lemma_open_res_mass() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_RES_MASS",
        "statement": (
            "Prove one of the following for ledger residual R(z) at deployed "
            "KB-MCA a+=1116048 (not merely aperiodic proxy):\n"
            "  (i)   max |R(z)| ≤ TARGET;\n"
            "  (ii)  max N_can_prim(z) ≤ floor(TARGET/17);\n"
            "  (iii) residual supports inject into a set of size ≤ n·p or ≤ t·p;\n"
            "  (iv)  residual can-cores inject into a set of size ≤ floor(TARGET/17) "
            "or ≤ n·p or ≤ t;\n"
            "  (v)   M_m^{res} ≤ 1 and U_phi ≤ floor(TARGET/17) "
            "(or U_res with side routing).\n"
            "Any one upgrades Route-D conditional closure toward residual atom "
            "(still subject to other first-match branches for full U≤B*)."
        ),
        "falsifier": (
            "A ledger-residual leaf z with |R(z)| > TARGET, or with N_can_prim "
            "larger than every proved budget under the claimed injection, after "
            "the named first-match deletions."
        ),
        "do_not": [
            "Re-prove global M_m ≤ 1 (refuted v8)",
            "Replace ledger residual by aperiodic proxy without justification",
            "Stack more multi-mate taxonomy without a mass bound",
        ],
    }


def lemma_naive_injection_bank() -> dict[str, Any]:
    return {
        "status": "PROVED_NEGATIVE_TOY_BANK",
        "name": "naive_core_injections_fail_on_proxy",
        "statement": (
            "On aperiodic residual-proxy can-cores for small dyadic (p,n), the maps "
            "C ↦ min(C), C ↦ (min(C), c_0), C ↦ (min(C), c_{m-1}), "
            "C ↦ (min(C), Phi_w(C)), and S ↦ (min(S), c_U) are not injective in "
            "general. Therefore these naive marks do not prove Bridge B/A at toy "
            "scale; a residual injection proof needs ledger structure or a "
            "different label."
        ),
        "proof": [
            "Computational certificates in toy_suite: collision max fibers > 1 "
            "for listed schemes on multiple (j,w) rows.",
            "min_b = (min, Phi_w) can be nearly injective (max fiber 2 on some "
            "rows) but still collides — not a proof.",
        ],
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    for p, n, j, w in [
        (17, 16, 9, 2),
        (17, 16, 7, 2),
        (17, 16, 10, 3),
        (17, 16, 9, 3),
        (17, 16, 6, 2),
    ]:
        e = w + 1
        m = j - e
        if m <= 0 or math.comb(n, j) > 12000:
            continue
        vals = domain_vals(p, n)
        # Group residual-proxy supports by Phi_w fiber z (lex dual is per fiber)
        by_z: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            if not aperiodic(S, n):
                continue
            z = phi_w(monic_rev([vals[i] for i in sorted(S)], p), w)
            by_z[z].append(S)

        residual_S = [S for mem in by_z.values() for S in mem]
        cores: list[frozenset[int]] = []
        for S in residual_S:
            ss = sorted(S)
            U = frozenset(ss[:e])
            cores.append(S - U)
        uniq_cores = list({tuple(sorted(c)): c for c in cores}.values())

        def core_lab(C: frozenset[int], sch: str) -> Any:
            pts = [vals[i] for i in sorted(C)]
            poly = monic_rev(pts, p)
            if sch == "min":
                return min(C)
            if sch == "min_c0":
                return (min(C), poly[-1])
            if sch == "min_b1":
                return (min(C), poly[1] if len(poly) > 1 else 0)
            if sch == "min_b":
                return (min(C), phi_w(poly, w))
            raise KeyError(sch)

        scheme_stats = {}
        for sch in ["min", "min_c0", "min_b1", "min_b"]:
            inv: dict[Any, int] = defaultdict(int)
            for C in uniq_cores:
                inv[core_lab(C, sch)] += 1
            scheme_stats[sch] = {
                "n_cores": len(uniq_cores),
                "n_labels": len(inv),
                "max_fiber": max(inv.values()) if inv else 0,
                "injective": max(inv.values(), default=0) <= 1,
            }

        # Per-fiber lex dual S -> (C, c_U)
        lex_ok = True
        max_lex_fiber = 1
        inv_min_cu: dict[Any, int] = defaultdict(int)
        total_lex_labels = 0
        for _z, mem in by_z.items():
            inv_lex: dict[Any, int] = defaultdict(int)
            for S in mem:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                polyU = monic_rev([vals[i] for i in sorted(U)], p)
                cU = polyU[-1]
                inv_lex[(tuple(sorted(C)), cU)] += 1
                inv_min_cu[(min(S), cU)] += 1
            mf = max(inv_lex.values()) if inv_lex else 1
            max_lex_fiber = max(max_lex_fiber, mf)
            if mf > 1:
                lex_ok = False
            total_lex_labels += len(inv_lex)
        ensure(lex_ok, "lex dual must inject per residual-proxy fiber")

        n_R = len(residual_S)
        n_can = len(uniq_cores)
        ensure(n_can <= n_R, "Ncan <= |R|")
        ensure(total_lex_labels == n_R, "lex bijects onto image per fiber sum")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "m": m,
                "n_R": n_R,
                "N_can": n_can,
                "lex_injective": True,
                "max_lex_fiber": max_lex_fiber,
                "schemes": scheme_stats,
                "min_S_cU_max_fiber": max(inv_min_cu.values()) if inv_min_cu else 0,
            }
        )

    ensure(any(not r["schemes"]["min_b"]["injective"] for r in rows), "bank collision")
    ensure(all(r["lex_injective"] for r in rows), "lex")
    # deployed arithmetic already gated in lemma_mass_arithmetic via build()

    return {"status": "PASS", "rows": rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    mass = lemma_mass_arithmetic()
    return {
        "packet": "kb_qatom_route_d_v14",
        "title": "Residual mass atom re-anchor (on-track north star)",
        "status": "PARTIAL_MASS_REANCHOR",
        "claims": {
            "proves_mass_sufficient_budgets": True,
            "proves_lex_dual_mass": True,
            "proves_routing_dual_import": True,
            "proves_injection_bridges": True,
            "proves_residual_injection": False,
            "proves_Mm_res_le_1": False,
            "proves_U_phi_atom": False,
            "proves_U_1116048_le_Bstar": False,
            "banks_naive_injection_failures": True,
        },
        "deployed": {
            "a_plus": A,
            "n": N,
            "j": J,
            "t": T,
            "w": W,
            "m": M,
            "p": P,
            "pack": PACK,
            "TARGET": TARGET,
            "TARGET_over_pack": TARGET_OVER_PACK,
            "n_p": N_P,
            "t_p": T_P,
            "pack_n_p": PACK * N_P,
            "pack_t_p": PACK * T_P,
            "B_gen": B_GEN,
            "B_rem": B_REM,
            "K_rem": K_REM,
            "log2_TARGET_over_pack": log2_int(TARGET_OVER_PACK),
            "log2_n_p": log2_int(N_P),
            "log2_t_p": log2_int(T_P),
        },
        "lemmas": {
            "north_star": lemma_north_star(),
            "mass_arithmetic": mass,
            "lex_dual": lemma_lex_dual(),
            "routing_dual": lemma_routing_dual(),
            "injection_bridges": lemma_injection_bridges(),
            "OPEN_RES_MASS": lemma_open_res_mass(),
            "naive_injection_bank": lemma_naive_injection_bank(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reanchor": "Residual mass is the attack surface; multi-mate taxonomy is support only",
            "best_bridges": "E2/E5 support injection, or core injection N_can≤n*p, or M_m^res=1 + U_phi",
            "next": (
                "Prove ledger residual support injection into D×F_p or [t]×F_p, "
                "or residual can-core injection into size ≤ TARGET/17, or M_m^res≤1 "
                "with U_phi bound — using first-match structure, not aperiodic proxy alone"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['m']} | {r['w']} | {r['n_R']} | {r['N_can']} | "
        f"{r['schemes']['min_b']['max_fiber']} | {r['schemes']['min_c0']['max_fiber']} | "
        f"{r['min_S_cU_max_fiber']} | {r['lex_injective']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v14: residual mass re-anchor

Status: `PARTIAL` — mass criteria + bridges **PROVED**; residual injection / atom **OPEN**.

## North star (on track)

Ledger residual mass at `a+ = {d['a_plus']}`:

```text
max |R(z)|  ≤  TARGET  =  {d['TARGET']}
```

or any equivalent E1/E2/E5 / N_can / (U_res,M_m^{{res}}) form below.

Multi-mate geometry (v8–v13) is **support structure**, not a substitute for mass.

## Sufficient budgets (PROVED arithmetic)

| Criterion | Bound | Fits TARGET? |
|---|---|---|
| N_can ≤ TARGET/17 | {d['TARGET_over_pack']} | pack atom |
| N_can ≤ n·p | {d['n_p']} (log2≈{d['log2_n_p']:.2f}) | yes (≤ TARGET/17) |
| N_can ≤ t·p | {d['t_p']} | yes |
| N_can ≤ t | {d['t']} | => |R| ≤ t·p via p-cover |
| |R| ≤ n·p (E5) | {d['n_p']} | yes |
| |R| ≤ t·p (E2) | {d['t_p']} | yes |

```text
17 · n · p  =  {d['pack_n_p']}  ≤  TARGET
17 · t · p  =  {d['pack_t_p']}  ≤  TARGET
```

## Dualities (PROVED)

```text
R  injects into  C_res x F_p     (lex: S |-> (C_can, c_U))
|R|  <=  p * N_can_prim
N_can_prim  <=  |R|
N_can_prim  <=  U_res * M_m^{{res,side}}
N_can_prim  <=  U_phi * M_m^{{res,phi}}
```

## Injection bridges (PROVED as reductions)

- Support injection |R|<=B (E2/E5) => mass.
- Core injection N_can<=B => pack/p-cover mass via budgets above.
- M_m^{{res,phi}}<=1 => N_can=U_phi; need U_phi<=TARGET/17.

## OPEN_RES_MASS

Prove **one** ledger-residual bound among (i)–(v) in the certificate JSON
(`OPEN_RES_MASS`). Falsifier: residual leaf with mass above TARGET / above the
claimed injection budget.

### Do not

- Re-prove global M_m≤1
- Treat aperiodic toys as ledger residual
- Continue multi-mate taxonomy without mass

## Toy bank (aperiodic proxy only)

Lex dual injective on residual proxy. Naive core marks not injective:

| j | m | w | |R| | N_can | max(min,Phi) | max(min,c0) | max(minS,cU) | lex OK |
|---|---|---|---:|---:|---:|---:|---:|---|
{tbl}

## Next real math

1. **Ledger** residual support injection into `D x F_p` or `[t] x F_p` (E5/E2), or
2. Residual can-core injection with |L| <= n*p or TARGET/17, or
3. M_m^{{res}}<=1 plus U_phi (or U_res) atom bound,

using first-match structure (marked incidence, paid cells), not proxy alone.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v14.py
python3 experimental/scripts/verify_kb_qatom_route_d_v14.py --check
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
        ensure(old["deployed"]["TARGET"] == cert["deployed"]["TARGET"], "target drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v14\n\n"
        "Residual mass atom re-anchor (on-track north star).\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v14.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v14 report\n\nstatus: {cert['status']}\n"
        f"TARGET: {cert['deployed']['TARGET']}\n"
        f"n*p: {cert['deployed']['n_p']}\n"
        f"OPEN_RES_MASS: true\n"
        f"toy rows: {len(cert['toy_suite']['rows'])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  north star: residual mass |R| ≤ TARGET")
    print(f"  n*p={cert['deployed']['n_p']} ≤ TARGET/17={cert['deployed']['TARGET_over_pack']}: YES")
    print(f"  17*n*p ≤ TARGET: YES")
    print(f"  OPEN_RES_MASS: residual injection / N_can / M_m^res+U_phi")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])} (lex dual OK; naive marks collide)")


if __name__ == "__main__":
    main()
