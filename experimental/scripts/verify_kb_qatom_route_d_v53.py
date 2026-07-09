#!/usr/bin/env python3
"""KB-MCA Route-D v53: C_unique PROVED — untyped core is the terminal block.

Closes the v47 ★ gap.  Setup: e = w+1 (route-D free-1), A_SP prefix U.

Proved:
  (1) Free-1 fiber auto-match: if free-1 U,V (equal e1..e_{e−1}) and
      max(U∪V) < min(C), then e_k(C⊔U)=e_k(C⊔V) for all k=1..w
      (since w=e−1).  Proof: Newton/elementary expansion
        e_k(C⊔U)−e_k(C⊔V) = e_{k−e}(C)·(e_e(U)−e_e(V))
      vanishes for k < e, hence for k≤w.
  (2) Core count for a free-1 side key (U,V):
        #cores = binom(n − 1 − max(U∪V), m_c)
      = # of m_c-subsets of the strict upper index interval
      {max(U∪V)+1, …, n−1}.
  (3) Untyped ⇔ unique core ⇔ binom(n−1−max(U∪V), m_c)=1
      ⇔ n−1−max(U∪V)=m_c ⇔ max(U∪V)=n−m_c−1=n'−1
      ⇔ unique core C_* = {n', n'+1, …, n−1}  (terminal m_c-block).
  (4) C_unique PROVED: every untyped free-1 CS pair has the SAME core C_*.
      Hence every pure-untyped high has unique core C_*.
  (5) Global pure-untyped cores: N_C = 1, namely {C_*}, when any pure-untyped
      high exists.  Reduction upgrades from
        |H_unt| ≤ N_C · H_*(n',e)   to   |H_unt| ≤ H_*(n',e) = H_*^pre(n',e).

OPEN: H_*^pre(n',e) ≤ H2 at deployed (n',e)=(A+e, e) — still the terminal
★_pre wall (v48–v52); e=2 closed by |H|≤p≤H2.

Does NOT prove H_*≤H2 for e>2; does NOT prove A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v53.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v53"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v53.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v53.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v53.report.md"
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
N_PRIME = A + E  # = n - m_c
H2 = E_P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_fiber_automatch() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_fiber_automatch_w_eq_e_minus_1",
        "statement": (
            "If free-1 U,V (e_i(U)=e_i(V) for i=1..e−1) and C is disjoint from "
            "U∪V with max(U∪V)<min(C), then e_k(C⊔U)=e_k(C⊔V) for k=1..w, "
            "where e=w+1 so w=e−1."
        ),
        "proof": [
            "e_k(C⊔U)=∑_{i=0}^k e_i(C) e_{k−i}(U).",
            "Difference = ∑_i e_i(C)(e_{k−i}(U)−e_{k−i}(V)).",
            "For free-1, e_j(U)=e_j(V) for j=1..e−1; e_0=1.",
            "Only possible nonzero: j=e term ⇒ e_{k−e}(C)·(e_e(U)−e_e(V)).",
            "For k<e this index k−e<0 ⇒ difference 0.",
            "w=e−1 ⇒ all k=1..w are <e ⇒ fiber match automatic.",
        ],
    }


def lemma_core_count() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_side_key_core_count",
        "statement": (
            "For free-1 (U,V), the A_SP cores are exactly the m_c-subsets of "
            "{max(U∪V)+1,…,n−1}; count = binom(n−1−max(U∪V), m_c)."
        ),
        "proof": [
            "A_SP requires max(U),max(V)<min(C) ⇒ C⊆{max(U∪V)+1..n−1}.",
            "Fiber match automatic (lemma fiber_automatch).",
            "Each such C of size m_c gives a multi-U free-1 pencil pair.",
        ],
    }


def lemma_untyped_terminal() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "untyped_iff_terminal_core_C_star",
        "statement": (
            f"Untyped ⇔ binom(n−1−max(U∪V),m_c)=1 ⇔ max(U∪V)=n'−1 "
            f"with n'=n−m_c, and the unique core is "
            f"C_*={{n',…,n−1}}. Deployed n'={N_PRIME}, |C_*|=m_c={M_C}."
        ),
        "proof": [
            "binom(N,m_c)=1 with m_c≥1 ⇔ N=m_c.",
            "N=n−1−max(U∪V)=m_c ⇔ max=n−m_c−1=n'−1.",
            "Upper interval {n'…n−1} has length m_c ⇒ unique C=C_*.",
        ],
    }


def lemma_C_unique() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "C_unique_pure_untyped_high",
        "statement": (
            "Every untyped free-1 CS pair has core C_*. Hence a pure-untyped "
            "high (all its free-1 CS pairs untyped) has unique core C_*."
        ),
        "proof": [
            "Lemma untyped_terminal: every untyped pair has core C_*.",
            "All pairs of a pure-untyped high are untyped ⇒ same C_*.",
        ],
    }


def lemma_N_C_one() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "N_C_eq_1_for_pure_untyped",
        "statement": (
            "The set of cores of pure-untyped highs is either empty or {C_*}. "
            "In particular N_C ≤ 1, and |H_unt| ≤ H_*^pre(n',e)."
        ),
        "proof": [
            "Every pure-untyped high has core C_* (C_unique).",
            "t=min(C_*)=n'; U's of pure-untyped live in I_{n'}.",
            "H_unt = H_unt(C_*) ⊆ free-1 multipad highs on I_{n'}.",
            "Hence |H_unt| ≤ H_*^pre(n',e).",
        ],
        "upgrade": (
            "v47 had |H_unt|≤N_C·H_*(n',e); now N_C=1 removes the N_C factor."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_Hstar_pre_nprime_le_H2",
        "statement": (
            f"Prove H_*^pre(n',e) ≤ H2={H2} for deployed n'={N_PRIME}, e={E}. "
            f"e=2: closed (|H|≤p≤H2). e>2: open (v48–v52)."
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


def census_row(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 90000:
        return None
    nprime = n - m_c
    C_star = frozenset(range(nprime, n))
    vals = domain_vals(p, n)

    fib: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        S = frozenset(exps)
        poly = monic_rev([vals[i] for i in sorted(S)], p)
        fib[tuple(poly[1 : w + 1])].append(S)

    side_cores: dict[Any, set] = defaultdict(set)
    side_Us: dict[Any, set] = defaultdict(set)
    for _z, members in fib.items():
        by: dict[Any, list] = defaultdict(list)
        for S in members:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = frozenset(S - U)
            high, c0 = free1_high_c0(U, vals, p)
            by[(tuple(sorted(C)), high)].append((tuple(sorted(U)), c0, C))
        for (_Ct, high), lst in by.items():
            Us = {u: (c0, C) for u, c0, C in lst}
            if len(Us) < 2:
                continue
            items = list(Us.items())
            for i, (u, a) in enumerate(items):
                for v, b in items[i + 1 :]:
                    if a[0] == b[0]:
                        continue
                    sk = (high, a[0], b[0])
                    side_cores[sk].add(frozenset(a[1]))
                    side_Us[sk].add(u)
                    side_Us[sk].add(v)

    n_unt = n_mp = 0
    pure_cores: set[Any] = set()
    multi_C_pure = 0
    # per-high cores among untyped-only highs
    high_pair_cores: dict[Any, set] = defaultdict(set)
    high_has_mp: set[Any] = set()
    for sk, cores in side_cores.items():
        high = sk[0]
        Us = side_Us[sk]
        mx = max(max(u) for u in Us)
        expected = math.comb(n - 1 - mx, m_c)
        ensure(len(cores) == expected, f"core count p={p} j={j} w={w}")
        if len(cores) == 1:
            n_unt += 1
            C = next(iter(cores))
            ensure(C == C_star, "C_star")
            ensure(mx == nprime - 1, "max terminal")
            high_pair_cores[high].add(C)
        else:
            n_mp += 1
            ensure(mx < nprime - 1, "mp max")
            high_has_mp.add(high)

    for high, cs in high_pair_cores.items():
        if high in high_has_mp:
            continue
        pure_cores |= cs
        if len(cs) > 1:
            multi_C_pure += 1

    # fiber auto-match spot check on one free-1 pair + random eligible C
    automatch_ok = True
    if n_unt + n_mp > 0:
        for sk, cores in side_cores.items():
            Us = list(side_Us[sk])
            if len(Us) < 2:
                continue
            U, V = set(Us[0]), set(Us[1])
            mx = max(U | V)
            # pick up to 3 eligible C
            upper = list(range(mx + 1, n))
            if len(upper) < m_c:
                continue
            for C in itertools.islice(itertools.combinations(upper, m_c), 3):
                Cset = set(C)
                pU = monic_rev([vals[i] for i in sorted(Cset | U)], p)
                pV = monic_rev([vals[i] for i in sorted(Cset | V)], p)
                if pU[1 : w + 1] != pV[1 : w + 1]:
                    automatch_ok = False
            break

    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "m_c": m_c,
        "nprime": nprime,
        "n_unt": n_unt,
        "n_mp": n_mp,
        "n_pure_cores": len(pure_cores),
        "multi_C_pure": multi_C_pure,
        "C_unique_ok": multi_C_pure == 0,
        "N_C_le_1": len(pure_cores) <= 1,
        "automatch_ok": automatch_ok,
        "all_unt_C_star": True,
    }


def toy_suite() -> dict[str, Any]:
    ensure(E == W + 1, "e=w+1")
    ensure(N_PRIME == N - M_C, "n'")
    ensure(N_PRIME == A + E, "n'=A+e")
    ensure(FREE_CORE == 846161, "fc")
    # deployed: only s=0 gives binom(m_c, m_c)=1 style for terminal
    ensure(math.comb(M_C, M_C) == 1, "terminal unique")
    ensure(math.comb(M_C + 1, M_C) == M_C + 1 > 1, "one free index multipad")

    rows = []
    for p, n in [(17, 16), (19, 18), (31, 30), (37, 36)]:
        for j in range(3, min(12, n // 2 + 2)):
            for w in range(1, j - 1):
                if math.comb(n, j) > 90000:
                    continue
                r = census_row(p, n, j, w)
                if r is None or (r["n_unt"] == 0 and r["n_mp"] == 0):
                    continue
                ensure(r["C_unique_ok"], "C_unique")
                ensure(r["N_C_le_1"], "N_C")
                ensure(r["automatch_ok"], "automatch")
                rows.append(r)

    ensure(len(rows) >= 20, "rows")
    ensure(any(r["n_unt"] > 0 for r in rows), "have untyped")
    ensure(any(r["n_mp"] > 0 for r in rows), "have multipad")
    ensure(all(r["multi_C_pure"] == 0 for r in rows), "no multi C pure")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "total_unt": sum(r["n_unt"] for r in rows),
            "total_mp": sum(r["n_mp"] for r in rows),
            "all_C_unique": True,
            "all_N_C_le_1": True,
            "all_automatch": True,
            "max_n_pure_cores": max(r["n_pure_cores"] for r in rows),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "m_c": M_C,
            "C_star": f"{{{N_PRIME}..{N - 1}}}",
            "H2": H2,
            "floor_np": FLOOR_NP,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v53",
        "title": "C_unique PROVED: untyped core = terminal block C_*; N_C=1",
        "status": "C_UNIQUE_PROVED",
        "claims": {
            "proves_free1_fiber_automatch": True,
            "proves_core_count_binom": True,
            "proves_untyped_iff_terminal_C_star": True,
            "proves_C_unique": True,
            "proves_N_C_le_1": True,
            "proves_H_unt_le_Hstar_pre_nprime": True,
            "proves_Hstar_pre_nprime_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "w": W,
            "m_c": M_C,
            "n_prime": N_PRIME,
            "C_star_interval": [N_PRIME, N - 1],
            "H2": H2,
            "floor_nprime_e": FLOOR_NP,
            "free_core": FREE_CORE,
        },
        "lemmas": {
            "fiber_automatch": lemma_fiber_automatch(),
            "core_count": lemma_core_count(),
            "untyped_terminal": lemma_untyped_terminal(),
            "C_unique": lemma_C_unique(),
            "N_C_one": lemma_N_C_one(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "closed": "C_unique; N_C=1; |H_unt|≤H_*^pre(n',e)",
            "wall": "H_*^pre(n',e)≤H2 for deployed e>2",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    sample = cert["toy_suite"]["rows"][:12]
    tbl = "\n".join(
        f"| {r['p']} | {r['j']} | {r['w']} | {r['n_unt']} | {r['n_mp']} | "
        f"{r['n_pure_cores']} | {r['C_unique_ok']} |"
        for r in sample
    )
    return f"""# KB-MCA Route-D v53: C_unique PROVED

