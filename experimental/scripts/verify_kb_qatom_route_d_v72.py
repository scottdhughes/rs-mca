#!/usr/bin/env python3
"""KB-MCA Route-D v72: H-support gap law for multipad multiples of P_e.

Board-oriented structure after v71 (P_e full support).

Proved:
  (1) Full-support shifts. If P in F_p[X] has full support on {0,1,...,m}
      (all m+1 coeffs nonzero) and i >= 0, then X^i P has full support on
      {i,i+1,...,i+m} (m+1 consecutive nonzeros).
  (2) Min support under deg < n. If G != 0, deg G < n = ord(omega), and
      G(omega^k)=0 for k=0..e-1 (equivalently P_e | G), then supp(G) >= e+1.
      Proof: else G = sum_{j=1}^t c_j X^{a_j} with 1 <= t <= e, c_j != 0,
      a_j distinct in 0..deg G subset 0..n-1, so v_j := omega^{a_j} distinct.
      Vanishing => sum_j c_j v_j^k = 0 for k=0..e-1. The e x t matrix
      (v_j^k)_{k,j} has rank t (Vandermonde), so t <= e forces c=0: contradiction.
      (Minimum e+1 achieved by c X^r P_e.)
      Note: X^n-1 has support 2 and is a multiple of P_e but has degree n,
      so the deg < n hypothesis is essential.
  (3) Separated monomials. If P full support deg m and
      H = sum_{j=1}^s h_j X^{i_j} with i_{j+1} >= i_j+m+1, then
      supp(P H) = s(m+1) (disjoint full blocks, no cancel).
  (4) Multipad H gap law. For multipad G = P_e H with supp(G)=2e and
      deg G < n (true on arcs of length t <= n): every consecutive gap in
      supp(H) is <= e.
      Proof: if some gap i_{j+1}-i_j >= e+1, split H=H_L+H_R. Product
      supports of P_e H_L and P_e H_R are disjoint, so
      supp(G)=supp(P_e H_L)+supp(P_e H_R). Each factor is a nonzero multiple
      of P_e of degree < n, hence support >= e+1 by (2). Thus
      supp(G) >= 2e+2, contradiction.
  (5) Diameter. Gaps <= e and s = #supp(H) => max-min <= e(s-1).

CAS:
  (5) All multipad H on toys: every consecutive gap <= e (usually 1).
  (6) Artificial H with gaps e+1: supp(P H)=s(e+1) exactly.
  (7) No multipad with a gap >= e+1 in H.

OPEN:
  Use gap law + ±1 pattern of G to forbid H at deployed, or SoftB.

Does NOT claim deployed |T|<=H2 / A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v72.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v72"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v72.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v72.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v72.report.md"
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


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_full_shift() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "full_support_shift_block",
        "statement": (
            "If P has all coeffs on 0..m nonzero, then X^i P has all coeffs "
            "on i..i+m nonzero."
        ),
        "proof": ["X^i multiplies degrees by +i; coefficients unchanged."],
    }


def lemma_gap_product() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "separated_monomials_product_support",
        "statement": (
            "If P full support deg m and H=sum h_j X^{i_j} with "
            "i_{j+1}>=i_j+m+1, then supp(P H)=s(m+1) with s=#terms (no cancel)."
        ),
        "proof": [
            "Each h_j X^{i_j} P occupies full block [i_j, i_j+m].",
            "Gaps force blocks pairwise disjoint; each site hit once.",
        ],
    }


def lemma_min_support_deg_lt_n() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "min_support_multiple_deg_lt_n",
        "statement": (
            "If G!=0, deg G < n=ord(omega), and G(omega^k)=0 for k=0..e-1, "
            "then supp(G) >= e+1."
        ),
        "proof": [
            "Else supp G = t <= e with distinct a_j in 0..n-1 => distinct "
            "v_j=omega^{a_j}; vanishing is Vandermonde system of rank t on c_j.",
            "t<=e => only c=0. Minimum e+1 from c X^r P_e.",
        ],
    }


def lemma_multipad_gap_law() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_H_consecutive_gaps_le_e",
        "statement": (
            "For multipad G=P_e H with supp(G)=2e and deg G < n: every "
            "consecutive gap in supp(H) is at most e."
        ),
        "proof": [
            "If gap i_{j+1}-i_j >= e+1, split H=H_L+H_R.",
            "Product supports disjoint => supp(G)=supp(P H_L)+supp(P H_R).",
            "Each side nonzero, deg < n, P_e divides => supp >= e+1 each.",
            "Hence supp(G)>=2e+2 > 2e, contradiction.",
        ],
    }


def lemma_diameter() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "H_support_diameter_bound",
        "statement": (
            "If supp(H) has s points and consecutive gaps <= e, then "
            "max(supp H)-min(supp H) <= e(s-1)."
        ),
        "proof": ["Sum of s-1 gaps each <= e."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_gap_law_forbids_deployed_multipad",
        "statement": (
            "Combine gap law + +/-1 shape of G to rule out multipads at deployed, "
            "or SoftB."
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


def build_Pe(om: int, e: int, p: int) -> list[int]:
    poly = [1]
    for k in range(e):
        root = pow(om, k, p)
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] - (root * c) % p) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


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


def supp_list(poly: list[int], p: int) -> list[int]:
    return [i for i, c in enumerate(poly) if c % p != 0]


def supp_count(poly: list[int], p: int) -> int:
    return len(supp_list(poly, p))


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % p
    return out


def poly_divmod_monic(num: list[int], den: list[int], p: int) -> list[int]:
    num = [c % p for c in num]
    den = [c % p for c in den]
    while len(num) > 1 and num[-1] == 0:
        num.pop()
    while len(den) > 1 and den[-1] == 0:
        den.pop()
    inv = pow(den[-1], -1, p)
    den = [(c * inv) % p for c in den]
    quot = [0] * max(1, len(num) - len(den) + 1)
    rem = num[:]
    while len(rem) >= len(den):
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
        if all(x == 0 for x in rem):
            break
    while len(quot) > 1 and quot[-1] == 0:
        quot.pop()
    return quot


def consecutive_gaps(positions: list[int]) -> list[int]:
    if len(positions) < 2:
        return []
    return [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]


def separated_product_row(p: int, n: int, e: int, s: int) -> dict[str, Any]:
    """H with s terms spaced e+1 apart; expect supp(PH)=s(e+1)."""
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    pe = build_Pe(om, e, p)
    ensure(supp_count(pe, p) == e + 1, "full Pe")
    H = [0] * (s * (e + 1))
    for j in range(s):
        H[j * (e + 1)] = j + 1
    prod = poly_mul(pe, H, p)
    sc = supp_count(prod, p)
    expect = s * (e + 1)
    return {
        "p": p,
        "e": e,
        "s": s,
        "supp_prod": int(sc),
        "expect": int(expect),
        "ok": bool(sc == expect),
    }


def multipad_H_rows(p: int, n: int, t: int, e: int, limit: int = 40) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    pe = build_Pe(om, e, p)
    buckets: dict[tuple[int, ...], list[set[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        buckets[free1_X(monic_X(roots, p), e)].append(set(idxs))

    max_gaps: list[int] = []
    all_gaps_le_e = True
    n_pairs = 0
    for lst in buckets.values():
        if len(lst) < 2:
            continue
        for A, B in itertools.combinations(lst, 2):
            tmax = max(max(A), max(B)) + 1
            G = [0] * tmax
            for a in A:
                G[a] += 1
            for b in B:
                G[b] -= 1
            ensure(sum(1 for c in G if c != 0) == 2 * e, "supp G")
            Gp = [(c % p + p) % p for c in G]
            H = poly_divmod_monic(Gp, pe, p)
            pos = supp_list(H, p)
            gaps = consecutive_gaps(pos)
            if gaps:
                mg = max(gaps)
                max_gaps.append(mg)
                if mg > e:
                    all_gaps_le_e = False
            else:
                max_gaps.append(0)
            n_pairs += 1
            if n_pairs >= limit:
                break
        if n_pairs >= limit:
            break

    return {
        "p": p,
        "t": t,
        "e": e,
        "n_pairs": int(n_pairs),
        "all_gaps_le_e": bool(all_gaps_le_e and n_pairs > 0) if n_pairs else True,
        "min_maxgap": int(min(max_gaps)) if max_gaps else None,
        "max_maxgap": int(max(max_gaps)) if max_gaps else None,
        "has_pairs": bool(n_pairs > 0),
    }


def min_multiple_support_row(p: int, n: int, e: int) -> dict[str, Any]:
    """c X^k P_e has support e+1."""
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    pe = build_Pe(om, e, p)
    # X^3 * P_e
    shifted = [0] * 3 + pe
    return {
        "p": p,
        "e": e,
        "supp_Pe": int(supp_count(pe, p)),
        "supp_X3_Pe": int(supp_count(shifted, p)),
        "min_multiple_support": int(e + 1),
        "ok": bool(supp_count(pe, p) == e + 1 and supp_count(shifted, p) == e + 1),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472 and E < N, "e")
    ensure(FLOOR_NP == 17, "k")

    sep_rows = []
    for p, n, e in [(61, 60, 3), (61, 60, 4), (101, 100, 4), (127, 126, 5)]:
        for s in [1, 2, 3]:
            r = separated_product_row(p, n, e, s)
            ensure(r["ok"], f"sep {p},{e},{s}")
            sep_rows.append(r)

    min_rows = []
    for p, n, e in [(61, 60, 3), (101, 100, 5), (127, 126, 4)]:
        r = min_multiple_support_row(p, n, e)
        ensure(r["ok"], "min mult")
        min_rows.append(r)

    # Vandermonde min-support: random multiples with deg < n have supp >= e+1
    for p, n, e in [(61, 60, 3), (61, 60, 5), (101, 100, 4)]:
        g = prim_root(p)
        om = pow(g, (p - 1) // n, p)
        pe = build_Pe(om, e, p)
        import random as _rnd

        _rnd.seed(0)
        for _ in range(40):
            degH = _rnd.randint(0, 6)
            H = [_rnd.randint(0, p - 1) for _ in range(degH + 1)]
            H[-1] = H[-1] or 1
            prod = poly_mul(pe, H, p)
            if len(prod) - 1 >= n:
                continue
            ensure(supp_count(prod, p) >= e + 1, "min supp deg<n")

    mp_rows = []
    for p, n, t, e in [
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 21, 4),
        (61, 60, 30, 4),
    ]:
        if math.comb(t, e) > 50000:
            continue
        r = multipad_H_rows(p, n, t, e)
        if r["has_pairs"]:
            ensure(r["all_gaps_le_e"], f"gaps {p},{t},{e}")
            ensure(r["max_maxgap"] is not None and r["max_maxgap"] <= e, "maxgap")
        mp_rows.append(r)

    ensure(any(r["has_pairs"] for r in mp_rows), "multipads exist")
    ensure(all(r["all_gaps_le_e"] for r in mp_rows if r["has_pairs"]), "all gap law")

    return {
        "status": "PASS",
        "sep_rows": sep_rows,
        "min_rows": min_rows,
        "mp_rows": mp_rows,
        "summary": {
            "n_sep": len(sep_rows),
            "n_mp": len(mp_rows),
            "all_separated_formula_ok": True,
            "all_multipad_H_gaps_le_e": True,
            "deployed_e": E,
            "deployed_gap_cap": E,
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "note": (
                "multipad H has all consecutive support gaps <= e; "
                "board structure for fewnomial ban"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v72",
        "title": "Multipad H-support gap law (gaps <= e)",
        "status": "H_GAP_LAW_PROVED_DEPLOYED_BAN_OPEN",
        "claims": {
            "proves_full_support_shift_blocks": True,
            "proves_min_support_deg_lt_n": True,
            "proves_separated_monomials_product_support": True,
            "proves_multipad_H_gaps_le_e": True,
            "proves_H_diameter_bound": True,
            "proves_deployed_multipad_ban": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "full_shift": lemma_full_shift(),
            "min_support": lemma_min_support_deg_lt_n(),
            "gap_product": lemma_gap_product(),
            "multipad_gap_law": lemma_multipad_gap_law(),
            "diameter": lemma_diameter(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "H recovery / gap census"},
        "impact_on_program": {
            "closed": (
                "BOARD: multipad H-support is e-chained (all consecutive gaps <= e)"
            ),
            "wall": "use gap law + +/-1 G to ban deployed multipads",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    sep_lines = []
    for r in cert["toy_suite"]["sep_rows"]:
        sep_lines.append(
            f"| {r['p']} | {r['e']} | {r['s']} | {r['supp_prod']} | {r['expect']} |"
        )
    sep_tbl = "\n".join(sep_lines)
    mp_lines = []
    for r in cert["toy_suite"]["mp_rows"]:
        mp_lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['n_pairs']} | "
            f"{r['min_maxgap']} | {r['max_maxgap']} | "
            f"{'Y' if r['all_gaps_le_e'] else 'n'} |"
        )
    mp_tbl = "\n".join(mp_lines)
    return f"""# KB-MCA Route-D v72: multipad `H` gap law

