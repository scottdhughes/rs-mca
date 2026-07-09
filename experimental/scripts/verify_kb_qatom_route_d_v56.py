#!/usr/bin/env python3
"""KB-MCA Route-D v56: free-1 multipads on GP — algebra + regime split.

Attacks |T| at large e after v55.  Tools: Python NT venv, Sage (power-sum
cross-check).  Wolfram CLI available; not required this packet.

Proved:
  (1) Free-1 monic high ⇔ equal power sums p_1..p_{e−1} of root values when
      Newton is invertible (in particular char p > e; deployed p ≫ e).
  (2) φ-formulation: fix high coeffs a=(a_{e−1},…,a_1). Define
        φ_a(r) = −(r^e + a_{e−1} r^{e−1} + ⋯ + a_1 r)  on the arc value set S.
      Then free-1 multipad highs are exactly those a for which φ_a has at least
      two fibres of size e in S.  |T| counts a with a size-e fibre containing
      the terminal value ω^{n'−1} and at least one other size-e fibre.
  (3) Trivial vanishing: if t < 2e then floor(t/e)<2 ⇒ no multipad ⇒ T=∅.
  (4) Hierarchy recall (v55): |T| ≤ min(p^{e−1}, C(t−1,e−1), C(t−1,2e−1)).

CAS (regime split — critical for deployed):
  (5) When t ∼ p (small primes): multipads can be dense (e=5,k=17,p=101,t=85
      ⇒ nH∼3.6e6, T∼4.4e5).  Random model fails here because C(t,e)/p^{e−1}=O(1).
  (6) When t ≪ p (p∼10^4, t/p ∼ 0.002–0.005, closer to deployed n'/p∼5.5e-4):
        e ≥ 4: nH=T=0 on all checked rows (e=4,5; k≤10).
        e = 3, k=17: rare multipads (T ∈ {0,1,2,3,9,…}), not identically empty.
  (7) Multipad pairs are not pure index-translates (0 translate pairs on suite).
  (8) Onset k_min(e) tends to grow with p (more room needed before first multipad).

Deployed (n'/p ∼ 5.5e-4, e=67472, k=17) sits deep in the sparse regime of (6).
Entropy (v55) still predicts empty; e=3 shows sparse ≠ automatic empty.

OPEN:
  Prove T=∅ or |T|≤H2 for deployed e on the KB arc (or for all e≥4 with t≪p).
  Do not claim residual card closed.

  python3 experimental/scripts/verify_kb_qatom_route_d_v56.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v56"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v56.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v56.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v56.report.md"
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


def lemma_power_sums() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_iff_power_sums_char_gt_e",
        "statement": (
            "For e-sets of field elements in char 0 or char p > e, equal monic "
            "highs (e_1..e_{e−1}) are equivalent to equal power sums p_1..p_{e−1} "
            "via Newton–Girard (triangular, diagonal k ≠ 0)."
        ),
        "proof": [
            "Newton: k e_k = sum_{i=1}^k (−1)^{i−1} e_{k−i} p_i for k < e.",
            "Triangular in either direction with pivots 1..e−1 invertible if char > e.",
            "Deployed p = 2^31−2^24+1 ≫ e = 67472.",
        ],
        "toys": "Sage: multipad partitions by monic high equal those by power sums (e=3).",
    }


def lemma_phi() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "phi_fibre_formulation_of_multipads",
        "statement": (
            "Let S ⊂ F be the arc values, |S|=t. For a=(a_{e−1},…,a_1) set "
            "φ_a(r)=−(r^e+a_{e−1}r^{e−1}+⋯+a_1 r). Multipad free-1 highs are "
            "exactly those a for which φ_a has ≥2 fibres of cardinality e in S. "
            "T corresponds to a with an e-fibre containing the terminal value and "
            "≥1 other e-fibre."
        ),
        "proof": [
            "Monic f_β=X^e+a_{e−1}X^{e−1}+⋯+a_1 X+β has root r ⇔ φ_a(r)=β.",
            "If |φ_a^{−1}(β)∩S|=e then f_β splits completely on that fibre "
            "(deg e, e roots) ⇒ that fibre is a free-1 e-set of high a.",
            "≥2 such β ⇒ multipad high; terminal value in a fibre ⇒ contributes to T.",
        ],
    }


def lemma_trivial_vanish() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "T_empty_when_t_lt_2e",
        "statement": "If t < 2e then T = ∅ (no multipad packing).",
        "proof": ["|F_H| ≤ floor(t/e) < 2 for every high."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_sparse_regime_T_bound",
        "statement": (
            f"In the sparse regime t ≪ p (deployed n'/p ≈ {N_PRIME/P:.3e}, e={E}, "
            f"k=17), prove T=∅ or |T|≤H2={H2}. CAS: e≥4 empty on p∼10^4 toys; "
            f"e=3 still has rare T>0 at k=17."
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


def power_sums(idxs, vals, p, e):
    out = []
    for k in range(1, e):
        s = 0
        for i in idxs:
            s = (s + pow(vals[i], k, p)) % p
        out.append(s)
    return tuple(out)


def nH_T_struct(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by_h: dict[Any, list] = defaultdict(list)
    by_ps: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        ix = tuple(sorted(idxs))
        by_h[monic_high(ix, vals, p, e)].append(ix)
        by_ps[power_sums(ix, vals, p, e)].append(ix)
    # multipad partitions agree?
    part_h = {frozenset(us) for us in by_h.values() if len(us) >= 2}
    part_ps = {frozenset(us) for us in by_ps.values() if len(us) >= 2}
    nH = len(part_h)
    T = 0
    translate = 0
    other = 0
    for us in by_h.values():
        if len(us) < 2:
            continue
        # terminal
        if any(t - 1 in u for u in us):
            # count terminal U in this fiber
            for u in us:
                if t - 1 in u:
                    T += 1
        for a, b in itertools.combinations(us, 2):
            da = [b[i] - a[i] for i in range(e)]
            if len(set(da)) == 1:
                translate += 1
            else:
                other += 1
    return {
        "p": p,
        "e": e,
        "t": t,
        "nH": nH,
        "T": T,
        "parts_agree": part_h == part_ps,
        "translate_pairs": translate,
        "other_pairs": other,
        "t_over_p": t / p,
        "C_over_pe": math.comb(t, e) / (p ** (e - 1)),
    }


def is_prime(p: int) -> bool:
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    d = 3
    while d * d <= p:
        if p % d == 0:
            return False
        d += 2
    return True


def smallest_n_ge(p: int, n0: int) -> int | None:
    m = p - 1
    best = None
    d = 1
    while d * d <= m:
        if m % d == 0:
            for n in (d, m // d):
                if n >= n0 and n < p:
                    if best is None or n < best:
                        best = n
        d += 1
    return best


def toy_suite() -> dict[str, Any]:
    ensure(P > E, "char > e deployed")
    ensure(N_PRIME / P < 0.001, "deployed sparse t/p")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_NP == 17, "k")

    # power-sum agreement + no translates on small suite
    struct_rows = []
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [2, 3, 4]:
            for t in [4 * e, 6 * e, min(n, 10 * e)]:
                if t > n or math.comb(t, e) > 50000:
                    continue
                r = nH_T_struct(p, n, e, t)
                ensure(r["parts_agree"], "power sum vs monic")
                ensure(r["translate_pairs"] == 0, "no pure index translate multipads")
                struct_rows.append(r)
    ensure(len(struct_rows) >= 12, "struct rows")

    # trivial vanish
    r0 = nH_T_struct(61, 60, 5, 9)  # t=9 < 10=2e
    ensure(r0["nH"] == 0 and r0["T"] == 0, "trivial vanish")

    # dense regime: t~p has large T for e=3
    dense = nH_T_struct(31, 30, 3, 30)
    ensure(dense["T"] > dense["p"], "dense e3 T>p")

    # sparse regime: large p, small t/p
    sparse_rows = []
    sparse_e4_zero = True
    sparse_e3_has_T = False
    for p in [10007, 10009, 10037, 10061, 10067, 10079, 10091, 10103, 10111]:
        if not is_prime(p):
            continue
        n = smallest_n_ge(p, 51)
        if n is None:
            continue
        for e, k in [(3, 17), (4, 8), (4, 10), (5, 6)]:
            t = k * e
            if t > n or math.comb(t, e) > 200000:
                continue
            r = nH_T_struct(p, n, e, t)
            sparse_rows.append(r)
            if e >= 4 and r["nH"] != 0:
                sparse_e4_zero = False
            if e == 3 and r["T"] > 0:
                sparse_e3_has_T = True
    ensure(len(sparse_rows) >= 8, "sparse rows")
    ensure(sparse_e4_zero, "e>=4 sparse zero")
    # e=3 may or may not hit on this prime list; don't require has_T
    # but require all sparse have small T relative to H2-scale (always)
    ensure(all(r["T"] <= H2 for r in sparse_rows), "sparse T<=H2 trivial")
    ensure(all(r["t_over_p"] < 0.02 for r in sparse_rows), "sparse t/p")

    return {
        "status": "PASS",
        "struct_rows": struct_rows,
        "sparse_rows": sparse_rows,
        "dense_example": dense,
        "census": {
            "n_struct": len(struct_rows),
            "n_sparse": len(sparse_rows),
            "all_parts_agree": True,
            "all_no_translate": True,
            "sparse_e4_all_zero": sparse_e4_zero,
            "sparse_e3_any_T": sparse_e3_has_T,
            "dense_T": dense["T"],
            "dense_p": dense["p"],
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "p": P,
            "nprime_over_p": N_PRIME / P,
            "k_pack": FLOOR_NP,
            "H2": H2,
            "H2_over_p": H2 / P,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v56",
        "title": "Free-1 multipads on GP: phi fibres + sparse vs dense regime",
        "status": "REGIME_SPLIT_OPEN_SPARSE_PROOF",
        "claims": {
            "proves_free1_iff_power_sums_char_gt_e": True,
            "proves_phi_fibre_formulation": True,
            "proves_trivial_vanish_t_lt_2e": True,
            "cas_no_index_translate_multipads": True,
            "cas_dense_regime_large_T": True,
            "cas_sparse_e_ge_4_empty": True,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "power_sums": lemma_power_sums(),
            "phi": lemma_phi(),
            "trivial": lemma_trivial_vanish(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {
            "python_nt": "enum + regime surveys",
            "sage": "monic high vs power-sum partition equality (e=3)",
        },
        "impact_on_program": {
            "closed": "algebraic dictionary (phi, power sums); regime diagnosis",
            "wall": "prove sparse-regime bound for deployed e (e=3 still rare hits)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    sparse = cert["toy_suite"]["sparse_rows"][:12]
    stbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['t']} | {r['t_over_p']:.4f} | {r['nH']} | "
        f"{r['T']} | {r['C_over_pe']:.2e} |"
        for r in sparse
    )
    return f"""# KB-MCA Route-D v56: free-1 multipads on GP — regime split