Status: **C_unique PROVED**. Untyped core is the terminal block
`C_* = {{n',…,n−1}}`. Pure-untyped highs share this single core (`N_C=1`).

## Setup

Free-1 with `e = w+1` (route-D). A_SP: `U` = least `e` indices of `S`,
`C = S\\U`. Domain indices `{{0,…,n−1}}`, `n' = n − m_c = A+e`.

## Lemma — free-1 fiber auto-match (PROVED)

If `U,V` free-1 (`e_i` match for `i=1..e−1`) and `max(U∪V) < min(C)`, then

```text
e_k(C⊔U) = e_k(C⊔V)   for all k = 1..w
```

because `w = e−1` and

```text
e_k(C⊔U) − e_k(C⊔V) = e_{{k−e}}(C) · (e_e(U) − e_e(V))
```

vanishes for `k < e`.

## Lemma — core count (PROVED)

For free-1 `(U,V)`, A_SP cores are the `m_c`-subsets of
`{{max(U∪V)+1, …, n−1}}`:

```text
#cores(U,V)  =  binom(n − 1 − max(U∪V), m_c)
```

## Theorem — untyped ⇔ terminal core (PROVED)

```text
untyped  ⇔  #cores = 1
         ⇔  n − 1 − max(U∪V) = m_c
         ⇔  max(U∪V) = n' − 1
         ⇔  unique core C_* = {{n', n'+1, …, n−1}}
```

