#!/usr/bin/env python3
"""KB-MCA Route-D v51: prove U2e for all e (char ≠ 2) — close conditional of v50.

Proved:
  (1) Free-1 factorization form: U⊔V=W free-1 ⇔ monic f_U, f_V of deg e with
      f_U − f_V constant and f_U f_V = P_W := ∏_{w∈W}(X−w).
  (2) Write f_U = R+α, f_V = R+β with R monic deg e, R(0-coeff)=0
      (constant absorbed into α,β). Then
        R² + s R + p = P_W,  s=α+β, p=αβ.
  (3) Triangular recovery (char ≠ 2): coeffs of X^{2e−1},…,X^{e+1} in R²
      determine r_{e−1},…,r_1 uniquely from P_W. So R is unique for each W.
  (4) Coeff of X^e then determines s uniquely; lower degrees are existence
      constraints; degree 0 determines p. Quadratic T²−sT+p has at most two
      roots α,β ⇒ at most one unordered free-1 bipartition of W.
  (5) U2e PROVED for all e≥2 over fields of char ≠ 2 (any distinct 2e-set).
  (6) Unconditional (v50 conditional now theorem):
        H_*^pre(t,e) ≤ binom(t, 2e).
  (7) Deployed arithmetic (v50): binom(2e+s,s) ≤ H2 ⇔ s≤2, so
        t ≤ 2e+2  ⇒  H_*^pre(t,e) ≤ H2.
  (8) e=2 still closed by |H|≤p≤H2 independently of t.

OPEN:
  Residual pure-untyped windows may have t = min(C) up to n' ≫ 2e+2.
  Need residual t≤2e+2, or a large-t bound better than C(t,2e)
  (e.g. using GP structure / roots-of-unity, not bare set combinatorics).

Does NOT prove H_*^pre ≤ H2 at full deployed t-range; does NOT prove A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v51.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v51"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v51.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v51.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v51.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
E_P = E * P
N_PRIME = A + E
H2 = E_P // (2 * 31 * 30)
T_MIN = 2 * E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def binom_int(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c


def lemma_U2e() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "U2e_unique_free1_bipartition_char_ne_2",
        "statement": (
            "Let F be a field of char ≠ 2 and W ⊂ F a set of 2e distinct "
            "elements (e≥2). There is at most one unordered bipartition "
            "W = U ⊔ V with |U|=|V|=e such that the monic polynomials "
            "f_U, f_V have equal coefficients of X^{e−1},…,X^1 "
            "(free-1 / equal monic high)."
        ),
        "proof": [
            "Free-1 ⇔ f_U − f_V is constant and both monic of deg e.",
            "Write f_U = R+α, f_V = R+β with R monic deg e and constant "
            "term of R equal to 0 (absorb constants into α,β).",
            "Then R² + s R + p = P_W with s=α+β, p=αβ, P_W=∏(X−w).",
            "Char ≠ 2: the map R ↦ (coeffs of X^{2e−1},…,X^{e+1} in R²) is "
            "triangular with diagonal 2 on unknowns r_{e−1},…,r_1, hence "
            "R is uniquely determined by P_W (when a free-1 bip exists, "
            "and as a candidate in general).",
            "Coeff of X^e: s = p_e − [X^e](R²) is unique.",
            "Degrees e−1..1 are constraints; deg 0 fixes p.",
            "α,β are the ≤2 roots of T² − s T + p; the unordered pair "
            "{R+α, R+β} is unique ⇒ unique root-set bipartition.",
            "If α=β then f_U=f_V, so multiset of roots coincides; cannot "
            "partition 2e distinct elements into two equal e-sets.",
        ],
        "deployed_char": f"p={P} odd prime ⇒ char ≠ 2",
    }


def lemma_Hpre_Ct2e() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Hstar_pre_le_binom_t_2e",
        "statement": (
            "H_*^pre(t,e) ≤ binom(t, 2e) for all t,e (char ≠ 2). "
            "Formerly conditional on U2e in v50; U2e now proved."
        ),
        "proof": [
            "Each multipad high H has |F_H|≥2; pick any free-1 pair (U,V).",
            "W=U∪V has size 2e and admits a free-1 bipartition with high H.",
            "By U2e this high is the unique free-1 high for W, so H ↦ W injects "
            "multipad highs into 2e-subsets of I_t.",
            "Hence |H| ≤ binom(t,2e).",
        ],
    }


def lemma_t_le_2e2() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "t_le_2e_plus_2_implies_Hpre_le_H2",
        "statement": (
            f"Deployed e={E}: if t≤2e+2 then H_*^pre(t,e) ≤ binom(t,2e) ≤ "
            f"binom(2e+2,2) = {binom_int(2*E+2, 2)} ≤ H2 = {H2}."
        ),
        "proof": [
            "H* ≤ C(t,2e) by previous lemma.",
            "t≤2e+2 ⇒ C(t,2e)=C(t,t−2e)≤C(2e+2,2) (since t−2e≤2).",
            "Direct: C(2e,0)=1, C(2e+1,1)=2e+1, C(2e+2,2)≤H2; C(2e+3,3)>H2.",
        ],
        "values": {
            "C_2e_2": binom_int(2 * E + 2, 2),
            "C_2e_3": binom_int(2 * E + 3, 3),
            "H2": H2,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_residual_t_or_large_t_bound",
        "statement": (
            "Residual pure-untyped coext windows have t=min(C) ∈ [2e, n']. "
            f"Deployed n'={N_PRIME} gives binom(n',2e) ≫ H2. "
            "Need either (i) residual t ≤ 2e+2, or (ii) a GP/arc bound "
            "H_*^pre(t,e) ≪ binom(t,2e) for large t with k=⌊t/e⌋≤17."
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


def monic_poly_low(roots: list[int], p: int) -> list[int]:
    """Monic ∏(X−v), coefficients low-to-high."""
    poly = [1]
    for v in roots:
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] + c * ((-v) % p)) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


def poly_mul_low(a: list[int], b: list[int], p: int) -> list[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return r


def reconstruct_R(P: list[int], e: int, p: int) -> list[int]:
    """Unique monic R of deg e with R_0=0 from high half of P (char ≠ 2)."""
    ensure(len(P) == 2 * e + 1 and P[2 * e] == 1, "P monic 2e")
    ensure(p % 2 == 1, "char 2")
    r = [0] * (e + 1)
    r[e] = 1
    inv2 = pow(2, -1, p)
    for k in range(1, e):
        deg = 2 * e - k
        known = 0
        for i in range(0, e + 1):
            j = deg - i
            if 0 <= j <= e and i != e - k and j != e - k:
                known = (known + r[i] * r[j]) % p
        r[e - k] = ((P[deg] - known) % p) * inv2 % p
    ensure(r[0] == 0, "R const forced 0 by high system? may be nonzero if inconsistent")
    # Actually high system never constrains r[0]; we force r[0]=0 by convention.
    r[0] = 0
    return r


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


def free1_bipartitions_of_W(W, vals, p, e):
    W = list(W)
    highs = []
    seen: set[Any] = set()
    for U in itertools.combinations(W, e):
        Uf = frozenset(U)
        Vf = frozenset(W) - Uf
        key = tuple(sorted((tuple(sorted(Uf)), tuple(sorted(Vf)))))
        if key in seen:
            continue
        seen.add(key)
        if monic_high(sorted(Uf), vals, p, e) == monic_high(sorted(Vf), vals, p, e):
            highs.append(monic_high(sorted(Uf), vals, p, e))
    return highs


def verify_R_on_free1(W, vals, p, e) -> bool:
    """If free-1 bip exists, reconstructed R matches common high of f_U, f_V."""
    W = list(W)
    for U in itertools.combinations(W, e):
        Uf = frozenset(U)
        Vf = frozenset(W) - Uf
        if tuple(sorted(Uf)) > tuple(sorted(Vf)):
            continue
        if monic_high(Uf, vals, p, e) != monic_high(Vf, vals, p, e):
            continue
        fU = monic_poly_low([vals[i] for i in Uf], p)
        fV = monic_poly_low([vals[i] for i in Vf], p)
        Pw = monic_poly_low([vals[i] for i in W], p)
        R = reconstruct_R(Pw, e, p)
        ensure(R[0] == 0, "R0")
        for k in range(1, e + 1):
            ensure(fU[k] == fV[k] == R[k], f"match k={k}")
        ensure(poly_mul_low(fU, fV, p) == Pw, "product")
        # s unique from deg e
        R2 = poly_mul_low(R, R, p)
        while len(R2) < 2 * e + 1:
            R2.append(0)
        s = (Pw[e] - R2[e]) % p
        ensure((fU[0] + fV[0]) % p == s, "s=α+β")
        return True
    return False


def Hpre_maps(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))

    nH = 0
    W_to_H: dict[Any, Any] = {}
    inject_ok = True
    for h, us in by.items():
        if len(us) < 2:
            continue
        nH += 1
        us_s = sorted(us)
        U, V = us_s[0], us_s[1]
        W = frozenset(U) | frozenset(V)
        if W in W_to_H and W_to_H[W] != h:
            inject_ok = False
        W_to_H[W] = h

    max_bip = 0
    multi_bip = 0
    checked_W = 0
    free1_R_ok = 0
    if binom_int(t, 2 * e) <= 4000 and t >= 2 * e:
        for W in itertools.combinations(range(t), 2 * e):
            checked_W += 1
            hs = free1_bipartitions_of_W(W, vals, p, e)
            max_bip = max(max_bip, len(hs))
            if len(hs) > 1:
                multi_bip += 1
            if len(hs) == 1 and verify_R_on_free1(W, vals, p, e):
                free1_R_ok += 1

    Ct2e = binom_int(t, 2 * e) if t >= 2 * e else 0
    return {
        "p": p,
        "n": n,
        "e": e,
        "t": t,
        "nH": nH,
        "pair_map_injective": inject_ok,
        "nH_le_Ct2e": nH <= Ct2e if t >= 2 * e else True,
        "Ct2e": Ct2e,
        "max_bip_per_W": max_bip,
        "multi_bip_W": multi_bip,
        "checked_W": checked_W,
        "free1_R_verified": free1_R_ok,
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "p odd")
    ensure(P <= H2, "p<=H2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(binom_int(2 * E + 2, 2) <= H2, "s2")
    ensure(binom_int(2 * E + 3, 3) > H2, "s3")

    # Algebraic identity: any free-1 bip on toys reconstructs R
    rows = []
    total_free1_R = 0
    for p, n in [(17, 16), (31, 30), (61, 60), (73, 72), (101, 100)]:
        for e in [2, 3, 4]:
            for t in range(2 * e, min(n, 3 * e + 4) + 1):
                if math.comb(t, e) > 25000:
                    continue
                r = Hpre_maps(p, n, e, t)
                ensure(r["pair_map_injective"], "inject")
                ensure(r["nH_le_Ct2e"], "Ct2e")
                ensure(r["multi_bip_W"] == 0, "U2e toys")
                total_free1_R += r["free1_R_verified"]
                rows.append(r)

    ensure(len(rows) >= 20, "rows")
    ensure(total_free1_R >= 10, "R verify count")

    # Direct e=2 classic uniqueness still holds
    vals = domain_vals(17, 16)
    for W in itertools.combinations(range(12), 4):
        ensure(len(free1_bipartitions_of_W(W, vals, 17, 2)) <= 1, "e2")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "all_pair_map_injective": True,
            "all_nH_le_Ct2e": True,
            "all_bip_unique": True,
            "free1_R_verified_total": total_free1_R,
            "max_nH": max(r["nH"] for r in rows),
        },
        "deployed_binom": {
            "C_2e2_2": binom_int(2 * E + 2, 2),
            "C_2e3_3": binom_int(2 * E + 3, 3),
            "H2": H2,
            "C_nprime_2e_digits": len(str(binom_int(N_PRIME, min(2 * E, 40)))),  # symbolic note
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v51",
        "title": "U2e PROVED (char≠2) ⇒ H_*^pre ≤ C(t,2e) unconditional",
        "status": "U2E_PROVED_LARGE_T_OPEN",
        "claims": {
            "proves_U2e_all_e_char_ne_2": True,
            "proves_Hpre_le_Ct2e_unconditional": True,
            "proves_t_le_2e_plus_2_implies_H2": True,
            "proves_e2_Hpre_le_H2_all_t": True,
            "proves_residual_t_le_2e_plus_2": False,
            "proves_Hpre_deployed_full_window_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "n_prime": N_PRIME,
            "t_min": T_MIN,
            "t_max": N_PRIME,
            "H2": H2,
            "C_2e_plus_2_choose_2": binom_int(2 * E + 2, 2),
            "C_2e_plus_3_choose_3": binom_int(2 * E + 3, 3),
            "free_core": FREE_CORE,
            "p_odd": True,
        },
        "lemmas": {
            "U2e": lemma_U2e(),
            "Hpre_Ct2e": lemma_Hpre_Ct2e(),
            "t_gate": lemma_t_le_2e2(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "closed": "U2e + C(t,2e) bound; t≤2e+2 residual gate",
            "gaps": "control residual min(C) or GP large-t H_*^pre bound",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    db = cert["toy_suite"]["deployed_binom"]
    rows = cert["toy_suite"]["rows"]
    sample = sorted(rows, key=lambda r: (-r["e"], -r["t"]))[:16]
    tbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['t']} | {r['nH']} | {r['Ct2e']} | "
        f"{r['multi_bip_W']} | {r['free1_R_verified']} |"
        for r in sample
    )
    return f"""# KB-MCA Route-D v51: U2e PROVED (char ≠ 2)