Status: **algebraic dictionary PROVED**; **dense vs sparse regime** diagnosed;
deployed `|T|≤H2` still **OPEN** (local packet, not on `main`).

## Setup

```text
|H_unt| = |T|   (v54 star)
deployed: n'={d['n_prime']}, e={d['e']}, n'/p ≈ {d['nprime_over_p']:.3e}, k={d['k_pack']}
H2/p ≈ {d['H2_over_p']:.4f}
```

## Dictionary (PROVED)

### Power sums
For char `p > e`: free-1 monic high ⇔ equal power sums `p_1..p_{{e−1}}` (Newton).

### φ-fibres
For high coeffs `a`, on arc values `S`:

```text
φ_a(r) = −(r^e + a_{{e−1}} r^{{e−1}} + ⋯ + a_1 r)
```

Multipad highs = those `a` with **≥2 fibres of size e**.  
`T` = such `a` with an e-fibre containing the terminal value.

### Trivial vanish
`t < 2e` ⇒ `T = ∅`.

## Regime split (CAS)

| Regime | Example | Multipads |
|---|---|---|
| **Dense** `t ∼ p` | p=101, e=5, t=85 (k=17) | nH∼3.6e6, T∼4.4e5 (huge) |
| **Sparse** `t ≪ p` | p∼10^4, t/p∼0.003–0.005 | e≥4: **empty**; e=3 k=17: **rare** T∈{{0,1,2,…}} |

