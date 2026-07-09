#!/usr/bin/env python3
"""KB-MCA Route-D v62: Gauss-sharp All bound |All| <= sqrt(p) t W_inf <= p t^{3/2}.

Improves v60/v61 envelope for e=3 free-1 high sums using |hatH|=sqrt(p).

Proved:
  (1) Quadratic Fourier is flat Gauss. For a != 0 in F_p (p odd),
        H(s) = psi(a s^2 + b s),
        hatH(xi) = sum_s H(s) psi(xi s)
      satisfies |hatH(xi)| = sqrt(p) for every xi (classical Gauss sum after
      completing the square).
  (2) Refined All bound (l1 != 0). With All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3
      and W_inf = max |hat_mu|,
        |All| <= p^{-1} * sqrt(p) * sum_xi |hat_mu(xi)|^3
             <= p^{-1/2} * W_inf * sum_xi |hat_mu|^2
             = p^{-1/2} * W_inf * (p t)     (Plancherel: sum |hat_mu|^2 = p t)
             = sqrt(p) * t * W_inf
             <= sqrt(p) * t * sqrt(p t)     (v61)
             = p * t^{3/2}.
  (3) Consequently
        |S| <= (1/6)( sqrt(p) t W_inf + 3t(t-1)+t )
             <= (1/6)( p t^{3/2} + 3t(t-1)+t ).
  (4) Comparison with v61 envelope p^2 t^{3/2}:
        v60/v61 used |All| <= sqrt(p) W_inf^3 <= p^2 t^{3/2};
        v62 replaces that by sqrt(p) t W_inf <= p t^{3/2}.
        Ratio of old/new ~ W_inf / t <= sqrt(p/t), large in the sparse regime.
  (5) Still too weak for sqrt-cancel: bound/sqrt(C) ~ p * sqrt(6) -> infinity.
      Even typical W_inf ~ sqrt(t) only yields |All| ~ sqrt(p) t^{3/2}, ratio ~ sqrt(p).

CAS:
  (6) |hatH(xi)| = sqrt(p) constant on all tested (p,a,b).
  (7) |All| <= sqrt(p) t W_inf on identity rows; new bound << old p^2 bound.
  (8) Empirical |S|/sqrt(C) still O(1)-O(3); new envelope still >> sqrt(C).

OPEN:
  Further cancel in sum_xi hatH(-xi) hat_mu(xi)^3 beyond |hat_mu|^3 envelope
  (need phase of hat_mu on GP arcs / higher-moment structure).

Does NOT close |T|<=H2 for e>2 unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v62.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v62"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v62.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v62.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v62.report.md"
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


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_gauss_flat() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "quadratic_Fourier_flat_Gauss",
        "statement": (
            "For a!=0, H(s)=psi(a s^2 + b s) has |hatH(xi)|=sqrt(p) for all xi."
        ),
        "proof": [
            "Complete the square: a s^2 + (b+xi)s = a(s + (b+xi)/(2a))^2 - disc/(4a).",
            "Translate s; remaining sum is the standard Gauss sum G(a) with |G(a)|=sqrt(p).",
        ],
    }


def lemma_All_refined() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_All_le_sqrtp_t_Winf",
        "statement": (
            "For l1!=0: |All| <= sqrt(p) * t * W_inf <= p * t^{3/2}."
        ),
        "proof": [
            "All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3 (v60).",
            "|hatH|=sqrt(p) => |All| <= p^{-1/2} sum |hat_mu|^3.",
            "sum |hat_mu|^3 <= W_inf sum |hat_mu|^2 = W_inf * p t.",
            "Thus |All| <= p^{-1/2} W_inf p t = sqrt(p) t W_inf.",
            "v61: W_inf <= sqrt(p t) => |All| <= p t^{3/2}.",
        ],
    }


def lemma_S_refined() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_S_refined_envelope",
        "statement": (
            "|S| <= (1/6)( sqrt(p) t W_inf + 3t(t-1)+t ) "
            "<= (1/6)( p t^{3/2} + 3t(t-1)+t )."
        ),
        "proof": ["v60 diagonal identity + refined All bound."],
    }


def lemma_still_weak() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_refined_envelope_still_weak",
        "statement": (
            "Refined envelope / sqrt(C) ~ p * sqrt(6) -> infinity; still cannot "
            "force v58 sqrt-cancel. Improvement over v61 is factor ~ sqrt(p/t)."
        ),
        "proof": [
            "sqrt(C) ~ t^{3/2}/sqrt(6); bound ~ p t^{3/2}/6 => ratio ~ p/sqrt(6).",
            "Old envelope ~ p^2 t^{3/2}/6; ratio old/new ~ p when W_inf~sqrt(pt).",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_oscillatory_hat_mu_cubed",
        "statement": (
            "Bound |sum_xi hatH(-xi) hat_mu(xi)^3| with phase cancellation "
            "(beyond sum |hat_mu|^3) for GP-arc free-1 highs; reach |S|<=sqrt(C)."
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


def hatH_mags(p: int, a: int, b: int) -> dict[str, Any]:
    s = np.arange(p)
    phase = (a * ((s * s) % p) + b * s) % p
    H = np.exp(2j * np.pi * phase / p)
    # numpy fft uses minus sign; magnitude unchanged for quadratic Gauss
    mags = np.abs(np.fft.fft(H))
    sp = math.sqrt(p)
    return {
        "p": p,
        "a": a,
        "b": b,
        "min_abs": float(np.min(mags)),
        "max_abs": float(np.max(mags)),
        "sqrt_p": float(sp),
        "flat": bool(np.max(np.abs(mags - sp)) < 1e-6),
    }


def max_W_inf(p: int, vals: list[int]) -> float:
    t = len(vals)
    m = 0.0
    for A in range(p):
        f = np.zeros(p, dtype=np.complex128)
        for x in vals:
            f[x] += np.exp(2j * np.pi * ((A * ((x * x) % p)) % p) / p)
        m = max(m, float(np.max(np.abs(np.fft.fft(f)))))
    return m


def row_All_bounds(p: int, n: int, t: int, l0: int, l1: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    inv2 = pow(2, -1, p)
    # direct All
    All = 0j
    S = 0j
    for i in range(t):
        for j in range(t):
            for k in range(t):
                h0, h1 = monic_high3(vals[i], vals[j], vals[k], p)
                All += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)
    for i, j, k in itertools.combinations(range(t), 3):
        h0, h1 = monic_high3(vals[i], vals[j], vals[k], p)
        S += np.exp(2j * np.pi * ((l0 * h0 + l1 * h1) % p) / p)

    # mu and Fourier
    g_coeff = (-inv2 * l1) % p
    mu = np.zeros(p, dtype=np.complex128)
    for x in vals:
        mu[x] += np.exp(2j * np.pi * ((g_coeff * ((x * x) % p)) % p) / p)
    hat_mu = np.fft.fft(mu)  # convention consistent with prior packets
    Winf = float(np.max(np.abs(hat_mu)))
    sum_abs3 = float(np.sum(np.abs(hat_mu) ** 3))
    sum_abs2 = float(np.sum(np.abs(hat_mu) ** 2))

    # hatH with H(s)=psi((l1/2)s^2 - l0 s)
    a = (inv2 * l1) % p
    b = (-l0) % p
    s = np.arange(p)
    H = np.exp(2j * np.pi * ((a * ((s * s) % p) + b * s) % p) / p)
    hatH = np.fft.fft(H)
    # All via Fourier: careful with numpy sign. Use reconstruction check.
    # Direct: All = sum_s H(s) (mu*mu*mu)(s)
    conv3 = np.fft.ifft(hat_mu**3)
    All_conv = float(np.abs(np.sum(H * conv3)))
    # note: ifft normalizes; mu via fft means ifft(fft(mu)^3) = mu*mu*mu * p^2 / p? 
    # circular: fft(mu*mu*mu) = fft(mu)^3 / ? 
    # numpy: fft(ifft(a)*n) etc. Safer use already-proved v60 path via abs bounds only.

    bound_new = math.sqrt(p) * t * Winf
    bound_old = math.sqrt(p) * (Winf**3)
    bound_pt32 = p * (t**1.5)
    # analytic refined from sum |muhat|^3
    bound_from_L3 = (1 / math.sqrt(p)) * sum_abs3
    # plancherel check
    plancherel_ok = abs(sum_abs2 - p * t) / (p * t) < 1e-8

    C = math.comb(t, 3)
    return {
        "p": p,
        "t": t,
        "l0": l0,
        "l1": l1,
        "abs_All": float(abs(All)),
        "abs_S": float(abs(S)),
        "Winf": float(Winf),
        "sum_hatmu2": float(sum_abs2),
        "p_t": float(p * t),
        "plancherel_ok": bool(plancherel_ok),
        "bound_new": float(bound_new),
        "bound_old": float(bound_old),
        "bound_pt32": float(bound_pt32),
        "bound_from_L3": float(bound_from_L3),
        "All_le_new": bool(abs(All) <= bound_new + 1e-4),
        "All_le_old": bool(abs(All) <= bound_old + 1e-4),
        "All_le_L3": bool(abs(All) <= bound_from_L3 + 1e-4),
        "new_over_old": float(bound_new / bound_old) if bound_old > 0 else None,
        "S_bound_new": float((1 / 6) * (bound_new + 3 * t * (t - 1) + t)),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(abs(S) / math.sqrt(C)),
        "new_bound_over_sqrtC": float(
            ((1 / 6) * (bound_new + 3 * t * (t - 1) + t)) / math.sqrt(C)
        ),
        "All_conv_abs": float(All_conv),
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
    Winf = max_W_inf(p, vals[:t])
    bound_S = (1 / 6) * (math.sqrt(p) * t * Winf + 3 * t * (t - 1) + t)
    bound_pt = (1 / 6) * (p * (t**1.5) + 3 * t * (t - 1) + t)
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "maxS": float(maxS),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
        "Winf": float(Winf),
        "bound_S_new": float(bound_S),
        "bound_S_pt32": float(bound_pt),
        "maxS_le_new": bool(maxS <= bound_S + 1e-6),
        "new_over_sqrtC": float(bound_S / math.sqrt(C)),
        "forces_sqrt_cancel": bool(bound_S <= math.sqrt(C) + 1e-9),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char!=2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    gauss_rows = []
    for p in [61, 101, 127]:
        for a, b in [(1, 0), (3, 5), (7, 11), (17, 23)]:
            r = hatH_mags(p, a % p, b % p)
            ensure(r["flat"], f"gauss flat {p},{a}")
            gauss_rows.append(r)
    ensure(len(gauss_rows) >= 12, "gauss rows")

    id_rows = []
    for p, n, t in [(61, 60, 12), (61, 60, 15), (101, 100, 12), (101, 100, 15)]:
        for l0, l1 in [(1, 1), (3, 5), (2, 7)]:
            r = row_All_bounds(p, n, t, l0, l1)
            ensure(r["plancherel_ok"], "plancherel mu")
            ensure(r["All_le_new"], "All<=new")
            ensure(r["All_le_L3"], "All<=L3")
            ensure(r["new_over_old"] is not None and r["new_over_old"] < 1.0 + 1e-9, "new tighter")
            id_rows.append(r)
    ensure(len(id_rows) >= 8, "id rows")

    max_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for t in [15, 24, 36]:
            if t > n or math.comb(t, 3) > 20000:
                continue
            r = maxS_e3(p, n, t)
            ensure(r["maxS_le_new"], "maxS new bound")
            ensure(not r["forces_sqrt_cancel"], "still weak")
            max_rows.append(r)
    ensure(len(max_rows) >= 6, "max rows")
    ensure(max(r["S_over_sqrtC"] for r in max_rows) < 5, "emp")

    return {
        "status": "PASS",
        "gauss_rows": gauss_rows,
        "id_rows": id_rows,
        "max_rows": max_rows,
        "census": {
            "n_gauss": len(gauss_rows),
            "n_id": len(id_rows),
            "n_max": len(max_rows),
            "all_hatH_flat": True,
            "all_All_le_new": True,
            "envelope_still_weak": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in max_rows),
            "max_new_over_sqrtC": max(r["new_over_sqrtC"] for r in max_rows),
            "max_new_over_old": max(r["new_over_old"] for r in id_rows),
            "min_new_over_old": min(r["new_over_old"] for r in id_rows),
            "deployed_asymp_p_over_sqrt6": float(P / math.sqrt(6)),
            "log10_deployed_asymp": float(math.log10(P / math.sqrt(6))),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "note": (
                "All <= sqrt(p) t W_inf <= p t^{3/2}; still ~p short of sqrt-cancel"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v62",
        "title": "Gauss-sharp All bound: |All|<=sqrt(p) t W_inf <= p t^{3/2}",
        "status": "ALL_REFINED_STILL_WEAK_OSCILLATORY_OPEN",
        "claims": {
            "proves_hatH_flat_Gauss": True,
            "proves_All_le_sqrtp_t_Winf": True,
            "proves_All_le_p_t32": True,
            "proves_refined_still_weak_for_sqrt_cancel": True,
            "proves_S_le_sqrtC": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "gauss_flat": lemma_gauss_flat(),
            "All_refined": lemma_All_refined(),
            "S_refined": lemma_S_refined(),
            "still_weak": lemma_still_weak(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "Gauss flat + All bounds", "python_nt": "GP domain"},
        "impact_on_program": {
            "closed": (
                "e=3 All envelope improved p^2 t^{3/2} -> p t^{3/2} "
                "(Gauss |hatH|=sqrt(p) + L1-Linf on hat_mu)"
            ),
            "wall": "still need oscillatory cancel in sum hatH hat_mu^3",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    id_lines = []
    for r in cert["toy_suite"]["id_rows"][:8]:
        id_lines.append(
            f"| {r['p']} | {r['t']} | {r['l0']},{r['l1']} | {r['abs_All']:.1f} | "
            f"{r['bound_new']:.1e} | {r['bound_old']:.1e} | {r['new_over_old']:.3f} |"
        )
    id_tbl = "\n".join(id_lines)
    max_lines = []
    for r in cert["toy_suite"]["max_rows"]:
        max_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['bound_S_new']:.1e} | "
            f"{r['sqrtC']:.1f} | {r['S_over_sqrtC']:.2f} | {r['new_over_sqrtC']:.1e} |"
        )
    max_tbl = "\n".join(max_lines)
    return f"""# KB-MCA Route-D v62: Gauss-sharp All bound

