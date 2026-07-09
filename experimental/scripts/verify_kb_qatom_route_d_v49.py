#!/usr/bin/env python3
"""KB-MCA Route-D v49: co-extension free-1 multipads live in index prefixes.

Attacks ★_D via A_SP prefix geometry (canonical U = sorted(S)[:e]).

Proved:
  (1) Prefix co-extension window: if S uses U = e least indices of S and
      C = S\\U, then max(U) < min(C). Every multi-U free-1 pencil with core C
      has all its U ⊆ I_t := {0,1,...,t−1} with t = min(C).
  (2) Multipad packing in the window: need ⌊t/e⌋ ≥ 2 ⇒ t ≥ 2e.
      Combined with |C|=m_c ⊆ {t,...,n−1}: t ≤ n−m_c = n' := A+e.
      Deployed: t ∈ [2e, n'] = [134944, 1183520].
  (3) Per-core bound: |H_coext(C)| ≤ H_*^{pre}(t,e) where H_*^{pre}(t,e) is the
      number of free-1 multipad highs among e-subsets of the index prefix I_t
      of the fixed domain D (values ω^0,...,ω^{t−1}).
  (4) Global pure-untyped under C_unique:
        |H_unt| ≤ sum_C H_*^{pre}(min(C), e) ≤ N_C · max_{t∈[2e,n']} H_*^{pre}(t,e).
  (5) e=2: H_*^{pre}(t,2) ≤ p ≤ H2 for all t (coeff bound) — coext card OK for e=2.
  (6) REFUTED as general: H_*^{pre}(t,e) ≤ ⌊t/e⌋ (toys / prefix census).

CAS:
  (7) Prefix free-1 (stdlib): e=2 always ≤p; e=3 grows with t, ≪p² for small t,
      approaches p² as t→n=p−1.
  (8) Coext census matches: multi-U free-1 pencils obey max(U)<min(C).

OPEN ★_pre:
  Bound max_{t≤n'} H_*^{pre}(t,e) for deployed (e,n') — free-1 multipads on a
  length-t arc of the KB roots-of-unity domain with e≈t/k, k≤17.

Does NOT prove ★_pre ≤ H2 at deployed scale.

  python3 experimental/scripts/verify_kb_qatom_route_d_v49.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v49"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v49.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v49.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v49.report.md"
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
N_PRIME = A + E  # max window
T_MIN = 2 * E  # min window for multipad
H2 = E_P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


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


def monic_high_idxs(idxs, vals, p, e):
    poly = monic_rev([vals[i] for i in idxs], p)
    return tuple(poly[1:e])


def lemma_prefix_window() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "coext_free1_lives_in_index_prefix",
        "statement": (
            "Under the A_SP prefix split U = e least domain indices of S and "
            "C = S\\U: max(U) < min(C). Any multi-U free-1 pencil with core C "
            "has every U ⊆ I_t = {0,...,t−1}, t = min(C)."
        ),
        "proof": [
            "By construction of sorted-index prefix: every index in U is < every "
            "index in C, so U ⊆ {0,...,min(C)−1}.",
            "Multi-U pencil fixes C and varies U among free-1 mates of a high.",
        ],
    }


def lemma_window_range() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_window_range",
        "statement": (
            f"For a multipad free-1 pencil (|F|≥2) with core C of size m_c: "
            f"t=min(C) satisfies 2e ≤ t ≤ n−m_c. Deployed: "
            f"{T_MIN} ≤ t ≤ {N_PRIME}."
        ),
        "proof": [
            "⌊t/e⌋ ≥ 2 for two disjoint e-sets in I_t ⇒ t ≥ 2e.",
            "C ⊆ {t,...,n−1}, |C|=m_c ⇒ n−t ≥ m_c ⇒ t ≤ n−m_c = n' = A+e.",
        ],
        "deployed": {"t_min": T_MIN, "t_max": N_PRIME, "e": E, "n_prime": N_PRIME},
    }


def lemma_per_core_prefix() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "H_coext_C_le_Hstar_prefix",
        "statement": (
            "|H_coext(C)| ≤ H_*^{pre}(min(C), e): free-1 multipad highs among "
            "e-subsets of the index prefix I_t of D (values ω^0..ω^{t−1})."
        ),
        "proof": [
            "Lemma prefix window: all coext free-1 U of C lie in I_t.",
            "Highs of multi-U free-1 pencils with that C are free-1 multipad "
            "highs realized inside I_t.",
        ],
    }


def lemma_global() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "H_unt_le_NC_max_Hstar_pre",
        "statement": (
            "Under C_unique (v47): |H_unt| ≤ N_C · max_{t∈[2e,n']} H_*^pre(t,e). "
            "Card closes if that max ≤ H2/N_C (e.g. N_C=1 ⇒ need max H_*^pre ≤ H2)."
        ),
        "proof": ["v47 reduction + Lemmas prefix/per-core/window range."],
        "deployed_H2": H2,
    }


def lemma_e2() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "prefix_e2_Hstar_le_p_le_H2",
        "statement": (
            "For e=2, H_*^pre(t,2) ≤ p ≤ H2 for all t (high = one F_p coeff). "
            "Co-extension residual card closes for e=2."
        ),
        "proof": ["v48 coeff bound specialized to e=2; independent of t."],
        "deployed_e": E,
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_Hstar_prefix_deployed",
        "statement": (
            f"Bound max_t H_*^pre(t, e={E}) for t≤n'={N_PRIME} — free-1 multipad "
            f"highs on a length-t arc of the KB cyclic domain. Target ≤ H2={H2} "
            f"(or ≤ H2/N_C)."
        ),
        "note": (
            "Not ambient cyclic of size t in a field of size ~t (v48 refuted that "
            "for e=3). This is an arc inside the fixed n-point roots-of-unity domain."
        ),
    }


def Hstar_prefix(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    counts: dict[Any, int] = defaultdict(int)
    for idxs in itertools.combinations(range(t), e):
        counts[monic_high_idxs(idxs, vals, p, e)] += 1
    nH = sum(1 for c in counts.values() if c >= 2)
    max_f = max(counts.values()) if counts else 0
    return {
        "p": p,
        "n": n,
        "e": e,
        "t": t,
        "nH": nH,
        "max_f": max_f,
        "floor": t // e,
        "comb": math.comb(t, e),
        "p_pow": p ** (e - 1),
        "nH_le_p_pow": nH <= p ** (e - 1),
        "nH_le_floor": nH <= max(t // e, 1),
    }


def coext_census(p: int, n: int, j: int, w: int) -> dict[str, Any] | None:
    e = w + 1
    m_c = j - e
    if m_c <= 0 or math.comb(n, j) > 80000:
        return None
    fc = m_c - w
    vals = domain_vals(p, n)
    pencils: dict[Any, list] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        ss = sorted(exps)
        U = frozenset(ss[:e])
        C = frozenset(ss[e:])
        # verify prefix
        ensure(max(U) < min(C), "prefix")
        high, c0 = free1_high_c0(U, vals, p)
        pencils[(tuple(sorted(C)), high)].append((U, c0))

    C_highs: dict[Any, set] = defaultdict(set)
    max_f = 0
    wins = []
    for (Ct, high), lst in pencils.items():
        us = {tuple(sorted(U)) for U, _ in lst}
        if len(us) >= 2:
            C_highs[Ct].add(high)
            max_f = max(max_f, len(us))
            t = min(Ct)
            wins.append(t)
            ensure(t >= e, "t>=e")
            # all U in window
            for U, _ in lst:
                ensure(max(U) < t, "U in window")

    all_H = set()
    for hs in C_highs.values():
        all_H |= hs
    max_H_per_C = max((len(v) for v in C_highs.values()), default=0)
    return {
        "p": p,
        "n": n,
        "j": j,
        "w": w,
        "e": e,
        "fc": fc,
        "m_c": m_c,
        "nH_coext": len(all_H),
        "n_C": len(C_highs),
        "max_H_per_C": max_H_per_C,
        "max_f": max_f,
        "min_t": min(wins) if wins else 0,
        "max_t": max(wins) if wins else 0,
        "multipad_t_ge_2e": all(t >= 2 * e for t in wins) if wins else True,
    }


def toy_suite() -> dict[str, Any]:
    ensure(T_MIN == 2 * E, "tmin")
    ensure(N_PRIME == A + E, "nmax")
    ensure(T_MIN <= N_PRIME, "range nonempty")
    ensure(FLOOR_NP == 17, "floor")
    ensure(P <= H2, "p H2")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E != 2, "deployed e not 2")

    # prefix H_* samples
    pre_rows = []
    for p, n, e, t in [
        (17, 16, 2, 8),
        (17, 16, 2, 16),
        (17, 16, 3, 8),
        (17, 16, 3, 12),
        (17, 16, 3, 16),
        (31, 30, 2, 15),
        (31, 30, 2, 30),
        (31, 30, 3, 12),
        (31, 30, 3, 20),
        (31, 30, 3, 30),
        (73, 72, 3, 18),
        (73, 72, 3, 36),
        (73, 72, 3, 72),
        (101, 100, 3, 15),
        (101, 100, 3, 30),
        (101, 100, 3, 50),
    ]:
        if math.comb(t, e) > 100000:
            continue
        r = Hstar_prefix(p, n, e, t)
        ensure(r["nH_le_p_pow"], "coeff")
        if e == 2:
            ensure(r["nH"] <= p, "e2")
        pre_rows.append(r)

    ensure(any(not r["nH_le_floor"] for r in pre_rows if r["e"] >= 3), "refute floor")

    # coext census
    co_rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (19, 18, 5, 2),
        (19, 18, 6, 2),
        (19, 18, 7, 2),
        (31, 30, 4, 2),
        (31, 30, 5, 2),
        (31, 30, 6, 2),
    ]:
        r = coext_census(p, n, j, w)
        if r is None or r["nH_coext"] == 0:
            continue
        ensure(r["multipad_t_ge_2e"] or r["max_f"] < 2, "t>=2e")
        co_rows.append(r)

    ensure(len(co_rows) >= 8, "co rows")
    ensure(all(r["min_t"] >= r["e"] for r in co_rows), "min t")

    return {
        "status": "PASS",
        "prefix_rows": pre_rows,
        "coext_rows": co_rows,
        "census": {
            "n_prefix": len(pre_rows),
            "n_coext": len(co_rows),
            "max_prefix_nH": max(r["nH"] for r in pre_rows),
            "max_coext_H_per_C": max(r["max_H_per_C"] for r in co_rows),
            "max_coext_nH": max(r["nH_coext"] for r in co_rows),
            "all_prefix_windows_ok": True,
            "refute_Hpre_le_floor": True,
            "e2_pre_le_p": True,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v49",
        "title": "Co-extension free-1 multipads live in index prefixes",
        "status": "PARTIAL_COEXT_PREFIX",
        "claims": {
            "proves_prefix_window": True,
            "proves_window_range_2e_to_nprime": True,
            "proves_Hcoext_le_Hstar_prefix": True,
            "proves_e2_prefix_le_H2": True,
            "refutes_Hstar_pre_le_floor": True,
            "proves_Hstar_pre_deployed_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "m_c": M_C,
            "n_prime": N_PRIME,
            "t_min": T_MIN,
            "t_max": N_PRIME,
            "floor_nprime_e": FLOOR_NP,
            "H2": H2,
            "free_core": FREE_CORE,
            "e_over_nprime": E / N_PRIME,
        },
        "lemmas": {
            "prefix_window": lemma_prefix_window(),
            "window_range": lemma_window_range(),
            "per_core": lemma_per_core_prefix(),
            "global": lemma_global(),
            "e2": lemma_e2(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "geometry": (
                "Co-extension free-1 multipads = free-1 multipads on an index "
                "prefix I_t of D with t=min(C) ∈ [2e, n']"
            ),
            "wall": "H_*^{pre}(t,e) for large e on roots-of-unity arcs",
            "vs_v48": "Not abstract cyclic field domains — arcs inside fixed D",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    pre = cert["toy_suite"]["prefix_rows"]
    co = cert["toy_suite"]["coext_rows"]
    ptbl = "\n".join(
        f"| {r['n']} | {r['e']} | {r['t']} | {r['nH']} | {r['floor']} | "
        f"{r['nH_le_floor']} | {r['p_pow']} |"
        for r in pre
    )
    ctbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['fc']} | {r['nH_coext']} | {r['max_H_per_C']} | "
        f"{r['n_C']} | {r['min_t']} | {r['max_t']} | {r['multipad_t_ge_2e']} |"
        for r in co
    )
    return f"""# KB-MCA Route-D v49: co-extension free-1 = prefix free-1 multipads

