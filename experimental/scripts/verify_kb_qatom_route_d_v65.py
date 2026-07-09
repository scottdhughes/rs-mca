#!/usr/bin/env python3
"""KB-MCA Route-D v65: additive energy via |G|^4; subgroup |G|<=sqrt(p)+1.

Pushes soft-B / e=3 CS path by controlling E_+(S) = sum_s r(s)^2 for arc sets
(v64: |All| <= sqrt(E_+ p t) for e=3).

Proved:
  (1) Energy identity (any t-set S subset F_p). With
        G(alpha) = sum_{x in S} psi(alpha x),
        r(s) = |{(x,y) in S^2: x+y = s}| = |S cap (s-S)|  (ordered),
      one has
        sum_s r(s)^2 = p^{-1} sum_alpha |G(alpha)|^4.
      (Fourier: r = 1_S * 1_S, hat r = G·G, Plancherel on r.)
  (2) L^infty / L^2 bound (any t-set). Using |G(0)|=t,
        max_{a!=0}|G(a)| <= M := sqrt(p t - t^2)  (v59 Plancherel),
        sum |G|^4 <= t^4 + M^2 (p t - t^2) = t^4 + t^2 (p-t)^2,
      hence
        E_+(S) := sum r^2 <= t^2 ( t^2 + (p-t)^2 ) / p.
  (3) Multiplicative subgroup bound. If H subset F_p^* is a subgroup of order
        t | (p-1) and a != 0, then
        |sum_{x in H} psi(a x)| <= sqrt(p) + t/(p-1) <= sqrt(p) + 1.
      Proof: 1_H(x) = (t/(p-1)) sum_{chi: chi|_H = 1} chi(x) on F_p^*;
        sum_{x in H} psi(a x) = (t/(p-1)) sum_{chi|H=1} chi(a)^{-1} tau(chi)
        with Gauss |tau(chi)|=sqrt(p) (chi nontrivial) and tau(triv)=-1;
        there are (p-1)/t such chi, one trivial => bound as above.
  (4) Subgroup energy. For such H, E_+(H) <= t^4/p + (sqrt(p)+1)^4.
      (Plug |G(0)|=t and |G(a)|<=sqrt(p)+1 into (1).)
  (5) e=3 CS consequence (v64). On a subgroup arc,
        |All| <= sqrt(E_+ p t) <= sqrt( (t^4/p + (sqrt(p)+1)^4) p t )
               = sqrt( t^5 + (sqrt(p)+1)^4 p t ).
      Dominant term ~ p^{3/2} t^{1/2} when t = O(p); still >> sqrt(C)~t^{3/2}/sqrt(6)
      by ~ p^{3/2}/t  (method gap for e=3 sqrt-cancel unchanged in order).
  (6) Deployed residual arc is an *incomplete* length-n' prefix of the cyclic
      subgroup of order n=2^{21} | (p-1), not the full subgroup. Bound (3)
      applies to full subgroups only; incomplete GP remains OPEN for the √p law.

CAS:
  (7) Identity (1) holds (err ~ 1e-12).
  (8) Bound (2) holds; often loose vs true E_+.
  (9) Subgroup max_{a!=0}|G| <= sqrt(p)+1 on all tested (p,t) with t|(p-1).
  (10) Incomplete prefixes: max|G| still <= sqrt(p)+1 on tested rows but not proved.
  (11) Deployed B_*=sqrt(2 H2)~3.93e5 restated; still no max|S|<=B_* proof.

OPEN:
  Incomplete GP: prove max|G| << sqrt(p t) (ideally O(sqrt(p) polylog) or better)
  for prefixes of the order-n KB subgroup; or hit soft-B max|S|<=B_* for general e.

Does NOT close |T|<=H2; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v65.py --check
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v65"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v65.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v65.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v65.report.md"
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


def lemma_energy_id() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "additive_energy_via_G4",
        "statement": (
            "For any S subset F_p: sum_s r(s)^2 = p^{-1} sum_alpha |G(alpha)|^4 "
            "with r(s)=|S cap (s-S)| (ordered) and G= Fourier of 1_S."
        ),
        "proof": [
            "r = 1_S * 1_S (additive convolution).",
            "hat r = G · G.",
            "Plancherel: sum_s |r|^2 = p^{-1} sum_alpha |hat r|^2 = p^{-1} sum |G|^4.",
        ],
    }


def lemma_energy_LinfL2() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "energy_Linf_L2_bound",
        "statement": (
            "E_+(S) <= t^2 (t^2 + (p-t)^2) / p for |S|=t, "
            "via max_{a!=0}|G|<=sqrt(p t - t^2)."
        ),
        "proof": [
            "sum |G|^4 <= |G(0)|^4 + max_{a!=0}|G|^2 * sum_{a!=0}|G|^2.",
            "|G(0)|=t; sum_{a!=0}|G|^2 = p t - t^2; max^2 <= p t - t^2.",
            "Thus sum|G|^4 <= t^4 + (pt-t^2)^2 = t^4 + t^2(p-t)^2.",
            "Divide by p.",
        ],
    }


def lemma_subgroup_G() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multiplicative_subgroup_G_le_sqrtp_plus_1",
        "statement": (
            "If H <= F_p^* has order t|(p-1) and a!=0, then "
            "|sum_{x in H} psi(a x)| <= sqrt(p) + t/(p-1) <= sqrt(p)+1."
        ),
        "proof": [
            "On F_p^*: 1_H = (t/(p-1)) sum_{chi: chi|_H=1} chi.",
            "sum_{x in H} psi(a x) = (t/(p-1)) sum_{chi|H=1} chi(a)^{-1} tau(chi).",
            "tau(triv)=-1; |tau(nontriv)|=sqrt(p); # of chi with chi|H=1 is (p-1)/t.",
            "Triangle => (t/(p-1))(1 + ((p-1)/t - 1) sqrt(p)) "
            "= t/(p-1) + (1 - t/(p-1))sqrt(p) <= sqrt(p)+1.",
        ],
    }


def lemma_subgroup_energy() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "subgroup_energy_bound",
        "statement": (
            "For multiplicative subgroup H of order t: "
            "E_+(H) <= t^4/p + (sqrt(p)+1)^4."
        ),
        "proof": [
            "sum|G|^4 <= t^4 + (p-1)(sqrt(p)+1)^4.",
            "E_+ = p^{-1} sum|G|^4 <= t^4/p + (1-1/p)(sqrt(p)+1)^4 "
            "<= t^4/p + (sqrt(p)+1)^4.",
        ],
    }


def lemma_deployed_incomplete() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "deployed_arc_is_incomplete_GP",
        "statement": (
            f"Deployed pure-untyped window is a length-n'={N_PRIME} prefix of the "
            f"cyclic subgroup of n={N}=2^21-th roots in F_p (n | p-1). "
            "Subgroup |G|<=sqrt(p)+1 applies to the full order-n (or order-t) "
            "subgroup, not automatically to the incomplete prefix of length n'."
        ),
        "proof": [
            f"p-1 = 2^24 * 127, so 2^21 | (p-1).",
            "MCA domain = full mu_n; residual arc uses first n' indices only.",
            "n' = 1183520 < n = 2097152.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_incomplete_GP_G_and_soft_B",
        "statement": (
            f"Prove sharp |G| for incomplete GP prefixes (deployed n'), and/or "
            f"max|S|<=B_*~{B_STAR:.0f} for free-1 highs at deployed (n',e)."
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


def subgroup_vals(p: int, t: int) -> list[int]:
    ensure((p - 1) % t == 0, f"t|{p-1}")
    g = prim_root(p)
    om = pow(g, (p - 1) // t, p)
    return [pow(om, i, p) for i in range(t)]


def gp_prefix(p: int, n: int, t: int) -> list[int]:
    ensure((p - 1) % n == 0, f"n|{p-1}")
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(t)]


def analyze_set(p: int, vals: list[int], kind: str) -> dict[str, Any]:
    t = len(vals)
    ind = np.zeros(p, dtype=np.complex128)
    for x in vals:
        ind[x] += 1.0
    hat = np.fft.fft(ind)  # |hat[a]| = |G| under either sign
    mags = np.abs(hat)
    g0 = float(mags[0])
    gmax = float(np.max(mags[1:])) if p > 1 else 0.0
    sum_G2 = float(np.sum(mags**2))
    sum_G4 = float(np.sum(mags**4))
    # r via ifft(|hat|^2); numpy ifft => r(s) = sum_x 1(x)1(s-x)
    r = np.fft.ifft(mags**2).real
    E = float(np.sum(r**2))
    E_from_G4 = sum_G4 / p
    M_plan = math.sqrt(p * t - t * t) if t < p else float(t)
    E_bound_LinfL2 = (t**2 * (t**2 + (p - t) ** 2)) / p
    sqrtp = math.sqrt(p)
    subgroup_bound = sqrtp + 1.0
    return {
        "kind": kind,
        "p": p,
        "t": t,
        "G0": g0,
        "G0_ok": bool(abs(g0 - t) < 1e-6),
        "Gmax": gmax,
        "sqrt_p": float(sqrtp),
        "sqrt_pt_t2": float(M_plan),
        "Gmax_le_plancherel": bool(gmax <= M_plan + 1e-6),
        "Gmax_le_sqrtp_plus_1": bool(gmax <= subgroup_bound + 1e-6),
        "sum_G2": sum_G2,
        "plancherel_G2_ok": bool(abs(sum_G2 - p * t) < 1e-6),
        "sum_G4": sum_G4,
        "E_plus": E,
        "E_from_G4": float(E_from_G4),
        "energy_id_err": float(abs(E - E_from_G4)),
        "energy_id_ok": bool(abs(E - E_from_G4) < 1e-6),
        "E_bound_LinfL2": float(E_bound_LinfL2),
        "E_le_LinfL2": bool(E <= E_bound_LinfL2 + 1e-6),
        "E_bound_subgroup": float((t**4) / p + (sqrtp + 1) ** 4),
        "E_over_t2": float(E / (t * t)),
        "CS_All_bound": float(math.sqrt(E * p * t)),  # v64
        "v62_All_bound": float(p * (t**1.5)),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")
    ensure((P - 1) % N == 0, "n|p-1 deployed")
    ensure(N_PRIME < N, "incomplete deployed")

    sub_rows = []
    for p in [61, 73, 97, 101, 109, 127, 151, 181]:
        # all proper divisors of p-1 with 3 <= t <= (p-1)//2
        for t in range(3, (p - 1) // 2 + 1):
            if (p - 1) % t != 0:
                continue
            r = analyze_set(p, subgroup_vals(p, t), "subgroup")
            ensure(r["G0_ok"], "G0")
            ensure(r["plancherel_G2_ok"], "G2")
            ensure(r["energy_id_ok"], "E id")
            ensure(r["E_le_LinfL2"], "E LinfL2")
            ensure(
                r["Gmax_le_sqrtp_plus_1"],
                f"sub Gmax {p},{t}: {r['Gmax']} > {r['sqrt_p']+1}",
            )
            ensure(r["E_plus"] <= r["E_bound_subgroup"] + 1e-6, "sub E bound")
            sub_rows.append(r)
    ensure(len(sub_rows) >= 20, "sub rows")

    inc_rows = []
    for p, n, t in [
        (61, 60, 12),
        (61, 60, 15),
        (61, 60, 30),
        (101, 100, 20),
        (101, 100, 40),
        (127, 126, 18),
        (127, 126, 36),
        (127, 126, 63),
    ]:
        if t > n or (p - 1) % n != 0:
            continue
        r = analyze_set(p, gp_prefix(p, n, t), "incomplete_gp")
        ensure(r["energy_id_ok"], "inc E id")
        ensure(r["E_le_LinfL2"], "inc E bound")
        ensure(r["Gmax_le_plancherel"], "inc plancherel")
        # empirical: often <= sqrt(p)+1 but not asserted as theorem
        inc_rows.append(r)
    ensure(len(inc_rows) >= 6, "inc rows")

    # deployed structural facts
    deployed = {
        "n": N,
        "n_prime": N_PRIME,
        "e": E,
        "p": P,
        "H2": H2,
        "B_star": float(B_STAR),
        "n_divides_p_minus_1": bool((P - 1) % N == 0),
        "n_prime_lt_n": bool(N_PRIME < N),
        "full_subgroup_order_n_G_bound_proved": True,
        "incomplete_prefix_G_bound_proved": False,
    }

    return {
        "status": "PASS",
        "sub_rows": sub_rows,
        "inc_rows": inc_rows,
        "deployed_structure": deployed,
        "census": {
            "n_sub": len(sub_rows),
            "n_inc": len(inc_rows),
            "all_energy_ids_ok": True,
            "all_sub_G_le_sqrtp_plus_1": True,
            "max_sub_Gmax_over_sqrtp": max(
                r["Gmax"] / r["sqrt_p"] for r in sub_rows
            ),
            "max_inc_Gmax_over_sqrtp": max(
                r["Gmax"] / r["sqrt_p"] for r in inc_rows
            ),
            "max_sub_E_over_t2": max(r["E_over_t2"] for r in sub_rows),
            "max_inc_E_over_t2": max(r["E_over_t2"] for r in inc_rows),
            "max_energy_id_err": max(
                r["energy_id_err"] for r in sub_rows + inc_rows
            ),
            "frac_inc_Gmax_le_sqrtp_plus_1": sum(
                1 for r in inc_rows if r["Gmax_le_sqrtp_plus_1"]
            )
            / len(inc_rows),
            "B_star": float(B_STAR),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "note": (
                "subgroup |G|<=sqrt(p)+1 PROVED; deployed arc incomplete; "
                "soft-B still open"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v65",
        "title": "Additive energy via |G|^4; subgroup |G|<=sqrt(p)+1",
        "status": "ENERGY_SUBGROUP_PROVED_INCOMPLETE_SOFTB_OPEN",
        "claims": {
            "proves_energy_identity_G4": True,
            "proves_energy_Linf_L2_bound": True,
            "proves_subgroup_G_le_sqrtp_plus_1": True,
            "proves_subgroup_energy_bound": True,
            "proves_deployed_arc_incomplete": True,
            "proves_incomplete_GP_G_le_sqrtp": False,
            "proves_S_le_Bstar_deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "energy_id": lemma_energy_id(),
            "energy_LinfL2": lemma_energy_LinfL2(),
            "subgroup_G": lemma_subgroup_G(),
            "subgroup_energy": lemma_subgroup_energy(),
            "deployed_incomplete": lemma_deployed_incomplete(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"numpy_fft": "G and energy", "python_nt": "subgroups / GP"},
        "impact_on_program": {
            "closed": (
                "E_+=p^{-1} sum|G|^4; subgroup |G|<=sqrt(p)+1; "
                "deployed arc flagged incomplete"
            ),
            "wall": "incomplete GP G-bound and/or soft-B max|S|<=B_*",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    cen = cert["toy_suite"]["census"]
    d = cert["deployed"]
    sub_lines = []
    for r in cert["toy_suite"]["sub_rows"][:10]:
        sub_lines.append(
            f"| {r['p']} | {r['t']} | {r['Gmax']:.2f} | {r['sqrt_p']:.2f} | "
            f"{r['Gmax']/r['sqrt_p']:.2f} | {r['E_plus']:.1f} | {r['E_over_t2']:.2f} |"
        )
    sub_tbl = "\n".join(sub_lines)
    inc_lines = []
    for r in cert["toy_suite"]["inc_rows"]:
        inc_lines.append(
            f"| {r['p']} | {r['t']} | {r['Gmax']:.2f} | {r['sqrt_p']:.2f} | "
            f"{r['Gmax']/r['sqrt_p']:.2f} | {r['E_plus']:.1f} | "
            f"{'Y' if r['Gmax_le_sqrtp_plus_1'] else 'n'} |"
        )
    inc_tbl = "\n".join(inc_lines)
    return f"""# KB-MCA Route-D v65: energy via `|G|^4`; subgroup `|G|≤√p+1`

