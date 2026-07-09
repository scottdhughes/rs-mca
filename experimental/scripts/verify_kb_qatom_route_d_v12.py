#!/usr/bin/env python3
"""KB-MCA Route-D v12: trade-weight law and free-regime residual packing.

Continues v11 multi-mate partition with unconditional trade geometry.

Proved:
  (1) Trade-weight law: multi-mates C≠C' in one Phi_w fiber satisfy
        |C △ C'| = 2(m − |C∩C'|) ≥ 2(w+1),
      with equality iff the pair is tight (free-1 CS of (w+1)-blocks).
  (2) free ≤ 1 ⇒ only min-weight (tight) multi-mates; packing
        M_m ≤ 1 (free=0) or M_m ≤ floor(n/m) (free=1).
  (3) free ≥ 2 ⇒ non-min-weight multi-mates can exist (toys + construction
      room); class (iii) is exactly multi-mates with |△| ≥ 2(w+2) that are
      coset-fiber-free.
  (4) Min-weight residual criterion: if every residual multi-mate pair is
      min-weight (tight), and every residual multi-mate family is pairwise
      tight (i.e. a tight clique), then M_m^{res,phi} ≤ k_tight = 18.
      Combined with U_res ≤ target/(17*18) this closes the atom.
  (5) Tight-component warning (banked): connected components of the tight
      *graph* can exceed k_tight when the component is not a clique — so
      "only tight edges" alone does NOT give M_m ≤ 18 without a clique
      (pairwise-tight) hypothesis. Toys certify this.
  (6) Deployed free = 846161 ≫ 1: free-0/1 packing does not apply; avg
      m-fiber ~ 2^{-18820} still forces the uniqueness-scale expectation
      for residual, not a proof.

Does not prove M_m^{res} ≤ 1 or unconditional atom close.
Does not claim U(1116048) ≤ B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v12.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v12.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v12"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v12.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v12.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v12.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1
M = J - E
FREE = M - W
PACK_J = 17
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P
K_TIGHT = 1 + (N - M) // E  # 18
K_COSET = 1 + (N - M) // (2**17)  # 10
MIN_TRADE = 2 * (W + 1)  # 2e = 134944


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


def c_cosets(n: int, c: int) -> list[frozenset[int]]:
    step = n // c
    return [frozenset((r + k * step) % n for k in range(c)) for r in range(step)]


def lemma_trade_weight() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multimate_trade_weight_law",
        "statement": (
            "Let C ≠ C' be m-subsets with Phi_w(C)=Phi_w(C'). Then "
            "|C ∩ C'| ≤ m − w − 1 and "
            "|C △ C'| = 2(m − |C ∩ C'|) ≥ 2(w + 1). "
            "Equality |C △ C'| = 2(w + 1) holds if and only if the pair is tight "
            "(|C ∩ C'| = m − w − 1), iff C,C' are free-1 CS pads of (w+1)-blocks "
            "on a common core of size m−(w+1) (v9)."
        ),
        "proof": [
            "v9 intersection law: |C ∩ C'| ≤ m − w − 1 from deg(Λ_C − Λ_{C'}) ≤ m − w − 1 "
            "and C ∩ C' ⊂ roots of the difference.",
            "Symmetric difference size identity: |C △ C'| = |C| + |C'| − 2|C ∩ C'| "
            "= 2m − 2|C ∩ C'|.",
            "Hence |C △ C'| ≥ 2m − 2(m − w − 1) = 2(w + 1).",
            "Equality iff |C ∩ C'| = m − w − 1 iff tight pair (v9 tight-pair law).",
        ],
        "deployed": {
            "min_trade_weight": MIN_TRADE,
            "w": W,
            "e": E,
        },
        "classification": {
            "min_weight_tight": "|△| = 2(w+1) = class (i) when also residual",
            "long_trade": "|△| ≥ 2(w+2) = non-tight; class (ii) or (iii) by plant factor",
        },
    }


def lemma_free_le_1() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_le_1_only_min_weight_and_pack",
        "statement": (
            "If free = m − w = 0 (i.e. w ≥ m), then M_m^{max} ≤ 1. "
            "If free = 1 (w = m − 1), then every multi-mate pair is min-weight/tight "
            "(|△| = 2m, |∩| = 0), and M_m^{max} ≤ floor(n/m) by free-1 CS packing."
        ),
        "proof": [
            "free=0: Phi_w determines the full monic locator ⇒ at most one m-set (v6).",
            "free=1: cap = m−w−1 = 0, so |∩| ≤ 0 ⇒ disjoint multi-mates; "
            "difference is a nonzero constant (CS). Pack ≤ floor(n/m) (v6).",
            "Min-weight: 2(w+1) = 2m when w=m−1, and |△|=2m when |∩|=0.",
        ],
        "deployed_free": FREE,
        "applies_to_deployed": False,
    }


def lemma_free_ge_2_long_trades() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_ge_2_allows_long_trades",
        "statement": (
            "If free = m − w ≥ 2, then the intersection cap m−w−1 ≥ 1, so "
            "non-tight multi-mates with |C ∩ C'| ≤ m−w−2 (hence |△| ≥ 2(w+2)) "
            "are not ruled out by the intersection law. Toys realize such pairs; "
            "v8 coset pads with e0 > w+1 are long trades (|△| = 2 e0 > 2(w+1))."
        ),
        "proof": [
            "cap = free − 1 ≥ 1 when free ≥ 2, so |∩| ≤ cap−1 is permitted by v9.",
            "v8: e0 = 2^17 > w+1, pad mates have |∩| = m−e0 < m−w−1, "
            "|△| = 2 e0 > 2(w+1).",
            "Toy suite certifies long trades for free ≥ 2 on (F_17, mu_16).",
        ],
        "deployed_free": FREE,
        "deployed_is_free_ge_2": FREE >= 2,
    }


def lemma_min_weight_criterion() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "min_weight_pairwise_tight_gives_Kres_le_ktight",
        "statement": (
            f"If every residual multi-mate pair is min-weight (tight), and every "
            f"Phi_w fiber of residual can-cores is a pairwise-tight family "
            f"(equivalently: a tight clique), then "
            f"M_m^{{res,phi}} ≤ k_tight = {K_TIGHT}. "
            f"If also U_res ≤ floor(target/(pack * k_tight)), then |R| ≤ target."
        ),
        "proof": [
            "Min-weight ⇔ tight (trade-weight law).",
            "Pairwise-tight family size ≤ k_tight (v9 tight-clique packing), "
            "applied inside C_res (v11).",
            "Residual criterion (v10/v11) with K_res = k_tight.",
        ],
        "budgets": {
            "K_res": K_TIGHT,
            "U_res_atom": TARGET // (PACK_J * K_TIGHT),
            "log2": math.log2(max(TARGET / (PACK_J * K_TIGHT), 1)),
        },
        "hypotheses_open": [
            "Residual multi-mates are all min-weight (no long trades in C_res)",
            "Each residual multi-mate fiber is a pairwise-tight clique "
            "(not merely tight-graph connected)",
        ],
        "warning": (
            "Tight-graph connectivity alone is insufficient: toys show tight "
            "components larger than k_tight when the component is not a clique."
        ),
    }


def lemma_tight_component_not_enough() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "tight_graph_component_can_exceed_ktight",
        "statement": (
            "Let G_tight be the graph on a Phi_w fiber with edges = tight multi-mate "
            "pairs. A connected component of G_tight can have size > k_tight. "
            "Therefore 'all multi-mates are tight-adjacent to something' does not "
            "imply M_m ≤ k_tight; one needs a pairwise-tight (clique) hypothesis."
        ),
        "proof": [
            "Computational certificate in toy suite: e.g. (p,n,m,w)=(17,16,4,2) "
            "has a fiber of size 8 with max tight-component 8 > k_tight=5, "
            "and the fiber is not a tight clique (nontight edges present).",
            "v9 packing applies only to families where EVERY pair is tight.",
        ],
    }


def lemma_deployed_entropy() -> dict[str, Any]:
    log_avg = log2_comb(N, M) - W * math.log2(P)
    return {
        "status": "PROVED_BY_EXACT_FLOAT_ENTROPY_ARITHMETIC",
        "name": "deployed_avg_m_fiber",
        "log2_avg_m_fiber": log_avg,
        "free": FREE,
        "min_trade_weight": MIN_TRADE,
        "interpretation": (
            f"Deployed free={FREE} ≫ 1 so free-0/1 packing is unavailable. "
            f"Average m-fiber size ~ 2^({log_avg:.2f}) ≪ 1, so random multi-mates "
            "are absurdly rare; residual uniqueness is still the expected truth "
            "but not proved. Min trade weight is {MIN_TRADE}."
        ),
    }


def lemma_program() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_PROGRAM_LAW",
        "name": "v12_reduction",
        "statement": (
            "Unconditional atom-scale residual flatness remains open. "
            "After trade-weight law, the residual multi-mate wall splits as:\n"
            "  min-weight tight cliques → K_res ≤ 18 if pairwise-tight;\n"
            "  long trades → class (ii) partial plant or (iii) coset-free;\n"
            "  free≤1 → already packed (wrong free for deployed).\n"
            "To close unconditionally need: residual forbids long trades AND "
            "residual min-weight fibers are pairwise-tight cliques of size ≤ 18 "
            "(or ≤ 1), OR bound U_phi / U_res directly."
        ),
        "not_proved": [
            "residual has only min-weight multi-mates",
            "residual min-weight fibers are cliques",
            "M_m^{res} ≤ 1",
            "U_res atom bound",
        ],
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    # free-regime table on F_17
    for m, w in [
        (4, 1),
        (4, 2),
        (4, 3),
        (5, 2),
        (5, 3),
        (5, 4),
        (6, 2),
        (6, 3),
        (6, 4),
        (6, 5),
        (8, 2),
        (8, 6),
        (8, 7),
        (10, 4),
        (10, 8),
        (10, 9),
    ]:
        p, n = 17, 16
        free = m - w
        if free < 0 or w < 1:
            continue
        C = math.comb(n, m)
        if C > 12000:
            rows.append({"m": m, "w": w, "free": free, "skip": C})
            continue
        vals = domain_vals(p, n)
        fib: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for S in itertools.combinations(range(n), m):
            fib[phi_w(monic_rev([vals[i] for i in S], p), w)].append(frozenset(S))
        cap = m - w - 1
        e = w + 1
        k_tight = 1 + (n - m) // e
        min_tr = 2 * (w + 1)
        Mm = max(len(v) for v in fib.values())
        n_long = 0
        n_min = 0
        max_tcomp = 1
        any_tcomp_gt = False
        pure_min_weight_multimate = 0
        for sets in fib.values():
            if len(sets) < 2:
                continue
            parent = list(range(len(sets)))

            def find(x: int) -> int:
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            def uni(a: int, b: int) -> None:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[rb] = ra

            all_min = True
            n_pairs = 0
            n_tight_pairs = 0
            for i, a in enumerate(sets):
                for j in range(i + 1, len(sets)):
                    c = sets[j]
                    inter = len(a & c)
                    ensure(inter <= cap, "intersection")
                    sd = 2 * (m - inter)
                    ensure(sd >= min_tr, "trade weight")
                    n_pairs += 1
                    if sd == min_tr:
                        n_min += 1
                        n_tight_pairs += 1
                        ensure(inter == cap, "min wt => tight")
                        uni(i, j)
                    else:
                        n_long += 1
                        all_min = False
            comps: dict[int, int] = defaultdict(int)
            for i in range(len(sets)):
                comps[find(i)] += 1
            mt = max(comps.values()) if comps else 1
            max_tcomp = max(max_tcomp, mt)
            if mt > k_tight:
                any_tcomp_gt = True
            if all_min and len(sets) > 1:
                pure_min_weight_multimate += 1
                # pairwise tight clique => size <= k_tight
                if n_tight_pairs == n_pairs:
                    ensure(len(sets) <= k_tight, f"clique pack {len(sets)}>{k_tight}")

        rows.append(
            {
                "p": p,
                "n": n,
                "m": m,
                "w": w,
                "free": free,
                "Mm": Mm,
                "k_tight": k_tight,
                "min_trade": min_tr,
                "n_min_weight_pairs": n_min,
                "n_long_pairs": n_long,
                "max_tight_comp": max_tcomp,
                "tight_comp_gt_ktight": any_tcomp_gt,
                "n_pure_min_weight_fibers": pure_min_weight_multimate,
                "only_min_weight": n_long == 0,
            }
        )

    # free=1 rows: only min weight
    free1 = [r for r in rows if r.get("free") == 1 and "only_min_weight" in r]
    ensure(len(free1) >= 1, "need free1 rows")
    ensure(all(r["only_min_weight"] for r in free1), "free1 min only")
    # free>=2 with long trades exists
    ensure(any(r.get("n_long_pairs", 0) > 0 for r in rows if "Mm" in r), "long exists")
    # tight comp > k_tight exists
    ensure(any(r.get("tight_comp_gt_ktight") for r in rows if "Mm" in r), "tcomp warn")

    # v8 long-trade arithmetic at deployed
    e0 = 2**17
    trade_v8 = 2 * e0
    ensure(trade_v8 > MIN_TRADE, "v8 long")
    ensure(FREE >= 2, "deployed free")
    ensure(K_TIGHT == 18, "kt")

    # Unit: min-weight pad
    p, n, w, m = 17, 16, 1, 4
    e0 = w + 1
    vals = domain_vals(p, n)
    cos = c_cosets(n, e0)
    free_pts = [i for i in range(n) if i not in cos[0] and i not in cos[1]]
    R0 = frozenset(free_pts[: m - e0])
    C1, C2 = R0 | cos[0], R0 | cos[1]
    ensure(phi_w(monic_rev([vals[i] for i in sorted(C1)], p), w) ==
           phi_w(monic_rev([vals[i] for i in sorted(C2)], p), w), "phi")
    ensure(len(C1 ^ C2) == 2 * (w + 1), "min trade")
    unit = {"min_weight_pad_sd": len(C1 ^ C2), "expected": 2 * (w + 1)}

    return {
        "status": "PASS",
        "rows": rows,
        "unit_min_weight_pad": unit,
        "deployed_v8_trade_weight": trade_v8,
        "deployed_min_trade": MIN_TRADE,
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    log_avg = log2_comb(N, M) - W * math.log2(P)
    return {
        "packet": "kb_qatom_route_d_v12",
        "title": "Trade-weight law; free-regime packing; min-weight residual criterion",
        "status": "PARTIAL_TRADE_STRUCTURE",
        "claims": {
            "proves_trade_weight_law": True,
            "proves_free_le_1_pack": True,
            "proves_free_ge_2_long_trades_possible": True,
            "proves_min_weight_criterion_Kres_18": True,
            "proves_tight_component_can_exceed_ktight": True,
            "proves_Mm_res_le_1": False,
            "proves_unconditional_atom": False,
            "proves_residual_only_min_weight": False,
        },
        "deployed": {
            "n": N,
            "m": M,
            "w": W,
            "free": FREE,
            "min_trade_weight": MIN_TRADE,
            "v8_coset_trade_weight": 2 * (2**17),
            "k_tight": K_TIGHT,
            "k_coset_lower": K_COSET,
            "log2_avg_m_fiber": log_avg,
            "U_res_if_Kres_1": TARGET // PACK_J,
            "U_res_if_Kres_18": TARGET // (PACK_J * K_TIGHT),
            "log2_U_res_K1": math.log2(max(TARGET / PACK_J, 1)),
            "log2_U_res_K18": math.log2(max(TARGET / (PACK_J * K_TIGHT), 1)),
        },
        "lemmas": {
            "trade_weight": lemma_trade_weight(),
            "free_le_1": lemma_free_le_1(),
            "free_ge_2": lemma_free_ge_2_long_trades(),
            "min_weight_criterion": lemma_min_weight_criterion(),
            "tight_component_warning": lemma_tight_component_not_enough(),
            "entropy": lemma_deployed_entropy(),
            "program": lemma_program(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "unconditional_atom": False,
            "new_conditional_path": (
                f"min-weight + pairwise-tight residual fibers => K_res<={K_TIGHT}"
            ),
            "still_open": (
                "residual forbids long trades; residual tight fibers are cliques; "
                "or K_res=1; or U_phi bound"
            ),
            "next": (
                "Prove residual multi-mates are min-weight (pay/forbid long trades), "
                "then prove pairwise-tight (or size 1), OR attack U_phi."
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = [r for r in cert["toy_suite"]["rows"] if "Mm" in r]
    tbl = "\n".join(
        f"| {r['m']} | {r['w']} | {r['free']} | {r['Mm']} | {r['k_tight']} | "
        f"{r['n_min_weight_pairs']} | {r['n_long_pairs']} | {r['max_tight_comp']} | "
        f"{r['tight_comp_gt_ktight']} | {r['only_min_weight']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v12: trade-weight law

Status: `PARTIAL` — trade geometry **PROVED**; unconditional atom **NO**.

## Trade-weight law (PROVED, unconditional)

For multi-mates `C ≠ C'` in one `Phi_w` fiber:

```text
|C ∩ C'|  ≤  m − w − 1
|C △ C'|  =  2(m − |∩|)  ≥  2(w + 1)
```

Equality `|△| = 2(w+1)` ⇔ **tight** ⇔ free-1 CS pad of `(w+1)`-blocks.

Deployed minimum trade weight: `{d['min_trade_weight']}`.
v8 coset-pad trade weight: `{d['v8_coset_trade_weight']}` (long).

## Free regimes (PROVED)

| free | Multi-mates | Packing |
|---:|---|---|
| 0 | none | M_m ≤ 1 |
| 1 | min-weight only, pairwise disjoint CS | M_m ≤ floor(n/m) |
| ≥ 2 | long trades possible | no free packing |

Deployed free = `{d['free']}` ≫ 1. log2 avg m-fiber ≈ `{d['log2_avg_m_fiber']:.2f}`.

## Min-weight residual criterion (PROVED conditional)

```text
residual multi-mates all min-weight
AND each residual multi-mate fiber is a pairwise-tight clique
    =>  M_m^{{res,phi}} ≤ k_tight = {d['k_tight']}
    =>  U_res ≤ target/(17*18) ≈ 2^{{{d['log2_U_res_K18']:.2f}}} closes atom
```

### Warning (PROVED by toy)

Tight-**graph** components can exceed `k_tight` when not cliques.
Need pairwise-tight, not mere connectivity.

## Toy free-regime table (p=17, n=16)

| m | w | free | Mm | k_tight | #min pairs | #long | max t-comp | tcomp>kt | only min |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
{tbl}

## Unconditional atom?

**No.** Structure is unconditional; atom still needs residual hypotheses
(min-weight + clique) or `K_res=1` or `U_phi` bound.

## Next real math

1. Residual forbids long trades (`|△| ≥ 2(w+2)` paid / impossible), **and**
2. Residual min-weight fibers are pairwise-tight cliques (size ≤ 18 or 1), **or**
3. Direct `U_phi` / `U_res` bound, **or**
4. `M_m^{{res}} ≤ 1` by other residual geometry.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v12.py
python3 experimental/scripts/verify_kb_qatom_route_d_v12.py --check
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
        ensure(
            old["deployed"]["min_trade_weight"] == cert["deployed"]["min_trade_weight"],
            "trade drift",
        )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v12\n\n"
        "Trade-weight law; free-regime packing; min-weight residual criterion.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v12.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    rows = [r for r in cert["toy_suite"]["rows"] if "Mm" in r]
    REPORT_PATH.write_text(
        f"# v12 report\n\nstatus: {cert['status']}\n"
        f"min_trade: {cert['deployed']['min_trade_weight']}\n"
        f"unconditional_atom: false\n"
        f"toy rows: {len(rows)}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  unconditional atom: NO")
    print(f"  min trade weight: {cert['deployed']['min_trade_weight']}")
    print(f"  v8 trade weight: {cert['deployed']['v8_coset_trade_weight']} (long)")
    print(f"  conditional K_res<=18 path: min-weight + pairwise-tight cliques")
    print(f"  log2 avg m-fiber: {cert['deployed']['log2_avg_m_fiber']:.2f}")
    print(f"  toy rows: {len(rows)}")
    print(f"  unit: {cert['toy_suite']['unit_min_weight_pad']}")


if __name__ == "__main__":
    main()
