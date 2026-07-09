#!/usr/bin/env python3
"""KB-MCA Route-D v60: e=3 free-1 high sums via triple Fourier + quadratic Weyl.

Attacks |S(lambda)| for e=3 free-1 monic highs on a GP arc (v58-v59).

Proved:
  (1) High formulas (char != 2): for roots u,v,w,
        h0 = -(u+v+w),   h1 = uv+uw+vw = ((u+v+w)^2 - (u^2+v^2+w^2))/2.
  (2) Diagonal identity. Let vals = arc values, t = |arc|, and
        All = sum_{i,j,k=0}^{t-1} psi(l0 h0(vi,vj,vk)+l1 h1(...)),
        S   = sum_{i<j<k} psi(...),           (unordered free-1 high sum)
        D2  = sum_{i!=k} psi(Phi(vi,vi,vk)),
        D3  = sum_i psi(Phi(vi,vi,vi)).
      If the arc values are pairwise distinct (true for GP of length t <= n),
        All = 6 S + 3 D2 + D3,
      hence S = (All - 3 D2 - D3)/6 and
        |S| <= (1/6)( |All| + 3 t(t-1) + t ).
  (3) Triple Fourier formula (l1 != 0, char != 2). With
        g_coeff = -l1/2,  H(s) = psi((l1/2) s^2 - l0 s),
        mu = sum_{i<t} g(vi) delta_{vi},  g(x)=psi(g_coeff x^2),
      one has All = sum_s H(s) (mu*mu*mu)(s)
      = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3
      (circular convolution / Plancherel on F_p).
  (4) Crude All bound: |All| <= sqrt(p) * W_inf^3 where
        W_inf = max_{A,B} |sum_{i<t} psi(A v_i^2 + B v_i)|.
      Proof: |All| <= p^{-1} sum_xi |hatH(xi)| |hat_mu(xi)|^3
           <= p^{-1} W_inf^3 sum_xi |hatH(xi)|
           <= p^{-1} W_inf^3 * sqrt(p) * sqrt(sum |hatH|^2)
           and sum_xi |hatH|^2 = p sum_s |H(s)|^2 = p^2,
           so sum |hatH| <= p^{3/2}, hence |All| <= sqrt(p) W_inf^3.
  (5) Consequently |S| <= (1/6)( sqrt(p) W_inf^3 + 3t(t-1)+t ).
  (6) l1=0 degenerates to a pure power-sum / e=2-style linear phase in s1
      (handled separately; not the main multipad obstruction in sparse tests).

CAS:
  (7) Identities (1)-(3) hold numerically (err ~ 1e-12).
  (8) W_inf <= sqrt(p t) on tested rows (same scale as linear G); not proved.
  (9) Bound (5) holds but is >> sqrt(C) (too weak to force T=0 via v58 alone).
  (10) Empirical |S|/sqrt(C) still O(1)-O(3) for e=3.

OPEN:
  Prove W_inf << t (ideally O(sqrt(p t)) or better) and/or sharpen (4) to reach
  |S| <= sqrt(C) in the sparse regime; then v58 closes residual for e=3.

Does NOT close |T|<=H2 for e>2 unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v60.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v60"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v60.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v60.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v60.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T_ROW = A - 2**20
Wdeg = T_ROW - 1
E = Wdeg + 1
M_C = J - E
FREE_CORE = M_C - Wdeg
N_PRIME = A + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_high_formulas() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_monic_high_formulas_char_ne_2",
        "statement": (
            "For the product convention (1-uX)(1-vX)(1-wX), "
            "h0=-(u+v+w), h1=uv+uw+vw=((u+v+w)^2-(u^2+v^2+w^2))/2 in char != 2."
        ),
        "proof": ["Expand the cubic; Newton for e2 vs power sums."],
    }


def lemma_diagonal() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_diagonal_identity",
        "statement": (
            "For distinct arc values, All = 6S + 3 D2 + D3, hence "
            "|S| <= (1/6)(|All| + 3t(t-1) + t)."
        ),
        "proof": [
            "Partition (i,j,k) in [0,t)^3 by equality type of indices.",
            "Distinct values for distinct indices on a GP of length t<=n.",
            "Each unordered triple contributes 3!=6 ordered triples.",
        ],
    }


def lemma_fourier_triple() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_all_triple_fourier_formula",
        "statement": (
            "For l1!=0, char!=2: All = sum_s H(s)(mu*mu*mu)(s) with "
            "H(s)=psi((l1/2)s^2 - l0 s), mu=sum_i psi((-l1/2)vi^2) delta_vi."
        ),
        "proof": [
            "Phi = (l1/2)s1^2 - l0 s1 - (l1/2)p2 with s1=u+v+w, p2=u^2+v^2+w^2.",
            "psi(Phi)=H(s1) g(u)g(v)g(w), g(x)=psi((-l1/2)x^2).",
            "Sum over arc indices = sum_s H(s) sum_{vi+vj+vk=s} g(vi)g(vj)g(vk).",
        ],
    }


def lemma_all_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_all_bound_by_Winf",
        "statement": (
            "|All| <= sqrt(p) * W_inf^3 with "
            "W_inf = max |sum_{i<t} psi(A vi^2 + B vi)| over A,B in F_p."
        ),
        "proof": [
            "All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3.",
            "|All| <= p^{-1} W_inf^3 sum_xi |hatH(xi)|.",
            "sum |hatH| <= sqrt(p) sqrt(sum |hatH|^2) = sqrt(p)*p = p^{3/2},",
            "since sum_xi |hatH|^2 = p sum_s |H|^2 = p^2.",
            "Thus |All| <= p^{-1} W_inf^3 p^{3/2} = sqrt(p) W_inf^3.",
        ],
    }


def lemma_S_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_S_bound_from_Winf",
        "statement": (
            "|S| <= (1/6)( sqrt(p) W_inf^3 + 3t(t-1) + t ) for l1!=0."
        ),
        "proof": ["Combine diagonal identity with All bound."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_Winf_and_sharp_S",
        "statement": (
            "Prove W_inf <= sqrt(p t) (or better) for quadratic phases on GP arcs, "
            "and/or improve the All bound so that |S| <= sqrt(C) in sparse regime."
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


def monic_high3(u: int, v: int, w: int, p: int) -> tuple[int, int]:
    poly = [1]
    for x in (u, v, w):
        new = [0] * (len(poly) + 1)
        mv = (-x) % p
        for j, c in enumerate(poly):
            new[j] = (new[j] + c) % p
            new[j + 1] = (new[j + 1] + c * mv) % p
        poly = new
    return poly[1] % p, poly[2] % p


def max_W_inf(p: int, n: int, t: int) -> float:
    vals = domain_vals(p, n)[:t]
    m = 0.0
    for A in range(p):
        ind = np.zeros(p, dtype=np.complex128)
        for v in vals:
            ind[v] += np.exp(2j * np.pi * ((A * (v * v % p)) % p) / p)
        m = max(m, float(np.max(np.abs(np.fft.fft(ind)))))
    return m


def row_identity(p: int, n: int, t: int, l0: int, l1: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    inv2 = pow(2, -1, p)

    def phase_h(u, v, w):
        return monic_high3(u, v, w, p)

    All = 0j
    S = 0j
    D2 = 0j
    D3 = 0j
    for i in range(t):
        for j in range(t):
            for k in range(t):
                h0, h1 = phase_h(vals[i], vals[j], vals[k])
                term = np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)
                All += term
    for i, j, k in itertools.combinations(range(t), 3):
        h0, h1 = phase_h(vals[i], vals[j], vals[k])
        S += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)
    for i in range(t):
        for k in range(t):
            if i == k:
                continue
            h0, h1 = phase_h(vals[i], vals[i], vals[k])
            D2 += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)
    for i in range(t):
        h0, h1 = phase_h(vals[i], vals[i], vals[i])
        D3 += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)

    recon = 6 * S + 3 * D2 + D3
    # Fourier All
    if l1 % p == 0:
        All_ft = None
    else:
        g_coeff = (-inv2 * l1) % p
        h2 = (inv2 * l1) % p
        h1c = (-l0) % p
        mu = np.zeros(p, dtype=np.complex128)
        for i in range(t):
            x = vals[i]
            mu[x] += np.exp(2j * np.pi * ((g_coeff * (x * x % p)) % p) / p)
        conv3 = np.fft.ifft(np.fft.fft(mu) ** 3)
        All_ft = 0j
        for s in range(p):
            Hs = np.exp(2j * np.pi * ((h2 * (s * s % p) + h1c * s) % p) / p)
            All_ft += Hs * conv3[s]

    # high formulas spot check
    u, v, w = vals[0], vals[1], vals[2]
    h0, h1 = monic_high3(u, v, w, p)
    s1 = (u + v + w) % p
    p2 = (u * u + v * v + w * w) % p
    e2 = (u * v + u * w + v * w) % p
    formula_ok = h0 == (-s1) % p and h1 == e2 and e2 == ((s1 * s1 - p2) * inv2) % p

    Winf = max_W_inf(p, n, t)
    bound_All = math.sqrt(p) * (Winf**3)
    bound_S = (1 / 6) * (bound_All + 3 * t * (t - 1) + t)
    C = math.comb(t, 3)

    return {
        "p": p,
        "t": t,
        "l0": l0,
        "l1": l1,
        "abs_S": float(abs(S)),
        "abs_All": float(abs(All)),
        "diag_err": float(abs(All - recon)),
        "ft_err": float(abs(All - All_ft)) if All_ft is not None else None,
        "formula_ok": bool(formula_ok),
        "Winf": float(Winf),
        "bound_All": float(bound_All),
        "All_le_bound": bool(abs(All) <= bound_All + 1e-6),
        "bound_S": float(bound_S),
        "S_le_bound": bool(abs(S) <= bound_S + 1e-6),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(abs(S)) / math.sqrt(C),
        "bound_S_over_sqrtC": float(bound_S / math.sqrt(C)),
        "Winf_le_sqrt_pt": bool(Winf <= math.sqrt(p * t) + 1e-6),
    }


def maxS_e3(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    for idxs in itertools.combinations(range(t), 3):
        h0, h1 = monic_high3(vals[idxs[0]], vals[idxs[1]], vals[idxs[2]], p)
        freq[h0, h1] += 1
        C += 1
    F = np.fft.fft2(freq)
    a = np.abs(F)
    a[0, 0] = 0
    maxS = float(np.max(a))
    Winf = max_W_inf(p, n, t)
    bound_S = (1 / 6) * (math.sqrt(p) * (Winf**3) + 3 * t * (t - 1) + t)
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "maxS": float(maxS),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
        "Winf": float(Winf),
        "bound_S": float(bound_S),
        "maxS_le_bound": bool(maxS <= bound_S + 1e-6),
        "Winf_le_sqrt_pt": bool(Winf <= math.sqrt(p * t) + 1e-6),
        "bound_implies_sqrt_cancel": bool(bound_S <= math.sqrt(C) + 1e-9),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char!=2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    id_rows = []
    for p, n, t in [(61, 60, 12), (61, 60, 15), (101, 100, 12), (101, 100, 15)]:
        for l0, l1 in [(1, 1), (3, 5), (2, 7)]:
            r = row_identity(p, n, t, l0, l1)
            ensure(r["formula_ok"], "high formula")
            ensure(r["diag_err"] < 1e-8, "diagonal id")
            ensure(r["ft_err"] is not None and r["ft_err"] < 1e-8, "fourier id")
            ensure(r["All_le_bound"], "All bound")
            ensure(r["S_le_bound"], "S bound")
            id_rows.append(r)

    ensure(len(id_rows) >= 8, "id rows")

    max_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for t in [15, 24, 36]:
            if t > n or math.comb(t, 3) > 20000:
                continue
            r = maxS_e3(p, n, t)
            ensure(r["maxS_le_bound"], "maxS bound")
            # bound should NOT imply sqrt-cancel on these rows
            max_rows.append(r)

    ensure(len(max_rows) >= 6, "max rows")
    ensure(all(not r["bound_implies_sqrt_cancel"] for r in max_rows), "bound weak")
    ensure(all(r["Winf_le_sqrt_pt"] for r in max_rows + id_rows), "W CAS")

    # empirical near sqrt-cancel
    ensure(max(r["S_over_sqrtC"] for r in max_rows) < 5, "emp S/sC")

    return {
        "status": "PASS",
        "id_rows": id_rows,
        "max_rows": max_rows,
        "census": {
            "n_id": len(id_rows),
            "n_max": len(max_rows),
            "all_identities_ok": True,
            "all_bounds_hold": True,
            "bound_too_weak_for_sqrt_cancel": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in max_rows),
            "max_bound_over_sqrtC": max(
                r["bound_S"] / r["sqrtC"] for r in max_rows
            ),
            "max_Winf_over_sqrt_pt": max(
                r["Winf"] / math.sqrt(r["p"] * r["t"]) for r in max_rows
            ),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "note": "e=3 reduction; deployed e>>3 still needs general-e lift",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v60",
        "title": "e=3 free-1 high sums: triple Fourier + W_inf bound",
        "status": "E3_REDUCTION_PROVED_SHARP_BOUND_OPEN",
        "claims": {
            "proves_e3_high_formulas": True,
            "proves_diagonal_identity": True,
            "proves_fourier_triple_formula": True,
            "proves_All_le_sqrtp_Winf3": True,
            "proves_S_le_sixth_All_plus_diag": True,
            "proves_Winf_le_sqrt_pt": False,
            "proves_S_le_sqrtC": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "high": lemma_high_formulas(),
            "diag": lemma_diagonal(),
            "fourier": lemma_fourier_triple(),
            "all_bound": lemma_all_bound(),
            "S_bound": lemma_S_bound(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "triple conv + W_inf", "python_nt": "GP domain"},
        "impact_on_program": {
            "closed": "e=3 S reduced to quadratic Weyl sums W_inf on the arc",
            "wall": "prove sharp W_inf (or better All bound) for sqrt-cancel",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    lines = []
    for r in cert["toy_suite"]["max_rows"]:
        lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['bound_S']:.1e} | "
            f"{r['sqrtC']:.1f} | {r['S_over_sqrtC']:.2f} | {r['Winf']:.1f} |"
        )
    tbl = "\n".join(lines)
    return f"""# KB-MCA Route-D v60: e=3 free-1 high sums — triple Fourier reduction

