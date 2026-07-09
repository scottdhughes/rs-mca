#!/usr/bin/env python3
"""KB-MCA Route-D v71: full support of P_e (q-binomial); sparse product wall.

After v70 (G = P_e H multipad form), control the divisor P_e.

Proved:
  (1) q-binomial formula. Let omega in F_p have order n, and 1 <= e < n. Set
        R = {1, omega, omega^2, ..., omega^{e-1}}.
      The elementary symmetric sums e_j = e_j(R) satisfy
        e_j = omega^{j(j-1)/2} * binom(e,j)_omega
      where the Gaussian binomial is
        binom(e,j)_omega = prod_{i=0}^{j-1} (omega^{e-i}-1)/(omega^{i+1}-1)
      for 0 < j <= e, and e_0 = 1.
  (2) Nonvanishing. For 0 <= j <= e and e < n = ord(omega):
        omega^m != 1 for all m = 1,...,e  (since e < n),
      so every numerator and denominator in (1) is nonzero in F_p. Hence
        e_j != 0 for all j = 0,...,e.
  (3) Full support of P_e. With
        P_e(X) = prod_{k=0}^{e-1} (X - omega^k)
               = sum_{j=0}^e (-1)^{e-j} e_{e-j} X^j,
      (2) => every coefficient of P_e is nonzero: supp(P_e) = e+1 = deg(P_e)+1.
  (4) Multipad product constraint (v70+v69). Any free-1 multipad gives
        G = P_e * H  with  supp(G) = 2e,  coeffs(G) in {-1,0,1},
        deg G in [e, t-1],  deg H = deg G - e.
      In particular H cannot be 0, and for e >= 2 one has 2e > e+1 = supp(P_e),
      so G is a proper multiple (deg H >= 0 always; constant H gives
      supp(G)=e+1 != 2e for e!=1, hence deg H >= 1 for e>=2).
  (5) Generic support gap (structural, CAS-backed). For random H of degree d,
      supp(P_e H) is typically ~ e+d+1, which exceeds 2e once d > e.
      Multipads (when they exist) achieve the atypical value supp=2e with large d,
      i.e. extreme cancellation. Deployed e ~ 6.7e4 forces any multipad H to
      cancel from expected support ~ e + (deg G - e) + 1 = deg G + 1 <= t
      down to 2e — a cancellation of size ~ t - 2e at max degree.

CAS:
  (6) Formula (1) matches direct P_e; all e_j nonzero for tested e < n.
  (7) supp(P_e)=e+1 always on tested rows e=2..19.
  (8) Multipad G always supp=2e; random P_e*H support grows with deg H.
  (9) No multipad with deg H = 0 (constant) for e>=2.

OPEN:
  Prove that no H in F_p[X] yields G = P_e H with supp(G)=2e and
  coeffs in {-1,0,1} balanced (e plus, e minus) for A,B subset {0..n'-1}
  at deployed — or SoftB.

Does NOT claim deployed injectivity / A_SP.

  python3 experimental/scripts/verify_kb_qatom_route_d_v71.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v71"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v71.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v71.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v71.report.md"
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


def lemma_qbinomial() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Pe_coeffs_via_gaussian_binomial",
        "statement": (
            "For ord(omega)=n and 1<=e<n: e_j(1,omega,...,omega^{e-1}) = "
            "omega^{j(j-1)/2} * binom(e,j)_omega with the usual Gaussian product."
        ),
        "proof": [
            "Standard q-identity for elementary symmetric means of a geometric "
            "progression 1, q, ..., q^{e-1} at q=omega (see e.g. q-binomial theorem).",
            "Verified against direct expansion of P_e on toys.",
        ],
    }


def lemma_nonvanishing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "gaussian_binomial_nonzero_when_e_lt_ord",
        "statement": (
            "If ord(omega)=n and 1<=e<n then binom(e,j)_omega != 0 in F_p "
            "for all 0<=j<=e, hence all e_j != 0."
        ),
        "proof": [
            "binom(e,j)_omega = prod_{i=0}^{j-1} (omega^{e-i}-1)/(omega^{i+1}-1).",
            "For 1<=m<=e<n: n does not divide m => omega^m != 1.",
            "All factors nonzero (and invertible) in F_p.",
            "e_j = omega^{j(j-1)/2} * binom(e,j)_omega with omega power nonzero.",
        ],
    }


def lemma_full_support() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Pe_full_support",
        "statement": (
            "P_e(X)=prod_{k=0}^{e-1}(X-omega^k) has all e+1 coefficients nonzero "
            "whenever 1<=e<ord(omega)."
        ),
        "proof": [
            "P_e = sum_{j=0}^e (-1)^{e-j} e_{e-j} X^j.",
            "e_m != 0 for all m=0..e by nonvanishing lemma.",
        ],
    }


def lemma_multipad_support_constraint() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_requires_cancelled_multiple",
        "statement": (
            "Any free-1 multipad G=P_e H has supp(G)=2e > e+1=supp(P_e) for e>=2, "
            "hence deg H >= 1 and G is a cancelled proper multiple of P_e."
        ),
        "proof": [
            "v69: multipads disjoint => supp(G)=2e.",
            "v70: G=P_e H.",
            "Full support P_e: constant H => G is scalar * P_e => supp=e+1.",
            "e>=2 => e+1 < 2e => H nonconstant (deg H >= 1).",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_no_cancelled_multiple_supp_2e_deployed",
        "statement": (
            f"No H gives supp(P_e H)=2e with multipad sign pattern on "
            f"{{0..n'-1}} at e={E}, n'={N_PRIME}."
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


def gauss_binom(e: int, j: int, w: int, p: int) -> int:
    if j < 0 or j > e:
        return 0
    if j == 0:
        return 1
    num = 1
    for i in range(j):
        num = num * ((pow(w, e - i, p) - 1) % p) % p
        den = (pow(w, i + 1, p) - 1) % p
        ensure(den % p != 0, "den")
        num = num * pow(den, -1, p) % p
    return num


def e_j_formula(e: int, j: int, w: int, p: int) -> int:
    if j < 0 or j > e:
        return 0
    if j == 0:
        return 1
    return gauss_binom(e, j, w, p) * pow(w, j * (j - 1) // 2, p) % p


def build_Pe(om: int, e: int, p: int) -> list[int]:
    poly = [1]
    for k in range(e):
        root = pow(om, k, p)
        new = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            new[j] = (new[j] - (root * c) % p) % p
            new[j + 1] = (new[j + 1] + c) % p
        poly = new
    return poly


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


def supp(poly: list[int], p: int | None = None) -> int:
    if p is None:
        return sum(1 for c in poly if c != 0)
    return sum(1 for c in poly if c % p != 0)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % p
    return out


def formula_row(p: int, n: int, e: int) -> dict[str, Any]:
    ensure((p - 1) % n == 0, "n|p-1")
    ensure(1 <= e < n, "e range")
    g = prim_root(p)
    w = pow(g, (p - 1) // n, p)
    pe = build_Pe(w, e, p)
    # check formula: pe[j] = (-1)^{e-j} e_{e-j}
    formula_ok = True
    all_ej_nz = True
    for j in range(e + 1):
        ej = e_j_formula(e, e - j, w, p)
        if ej % p == 0:
            all_ej_nz = False
        expected = ((-1) ** (e - j) * ej) % p
        if pe[j] % p != expected:
            formula_ok = False
    s = supp(pe, p)
    return {
        "p": p,
        "n": n,
        "e": e,
        "supp_Pe": int(s),
        "full_support": bool(s == e + 1),
        "formula_ok": bool(formula_ok),
        "all_ej_nonzero": bool(all_ej_nz),
    }


def multipad_support_row(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(t)]
    pe = build_Pe(om, e, p)
    buckets: dict[tuple[int, ...], list[set[int]]] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        buckets[free1_X(monic_X(roots, p), e)].append(set(idxs))

    pair_supps: list[int] = []
    degHs: list[int] = []
    for lst in buckets.values():
        if len(lst) < 2:
            continue
        for A, B in itertools.combinations(lst, 2):
            coef = [0] * t
            for a in A:
                coef[a] += 1
            for b in B:
                coef[b] -= 1
            s = supp(coef)
            pair_supps.append(s)
            dG = max(i for i, c in enumerate(coef) if c != 0)
            degHs.append(dG - e)
            ensure(s == 2 * e, "multipad supp 2e")
            ensure(A.isdisjoint(B), "disjoint")
            if len(pair_supps) >= 20:
                break
        if len(pair_supps) >= 20:
            break

    return {
        "p": p,
        "t": t,
        "e": e,
        "supp_Pe": int(supp(pe, p)),
        "n_pairs_checked": len(pair_supps),
        "all_supp_2e": bool(all(s == 2 * e for s in pair_supps)) if pair_supps else True,
        "min_degH": int(min(degHs)) if degHs else None,
        "max_degH": int(max(degHs)) if degHs else None,
        "has_multipads": bool(len(pair_supps) > 0),
    }


def random_multiple_row(
    p: int, n: int, e: int, degH: int, trials: int = 25
) -> dict[str, Any]:
    g = prim_root(p)
    om = pow(g, (p - 1) // n, p)
    pe = build_Pe(om, e, p)
    rng = np.random.default_rng(0)
    supps = []
    for _ in range(trials):
        H = [int(rng.integers(0, p)) for _ in range(degH + 1)]
        if H[-1] % p == 0:
            H[-1] = 1
        prod = poly_mul(pe, H, p)
        supps.append(supp(prod, p))
    return {
        "p": p,
        "e": e,
        "degH": degH,
        "supp_Pe": int(supp(pe, p)),
        "min_supp": int(min(supps)),
        "max_supp": int(max(supps)),
        "med_supp": float(np.median(supps)),
        "two_e": int(2 * e),
        "min_ge_two_e": bool(min(supps) >= 2 * e),
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(E < N, "e < n deployed")
    ensure(FLOOR_NP == 17, "k")

    # deployed nonvanishing hypothesis applies: e < n
    ensure(E < N, "deployed e < ord")

    form_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in range(2, 16):
            if e >= n:
                continue
            r = formula_row(p, n, e)
            ensure(r["formula_ok"], f"formula {p},{e}")
            ensure(r["all_ej_nonzero"], f"ej {p},{e}")
            ensure(r["full_support"], f"full {p},{e}")
            form_rows.append(r)
    ensure(len(form_rows) >= 30, "form rows")

    mp_rows = []
    for p, n, t, e in [
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 21, 4),
        (61, 60, 21, 4),
    ]:
        if math.comb(t, e) > 40000:
            continue
        r = multipad_support_row(p, n, t, e)
        if r["has_multipads"]:
            ensure(r["all_supp_2e"], "2e")
            ensure(r["min_degH"] is not None and r["min_degH"] >= 1, "degH>=1")
        mp_rows.append(r)

    ensure(any(r["has_multipads"] for r in mp_rows), "some mp")

    rand_rows = []
    for p, n, e in [(61, 60, 3), (61, 60, 5), (101, 100, 4), (127, 126, 5)]:
        for degH in [0, 1, 2, 3, 5, 8]:
            rand_rows.append(random_multiple_row(p, n, e, degH))

    # constant H never hits supp 2e for e>=2
    for r in rand_rows:
        if r["degH"] == 0 and r["e"] >= 2:
            ensure(r["min_supp"] == r["e"] + 1, "const mult")
            ensure(r["min_supp"] != r["two_e"], "const != 2e")

    return {
        "status": "PASS",
        "form_rows": form_rows,
        "mp_rows": mp_rows,
        "rand_rows": rand_rows,
        "summary": {
            "n_form": len(form_rows),
            "n_mp": len(mp_rows),
            "n_rand": len(rand_rows),
            "all_Pe_full_support": True,
            "all_formula_ok": True,
            "all_multipad_supp_2e": True,
            "deployed_e": E,
            "deployed_n": N,
            "deployed_e_lt_n": True,
            "deployed_implies_Pe_full_support": True,
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "n": N,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "supp_Pe": E + 1,
            "multipad_supp": 2 * E,
            "note": (
                "P_e full support e+1 PROVED for e<n; multipad needs cancelled "
                "multiple with supp 2e; ban OPEN"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v71",
        "title": "P_e full support via q-binomial; cancelled multiple wall",
        "status": "PE_FULL_SUPPORT_PROVED_CANCELLED_MULTIPLE_OPEN",
        "claims": {
            "proves_Pe_qbinomial_formula": True,
            "proves_ej_nonzero_when_e_lt_ord": True,
            "proves_Pe_full_support": True,
            "proves_multipad_needs_degH_ge_1": True,
            "proves_no_cancelled_multiple_at_deployed": False,
            "proves_deployed_injectivity": False,
            "proves_SoftB_Deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "qbinomial": lemma_qbinomial(),
            "nonvanishing": lemma_nonvanishing(),
            "full_support": lemma_full_support(),
            "multipad_constraint": lemma_multipad_support_constraint(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "P_e / multipad support", "numpy": "random multiples"},
        "impact_on_program": {
            "closed": "P_e always full support e+1 (e < ord omega); multipads need cancelled H",
            "wall": "rule out supp(P_e H)=2e multipad sign pattern at deployed",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    form_lines = []
    for r in cert["toy_suite"]["form_rows"][:12]:
        form_lines.append(
            f"| {r['p']} | {r['e']} | {r['supp_Pe']} | "
            f"{'Y' if r['full_support'] else 'n'} | "
            f"{'Y' if r['formula_ok'] else 'n'} |"
        )
    form_tbl = "\n".join(form_lines)
    mp_lines = []
    for r in cert["toy_suite"]["mp_rows"]:
        mp_lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | {r['supp_Pe']} | "
            f"{r['n_pairs_checked']} | {r['min_degH']} | {r['max_degH']} |"
        )
    mp_tbl = "\n".join(mp_lines)
    rand_lines = []
    for r in cert["toy_suite"]["rand_rows"]:
        if r["degH"] in (0, 2, 5, 8):
            rand_lines.append(
                f"| {r['p']} | {r['e']} | {r['degH']} | {r['min_supp']} | "
                f"{r['med_supp']:.0f} | {r['max_supp']} | {r['two_e']} |"
            )
    rand_tbl = "\n".join(rand_lines)
    return f"""# KB-MCA Route-D v71: full support of `P_e`

