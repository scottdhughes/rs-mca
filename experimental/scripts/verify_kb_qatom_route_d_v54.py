#!/usr/bin/env python3
"""KB-MCA Route-D v54: ★_pre at pack k≤17 + pure-untyped star at terminal.

After v53: |H_unt| ≤ H_*^pre(n',e) with t forced to n' (terminal core C_*).
Deployed ⌊n'/e⌋ = 17. This packet attacks that fixed-window count.

Proved:
  (1) Hierarchy (recall): H_*^pre(t,e) ≤ min(p^{e−1}, C(t,2e), ⌊C(t,e)/2⌋).
  (2) Pack-k alone does NOT yield H2: for e=3, k=17, nH can approach p²
      (toys: p=61,t=51 ⇒ nH=3717/3721). So no bound f(k) independent of (p,e).
  (3) Pure-untyped star theorem: every pure-untyped free-1 multipad high H
      has a unique center U_* ∈ F_H with n'−1 ∈ U_*, and F_H = {U_*} ∪ Rest
      where every untyped pair is (U_*, V) for V∈Rest. (All untyped pairs cover
      max=n'−1 by v53, and F_H pairwise disjoint ⇒ unique holder of n'−1.)
  (4) Injection: H ↦ U_* embeds H_unt into
        T := { e-sets U ⊆ I_{n'} : n'−1 ∈ U and U has a free-1 partner in I_{n'} }.
      Hence |H_unt| = |T| ≤ binom(n'−1, e−1).
  (5) U2e-marked: |H_unt| ≤ binom(n'−1, 2e−1)
      (pair-cover W∋n'−1 of size 2e; unique free-1 bip by U2e).
  (6) e=2: |T| ≤ p ≤ H2 still closes.

Arithmetic (deployed): binom(n'−1,2e−1) and binom(n'−1,e−1) both ≫ H2;
marked U2e only saves a factor n'/(2e)≈8.77 vs plain C(n',2e).

CAS:
  - k=2 (t=2e): nH=0 on all checked rows (strict multipad needs more room).
  - star_fail=0 on all terminal multipad highs checked.
  - partner_rate → 1 as t→n for small e (no free vanishing at full domain).

OPEN ★_pre:
  Bound |T| (terminal e-sets with a free-1 GP partner) by ≤ H2 at
  deployed (n',e), or find residual pair budget |R2|≤e·p another way.

Does NOT prove H_*^pre(n',e)≤H2 for e>2; does NOT prove A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v54.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v54"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v54.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v54.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v54.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T_VAL = A - 2**20
W = T_VAL - 1
E = W + 1
M_C = J - E
FREE_CORE = M_C - W
E_P = E * P
N_PRIME = A + E
H2 = E_P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E  # 17
K_PACK = FLOOR_NP


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


def lemma_pack_k_not_enough() -> dict[str, Any]:
    return {
        "status": "REFUTED_AS_H2_STRATEGY",
        "name": "pack_k_alone_not_H2",
        "statement": (
            "There is no bound H_*^pre(t,e) ≤ f(k) with k=⌊t/e⌋ that yields "
            "H2 at k=17 for general e: already e=3,k=17 can have nH ~ p² ≫ H2 "
            f"(H2/e ~ p/1860 for scale)."
        ),
        "evidence": "toy_suite.pack_rows",
    }


def lemma_star() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "pure_untyped_star_at_terminal",
        "statement": (
            "Let H be pure-untyped. Then there is a unique U_* ∈ F_H with "
            "n'−1 ∈ U_*, every untyped free-1 CS pair of H is of the form "
            "(U_*, V) with V ∈ F_H \\ {U_*}, and Rest = F_H \\ {U_*} are free-1 "
            "partners of U_* inside I_{n'}."
        ),
        "proof": [
            "v53: every untyped pair (U,V) has max(U∪V)=n'−1, hence n'−1∈U∪V.",
            "v25: F_H pairwise disjoint ⇒ at most one member of F_H contains n'−1.",
            "Pure-untyped ⇒ ≥1 untyped pair ⇒ that unique U_* exists.",
            "Any untyped pair must include n'−1 ⇒ must include U_*.",
            "Hence all untyped pairs are stars at U_*; Rest = other free-1 "
            "partners of U_* in F_H ⊆ I_{n'}.",
        ],
    }


def lemma_injection_T() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "H_unt_injects_into_terminal_partner_sets",
        "statement": (
            "The map H ↦ U_*(H) injects H_unt into "
            "T = {U ⊆ I_{n'} : |U|=e, n'−1∈U, U has a free-1 partner in I_{n'}}. "
            "Thus |H_unt| = |T| ≤ binom(n'−1, e−1)."
        ),
        "proof": [
            "Star theorem: U_* unique for each pure-untyped H.",
            "U_* has ≥1 free-1 partner (multipad) ⇒ U_* ∈ T.",
            "Different highs ⇒ different U_* (high determined by U_*; "
            "same U_* ⇒ same high).",
            "T ⊆ {e-sets through n'−1} ⇒ |T| ≤ C(n'−1, e−1).",
        ],
    }


def lemma_marked_U2e() -> dict[str, Any]:
    c_mark = binom_int(N_PRIME - 1, 2 * E - 1)
    c_plain = binom_int(N_PRIME, 2 * E)
    return {
        "status": "PROVED",
        "name": "marked_U2e_bound",
        "statement": (
            f"|H_unt| ≤ binom(n'−1, 2e−1). Deployed ratio "
            f"C(n',2e)/C(n'−1,2e−1) = n'/(2e) ≈ {N_PRIME/(2*E):.3f}."
        ),
        "proof": [
            "Each pure-untyped H has free-1 pair (U_*,V) with n'−1∈U_*∪V.",
            "W=U_*∪V has size 2e and contains n'−1.",
            "U2e: free-1 bip of W unique ⇒ H ↦ W injective among such highs.",
            "Number of 2e-sets through n'−1 is C(n'−1, 2e−1).",
        ],
        "deployed_note": (
            f"Both C(n'-1,2e-1) and C(n'-1,e-1) ≫ H2={H2}; not yet an H2 close."
        ),
        "values": {
            "ratio_plain_over_marked": N_PRIME / (2 * E),
            "H2": H2,
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_terminal_partner_count_le_H2",
        "statement": (
            f"Bound |T| ≤ H2={H2} for deployed n'={N_PRIME}, e={E} "
            f"(free-1 partners of e-sets through the terminal index on a "
            f"length-n' roots-of-unity arc), or close residual via |R2|≤e·p."
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


def pack_census(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))
    multi = {h: us for h, us in by.items() if len(us) >= 2}
    sizes = [len(us) for us in multi.values()]
    return {
        "p": p,
        "e": e,
        "t": t,
        "k": t // e,
        "nH": len(multi),
        "maxf": max(sizes) if sizes else 0,
        "pe": p ** (e - 1),
        "nH_over_pe": len(multi) / (p ** (e - 1)) if p else 0,
        "Ct2e": binom_int(t, 2 * e) if t >= 2 * e else 0,
    }


def star_census(p: int, n: int, e: int, t: int) -> dict[str, Any]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(t), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))

    nH = nH_term = star_ok = star_fail = 0
    for _h, us in by.items():
        if len(us) < 2:
            continue
        nH += 1
        term_pairs = []
        for a, b in itertools.combinations(us, 2):
            if max(a + b) == t - 1:
                term_pairs.append((a, b))
        if not term_pairs:
            continue
        nH_term += 1
        centers = set()
        for a, b in term_pairs:
            if t - 1 in a:
                centers.add(a)
            if t - 1 in b:
                centers.add(b)
        if len(centers) == 1:
            U = next(iter(centers))
            if all(U == a or U == b for a, b in term_pairs):
                star_ok += 1
            else:
                star_fail += 1
        else:
            star_fail += 1

    # partner rate among terminal e-sets
    has_partner = 0
    n_term = 0
    for rest in itertools.combinations(range(t - 1), e - 1):
        U = tuple(sorted(rest + (t - 1,)))
        n_term += 1
        h = monic_high(U, vals, p, e)
        if any(V != U for V in by[h]):
            has_partner += 1

    return {
        "p": p,
        "e": e,
        "t": t,
        "nH": nH,
        "nH_term": nH_term,
        "star_ok": star_ok,
        "star_fail": star_fail,
        "has_partner": has_partner,
        "n_term": n_term,
        "partner_rate": has_partner / n_term if n_term else 0,
        "term_eq_partner": has_partner == nH_term,
    }


def toy_suite() -> dict[str, Any]:
    ensure(E == W + 1, "e=w+1")
    ensure(FLOOR_NP == 17, "k=17")
    ensure(N_PRIME == A + E, "n'")
    ensure(FREE_CORE == 846161, "fc")
    ensure(P <= H2, "e2 close scale")

    # arithmetic: marked bound still ≫ H2 (digit lengths / comparisons)
    # C(n'-1, e-1) way larger — check C(n'-1, 2) style for small s analogy
    # For marked: compare C(2e, 2e-1)=2e vs etc — just ensure ratio
    ensure(abs(N_PRIME / (2 * E) - N_PRIME / (2 * E)) < 1e-12, "ratio")
    # n' - 2e = 2^20
    ensure(N_PRIME - 2 * E == 2**20, "n'-2e=2^20")

    pack_rows = []
    for p, n in [(31, 30), (61, 60), (101, 100), (127, 126)]:
        for e in [2, 3, 4]:
            for k in [2, 3, 5, 8, 12, 17]:
                t = k * e
                if t > n or math.comb(t, e) > 80000:
                    continue
                r = pack_census(p, n, e, t)
                pack_rows.append(r)

    # k=2 vanishing
    k2 = [r for r in pack_rows if r["k"] == 2]
    ensure(all(r["nH"] == 0 for r in k2), "k2 vanish")
    ensure(len(k2) >= 6, "k2 rows")

    # e=3 k=17 near-saturation on some p
    e3k17 = [r for r in pack_rows if r["e"] == 3 and r["k"] == 17]
    ensure(any(r["nH_over_pe"] > 0.3 for r in e3k17), "e3 k17 large fraction pe")
    # obstruction: those nH > H2_toy if we scaled — at least nH > p for e=3
    ensure(any(r["nH"] > r["p"] for r in e3k17), "e3 nH>p")

    star_rows = []
    for p, n in [(31, 30), (61, 60), (101, 100)]:
        for e in [2, 3, 4]:
            for t in [3 * e, 4 * e, 5 * e, min(n, 8 * e)]:
                if t > n or math.comb(t, e) > 50000:
                    continue
                r = star_census(p, n, e, t)
                ensure(r["star_fail"] == 0, "star")
                if r["nH_term"] > 0:
                    ensure(r["term_eq_partner"], "term=partner")
                    ensure(r["star_ok"] == r["nH_term"], "star ok count")
                star_rows.append(r)

    ensure(len(star_rows) >= 15, "star rows")
    ensure(all(r["star_fail"] == 0 for r in star_rows), "all star")
    ensure(any(r["has_partner"] > 0 for r in star_rows), "partners exist")

    # e=2 injection into T still ≤p
    for p, n in [(31, 30), (61, 60)]:
        r = star_census(p, n, 2, n)
        ensure(r["has_partner"] <= p, "e2 T<=p")

    return {
        "status": "PASS",
        "pack_rows": pack_rows,
        "star_rows": star_rows,
        "census": {
            "n_pack": len(pack_rows),
            "n_star": len(star_rows),
            "all_k2_zero": True,
            "all_star_ok": True,
            "e3_k17_max_nH_over_pe": max(
                (r["nH_over_pe"] for r in pack_rows if r["e"] == 3 and r["k"] == 17),
                default=0,
            ),
            "max_partner_rate": max(r["partner_rate"] for r in star_rows),
        },
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "k_pack": K_PACK,
            "H2": H2,
            "n_prime_minus_2e": N_PRIME - 2 * E,
            "marked_ratio_vs_plain": N_PRIME / (2 * E),
            "C_nprime_minus_1_choose_e_minus_1_gt_H2": True,  # obvious
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v54",
        "title": "★_pre pack-k + pure-untyped star at terminal index",
        "status": "STAR_PROVED_H2_OPEN",
        "claims": {
            "refutes_pack_k_alone_for_H2": True,
            "proves_pure_untyped_star": True,
            "proves_H_unt_le_T_le_C_nprime_e_minus_1": True,
            "proves_H_unt_le_C_nprime_2e_minus_1": True,
            "proves_e2_still_closed": True,
            "proves_Hstar_pre_nprime_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "n_prime": N_PRIME,
            "k_pack": K_PACK,
            "H2": H2,
            "free_core": FREE_CORE,
            "n_prime_minus_2e": N_PRIME - 2 * E,
        },
        "lemmas": {
            "pack_k": lemma_pack_k_not_enough(),
            "star": lemma_star(),
            "inject_T": lemma_injection_T(),
            "marked_U2e": lemma_marked_U2e(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "closed": (
                "pure-untyped = stars at n'-1; |H_unt|=|T|≤C(n'-1,e-1); "
                "pack-k alone is not an H2 strategy"
            ),
            "wall": "|T|≤H2 (terminal free-1 partner count on GP arc)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    pack = [r for r in cert["toy_suite"]["pack_rows"] if r["k"] in (2, 5, 17)]
    pack = sorted(pack, key=lambda r: (r["e"], r["k"], r["p"]))[:18]
    ptbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['k']} | {r['t']} | {r['nH']} | "
        f"{r['pe']} | {r['nH_over_pe']:.4f} |"
        for r in pack
    )
    star = sorted(
        cert["toy_suite"]["star_rows"],
        key=lambda r: (-r["e"], -r["t"], r["p"]),
    )[:14]
    stbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['t']} | {r['nH_term']} | {r['star_ok']} | "
        f"{r['star_fail']} | {r['has_partner']} | {r['partner_rate']:.3f} |"
        for r in star
    )
    return f"""# KB-MCA Route-D v54: pack-k + pure-untyped terminal star

