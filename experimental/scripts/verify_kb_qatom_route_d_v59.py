#!/usr/bin/env python3
"""KB-MCA Route-D v59: Plancherel bound on arc character sums G; e=2 S bound.

Continues v58 attack on |S(lambda)| for free-1 high exponential sums.

Proved:
  (1) Arc indicator Plancherel. Let S_arc subset F_p be any t-element set
      (in particular a GP arc), and
        G(a) = sum_{x in S_arc} psi(a x),   a in F_p.
      Then sum_{a != 0} |G(a)|^2 = p t - t^2, hence
        max_{a != 0} |G(a)|  <=  sqrt(p t - t^2)  <= sqrt(p t).
  (2) e=2 free-1 high sum (v58): with v_i = arc values,
        S(lam) = (1/2)( G(lam)^2 - G(2 lam) ).
      Therefore
        max_{lam != 0} |S(lam)|  <=  (1/2)( p t - t^2 + sqrt(p t - t^2) ).
  (3) Combined with v58 conditional coll bound for e=2:
        coll <= C^2/p + B_S^2,  C=binom(t,2), B_S as in (2).
      This is rigorous but at deployed e=2 scale is far weaker than |T|<=p
      (already closed). Recorded for the method, not as the e=2 card path.

CAS:
  (4) max|G| respects sqrt(pt-t^2); often much smaller (e.g. ~ few * sqrt(t)).
  (5) Empirically |S|/sqrt(C) = O(1)-O(8) for e=2; Plancherel-composed B_S
      is >> sqrt(C) when t << p (so this G-bound does NOT prove sqrt-cancel
      for S). Full multiplicative group t=p-1: |G|=1, |S|=1 (exact).
  (6) e=3: |S|/sqrt(C) ~ 1.7-2.9 on small-p suite (near sqrt-cancel empirically).

OPEN:
  Prove |S(lambda)| <= sqrt(C) (or B with C^2/p^{e-1}+B^2 <= 2 H2) for e>=3
  free-1 highs on GP arcs; improve e=2 S bound below the G-composition if desired.

Does NOT unconditionally close |T|<=H2 for e>2.

  python3 experimental/scripts/verify_kb_qatom_route_d_v59.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v59"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v59.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v59.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v59.report.md"
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


def lemma_G_plancherel() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "arc_additive_sum_L2_to_Linf",
        "statement": (
            "For any S_arc subset F_p with |S_arc|=t and nontrivial additive psi, "
            "G(a)=sum_{x in S_arc} psi(a x) satisfies "
            "sum_{a!=0}|G(a)|^2 = p t - t^2, hence "
            "max_{a!=0}|G(a)| <= sqrt(p t - t^2) <= sqrt(p t)."
        ),
        "proof": [
            "Let 1_S be the indicator of S_arc on F_p. Fourier transform on F_p:",
            "sum_a |hat 1_S(a)|^2 = p sum_x 1_S(x)^2 = p t  (Plancherel).",
            "hat 1_S(0) = t, so sum_{a!=0}|G(a)|^2 = p t - t^2.",
            "Therefore some/max |G(a)|^2 <= p t - t^2.",
        ],
    }


def lemma_e2_S_from_G() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_S_bound_from_G_plancherel",
        "statement": (
            "For e=2 free-1 highs on an arc of t values in F_p, "
            "max_{lam!=0}|S(lam)| <= (1/2)(p t - t^2 + sqrt(p t - t^2))."
        ),
        "proof": [
            "S(lam)=(1/2)(G(lam)^2 - G(2 lam)) (v58).",
            "|S| <= (1/2)(|G(lam)|^2 + |G(2lam)|) <= (1/2)(M^2 + M)",
            "with M=sqrt(p t - t^2) from previous lemma.",
        ],
    }


def lemma_full_star() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "full_multiplicative_group_G_eq_minus_one",
        "statement": (
            "If S_arc = F_p^x (e.g. t=n=p-1 with omega primitive), then "
            "G(a) = sum_{x!=0} psi(a x) = -1 for a != 0, hence for e=2, |S(lam)|=1."
        ),
        "proof": [
            "sum_{x in F_p} psi(a x) = 0 for a!=0, and the x=0 term is 1, so sum_{x!=0}=-1.",
            "S=(1/2)(G^2 - G(2lam)) = (1/2)(1 - (-1)) = 1.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_S_sqrtC_for_e_ge_3_and_sharp_e2",
        "statement": (
            "Prove |S(lambda)| <= sqrt(C) for free-1 high sums on GP arcs "
            f"(especially e>=3, deployed e={E}). The G-Plancherel bound gives "
            "only |S|=O(p t) for e=2 composition, which does not imply sqrt-cancel."
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


def G_stats(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    ind = np.zeros(p, dtype=np.float64)
    for i in range(t):
        ind[vals[i]] += 1
    F = np.fft.fft(ind)
    absG = np.abs(F)
    maxG = float(np.max(absG[1:]))
    # Plancherel check: sum_{a!=0}|G|^2 = pt - t^2
    sumG2 = float(np.dot(absG[1:], absG[1:]))
    expected = p * t - t * t
    bound = math.sqrt(max(expected, 0))
    return {
        "p": p,
        "t": t,
        "maxG": maxG,
        "sumG2": sumG2,
        "sumG2_expected": expected,
        "bound": bound,
        "maxG_le_bound": maxG <= bound + 1e-6,
        "plancherel_err": abs(sumG2 - expected),
        "sqrt_p": math.sqrt(p),
        "sqrt_t": math.sqrt(t),
        "sqrt_pt": math.sqrt(p * t),
    }


def e2_S_stats(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    ind = np.zeros(p, dtype=np.float64)
    for i in range(t):
        ind[vals[i]] += 1
    F = np.fft.fft(ind)
    maxG = float(np.max(np.abs(F[1:])))
    maxS = 0.0
    for lam in range(1, p):
        G1 = F[lam]
        G2 = F[(2 * lam) % p]
        S = 0.5 * (G1 * G1 - G2)
        maxS = max(maxS, abs(S))
    C = t * (t - 1) // 2
    M = math.sqrt(p * t - t * t)
    B_S_thm = 0.5 * (M * M + M)
    return {
        "p": p,
        "t": t,
        "C": C,
        "maxG": maxG,
        "maxS": float(maxS),
        "sqrtC": math.sqrt(C),
        "S_over_sqrtC": float(maxS) / math.sqrt(C),
        "B_S_thm": B_S_thm,
        "S_le_B_thm": float(maxS) <= B_S_thm + 1e-6,
        "thm_implies_sqrt_cancel": B_S_thm <= math.sqrt(C) + 1e-9,
        "coll_bound_thm": C * C / p + B_S_thm * B_S_thm,
    }


def e3_S_stats(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    for idxs in itertools.combinations(range(t), 3):
        poly = [1]
        for i in idxs:
            v = vals[i]
            new = [0] * (len(poly) + 1)
            mv = (-v) % p
            for j, c in enumerate(poly):
                new[j] = (new[j] + c) % p
                new[j + 1] = (new[j + 1] + c * mv) % p
            poly = new
        freq[poly[1] % p, poly[2] % p] += 1
        C += 1
    F = np.fft.fft2(freq)
    absS = np.abs(F)
    absS[0, 0] = 0
    maxS = float(np.max(absS))
    return {
        "p": p,
        "t": t,
        "C": C,
        "maxS": maxS,
        "sqrtC": math.sqrt(C),
        "S_over_sqrtC": maxS / math.sqrt(C),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P > E, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    g_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126), (10007, 5003), (20011, 2001)]:
        for t in [20, 40, 50, 100]:
            if t >= n or t >= p:
                continue
            if (p - 1) % n != 0:
                continue
            r = G_stats(p, n, t)
            ensure(r["maxG_le_bound"], "G bound")
            ensure(r["plancherel_err"] < 1e-4 * max(r["sumG2_expected"], 1), "plancherel G")
            g_rows.append(r)

    ensure(len(g_rows) >= 8, "g rows")

    e2_rows = []
    for p, n in [(61, 60), (101, 100), (10007, 5003)]:
        for t in [20, 34, 50]:
            if t > n:
                continue
            r = e2_S_stats(p, n, t)
            ensure(r["S_le_B_thm"], "S from G bound")
            e2_rows.append(r)

    # full star: t=n=p-1
    full_rows = []
    for p in [61, 101, 127]:
        n = p - 1
        r = e2_S_stats(p, n, n)
        ensure(r["maxG"] < 1.01, "full G ~ 1")
        ensure(r["maxS"] < 1.01, "full S ~ 1")
        full_rows.append(r)

    # G-bound does not imply sqrt-cancel for sparse large p
    sparse_fail = [r for r in e2_rows if r["p"] >= 1000 and not r["thm_implies_sqrt_cancel"]]
    ensure(len(sparse_fail) >= 1, "G-bound not enough for sqrt-cancel sparsely")

    e3_rows = []
    for p, n in [(61, 60), (101, 100)]:
        for t in [18, 30, 51]:
            if t > n or math.comb(t, 3) > 30000:
                continue
            e3_rows.append(e3_S_stats(p, n, t))

    ensure(len(e3_rows) >= 4, "e3")

    return {
        "status": "PASS",
        "g_rows": g_rows,
        "e2_rows": e2_rows,
        "e3_rows": e3_rows,
        "full_rows": full_rows,
        "census": {
            "n_g": len(g_rows),
            "n_e2": len(e2_rows),
            "n_e3": len(e3_rows),
            "all_G_plancherel": True,
            "all_S_le_G_bound": True,
            "full_star_G_S_unit": True,
            "G_bound_not_sqrt_cancel_sparse": True,
            "max_e2_S_over_sqrtC": max(r["S_over_sqrtC"] for r in e2_rows),
            "max_e3_S_over_sqrtC": max(r["S_over_sqrtC"] for r in e3_rows),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "G_bound_deployed_e2": 0.5
            * (
                (P * N_PRIME - N_PRIME**2)
                + math.sqrt(P * N_PRIME - N_PRIME**2)
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v59",
        "title": "Plancherel bound on arc G-sums; e=2 S from G; sqrt-cancel still open",
        "status": "G_PLANCHEREL_PROVED_SQRT_CANCEL_OPEN",
        "claims": {
            "proves_G_max_le_sqrt_pt_minus_t2": True,
            "proves_e2_S_bound_from_G": True,
            "proves_full_star_G_eq_1": True,
            "proves_sqrt_cancellation": False,
            "G_bound_implies_sqrt_cancel": False,
            "proves_T_le_H2_deployed_e_gt_2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "G_plancherel": lemma_G_plancherel(),
            "e2_S": lemma_e2_S_from_G(),
            "full_star": lemma_full_star(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "G and S via FFT", "python_nt": "GP domain"},
        "impact_on_program": {
            "closed": "sharp L2->Linf for arc additive sums G; e=2 S via G",
            "wall": "sqrt-cancel for S (e>=3 especially); G-bound too coarse for S",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    g_lines = []
    for r in cert["toy_suite"]["g_rows"][:10]:
        g_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxG']:.2f} | {r['bound']:.2f} | "
            f"{r['plancherel_err']:.1e} |"
        )
    e2_lines = []
    for r in cert["toy_suite"]["e2_rows"]:
        e2_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['B_S_thm']:.1e} | "
            f"{r['sqrtC']:.1f} | {r['S_over_sqrtC']:.2f} | {r['thm_implies_sqrt_cancel']} |"
        )
    e3_lines = []
    for r in cert["toy_suite"]["e3_rows"]:
        e3_lines.append(
            f"| {r['p']} | {r['t']} | {r['maxS']:.1f} | {r['sqrtC']:.1f} | "
            f"{r['S_over_sqrtC']:.2f} |"
        )
    return f"""# KB-MCA Route-D v59: Plancherel bound on arc sums `G`

