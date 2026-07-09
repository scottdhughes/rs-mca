#!/usr/bin/env python3
"""KB-MCA Route-D v63: bilinear All factorization + fourth-moment energy of highs.

Attacks oscillatory e=3 wall after v60-v62 envelope exhaustion.

Proved:
  (1) Bilinear factorization (any arc values, char != 2). With monic free-1 phase
        Phi(u,v,w) = l0 h0 + l1 h1 = -l0(u+v+w) + l1(uv+uw+vw),
      one has
        Phi = [-l0(u+v) + l1 u v] + w [-l0 + l1(u+v)].
      Hence
        All = sum_{i,j,k < t} psi(Phi(v_i,v_j,v_k))
            = sum_{i,j < t} psi(-l0(v_i+v_j)+l1 v_i v_j)
                        * G(-l0 + l1(v_i+v_j)),
      where G(alpha) = sum_{k<t} psi(alpha v_k)  (linear arc sum; v59).
  (2) Representation form. Let r2(s) = # {(i,j): v_i+v_j = s}. Then for l1 != 0
        All = sum_s r2(s) * (average of psi(-l0 s + l1 u v) over vi+vj=s) * ...
      and the absolute bound
        |All| <= sum_s r2(s) |G(-l0 + l1 s)|
             <= t * r2(s*) + M * (t^2 - r2(s*))
      where s* = l0 * l1^{-1}, M = max_{alpha != 0} |G(alpha)| <= sqrt(p t - t^2),
      and r2(s*) <= t (distinct arc values: for each i at most one j).
      In particular |All| <= t^2 (1 + M) <= t^2 (1 + sqrt(p t)).
  (3) S envelope from (2): |S| <= (1/6)(|All| + 3t(t-1)+t) with |All| as above.
      Regime: bilinear envelope ~ t^{5/2} sqrt(p) beats v62's p t^{3/2} iff t << sqrt(p);
      at deployed n' ~ 1.2e6 > sqrt(p) ~ 4.6e4 the v62 envelope is tighter. Neither
      reaches sqrt(C).
  (4) Fourth-moment / additive energy. For S(lambda) = sum_U psi(<lambda, high(U)>)
      on F_p^{e-1} (here e=3 => d=2), numpy/analytic Plancherel gives
        sum_lambda |S(lambda)|^2 = p^d sum_h m_h^2,
        sum_lambda |S(lambda)|^4 = p^d sum_z r_m(z)^2,
      where r_m(z) = sum_h m_h m_{h+z} (additive autocorrelation of the high
      multiset). Equivalently sum_z r_m(z)^2 is the additive energy of m.
  (5) L2 scale: if highs are nearly injective (sum m_h^2 ~ C), then
        (p^{-d} sum |S|^2)^{1/2} ~ sqrt(C),
      i.e. RMS of S is the sqrt-cancel scale (matches empirics). Pointwise max
      is not controlled by L2 alone.

CAS:
  (6) Factorization (1) holds (err ~ 1e-12).
  (7) Bound (2) holds; sum_s r2|G| often ~2x tighter than t^2(1+M).
  (8) Energy identity (4) holds numerically.
  (9) Empirical max|S|/sqrt(C) = O(1)-O(3); energy / C^2 mild; no toy with
      |S|>5 sqrt(C) on tested sparse rows.
  (10) Neither bilinear nor v62 envelope forces sqrt-cancel on toys or deployed.

OPEN:
  Oscillatory sum sum_{i,j} psi(K(v_i,v_j)) G(alpha(v_i,v_j)) — keep the phase of
  G and of K, not |G|. Alternate: bound additive energy of free-1 highs of
  3-subsets of a GP well enough for a large-values argument (still insufficient
  alone for uniform |S|<=sqrt(C) without extra structure).

Does NOT close |T|<=H2 for e>2 unconditionally.

  python3 experimental/scripts/verify_kb_qatom_route_d_v63.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v63"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v63.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v63.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v63.report.md"
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


def lemma_bilinear() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_All_bilinear_factorization",
        "statement": (
            "All = sum_{i,j} psi(-l0(vi+vj)+l1 vi vj) * G(-l0+l1(vi+vj)), "
            "G(alpha)=sum_k psi(alpha v_k)."
        ),
        "proof": [
            "Phi(u,v,w) = -l0(u+v+w)+l1(uv+uw+vw)",
            "        = [-l0(u+v)+l1 uv] + w[-l0+l1(u+v)].",
            "Sum on w over the arc = G(-l0+l1(u+v)).",
        ],
    }


def lemma_abs_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e3_All_abs_via_r2_G",
        "statement": (
            "|All| <= sum_s r2(s)|G(-l0+l1 s)| <= t^2 (1+M) with "
            "M=max_{a!=0}|G(a)|<=sqrt(p t - t^2), r2(s*)<=t."
        ),
        "proof": [
            "Group pairs (i,j) by s=vi+vj; each contributes a unimodular times G.",
            "Distinct values => for fixed i, at most one j with vi+vj=s* => r2(s*)<=t.",
            "v59: max_{a!=0}|G|<=sqrt(p t - t^2); |G(0)|=t.",
        ],
    }


def lemma_fourth() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "fourth_moment_energy_identity",
        "statement": (
            "On F_p^d, d=e-1: sum_lambda |S|^2 = p^d sum_h m_h^2 and "
            "sum_lambda |S|^4 = p^d sum_z r_m(z)^2 with r_m = m * m_rev "
            "(additive energy of the high multiset)."
        ),
        "proof": [
            "Plancherel for f=m on the finite abelian group F_p^d.",
            "sum_chi |hat f|^4 = |G| sum_z |(f*f^vee)(z)|^2.",
            "Here hat f = S, |G|=p^d, f^vee(x)=f(-x) for real m.",
        ],
    }


def lemma_L2_scale() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "L2_RMS_is_sqrt_cancel_scale",
        "statement": (
            "If sum_h m_h^2 = C (injective highs), then "
            "(p^{-d} sum_lambda |S|^2)^{1/2} = sqrt(C). "
            "RMS of S is exactly the v58 sqrt-cancel threshold; only the max is open."
        ),
        "proof": [
            "Plancherel: p^{-d} sum |S|^2 = sum m_h^2 = C.",
            "Root-mean-square over lambda is sqrt(C).",
        ],
    }


def lemma_regime() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "bilinear_vs_v62_regime",
        "statement": (
            "Absolute bilinear envelope t^2 sqrt(p t) vs v62 envelope p t^{3/2}: "
            "bilinear better iff t = o(sqrt(p)). Deployed n' > sqrt(p) so v62 tighter; "
            "both >> sqrt(C)."
        ),
        "proof": [
            "Ratio bilinear/v62 ~ t / sqrt(p).",
            "Deployed: n'/sqrt(p) ~ 1.18e6 / 4.6e4 ~ 25 > 1.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_oscillatory_bilinear_or_energy",
        "statement": (
            "Bound sum_{i,j} psi(K(vi,vj)) G(alpha(vi,vj)) with phases, or prove "
            "|S|<=sqrt(C) by GP energy structure of free-1 highs."
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


def linear_G(p: int, vals: list[int]) -> np.ndarray:
    """G(alpha) for all alpha via FFT of arc indicator."""
    ind = np.zeros(p, dtype=np.complex128)
    for x in vals:
        ind[x] += 1.0
    # G(a) = sum_x 1_S(x) psi(a x) = fft(ind) with numpy minus sign; |G| ok
    return np.fft.fft(ind)


def row_bilinear(p: int, n: int, t: int, l0: int, l1: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    # direct All and S
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

    # factorization
    G = linear_G(p, vals)
    # rebuild G with +psi convention matching direct sums:
    # use explicit G for accuracy on small p
    def G_explicit(alpha: int) -> complex:
        s = 0j
        for x in vals:
            s += np.exp(2j * np.pi * ((alpha * x) % p) / p)
        return s

    All_fact = 0j
    for i in range(t):
        for j in range(t):
            u, v = vals[i], vals[j]
            base = (-l0 * ((u + v) % p) + l1 * ((u * v) % p)) % p
            alpha = (-l0 + l1 * ((u + v) % p)) % p
            All_fact += np.exp(2j * np.pi * base / p) * G_explicit(alpha)

    # r2 and abs bound
    r2 = Counter((vals[i] + vals[j]) % p for i in range(t) for j in range(t))
    bound_r2G = 0.0
    for s, cnt in r2.items():
        alpha = (-l0 + l1 * s) % p
        bound_r2G += cnt * abs(G_explicit(alpha))

    M = 0.0
    for a in range(1, p):
        M = max(M, abs(G_explicit(a)))
    M_plan = math.sqrt(p * t - t * t) if t < p else float(t)
    s_star = (l0 * pow(l1, -1, p)) % p
    r_star = r2.get(s_star, 0)
    bound_simple = abs(G_explicit(0)) * r_star + M * (t * t - r_star)

    bound_v62 = p * (t**1.5)
    bound_bilin_asym = (t**2) * (1.0 + math.sqrt(p * t))
    C = math.comb(t, 3)
    bound_S = (1 / 6) * (bound_r2G + 3 * t * (t - 1) + t)

    return {
        "p": p,
        "t": t,
        "l0": l0,
        "l1": l1,
        "abs_All": float(abs(All)),
        "abs_S": float(abs(S)),
        "fact_err": float(abs(All - All_fact)),
        "M": float(M),
        "M_le_plancherel": bool(M <= M_plan + 1e-6),
        "r_star": int(r_star),
        "r_star_le_t": bool(r_star <= t),
        "bound_r2G": float(bound_r2G),
        "bound_simple": float(bound_simple),
        "All_le_r2G": bool(abs(All) <= bound_r2G + 1e-4),
        "All_le_simple": bool(abs(All) <= bound_simple + 1e-4),
        "bound_v62": float(bound_v62),
        "bound_bilin_asym": float(bound_bilin_asym),
        "r2G_over_v62": float(bound_r2G / bound_v62),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(abs(S) / math.sqrt(C)),
        "bound_S_over_sqrtC": float(bound_S / math.sqrt(C)),
        "forces_sqrt_cancel": bool(bound_S <= math.sqrt(C) + 1e-9),
    }


def row_energy(p: int, n: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    freq = np.zeros((p, p), dtype=np.float64)
    C = 0
    for idxs in itertools.combinations(range(t), 3):
        h0, h1 = monic_high3(vals[idxs[0]], vals[idxs[1]], vals[idxs[2]], p)
        freq[h0, h1] += 1
        C += 1
    F = np.fft.fft2(freq)
    absF = np.abs(F)
    sum_S2 = float(np.sum(absF**2))
    sum_S4 = float(np.sum(absF**4))
    sum_m2 = float(np.sum(freq**2))
    # autocorrelation r_m via FFT: r = ifft(|F|^2) * scale
    # numpy: ifft(fft(m) * conj(fft(m))) = m * m_rev circular
    r = np.fft.ifft2(np.abs(F) ** 2).real
    # for real m, sum_z r(z)^2 should equal p^{-d} sum |S|^4? 
    # fft2 convention: sum |F|^2 = p^d sum m^2
    # sum |F|^4 = p^d sum_z r_raw(z)^2 with r_raw = ifft(|F|^2) * ?
    # Check identity: sum |F|^4 / p^d  == sum r^2
    sum_r2 = float(np.sum(r**2))
    # scale: ifft(|F|^2) gives sum_h m_h m_{h-z} * ? 
    # Actually np.fft.ifft2(fft2(a)*conj(fft2(b))) related by 1 factor
    # For a=b=m: corr[z] = sum_h m[h] m[(h-z)%] 
    # ifft2(|fft2(m)|^2) = ifft2(fft2(m)*conj(fft2(m))) 
    # Identity used in packet: sum|S|^4 = p^d sum_z r(z)^2 with matching r.
    # Verify numerically which scale works:
    # expect sum_S2 == p*p * sum_m2
    plancherel_ok = abs(sum_S2 - (p * p) * sum_m2) / max(sum_S2, 1) < 1e-8

    # energy from ifft: r_np = ifft2(|F|^2); for numpy, 
    # sum_h m_h m_{h-z} = (1/p^d) * ifft? 
    # Direct small check via formula sum|S|^4 / p^2 == sum_z (sum_h m_h m_{h+z})^2
    # Compute r_direct via ifft with correct scale:
    # fft2(m)[k] = sum_h m_h exp(-2pi i k h / p)
    # sum_k |fft2(m)[k]|^2 exp(2pi i k z / p) = p^d sum_h m_h m_{h-z}
    # so r(z) = sum_h m_h m_{h-z} = ifft2(|F|^2)[z]   if ifft has 1/N and fft has no 1/N
    # numpy ifft2(x) = 1/N sum ... so ifft2(|F|^2) = (1/p^d) * (p^d r) = r
    # Yes r = ifft2(|F|^2).real should be the autocorrelation.
    # Then sum |F|^4 = sum_k |F|^4 
    # Parseval on r: sum_z r(z)^2 = p^{-d} sum_k |F|^4 ? 
    # fft2(r) = |F|^2, sum |fft2(r)|^2 = p^d sum r^2 => sum |F|^4 = p^d sum r^2
    energy_id_ok = abs(sum_S4 - (p * p) * sum_r2) / max(sum_S4, 1) < 1e-6

    absF0 = absF.copy()
    absF0[0, 0] = 0
    maxS = float(np.max(absF0))
    return {
        "p": p,
        "t": t,
        "C": int(C),
        "sum_m2": float(sum_m2),
        "max_m": int(np.max(freq)),
        "sum_S2": float(sum_S2),
        "sum_S4": float(sum_S4),
        "sum_r2": float(sum_r2),
        "plancherel_ok": bool(plancherel_ok),
        "energy_id_ok": bool(energy_id_ok),
        "maxS": float(maxS),
        "sqrtC": float(math.sqrt(C)),
        "S_over_sqrtC": float(maxS / math.sqrt(C)),
        "energy_over_C2": float(sum_r2 / (C * C)) if C else None,
        "injective": bool(abs(sum_m2 - C) < 1e-9),
        "RMS_S": float(math.sqrt(sum_S2 / (p * p))),  # = sqrt(sum m^2)
        "RMS_over_sqrtC": float(math.sqrt(sum_m2 / C)) if C else None,
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char!=2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    bil_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 15),
        (101, 100, 15),
        (101, 100, 20),
        (127, 126, 15),
        (127, 126, 24),
    ]:
        for l0, l1 in [(1, 1), (3, 5)]:
            r = row_bilinear(p, n, t, l0, l1)
            ensure(r["fact_err"] < 1e-8, f"fact {p},{t}")
            ensure(r["All_le_r2G"], "r2G bound")
            ensure(r["All_le_simple"], "simple bound")
            ensure(r["M_le_plancherel"], "M plancherel")
            ensure(r["r_star_le_t"], "r*")
            ensure(not r["forces_sqrt_cancel"], "still weak")
            bil_rows.append(r)
    ensure(len(bil_rows) >= 10, "bil rows")

    en_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 20),
        (61, 60, 36),
        (101, 100, 15),
        (101, 100, 24),
        (127, 126, 15),
        (127, 126, 36),
    ]:
        if math.comb(t, 3) > 20000:
            continue
        r = row_energy(p, n, t)
        ensure(r["plancherel_ok"], f"plan {p},{t}")
        ensure(r["energy_id_ok"], f"energy {p},{t}")
        ensure(r["S_over_sqrtC"] < 5, "emp S")
        en_rows.append(r)
    ensure(len(en_rows) >= 6, "en rows")

    # regime numbers
    deployed_t = N_PRIME
    ratio_t_over_sqrtp = deployed_t / math.sqrt(P)
    bilin_better_deployed = deployed_t < math.sqrt(P)

    return {
        "status": "PASS",
        "bil_rows": bil_rows,
        "en_rows": en_rows,
        "census": {
            "n_bil": len(bil_rows),
            "n_en": len(en_rows),
            "all_factorizations_ok": True,
            "all_energy_ids_ok": True,
            "envelope_still_weak": True,
            "max_S_over_sqrtC": max(r["S_over_sqrtC"] for r in en_rows),
            "max_bound_S_over_sqrtC": max(
                r["bound_S_over_sqrtC"] for r in bil_rows
            ),
            "min_r2G_over_v62": min(r["r2G_over_v62"] for r in bil_rows),
            "max_r2G_over_v62": max(r["r2G_over_v62"] for r in bil_rows),
            "max_energy_over_C2": max(r["energy_over_C2"] for r in en_rows),
            "max_fact_err": max(r["fact_err"] for r in bil_rows),
            "deployed_t_over_sqrtp": float(ratio_t_over_sqrtp),
            "deployed_bilin_better_than_v62": bool(bilin_better_deployed),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "sqrt_p": float(math.sqrt(P)),
            "note": (
                "bilinear All factorization + energy identity; "
                "absolute bounds still short of sqrt-cancel"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v63",
        "title": "Bilinear All factorization + fourth-moment energy of highs",
        "status": "BILINEAR_ENERGY_PROVED_OSCILLATORY_OPEN",
        "claims": {
            "proves_All_bilinear_factorization": True,
            "proves_All_abs_via_r2_G": True,
            "proves_fourth_moment_energy_identity": True,
            "proves_L2_RMS_is_sqrt_cancel_scale": True,
            "proves_bilinear_vs_v62_regime": True,
            "proves_S_le_sqrtC": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "bilinear": lemma_bilinear(),
            "abs_bound": lemma_abs_bound(),
            "fourth": lemma_fourth(),
            "L2_scale": lemma_L2_scale(),
            "regime": lemma_regime(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "G, energy, maxS", "python_nt": "GP domain"},
        "impact_on_program": {
            "closed": (
                "e=3 All = bilinear form in arc pairs times linear G; "
                "fourth moment = additive energy of highs; L2 sits at sqrt(C)"
            ),
            "wall": "oscillatory bilinear sum (keep phases of K and G)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    bil_lines = []
    for r in cert["toy_suite"]["bil_rows"][:8]:
        bil_lines.append(
            f"| {r['p']} | {r['t']} | {r['l0']},{r['l1']} | {r['abs_All']:.1f} | "
            f"{r['bound_r2G']:.1e} | {r['bound_v62']:.1e} | {r['r2G_over_v62']:.2f} | "
            f"{r['S_over_sqrtC']:.2f} |"
        )
    bil_tbl = "\n".join(bil_lines)
    en_lines = []
    for r in cert["toy_suite"]["en_rows"]:
        en_lines.append(
            f"| {r['p']} | {r['t']} | {r['C']} | {r['sum_m2']:.0f} | {r['max_m']} | "
            f"{r['S_over_sqrtC']:.2f} | {r['energy_over_C2']:.3f} | "
            f"{r['RMS_over_sqrtC']:.3f} |"
        )
    en_tbl = "\n".join(en_lines)
    return f"""# KB-MCA Route-D v63: bilinear All + high energy

