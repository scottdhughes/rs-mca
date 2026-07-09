#!/usr/bin/env python3
"""KB-MCA Route-D v61: prove W_inf <= sqrt(p t); e=3 envelope still too weak.

Closes OPEN item (1) from v60: quadratic Weyl sums on any arc.

Proved:
  (1) Per-A Plancherel for quadratic phases. Fix A in F_p and any t-element
      set S_arc subset F_p (pairwise distinct values). Define
        W(A,B) = sum_{x in S_arc} psi(A x^2 + B x),
        f_A(x) = 1_{S_arc}(x) * psi(A x^2).
      Then W(A,B) = sum_x f_A(x) psi(B x)  (Fourier of f_A), and
        sum_B |W(A,B)|^2 = p sum_x |f_A(x)|^2 = p t,
      since |psi| = 1 on the support of size t.
  (2) Consequently, for every A,
        max_B |W(A,B)| <= sqrt(sum_B |W(A,B)|^2) = sqrt(p t).
      Therefore
        W_inf := max_{A,B} |W(A,B)| <= sqrt(p t).
      (No GP structure used: any t-set works.)
  (3) Plug into v60 All bound: |All| <= sqrt(p) W_inf^3 <= sqrt(p) (p t)^{3/2}
        = p^2 t^{3/2}.
      Hence for l1 != 0,
        |S| <= (1/6)( p^2 t^{3/2} + 3 t(t-1) + t ).
  (4) This envelope CANNOT force |S| <= sqrt(C) for large p: with C = binom(t,3),
        sqrt(C) ~ t^{3/2}/sqrt(6), so bound/sqrt(C) ~ p^2 / sqrt(6) -> infinity.
      Absolute-value estimates on the triple Fourier sum are therefore
      insufficient for the v58 sqrt-cancel close on e=3.

CAS:
  (5) sum_B |W(A,B)|^2 = p t for every tested (p,t,A) (err ~ 1e-8 relative).
  (6) W_inf <= sqrt(p t) on all rows; ratio max ~ 0.8 as in v60.
  (7) Envelope bound holds and bound/sqrt(C) >> 1 (scales like p^2).
  (8) Empirical max|S|/sqrt(C) still O(1)-O(3).

OPEN:
  Force |S| <= sqrt(C) by oscillatory cancellation in
    All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3
  (phase structure of hat_mu on GP arcs), not by envelope |hatH| |hat_mu|^3.
  Gauss flatness of |hatH| makes Cauchy-Schwarz on sum |hatH| essentially
  sharp, so the bottleneck is hat_mu, not hatH.

Does NOT close |T|<=H2 for e>2 unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v61.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v61"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v61.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v61.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v61.report.md"
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


def lemma_W_plancherel() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "W_per_A_Plancherel",
        "statement": (
            "For any t-set S_arc subset F_p and any A: "
            "sum_B |W(A,B)|^2 = p t, where "
            "W(A,B)=sum_{x in S_arc} psi(A x^2 + B x)."
        ),
        "proof": [
            "f_A(x) = 1_{S_arc}(x) psi(A x^2); |f_A(x)|=1_S(x).",
            "W(A,B) = sum_x f_A(x) psi(B x) = hat f_A at frequency B (sign convention).",
            "Plancherel on F_p: sum_B |hat f|^2 = p sum_x |f|^2 = p t.",
        ],
    }


def lemma_Winf() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Winf_le_sqrt_pt",
        "statement": (
            "W_inf = max_{A,B} |W(A,B)| <= sqrt(p t) for any t-set S_arc."
        ),
        "proof": [
            "For each A: max_B |W(A,B)| <= sqrt(sum_B |W|^2) = sqrt(p t).",
            "Take max over A.",
        ],
    }


def lemma_S_envelope() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_S_envelope_from_Winf_plancherel",
        "statement": (
            "For l1!=0, |S| <= (1/6)( p^2 t^{3/2} + 3t(t-1)+t )."
        ),
        "proof": [
            "v60: |All| <= sqrt(p) W_inf^3 and |S| <= (1/6)(|All|+3t(t-1)+t).",
            "W_inf <= sqrt(p t) => |All| <= sqrt(p) (p t)^{3/2} = p^2 t^{3/2}.",
        ],
    }


def lemma_envelope_too_weak() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_envelope_cannot_force_sqrt_cancel",
        "statement": (
            "The absolute envelope (1/6)(p^2 t^{3/2}+O(t^2)) exceeds sqrt(binom(t,3)) "
            "by a factor ~ p^2/sqrt(6) as p->infty (fixed density or sparse t). "
            "Hence envelope bounds alone cannot yield v58 sqrt-cancel for e=3."
        ),
        "proof": [
            "sqrt(C) = sqrt(t(t-1)(t-2)/6) ~ t^{3/2}/sqrt(6).",
            "bound / sqrt(C) ~ p^2 / sqrt(6) -> infinity for any t>=3 as p grows.",
            "Even the optimistic W_inf ~ sqrt(t) (typical L2 size) only improves "
            "to |All| <= sqrt(p) t^{3/2}, still ratio ~ sqrt(p) -> infinity.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_oscillatory_triple_Fourier",
        "statement": (
            "Prove |S| <= sqrt(C) for free-1 e=3 highs on GP arcs via cancellation "
            "in All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3, not envelope estimates. "
            "Then lift to general e and close |T|<=H2."
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


def W_row_plancherel(p: int, vals: list[int], A: int) -> dict[str, Any]:
    """For fixed A: compute all W(A,B) via FFT of f_A; check Plancherel."""
    t = len(vals)
    f = np.zeros(p, dtype=np.complex128)
    for x in vals:
        phase = (A * ((x * x) % p)) % p
        f[x] += np.exp(2j * np.pi * phase / p)
    # W(A,B) = sum_x f(x) exp(2 pi i B x / p) = FFT(f)[B]
    W = np.fft.fft(f)
    sum_sq = float(np.sum(np.abs(W) ** 2))
    target = float(p * t)
    max_abs = float(np.max(np.abs(W)))
    return {
        "A": int(A),
        "t": int(t),
        "sum_B_W2": sum_sq,
        "p_t": target,
        "rel_err": abs(sum_sq - target) / target,
        "max_B_W": max_abs,
        "sqrt_pt": math.sqrt(p * t),
        "max_le_sqrt_pt": bool(max_abs <= math.sqrt(p * t) + 1e-6),
    }


def W_inf_and_plancherel(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    rows = []
    # sample A: all for small p, otherwise a covering sample
    if p <= 127:
        A_list = list(range(p))
    else:
        A_list = list(range(0, p, max(1, p // 32)))[:40]
        if 1 not in A_list:
            A_list.append(1)
        if 0 not in A_list:
            A_list.append(0)
    for A in A_list:
        rows.append(W_row_plancherel(p, vals, A))
    Winf = max(r["max_B_W"] for r in rows)
    # full W_inf needs max over all A; for small p we have all A
    full = p <= 127
    return {
        "p": p,
        "t": t,
        "n_A": len(rows),
        "full_A_scan": full,
        "max_plancherel_rel_err": max(r["rel_err"] for r in rows),
        "all_plancherel_ok": bool(all(r["rel_err"] < 1e-8 for r in rows)),
        "all_max_le_sqrt_pt": bool(all(r["max_le_sqrt_pt"] for r in rows)),
        "Winf_sample": float(Winf),
        "sqrt_pt": float(math.sqrt(p * t)),
        "Winf_over_sqrt_pt": float(Winf / math.sqrt(p * t)),
        "Winf_le_sqrt_pt": bool(Winf <= math.sqrt(p * t) + 1e-6),
    }


def envelope_row(p: int, t: int) -> dict[str, Any]:
    C = math.comb(t, 3)
    bound_All = (p**2) * (t**1.5)
    bound_S = (1 / 6) * (bound_All + 3 * t * (t - 1) + t)
    sqrtC = math.sqrt(C)
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "sqrtC": float(sqrtC),
        "bound_S_envelope": float(bound_S),
        "bound_over_sqrtC": float(bound_S / sqrtC),
        "envelope_forces_sqrt_cancel": bool(bound_S <= sqrtC + 1e-9),
        "asymp_p2_over_sqrt6": float((p**2) / math.sqrt(6)),
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
    env = envelope_row(p, t)
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "maxS": float(maxS),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
        "bound_S_envelope": env["bound_S_envelope"],
        "bound_over_sqrtC": env["bound_over_sqrtC"],
        "maxS_le_envelope": bool(maxS <= env["bound_S_envelope"] + 1e-6),
        "envelope_forces_sqrt_cancel": env["envelope_forces_sqrt_cancel"],
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char!=2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    plan_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 24),
        (61, 60, 36),
        (101, 100, 15),
        (101, 100, 36),
        (127, 126, 15),
        (127, 126, 36),
    ]:
        r = W_inf_and_plancherel(p, n, t)
        ensure(r["all_plancherel_ok"], f"plancherel {p},{t}")
        ensure(r["all_max_le_sqrt_pt"], f"max<=sqrt(pt) {p},{t}")
        ensure(r["Winf_le_sqrt_pt"], f"Winf {p},{t}")
        plan_rows.append(r)

    ensure(len(plan_rows) >= 6, "plan rows")

    env_rows = []
    for p, t in [(61, 15), (61, 36), (101, 24), (127, 36), (P, N_PRIME)]:
        r = envelope_row(p, t if t < 10**6 else 1000)
        # for deployed use symbolic t=1000 stand-in only for asymptotics table;
        # real deployed t = n' is huge but ratio is p^2-driven
        ensure(not r["envelope_forces_sqrt_cancel"], f"env weak {p},{t}")
        env_rows.append(r)

    # asymptotic lemma check on toys
    for r in env_rows:
        if r["p"] < 10**6:
            ensure(r["bound_over_sqrtC"] > 10, "env >> sqrtC")

    max_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for t in [15, 24, 36]:
            if t > n or math.comb(t, 3) > 20000:
                continue
            r = maxS_e3(p, n, t)
            ensure(r["maxS_le_envelope"], "maxS envelope")
            ensure(not r["envelope_forces_sqrt_cancel"], "not cancel")
            max_rows.append(r)

    ensure(len(max_rows) >= 6, "max rows")
    ensure(max(r["S_over_sqrtC"] for r in max_rows) < 5, "emp S/sC")

    # deployed ratio of envelope vs sqrt(C) at t = n' is meaningless to compute
    # fully (C huge); report asymptotic factor p^2/sqrt(6)
    deployed_factor = (P**2) / math.sqrt(6)

    return {
        "status": "PASS",
        "plan_rows": plan_rows,
        "env_rows": [
            {k: v for k, v in r.items()} for r in env_rows if r["p"] < 10**6
        ],
        "max_rows": max_rows,
        "census": {
            "n_plan": len(plan_rows),
            "n_max": len(max_rows),
            "all_plancherel_ok": True,
            "all_Winf_le_sqrt_pt": True,
            "envelope_always_weak": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in max_rows),
            "max_bound_over_sqrtC": max(r["bound_over_sqrtC"] for r in max_rows),
            "max_Winf_over_sqrt_pt": max(
                r["Winf_over_sqrt_pt"] for r in plan_rows
            ),
            "max_plancherel_rel_err": max(
                r["max_plancherel_rel_err"] for r in plan_rows
            ),
            "deployed_asymp_p2_over_sqrt6": float(deployed_factor),
            "log10_deployed_asymp": float(math.log10(deployed_factor)),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "note": (
                "W_inf<=sqrt(pt) PROVED; e=3 envelope ~ p^2 t^{3/2} "
                "cannot force sqrt-cancel (factor ~ p^2/sqrt(6))"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v61",
        "title": "Prove W_inf <= sqrt(p t); e=3 envelope too weak for sqrt-cancel",
        "status": "WINF_PROVED_ENVELOPE_TOO_WEAK_OSCILLATORY_OPEN",
        "claims": {
            "proves_W_per_A_Plancherel": True,
            "proves_Winf_le_sqrt_pt": True,
            "proves_e3_S_envelope_p2_t32": True,
            "proves_envelope_cannot_force_sqrt_cancel": True,
            "proves_S_le_sqrtC": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "W_plancherel": lemma_W_plancherel(),
            "Winf": lemma_Winf(),
            "S_envelope": lemma_S_envelope(),
            "envelope_too_weak": lemma_envelope_too_weak(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "per-A Plancherel + e=3 maxS", "python_nt": "GP domain"},
        "impact_on_program": {
            "closed": "W_inf <= sqrt(p t) unconditionally (any t-set)",
            "wall": (
                "e=3 needs oscillatory cancel in triple Fourier; "
                "envelope path is dead for sqrt-cancel"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    plan_lines = []
    for r in cert["toy_suite"]["plan_rows"]:
        plan_lines.append(
            f"| {r['p']} | {r['t']} | {r['Winf_sample']:.1f} | {r['sqrt_pt']:.1f} | "
            f"{r['Winf_over_sqrt_pt']:.2f} | {r['max_plancherel_rel_err']:.1e} |"
        )
    plan_tbl = "\n".join(plan_lines)
    max_lines = []
    for r in cert["toy_suite"]["max_rows"]:
        max_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['bound_S_envelope']:.1e} | "
            f"{r['sqrtC']:.1f} | {r['S_over_sqrtC']:.2f} | {r['bound_over_sqrtC']:.1e} |"
        )
    max_tbl = "\n".join(max_lines)
    return f"""# KB-MCA Route-D v61: `W_inf <= sqrt(p t)` PROVED; envelope dead for √-cancel