## Theorem C_unique (PROVED)

Every untyped free-1 CS pair has core `C_*`. A pure-untyped high therefore has
unique core `C_*`.

## Corollary — N_C = 1 (PROVED)

```text
|H_unt|  =  |H_unt(C_*)|  ≤  H_*^pre(n', e)
```

Upgrades v47 (`N_C · H_*`) by killing the `N_C` factor.

Deployed: `n'={d['n_prime']}`, `C_* = {{{d['n_prime']}..{N-1}}}`, `⌊n'/e⌋={d['floor_nprime_e']}`.

## Toys

| p | j | w | n_unt | n_mp | n_pure_cores | C_unique |
|---|---:|---:|---:|---:|---:|---|
{tbl}

Census: rows={cen['n_rows']}; unt={cen['total_unt']}; mp={cen['total_mp']};
all C_unique; all N_C≤1; core counts match binom.

## Residual card path (updated)

```text
C_unique + N_C=1
  ⇒  |H_unt| ≤ H_*^pre(n', e)
  ⇒  residual card if H_*^pre(n',e) ≤ H2
```

e=2: `H_*^pre ≤ p ≤ H2` (v48). e>2: OPEN.

## OPEN

1. `H_*^pre(n',e) ≤ H2` at deployed e={d['e']} (★_pre wall)
2. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v53.py --check
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
        "# kb-qatom-route-d-v53\n\n"
        "C_unique PROVED: untyped core = terminal block; N_C=1.\n"
    )
    REPORT_PATH.write_text(
        f"# v53 report\n\nstatus: {cert['status']}\n"
        f"C_unique: PROVED\n"
        f"N_C=1: PROVED\n"
        f"|H_unt| <= H_*^pre(n',e): PROVED\n"
        f"OPEN H_*^pre(n',e)<=H2: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free-1 fiber auto-match (w=e−1): PROVED")
    print("  untyped ⇔ terminal core C_*: PROVED")
    print("  C_unique: PROVED")
    print("  N_C=1 ⇒ |H_unt|≤H_*^pre(n',e): PROVED")
    print(
        f"  toys: {cen['n_rows']} rows; unt={cen['total_unt']}; "
        f"mp={cen['total_mp']}; all C_unique"
    )
    print(f"  OPEN: H_*^pre(n'={N_PRIME},e={E}) ≤ H2={H2}")


if __name__ == "__main__":
    main()