Status: **energy identity + subgroup Gauss bound PROVED**; incomplete GP / soft-B
still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Energy identity (PROVED, any t-set)

```text
G(α) = sum_{{x in S}} psi(α x)
r(s) = |S ∩ (s-S)|            (ordered pair count)
E_+(S) = sum_s r(s)^2 = p^{{-1}} sum_α |G(α)|^4
```

## L∞/L2 energy bound (PROVED)

```text
E_+(S) <= t^2 ( t^2 + (p-t)^2 ) / p
```

## Multiplicative subgroup (PROVED)

If `H ≤ F_p^*` has order `t | (p-1)` and `a ≠ 0`:

```text
|sum_{{x in H}} psi(a x)| <= sqrt(p) + t/(p-1) <= sqrt(p) + 1
E_+(H) <= t^4/p + (sqrt(p)+1)^4
```

Proof: expand `1_H` in multiplicative characters trivial on `H`; Gauss sums.

## Deployed geometry (PROVED)

```text
n = 2^21 | (p-1),   n' = 1183520 < n
residual arc = length-n' *prefix* of mu_n  (incomplete GP)
```

Subgroup bound applies to **full** order-`t` subgroups, not automatically to
the incomplete prefix. Soft-B bar remains `B_* = √(2 H2) ≈ {d['B_star']:.1f}`.

