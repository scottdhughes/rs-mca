#!/usr/bin/env python3
"""KB-MCA Route-D v69: multipads are disjoint; injectivity for t < 2e.

Structural close-path after v68 injectivity program.

Proved:
  (1) Multipads are root-disjoint (any field, any ambient set). If U != V are
      free-1 multipads (same monic free-1 high), then the monic polynomials
      satisfy f_U - f_V = delta (nonzero constant). A common root r would give
      0 - 0 = delta, contradiction. Hence U cap V = empty and |U cup V| = 2e.
  (2) Same derivative. f_U - f_V constant => f_U' = f_V' (char 0 or char > e
      so monic degree-e derivative is well-defined of degree e-1).
  (3) Threshold injectivity. If t < 2e then no two disjoint e-subsets of an
      ambient t-set exist, hence no free-1 multipads, hence free-1 high is
      injective on e-subsets of I_t, hence coll=0 and |T|=0 (v68).
  (4) GP index form. For U = {omega^a : a in A} subset mu_n with A subset
      {0,...,t-1}, the power sums are
        p_k(U) = sum_{a in A} omega^{a k}.
      Free-1 multipad of power-sum type (char > e) <=> A != B, |A|=|B|=e,
      and sum_{a in A} omega^{a k} = sum_{b in B} omega^{b k} for k=1..e-1
      (and automatically k=0 by equal size). With (1), A cap B = empty.
  (5) Deployed regime. n' = 1183520, e = 67472, 2e = 134944, n' > 2e
      (floor(n'/e)=17). Threshold (3) does NOT close deployed; need a GP-specific
      multipad obstruction for t >= 2e.

CAS:
  (6) All multipads on tested GP arcs have inter=0 and |cup|=2e.
  (7) t < 2e rows: always injective (coll=0).
  (8) t >= 2e: multipads appear (e=3,4 toys) but always disjoint.
  (9) Level-set check: U = {x in arc : f_V(x) = -delta} on tested multipads.

OPEN:
  Forbid disjoint multipads A,B subset {0..n'-1} with matching GP power sums
  p_k for k=1..e-1 at deployed (n',e), or prove SoftB.

Does NOT claim deployed injectivity; does NOT claim A_SP<=t*p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v69.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v69"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v69.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v69.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v69.report.md"
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


def lemma_disjoint() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_multipads_are_disjoint",
        "statement": (
            "Any free-1 multipad pair U!=V satisfies U cap V = empty and "
            "|U cup V| = 2e."
        ),
        "proof": [
            "Same free-1 monic high => f_U - f_V = delta (nonzero constant).",
            "If r in U cap V then f_U(r)=f_V(r)=0 => delta=0, contradiction.",
            "|U|=|V|=e and disjoint => |cup|=2e.",
        ],
    }


def lemma_same_derivative() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multipad_same_derivative",
        "statement": (
            "Free-1 multipad monic polys satisfy f_U' = f_V' "
            "(identical derivatives)."
        ),
        "proof": ["f_U - f_V constant => derivatives equal."],
    }


def lemma_threshold_inj() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "injectivity_when_t_lt_2e",
        "statement": (
            "If t < 2e then free-1 high is injective on e-subsets of any t-set, "
            "hence coll=0 and |T|=0."
        ),
        "proof": [
            "Multipad needs two disjoint e-sets => at least 2e ambient points.",
            "t < 2e forbids multipads => injective => v68 close.",
        ],
    }


def lemma_gp_index() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "GP_power_sum_index_form",
        "statement": (
            "For U={omega^a : a in A}, p_k(U)=sum_{a in A} omega^{a k}; "
            "power-sum free-1 multipad <=> matching DFT moments k=1..e-1 "
            "on index sets A,B of size e (disjoint by (1))."
        ),
        "proof": [
            "Direct expansion p_k = sum_{a in A} (omega^a)^k = sum_a omega^{a k}.",
            "v56: free-1 monic high <=> power sums in char > e.",
        ],
    }


def lemma_deployed_not_threshold() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "deployed_exceeds_2e_threshold",
        "statement": (
            f"Deployed n'={N_PRIME} >= 2e={TWO_E} (ratio n'/e={N_PRIME/E:.4f}); "
            "threshold injectivity (3) does not apply; GP multipad ban still open."
        ),
        "proof": [f"2e={TWO_E}, n'={N_PRIME}, floor(n'/e)={FLOOR_NP}."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_no_GP_multipad_at_deployed",
        "statement": (
            "No disjoint A,B subset {0..n'-1}, |A|=|B|=e, with "
            "sum_{a in A} omega^{a k} = sum_{b in B} omega^{b k} for all "
            "k=1..e-1 (deployed omega of order n)."
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


def monic_X(roots: list[int], p: int) -> list[int]:
    """Standard monic prod (X-r), coeffs low to high, leading 1."""
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


def eval_poly(poly: list[int], x: int, p: int) -> int:
    s = 0
    xp = 1
    for c in poly:
        s = (s + c * xp) % p
        xp = (xp * x) % p
    return s


def census(p: int, n: int, t: int, e: int) -> dict[str, Any]:
    vals = domain_vals(p, n)[:t]
    buckets: dict[tuple[int, ...], list[tuple[tuple[int, ...], list[int], list[int]]]] = (
        defaultdict(list)
    )
    for idxs in itertools.combinations(range(t), e):
        roots = [vals[i] for i in idxs]
        poly = monic_X(roots, p)
        buckets[free1_X(poly, e)].append((idxs, roots, poly))

    C = math.comb(t, e)
    coll = 0
    max_m = 1
    multipad_pairs = 0
    inters: list[int] = []
    cups: list[int] = []
    level_ok = 0
    level_checked = 0

    for h, lst in buckets.items():
        m = len(lst)
        max_m = max(max_m, m)
        if m >= 2:
            coll += m * (m - 1)
        for a, b in itertools.combinations(lst, 2):
            ia, ra, pa = a
            ib, rb, pb = b
            UA, UB = set(ra), set(rb)
            inter = len(UA & UB)
            cup = len(UA | UB)
            inters.append(inter)
            cups.append(cup)
            multipad_pairs += 1
            ensure(inter == 0, "disjoint")
            ensure(cup == 2 * e, "cup 2e")
            # poly differ only in constant
            ensure(pa[1:e] == pb[1:e], "free1")
            ensure(pa[e] == 1 and pb[e] == 1, "monic")
            delta = (pa[0] - pb[0]) % p
            ensure(delta != 0, "delta")
            # level set: U = {x in arc: f_V(x) = -delta}
            if level_checked < 8:
                lev = {x for x in vals if eval_poly(pb, x, p) == (-delta) % p}
                ensure(lev == UA, "level set U")
                level_ok += 1
                level_checked += 1

    return {
        "p": p,
        "t": t,
        "e": e,
        "C": int(C),
        "distinct": len(buckets),
        "max_m": int(max_m),
        "coll": int(coll),
        "multipad_pairs": int(multipad_pairs),
        "injective": bool(max_m == 1),
        "t_lt_2e": bool(t < 2 * e),
        "all_multipads_disjoint": bool(all(i == 0 for i in inters)) if inters else True,
        "all_cups_2e": bool(all(c == 2 * e for c in cups)) if cups else True,
        "level_ok": int(level_ok),
        "min_inter": int(min(inters)) if inters else None,
        "max_inter": int(max(inters)) if inters else None,
    }


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "char")
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(FLOOR_NP == 17, "k")
    ensure(N_PRIME > TWO_E, "deployed t>2e")
    ensure(N_PRIME // E == 17, "pack")
    ensure(P > E, "char>e")

    rows = []
    # threshold regime t < 2e: must be injective
    for p, n in [(61, 60), (101, 100), (127, 126)]:
        for e in [3, 4, 5]:
            for t in [e, e + 1, 2 * e - 1]:
                if t > n or math.comb(t, e) > 25000:
                    continue
                r = census(p, n, t, e)
                ensure(r["t_lt_2e"], "flag")
                ensure(r["injective"], f"threshold inj p={p} e={e} t={t}")
                ensure(r["coll"] == 0, "coll0")
                rows.append(r)

    # multipad regime t >= 2e
    multi_rows = []
    for p, n, t, e in [
        (61, 60, 17, 3),
        (61, 60, 24, 3),
        (101, 100, 17, 3),
        (101, 100, 21, 4),
        (127, 126, 18, 3),
        (127, 126, 21, 4),
        (61, 60, 21, 4),
    ]:
        if math.comb(t, e) > 40000:
            continue
        r = census(p, n, t, e)
        ensure(r["all_multipads_disjoint"], "disjoint")
        ensure(r["all_cups_2e"], "cup")
        multi_rows.append(r)
        rows.append(r)

    ensure(any(r["multipad_pairs"] > 0 for r in multi_rows), "some multipads")
    ensure(all(r["injective"] for r in rows if r["t_lt_2e"]), "all threshold")

    return {
        "status": "PASS",
        "rows": rows,
        "summary": {
            "n_rows": len(rows),
            "n_threshold_inj": sum(1 for r in rows if r["t_lt_2e"]),
            "n_with_multipads": sum(1 for r in rows if r["multipad_pairs"] > 0),
            "all_threshold_injective": True,
            "all_multipads_disjoint": True,
            "all_cups_2e": True,
            "deployed_n_prime": N_PRIME,
            "deployed_e": E,
            "deployed_2e": TWO_E,
            "deployed_t_ge_2e": True,
            "deployed_floor_n_over_e": FLOOR_NP,
            "B_star": float(B_STAR),
            "H2": H2,
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "two_e": TWO_E,
            "p": P,
            "H2": H2,
            "B_star": float(B_STAR),
            "threshold_closes_deployed": False,
            "note": (
                "multipads disjoint + t<2e injectivity PROVED; "
                "deployed n'>=2e so GP multipad ban still open"
            ),
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v69",
        "title": "Multipads disjoint; injectivity for t<2e",
        "status": "DISJOINT_THRESHOLD_PROVED_DEPLOYED_GP_OPEN",
        "claims": {
            "proves_multipads_disjoint": True,
            "proves_multipad_same_derivative": True,
            "proves_injectivity_when_t_lt_2e": True,
            "proves_GP_index_power_sum_form": True,
            "proves_deployed_exceeds_2e": True,
            "proves_deployed_injectivity": False,
            "proves_SoftB_Deployed": False,
            "proves_T_le_H2_deployed": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "disjoint": lemma_disjoint(),
            "same_derivative": lemma_same_derivative(),
            "threshold_inj": lemma_threshold_inj(),
            "gp_index": lemma_gp_index(),
            "deployed_not_threshold": lemma_deployed_not_threshold(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {"python_nt": "GP multipad census + level sets"},
        "impact_on_program": {
            "closed": (
                "Multipads always disjoint (root argument); "
                "t<2e => injectivity => |T|=0"
            ),
            "wall": f"deployed n'={N_PRIME} >= 2e={TWO_E}: ban GP multipads",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    s = cert["toy_suite"]["summary"]
    d = cert["deployed"]
    lines = []
    for r in cert["toy_suite"]["rows"]:
        lines.append(
            f"| {r['p']} | {r['e']} | {r['t']} | "
            f"{'Y' if r['t_lt_2e'] else 'n'} | "
            f"{'Y' if r['injective'] else 'n'} | {r['multipad_pairs']} | "
            f"{r['max_m']} | {r['coll']} |"
        )
    tbl = "\n".join(lines)
    return f"""# KB-MCA Route-D v69: multipads disjoint; `t < 2e` injectivity

