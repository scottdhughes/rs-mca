#!/usr/bin/env python3
"""KB-MCA Route-D v66: incomplete GP arc sum |G| bound via Dirichlet completion.

Closes the incomplete-prefix gap left by v65 (full subgroup |G|<=sqrt(p)+1 only).

Proved:
  (1) Dirichlet expansion. Let omega have order n | (p-1), S_t = {omega^k: 0<=k<t}
      with 1 <= t <= n, and for alpha in F_p
        G_t(alpha) = sum_{k=0}^{t-1} psi(alpha omega^k).
      Write 1_{[0,t)}(k) = n^{-1} sum_{m=0}^{n-1} D(m) e^{2 pi i m k / n} with
        D(m) = sum_{j=0}^{t-1} e^{-2 pi i m j / n}
      (so D(0)=t and |D(m)| = |sin(pi t m/n)/sin(pi m/n)| for m != 0 mod n).
      Then
        G_t(alpha) = n^{-1} sum_{m=0}^{n-1} D(m) J(m, alpha),
        J(m,alpha) = sum_{k=0}^{n-1} psi(alpha omega^k) e^{2 pi i m k / n}.
  (2) Mixed Gauss bound for J. For alpha != 0:
        |J(0,alpha)| <= sqrt(p) + 1          (full subgroup sum; v65),
        |J(m,alpha)| <= sqrt(p)              for m != 0 mod n.
      Proof of m!=0: J(m,alpha) = sum_{x in H} psi(alpha x) eta(x) with H=<omega>,
      eta(omega^k)=e^{2 pi i m k / n} nontrivial on H. Expand 1_H via characters
      trivial on H and apply |tau(chi)|=sqrt(p) for all resulting nontrivial
      multiplicative characters (none is trivial because eta is nontrivial on H).
  (3) Dirichlet kernel mass. For 1 <= t <= n,
        sum_{m=1}^{n-1} |D(m)| <= n (1 + ln n).
      Proof: |D(m)| <= n / (2 d(m)) where d(m)=min(m mod n, n - m mod n),
      using |sin(pi m/n)| >= 2 d(m)/n; then
        sum_{m!=0}|D| <= 2 sum_{d=1}^{floor(n/2)} n/(2d) = n H_{floor(n/2)}
        <= n (1 + ln n).
  (4) Incomplete bound. For alpha != 0 and 1 <= t <= n,
        |G_t(alpha)|
          <= (t/n)(sqrt(p)+1) + sqrt(p) (1 + ln n).
      (Combine (1)-(3).) For alpha=0, G_t(0)=t.
  (5) Comparison. Plancherel only gives |G_t| <= sqrt(p t - t^2). The incomplete
      bound is O(sqrt(p) log n + (t/n) sqrt(p)), independent of t except the
      t/n term — much smaller than sqrt(p t) when t is large.
  (6) Deployed numbers (KB): n=2^21, n'=1183520, p=2^31-2^24+1,
        |G_{n'}(alpha)| <= ~7.44e5   for alpha != 0,
        vs Plancherel ~5.02e7, vs B_*=sqrt(2 H2)~3.93e5.
      So incomplete |G| is within a small factor of the soft-B scale (but G is
      the linear arc sum, not the free-1 high sum S).

CAS:
  (7) Bound (4) holds on all tested (p,n,t) incomplete prefixes.
  (8) sum_{m!=0}|D(m)| <= n(1+ln n) holds on tested rows.
  (9) Deployed incomplete bound ~7.44e5 < Plancherel / 60.

OPEN:
  Soft-B still needs max_lambda |S(lambda)| <= B_* for free-1 highs of e-sets
  (not linear G). Incomplete |G| feeds e=2 / bilinear e=3 machinery; general e
  remains the wall.

Does NOT close |T|<=H2; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v66.py --check
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v66"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v66.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v66.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v66.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A_DEP = 1_116_048
J_CORE = N - A_DEP
T_ROW = A_DEP - 2**20
Wdeg = T_ROW - 1
E = Wdeg + 1
M_C = J_CORE - E
FREE_CORE = M_C - Wdeg
N_PRIME = A_DEP + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E
B_STAR = math.sqrt(2 * H2)


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def incomplete_G_bound(p: int, n: int, t: int) -> float:
    """Proved upper bound on max_{alpha != 0} |G_t(alpha)|."""
    return (t / n) * (math.sqrt(p) + 1.0) + math.sqrt(p) * (1.0 + math.log(n))


def lemma_dirichlet() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "incomplete_GP_Dirichlet_expansion",
        "statement": (
            "G_t(alpha) = n^{-1} sum_m D(m) J(m,alpha) with "
            "D(m)=sum_{j<t} e^{-2 pi i m j / n}, "
            "J(m,alpha)=sum_{k<n} psi(alpha omega^k) e^{2 pi i m k / n}."
        ),
        "proof": [
            "Fourier expansion of 1_{[0,t)} on Z/nZ.",
            "Substitute into sum_{k<t} psi(alpha omega^k).",
        ],
    }


def lemma_J() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "mixed_Gauss_J_bound",
        "statement": (
            "For alpha!=0: |J(0,alpha)|<=sqrt(p)+1; "
            "|J(m,alpha)|<=sqrt(p) for m not equiv 0 mod n."
        ),
        "proof": [
            "m=0: full subgroup sum (v65).",
            "m!=0: J=sum_{x in H} psi(alpha x) eta(x), eta nontrivial on H.",
            "1_H = (n/(p-1)) sum_{rho|H=1} rho; expand; all resulting "
            "multiplicative characters are nontrivial (eta nontrivial on H), "
            "each Gauss sum has magnitude sqrt(p); triangle with "
            "(n/(p-1))*((p-1)/n)*sqrt(p)=sqrt(p).",
        ],
    }


def lemma_D_mass() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Dirichlet_kernel_mass",
        "statement": "sum_{m=1}^{n-1} |D(m)| <= n (1 + ln n) for 1<=t<=n.",
        "proof": [
            "|D(m)| = |sin(pi t m/n)/sin(pi m/n)| <= 1/|sin(pi m/n)|.",
            "|sin(pi m/n)| >= 2 d(m)/n with d(m)=min(m,n-m) on 1..n-1 "
            "(sin(pi x) >= 2x on [0,1/2]).",
            "Thus |D(m)| <= n/(2 d(m)).",
            "sum_{m!=0}|D| <= 2 sum_{d=1}^{floor(n/2)} n/(2d) = n H_{floor(n/2)}.",
            "H_k <= 1 + ln k <= 1 + ln n.",
        ],
    }


def lemma_incomplete() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "incomplete_GP_G_bound",
        "statement": (
            "For alpha!=0, 1<=t<=n, |G_t(alpha)| <= "
            "(t/n)(sqrt(p)+1) + sqrt(p)(1+ln n)."
        ),
        "proof": [
            "|G_t| <= n^{-1}( |D(0)||J(0)| + sum_{m!=0}|D(m)||J(m)| ).",
            "<= n^{-1}( t (sqrt(p)+1) + sqrt(p) sum_{m!=0}|D| ).",
            "<= (t/n)(sqrt(p)+1) + sqrt(p)(1+ln n).",
        ],
    }


def lemma_deployed_num() -> dict[str, Any]:
    bnd = incomplete_G_bound(P, N, N_PRIME)
    plan = math.sqrt(P * N_PRIME - N_PRIME**2)
    return {
        "status": "PROVED",
        "name": "deployed_incomplete_G_numerics",
        "statement": (
            f"At deployed (n,n',p): max_{{a!=0}}|G_{{n'}}(a)| <= {bnd:.1f}, "
            f"vs Plancherel {plan:.1f}, vs B_*={B_STAR:.1f}."
        ),
        "proof": ["Plug n=2^21, n'=1183520, p=KoalaBear into (4)."],
        "numbers": {
            "bound": bnd,
            "plancherel": plan,
            "B_star": B_STAR,
            "bound_over_plancherel": bnd / plan,
            "bound_over_B_star": bnd / B_STAR,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_soft_B_free1_S",
        "statement": (
            f"Prove max|S(lambda)| <= B_*~{B_STAR:.0f} for free-1 monic highs "
            "of e-sets on the deployed GP arc (linear G bound is not enough alone)."
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


def gp_prefix(p: int, n: int, t: int) -> list[int]:
    ensure((p - 1) % n == 0, "n|p-1")
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(t)]


def sum_abs_D(n: int, t: int) -> float:
    s = 0.0
    for m in range(1, n):
        # |sin(pi t m / n) / sin(pi m / n)|
        denom = math.sin(math.pi * m / n)
        if abs(denom) < 1e-18:
            s += float(t)  # m multiple of n — should not occur in 1..n-1
        else:
            s += abs(math.sin(math.pi * t * m / n) / denom)
    return s


def max_G_nonzero(p: int, n: int, t: int) -> dict[str, Any]:
    vals = gp_prefix(p, n, t)
    ind = np.zeros(p, dtype=np.complex128)
    for x in vals:
        ind[x] += 1.0
    mags = np.abs(np.fft.fft(ind))
    g0 = float(mags[0])
    gmax = float(np.max(mags[1:])) if p > 1 else 0.0
    bnd = incomplete_G_bound(p, n, t)
    plan = math.sqrt(p * t - t * t) if t < p else float(t)
    return {
        "p": p,
        "n": n,
        "t": t,
        "G0": g0,
        "Gmax": gmax,
        "bound": float(bnd),
        "plancherel": float(plan),
        "Gmax_le_bound": bool(gmax <= bnd + 1e-6),
        "Gmax_le_plancherel": bool(gmax <= plan + 1e-6),
        "bound_over_plancherel": float(bnd / plan) if plan > 0 else None,
        "t_over_n": float(t / n),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")
    ensure((P - 1) % N == 0, "n|p-1")
    ensure(1 <= N_PRIME <= N, "n' range")

    # Dirichlet mass checks
    D_rows = []
    for n, t in [(60, 15), (60, 30), (60, 60), (100, 25), (100, 50), (126, 63), (126, 126)]:
        sD = sum_abs_D(n, t)
        mass_bound = n * (1.0 + math.log(n))
        ensure(sD <= mass_bound + 1e-6, f"D mass n={n} t={t}: {sD} > {mass_bound}")
        D_rows.append(
            {
                "n": n,
                "t": t,
                "sum_abs_D": float(sD),
                "bound_n_1_ln_n": float(mass_bound),
                "ok": True,
            }
        )

    # incomplete G checks
    G_rows = []
    configs = [
        (61, 60, 15),
        (61, 60, 30),
        (61, 60, 45),
        (61, 60, 60),
        (101, 100, 25),
        (101, 100, 50),
        (101, 100, 75),
        (101, 100, 100),
        (127, 126, 31),
        (127, 126, 63),
        (127, 126, 94),
        (127, 126, 126),
        (73, 72, 24),
        (73, 72, 48),
        (97, 96, 32),
        (97, 96, 64),
    ]
    for p, n, t in configs:
        if (p - 1) % n != 0 or t > n:
            continue
        r = max_G_nonzero(p, n, t)
        ensure(abs(r["G0"] - t) < 1e-6, "G0=t")
        ensure(r["Gmax_le_bound"], f"G bound {p},{t}: {r['Gmax']} > {r['bound']}")
        ensure(r["Gmax_le_plancherel"], "plancherel")
        G_rows.append(r)
    ensure(len(G_rows) >= 12, "G rows")

    dep_bound = incomplete_G_bound(P, N, N_PRIME)
    dep_plan = math.sqrt(P * N_PRIME - N_PRIME**2)
    ensure(dep_bound < dep_plan, "deployed better than plancherel")
    ensure(dep_bound < 1e6, "deployed scale sanity")

    return {
        "status": "PASS",
        "D_rows": D_rows,
        "G_rows": G_rows,
        "deployed_numerics": {
            "n": N,
            "n_prime": N_PRIME,
            "p": P,
            "incomplete_bound": float(dep_bound),
            "plancherel_bound": float(dep_plan),
            "B_star": float(B_STAR),
            "bound_over_plancherel": float(dep_bound / dep_plan),
            "bound_over_B_star": float(dep_bound / B_STAR),
            "t_over_n": float(N_PRIME / N),
            "ln_n": float(math.log(N)),
        },
        "census": {
            "n_D": len(D_rows),
            "n_G": len(G_rows),
            "all_G_le_incomplete_bound": True,
            "all_D_mass_ok": True,
            "max_Gmax_over_bound": max(r["Gmax"] / r["bound"] for r in G_rows),
            "min_bound_over_plancherel": min(
                r["bound_over_plancherel"] for r in G_rows if r["t"] < r["n"]
            ),
            "deployed_incomplete_bound": float(dep_bound),
            "deployed_plancherel": float(dep_plan),
            "deployed_B_star": float(B_STAR),
            "deployed_bound_over_plancherel": float(dep_bound / dep_plan),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "n": N,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "incomplete_G_bound": float(dep_bound),
            "note": (
                "incomplete |G|<= (t/n)(sqrt(p)+1)+sqrt(p)(1+ln n) PROVED; "
                "soft-B for free-1 S still open"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v66",
        "title": "Incomplete GP |G| bound via Dirichlet completion",
        "status": "INCOMPLETE_G_PROVED_SOFTB_S_OPEN",
        "claims": {
            "proves_Dirichlet_expansion": True,
            "proves_J_mixed_Gauss_bound": True,
            "proves_Dirichlet_kernel_mass": True,
            "proves_incomplete_GP_G_bound": True,
            "proves_deployed_incomplete_numerics": True,
            "proves_S_le_Bstar_deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "dirichlet": lemma_dirichlet(),
            "J": lemma_J(),
            "D_mass": lemma_D_mass(),
            "incomplete": lemma_incomplete(),
            "deployed_num": lemma_deployed_num(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "max|G|", "python_nt": "GP prefixes + D mass"},
        "impact_on_program": {
            "closed": (
                "incomplete GP |G_t| <= (t/n)(sqrt(p)+1)+sqrt(p)(1+ln n); "
                "deployed ~7.44e5 vs Plancherel ~5e7"
            ),
            "wall": "soft-B max|S|<=B_* for free-1 highs (not linear G)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    dep = cert["toy_suite"]["deployed_numerics"]
    d = cert["deployed"]
    g_lines = []
    for r in cert["toy_suite"]["G_rows"]:
        g_lines.append(
            f"| {r['p']} | {r['n']} | {r['t']} | {r['Gmax']:.2f} | {r['bound']:.1f} | "
            f"{r['plancherel']:.1f} | {r['Gmax']/r['bound']:.3f} |"
        )
    g_tbl = "\n".join(g_lines)
    return f"""# KB-MCA Route-D v66: incomplete GP `|G|` bound