Status: **`max|G| <= sqrt(p t - t^2)` PROVED**; e=2 `S` bound from `G` PROVED;
that bound **does not** yield √-cancellation for `S` when `t << p`. Local packet.

## Arc sum G (PROVED)

For any `t`-set `S_arc ⊂ F_p` (GP arc included):

```text
G(a) = sum_{{x in S_arc}} psi(a x)
sum_{{a != 0}} |G(a)|^2 = p t - t^2
max_{{a != 0}} |G(a)|  <=  sqrt(p t - t^2)  <= sqrt(p t)
```

### CAS

| p | t | max|G| | bound | Plancherel err |
|---|---:|---:|---:|---:|
{chr(10).join(g_lines)}

## e=2: S from G (PROVED)

```text
S(lam) = (1/2)(G(lam)^2 - G(2 lam))
|S| <= (1/2)(M^2 + M),  M = sqrt(p t - t^2)
```

| p | t | max|S| | B_S thm | √C | S/√C | thm⇒√-cancel? |
|---|---:|---:|---:|---:|---:|---|
{chr(10).join(e2_lines)}

Sparse large `p`: thm **fails** to imply √-cancel (`B_S thm >> √C`), while
empirical `S/√C` stays moderate. Need a sharper `S` estimate than composing
the `G` bound.