Status: **disjointness + threshold injectivity PROVED**; deployed GP multipad ban
**OPEN**. Local on `scott/kb-route-d-T-bound`.

## Multipads are disjoint (PROVED, ambient-independent)

```text
f_U - f_V = delta != 0  (same free-1 high)
r in U cap V  =>  f_U(r)=f_V(r)=0  =>  delta=0  contradiction
=>  U cap V = empty,  |U cup V| = 2e
f_U' = f_V'
```

## Threshold injectivity (PROVED)

```text
t < 2e  =>  no two disjoint e-subsets
        =>  no multipads
        =>  free-1 high injective
        =>  coll = 0  =>  |T| = 0     (v68)
```

## Deployed numbers

| symbol | value |
|---|---:|
| e | {d['e']} |
| 2e | {d['two_e']} |
| n' | {d['n_prime']} |
| n' >= 2e? | **yes** (threshold does not close) |
| floor(n'/e) | {s['deployed_floor_n_over_e']} |

## GP index form (PROVED)

```text
U = {{ omega^a : a in A }}
p_k(U) = sum_{{a in A}} omega^{{a k}}
multipad <=> disjoint A,B size e with equal moments k=1..e-1
```

## CAS

| p | e | t | t&lt;2e? | inj? | #mp pairs | max m | coll |
|---|---:|---:|---|---|---:|---:|---:|
{tbl}

- all `t < 2e` rows injective
- all multipad pairs disjoint with cup size 2e
- level-set identity checked on sample multipads

## Link

| result | status |
|---|---|
| injectivity => |T|=0 | CLOSED (v68) |
| **t &lt; 2e => injectivity** | **CLOSED (v69)** |
| multipads disjoint | CLOSED (v69) |
| deployed injectivity | OPEN (n' &gt; 2e) |
| SoftB fallback | OPEN |

## OPEN

Forbid disjoint index multipads on `{{0..n'-1}}` with matching GP power sums
`k=1..e-1` at deployed parameters (or SoftB).

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v69.py --check
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
        "# kb-qatom-route-d-v69\n\n"
        "Multipads disjoint; injectivity for t<2e; deployed GP multipad ban OPEN.\n"
    )
    s = cert["toy_suite"]["summary"]
    REPORT_PATH.write_text(
        f"# v69 report\n\nstatus: {cert['status']}\n"
        f"multipads disjoint: PROVED\n"
        f"t<2e injectivity: PROVED\n"
        f"deployed n'>=2e: yes (open GP ban)\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free-1 multipads are disjoint (|cup|=2e): PROVED")
    print("  t < 2e => injectivity => |T|=0: PROVED")
    print("  GP index power-sum form: PROVED")
    print(
        f"  deployed: n'={s['deployed_n_prime']} >= 2e={s['deployed_2e']} "
        f"(threshold does NOT close); floor(n'/e)={s['deployed_floor_n_over_e']}"
    )
    print(
        f"  CAS: rows={s['n_rows']}; threshold inj={s['n_threshold_inj']}; "
        f"multipad rows={s['n_with_multipads']}; all multipads disjoint"
    )
    print("  OPEN: no GP multipad at deployed (or SoftB)")


if __name__ == "__main__":
    main()
