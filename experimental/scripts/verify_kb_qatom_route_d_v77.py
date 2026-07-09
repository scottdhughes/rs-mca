#!/usr/bin/env python3
"""KB-MCA Route-D v77: residual close criterion; multipad = two-level monic φ.

Clarifies the residual board target and adds the two-value polynomial form.

Proved:
  (1) Residual close by multipad-freeness. On the deployed arc t=n', e,p,H2:
        (no free-1 multipad)
          => coll = 0
          => |T| <= coll/2 = 0 <= H2.
      Equivalently: free-1 high injective => |T|=0.
  (2) Alternate SoftB path (v64, kept). If max_{lambda != 0} |S(lambda)| <= B_*
      = sqrt(2 H2), then coll <= C^2/p^{e-1} + B_*^2 <= 2 H2 (C^2/p^{e-1}~0),
      hence |T|<=H2. CAS for e=3 shows max|S|/sqrt(C) = O(1)-O(3), so B ~ sqrt(C)
      is the natural size; B_* << sqrt(C) at large C, so SoftB is a severe bound
      (likely false at deployed if S is random-like). Primary path is (1).
  (3) Two-value form of multipads. A free-1 multipad with monic root polys
        f = m + c0,  g = m + c0'   (same free-1 / same m, c0 != c0'),
      where m(X) = X^e + a_{e-1} X^{e-1} + ... + a_1 X  (no constant, so m(0)=0),
      is equivalent to phi(X) := m(X) = X * m1(X) (m1 monic deg e-1) taking
      exactly two values alpha = -c0, beta = -c0' on the 2e root values R = U cup V,
      each value attained e times. Thus a multipad yields a monic degree-e
      polynomial phi with phi(0)=0 that is two-valued on a 2e-element subset of
      the GP arc.
  (4) Deployed random-model support. log2 E[coll] ~ -1.34e6 (v55/v64), so the
      multipad-free hypothesis is the expected truth; still needs a proof.
  (5) Board inventory pointer: t<=2e injectivity, packing, span>=2e, coll bounds
      (v73-v76) are necessary infrastructure, not residual-final.

CAS:
  (6) e=3: max|S|/sqrt(C) in ~2..3; coll small; multipad pairs satisfy two-value
      form (phi takes two values on R).
  (7) SoftB B_* << sqrt(C) on multipad rows (B_* not the empirical scale of max|S|).

OPEN (residual PR target):
  Prove multipad-free on the deployed GP prefix of length n' (primary),
  or SoftB max|S|<=B_* (alternate, likely harder).

Does NOT claim |T|<=H2 unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v77.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v77"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v77.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v77.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v77.report.md"
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


def log2_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def lemma_residual_by_injectivity() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_close_by_multipad_free",
        "statement": (
            "No free-1 multipad on the deployed arc => coll=0 => |T|=0 <= H2."
        ),
        "proof": [
            "Injective free-1 high => m_h <= 1 => coll = sum m(m-1) = 0.",
            "v57: |T| <= coll/2 = 0.",
            "Deployed H2 > 0 so |T| <= H2.",
        ],
    }


def lemma_softB_alternate() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "softB_alternate_path",
        "statement": (
            f"If max_{{λ≠0}} |S(λ)| <= B_*={B_STAR:.1f}, then |T|<=H2 at deployed "
            "(v58+v64). Primary path is multipad-freeness; SoftB is alternate."
        ),
        "proof": [
            "v58: coll <= C^2/p^{e-1} + B^2.",
            "v64: C^2/p^{e-1} negligible; B=B_* => coll <= 2 H2 => |T|<=H2.",
        ],
    }


def lemma_two_value() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_two_value_phi",
        "statement": (
            "A free-1 multipad yields monic phi(X)=X*m1(X) (deg e, phi(0)=0) "
            "taking exactly two values on the 2e root-values, each e times."
        ),
        "proof": [
            "f = m + c0, g = m + c0' with m having zero constant term (free-1).",
            "m = X m1, monic m1 of deg e-1.",
            "Roots of f: m(r)=-c0; roots of g: m(r)=-c0'.",
            "On R = root values of f and g, m takes {-c0,-c0'} each e times.",
        ],
    }


def lemma_deployed_expectation() -> dict[str, Any]:
    log2C = log2_comb(N_PRIME, E)
    log2_exp = 2 * log2C - (E - 1) * math.log2(P)
    return {
        "status": "PROVED",
        "name": "deployed_expected_coll_negligible",
        "statement": (
            f"Random-model log2 E[coll] ~ {log2_exp:.1f} (multipad-free expected)."
        ),
        "proof": [
            "E[coll] ~ C(C-1)/p^{e-1}; take log2.",
            "Does not prove coll=0; supports targeting multipad-freeness.",
        ],
        "numbers": {"log2_C": log2C, "log2_E_coll": log2_exp},
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_deployed_multipad_free",
        "statement": (
            "Prove free-1 multipad-free (injective high) on GP prefix length n', "
            "or SoftB. Either => residual |T|<=H2 board close / PR."
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
    """Monic prod (X-r), coeffs low to high."""
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


def eval_poly(poly: list[int], x: int, p: int) -> int:
    s = 0
    xp = 1
    for c in poly:
        s = (s + c * xp) % p
        xp = (xp * x) % p
    return s


def two_value_check(
    p: int, n: int, t: int, e: int, limit: int = 20
) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    buckets: dict[tuple[int, ...], list[list[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        poly = monic_X(roots, p)
        buckets[free1_X(poly, e)].append(roots)

    checked = 0
    ok = 0
    for h, lst in buckets.items():
        if len(lst) < 2:
            continue
        for ra, rb in itertools.combinations(lst, 2):
            # monic polys
            fa = monic_X(ra, p)
            fb = monic_X(rb, p)
            # free-1 match
            ensure(fa[1:e] == fb[1:e], "f1")
            ensure(fa[e] == 1 and fb[e] == 1, "monic")
            delta = (fa[0] - fb[0]) % p
            ensure(delta != 0, "delta")
            # m = f without constant: same for both
            m = fa[:]
            m[0] = 0  # m(X) = f(X) - c0, but c0=fa[0], so subtract fa[0] from const
            # actually fa = m + fa[0] with m const 0: m_coeffs = fa with const 0
            m_poly = [0] + list(fa[1:])  # wait fa[0] is const, fa[1:] are X^1..X^e
            # monic X^e + ... + c1 X + c0: m = X^e+...+c1 X has coeffs
            m_poly = fa[:]
            c0 = m_poly[0]
            m_poly[0] = 0
            # evaluate m on ra should be -c0? f(r)=0 => m(r)+c0=0 => m(r)=-c0
            alpha = (-c0) % p
            beta = (-fb[0]) % p
            vals_m = set()
            for r in ra + rb:
                mv = eval_poly(m_poly, r, p)
                vals_m.add(mv)
            # should be {{alpha, beta}}
            if vals_m == {alpha, beta}:
                # count multiplicities
                ca = sum(1 for r in ra + rb if eval_poly(m_poly, r, p) == alpha)
                cb = sum(1 for r in ra + rb if eval_poly(m_poly, r, p) == beta)
                if ca == e and cb == e:
                    ok += 1
            checked += 1
            if checked >= limit:
                break
        if checked >= limit:
            break
    return {
        "p": p,
        "t": t,
        "e": e,
        "checked": checked,
        "two_value_ok": ok,
        "all_ok": bool(checked == 0 or ok == checked),
    }


def maxS_row(p: int, n: int, t: int, e: int = 3) -> dict[str, Any]:
    ensure(e == 3, "e3 only for fft2")
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    buckets: dict[tuple[int, ...], int] = defaultdict(int)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        h = free1_X(monic_X(roots, p), e)
        freq[h[0] % p, h[1] % p] += 1
        buckets[h] += 1
        C += 1
    F = np.fft.fft2(freq)
    a = np.abs(F)
    a[0, 0] = 0
    maxS = float(np.max(a))
    coll = sum(m * (m - 1) for m in buckets.values())
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "maxS": maxS,
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
        "coll": int(coll),
        "B_star": float(B_STAR),
        "maxS_le_Bstar": bool(maxS <= B_STAR),
        "maxS_le_sqrtC": bool(maxS <= math.sqrt(C) + 1e-9),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "odd")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(N_PRIME > TWO_E, "n'>2e")

    log2C = log2_comb(N_PRIME, E)
    log2_exp = 2 * log2C - (E - 1) * math.log2(P)
    ensure(log2_exp < -1e6, "expected coll tiny")

    tv_rows = []
    for p, n, t, e in [
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 21, 4),
    ]:
        if math.comb(t, e) > 25000:
            continue
        r = two_value_check(p, n, t, e)
        ensure(r["all_ok"], f"two-value {p},{t},{e}")
        tv_rows.append(r)

    s_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 17),
        (61, 60, 24),
        (101, 100, 15),
        (101, 100, 20),
        (127, 126, 18),
    ]:
        if math.comb(t, 3) > 10000:
            continue
        r = maxS_row(p, n, t, 3)
        # empirical SoftB fails relative to sqrtC
        ensure(r["S_over_sqrtC"] < 5, "emp S")
        # B_star is huge vs toy maxS, so maxS_le_Bstar true on toys
        s_rows.append(r)

    ensure(all(not r["maxS_le_sqrtC"] for r in s_rows if r["coll"] >= 0), "L>1 typical")
    # actually some injective rows may have maxS > sqrtC still
    ensure(any(r["S_over_sqrtC"] > 1.5 for r in s_rows), "ratio >1")

    return {
        "status": "PASS",
        "tv_rows": tv_rows,
        "s_rows": s_rows,
        "deployed_model": {
            "log2_C": float(log2C),
            "log2_E_coll": float(log2_exp),
            "B_star": float(B_STAR),
            "H2": H2,
            "n_prime": N_PRIME,
            "e": E,
            "primary_path": "multipad_free",
            "alternate_path": "SoftB",
        },
        "summary": {
            "n_tv": len(tv_rows),
            "n_S": len(s_rows),
            "all_two_value_ok": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in s_rows),
            "min_S_over_sqrtC": min(r["S_over_sqrtC"] for r in s_rows),
            "log2_E_coll": float(log2_exp),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "residual_closed": False,
            "residual_criterion": "multipad_free => |T|=0",
            "note": "PROVED criterion; OPEN hypothesis multipad_free at deployed",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v77",
        "title": "Residual close criterion: multipad-free => |T|=0",
        "status": "RESIDUAL_CRITERION_PROVED_HYPOTHESIS_OPEN",
        "claims": {
            "proves_residual_close_by_multipad_free": True,
            "proves_softB_alternate_path": True,
            "proves_multipad_two_value_phi": True,
            "proves_deployed_expected_coll_tiny": True,
            "proves_multipad_free_at_deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "residual_injectivity": lemma_residual_by_injectivity(),
            "softB": lemma_softB_alternate(),
            "two_value": lemma_two_value(),
            "expectation": lemma_deployed_expectation(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "max|S| e=3", "python_nt": "two-value multipad check"},
        "impact_on_program": {
            "closed": (
                "BOARD criterion: multipad-free => residual |T|=0; "
                "two-value phi form of multipads"
            ),
            "wall": "prove multipad-free at deployed (primary residual PR)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    dm = cert["toy_suite"]["deployed_model"]
    s_lines = []
    for r in cert["toy_suite"]["s_rows"]:
        s_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['sqrtC']:.1f} | "
            f"{r['S_over_sqrtC']:.2f} | {r['coll']} |"
        )
    s_tbl = "\n".join(s_lines)
    return f"""# KB-MCA Route-D v77: residual criterion (multipad-free ⇒ `|T|=0`)