### Full multiplicative group (PROVED)

`S_arc = F_p^x` ⇒ `G(a)=-1` (`a!=0`) ⇒ e=2 `|S|=1`.

## e=3 empirical

| p | t | max|S| | √C | S/√C |
|---|---:|---:|---:|---:|
{chr(10).join(e3_lines)}

## Link to residual card (v58)

```text
sqrt-cancel |S|<=√C  ⇒  coll <= C^2/p^{{e-1}}  ⇒  T=0 at deployed
```

v59 gives tools for e=2 `G`/`S` but **not** yet √-cancel for general free-1 highs.

Deployed e=2 card path remains `|T|<=p<=H2` (v48/v54), not this coll bound.

## OPEN

1. Prove `|S(lambda)| <= √C` for free-1 highs on GP arcs (e≥3 primary).  
2. Sharpen e=2 `S` beyond `O(p t)` composition (optional).  
3. Multilinear / hybrid sum expression for e≥3 analogous to e=2 `G`-formula.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v59.py --check
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
        "# kb-qatom-route-d-v59\n\n"
        "Plancherel bound max|G|<=sqrt(pt-t^2); e=2 S from G; sqrt-cancel open.\n"
    )
    REPORT_PATH.write_text(
        f"# v59 report\n\nstatus: {cert['status']}\n"
        f"G Plancherel: PROVED\n"
        f"e2 S from G: PROVED\n"
        f"OPEN sqrt-cancel: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  max|G| <= sqrt(p t - t^2): PROVED (Plancherel on F_p)")
    print("  e=2 |S| <= 1/2(M^2+M), M=sqrt(pt-t^2): PROVED")
    print("  full F_p^*: |G|=1, e=2 |S|=1: PROVED")
    print(
        f"  CAS: G rows={cen['n_g']}; e2 S/sqrtC max={cen['max_e2_S_over_sqrtC']:.2f}; "
        f"e3 max={cen['max_e3_S_over_sqrtC']:.2f}; G-bound NOT => sqrt-cancel sparsely"
    )
    print("  OPEN: prove |S|<=sqrt(C) for free-1 highs (e>=3)")


if __name__ == "__main__":
    main()