Status: **U2e PROVED** for all e≥2 in char ≠ 2; hence
`H_*^pre(t,e) ≤ binom(t,2e)` **unconditional**. Full deployed window still OPEN.

## Theorem U2e

Let `F` be a field of characteristic ≠ 2, `e≥2`, and `W ⊂ F` a set of `2e`
distinct elements. There is **at most one** unordered bipartition
`W = U ⊔ V` with `|U|=|V|=e` such that monic `f_U, f_V` share coefficients of
`X^{{e−1}},…,X^1` (free-1 / equal monic high).

### Proof

1. Free-1 ⇔ `f_U − f_V` is constant, both monic of degree `e`.
2. Write `f_U = R+α`, `f_V = R+β` with `R` monic degree `e` and constant term
   of `R` equal to 0. Then
   ```text
   R² + s R + p = P_W,   s=α+β, p=αβ,   P_W = ∏_{{w∈W}}(X−w).
   ```
3. **Triangular recovery (char ≠ 2).** Coefficients of `X^{{2e−1}},…,X^{{e+1}}`
   in `R²` form a triangular system with diagonal factor `2` in the unknowns
   `r_{{e−1}},…,r_1`. Hence `R` is uniquely determined by `P_W`.
4. Coefficient of `X^e` fixes `s` uniquely; degrees `e−1..1` are existence
   constraints; degree 0 fixes `p`.