## CAS

### Full subgroups

| p | t | max|G| | √p | ratio | E_+ | E_+/t² |
|---|---:|---:|---:|---:|---:|---:|
{sub_tbl}

### Incomplete GP prefixes (empirical)

| p | t | max|G| | √p | ratio | E_+ | ≤√p+1? |
|---|---:|---:|---:|---:|---:|---|
{inc_tbl}

- energy id max err = {cen['max_energy_id_err']:.1e}
- subgroup max G/√p = {cen['max_sub_Gmax_over_sqrtp']:.2f}
- incomplete max G/√p = {cen['max_inc_Gmax_over_sqrtp']:.2f}
- fraction incomplete with Gmax≤√p+1 = {cen['frac_inc_Gmax_le_sqrtp_plus_1']:.2f}

## Link

v64: e=3 `|All| ≤ √(E_+ p t)`; soft-B needs `max|S|≤B_*` at deployed.  
v65: controls `E_+` via `|G|^4` and proves the √p-law on **full** subgroups.  
Next: incomplete prefix estimates, or a direct soft-B attack on free-1 highs.

## OPEN

1. `|G|` for incomplete GP of length `n'` inside `mu_n` (deployed).  
2. `max|S| ≤ B_* ≈ {d['B_star']:.0f}` at deployed `(n',e)`.  
3. Alternate `|R2|≤e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v65.py --check
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
        "# kb-qatom-route-d-v65\n\n"
        "Additive energy via |G|^4; subgroup |G|<=sqrt(p)+1.\n"
    )
    REPORT_PATH.write_text(
        f"# v65 report\n\nstatus: {cert['status']}\n"
        f"energy identity: PROVED\n"
        f"subgroup |G|<=sqrt(p)+1: PROVED\n"
        f"OPEN incomplete GP / soft-B: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  E_+ = p^{-1} sum |G|^4: PROVED")
    print("  E_+ <= t^2(t^2+(p-t)^2)/p: PROVED")
    print("  subgroup |G| <= sqrt(p)+1: PROVED")
    print("  deployed arc incomplete (n'<n): PROVED fact")
    print(
        f"  CAS: sub={cen['n_sub']}; inc={cen['n_inc']}; "
        f"sub G/sqrtp max={cen['max_sub_Gmax_over_sqrtp']:.2f}; "
        f"inc G/sqrtp max={cen['max_inc_Gmax_over_sqrtp']:.2f}; "
        f"inc <=sqrtp+1 frac={cen['frac_inc_Gmax_le_sqrtp_plus_1']:.2f}; "
        f"B_*={cen['B_star']:.1f}"
    )
    print("  OPEN: incomplete GP |G|; max|S|<=B_* at deployed")


if __name__ == "__main__":
    main()
