#!/usr/bin/env python3
"""KB-MCA Route-D v58: Fourier identity for coll + conditional square-root cancel.

Attacks |T| via coll (v57): |T| <= nH <= coll/2.

Proved:
  (1) Plancherel identity on F_p^{e-1}. Let m_h = # e-subsets of I_t with monic
      high h, C = binom(t,e), d = e-1. With additive characters psi and
        S(lambda) = sum_{e-subsets U} psi(<lambda, high(U)>),
      one has
        sum_h m_h^2 = p^{-d} sum_{lambda} |S(lambda)|^2,
        S(0) = C,
        coll := sum_h m_h(m_h-1) = sum m_h^2 - C.
  (2) Conditional bound: if |S(lambda)| <= B for all lambda != 0, then
        coll <= C^2/p^d + B^2 - C + C/p^d
             <= C^2/p^d + B^2.
  (3) Square-root cancellation corollary: if B <= sqrt(C), then
        coll <= C^2 / p^{e-1}.
      At deployed (n',e,p), C^2/p^{e-1} has log2 ~ -1.34e6, so coll = 0 and T=0
      under this hypothesis.
  (4) e=2 closed form:
        S(lam) = (1/2) ( G(lam)^2 - G(2 lam) ),
      G(lam) = sum_{i=0}^{t-1} psi(lam * omega^i)  (arc of GP values).
      Trivial |G|<=t => |S| <= (t^2+t)/2, giving coll = O(t^4) (too weak for
      H2 via coll, but e=2 already closed by |T|<=p).

CAS (numpy FFT):
  (5) Identity (1) holds to numerical error ~1e-12.
  (6) Empirical max_{lam!=0}|S|/sqrt(C) is O(1)-O(10) on tested (p,t,e=2,3),
      i.e. near square-root cancellation — not a proof.
  (7) Trivial e=2 geom bound B=O(t^2) is far too large at deployed scale.

OPEN:
  Prove |S(lambda)| <= sqrt(C) * L (any L with L^2 C^0 <= 2 H2 after the
  C^2/p^d term, e.g. L=1) for free-1 high exponential sums on GP arcs in the
  sparse regime — or any B with B^2 + C^2/p^{e-1} <= 2 H2.

Does NOT claim |T|<=H2 unconditionally for e>2; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v58.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v58"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v58.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v58.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v58.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T_ROW = A - 2**20
W = T_ROW - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
N_PRIME = A + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


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


def lemma_plancherel() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "plancherel_collision_identity",
        "statement": (
            "With d=e-1, C=binom(t,e), S(lambda)=sum_U psi(<lambda,high(U)>), "
            "sum_h m_h^2 = p^{-d} sum_lambda |S(lambda)|^2 and "
            "coll = sum m_h^2 - C."
        ),
        "proof": [
            "Fourier inversion / Plancherel for the finite abelian group F_p^d:",
            "sum_h m_h^2 = p^{-d} sum_lambda |hat m(lambda)|^2 with hat m = S.",
            "coll = sum_h m_h(m_h-1) = sum m_h^2 - sum m_h = sum m_h^2 - C.",
        ],
    }


def lemma_conditional_B() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coll_bound_from_max_S",
        "statement": (
            "If |S(lambda)| <= B for all lambda != 0, then "
            "coll <= C^2/p^{e-1} + B^2 - C + C/p^{e-1} <= C^2/p^{e-1} + B^2."
        ),
        "proof": [
            "sum m^2 = p^{-d}(C^2 + sum_{lam!=0}|S|^2) <= p^{-d}(C^2 + (p^d-1)B^2)",
            "  = C^2/p^d + B^2 - B^2/p^d.",
            "coll = sum m^2 - C <= C^2/p^d + B^2 - C.",
            "(Dropping negative -B^2/p^d strengthens the upper bound only by "
            "replacing with +B^2; the stated form keeps -C + C/p^d from "
            "expanding carefully: sum m^2 <= C^2/p^d + B^2(1-p^{-d}), "
            "coll <= C^2/p^d + B^2 - C + o(1) for large p^d.)",
        ],
    }


def lemma_sqrt_cancel() -> dict[str, Any]:
    log2_term = 2 * log2_comb(N_PRIME, E) - (E - 1) * math.log2(P)
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "sqrt_cancellation_implies_T_empty_deployed",
        "statement": (
            "If |S(lambda)| <= sqrt(C) for all lambda != 0 (square-root cancellation), "
            "then coll <= C^2/p^{e-1}. At deployed (n',e,p) this is < 1 "
            f"(log2 ~ {log2_term:.1f}), hence coll=0, nH=0, T=0, residual card closes."
        ),
        "proof": [
            "Apply conditional bound with B^2 = C: coll <= C^2/p^d + C - C = C^2/p^d.",
            "Deployed C=binom(n',e), d=e-1: direct log-combinatorics.",
        ],
        "values": {"log2_C2_over_pe": log2_term, "H2": H2},
        "gap": "Square-root cancellation is NOT proved for free-1 high sums on GP arcs.",
    }


def lemma_e2_closed_form() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_S_closed_form",
        "statement": (
            "For e=2, high(U) = -(v_i+v_j) for U={i,j}. Then "
            "S(lam) = (1/2)(G(lam)^2 - G(2 lam)) with "
            "G(lam)=sum_{k=0}^{t-1} psi(lam * omega^k)."
        ),
        "proof": [
            "sum_{i<j} f_i f_j = ((sum f_i)^2 - sum f_i^2)/2 with f_k=psi(lam v_k).",
            "f_k^2 = psi(2 lam v_k).",
        ],
        "note": "Trivial |G|<=t gives |S|<=(t^2+t)/2; too weak for H2 via coll. e=2 uses |T|<=p.",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_sqrt_cancellation_or_B_bound",
        "statement": (
            "Prove |S(lambda)| <= sqrt(C) (or any B with "
            "C^2/p^{e-1} + B^2 <= 2 H2) for free-1 monic-high exponential sums "
            f"on the length-n'={N_PRIME} KB arc at e={E}."
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


def e2_fft_row(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros(p, dtype=np.float64)
    C = 0
    for i, j in itertools.combinations(range(t), 2):
        h = (-(vals[i] + vals[j])) % p
        freq[h] += 1
        C += 1
    sum_m2 = float(np.dot(freq, freq))
    coll = sum_m2 - C
    F = np.fft.fft(freq)
    absS = np.abs(F)
    maxB = float(np.max(absS[1:]))
    recon = float(np.dot(absS, absS) / p)
    # closed form max |S|
    maxB2 = 0.0
    if p <= 300:
        for lam in range(1, p):
            s1 = sum(np.exp(-2j * np.pi * lam * vals[i] / p) for i in range(t))
            s2 = sum(np.exp(-2j * np.pi * ((2 * lam) % p) * vals[i] / p) for i in range(t))
            S = 0.5 * (s1 * s1 - s2)
            maxB2 = max(maxB2, abs(S))
    else:
        maxB2 = None
    Btriv = 0.5 * (t * t + t)
    return {
        "p": p,
        "e": 2,
        "t": t,
        "C": C,
        "coll": int(round(coll)),
        "sum_m2": sum_m2,
        "recon": recon,
        "maxB": maxB,
        "maxB2": maxB2,
        "sqrtC": math.sqrt(C),
        "B_over_sqrtC": maxB / math.sqrt(C),
        "Btriv": Btriv,
        "cond_bound": C * C / p + maxB * maxB,
        "recon_err": abs(recon - sum_m2),
        "closed_form_match": (
            bool(abs(maxB - maxB2) < 1e-6) if maxB2 is not None else None
        ),
    }


def e3_fft_row(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    for idxs in itertools.combinations(range(t), 3):
        h = monic_high(idxs, vals, p, 3)
        freq[h[0] % p, h[1] % p] += 1
        C += 1
    sum_m2 = float(np.sum(freq * freq))
    coll = sum_m2 - C
    F = np.fft.fft2(freq)
    absS = np.abs(F)
    absS0 = absS.copy()
    absS0[0, 0] = 0
    maxB = float(np.max(absS0))
    recon = float(np.sum(absS * absS) / (p * p))
    return {
        "p": p,
        "e": 3,
        "t": t,
        "C": C,
        "coll": int(round(coll)),
        "sum_m2": sum_m2,
        "recon": recon,
        "maxB": maxB,
        "sqrtC": math.sqrt(C),
        "B_over_sqrtC": maxB / math.sqrt(C),
        "cond_bound": C * C / (p * p) + maxB * maxB,
        "recon_err": abs(recon - sum_m2),
        "exp_coll": C * (C - 1) / (p * p),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P > E, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    # deployed entropy under sqrt cancel
    log2_term = 2 * log2_comb(N_PRIME, E) - (E - 1) * math.log2(P)
    ensure(log2_term < -1000, "deployed C2/pe tiny")

    e2_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126), (10007, 5003)]:
        for t in [16, 24, 34, 50]:
            if t > n:
                continue
            r = e2_fft_row(p, n, t)
            ensure(r["recon_err"] < 1e-6, "e2 plancherel")
            ensure(r["coll"] >= 0, "coll")
            # conditional bound holds
            ensure(r["coll"] <= r["cond_bound"] + 1e-6, "cond B")
            if r["closed_form_match"] is not None:
                ensure(r["closed_form_match"], "e2 closed form")
            e2_rows.append(r)

    ensure(len(e2_rows) >= 8, "e2 rows")

    e3_rows = []
    for p, n in [(31, 30), (61, 60)]:
        for t in [12, 18, 24, 30]:
            if t > n:
                continue
            r = e3_fft_row(p, n, t)
            ensure(r["recon_err"] < 1e-6, "e3 plancherel")
            ensure(r["coll"] <= r["cond_bound"] + 1e-6, "e3 cond")
            e3_rows.append(r)

    ensure(len(e3_rows) >= 6, "e3 rows")

    # empirical near-sqrt cancel: B/sqrtC not huge
    ensure(all(r["B_over_sqrtC"] < 20 for r in e2_rows + e3_rows), "B not wild")

    # trivial bound fails deployed-scale comparison for e=2 path via coll
    t_dep = N_PRIME
    Btriv = 0.5 * (t_dep * t_dep + t_dep)
    ensure(Btriv * Btriv > 2 * H2, "trivial too weak")

    return {
        "status": "PASS",
        "e2_rows": e2_rows,
        "e3_rows": e3_rows,
        "census": {
            "n_e2": len(e2_rows),
            "n_e3": len(e3_rows),
            "all_plancherel_ok": True,
            "all_cond_bound_ok": True,
            "max_B_over_sqrtC": max(
                r["B_over_sqrtC"] for r in e2_rows + e3_rows
            ),
            "min_B_over_sqrtC": min(
                r["B_over_sqrtC"] for r in e2_rows + e3_rows
            ),
            "log2_C2_over_pe_deployed": log2_term,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "log2_C2_over_pe": log2_term,
            "sqrt_cancel_implies_T_empty": True,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v58",
        "title": "Fourier coll identity + conditional square-root cancellation",
        "status": "FOURIER_PROVED_SQRT_CANCEL_OPEN",
        "claims": {
            "proves_plancherel_coll_identity": True,
            "proves_coll_bound_from_max_S": True,
            "proves_sqrt_cancel_implies_T_empty_deployed": True,
            "proves_e2_S_closed_form": True,
            "proves_sqrt_cancellation": False,
            "proves_T_le_H2_deployed_unconditional": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "plancherel": lemma_plancherel(),
            "cond_B": lemma_conditional_B(),
            "sqrt_cancel": lemma_sqrt_cancel(),
            "e2_form": lemma_e2_closed_form(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {
            "numpy_fft": "Plancherel verification e=2,3",
            "python_nt": "GP domain + monic high",
        },
        "impact_on_program": {
            "closed": (
                "coll controlled by max |S|; sqrt-cancel => T=0 at deployed"
            ),
            "wall": "prove square-root (or better) cancellation for S(lambda)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    e2 = sorted(cert["toy_suite"]["e2_rows"], key=lambda r: (r["p"], r["t"]))[:12]
    lines = []
    for r in e2:
        lines.append(
            f"| {r['p']} | {r['t']} | {r['coll']} | {r['maxB']:.1f} | "
            f"{r['sqrtC']:.1f} | {r['B_over_sqrtC']:.2f} | {r['recon_err']:.0e} |"
        )
    tbl = "\n".join(lines)
    e3 = cert["toy_suite"]["e3_rows"][:8]
    lines3 = []
    for r in e3:
        lines3.append(
            f"| {r['p']} | {r['t']} | {r['coll']} | {r['exp_coll']:.1f} | "
            f"{r['maxB']:.1f} | {r['B_over_sqrtC']:.2f} |"
        )
    tbl3 = "\n".join(lines3)
    return f"""# KB-MCA Route-D v58: Fourier identity for `coll` + conditional √-cancel

