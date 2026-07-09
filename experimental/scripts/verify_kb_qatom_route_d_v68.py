#!/usr/bin/env python3
"""KB-MCA Route-D v68: free-1 high injectivity close path + e_e identity.

Completion attack after v67 closure board.

Proved:
  (1) Power-sum / free-1 phase (char > e). For free-1 monic high equivalent to
      power sums p1..p_{e-1} (v56; char p > e), and lambda != 0, there is a
      unique non-constant polynomial Q of degree at most e-1 with
        <lambda, high_power(U)> = sum_{x in U} Q(x)  (mod p, in the exponent).
  (2) Elementary-symmetric identity. Let v_0..v_{t-1} be the arc values and
        u_i = psi(Q(v_i)),
      then the free-1 high exponential sum is the elementary symmetric mean
        S(Q) = sum_{|U|=e} psi(sum_{x in U} Q(x)) = e_e(u_0,...,u_{t-1}),
      i.e. the coefficient of z^e in prod_i (1 + z u_i).
  (3) Injectivity => coll = 0 => |T| = 0. If the free-1 high map
        high: {e-subsets of I_t} -> F_p^{e-1}
      is injective, then m_h <= 1 for all h, coll = sum m(m-1) = 0, hence
      |T| <= coll/2 = 0 <= H2 (v57). This is an *unconditional* residual close
      on any (t,e) where injectivity holds — stronger than soft-B.
  (4) Multipad polynomial criterion. Distinct e-sets U,V with the same free-1
      monic high iff the monic polynomials f_U, f_V agree in degrees 1..e-1 and
        f_U - f_V = delta  (nonzero constant).
      Equivalently U = {x : f_V(x) = -delta} and V = {x : f_U(x) = delta},
      so U,V are full level sets of a monic degree-e polynomial at two values.
  (5) Pigeonhole room at deployed. log2 binom(n',e) ~ 3.73e5 and
      log2 p^{e-1} ~ 2.09e6, so binom(n',e) << p^{e-1}: injectivity is not
      obstructed by counting. Random-model expected coll has log2 ~ -1.34e6.
  (6) Soft-B remains sufficient (v64) but injectivity is the preferred close:
      coll=0 => residual empty, no need for Fourier B_*.

CAS:
  (7) Identity (2) holds (err ~ 1e-12) on e=3,4 toys.
  (8) Sparse e=4, t<=3e: often injective (coll=0); multipads appear as t grows.
  (9) term_clash=0 on all tested rows (matches v57 terminal injectivity).
  (10) Deployed pigeonhole / random-model numbers match v55/v64.

OPEN:
  Prove free-1 high injectivity on the deployed GP prefix of length n'
  (or SoftB_Deployed). Either closes |T|<=H2 via v67/v68.

Does NOT claim injectivity at deployed; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v68.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v68"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v68.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v68.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v68.report.md"
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


def log2_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def lemma_ee_identity() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_S_equals_elementary_symmetric_of_u",
        "statement": (
            "For Q of deg <= e-1: S = sum_{|U|=e} psi(sum_{x in U} Q(x)) "
            "= e_e(u) with u_i = psi(Q(v_i))."
        ),
        "proof": [
            "Expand prod_i (1 + z u_i) = sum_k z^k e_k(u).",
            "Coefficient of z^e is sum_{|I|=e} prod_{i in I} u_i "
            "= sum_{|I|=e} psi(sum_{i in I} Q(v_i)).",
        ],
    }


def lemma_injectivity_close() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "injectivity_implies_T_zero",
        "statement": (
            "If free-1 high is injective on e-subsets of I_t, then coll=0 "
            "and |T|<=coll/2=0 <= H2."
        ),
        "proof": [
            "Injective => m_h in {0,1} => coll = sum m(m-1) = 0.",
            "v57: |T| <= coll/2 = 0.",
        ],
    }


def lemma_multipad_poly() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_monic_polynomial_criterion",
        "statement": (
            "U!=V are free-1 multipads iff monic f_U, f_V differ by a nonzero "
            "constant delta (agree in degrees 1..e-1)."
        ),
        "proof": [
            "Free-1 monic high = coeffs of X^{e-1},...,X^1 (or equiv e1..e_{e-1}).",
            "Same high => f_U - f_V is constant delta.",
            "delta=0 => f_U=f_V => same root set (char 0 / distinct roots).",
        ],
    }


def lemma_pigeonhole_room() -> dict[str, Any]:
    log2C = log2_comb(N_PRIME, E)
    log2_space = (E - 1) * math.log2(P)
    return {
        "status": "PROVED",
        "name": "deployed_pigeonhole_room_for_injectivity",
        "statement": (
            f"log2 C ~ {log2C:.1f} << log2 p^{{e-1}} ~ {log2_space:.1f}; "
            "injectivity not counting-obstructed. E[coll] log2 ~ "
            f"{2*log2C - log2_space:.1f}."
        ),
        "proof": [
            "Image lives in F_p^{e-1} of size p^{e-1}.",
            "C = binom(n',e); compare logs by summing log2 ratios.",
        ],
        "numbers": {
            "log2_C": log2C,
            "log2_p_em1": log2_space,
            "log2_space_over_C": log2_space - log2C,
            "log2_expected_coll": 2 * log2C - log2_space,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_injectivity_or_SoftB_deployed",
        "statement": (
            "Prove free-1 high injectivity on the deployed GP prefix, "
            f"or SoftB max|S|<=B_*~{B_STAR:.0f}."
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


def monic_high_free1(roots: list[int], p: int) -> tuple[int, ...]:
    poly = [1]
    for x in roots:
        new = [0] * (len(poly) + 1)
        mv = (-x) % p
        for j, c in enumerate(poly):
            new[j] = (new[j] + c) % p
            new[j + 1] = (new[j + 1] + c * mv) % p
        poly = new
    e = len(roots)
    return tuple(poly[1:e])


def monic_poly_full(roots: list[int], p: int) -> list[int]:
    poly = [1]
    for x in roots:
        new = [0] * (len(poly) + 1)
        mv = (-x) % p
        for j, c in enumerate(poly):
            new[j] = (new[j] + c) % p
            new[j + 1] = (new[j + 1] + c * mv) % p
        poly = new
    return poly  # length e+1


def census_row(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    C = 0
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        h = monic_high_free1(roots, p)
        buckets[h].append(idxs)
        C += 1
    coll = 0
    maxm = 1
    multipads = 0
    for lst in buckets.values():
        m = len(lst)
        maxm = max(maxm, m)
        if m >= 2:
            multipads += 1
            coll += m * (m - 1)
    term_buckets: dict[tuple[int, ...], int] = defaultdict(int)
    for idxs in itertools.combinations(range(t), e):
        if (t - 1) not in idxs:
            continue
        roots = [vals[i] for i in idxs]
        term_buckets[monic_high_free1(roots, p)] += 1
    term_clash = sum(1 for m in term_buckets.values() if m >= 2)

    # multipad poly criterion spot-check
    poly_ok = True
    checked = 0
    for h, lst in buckets.items():
        if len(lst) < 2:
            continue
        for a, b in itertools.combinations(lst[:3], 2):
            pa = monic_poly_full([vals[i] for i in a], p)
            pb = monic_poly_full([vals[i] for i in b], p)
            # free-1 coeffs equal
            ensure(pa[1:e] == pb[1:e], "high match")
            # differ only in constant term index e
            mid_eq = all(pa[j] == pb[j] for j in range(e))  # 0..e-1? 
            # poly[0]=1, poly[1..e-1] free-1, poly[e]=const
            ensure(pa[0] == 1 and pb[0] == 1, "monic")
            ensure(pa[1:e] == pb[1:e], "free1")
            delta = (pa[e] - pb[e]) % p
            ensure(delta != 0, "distinct sets => delta!=0")
            # only constant differs among non-leading: degrees e-1..1 already equal
            checked += 1
            if checked >= 5:
                break
        if checked >= 5:
            break

    return {
        "p": p,
        "t": t,
        "e": e,
        "C": int(C),
        "distinct": len(buckets),
        "max_m": int(maxm),
        "coll": int(coll),
        "multipad_highs": int(multipads),
        "term_clash": int(term_clash),
        "injective": bool(maxm == 1),
        "T_zero_if_injective": True,
        "poly_criterion_checked": int(checked),
        "poly_criterion_ok": bool(poly_ok),
    }


def ee_identity_row(
    p: int, n: int, t: int, e: int, lams: list[int]
) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    ensure(len(lams) == e - 1, "lam len")

    def Q(x: int) -> int:
        s = 0
        for j, lam in enumerate(lams):
            s = (s + lam * pow(x, j + 1, p)) % p
        return s

    u = [np.exp(2j * np.pi * Q(v) / p) for v in vals]
    poly = np.array([1 + 0j])
    for ui in u:
        poly = np.convolve(poly, [1, ui])
    ee = poly[e] if e < len(poly) else 0j
    S = 0j
    for idxs in itertools.combinations(range(t), e):
        phase = 0
        for i in idxs:
            phase = (phase + Q(vals[i])) % p
        S += np.exp(2j * np.pi * phase / p)
    return {
        "p": p,
        "t": t,
        "e": e,
        "lams": lams,
        "abs_S": float(abs(S)),
        "abs_ee": float(abs(ee)),
        "err": float(abs(S - ee)),
        "ok": bool(abs(S - ee) < 1e-8),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(P > E, "char > e for Newton free-1")

    # pigeonhole
    log2C = log2_comb(N_PRIME, E)
    log2_space = (E - 1) * math.log2(P)
    log2_exp_coll = 2 * log2C - log2_space
    ensure(log2C < log2_space - 100, "room")
    ensure(log2_exp_coll < -1e6, "expected coll ~0")

    ee_rows = []
    for p, n, t, e, lams in [
        (61, 60, 12, 3, [1, 0]),
        (61, 60, 12, 3, [1, 1]),
        (61, 60, 12, 3, [3, 5]),
        (61, 60, 15, 4, [1, 0, 0]),
        (61, 60, 15, 4, [1, 1, 2]),
        (61, 60, 15, 4, [3, 5, 7]),
        (101, 100, 12, 3, [1, 0]),
        (101, 100, 12, 3, [2, 7]),
        (127, 126, 14, 3, [1, 1]),
        (127, 126, 16, 4, [1, 0, 1]),
    ]:
        r = ee_identity_row(p, n, t, e, lams)
        ensure(r["ok"], f"ee id {p},{t},{e}")
        ee_rows.append(r)

    census = []
    configs = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [3, 4, 5]:
            for t in [e + 2, 2 * e, 3 * e, min(4 * e, n // 2)]:
                if t < e or t > n:
                    continue
                if math.comb(t, e) > 30000:
                    continue
                configs.append((p, n, t, e))
    for p, n, t, e in configs:
        r = census_row(p, n, t, e)
        ensure(r["term_clash"] == 0, "term clash")
        if r["injective"]:
            ensure(r["coll"] == 0, "inj coll")
        census.append(r)

    ensure(len(census) >= 12, "census")
    ensure(any(r["injective"] for r in census), "some injective")
    ensure(any(not r["injective"] for r in census), "some multipads exist")
    # sparse e=4 at t=2e often injective
    sparse4 = [
        r
        for r in census
        if r["e"] == 4 and r["t"] <= 2 * r["e"] + 2
    ]
    ensure(all(r["injective"] for r in sparse4), "sparse e4 inj")

    return {
        "status": "PASS",
        "ee_rows": ee_rows,
        "census": census,
        "deployed_injectivity_room": {
            "log2_C": float(log2C),
            "log2_p_em1": float(log2_space),
            "log2_p_em1_over_C": float(log2_space - log2C),
            "log2_expected_coll": float(log2_exp_coll),
            "pigeonhole_obstruction": False,
            "random_model_coll_empty": True,
        },
        "summary": {
            "n_ee": len(ee_rows),
            "n_census": len(census),
            "n_injective": sum(1 for r in census if r["injective"]),
            "n_with_multipads": sum(1 for r in census if not r["injective"]),
            "max_coll": max(r["coll"] for r in census),
            "all_term_clash_zero": True,
            "all_ee_ok": True,
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
                "injectivity => |T|=0 PROVED as implication; "
                "deployed injectivity OPEN (random model empty coll)"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v68",
        "title": "Free-1 high injectivity close path + e_e identity",
        "status": "INJECTIVITY_PATH_PROVED_DEPLOYED_INJ_OPEN",
        "claims": {
            "proves_S_equals_ee_of_u": True,
            "proves_injectivity_implies_T_zero": True,
            "proves_multipad_poly_criterion": True,
            "proves_deployed_pigeonhole_room": True,
            "proves_deployed_injectivity": False,
            "proves_SoftB_Deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "ee_identity": lemma_ee_identity(),
            "injectivity_close": lemma_injectivity_close(),
            "multipad_poly": lemma_multipad_poly(),
            "pigeonhole_room": lemma_pigeonhole_room(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy": "e_e identity", "python_nt": "GP multipad census"},
        "impact_on_program": {
            "closed": (
                "Preferred residual close: free-1 high injectivity => coll=0 => |T|=0; "
                "S=e_e(u) identity for power-sum phase"
            ),
            "wall": "prove injectivity (or SoftB) at deployed GP prefix",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    room = cert["toy_suite"]["deployed_injectivity_room"]
    d = cert["deployed"]
    cen_lines = []
    for r in cert["toy_suite"]["census"]:
        cen_lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['C']} | {r['distinct']} | "
            f"{r['max_m']} | {r['coll']} | {r['term_clash']} | "
            f"{'Y' if r['injective'] else 'n'} |"
        )
    cen_tbl = "\n".join(cen_lines)
    return f"""# KB-MCA Route-D v68: injectivity close path