Status: `PARTIAL` — **prefix window geometry PROVED**; residual untyped highs
reduce to `H_*^{{pre}}` on index arcs; deployed bound still **OPEN**.

## Geometry (PROVED)

A_SP uses `U =` e least indices of `S`, `C = S\\U`:

```text
max(U) < min(C) = t
⇒  U ⊆ I_t = {{0,1,...,t−1}}
```

Multi-U free-1 pencil with core `C` ⇒ all free-1 mates live in **I_t**.

Multipad (`|F|≥2`) forces:

```text
2e  ≤  t  ≤  n − m_c  =  n'  =  A+e
```

Deployed window range:

```text
t ∈ [{d['t_min']}, {d['t_max']}]
⌊n'/e⌋ = {d['floor_nprime_e']}
e/n' ≈ {d['e_over_nprime']:.4f}
```

## Bound (PROVED)

```text
|H_coext(C)|  ≤  H_*^{{pre}}(min(C), e)
```

`H_*^{{pre}}(t,e)` = # free-1 multipad highs among e-subsets of the prefix
`{{ω^0,...,ω^{{t−1}}}}` of the fixed KB domain.

Under C_unique (v47):

```text
|H_unt|  ≤  N_C · max_{{t ∈ [2e,n']}} H_*^{{pre}}(t,e)
```