Status: **Plancherel + conditional bounds PROVED**; square-root cancellation **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Goal

```text
|T| <= coll/2
```
Close residual if `coll/2 <= H2` at deployed scale.

## Plancherel (PROVED)

```text
sum_h m_h^2 = p^{{-(e-1)}} sum_lambda |S(lambda)|^2
S(lambda) = sum_{{e-subsets U of I_t}} psi(<lambda, high(U)>)
coll = sum m_h^2 - C,   C = binom(t,e)
```

## Conditional bound (PROVED)

If `|S(lambda)| <= B` for all `lambda != 0`:

```text
coll  <=  C^2 / p^{{e-1}}  +  B^2
```

### Square-root cancellation corollary (PROVED conditional)

If `B <= sqrt(C)` for all nontrivial lambda:

```text
coll  <=  C^2 / p^{{e-1}}
```

**Deployed:** `log2(C^2/p^{{e-1}}) ≈ {d['log2_C2_over_pe']:.1f}` ⇒ `coll = 0` ⇒ `T = 0`.

This is the cleanest residual-card close — **if** √-cancellation is proved.

## e=2 closed form (PROVED)

```text
S(lam) = (1/2)( G(lam)^2 - G(2 lam) )
G(lam) = sum_{{k < t}} psi(lam * omega^k)
```

