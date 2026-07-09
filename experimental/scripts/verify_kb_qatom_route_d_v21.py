#!/usr/bin/env python3
"""KB-MCA Route-D v21: M_pad degree obstruction + side-pair → e·p path.

Continues v20 pair-injection attack with algebraic M_pad control.

Proved:
  (1) Multipad degree obstruction: if two distinct cores C,C' share the same
      free-1 CS sides (U,V) and Phi_w(C∪U)=Phi_w(C'∪U), then
        deg(Λ_C − Λ_{C'}) ≤ j − 2w − 2.
      Consequently if j < 2w+2 then Λ_C=Λ_{C'}, so M_pad(z) ≤ 1 for all z.
  (2) Deployed check: j=981104, 2w+2=134944, j > 2w+2 — obstruction does NOT
      force M_pad=1 at the KB row (degree room remains).
  (3) Payment path when M_pad≤1 (v20): N_ord=N_side; need inject free-1 CS
      ordered pairs into |L|≤t·p. Deployed t=e=w+1 so target size e·p.
  (4) Toy bank: j < 2w+2 ⇒ measured max M_pad=1; when j≥2w+2, M_pad can be ≥2
      (e.g. j=6,w=2: 2w+2=6). e·p-scale marks (min U mod e, c) not injective
      when M_pad≥2 or dense multi-pencils.
  (5) Refined OPEN: either prove M_pad≤1 by non-degree reasons at deployed
      (split constraints / residual), or inject CS pairs into e·p despite M_pad.

Does NOT prove M_pad≤1 deployed or e·p pair injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v21.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v21.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v21"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v21.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v21.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v21.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
PACK = 17
T_P = T * P


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def prim_root(p: int) -> int:
    fac: list[int] = []
    n = p - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no prim root")


def domain_vals(p: int, n: int) -> list[int]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    return [pow(om, i, p) for i in range(n)]


def monic_rev(pts: list[int], p: int) -> list[int]:
    poly = [1]
    for v in pts:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def phi_w(poly: list[int], w: int) -> tuple[int, ...]:
    return tuple(poly[1 : w + 1])


def deg_diff(pa: list[int], pb: list[int], deg: int, p: int) -> int:
    for k in range(deg - 1, -1, -1):
        idx = deg - k
        if idx < len(pa) and (pa[idx] - pb[idx]) % p != 0:
            return k
    return -1


def lemma_multipad_degree() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_core_difference_degree_bound",
        "statement": (
            "Suppose C ≠ C' are (j−e)-subsets, U,V are disjoint e-subsets with "
            "e=w+1, Λ_U−Λ_V = c ∈ F_p^×, and "
            "Phi_w(C∪U)=Phi_w(C'∪U)  (hence also = Phi_w(C∪V)=Phi_w(C'∪V)). "
            "Then deg(Λ_C − Λ_{C'}) ≤ j − 2w − 2."
        ),
        "proof": [
            "Λ_{C∪U} = Λ_C Λ_U and Λ_{C'∪U} = Λ_{C'} Λ_U (disjoint unions).",
            "Phi_w equal means the monic degree-j locators agree in coefficients of "
            "X^{j−1},…,X^{j−w}, so deg(Λ_C Λ_U − Λ_{C'} Λ_U) ≤ j−w−1.",
            "Factor: (Λ_C − Λ_{C'}) Λ_U has degree deg(Λ_C−Λ_{C'})+e.",
            "Hence deg(Λ_C−Λ_{C'})+e ≤ j−w−1.",
            "e=w+1 ⇒ deg(Λ_C−Λ_{C'}) ≤ j−w−1−(w+1) = j−2w−2.",
        ],
        "deployed": {
            "j": J,
            "w": W,
            "j_minus_2w_minus_2": J - 2 * W - 2,
            "two_w_plus_2": 2 * W + 2,
            "j_lt_2w_plus_2": J < 2 * W + 2,
        },
    }


def lemma_Mpad_one_if_j_small() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "M_pad_le_1_when_j_lt_2w_plus_2",
        "statement": (
            "If j < 2w+2, then M_pad(z) ≤ 1 for every z. "
            "Indeed j−2w−2 < 0 forces deg(Λ_C−Λ_{C'}) < 0, so Λ_C=Λ_{C'}."
        ),
        "proof": [
            "Apply multipad degree bound. Negative degree bound ⇒ difference zero.",
            "Distinct sets have distinct monic locators, contradiction unless C=C'.",
        ],
        "deployed_applies": J < 2 * W + 2,  # False
        "note": (
            "Deployed j ≫ 2w+2, so this sufficient condition does not fire. "
            "It does prove M_pad=1 on all shallow-w regimes with j < 2w+2."
        ),
    }


def lemma_deployed_room() -> dict[str, Any]:
    return {
        "status": "PROVED_BY_EXACT_INTEGER_ARITHMETIC",
        "name": "deployed_degree_room_for_multipad",
        "statement": (
            f"At deployed j={J}, w={W}: j−2w−2 = {J-2*W-2} ≥ 0 and "
            f"j ≥ 2w+2 = {2*W+2}. Degree obstruction does not rule out M_pad≥2."
        ),
        "proof": ["Direct comparison of integers."],
    }


def lemma_path_when_Mpad1() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "path_after_M_pad_one",
        "statement": (
            "If M_pad≤1 then N_ord=N_side (v20) and A_SP payment reduces to "
            "injecting ordered free-1 CS e-set pairs into a set of size ≤ t·p. "
            f"Deployed t=e=w+1, so the natural budget is e·p = t·p = {T_P}."
        ),
        "proof": ["v20 payment bridge + deployed t=e."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_M_pad_deployed_and_ep_injection",
        "statement": (
            "(1) Prove M_pad≤1 at deployed despite j>2w+2 (using split support "
            "constraints, residual, or first-match), OR bound M_pad by a small "
            "constant.\n"
            "(2) Inject free-1 CS ordered pairs (U,V) into size e·p "
            f"(={T_P} labels). Candidate form: one index in {{0..e−1}} and one "
            "field element — toys fail when multipads/dense pencils exist."
        ),
        "cas": (
            "Sage/msolve: ideal for monic Λ_C ≠ Λ_{C'} of degree j−e with "
            "(Λ_C−Λ_{C'})Λ_U of degree ≤ j−w−1 and both fully split — emptiness "
            "in residual regimes."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    for p, n, j, w in [
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 6, 4),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 8, 4),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
        (17, 16, 10, 2),
        (17, 16, 10, 3),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 4, 1),
        (17, 16, 4, 2),
    ]:
        e = w + 1
        if e >= j or math.comb(n, j) > 20000:
            continue
        vals = domain_vals(p, n)
        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        def split(S: frozenset[int]) -> tuple[Any, ...]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, tuple(polyU[1:-1]), polyU[-1], U, polyU

        max_Mpad = 1
        max_nord = 0
        max_core_diff_deg = -1
        pred = j < 2 * w + 2
        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                C, high, c0, U, pU = split(S)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, pU))
            pads: dict[Any, list] = defaultdict(list)
            nord = 0
            for _key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, pU = a
                        C2, V, c0V, pV = b
                        if (c0U - c0V) % p == 0:
                            continue
                        nord += 1
                        pads[(tuple(pU[1:-1]), c0U, c0V)].append(C)
            max_nord = max(max_nord, nord)
            if pads:
                # unique cores per side key
                for _sk, Cs in pads.items():
                    uniq = {tuple(sorted(C)) for C in Cs}
                    max_Mpad = max(max_Mpad, len(uniq))
                    if len(uniq) >= 2:
                        # measure core locator diff degree
                        C1 = frozenset(list(uniq)[0])
                        C2 = frozenset(list(uniq)[1])
                        pC1 = monic_rev([vals[i] for i in sorted(C1)], p)
                        pC2 = monic_rev([vals[i] for i in sorted(C2)], p)
                        mc = len(C1)
                        dd = deg_diff(pC1, pC2, mc, p)
                        max_core_diff_deg = max(max_core_diff_deg, dd)
                        ensure(dd <= j - 2 * w - 2, f"core deg {dd} > {j-2*w-2}")

        if pred:
            ensure(max_Mpad <= 1, f"j<2w+2 => Mpad1 got {max_Mpad} at j={j} w={w}")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "j_lt_2w2": pred,
                "max_Mpad": max_Mpad,
                "max_nord": max_nord,
                "max_core_diff_deg": max_core_diff_deg,
                "deg_bound": j - 2 * w - 2,
            }
        )

    ensure(any(r["j_lt_2w2"] and r["max_Mpad"] <= 1 for r in rows), "small j")
    ensure(any((not r["j_lt_2w2"]) and r["max_Mpad"] >= 2 for r in rows), "large multipad")
    ensure(J >= 2 * W + 2, "deployed room")
    ensure(J - 2 * W - 2 >= 0, "deployed deg bound nonneg")
    return {"status": "PASS", "rows": rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v21",
        "title": "M_pad degree obstruction j-2w-2; path to e·p pair injection",
        "status": "PARTIAL_MPAD_DEGREE",
        "claims": {
            "proves_multipad_degree_bound": True,
            "proves_M_pad_le_1_if_j_lt_2w_plus_2": True,
            "proves_M_pad_le_1_deployed": False,
            "proves_ep_pair_injection": False,
            "proves_A_SP_le_tp": False,
            "toy_confirms_degree_bound": True,
            "toy_confirms_j_lt_threshold": True,
        },
        "deployed": {
            "j": J,
            "w": W,
            "e": E,
            "t": T,
            "t_equals_e": T == E,
            "two_w_plus_2": 2 * W + 2,
            "j_minus_2w_minus_2": J - 2 * W - 2,
            "j_lt_2w_plus_2": J < 2 * W + 2,
            "t_p": T_P,
            "e_p": E * P,
        },
        "lemmas": {
            "multipad_degree": lemma_multipad_degree(),
            "M_pad_small_j": lemma_Mpad_one_if_j_small(),
            "deployed_room": lemma_deployed_room(),
            "path_Mpad1": lemma_path_when_Mpad1(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "win": "M_pad=1 for all rows with j<2w+2 (proved)",
            "deployed": "degree room j-2w-2>0; need non-degree multipad control or ep injection",
            "next": "Kill multipads by split/residual constraints, or e·p mark for CS pairs",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['j_lt_2w2']} | {r['max_Mpad']} | "
        f"{r['max_nord']} | {r['deg_bound']} | {r['max_core_diff_deg']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v21: M_pad degree obstruction

Status: `PARTIAL` — multipad **degree bound** PROVED; deployed `M_pad≤1` **OPEN**.

## Multipad degree bound (PROVED)

If two distinct cores share the same free-1 CS sides `(U,V)` and the same
fiber prefix via `C∪U`:

```text
deg(Λ_C − Λ_{{C'}})  ≤  j − 2w − 2
```

### Corollary

```text
j < 2w + 2   ⇒   M_pad(z) ≤ 1  for all z
```

## Deployed arithmetic

```text
j           = {d['j']}
2w+2        = {d['two_w_plus_2']}
j < 2w+2?   = {d['j_lt_2w_plus_2']}
j−2w−2      = {d['j_minus_2w_minus_2']}   (≥ 0: degree room for multipads)
t = e = w+1 = {d['t']}
t·p = e·p   = {d['t_p']}
```

So the **sufficient** condition `j<2w+2` does **not** apply to KB-MCA.
Multipads are not ruled out by degree alone.

## Payment path (still)

```text
M_pad ≤ 1  +  CS pairs inject into e·p
    ⇒  N_ord ≤ e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

## Toys

| j | w | j<2w+2? | max M_pad | max N_ord | deg bound | max core diff deg |
|---|---|---|---:|---:|---:|---:|
{tbl}

When `j<2w+2`, measured `M_pad=1`. When multipads exist, core diff degrees
respect `≤ j−2w−2`.

## OPEN

1. **Deployed M_pad≤1** by split-support / residual reasons beyond degree
2. **Inject free-1 CS pairs into e·p** (natural: index in `{{0..e−1}}` × F_p)

## CAS

Sage/msolve: system for two monic split cores with
`(Λ_C−Λ_{{C'}})Λ_U` of degree `≤ j−w−1` — restrict to regimes or find
structural constraints forcing `C=C'`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v21.py --check
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
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v21\n\nM_pad degree obstruction j-2w-2.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v21 report\n\nstatus: {cert['status']}\n"
        f"j_lt_2w_plus_2 deployed: {cert['deployed']['j_lt_2w_plus_2']}\n"
        f"j-2w-2: {cert['deployed']['j_minus_2w_minus_2']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  multipad deg(Λ_C-Λ_C') <= j-2w-2: PROVED")
    print(f"  j < 2w+2 => M_pad<=1: PROVED (deployed? {J < 2*W+2})")
    print(f"  deployed j-2w-2 = {J-2*W-2} (room for multipads)")
    print(f"  next: M_pad at deployed without degree, or CS pairs -> e*p")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
