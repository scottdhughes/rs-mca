#!/usr/bin/env python3
"""KB-MCA Route-D v55: attack |T| ≤ H2 — structure, entropy, CAS.

Primary wall after v53–v54:
  |H_unt| = |T|,
  T = { e-sets U ⊆ I_{n'} : n'−1 ∈ U and U has a free-1 partner on I_{n'} }.
Close residual card if |T| ≤ H2 (e=2 already via |T|≤p≤H2).

Proved:
  (1) Bound hierarchy (char ≠ 2 for marked U2e):
        |T| ≤ min( p^{e−1}, binom(n'−1, e−1), binom(n'−1, 2e−1) ).
      Reasons: high injection; terminal e-sets; marked free-1 pair-cover (v51/v54).
  (2) e=2: |T| ≤ min(p, n'−1) ≤ p ≤ H2 — residual path CLOSED for e=2.
  (3) Star recall (v54): pure-untyped highs biject with T.

CAS / heuristics (not a deployed proof):
  (4) For e≥3, ambient |T| can exceed p (e.g. p=31,e=3,t=30 ⇒ |T|=406).
      So |T|≤p is false for e≥3; need stronger structure or deployed regime.
  (5) e=3 growth: |T| rises smoothly with t (toys), not sparse at t~p/3.
  (6) Deployed entropy (random high map model): with N = C(n',e) balls into
      p^{e−1} bins,
        E[# colliding pairs] ≈ N²/(2 p^{e−1})  has  log2 ≈ −1.34×10^6
      i.e. astronomically <1.  Heuristic: multipads (hence T) are empty at
      deployed (e,n',p).  NOT a theorem — highs of GP e-sets are algebraic,
      not random, and e=2 is a structured counterexample to “always empty”.

OPEN:
  Prove |T|≤H2 (or T=∅) at deployed (n',e,p) using GP/free-1 algebra —
  not random heuristics alone.  Alternate: |R2|≤e·p.

Tools used this packet: Python NT venv (exact enum), Sage (e=3 power-sum
cross-check), log-combinatorial arithmetic for deployed entropy.
  (Wolfram Engine present but activation gate blocked this session.)

Does NOT claim |T|≤H2 at deployed e>2; does NOT claim A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v55.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v55"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v55.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v55.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v55.report.md"
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
E_P = E * P
N_PRIME = A + E
H2 = E_P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def lemma_hierarchy() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "T_bound_hierarchy",
        "statement": (
            f"|T| ≤ min(p^{{e−1}}, C(n'−1,e−1), C(n'−1,2e−1)) "
            f"with n'={N_PRIME}, e={E}."
        ),
        "proof": [
            "High map U↦monic high ∈ F_p^{e−1}: different T-sets can share a high "
            "only as multipad partners; |image of multipad highs through terminal| "
            "≤ p^{e−1}, and H↦U_* injects so |T|≤p^{e−1}.",
            "T ⊆ {e-sets through n'−1} ⇒ |T|≤C(n'−1,e−1).",
            "Marked U2e (v51/v54): free-1 pair-cover through n'−1 ⇒ |T|≤C(n'−1,2e−1).",
        ],
    }


def lemma_e2() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_T_le_p_le_H2",
        "statement": "For e=2: |T| ≤ min(p, n'−1) ≤ p ≤ H2.",
        "proof": [
            "e=2 free-1 ⇔ equal pair-sums (char≠2).",
            "Multipad highs inject into F_p (the common sum) ⇒ ≤p (v48).",
            "T ⊆ terminal 2-sets ⇒ ≤n'−1.",
            "Deployed p≤H2.",
        ],
    }


def lemma_entropy_heuristic() -> dict[str, Any]:
    log2_C = log2_comb(N_PRIME, E)
    log2_pe = (E - 1) * math.log2(P)
    log2_exp = 2 * log2_C - 1.0 - log2_pe  # N^2/(2 pe)
    return {
        "status": "HEURISTIC",
        "name": "deployed_random_model_expected_multipads",
        "statement": (
            "If free-1 highs of e-subsets of I_{n'} were uniform in F_p^{e−1}, "
            f"then E[# colliding pairs] ~ C(n',e)^2/(2 p^(e-1)) has log2 ~ {log2_exp:.1f} "
            f"(~ 10^({log2_exp/math.log2(10):.0f})), so <<1. Suggests T empty at deployed, "
            "but e=2 is a structured counterexample to 'always empty', so this is "
            "only a large-e heuristic."
        ),
        "values": {
            "log2_C_nprime_e": log2_C,
            "log2_p_to_e_minus_1": log2_pe,
            "log2_expected_colliding_pairs": log2_exp,
            "log2_H2": math.log2(H2),
            "e_over_nprime": E / N_PRIME,
            "nprime_over_p": N_PRIME / P,
            "k_pack": FLOOR_NP,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_T_le_H2_deployed",
        "statement": (
            f"Prove |T|≤H2={H2} (or T=∅) for deployed n'={N_PRIME}, e={E}, "
            f"p={P} on the KB roots-of-unity arc — using free-1/GP algebra, "
            "not only random-model entropy."
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


def T_census(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))
    nH = sum(1 for us in by.values() if len(us) >= 2)
    T = 0
    for rest in itertools.combinations(range(t - 1), e - 1):
        U = tuple(sorted(rest + (t - 1,)))
        if len(by[monic_high(U, vals, p, e)]) >= 2:
            T += 1
    return {
        "p": p,
        "n": n,
        "e": e,
        "t": t,
        "T": T,
        "nH": nH,
        "C_term": math.comb(t - 1, e - 1),
        "pe": p ** (e - 1),
        "T_le_pe": T <= p ** (e - 1),
        "T_le_C": T <= math.comb(t - 1, e - 1),
        "T_le_p": T <= p,
    }


def toy_suite() -> dict[str, Any]:
    ensure(E == W + 1, "e=w+1")
    ensure(N_PRIME == A + E, "n'")
    ensure(FREE_CORE == 846161, "fc")
    ensure(P <= H2, "p<=H2")
    ensure(FLOOR_NP == 17, "k")

    # entropy numbers finite
    h = lemma_entropy_heuristic()
    ensure(h["values"]["log2_expected_colliding_pairs"] < -1000, "entropy tiny")
    ensure(h["values"]["log2_C_nprime_e"] < h["values"]["log2_p_to_e_minus_1"], "C<<pe")

    rows = []
    for p, n in [(31, 30), (61, 60), (101, 100), (127, 126)]:
        for e in [2, 3, 4]:
            for t in [3 * e, 4 * e, 5 * e, min(n, 8 * e), n]:
                if t > n or t < 2 * e or math.comb(t, e) > 60000:
                    continue
                r = T_census(p, n, e, t)
                ensure(r["T_le_pe"], "T<=pe")
                ensure(r["T_le_C"], "T<=C")
                if e == 2:
                    ensure(r["T_le_p"], "e2 T<=p")
                rows.append(r)

    ensure(len(rows) >= 20, "rows")
    # e=2 saturates near full arc
    e2full = [r for r in rows if r["e"] == 2 and r["t"] == r["n"]]
    ensure(all(r["T"] == r["t"] - 1 or r["T"] <= r["p"] for r in e2full), "e2 full")
    # e=3 can beat p
    e3 = [r for r in rows if r["e"] == 3 and r["T"] > r["p"]]
    ensure(len(e3) >= 1, "e3 T>p exists")

    # hierarchy vs H2 for e=2 on toys
    ensure(all(r["T"] <= H2 for r in rows if r["e"] == 2), "e2 vs H2")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_rows": len(rows),
            "all_T_le_pe": True,
            "all_T_le_C": True,
            "all_e2_T_le_p": True,
            "e3_T_gt_p_examples": len(e3),
            "max_T": max(r["T"] for r in rows),
            "max_T_over_p": max(r["T"] / r["p"] for r in rows),
        },
        "entropy": h["values"],
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "H2": H2,
            "H2_over_p": H2 / P,
            "k_pack": FLOOR_NP,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v55",
        "title": "Attack |T|≤H2: hierarchy + deployed entropy heuristic",
        "status": "HIERARCHY_PROVED_DEPLOYED_T_OPEN",
        "claims": {
            "proves_T_hierarchy": True,
            "proves_e2_T_le_H2": True,
            "heuristic_deployed_T_empty": True,
            "proves_T_le_H2_deployed_e_gt_2": False,
            "proves_A_SP_le_tp": False,
            "refutes_T_le_p_for_e_ge_3": True,
        },
        "deployed": toys["deployed"],
        "lemmas": {
            "hierarchy": lemma_hierarchy(),
            "e2": lemma_e2(),
            "entropy": lemma_entropy_heuristic(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "tools": {
            "python_nt_venv": "exact GP free-1 enum + log-combinatorics",
            "sage": "e=3 power-sum cross-check (session)",
            "pari": "available; e=2 smoke",
            "wolfram": "activation gate this session — not used",
        },
        "impact_on_program": {
            "closed": "e=2 path; bound hierarchy; entropy shows random model empty",
            "wall": "algebraic proof |T|≤H2 at large deployed e",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    en = cert["toy_suite"]["entropy"]
    cen = cert["toy_suite"]["census"]
    rows = sorted(
        cert["toy_suite"]["rows"],
        key=lambda r: (r["e"], -r["t"], r["p"]),
    )[:20]
    tbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['t']} | {r['T']} | {r['nH']} | "
        f"{r['C_term']} | {r['pe']} | {r['T_le_p']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v55: attack `|T| ≤ H2`

Status: **hierarchy PROVED**; **e=2 CLOSED**; deployed e>2 still **OPEN**.
Random-model entropy strongly suggests `T=∅` at deployed scale (heuristic only).

## Setup (v53–v54)

```text
|H_unt| = |T|
T = {{ U ⊆ I_{{n'}} : |U|=e, n'−1 ∈ U, U has free-1 partner on I_{{n'}} }}
n'={d['n_prime']}, e={d['e']}, k=⌊n'/e⌋={d['k_pack']}, H2={d['H2']}
H2/p ≈ {d['H2_over_p']:.4f}
```

## Hierarchy (PROVED)

```text
|T|  ≤  min( p^{{e−1}},  binom(n'−1, e−1),  binom(n'−1, 2e−1) )
```

## e=2 (PROVED)

```text
|T| ≤ min(p, n'−1) ≤ p ≤ H2
```

## Deployed entropy heuristic (NOT a proof)

Random model: `C(n',e)` highs drawn uniformly in `F_p^{{e−1}}`:

| quantity | log2 |
|---|---:|
| `C(n',e)` | {en['log2_C_nprime_e']:.2f} |
| `p^{{e−1}}` | {en['log2_p_to_e_minus_1']:.2f} |
| `E[# colliding pairs] ≈ C²/(2 p^{{e−1}})` | **{en['log2_expected_colliding_pairs']:.1f}** |
| `H2` | {en['log2_H2']:.2f} |

So under uniformity, expected multipad pairs are `2^{{-1.3×10^6}}` — empty for all
practical purposes. **Caveat:** free-1 highs on a GP are algebraic; e=2 is a
structured regime with `|T|∼n'` multipads. Large-e needs a real GP argument.

## CAS (toys)

| p | e | t | \|T\| | nH | C(t−1,e−1) | p^{{e−1}} | T≤p? |
|---|---:|---:|---:|---:|---:|---:|---|
{tbl}

- All rows: `T ≤ p^{{e−1}}` and `T ≤ C(t−1,e−1)`.
- e=2: always `T ≤ p`.
- e≥3: **`T > p` occurs** ({cen['e3_T_gt_p_examples']}+ examples) — no `|T|≤p` for e>2.

## Residual card path

```text
e=2: |T|≤H2 ✓
e>2 deployed: need algebraic |T|≤H2 or T=∅  (entropy suggests empty)
alternate: |R2|≤e·p
```

## OPEN

1. **Prove** `|T|≤H2` or `T=∅` at deployed `(n',e)` on the KB arc.
2. Do not treat random-model entropy as a theorem.
3. `A_SP ≤ t·p`.

## Tools

- Python NT venv: exact enum + log-combinatorics
- Sage: e=3 elementary-symmetric cross-check
- PARI/GP, Oscar available for follow-up character-sum / FF work

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v55.py --check
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
        "# kb-qatom-route-d-v55\n\n"
        "Attack |T|<=H2: hierarchy proved; e=2 closed; deployed open; entropy heuristic.\n"
    )
    REPORT_PATH.write_text(
        f"# v55 report\n\nstatus: {cert['status']}\n"
        f"hierarchy: PROVED\n"
        f"e2: PROVED\n"
        f"deployed |T|<=H2: OPEN\n"
        f"entropy log2 E[pairs]: "
        f"{cert['toy_suite']['entropy']['log2_expected_colliding_pairs']:.1f}\n"
    )
    cen = cert["toy_suite"]["census"]
    en = cert["toy_suite"]["entropy"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  |T| hierarchy min(p^{e-1}, C(n'-1,e-1), C(n'-1,2e-1)): PROVED")
    print("  e=2 |T|≤p≤H2: PROVED")
    print(
        f"  entropy log2 E[multipad pairs] ≈ {en['log2_expected_colliding_pairs']:.1f} "
        "(heuristic T≈∅ deployed)"
    )
    print(
        f"  toys: {cen['n_rows']} rows; e3 T>p examples={cen['e3_T_gt_p_examples']}; "
        f"max T/p={cen['max_T_over_p']:.2f}"
    )
    print(f"  OPEN: prove |T|≤H2 at deployed e={E} (not just entropy)")


if __name__ == "__main__":
    main()