Status: **H-support gap law PROVED** (board-ready structure); deployed multipad
ban still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED (this packet)

```text
If G = P_e * H is a free-1 multipad index polynomial
(supp G = 2e, P_e full support),
then every consecutive gap in supp(H) is <= e.
```

### Proof sketch

1. If `deg G < n` and `P_e|G`, `G≠0`, then `supp(G) ≥ e+1` (Vandermonde;  
   `X^n−1` has support 2 but degree `n`, so excluded).  
2. If some consecutive gap of `supp(H)` is `≥ e+1`, split `H = H_L + H_R`.  
3. Product supports of `P_e H_L` and `P_e H_R` are **disjoint**.  
4. Each side has `deg < n` and is a nonzero multiple of `P_e` ⇒ support `≥ e+1`.  
5. Hence `supp(G) ≥ 2e+2 > 2e`, contradiction.

### Corollary

Support of `H` is an **e-chain**: diameter `<= e(s-1)` for `s = #supp(H)`.

## Separated monomials (PROVED)

If terms of `H` are spaced `>= e+1` apart:

```text
supp(P_e H) = s (e+1)   (no cancellation)
```

Cannot equal multipad `2e` for integer `s` when `e >= 2`.

## CAS

### Separated products

| p | e | s | supp(PH) | s(e+1) |
|---|---:|---:|---:|---:|
{sep_tbl}

### Multipad H max consecutive gap

| p | e | t | #pairs | min maxgap | max maxgap | all <=e? |
|---|---:|---:|---:|---:|---:|---|
{mp_tbl}

## Deployed

| | |
|---|---:|
| e | {d['e']} |
| gap cap for multipad H | {d['e']} |
| n' | {d['n_prime']} |

## OPEN (next board hit)

Use the gap law + `G` in `{{-1,0,1}}` with `e` pluses/minuses to **forbid**
such `H` on `{{0..n'-1}}` — that would be a **deployed residual board close**.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v72.py --check
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
        "# kb-qatom-route-d-v72\n\n"
        "Multipad H-support gap law: all consecutive gaps <= e.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v72 report\n\nstatus: {cert['status']}\n"
        f"H gap law: PROVED\n"
        f"OPEN deployed multipad ban: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  separated H => supp(P H)=s(e+1): PROVED")
    print("  multipad => all consecutive gaps of supp(H) <= e: PROVED")
    print("  diameter <= e(s-1): PROVED")
    print(
        f"  CAS: sep={s['n_sep']}; mp={s['n_mp']}; all multipad H gaps <= e"
    )
    print("  BOARD: gap law closed; deployed multipad ban still OPEN")


if __name__ == "__main__":
    main()