Status: **factorization + energy identities PROVED**; absolute bounds still
**short** of `|S|<=√C`. Local on `scott/kb-route-d-T-bound`.

## Bilinear factorization (PROVED)

```text
Phi(u,v,w) = -l0(u+v+w) + l1(uv+uw+vw)
           = [-l0(u+v)+l1 uv] + w [-l0 + l1(u+v)]

All = sum_{{i,j}} psi(-l0(vi+vj)+l1 vi vj) * G(-l0 + l1(vi+vj))
G(alpha) = sum_{{k<t}} psi(alpha v_k)
```

## Absolute bound (PROVED, still weak)

```text
|All| <= sum_s r2(s) |G(-l0 + l1 s)|
      <= t^2 (1 + M),   M = max_{{a!=0}}|G(a)| <= sqrt(p t - t^2)
```

Regime vs v62 (`|All|<= p t^{{3/2}}`): bilinear better iff `t = o(sqrt(p))`.  
Deployed `n'/sqrt(p) ≈ {cen['deployed_t_over_sqrtp']:.1f}` ⇒ **v62 tighter**; both ≫ √C.

## Fourth moment = energy (PROVED)

```text
sum_lambda |S|^2 = p^{{e-1}} sum_h m_h^2
sum_lambda |S|^4 = p^{{e-1}} sum_z r_m(z)^2
```

