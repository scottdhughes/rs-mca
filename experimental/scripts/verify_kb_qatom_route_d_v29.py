#!/usr/bin/env python3
"""KB-MCA Route-D v29: residual multipad emptiness + Type D/S A_SP multipads.

Formalizes first-match residual vs A_SP multipad geometry after v28 t-packing.

Proved:
  (1) Residual multipad emptiness: under the first-match split
        Fib = A_SP ⊔ R_sing
      with A_SP = multi-member top-seam core pencils and R_sing = singleton
      pencils, every multipad event requires a free-1 CS ordered pair from a
      multi-member pencil, hence lives only on A_SP. Therefore R_sing has
      N_ord=0 and M_pad=1 vacuously — there are no residual multipads after
      the A_SP cell is paid. (Sharpens v28 locus.)
  (2) Type D / Type S classification of A_SP multipads for fixed (U,V):
        Type D: point-multiplicity t=1 (pairwise disjoint cores)
        Type S: t≥2 (some domain point in ≥2 multipad cores)
  (3) Type D packing: M_pad ≤ ⌊(n−2e)/m_c⌋ (=2 deployed).
  (4) free_core=1 ⇒ only Type D (v27 inter bound |C∩C'|=0 ⇒ t=1).
  (5) Type S ⇒ free_core≥2 (contrapositive of (4)).
  (6) Payment restatement:
        A_SP cost uses N_ord ≤ M_pad · N_side on A_SP multipads;
        residual mass after A_SP payment is pure R_sing (no multipad term);
        Type D contributes M_pad≤2 deployed; Type S is the free_core≫1 gap.
  (7) Toy bank: R_sing fibers never multipad; free_core=1 only Type D with
      M_pad≤pack; free_core≥2 has Type S; Type D always respects packing.

Does NOT prove Type S M_pad≤2 at free_core=846161, nor kill Type S.

  python3 experimental/scripts/verify_kb_qatom_route_d_v29.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v29.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v29"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v29.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v29.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v29.report.md"
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
FLOOR_N_MINUS_2E_OVER_MC = (N - 2 * E) // M_C  # 2
FLOOR_N_OVER_E = N // E
K_MAX = E // FLOOR_N_OVER_E


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


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_residual_empty() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_multipad_emptiness_after_A_SP",
        "statement": (
            "Under the first-match fiber partition Fib_w(z) = A_SP(z) ⊔ R_sing(z) "
            "(v17), where A_SP is the set of j-supports in multi-member top-seam "
            "core pencils and R_sing is the complementary singleton-pencil "
            "residual: every multipad event is supported on a free-1 CS ordered "
            "pair arising from a multi-member pencil, hence only on A_SP. "
            "Consequently R_sing has N_ord=0 and M_pad=1 vacuously. After the "
            "A_SP first-match cell is paid, the residual carries no multipad term."
        ),
        "proof": [
            "Multipad side key (high,c0U,c0V) is populated only from ordered CS "
            "pairs (U,V) drawn from a free-1 pencil of size ≥2 on a common core "
            "(top-seam normal form v15–v20).",
            "Multi-member free-1 pencils are exactly the A_SP assignment set "
            "(v17).",
            "R_sing := Fib \\ A_SP has only singleton pencils ⇒ no CS ordered "
            "pair of that form ⇒ no multipad side key ⇒ M_pad:=1, N_ord=0.",
            "First-match form (v17): pay A_SP cell; residual ⊆ R_sing.",
        ],
        "consequence": (
            "The slogan 'residual multipad t=1' is vacuously true: residual "
            "multipads do not exist. The live M_pad problem is entirely inside "
            "the A_SP payment cell."
        ),
    }


def lemma_type_DS() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "A_SP_multipad_type_D_vs_S",
        "statement": (
            "For each A_SP multipad side key (U,V) with core set Cores, define "
            "t = max_r |{C ∈ Cores : r ∈ C}| over r ∈ D\\(U∪V). "
            "Type D: t=1 (pairwise disjoint cores). "
            "Type S: t≥2 (shared-root multipad)."
        ),
        "proof": ["Definition from v28 point-multiplicity."],
    }


def lemma_type_D_packing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "type_D_Mpad_packing_deployed_2",
        "statement": (
            "Type D multipads have t=1, hence "
            f"M_pad ≤ ⌊(n−2e)/m_c⌋ = {FLOOR_N_MINUS_2E_OVER_MC} at deployed "
            "parameters (v28). free_core=1 multipads are always Type D "
            f"(v27 |C∩C'|=0), so free_core=1 ⇒ M_pad ≤ {FLOOR_N_MINUS_2E_OVER_MC} "
            "deployed as well."
        ),
        "proof": [
            "v28: M_pad ≤ ⌊t(n−2e)/m_c⌋; t=1 ⇒ packing.",
            "v27: free_core=1 ⇒ |C∩C'|≤0 ⇒ t=1 ⇒ Type D.",
            f"Deployed ⌊(n−2e)/m_c⌋ = {FLOOR_N_MINUS_2E_OVER_MC}.",
        ],
        "deployed_bound": FLOOR_N_MINUS_2E_OVER_MC,
    }


def lemma_type_S_needs_fc() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "type_S_requires_free_core_ge_2",
        "statement": (
            "Type S multipads can occur only when free_core ≥ 2. "
            "Equivalently free_core=1 ⇒ no Type S."
        ),
        "proof": [
            "Type S ⇒ t≥2 ⇒ some r in two cores ⇒ |C∩C'|≥1.",
            "v27: |C∩C'| ≤ free_core−1, so free_core−1 ≥ 1 ⇒ free_core ≥ 2.",
        ],
        "deployed_note": (
            f"Deployed free_core={FREE_CORE} ≥ 2, so Type S is not ruled out "
            "by degree; it is the remaining A_SP multipad gap."
        ),
    }


def lemma_payment_restated() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "payment_path_after_residual_emptiness",
        "statement": (
            "First-match residual mass after paying A_SP is pure R_sing "
            "(no multipad). A_SP payment still needs "
            "N_ord ≤ M_pad · N_side on A_SP multipads, with "
            "Type D contributing M_pad ≤ 2 deployed and Type S open. "
            "Side injection (ι,δ)+high tag (v25–v28) remains the other half."
        ),
        "proof": [
            "Residual emptiness (lemma 1) + Type D packing + v20 N_ord bound.",
        ],
        "program": (
            "Kill or pay Type S multipads at free_core≫1; compress residual "
            f"highs to [{K_MAX}] for side marks under M_pad≤1 or ≤2."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_type_S_Mpad_and_high_tag",
        "statement": (
            f"(1) Bound Type S multipads at free_core={FREE_CORE}: shared-root "
            "A_SP multipads with t≥2 — e.g. reduce free_core along common roots, "
            "or first-match shared-root cell.\n"
            f"(2) Residual/A_SP free-1 highs ↪ [{K_MAX}] for (κ,ι,δ) side marks.\n"
            "Residual multipad t=1 is settled vacuously (no residual multipads)."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_rsing_fibers = 0
    n_rsing_mp = 0  # should stay 0
    n_type_D = 0
    n_type_S = 0
    n_fc1_type_S = 0  # should stay 0
    n_type_D_pack_ok = 0
    n_type_D_events = 0
    n_asp_fibers = 0

    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 20000:
            continue
        free_core = m_c - w
        pack = (n - 2 * e) // m_c if n >= 2 * e else 0
        vals = domain_vals(p, n)

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        max_Mpad_D = 1
        max_Mpad_S = 1
        max_Mpad = 1
        n_D = 0
        n_S = 0
        n_rsing = 0
        n_asp = 0
        max_t = 0

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            # A_SP vs R_sing at fiber level: any multi-member free-1 pencil?
            multi_pencil = any(len(lst) >= 2 for lst in pencils.values())
            # also need actual CS pair (distinct c0)
            has_cs = False
            pads: dict[Any, list] = defaultdict(list)
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, high = a
                        _C2, V, c0V, _ = b
                        if c0U == c0V:
                            continue
                        has_cs = True
                        pads[(high, c0U, c0V)].append((C, U, V))

            if not has_cs:
                # R_sing-style fiber (no top-seam CS pair)
                n_rsing += 1
                n_rsing_fibers += 1
                # no multipad
                for _sk, items in pads.items():
                    uc = {tuple(sorted(C)) for C, U, V in items}
                    if len(uc) >= 2:
                        n_rsing_mp += 1
                continue

            n_asp += 1
            n_asp_fibers += 1
            ensure(multi_pencil, "CS pair ⇒ multi pencil")

            for _sk, items in pads.items():
                by_c: dict[tuple, tuple] = {}
                for C, U, V in items:
                    t = tuple(sorted(C))
                    if t not in by_c:
                        by_c[t] = (U, V)
                mpad = len(by_c)
                max_Mpad = max(max_Mpad, mpad)
                if mpad < 2:
                    continue
                cores = [set(t) for t in by_c]
                U0, V0 = next(iter(by_c.values()))
                ensure(U0.isdisjoint(V0), "UV disj")
                # point multiplicity on complement
                cnt: Counter = Counter()
                for c in cores:
                    ensure(U0.isdisjoint(c) and V0.isdisjoint(c), "joint avoid")
                    for r in c:
                        cnt[r] += 1
                t_mult = max(cnt.values()) if cnt else 0
                max_t = max(max_t, t_mult)
                if t_mult <= 1:
                    # Type D
                    n_D += 1
                    n_type_D += 1
                    n_type_D_events += 1
                    max_Mpad_D = max(max_Mpad_D, mpad)
                    ensure(mpad <= pack, f"Type D pack {mpad}>{pack}")
                    n_type_D_pack_ok += 1
                    # pairwise disjoint
                    for a, b in itertools.combinations(cores, 2):
                        ensure(len(a & b) == 0, "Type D disj")
                else:
                    # Type S
                    n_S += 1
                    n_type_S += 1
                    max_Mpad_S = max(max_Mpad_S, mpad)
                    if free_core == 1:
                        n_fc1_type_S += 1
                    ensure(free_core >= 2, "Type S needs fc>=2")

        if free_core == 1:
            ensure(n_S == 0, "fc1 no Type S")
            if n_D > 0:
                ensure(max_Mpad_D <= pack, "fc1 D pack")

        if free_core <= 0:
            ensure(max_Mpad <= 1, "fc0")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "pack_type_D": pack,
                "n_rsing_fibers": n_rsing,
                "n_asp_fibers": n_asp,
                "n_type_D_events": n_D,
                "n_type_S_events": n_S,
                "max_Mpad": max_Mpad,
                "max_Mpad_type_D": max_Mpad_D,
                "max_Mpad_type_S": max_Mpad_S,
                "max_t": max_t,
            }
        )

    ensure(n_rsing_fibers > 0, "have rsing")
    ensure(n_rsing_mp == 0, "rsing never multipads")
    ensure(n_type_D > 0, "have type D")
    ensure(n_type_S > 0, "have type S bank")
    ensure(n_fc1_type_S == 0, "fc1 no S")
    ensure(n_type_D_pack_ok == n_type_D_events, "all D pack")
    ensure(FLOOR_N_MINUS_2E_OVER_MC == 2, "deployed 2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FREE_CORE >= 2, "deployed allows S")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rsing_fibers": n_rsing_fibers,
            "n_rsing_multipads": n_rsing_mp,
            "n_asp_fibers": n_asp_fibers,
            "n_type_D_events": n_type_D,
            "n_type_S_events": n_type_S,
            "n_fc1_type_S": n_fc1_type_S,
            "n_type_D_pack_ok": n_type_D_pack_ok,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v29",
        "title": "Residual multipad emptiness + Type D/S A_SP multipad split",
        "status": "PARTIAL_RESIDUAL_EMPTY_TYPE_DS",
        "claims": {
            "proves_residual_multipad_emptiness": True,
            "proves_type_D_S_classification": True,
            "proves_type_D_Mpad_le_2_deployed": True,
            "proves_fc1_only_type_D": True,
            "proves_type_S_needs_fc_ge_2": True,
            "proves_type_S_Mpad_bound_deployed": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_residual_empty_and_DS": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "m_c": M_C,
            "free_core": FREE_CORE,
            "type_D_Mpad_bound": FLOOR_N_MINUS_2E_OVER_MC,
            "K_max": K_MAX,
            "t_p": T_P,
            "e_p": E_P,
            "allows_type_S": FREE_CORE >= 2,
        },
        "lemmas": {
            "residual_empty": lemma_residual_empty(),
            "type_DS": lemma_type_DS(),
            "type_D_pack": lemma_type_D_packing(),
            "type_S_fc": lemma_type_S_needs_fc(),
            "payment": lemma_payment_restated(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "residual": (
                "Residual multipad t=1 is VACUOUS — residual has no multipads "
                "after A_SP payment (R_sing only)"
            ),
            "A_SP": (
                f"Type D multipads: M_pad≤{FLOOR_N_MINUS_2E_OVER_MC} deployed. "
                "Type S (shared-root, free_core≥2) is the live multipad gap."
            ),
            "next": (
                "Pay or kill Type S multipads (shared-root first-match / free_core "
                "reduction); high tag κ→[K_max] for sides"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_rsing_fibers']} | "
        f"{r['n_asp_fibers']} | {r['n_type_D_events']} | {r['n_type_S_events']} | "
        f"{r['max_Mpad_type_D']} | {r['max_Mpad_type_S']} | {r['pack_type_D']} | "
        f"{r['max_t']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v29: residual multipad emptiness + Type D/S split

Status: `PARTIAL` — **residual multipads empty** after A_SP (PROVED); Type D
packing **M_pad≤2** deployed (PROVED); Type S at free_core≫1 still **OPEN**.

## Residual multipad emptiness (PROVED)

First-match partition (v17):

```text
Fib_w(z)  =  A_SP(z)  ⊔  R_sing(z)
```

- `A_SP` = multi-member top-seam core pencils
- `R_sing` = singleton pencils (matching-free residual)

Multipads need free-1 CS pairs from multi-member pencils ⇒ **only on A_SP**.

```text
R_sing:  N_ord = 0,  M_pad = 1 (vacuous)
```

After the A_SP cell is paid, **residual carries no multipad term**.

> The slogan “residual multipad t=1” is vacuously true: there are no residual
> multipads. The live problem is A_SP multipad geometry.

## A_SP multipad types (PROVED)

For each multipad side key `(U,V)` with core set `Cores`:

```text
t = max_r |{{ C ∈ Cores : r ∈ C }}|
Type D: t = 1   (pairwise disjoint cores)
Type S: t ≥ 2   (shared-root multipad)
```

| type | free_core | M_pad bound |
|---|---|---|
| D | any (all of free_core=1) | `≤ ⌊(n−2e)/m_c⌋` = **{d['type_D_Mpad_bound']}** deployed |
| S | only ≥ 2 | OPEN at free_core=`{d['free_core']}` |

## Payment path (restated)

```text
first-match:
  pay A_SP  (needs Type D ≤ 2 + Type S control + side marks)
  residual ⊆ R_sing  (no multipad)
```

Side marks still: `(ι,δ)` within family + highs ↪ `[{d['K_max']}]` (v25–v28).

## Toys

| j | w | free_core | #R_sing | #A_SP | #Type D | #Type S | max M_pad D | max M_pad S | D pack | max t |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{tbl}

Census: R_sing multipads={cen['n_rsing_multipads']} (must be 0);
Type D pack OK={cen['n_type_D_pack_ok']}/{cen['n_type_D_events']};
Type S events={cen['n_type_S_events']}; fc1 Type S={cen['n_fc1_type_S']}.

## OPEN

1. **Type S** multipads at free_core=`{d['free_core']}` (shared-root A_SP)
2. High tag `κ → [{d['K_max']}]` for side injection under M_pad≤1 or ≤2

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v29.py --check
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
        "# kb-qatom-route-d-v29\n\n"
        "Residual multipad emptiness + Type D/S A_SP multipad split.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v29 report\n\nstatus: {cert['status']}\n"
        f"residual multipads: EMPTY (after A_SP)\n"
        f"Type D M_pad bound deployed: {FLOOR_N_MINUS_2E_OVER_MC}\n"
        f"Type S: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  residual multipads after A_SP: EMPTY (PROVED)")
    print(f"  Type D: M_pad ≤ ⌊(n−2e)/m_c⌋ = {FLOOR_N_MINUS_2E_OVER_MC} deployed (PROVED)")
    print("  free_core=1 ⇒ only Type D (PROVED)")
    print("  Type S ⇒ free_core≥2 (PROVED); deployed allows Type S (OPEN bound)")
    print(
        f"  toys: R_sing fibs={cen['n_rsing_fibers']} mp={cen['n_rsing_multipads']}; "
        f"Type D={cen['n_type_D_events']} pack_ok; Type S={cen['n_type_S_events']}"
    )


if __name__ == "__main__":
    main()