Trivial `|G|<=t` ⇒ `|S|<=(t^2+t)/2` (too weak for H2 via coll; e=2 already uses `|T|<=p`).

## CAS (numpy FFT)

### e=2

| p | t | coll | max|B| | √C | B/√C | recon err |
|---|---:|---:|---:|---:|---:|---:|
{tbl}

### e=3

| p | t | coll | exp | max|B| | B/√C |
|---|---:|---:|---:|---:|---:|
{tbl3}

Census: Plancherel OK; B/√C in [{cen['min_B_over_sqrtC']:.2f}, {cen['max_B_over_sqrtC']:.2f}]
(near square-root cancellation empirically, not a proof).

## Gap

| Bound on max|S| | Enough for deployed T=0? |
|---|---|
| Trivial e=2 O(t²) | No |
| √C (random / L² folklore) | **Yes** (conditional theorem) |
| Proved √C for free-1 highs on GP | **OPEN** |

## OPEN

Prove square-root cancellation (or any sufficient B) for

```text
S(lambda) = sum_{{U subset I_{{n'}}, |U|=e}} psi(<lambda, high(U)>)
```

on the KB roots-of-unity arc — especially e≥3 sparse regime.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v58.py --check
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
        "# kb-qatom-route-d-v58\n\n"
        "Fourier coll identity + conditional square-root cancellation.\n"
    )
    REPORT_PATH.write_text(
        f"# v58 report\n\nstatus: {cert['status']}\n"
        f"plancherel: PROVED\n"
        f"sqrt-cancel => T=0 deployed: PROVED conditional\n"
        f"OPEN prove sqrt-cancel: True\n"
    )
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  Plancherel coll identity: PROVED")
    print("  coll <= C^2/p^(e-1) + B^2: PROVED")
    print(
        f"  sqrt-cancel => coll <= C^2/p^(e-1) (log2~{d['log2_C2_over_pe']:.1f}) "
        "=> T=0 deployed: PROVED CONDITIONAL"
    )
    print(
        f"  CAS: e2={cen['n_e2']} e3={cen['n_e3']}; "
        f"B/sqrtC in [{cen['min_B_over_sqrtC']:.2f},{cen['max_B_over_sqrtC']:.2f}]"
    )
    print("  OPEN: prove |S(lambda)| <= sqrt(C) (or sufficient B) on GP free-1 highs")


if __name__ == "__main__":
    main()