Status: **incomplete GP bound PROVED**; soft-B for free-1 `S` still **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Theorem (PROVED)

For `omega` of order `n | (p-1)`, `1 <= t <= n`, `alpha != 0`:

```text
G_t(alpha) = sum_{{k=0}}^{{t-1}} psi(alpha omega^k)

|G_t(alpha)|  <=  (t/n)(sqrt(p)+1)  +  sqrt(p) (1 + ln n)
```

### Proof outline

1. **Dirichlet completion** on `Z/nZ`: `G_t = n^{{-1}} sum_m D(m) J(m,alpha)`.  
2. **`|J(0)| <= sqrt(p)+1`**, **`|J(m)| <= sqrt(p)`** (`m != 0`) by subgroup /
   mixed Gauss sums (v65 + character expansion of `1_H`).  
3. **`sum_{{m!=0}} |D(m)| <= n(1+ln n)`** via `|D| <= n/(2d(m))` and harmonic sums.  
4. Triangle inequality yields the bound.

## Deployed numerics (PROVED arithmetic)

| quantity | value |
|---|---:|
| n | {dep['n']} |
| n' | {dep['n_prime']} |
| t/n | {dep['t_over_n']:.4f} |
| ln n | {dep['ln_n']:.3f} |
| **incomplete |G| bound** | **{dep['incomplete_bound']:.1f}** |
| Plancherel √(pt−t²) | {dep['plancherel_bound']:.1f} |
| bound / Plancherel | {dep['bound_over_plancherel']:.4f} |
| B_\\* = √(2 H2) | {dep['B_star']:.1f} |
| bound / B_\\* | {dep['bound_over_B_star']:.2f} |