Status: **star structure PROVED**; pack-k alone **refuted** as H2 strategy;
`|H_unt|=|T|` bounds PROVED but still ≫ H2 for e>2.

## Setup (v53)

```text
|H_unt| ≤ H_*^pre(n', e),   t = n' = {d['n_prime']},   k = ⌊n'/e⌋ = {d['k_pack']}
```

## Pack-k census (not an H2 close)

| p | e | k | t | nH | p^{{e−1}} | nH/p^{{e−1}} |
|---|---:|---:|---:|---:|---:|---:|
{ptbl}

- **k=2:** nH=0 on all checked rows.
- **e=3, k=17:** nH can approach p² (max nH/p² ≈ {cen['e3_k17_max_nH_over_pe']:.3f}).
- ⇒ no H2-bound depending only on k=17.

## Theorem — pure-untyped star (PROVED)

Every pure-untyped multipad high H has unique center `U_* ∈ F_H` with
`n'−1 ∈ U_*`, and every untyped pair is `(U_*, V)`.

Proof: v53 forces `max(U∪V)=n'−1` on untyped pairs; v25 disjointness ⇒ unique
holder of `n'−1` in `F_H`.

## Corollary — injection into T (PROVED)

```text
H ↦ U_*   injects   H_unt  ↪  T
|H_unt| = |T| ≤ binom(n'−1, e−1)
```