Status: **W_inf bound PROVED**; e=3 absolute envelope **too weak** (structural);
oscillatory triple-Fourier path **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Per-A Plancherel (PROVED)

For any t-set `S_arc subset F_p` and any `A`:

```text
W(A,B) = sum_{{x in S_arc}} psi(A x^2 + B x)
f_A(x) = 1_S(x) psi(A x^2)
sum_B |W(A,B)|^2 = p sum_x |f_A|^2 = p t
=> max_B |W(A,B)| <= sqrt(p t)
=> W_inf := max_{{A,B}} |W| <= sqrt(p t)
```

No GP hypothesis: holds for every t-set.

## e=3 envelope (PROVED, and dead)

Combine with v60 `|All| <= sqrt(p) W_inf^3`:

```text
|All| <= p^2 t^{{3/2}}
|S|   <= (1/6)( p^2 t^{{3/2}} + 3t(t-1)+t )
bound / sqrt(C) ~ p^2 / sqrt(6)  -> infinity
```

Even the optimistic typical size `W_inf ~ sqrt(t)` only yields ratio `~ sqrt(p)`.
Absolute-value estimates on the triple Fourier sum **cannot** force v58 √-cancel.

## CAS

### Plancherel / W_inf

| p | t | W_inf (sample) | √(pt) | ratio | Plancherel rel err |
|---|---:|---:|---:|---:|---:|
{plan_tbl}

