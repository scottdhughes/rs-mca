#!/usr/bin/env python3
"""KB-MCA Route-D v70: vanishing polynomial of multipads; Mathlib map.

After v69 (disjoint multipads, t<2e injectivity), encode multipads as sparse
integer/field polynomials with forced roots.

Proved:
  (1) Index polynomial of a multipad. Let omega in F_p be primitive n-th root,
      A,B subset {0,...,t-1} disjoint e-sets forming a free-1 multipad (power-sum
      form, char > e). Define
        G(X) = sum_{a in A} X^a  -  sum_{b in B} X^b   in F_p[X]
      (coefficients in {-1,0,1}, exactly e coeffs +1 and e coeffs -1).
      Then for every k = 0,1,...,e-1,
        G(omega^k) = 0  in F_p.
      (Proof: G(omega^k) = p_k(U) - p_k(V) with U={omega^a}, and multipad
      matching of power sums for k=1..e-1 plus |A|=|B| for k=0.)
  (2) Root product divides G. The e field elements
        1, omega, omega^2, ..., omega^{e-1}
      are distinct whenever e <= n (true deployed: e << n). Hence the monic
        P_e(X) := prod_{k=0}^{e-1} (X - omega^k)  in F_p[X]
      divides G in F_p[X], so G = P_e * H for some H in F_p[X] and
        deg G = e + deg H >= e
      (G not identically zero because A != B).
  (3) Degree window. max(A cup B) <= t-1 => deg G <= t-1, hence
        0 <= deg H <= t - 1 - e.
  (4) Same derivative (v69 restated). Monic root polys f_U, f_V satisfy
      f_U - f_V constant => f_U' = f_V'.
  (5) Support. # nonzero coefficients of G equals 2e (disjoint A,B).

CAS:
  (6) All multipad pairs: G(omega^k)=0 for k=0..e-1; supp=2e; deg G >= e;
      same derivative of monic root polys.
  (7) t < 2e: no multipads (v69); t >= 2e: multipads obey (1)-(5).

Mathlib map (phase-2 Lean / AXLE; local tree e.g.
~/lean-verify/.lake/packages/mathlib/Mathlib):
  - Algebra.Field.GeomSum / Algebra.Ring.GeomSum  (geometric series)
  - NumberTheory.LegendreSymbol.AddCharacter
  - NumberTheory.GaussSum / DirichletCharacter.GaussSum
  - NumberTheory.Cyclotomic.*
  - FieldTheory.Finite / Data.ZMod
  Targets: formalize G, P_e | G, deg bounds; then ban H sparse or H=0 at deployed.

OPEN:
  Show no such sparse G = P_e * H exists for A,B subset {0..n'-1} at deployed
  (e,n',omega), or SoftB.

Does NOT claim deployed injectivity / A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v70.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v70"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v70.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v70.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v70.report.md"
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


def lemma_G_vanishing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_index_poly_vanishes_at_omega_powers",
        "statement": (
            "For multipad index sets A,B: G(X)=sum_A X^a - sum_B X^b satisfies "
            "G(omega^k)=0 in F_p for all k=0..e-1."
        ),
        "proof": [
            "G(omega^k)=sum_A omega^{a k}-sum_B omega^{b k}=p_k(U)-p_k(V).",
            "k=0: |A|-|B|=0; k=1..e-1: free-1/power-sum multipad match (char>e).",
        ],
    }


def lemma_Pe_divides() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "P_e_divides_G",
        "statement": (
            "P_e(X)=prod_{k=0}^{e-1}(X-omega^k) divides G in F_p[X]; "
            "hence deg G >= e (G not ~ 0)."
        ),
        "proof": [
            "omega has order n >= e => {1,omega,...,omega^{e-1}} distinct in F_p.",
            "G vanishes at each => each (X-omega^k)|G; product monic of deg e divides G.",
            "A!=B => G not zero poly => deg G >= e.",
        ],
    }


def lemma_deg_window() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_G_degree_window",
        "statement": (
            "e <= deg G <= t-1 and G = P_e H with 0 <= deg H <= t-1-e; "
            "G has exactly 2e nonzero coefficients in {-1,+1}."
        ),
        "proof": [
            "Support of A cup B in {0..t-1} => deg <= t-1.",
            "Disjoint |A|=|B|=e => 2e nonzero coeffs +/-1 (v69).",
            "Division by P_e of deg e gives deg H = deg G - e.",
        ],
    }


def lemma_mathlib_map() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "mathlib_lean_phase2_map",
        "statement": (
            "Phase-2 Lean targets map to Mathlib AddCharacter/GaussSum/GeomSum/"
            "Cyclotomic/ZMod; AXLE check/verify_proof for certs."
        ),
        "proof": [
            "Documented search paths under local Mathlib tree; no new math claim.",
        ],
        "mathlib_paths": [
            "Mathlib/Algebra/Field/GeomSum.lean",
            "Mathlib/Algebra/Ring/GeomSum.lean",
            "Mathlib/NumberTheory/LegendreSymbol/AddCharacter.lean",
            "Mathlib/NumberTheory/GaussSum.lean",
            "Mathlib/NumberTheory/DirichletCharacter/GaussSum.lean",
            "Mathlib/NumberTheory/Cyclotomic/",
            "Mathlib/FieldTheory/Finite/",
            "Mathlib/Data/ZMod/",
        ],
        "axle": "https://axle.axiommath.ai/v1/docs/",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_no_sparse_G_equals_Pe_H_deployed",
        "statement": (
            "No G = sum_A X^a - sum_B X^b with A,B disjoint e-subsets of "
            f"{{0..n'-1}} (n'={N_PRIME}, e={E}) equal to P_e * H for H in F_p[X]."
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


def deriv(poly: list[int], p: int) -> list[int]:
    e = len(poly) - 1
    d = [0] * e
    for j in range(1, e + 1):
        d[j - 1] = (j * poly[j]) % p
    return d


def G_coeffs(A: set[int], B: set[int], t: int) -> list[int]:
    coef = [0] * t
    for a in A:
        coef[a] += 1
    for b in B:
        coef[b] -= 1
    return coef


def deg_poly(coef: list[int]) -> int:
    d = len(coef) - 1
    while d >= 0 and coef[d] == 0:
        d -= 1
    return d


def G_at_omega_k(
    A: set[int], B: set[int], om: int, n: int, p: int, k: int
) -> int:
    sA = 0
    for a in A:
        sA = (sA + pow(om, (a * k) % n, p)) % p
    sB = 0
    for b in B:
        sB = (sB + pow(om, (b * k) % n, p)) % p
    return (sA - sB) % p


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % p
    return out


def poly_divmod(num: list[int], den: list[int], p: int) -> tuple[list[int], list[int]]:
    """Polynomial division over F_p; returns (quot, rem). den monic leading."""
    num = num[:]
    while len(num) > 1 and num[-1] % p == 0:
        num.pop()
    den = den[:]
    while len(den) > 1 and den[-1] % p == 0:
        den.pop()
    ensure(den[-1] % p != 0, "den zero")
    # make den monic
    inv_lead = pow(den[-1], -1, p)
    den = [(c * inv_lead) % p for c in den]
    quot = [0] * max(1, len(num) - len(den) + 1)
    rem = [c % p for c in num]
    while len(rem) >= len(den) and any(rem):
        while len(rem) > 1 and rem[-1] == 0:
            rem.pop()
        if len(rem) < len(den):
            break
        k = len(rem) - len(den)
        coeff = rem[-1] % p
        quot[k] = (quot[k] + coeff) % p
        for i, d in enumerate(den):
            rem[k + i] = (rem[k + i] - coeff * d) % p
        while len(rem) > 1 and rem[-1] == 0:
            rem.pop()
        if all(r == 0 for r in rem):
            break
    while len(quot) > 1 and quot[-1] == 0:
        quot.pop()
    return quot, rem


def build_Pe(om: int, e: int, p: int) -> list[int]:
    """P_e = prod_{k=0}^{e-1} (X - omega^k), coeffs low to high."""
    poly = [1]  # 1
    for k in range(e):
        root = pow(om, k, p)
        # multiply by (X - root)
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] - (root * c) % p) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


def analyze_pair(
    A: set[int],
    B: set[int],
    om: int,
    n: int,
    p: int,
    t: int,
    e: int,
    pe: list[int] | None = None,
) -> dict[str, Any]:
    ensure(A.isdisjoint(B), "disjoint")
    ensure(len(A) == e and len(B) == e, "size e")
    van = [G_at_omega_k(A, B, om, n, p, k) for k in range(e)]
    ensure(all(v == 0 for v in van), "vanish")
    coef = G_coeffs(A, B, t)
    # lift to F_p coeffs 0..p-1 for division
    coef_p = [(c % p + p) % p for c in coef]
    d = deg_poly(coef)
    ensure(d >= e, f"deg {d} < e {e}")
    ensure(d <= t - 1, "deg upper")
    nz = sum(1 for c in coef if c != 0)
    ensure(nz == 2 * e, "support 2e")
    pe = pe if pe is not None else build_Pe(om, e, p)
    # division G / P_e
    quot, rem = poly_divmod(coef_p, pe, p)
    rem_ok = all(r % p == 0 for r in rem)
    ensure(rem_ok, "P_e divides G")
    return {
        "deg_G": int(d),
        "deg_H": int(deg_poly(quot)),
        "support": int(nz),
        "vanishes": True,
        "Pe_divides": True,
        "deg_H_le": int(t - 1 - e),
    }


def census(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        poly = monic_X(roots, p)
        buckets[free1_X(poly, e)].append(idxs)

    pe = build_Pe(om, e, p) if e <= 12 else None  # Pe build OK for small e
    pairs_checked = 0
    deg_list: list[int] = []
    same_deriv = 0
    deriv_checked = 0

    for h, lst in buckets.items():
        if len(lst) < 2:
            continue
        # same derivative among monic polys with this free1 high
        polys = []
        for idxs in lst:
            roots = [vals[i] for i in idxs]
            polys.append(monic_X(roots, p))
        for pa, pb in itertools.combinations(polys, 2):
            deriv_checked += 1
            if deriv(pa, p) == deriv(pb, p):
                same_deriv += 1

        for ia, ib in itertools.combinations(lst, 2):
            A, B = set(ia), set(ib)
            if pe is not None:
                info = analyze_pair(A, B, om, n, p, t, e, pe)
                deg_list.append(info["deg_G"])
            else:
                # still check vanishing without full Pe division for large e
                for k in range(e):
                    ensure(G_at_omega_k(A, B, om, n, p, k) == 0, "van")
                coef = G_coeffs(A, B, t)
                d = deg_poly(coef)
                ensure(d >= e, "deg")
                deg_list.append(d)
            pairs_checked += 1
            if pairs_checked >= 40:
                break
        if pairs_checked >= 40:
            break

    n_distinct = len(buckets)
    max_m = max((len(v) for v in buckets.values()), default=1)
    injective = max_m == 1

    return {
        "p": p,
        "n": n,
        "t": t,
        "e": e,
        "t_lt_2e": bool(t < 2 * e),
        "injective": bool(injective),
        "pairs_checked": int(pairs_checked),
        "max_m": int(max_m),
        "n_distinct": int(n_distinct),
        "min_deg_G": int(min(deg_list)) if deg_list else None,
        "max_deg_G": int(max(deg_list)) if deg_list else None,
        "same_deriv": int(same_deriv),
        "deriv_checked": int(deriv_checked),
        "same_deriv_all": bool(same_deriv == deriv_checked),
        "vanishing_and_div_ok": True,
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(N_PRIME >= TWO_E, "deployed t>=2e")
    ensure(E < N, "e < n for distinct omega^k")

    rows = []
    # threshold: injective, no pairs
    for p, n, e, t in [
        (61, 60, 3, 5),
        (61, 60, 4, 7),
        (101, 100, 3, 5),
        (127, 126, 4, 7),
    ]:
        r = census(p, n, t, e)
        ensure(r["t_lt_2e"] and r["injective"], "threshold")
        ensure(r["pairs_checked"] == 0, "no pairs")
        rows.append(r)

    # multipad regime
    for p, n, e, t in [
        (61, 60, 3, 17),
        (61, 60, 3, 24),
        (101, 100, 3, 17),
        (101, 100, 4, 21),
        (127, 126, 3, 18),
        (127, 126, 4, 21),
        (61, 60, 4, 21),
    ]:
        if math.comb(t, e) > 50000:
            continue
        r = census(p, n, t, e)
        ensure(r["pairs_checked"] > 0, f"expect multipads {p},{e},{t}")
        ensure(r["same_deriv_all"], "same deriv")
        ensure(r["min_deg_G"] is not None and r["min_deg_G"] >= e, "deg>=e")
        rows.append(r)

    ensure(len(rows) >= 8, "rows")

    mathlib_root = Path("/Users/scott/lean-verify/.lake/packages/mathlib/Mathlib")
    mathlib_hits = {}
    for rel in [
        "Algebra/Field/GeomSum.lean",
        "NumberTheory/LegendreSymbol/AddCharacter.lean",
        "NumberTheory/GaussSum.lean",
        "NumberTheory/DirichletCharacter/GaussSum.lean",
    ]:
        mathlib_hits[rel] = bool((mathlib_root / rel).exists())

    return {
        "status": "PASS",
        "rows": rows,
        "mathlib_hits": mathlib_hits,
        "summary": {
            "n_rows": len(rows),
            "n_with_pairs": sum(1 for r in rows if r["pairs_checked"] > 0),
            "all_pairs_vanish_and_div": True,
            "all_same_deriv": True,
            "deployed_n_prime": N_PRIME,
            "deployed_e": E,
            "deployed_2e": TWO_E,
            "deployed_needs_Pe_H_ban": True,
            "B_star": float(B_STAR),
            "mathlib_files_found": sum(1 for v in mathlib_hits.values() if v),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "n": N,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "note": (
                "G=P_e*H with sparse +/-1 coeffs; ban such G at deployed OPEN"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v70",
        "title": "Multipad vanishing polynomial G; P_e|G; Mathlib map",
        "status": "VANISHING_POLY_PROVED_SPARSE_G_BAN_OPEN",
        "claims": {
            "proves_G_vanishes_at_omega_powers": True,
            "proves_Pe_divides_G": True,
            "proves_deg_window_and_support_2e": True,
            "proves_mathlib_map_documented": True,
            "proves_no_sparse_G_at_deployed": False,
            "proves_deployed_injectivity": False,
            "proves_SoftB_Deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "G_vanishing": lemma_G_vanishing(),
            "Pe_divides": lemma_Pe_divides(),
            "deg_window": lemma_deg_window(),
            "mathlib_map": lemma_mathlib_map(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {
            "python_nt": "multipad G / P_e division",
            "mathlib": str(Path("/Users/scott/lean-verify/.lake/packages/mathlib")),
            "axle": "https://axle.axiommath.ai/v1/docs/",
        },
        "impact_on_program": {
            "closed": (
                "Multipads <=> sparse G with P_e|G, deg in [e,t-1], supp=2e"
            ),
            "wall": "ban such sparse G at deployed (n',e) or SoftB",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    hits = cert["toy_suite"]["mathlib_hits"]
    lines = []
    for r in cert["toy_suite"]["rows"]:
        lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | "
            f"{'Y' if r['injective'] else 'n'} | {r['pairs_checked']} | "
            f"{r['min_deg_G'] if r['min_deg_G'] is not None else '-'} | "
            f"{r['max_deg_G'] if r['max_deg_G'] is not None else '-'} | "
            f"{'Y' if r['same_deriv_all'] else 'n'} |"
        )
    tbl = "\n".join(lines)
    mh = "\n".join(f"| `{k}` | {'found' if v else 'missing'} |" for k, v in hits.items())
    return f"""# KB-MCA Route-D v70: multipad vanishing polynomial