## e=2 (PROVED)

`H_*^{{pre}}(t,2) ≤ p ≤ H2` for all t — coext residual card OK when e=2.

Deployed e={d['e']} ≫ 2.

## OPEN ★_pre

```text
max_{{t ≤ n'}} H_*^{{pre}}(t, e={d['e']})  ≤  H2 ?
```

Free-1 multipads on a **roots-of-unity arc** of length t, not an abstract
field-cyclic domain of size t (v48: those saturate p^{{e−1}} for e=3).

## Prefix H_* toys

| n | e | t | nH | floor | ≤floor? | p^{{e−1}} |
|---|---:|---:|---:|---:|---|---:|
{ptbl}

## Co-extension census (prefix enforced)

| j | w | fc | #H coext | max H/C | #C | min t | max t | t≥2e? |
|---|---|---:|---:|---:|---:|---:|---:|---|
{ctbl}

Census: max H/C={cen['max_coext_H_per_C']}; max coext H={cen['max_coext_nH']}.

## Path to residual card

```text
SR + Type D + H_M
  → pure-untyped free-1 highs
  → H_*^{{pre}} on I_t, t=min(C) ∈ [2e,n']
  → need max H_*^{{pre}} ≤ H2 (or H2/N_C)
```

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v49.py --check
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
        "# kb-qatom-route-d-v49\n\n"
        "Co-extension free-1 multipads live in index prefixes of D.\n"
    )
    REPORT_PATH.write_text(
        f"# v49 report\n\nstatus: {cert['status']}\n"
        f"prefix window: PROVED\n"
        f"OPEN Hstar_pre deployed: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  coext free-1 ⇒ U ⊆ I_t, t=min(C): PROVED")
    print(f"  multipad window t ∈ [{T_MIN}, {N_PRIME}]: PROVED")
    print("  |H_coext(C)| ≤ H_*^{pre}(t,e): PROVED")
    print(f"  e=2 prefix ≤p≤H2: PROVED; deployed e={E}")
    print(
        f"  toys: max H/C={cen['max_coext_H_per_C']}; "
        f"max prefix nH={cen['max_prefix_nH']}"
    )
    print(f"  OPEN ★_pre: max_t H_*^{{pre}}(t,{E}) ≤ H2={H2}")


if __name__ == "__main__":
    main()