Status: **injectivity ⇒ |T|=0 PROVED** as implication; deployed injectivity
**OPEN**. Local on `scott/kb-route-d-T-bound`.

## Preferred completion path

```text
free-1 high injective on e-subsets of I_{{n'}}
        =>  coll = 0
        =>  |T| = 0  <= H2     (v57)
```

This is stronger than soft-B (v64/v67): no Fourier bound needed if injectivity holds.

## S = e_e(u) (PROVED)

For power-sum / free-1 phase with `u_i = psi(Q(v_i))`:

```text
S = sum_{{|U|=e}} psi(sum_{{x in U}} Q(x)) = e_e(u_0,...,u_{{t-1}})
```

## Multipad criterion (PROVED)

`U ≠ V` share a free-1 high iff monic `f_U - f_V` is a nonzero constant.

## Deployed counting room (PROVED arithmetic)

| quantity | value |
|---|---:|
| log2 C | {room['log2_C']:.2f} |
| log2 p^{{e-1}} | {room['log2_p_em1']:.2f} |
| log2(p^{{e-1}}/C) | {room['log2_p_em1_over_C']:.2f} |
| log2 E[coll] (random) | {room['log2_expected_coll']:.1f} |

No pigeonhole obstruction; random model predicts **empty coll**.

## CAS