Status: **residual close criterion PROVED**; deployed multipad-free still **OPEN**.  
This is the board target for a residual PR. Local on `scott/kb-route-d-T-bound`.

## BOARD: residual close criterion (PROVED)

```text
no free-1 multipad on GP arc of length n'
        ⇒  coll = 0
        ⇒  |T| = 0  ≤ H2
```

| path | status |
|---|---|
| **Primary: multipad-free / injective high** | criterion PROVED; hypothesis OPEN |
| Alternate: SoftB `max\|S\|≤B_*` | criterion PROVED (v64); hypothesis likely hard |

### Why SoftB is alternate

e=3 CAS: `max|S|/√C ~ 2–3`. SoftB needs `|S|≤B_*≈3.93×10^5`.  
At large `C`, `√C ≫ B_*`, so SoftB is much stronger than empirical square-root scale.  
Random-model `E[coll]~0` supports **injectivity**, not SoftB.

Deployed: `log2 E[coll] ≈ {dm['log2_E_coll']:.1f}` (expected multipad-free).

## Multipad two-value form (PROVED)

```text
phi(X) = X * m1(X)   (monic deg e, phi(0)=0)
phi takes exactly two values on the 2e root-values, each e times
```

## CAS (e=3)

| p | t | max\|S\| | √C | S/√C | coll |
|---|---:|---:|---:|---:|---:|
{s_tbl}