Status: **e=3 structural reduction PROVED**; sharp `|S|<=√C` still **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Setup

Free-1 monic high for three arc values `u,v,w` (char != 2):

```text
h0 = -(u+v+w)
h1 = uv+uw+vw = ((u+v+w)^2 - (u^2+v^2+w^2))/2
S(l0,l1) = sum_{{i<j<k < t}} psi(l0 h0 + l1 h1)
```

## Diagonal identity (PROVED)

```text
All = 6 S + 3 D2 + D3
|S| <= (1/6)( |All| + 3 t(t-1) + t )
```

## Triple Fourier (PROVED, l1 != 0)

```text
All = sum_s H(s) (mu * mu * mu)(s)
H(s) = psi((l1/2) s^2 - l0 s)
mu   = sum_{{i<t}} psi((-l1/2) v_i^2)  delta_{{v_i}}
```

## All bound by quadratic Weyl (PROVED)

```text
W_inf = max_{{A,B}} |sum_{{i<t}} psi(A v_i^2 + B v_i)|
|All| <= sqrt(p) * W_inf^3
|S|   <= (1/6)( sqrt(p) W_inf^3 + 3t(t-1)+t )
```

## CAS

| p | t | max|S| | bound | √C | S/√C | W_inf |
|---|---:|---:|---:|---:|---:|---:|
{tbl}