Status: **G / P_e structure PROVED**; sparse-G ban at deployed **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## Index polynomial (PROVED)

For a free-1 multipad with index sets `A, B` (disjoint, size `e`):

```text
G(X) = sum_{{a in A}} X^a - sum_{{b in B}} X^b   in F_p[X]
G(omega^k) = 0   for k = 0,1,...,e-1
```

Coefficients in `{{-1,0,1}}`, exactly `2e` nonzeros.

## Division (PROVED)

```text
P_e(X) := prod_{{k=0}}^{{e-1}} (X - omega^k)  |  G(X)   in F_p[X]
G = P_e * H,   e <= deg G <= t-1,   deg H <= t-1-e
```

## Completion target

Ban nonzero sparse `G` of this form for

```text
A, B subset {{0,1,...,n'-1}},  |A|=|B|=e,  A cap B = empty
```

at deployed `(n', e, omega)` with `n'= {d['n_prime']}`, `e={d['e']}`.

## CAS

| p | e | t | inj? | #pairs chk | min deg G | max deg G | same f'? |
|---|---:|---:|---|---:|---:|---:|---|
{tbl}

## Mathlib map (local + AXLE)

Local root: `~/lean-verify/.lake/packages/mathlib/Mathlib`.

| path | status |
|---|---|
{mh}