| p | e | t | C | distinct | max m | coll | term_clash | inj? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
{cen_tbl}

- e_e identity rows: {s['n_ee']} (all OK)
- injective rows: {s['n_injective']} / {s['n_census']}
- all terminal clash = 0
- sparse e=4 at t~2e: injective on tested primes

## Link to closure board (v67)

| path | status |
|---|---|
| SoftB_Deployed => |T|<=H2 | CONDITIONAL (v64–v67) |
| **Injectivity => |T|=0** | **implication CLOSED (v68)** |
| Deployed injectivity / SoftB | **OPEN** |

B_\\* ≈ {d['B_star']:.1f} remains a fallback sufficient bound.

## OPEN

1. Prove free-1 high **injectivity** on the deployed GP prefix of length n'.  
2. Or prove SoftB_Deployed.  
3. Either yields residual certificate `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v68.py --check
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
        "# kb-qatom-route-d-v68\n\n"
        "Injectivity => |T|=0 close path; S=e_e(u); deployed injectivity OPEN.\n"
    )
    s = cert["toy_suite"]["summary"]
    room = cert["toy_suite"]["deployed_injectivity_room"]
    REPORT_PATH.write_text(
        f"# v68 report\n\nstatus: {cert['status']}\n"
        f"injectivity => |T|=0: PROVED implication\n"
        f"S=e_e(u): PROVED\n"
        f"deployed injectivity: OPEN\n"
        f"log2 E[coll]: {room['log2_expected_coll']:.1f}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  S = e_e(u) (power-sum phase): PROVED")
    print("  free-1 high injective => coll=0 => |T|=0: PROVED")
    print("  multipad monic poly criterion: PROVED")
    print(
        f"  deployed: log2 E[coll]={room['log2_expected_coll']:.1f}; "
        f"pigeonhole room log2={room['log2_p_em1_over_C']:.1f}"
    )
    print(
        f"  CAS: ee={s['n_ee']}; census={s['n_census']}; "
        f"injective={s['n_injective']}; multipad rows={s['n_with_multipads']}; "
        f"term_clash always 0"
    )
    print("  OPEN: deployed injectivity (or SoftB)")


if __name__ == "__main__":
    main()