### e=3 max|S| vs envelope

| p | t | max|S| | envelope | √C | S/√C | env/√C |
|---|---:|---:|---:|---:|---:|---:|
{max_tbl}

- Plancherel max rel err = {cen['max_plancherel_rel_err']:.1e}.
- max W_inf/√(pt) = {cen['max_Winf_over_sqrt_pt']:.2f}.
- Empirical S/√C max = {cen['max_S_over_sqrtC']:.2f}.
- Envelope/√C max on toys = {cen['max_bound_over_sqrtC']:.1e}.
- Deployed asymptotic factor `p^2/sqrt(6)` ≈ 10^{cen['log10_deployed_asymp']:.1f}.

## Link to residual card

v58 needs `|S|<=√C` ⇒ `T=0` at deployed.  
v60 reduced e=3 to `W_inf`.  
v61 **closes** `W_inf<=√(pt)` and **kills** the pure-envelope path.  
Next: phase cancellation in `All = p^{{-1}} sum hatH(-xi) hat_mu(xi)^3`.

Deployed e={d['e']} ≫ 3 needs general-e after e=3 is sharp.

## OPEN

1. Oscillatory bound on the triple Fourier sum for free-1 e=3 on GP arcs.  
2. Reach `|S|<=√C` sparsely for e=3, then general e.  
3. Alternate residual close `|R2|<=e·p` if exp-sums stall.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v61.py --check
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
        "# kb-qatom-route-d-v61\n\n"
        "Prove W_inf <= sqrt(p t); e=3 envelope too weak for sqrt-cancel.\n"
    )
    REPORT_PATH.write_text(
        f"# v61 report\n\nstatus: {cert['status']}\n"
        f"W_inf <= sqrt(p t): PROVED\n"
        f"envelope too weak for sqrt-cancel: PROVED\n"
        f"OPEN oscillatory triple Fourier: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  sum_B |W(A,B)|^2 = p t for each A: PROVED")
    print("  W_inf <= sqrt(p t): PROVED")
    print("  e=3 |S| envelope (1/6)(p^2 t^{3/2}+O(t^2)): PROVED")
    print("  envelope cannot force |S|<=sqrt(C) (factor ~ p^2/sqrt(6)): PROVED")
    print(
        f"  CAS: plan rows={cen['n_plan']}; max S/sqrtC={cen['max_S_over_sqrtC']:.2f}; "
        f"env/sqrtC max={cen['max_bound_over_sqrtC']:.1e}; "
        f"W_inf/sqrt(pt) max={cen['max_Winf_over_sqrt_pt']:.2f}; "
        f"plancherel rel err max={cen['max_plancherel_rel_err']:.1e}"
    )
    print("  OPEN: oscillatory cancel in triple Fourier (envelope path dead)")


if __name__ == "__main__":
    main()