Dense failure of the random model: `C(t,e)/p^{{e−1}} = O(1)`.  
Deployed `n'/p ∼ 5.5e-4` is **sparse**; entropy (v55) predicts empty.

### Sparse sample (this suite)

| p | e | t | t/p | nH | T | C/p^{{e−1}} |
|---|---:|---:|---:|---:|---:|---:|
{stbl}

Census: sparse e≥4 all zero = {cen['sparse_e4_all_zero']};  
sparse e=3 any T = {cen['sparse_e3_any_T']};  
dense e=3 example T={cen['dense_T']} on p={cen['dense_p']}.

### Structure
Multipad pairs are **not** pure index-translates (0 on struct suite).  
Monic-high partitions = power-sum partitions on checked rows.

## What this does *not* prove

- Not `T=∅` at deployed e (e=3 still has rare sparse multipads on toys).
- Not `|T|≤H2` by `p^{{e−1}}` (for e≥3, `p^{{e−1}} ≫ H2`).
- Not residual card / `A_SP≤t·p`.

## OPEN

Prove in the **sparse** regime (or at deployed parameters) that
`T=∅` or `|T|≤H2`, using the φ-fibre / power-sum dictionary — especially
controlling e=3-type rare events at large e.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v56.py --check
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
        "# kb-qatom-route-d-v56\n\n"
        "Free-1 multipads on GP: phi fibres + sparse/dense regime split.\n"
    )
    REPORT_PATH.write_text(
        f"# v56 report\n\nstatus: {cert['status']}\n"
        f"power sums / phi: PROVED\n"
        f"sparse e>=4 empty (CAS): {cert['toy_suite']['census']['sparse_e4_all_zero']}\n"
        f"OPEN sparse proof: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free-1 <=> power sums (char > e): PROVED")
    print("  phi-fibre multipad dictionary: PROVED")
    print("  t < 2e => T empty: PROVED")
    print(
        f"  CAS sparse e>=4 empty={cen['sparse_e4_all_zero']}; "
        f"sparse e=3 any T={cen['sparse_e3_any_T']}; "
        f"dense e=3 T={cen['dense_T']} on p={cen['dense_p']}"
    )
    print("  OPEN: prove sparse-regime |T|<=H2 at deployed e")


if __name__ == "__main__":
    main()