If highs injective (`sum m^2 = C`), RMS of `S` is exactly `√C` (v58 threshold).

## CAS

### Bilinear rows

| p | t | (l0,l1) | |All| | r2|G| bound | v62 | r2G/v62 | |S|/√C |
|---|---:|---|---:|---:|---:|---:|---:|
{bil_tbl}

### Energy / max|S|

| p | t | C | sum m² | max m | max|S|/√C | energy/C² | RMS/√C |
|---|---:|---:|---:|---:|---:|---:|---:|
{en_tbl}

- factorization max err = {cen['max_fact_err']:.1e}
- max S/√C = {cen['max_S_over_sqrtC']:.2f}
- r2G/v62 in [{cen['min_r2G_over_v62']:.2f}, {cen['max_r2G_over_v62']:.2f}]
- max bound_S/√C (bilinear) = {cen['max_bound_S_over_sqrtC']:.1e}

## Link

v58 needs pointwise `|S|<=√C`. L2 already sits there.  
v60–v62 exhausted `|hat_mu|` envelopes.  
v63 reduces All to **oscillatory bilinear** `sum psi(K) G(alpha)`.

Deployed e={d['e']} ≫ 3 after e=3 is sharp.

## OPEN

1. Phase-sensitive bound on `sum_{{i,j}} psi(K(vi,vj)) G(alpha(vi,vj))`.  
2. GP structure of additive energy of free-1 highs (secondary).  
3. Stress-search for counterexample `|S|>√C` on larger sparse toys.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v63.py --check
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
        "# kb-qatom-route-d-v63\n\n"
        "Bilinear All factorization + fourth-moment energy of highs.\n"
    )
    REPORT_PATH.write_text(
        f"# v63 report\n\nstatus: {cert['status']}\n"
        f"bilinear factorization: PROVED\n"
        f"fourth-moment energy: PROVED\n"
        f"OPEN oscillatory bilinear: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  All = sum_{i,j} psi(K) G(alpha): PROVED")
    print("  |All| <= sum r2|G| <= t^2(1+M): PROVED")
    print("  sum|S|^4 = p^d sum r_m^2 (energy): PROVED")
    print("  L2 RMS = sqrt(sum m^2) (injective => sqrt(C)): PROVED")
    print(
        f"  CAS: bil={cen['n_bil']}; en={cen['n_en']}; "
        f"max S/sqrtC={cen['max_S_over_sqrtC']:.2f}; "
        f"r2G/v62 in [{cen['min_r2G_over_v62']:.2f},{cen['max_r2G_over_v62']:.2f}]; "
        f"deployed t/sqrt(p)={cen['deployed_t_over_sqrtp']:.1f}"
    )
    print("  OPEN: oscillatory sum psi(K) G (keep phases)")


if __name__ == "__main__":
    main()