Incomplete linear `|G|` is ~**67×** tighter than Plancherel at deployed, and within
~**1.9×** of the soft-B scale `B_\\*` — but **soft-B applies to free-1 high sums `S`**,
not to linear arc sums `G`.

## CAS

| p | n | t | max|G| | bound | Plancherel | Gmax/bound |
|---|---:|---:|---:|---:|---:|---:|
{g_tbl}

- all rows satisfy Gmax ≤ bound (max Gmax/bound = {cen['max_Gmax_over_bound']:.3f})
- Dirichlet mass checks: {cen['n_D']} rows OK

## Link

v65: full subgroup `|G|≤√p+1`; deployed arc incomplete.  
v66: **incomplete bound proved**.  
e=2 / bilinear e=3 can now use `|G| ≪ √(pt)`.  
Residual close still needs `max|S|≤B_\\*≈{d['B_star']:.0f}` for free-1 highs.

## OPEN

1. **Primary:** `max_{{λ≠0}} |S(λ)| ≤ B_\\*` at deployed `(n',e)`.  
2. Feed incomplete `|G|` into e=3 CS / energy for sharper toy bounds.  
3. Alternate `|R2|≤e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v66.py --check
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
        "# kb-qatom-route-d-v66\n\n"
        "Incomplete GP |G| bound via Dirichlet completion.\n"
    )
    REPORT_PATH.write_text(
        f"# v66 report\n\nstatus: {cert['status']}\n"
        f"incomplete GP |G| bound: PROVED\n"
        f"OPEN soft-B free-1 S: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  G_t = n^{-1} sum D(m) J(m): PROVED expansion")
    print("  |J(0)|<=sqrt(p)+1, |J(m)|<=sqrt(p) (m!=0): PROVED")
    print("  sum|D| <= n(1+ln n): PROVED")
    print("  |G_t| <= (t/n)(sqrt(p)+1)+sqrt(p)(1+ln n) (a!=0): PROVED")
    print(
        f"  deployed bound={cen['deployed_incomplete_bound']:.1f} "
        f"(Plancherel={cen['deployed_plancherel']:.1f}, "
        f"ratio={cen['deployed_bound_over_plancherel']:.4f}); "
        f"B_*={cen['deployed_B_star']:.1f}"
    )
    print(
        f"  CAS: G rows={cen['n_G']}; max Gmax/bound={cen['max_Gmax_over_bound']:.3f}"
    )
    print("  OPEN: max|S|<=B_* for free-1 highs at deployed")


if __name__ == "__main__":
    main()