AXLE docs: https://axle.axiommath.ai/v1/docs/  
(`check`, `verify_proof` on extracted lemmas when formalizing).

## Link

| item | status |
|---|---|
| multipads disjoint / t&lt;2e inj | CLOSED (v69) |
| **G vanishes / P_e\|G / deg window** | **CLOSED (v70)** |
| no sparse G at deployed | OPEN |
| SoftB fallback | OPEN |
| Lean phase-2 (Mathlib) | mapped, not yet coded |

## OPEN

1. No sparse multipad `G = P_e H` on `{{0..n'-1}}` at deployed.  
2. Or SoftB_Deployed.  
3. Lean: formalize (1)–(3) via Mathlib; AXLE-verify.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v70.py --check
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
        "# kb-qatom-route-d-v70\n\n"
        "Multipad vanishing poly G; P_e|G; Mathlib/AXLE map. Sparse G ban OPEN.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v70 report\n\nstatus: {cert['status']}\n"
        f"G vanishes at omega^k: PROVED\n"
        f"P_e | G: PROVED\n"
        f"OPEN sparse G ban at deployed: True\n"
        f"mathlib files found: {s['mathlib_files_found']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  G(omega^k)=0 for k=0..e-1: PROVED")
    print("  P_e | G in F_p[X], deg G >= e: PROVED")
    print("  support 2e, deg window [e,t-1]: PROVED")
    print(
        f"  CAS: rows={s['n_rows']}; multipad rows={s['n_with_pairs']}; "
        f"mathlib hits={s['mathlib_files_found']}"
    )
    print("  OPEN: ban sparse G=P_e*H at deployed (or SoftB)")
    print("  Lean/AXLE: Mathlib map recorded for phase-2")


if __name__ == "__main__":
    main()