5. `α,β` are the ≤2 roots of `T² − s T + p`. The unordered pair `{{R+α,R+β}}`
   is unique, so the root-set bipartition is unique.
6. `α=β` forces `f_U=f_V`, impossible for a partition of `2e` distinct points.

Deployed KoalaBear `p = 2^31 − 2^24 + 1` is an odd prime, so char ≠ 2.

## Corollary (was v50 conditional)

```text
H_*^pre(t,e)  ≤  binom(t, 2e)
```

Each multipad high injects into its free-1 pair-cover `W = U∪V` (size `2e`)
by U2e uniqueness.

## Arithmetic residual gate (deployed)

| s | binom(2e+s, s) | ≤ H2? |
|---:|---:|---|
| 2 | {db['C_2e2_2']} | yes |
| 3 | {db['C_2e3_3']} | **no** |

```text
t ≤ 2e+2  ⇒  H_*^pre(t,e) ≤ H2
```

e=2: already `H_*^pre(t,2) ≤ p ≤ H2` for all t (v48/v50).

## Residual card path

```text
pure-untyped coext residual with min(C) ≤ 2e+2
  ⇒  H_*^pre ≤ H2  ⇒  residual free-1 card (v45–v47)
```

OR improve large-t bound using roots-of-unity / GP structure.

