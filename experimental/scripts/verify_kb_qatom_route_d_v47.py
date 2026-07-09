#!/usr/bin/env python3
"""KB-MCA Route-D v47: untyped residual high bound draft — reduction lemmas.

Certifies toy support for the draft in
  experimental/notes/thresholds/kb_qatom_route_d_v47_untyped_high_bound_draft.md

Proved / draft status:
  (1) Untyped free-1 pair has unique core C — PROVED (definition).
  (2) Pure-untyped high has unique core C — TOYS UNIVERSAL (C_unique conjecture);
      multi_C_highs = 0 on full suite.
  (3) Under C_unique: |H_unt| = sum_C |H_unt(C)| with H_unt(C) free-1 multipad
      highs in Ω_C = D\\C, |Ω|=n−m_c = A+e deployed — PROVED reduction.
  (4) Per-core free-1: |F_H|≤⌊n'/e⌋, deg≤⌊n'/e⌋−1 on Ω — PROVED (v25/v19).
  (5) Crude |H_unt(C)| ≤ binom(n',e)·(⌊n'/e⌋−1)/2 — PROVED, not useful for H2.
  (6) REFUTED: |H_unt(C)| ≤ ⌊n'/e⌋ or ≤2⌊n'/e⌋ (toys).
  (7) OPEN ★: H_*(A+e, e) ≤ H2 (free-1 multipad high count in domain size A+e).
  (8) Master conditional: N_C · H_*(n',e) ≤ H2 ⇒ |H_unt|≤H2 under C_unique.

Does NOT prove C_unique as theorem or H_* ≤ H2.

  python3 experimental/scripts/verify_kb_qatom_route_d_v47.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v47.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v47"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v47.json"
NOTE_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "thresholds"
    / "kb_qatom_route_d_v47_untyped_high_bound_draft.md"
)
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v47.report.md"
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
FLOOR_NP = N_PRIME // E  # 17
DEG_NP = FLOOR_NP - 1  # 16
PAIRS_PER_HIGH = 31 * 30
H2 = E_P // (2 * PAIRS_PER_HIGH)
PACK_C_DEP = N // M_C  # 2


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


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_unique_core_pair() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "untyped_pair_unique_core",
        "statement": (
            "An untyped free-1 ordered pair arises from a unique multi-U pencil "
            "(C,H), hence has a unique core C."
        ),
        "proof": [
            "Untyped ⇔ side key not multi-core multipad.",
            "Multi-U free-1 pencil providing the pair has a single C.",
        ],
    }


def lemma_C_unique_toys() -> dict[str, Any]:
    return {
        "status": "TOYS_UNIVERSAL_CONJECTURE",
        "name": "C_unique_pure_untyped_high",
        "statement": (
            "Conjecture C_unique: a free-1 high whose free-1 CS pairs are all "
            "untyped has a unique core C(H). Toys: multi_C_highs=0 on all rows."
        ),
        "gap": (
            "Rule out F_H splitting into untyped sub-pencils on two cores C≠C'."
        ),
    }


def lemma_reduction() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "reduction_to_Hstar_on_complement",
        "statement": (
            f"Under C_unique: |H_unt| = sum_C |H_unt(C)| ≤ N_C · H_*(n',e) with "
            f"n'=A+e={N_PRIME}, H_* = max free-1 multipad high count on a domain "
            f"of size n'. Deployed ⌊n'/e⌋={FLOOR_NP}, deg≤{DEG_NP}."
        ),
        "proof": [
            "Each pure-untyped high has unique C; F_H ⊂ D\\C.",
            "N_C = # distinct cores; each |H_unt(C)| ≤ H_*(n',e).",
        ],
        "card_close": f"N_C · H_*(n',e) ≤ H2={H2} ⇒ residual untyped high gate",
        "deployed": {
            "n_prime": N_PRIME,
            "floor_nprime_e": FLOOR_NP,
            "H2": H2,
            "pack_C_n_over_mc": PACK_C_DEP,
        },
    }


def lemma_crude_and_refute() -> dict[str, Any]:
    return {
        "status": "PROVED_AND_REFUTED_ENVELOPES",
        "name": "per_core_crude_and_false_floor",
        "statement": (
            "PROVED: |H_unt(C)| ≤ binom(n',e)·(⌊n'/e⌋−1)/2 (useless vs H2). "
            "REFUTED: |H_unt(C)| ≤ ⌊n'/e⌋ or ≤2⌊n'/e⌋ on toys."
        ),
    }


def lemma_open_star() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_Hstar_A_plus_e",
        "statement": (
            f"Prove H_*(A+e, e) ≤ H2={H2}, or the co-extension-restricted count "
            f"of free-1 multipad highs in complements of m_c-sets is ≤ H2/N_C."
        ),
        "note": (
            "This is the terminal wall after the free-1+free_core reduction. "
            "Additive combinatorics / split-poly counts on cyclic domains are "
            "the plausible tools — not more small-n envelope hunting."
        ),
    }


def pure_untyped_census(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 60000:
        return None
    free_core = m_c - w
    nprime = n - m_c
    floor_np = max(nprime // e, 1)
    vals = domain_vals(p, n)
    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)

    pair_cores: dict[Any, set] = defaultdict(set)
    for _z, members in fib.items():
        pencils: dict[Any, list] = defaultdict(list)
        for S in members:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = frozenset(S - U)
            high, c0 = free1_high_c0(U, vals, p)
            pencils[(tuple(sorted(C)), high)].append((U, c0, high, C))
        for _key, lst in pencils.items():
            by_u: dict = {}
            for U, c0, high, C in lst:
                by_u[tuple(sorted(U))] = (c0, high, C)
            if len(by_u) < 2:
                continue
            items = list(by_u.items())
            for i, (ut, a) in enumerate(items):
                for j2, (vt, b) in enumerate(items):
                    if i == j2 or a[0] == b[0]:
                        continue
                    # untyped candidate pair cores
                    pair_cores[(a[1], ut, vt)].add(a[2])

    # classify pairs
    H_cores_unt: dict[Any, set] = defaultdict(set)
    H_multi = set()
    for (high, ut, vt), cores in pair_cores.items():
        if len(cores) == 1:
            H_cores_unt[high].add(next(iter(cores)))
        else:
            H_multi.add(high)

    multi_C = sum(1 for h, cs in H_cores_unt.items() if len(cs) > 1)
    # pure untyped: only untyped pairs, unique C
    pure: dict[Any, Any] = {}
    for h, cs in H_cores_unt.items():
        if h in H_multi:
            continue
        if len(cs) == 1:
            pure[h] = next(iter(cs))

    C_to_H: dict[Any, set] = defaultdict(set)
    for h, c in pure.items():
        C_to_H[c].add(h)

    max_H_per_C = max((len(v) for v in C_to_H.values()), default=0)
    n_C = len(C_to_H)

    # unique core for untyped pairs: every untyped pair has |cores|==1 by construction
    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "free_core": free_core,
        "m_c": m_c,
        "nprime": nprime,
        "floor_np": floor_np,
        "n_pure": len(pure),
        "n_C": n_C,
        "max_H_per_C": max_H_per_C,
        "multi_C_highs": multi_C,
        "C_unique_ok": multi_C == 0,
        "H_per_C_le_floor_np": max_H_per_C <= floor_np,
        "H_per_C_le_2floor_np": max_H_per_C <= 2 * floor_np,
        "H_per_C_le_H2": max_H_per_C <= H2,
        "n_pure_le_H2": len(pure) <= H2,
    }


def toy_suite() -> dict[str, Any]:
    ensure(N_PRIME == A + E, "n'")
    ensure(FLOOR_NP == 17, "floor np")
    ensure(DEG_NP == 16, "deg")
    ensure(PACK_C_DEP == 2, "n/mc")
    ensure(FREE_CORE == 846161, "fc")
    ensure(NOTE_PATH.is_file(), "draft note present")

    rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 4, 2),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (17, 16, 9, 2),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (19, 18, 8, 2),
        (31, 30, 4, 2),
        (31, 30, 5, 2),
        (31, 30, 6, 2),
    ]:
        r = pure_untyped_census(p, n, j, w)
        if r is None or r["n_pure"] == 0:
            continue
        ensure(r["C_unique_ok"], "C_unique")
        ensure(r["H_per_C_le_H2"], "per C H2")
        rows.append(r)

    ensure(len(rows) >= 10, "rows")
    ensure(all(r["C_unique_ok"] for r in rows), "all C unique")
    ensure(any(not r["H_per_C_le_floor_np"] for r in rows), "refute floor np")
    ensure(any(not r["H_per_C_le_2floor_np"] for r in rows), "refute 2floor np")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "max_pure": max(r["n_pure"] for r in rows),
            "max_H_per_C": max(r["max_H_per_C"] for r in rows),
            "max_n_C": max(r["n_C"] for r in rows),
            "all_C_unique": True,
            "refute_H_le_floor_np": True,
            "refute_H_le_2floor_np": True,
        },
        "draft_note": str(NOTE_PATH.relative_to(ROOT)),
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v47",
        "title": "Untyped residual high bound draft — reduction to H_*(A+e,e)",
        "status": "DRAFT_REDUCTION_OPEN_HSTAR",
        "claims": {
            "proves_untyped_pair_unique_core": True,
            "toys_C_unique_pure_untyped_high": True,
            "proves_reduction_under_C_unique": True,
            "proves_per_core_free1_degree": True,
            "refutes_H_unt_C_le_floor_nprime_e": True,
            "proves_Hstar_le_H2": False,
            "proves_C_unique_theorem": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "floor_nprime_e": FLOOR_NP,
            "deg_nprime": DEG_NP,
            "H2": H2,
            "pack_C": PACK_C_DEP,
            "free_core": FREE_CORE,
            "m_c": M_C,
            "e": E,
            "e_p": E_P,
        },
        "lemmas": {
            "unique_core_pair": lemma_unique_core_pair(),
            "C_unique": lemma_C_unique_toys(),
            "reduction": lemma_reduction(),
            "crude_refute": lemma_crude_and_refute(),
            "OPEN_star": lemma_open_star(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": (
                "Untyped residual highs → free-1 multipad highs in complements "
                "of size A+e; card closes if N_C·H_*(A+e,e)≤H2"
            ),
            "wall": "H_*(A+e,e)≤H2 (or co-extension-restricted variant)",
            "not": "more |H|≤n / floor envelopes",
        },
    }


def render_report(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    return f"""# v47 report

