#!/usr/bin/env python3
"""KB-MCA Route-D v78: multipad factorization identity; residual PR checklist.

Pushes the residual multipad-free hypothesis into a rigid polynomial form.

Proved:
  (1) Global multipad factorization. A free-1 multipad with root-value sets U,V
      (each size e, disjoint) and monic root polys f,g with f-g=delta != 0 gives
        R := U cup V,   |R|=2e,
        (phi - alpha)(phi - beta) = Pi_R(X) := prod_{r in R} (X - r),
      where phi is monic of degree e, phi(0)=0, {alpha,beta}={-const(f), -const(g)},
      alpha != beta. Equivalently Pi_R = phi^2 - (alpha+beta) phi + alpha beta.
  (2) Product of roots. Evaluating at 0: alpha beta = prod_{r in R} (-r) * (-1)^{0?}
      With monic Pi_R(0) = (-1)^{2e} prod r = prod r, and
      (phi-alpha)(phi-beta) at 0 equals alpha beta (since phi(0)=0), hence
        alpha beta = prod_{r in R} r.
  (3) Linear coeff. Writing phi = X^e + c_{e-1} X^{e-1} + ... + c_1 X,
      matching X^{2e-1} in the identity gives
        2 c_{e-1} = - sum_{r in R} r
      (p odd). So c_{e-1} = -p_1(R)/2.
  (4) Residual criterion (v77). Multipad-free on deployed arc => |T|=0.
      Identity (1) is the obstruction form any multipad must satisfy: Pi_R must be
      a constant-shift square in the monic degree-e pencil {phi - c}_c with phi(0)=0.
  (5) t=2e case recovery. If R is a full length-2e GP {omega^0,...,omega^{2e-1}},
      then Pi_R=P_{2e} and (1) reduces to the square-shift obstruction of v74.

CAS:
  (6) Identity (1)-(3) hold on all tested multipad pairs (poly equality, product,
      linear coeff).
  (7) No multipad at t<=2e (v74); multipads for larger t always satisfy (1)-(3).

OPEN (residual PR):
  Show no 2e-set R of the deployed arc values admits a factorization (1) with
  phi monic, deg e, phi(0)=0. Then multipad-free => |T|=0 PR.

Does NOT claim multipad-free at deployed.

  python3 experimental/scripts/verify_kb_qatom_route_d_v78.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v78"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v78.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v78.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v78.report.md"
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


def lemma_factorization() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_Pi_R_factorization",
        "statement": (
            "Multipad => (phi-alpha)(phi-beta)=Pi_R with phi monic deg e, "
            "phi(0)=0, alpha!=beta, |R|=2e subset of arc values."
        ),
        "proof": [
            "f=m+c0, g=m+c0', m has zero constant, phi:=m.",
            "Roots of f: phi=alpha:=-c0; roots of g: phi=beta:=-c0'.",
            "phi monic deg e (as m is), phi(0)=0.",
            "Pi_R=(phi-alpha)(phi-beta) as monic polys of deg 2e with same roots.",
        ],
    }


def lemma_product() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "alpha_beta_eq_prod_R",
        "statement": "alpha * beta = prod_{r in R} r.",
        "proof": [
            "Evaluate (phi-alpha)(phi-beta)=Pi_R at X=0: alpha beta = Pi_R(0).",
            "Pi_R(0)=(-1)^{2e} prod r = prod r.",
        ],
    }


def lemma_linear_coeff() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "c_em1_eq_minus_half_sum_R",
        "statement": (
            "With phi=X^e + c_{e-1} X^{e-1}+... and p odd: "
            "2 c_{e-1} = -sum_{r in R} r."
        ),
        "proof": [
            "Expand phi^2 - (alpha+beta) phi + alpha beta and Pi_R.",
            "Coeff of X^{2e-1}: 2 c_{e-1} on left, -sum r on right.",
        ],
    }


def lemma_residual() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_via_no_factorization",
        "statement": (
            "If no arc 2e-set R admits factorization (1), then multipad-free "
            "=> |T|=0 at deployed."
        ),
        "proof": ["Every multipad produces such an R and factorization (1)."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_no_factorization_on_deployed_arc",
        "statement": (
            f"No 2e-set R of the n'={N_PRIME}-arc admits "
            "(phi-alpha)(phi-beta)=Pi_R with phi monic deg e={E}, phi(0)=0."
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


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % p
    return out


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        out[i] = (ai - bi) % p
    while len(out) > 1 and out[-1] % p == 0:
        out.pop()
    return out


def poly_scale_add(
    a: list[int], sa: int, b: list[int], sb: int, p: int
) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        out[i] = (sa * ai + sb * bi) % p
    return out


def verify_identity_pair(
    ra: list[int], rb: list[int], p: int, e: int
) -> dict[str, Any]:
    fa = monic_X(ra, p)
    fb = monic_X(rb, p)
    ensure(fa[1:e] == fb[1:e], "free1")
    ensure(fa[e] % p == 1 and fb[e] % p == 1, "monic")
    # phi = m with zero constant = fa with const 0
    phi = fa[:]
    c0a = phi[0] % p
    phi[0] = 0
    c0b = fb[0] % p
    alpha = (-c0a) % p
    beta = (-c0b) % p
    ensure(alpha != beta, "alpha!=beta")
    # phi monic deg e: phi[e]==1, phi[0]==0
    ensure(phi[e] % p == 1, "phi monic")
    ensure(phi[0] % p == 0, "phi(0)=0 coeff")

    # Pi_R
    R = ra + rb
    Pi = monic_X(R, p)
    ensure(len(Pi) == 2 * e + 1, "deg Pi")

    # (phi - alpha)(phi - beta) = phi^2 - (a+b)phi + ab
    # phi - alpha as poly: subtract alpha from const
    phi_a = phi[:]
    phi_a[0] = (phi_a[0] - alpha) % p
    phi_b = phi[:]
    phi_b[0] = (phi_b[0] - beta) % p
    prod = poly_mul(phi_a, phi_b, p)
    # compare to Pi
    # pad
    while len(prod) < len(Pi):
        prod.append(0)
    while len(Pi) < len(prod):
        Pi.append(0)
    id_ok = all(prod[i] % p == Pi[i] % p for i in range(len(Pi)))

    # product of roots
    prod_r = 1
    for r in R:
        prod_r = (prod_r * r) % p
    ab = (alpha * beta) % p
    prod_ok = ab == prod_r

    # linear coeff: 2 c_{e-1} = -sum R
    # phi = X^e + c_{e-1} X^{e-1} + ... ; coeff of X^{e-1} is phi[e-1]
    c_em1 = phi[e - 1] % p
    sum_r = sum(R) % p
    inv2 = pow(2, -1, p)
    linear_ok = (2 * c_em1) % p == (-sum_r) % p
    # also c_em1 == -sum_r * inv2
    linear_ok = linear_ok and (c_em1 == ((-sum_r) * inv2) % p)

    return {
        "id_ok": bool(id_ok),
        "prod_ok": bool(prod_ok),
        "linear_ok": bool(linear_ok),
        "alpha": int(alpha),
        "beta": int(beta),
    }


def census(p: int, n: int, t: int, e: int, limit: int = 25) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    buckets: dict[tuple[int, ...], list[list[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        buckets[free1_X(monic_X(roots, p), e)].append(roots)

    n_ok = 0
    n_chk = 0
    for lst in buckets.values():
        if len(lst) < 2:
            continue
        for ra, rb in itertools.combinations(lst, 2):
            r = verify_identity_pair(ra, rb, p, e)
            ensure(r["id_ok"], "factorization id")
            ensure(r["prod_ok"], "prod")
            ensure(r["linear_ok"], "linear")
            n_ok += 1
            n_chk += 1
            if n_chk >= limit:
                break
        if n_chk >= limit:
            break

    n_mp_highs = sum(1 for v in buckets.values() if len(v) >= 2)
    return {
        "p": p,
        "t": t,
        "e": e,
        "n_checked": n_chk,
        "n_ok": n_ok,
        "n_mp_highs": n_mp_highs,
        "all_ok": bool(n_chk == n_ok),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "odd")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(N_PRIME > TWO_E, "n'>2e")

    rows = []
    for p, n, t, e in [
        (61, 60, 13, 3),
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 9, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 16, 3),
        (127, 126, 21, 4),
        (43, 42, 12, 3),
        (73, 72, 14, 4),
    ]:
        if t > n or math.comb(t, e) > 30000:
            continue
        r = census(p, n, t, e)
        if r["n_mp_highs"] == 0:
            # still ok - no multipads to check
            rows.append(r)
            continue
        ensure(r["all_ok"], f"id {p},{t},{e}")
        ensure(r["n_checked"] > 0, "checked")
        rows.append(r)

    ensure(any(r["n_checked"] > 0 for r in rows), "some multipads checked")

    # free at t=2e
    for p, n, e in [(61, 60, 3), (101, 100, 4)]:
        r = census(p, n, 2 * e, e, limit=5)
        ensure(r["n_mp_highs"] == 0, "t=2e free")

    return {
        "status": "PASS",
        "rows": rows,
        "summary": {
            "n_rows": len(rows),
            "n_with_checks": sum(1 for r in rows if r["n_checked"] > 0),
            "all_identities_ok": True,
            "deployed_n_prime": N_PRIME,
            "deployed_e": E,
            "residual_hypothesis": "no factorization (1) on deployed arc",
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "residual_closed": False,
            "criterion": "no multipad factorization on arc => |T|=0",
            "note": "Identity PROVED; deployed nonexistence OPEN (residual PR)",
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v78",
        "title": "Multipad factorization (phi-a)(phi-b)=Pi_R; residual PR form",
        "status": "FACTORIZATION_IDENTITY_PROVED_DEPLOYED_OPEN",
        "claims": {
            "proves_multipad_Pi_R_factorization": True,
            "proves_alpha_beta_eq_prod_R": True,
            "proves_linear_coeff_relation": True,
            "proves_residual_via_no_factorization": True,
            "proves_no_factorization_at_deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "factorization": lemma_factorization(),
            "product": lemma_product(),
            "linear": lemma_linear_coeff(),
            "residual": lemma_residual(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "multipad poly identity check"},
        "impact_on_program": {
            "closed": (
                "BOARD form: multipad <=> Pi_R=(phi-a)(phi-b) with phi(0)=0 monic deg e"
            ),
            "wall": "no such R on deployed arc",
            "residual_PR": "prove wall => |T|=0 certificate",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    lines = []
    for r in cert["toy_suite"]["rows"]:
        lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['n_mp_highs']} | "
            f"{r['n_checked']} | {'Y' if r['all_ok'] else 'n'} |"
        )
    tbl = "\n".join(lines)
    return f"""# KB-MCA Route-D v78: multipad factorization identity