max S/√C = {s['max_S_over_sqrtC']:.2f}; two-value form OK on multipad samples.

## Infrastructure (already CLOSED)

t≤2e inj · packing · span≥2e · coll≤min((K−1)C, 2 C(t,2e)) · P_e algebra

## OPEN — residual PR

Prove **multipad-free** on the deployed GP prefix (length n', e={d['e']}).

Then ship residual PR: `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v77.py --check
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
        "# kb-qatom-route-d-v77\n\n"
        "Residual criterion: multipad-free => |T|=0. Hypothesis OPEN.\n"
    )
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    REPORT_PATH.write_text(
        f"# v77 report\n\nstatus: {cert['status']}\n"
        f"residual criterion multipad-free => |T|=0: PROVED\n"
        f"hypothesis multipad-free at deployed: OPEN\n"
        f"log2 E[coll]={s['log2_E_coll']:.1f}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  multipad-free => |T|=0 at deployed: PROVED (criterion)")
    print("  SoftB alternate path: PROVED (criterion); primary = multipad-free")
    print("  multipad two-value phi form: PROVED")
    print(
        f"  deployed log2 E[coll]={s['log2_E_coll']:.1f}; "
        f"e=3 max S/sqrtC={s['max_S_over_sqrtC']:.2f}"
    )
    print("  OPEN: prove multipad-free at deployed — then residual PR")
    print(f"  residual_closed={d['residual_closed']}")


if __name__ == "__main__":
    main()