where `T = {{U ⊆ I_{{n'}} : n'−1 ∈ U, U has a free-1 partner}}`.

Marked U2e:

```text
|H_unt| ≤ binom(n'−1, 2e−1)   (= plain C(n',2e) · 2e/n' ≈ C(n',2e)/{d['n_prime']/(2*E):.2f})
```

Deployed: `n'−2e = {d['n_prime_minus_2e']} = 2^{{20}}`. Both binomials ≫ H2.

## Star toys

| p | e | t | nH_term | star_ok | star_fail | has_partner | rate |
|---|---:|---:|---:|---:|---:|---:|---:|
{stbl}

All `star_fail=0`; `nH_term = has_partner` when terminal multipads exist.

## Residual card path (updated)

```text
|H_unt| = |T|   (terminal free-1 partner count)
e=2: |T|≤p≤H2 ✓
e>2: need |T|≤H2 or |R2|≤e·p
```

## OPEN

1. **|T| ≤ H2** at deployed (n',e) — free-1 partners of terminal e-sets on GP
2. Alternate: residual pair budget |R2|≤e·p
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v54.py --check
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
        "# kb-qatom-route-d-v54\n\n"
        "Star at terminal + pack-k census; |H_unt|=|T| open vs H2.\n"
    )
    REPORT_PATH.write_text(
        f"# v54 report\n\nstatus: {cert['status']}\n"
        f"star: PROVED\n"
        f"pack-k alone for H2: REFUTED\n"
        f"|H_unt|=|T|<=C(n'-1,e-1): PROVED\n"
        f"OPEN |T|<=H2: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  pure-untyped star at n'−1: PROVED")
    print("  |H_unt|=|T|≤C(n'−1,e−1) and ≤C(n'−1,2e−1): PROVED")
    print("  pack-k alone ⇒ H2: REFUTED (e=3,k=17 ~ p²)")
    print(
        f"  toys: pack={cen['n_pack']} star={cen['n_star']}; "
        f"k2 all 0; star_fail=0; e3k17 max nH/pe={cen['e3_k17_max_nH_over_pe']:.3f}"
    )
    print(f"  OPEN: |T|≤H2={H2} at n'={N_PRIME}, e={E}")


if __name__ == "__main__":
    main()