Status: **refined All envelope PROVED** (`|All| <= sqrt(p) t W_inf <= p t^{{3/2}}`);
still **too weak** for √-cancel. Local on `scott/kb-route-d-T-bound`.

## Gauss flatness (PROVED)

```text
H(s) = psi(a s^2 + b s),  a != 0
|hatH(xi)| = sqrt(p)  for all xi
```

## Refined All (PROVED)

```text
All = p^{{-1}} sum_xi hatH(-xi) hat_mu(xi)^3
|All| <= p^{{-1/2}} sum |hat_mu|^3
      <= p^{{-1/2}} W_inf * (p t)
      = sqrt(p) * t * W_inf
      <= p * t^{{3/2}}          (v61 W_inf <= sqrt(p t))
```

v60/v61 used `|All| <= sqrt(p) W_inf^3 <= p^2 t^{{3/2}}`.  
Sparse improvement factor `~ sqrt(p/t)`.

## S envelope (PROVED, still weak)

```text
|S| <= (1/6)( sqrt(p) t W_inf + O(t^2) ) <= (1/6)( p t^{{3/2}} + O(t^2) )
bound / sqrt(C) ~ p / sqrt(6)  -> infinity
```

## CAS

### |All| vs bounds (sample)

| p | t | (l0,l1) | |All| | new | old (v60) | new/old |
|---|---:|---|---:|---:|---:|---:|
{id_tbl}