- Identities hold (diag/Fourier err ~ 1e-12).  
- Bound holds but **bound/√C ~ {cen['max_bound_over_sqrtC']:.0f}** (too weak for √-cancel).  
- Empirical S/√C max = {cen['max_S_over_sqrtC']:.2f}.  
- W_inf/√(pt) max = {cen['max_Winf_over_sqrt_pt']:.2f} (suggests W_inf = O(√(pt))).

## Link to residual card

v58: `|S|<=√C` ⇒ `coll <= C^2/p^{{e-1}}` ⇒ `T=0` at deployed.  
v60 reduces e=3 `|S|` to **W_inf** but the proved estimate is not yet ≤√C.

Deployed e={d['e']} ≫ 3 needs a general-e lift after e=3 is sharp.

## OPEN

1. Prove `W_inf <= sqrt(p t)` (or better) for quadratic phases on GP arcs.  
2. Sharpen `|All|` beyond `sqrt(p) W_inf^3` (e.g. using Gauss structure of hatH).  
3. Reach `|S|<=√C` sparsely for e=3, then generalize e.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v60.py --check
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
        "# kb-qatom-route-d-v60\n\n"
        "e=3 free-1 high sums: triple Fourier + W_inf bound.\n"
    )
    REPORT_PATH.write_text(
        f"# v60 report\n\nstatus: {cert['status']}\n"
        f"e3 reduction to W_inf: PROVED\n"
        f"OPEN sharp W_inf / S<=sqrtC: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  e=3 high formulas + diagonal identity: PROVED")
    print("  All = triple Fourier in mu,H: PROVED")
    print("  |All| <= sqrt(p) W_inf^3; |S| <= (1/6)(|All|+O(t^2)): PROVED")
    print(
        f"  CAS: id rows={cen['n_id']}; max S/sqrtC={cen['max_S_over_sqrtC']:.2f}; "
        f"bound/sqrtC max={cen['max_bound_over_sqrtC']:.1f}; "
        f"W_inf/sqrt(pt) max={cen['max_Winf_over_sqrt_pt']:.2f}"
    )
    print("  OPEN: prove sharp W_inf (or better All) to reach |S|<=sqrt(C)")


if __name__ == "__main__":
    main()