Status: **`P_e` full support PROVED** (`e < ord ω`); multipad = cancelled multiple
with `supp=2e` **OPEN** to ban at deployed. Local on `scott/kb-route-d-T-bound`.

## q-binomial / nonvanishing (PROVED)

For `ord(ω)=n` and `1 ≤ e < n`:

```text
e_j(1,ω,...,ω^{{e-1}}) = ω^{{j(j-1)/2}} * binom(e,j)_ω
binom(e,j)_ω = prod_{{i=0}}^{{j-1}} (ω^{{e-i}}-1)/(ω^{{i+1}}-1)
```

All factors nonzero because `ω^m ≠ 1` for `1 ≤ m ≤ e < n`.  
Hence every `e_j ≠ 0`.

## Full support (PROVED)

```text
P_e(X) = prod_{{k=0}}^{{e-1}} (X - ω^k)
       = sum_j (-1)^{{e-j}} e_{{e-j}} X^j
supp(P_e) = e+1 = deg(P_e)+1
```

Deployed: `e={d['e']} < n={d['n']}` ⇒ **`supp(P_e) = e+1 = {d['supp_Pe']}`**.

## Multipad constraint (PROVED)

```text
G = P_e * H,   supp(G) = 2e = {d['multipad_supp']}
e >= 2  ⇒  2e > e+1  ⇒  deg H >= 1   (not a scalar multiple of P_e)
```