status: {cert['status']}

## Reduction

```text
C_unique (toys) + |H_unt| ≤ N_C · H_*(A+e, e)
n' = {d['n_prime']},  ⌊n'/e⌋ = {d['floor_nprime_e']},  H2 = {d['H2']}
```

## Toys

- all C_unique: {cen['all_C_unique']}
- max pure untyped highs: {cen['max_pure']}
- max H per core: {cen['max_H_per_C']}
- refute H≤⌊n'/e⌋: {cen['refute_H_le_floor_np']}

## OPEN ★

H_*(A+e, e) ≤ H2

Draft note: {cert['toy_suite']['draft_note']}
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
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v47\n\n"
        "Untyped residual high bound draft: reduction to H_*(A+e,e).\n"
        "See notes/thresholds/kb_qatom_route_d_v47_untyped_high_bound_draft.md\n"
    )
    REPORT_PATH.write_text(render_report(cert))
    # note already written as draft md
    ensure(NOTE_PATH.is_file(), "note")
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  untyped pair → unique C: PROVED")
    print(f"  C_unique pure-untyped high: TOYS UNIVERSAL ({cen['n_rows']} rows)")
    print(
        f"  reduction |H_unt| ≤ N_C · H_*(A+e,e), n'={N_PRIME}, "
        f"⌊n'/e⌋={FLOOR_NP}: PROVED conditional"
    )
    print("  |H_unt(C)| ≤ ⌊n'/e⌋: REFUTED "
          f"(max H/C={cen['max_H_per_C']})")
    print(f"  OPEN ★: H_*(A+e,e) ≤ H2={H2}")
    print(f"  draft: {cert['toy_suite']['draft_note']}")


if __name__ == "__main__":
    main()