### max|S|

| p | t | max|S| | new bound | √C | S/√C | new/√C |
|---|---:|---:|---:|---:|---:|---:|
{max_tbl}

- |hatH| flat on all {cen['n_gauss']} Gauss rows.
- new/old ratio in [{cen['min_new_over_old']:.3f}, {cen['max_new_over_old']:.3f}] on id rows (always < 1).
- Empirical S/√C max = {cen['max_S_over_sqrtC']:.2f}.
- new/√C max on toys = {cen['max_new_over_sqrtC']:.1e}.
- Deployed asymptotic `p/sqrt(6)` ≈ 10^{cen['log10_deployed_asymp']:.1f}.

## Link

v58 needs `|S|<=√C`.  
v61 killed pure `W_inf^3` path at `p^2`.  
v62 improves to `p` but **still short**.  
Next must use **phase** of `hat_mu` on the GP arc.

Deployed e={d['e']} ≫ 3 after e=3 is sharp.

## OPEN

1. Oscillatory `sum_xi hatH(-xi) hat_mu(xi)^3` for GP free-1 highs.  
2. `|S|<=√C` then general e; or alternate `|R2|<=e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v62.py --check
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
        "# kb-qatom-route-d-v62\n\n"
        "Gauss-sharp All bound |All|<=sqrt(p) t W_inf <= p t^{3/2}.\n"
    )
    REPORT_PATH.write_text(
        f"# v62 report\n\nstatus: {cert['status']}\n"
        f"hatH flat Gauss: PROVED\n"
        f"All <= sqrt(p) t W_inf <= p t^{{3/2}}: PROVED\n"
        f"still weak for sqrt-cancel: PROVED\n"
        f"OPEN oscillatory hat_mu^3: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  |hatH|=sqrt(p) flat Gauss: PROVED")
    print("  |All| <= sqrt(p) t W_inf <= p t^{3/2}: PROVED")
    print("  refined envelope still weak for sqrt-cancel: PROVED")
    print(
        f"  CAS: gauss={cen['n_gauss']}; id={cen['n_id']}; "
        f"S/sqrtC max={cen['max_S_over_sqrtC']:.2f}; "
        f"new/sqrtC max={cen['max_new_over_sqrtC']:.1e}; "
        f"new/old in [{cen['min_new_over_old']:.3f},{cen['max_new_over_old']:.3f}]"
    )
    print("  OPEN: oscillatory sum hatH hat_mu^3")


if __name__ == "__main__":
    main()