Status: **factorization form PROVED**; deployed nonexistence **OPEN** (residual PR).  
Local on `scott/kb-route-d-T-bound`.

## BOARD identity (PROVED)

A free-1 multipad produces a 2e-set `R` of arc values and

```text
(phi - alpha)(phi - beta)  =  Pi_R(X)  :=  prod_{{r in R}} (X - r)

phi monic, deg e,  phi(0) = 0,  alpha != beta
```

### Corollaries (PROVED)

```text
alpha * beta  =  prod_{{r in R}} r
2 c_{{e-1}}   =  - sum_{{r in R}} r     (p odd)
```

where `phi = X^e + c_{{e-1}} X^{{e-1}} + ... + c_1 X`.

### Residual PR shape

```text
no arc 2e-set R admits this factorization
        =>  multipad-free
        =>  |T| = 0  ≤ H2     (v77)
```

## CAS

| p | e | t | #mp highs | #pairs checked | id OK? |
|---|---:|---:|---:|---:|---|
{tbl}

## Deployed

| | |
|---|---:|
| n' | {d['n_prime']} |
| e | {d['e']} |
| residual closed? | **no** (hypothesis open) |

## OPEN

Prove **no factorization** on the deployed arc — then open residual PR with `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v78.py --check
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
        "# kb-qatom-route-d-v78\n\n"
        "Multipad factorization (phi-a)(phi-b)=Pi_R; residual PR form.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v78 report\n\nstatus: {cert['status']}\n"
        f"factorization identity: PROVED\n"
        f"OPEN deployed nonexistence: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  (phi-a)(phi-b)=Pi_R with phi(0)=0: PROVED")
    print("  alpha*beta=prod R; 2 c_{e-1}=-sum R: PROVED")
    print("  residual PR form: no such R => |T|=0: PROVED")
    print(
        f"  CAS: rows={s['n_rows']}; with checks={s['n_with_checks']}; all id OK"
    )
    print("  OPEN: no factorization on deployed arc — then residual PR")


if __name__ == "__main__":
    main()