Multipads require **cancellation** in the product down to support `2e`.

## CAS

### P_e formula / support (sample)

| p | e | supp(P_e) | full? | formula? |
|---|---:|---:|---|---|
{form_tbl}

### Multipad G

| p | e | t | supp(P_e) | #pairs | min degH | max degH |
|---|---:|---:|---:|---:|---:|---:|
{mp_tbl}

### Random multiples (sample)

| p | e | degH | min supp | med | max | 2e |
|---|---:|---:|---:|---:|---:|---:|
{rand_tbl}

Random `P_e H` support grows with `degH`; multipads sit on the rare cancelled locus.

## Link

| item | status |
|---|---|
| G = P_e H structure | CLOSED (v70) |
| **P_e full support** | **CLOSED (v71)** |
| multipad needs degH≥1 | CLOSED (v71) |
| ban cancelled supp=2e at deployed | OPEN |
| SoftB fallback | OPEN |

## OPEN

Prove no `H` yields multipad-shaped `P_e H` on `{{0..n'-1}}` at deployed  
(or SoftB). Mathlib: Gaussian binomials / cyclotomic; AXLE for certs.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v71.py --check
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
        "# kb-qatom-route-d-v71\n\n"
        "P_e full support via q-binomial; multipad cancelled-multiple wall.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v71 report\n\nstatus: {cert['status']}\n"
        f"P_e full support: PROVED\n"
        f"multipad needs degH>=1: PROVED\n"
        f"OPEN cancelled supp=2e ban: True\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  e_j via Gaussian binomial, nonzero for e < ord(omega): PROVED")
    print("  P_e full support (e+1 nonzero coeffs): PROVED")
    print("  multipad => deg H >= 1 (cancelled multiple): PROVED")
    print(
        f"  CAS: form={s['n_form']}; mp={s['n_mp']}; rand={s['n_rand']}; "
        f"deployed supp(P_e)={E+1} vs multipad supp={2*E}"
    )
    print("  OPEN: ban cancelled P_e*H with supp=2e at deployed")


if __name__ == "__main__":
    main()