## Toys

| p | e | t | nH | C(t,2e) | multi bip | R-verified free1 |
|---|---:|---:|---:|---:|---:|---:|
{tbl}

Census: rows={cen['n_rows']}; all bip unique; all nH≤C(t,2e);
free1 R-reconstructions verified={cen['free1_R_verified_total']}.

## OPEN

1. Force residual `t = min(C) ≤ 2e+2`, **or**
2. Bound `H_*^pre(t,e)` for `t ≤ n'={d['n_prime']}` with `k=⌊t/e⌋≤17`
   tighter than `binom(t,2e)`.
3. `A_SP ≤ t·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v51.py --check
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
        "# kb-qatom-route-d-v51\n\n"
        "U2e PROVED (char != 2) => H_*^pre <= C(t,2e) unconditional.\n"
    )
    REPORT_PATH.write_text(
        f"# v51 report\n\nstatus: {cert['status']}\n"
        f"U2e: PROVED\n"
        f"Hpre <= C(t,2e): PROVED unconditional\n"
        f"OPEN residual t or large-t GP bound: True\n"
    )
    cen = cert["toy_suite"]["census"]
    db = cert["toy_suite"]["deployed_binom"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  U2e (unique free-1 bipartition, all e, char≠2): PROVED")
    print("  H_*^pre(t,e) ≤ C(t,2e): PROVED (unconditional)")
    print(f"  t≤2e+2 ⇒ ≤H2 (C(2e+2,2)={db['C_2e2_2']}): PROVED")
    print(
        f"  toys: {cen['n_rows']} rows; bip unique; nH≤C; "
        f"R-verified free1={cen['free1_R_verified_total']}"
    )
    print("  OPEN: residual t≤2e+2 or large-t GP bound ≪ C(t,2e)")


if __name__ == "__main__":
    main()
