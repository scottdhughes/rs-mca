#!/usr/bin/env python3
"""KB-MCA Route-D v52: residual t-gate — sufficient H2 window vs multipad reality.

After v51 (U2e ⇒ H_*^pre ≤ C(t,2e); t≤2e+2 ⇒ H2), this packet checks whether
residual multipads can be forced into the arithmetic window.

Proved / certified:
  (1) Hierarchy (char ≠ 2): for all t,e,
        H_*^pre(t,e) ≤ min( p^{e−1}, binom(t,2e), ⌊binom(t,e)/2⌋ ).
      (coeff bound v48; U2e v51; pigeon).
  (2) Deployed arithmetic: among pure C(t,2e) comparisons to H2, only
        s := t − 2e ∈ {0,1,2}  works; s≥3 fails (v50/v51).
  (3) REFUTED as general multipad property: “every free-1 multipad high admits
      a free-1 pair with covering window t_min_pair ≤ 2e+2”.
      Toys: for e=3, p=31/61, frac with t_min_pair≤2e+2 is ~0; mean t_min_pair
      ≫ 2e. So ambient multipads live at large t; residual cannot inherit a
      free t≤2e+2 bound without extra structure.
  (4) Pack-k observation: k=⌊t/e⌋≤17 deployed still allows t up to n' with
      C(n',2e) ≫ H2; pack=2 alone only forces t<3e, still s up to e−1.
  (5) Random-core heuristic (not a residual theorem): E[min(C)] for uniform
      m_c-subsets is (n−m_c)/(m_c+1)≈n'/m_c≈1.3, so coext multipads with
      t≥2e are atypical among all cores — but residual is conditioned on
      multipad existence, so this does not force small residual t.

OPEN (sharpened):
  Bound H_*^pre(t,e) for t ∈ [2e,n'] by residual-specific structure
  (free_core / C_unique / Type filters), or bound |H_unt| by summing only
  residual cores — ambient ★_pre at full t-range is not H2-closed for e>2.

Does NOT prove residual t≤2e+2; does NOT prove A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v52.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v52"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v52.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v52.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v52.report.md"
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
H2 = E_P // (2 * 31 * 30)
T_MIN = 2 * E


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


def lemma_hierarchy() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Hpre_hierarchy",
        "statement": (
            "H_*^pre(t,e) ≤ min(p^{e-1}, C(t,2e), ⌊C(t,e)/2⌋) (char≠2 for C(t,2e))."
        ),
        "proof": [
            "p^{e-1}: monic high has e−1 free coeffs (v48).",
            "C(t,2e): U2e injection H↦W (v51).",
            "⌊C(t,e)/2⌋: each multipad high consumes ≥2 e-sets.",
        ],
    }


def lemma_arith_window() -> dict[str, Any]:
    vals = {s: binom_int(2 * E + s, s) for s in range(0, 5)}
    return {
        "status": "PROVED",
        "name": "only_s_le_2_C_bound_le_H2",
        "statement": (
            f"Deployed: C(2e+s,s)≤H2={H2} iff s∈{{0,1,2}} among s=0..4 checked; "
            f"s=3 already {vals[3]} > H2."
        ),
        "values": {str(s): vals[s] for s in vals},
        "H2": H2,
    }


def lemma_t_gate_refuted() -> dict[str, Any]:
    return {
        "status": "REFUTED",
        "name": "ambient_multipad_t_min_pair_le_2e_plus_2",
        "statement": (
            "It is FALSE that every free-1 multipad high on a cyclic domain "
            "admits some free-1 pair with covering window t_min_pair ≤ 2e+2. "
            "Hence residual cannot quote t≤2e+2 from ambient multipad geometry alone."
        ),
        "evidence": "toy_suite.t_gate_refutations",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_residual_specific_Hpre_or_core_sum",
        "statement": (
            "Close |H_unt|≤H2 via residual-only structure (C_unique + free_core "
            "filters + Type/SR/H_M), not ambient ★_pre at full t∈[2e,n']."
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


def multipad_windows(p: int, n: int, e: int) -> list[dict[str, Any]]:
    vals = domain_vals(p, n)
    by: dict[Any, list] = defaultdict(list)
    for idxs in itertools.combinations(range(n), e):
        by[monic_high(idxs, vals, p, e)].append(tuple(sorted(idxs)))
    rows = []
    for us in by.values():
        if len(us) < 2:
            continue
        pair_ts = []
        for a, b in itertools.combinations(us, 2):
            pair_ts.append(max(max(a), max(b)) + 1)
        union: set[int] = set()
        for u in us:
            union |= set(u)
        rows.append(
            {
                "fiber": len(us),
                "t_min_pair": min(pair_ts),
                "t_max_pair": max(pair_ts),
                "t_star_full": max(union) + 1,
            }
        )
    return rows


def toy_suite() -> dict[str, Any]:
    ensure(P % 2 == 1, "odd")
    ensure(FREE_CORE == 846161, "fc")
    ensure(binom_int(2 * E + 2, 2) <= H2, "s2")
    ensure(binom_int(2 * E + 3, 3) > H2, "s3")

    # hierarchy sanity on small rows
    hier_rows = []
    for p, n in [(17, 16), (31, 30), (61, 60)]:
        vals = domain_vals(p, n)
        for e in [2, 3]:
            for t in range(2 * e, min(n, 3 * e + 5) + 1):
                if math.comb(t, e) > 20000:
                    continue
                by: dict[Any, int] = defaultdict(int)
                for idxs in itertools.combinations(range(t), e):
                    by[monic_high(idxs, vals, p, e)] += 1
                nH = sum(1 for c in by.values() if c >= 2)
                bound = min(p ** (e - 1), binom_int(t, 2 * e), math.comb(t, e) // 2)
                ensure(nH <= bound, f"hier p={p} e={e} t={t}")
                hier_rows.append(
                    {"p": p, "e": e, "t": t, "nH": nH, "bound": bound}
                )

    # t-gate refutation census
    refutations = []
    window_rows = []
    for p, n in [(17, 16), (31, 30), (61, 60)]:
        for e in [2, 3]:
            if math.comb(n, e) > 60000:
                continue
            rows = multipad_windows(p, n, e)
            if not rows:
                continue
            gate = 2 * e + 2
            n_small = sum(1 for r in rows if r["t_min_pair"] <= gate)
            frac = n_small / len(rows)
            mean_t = sum(r["t_min_pair"] for r in rows) / len(rows)
            rec = {
                "p": p,
                "n": n,
                "e": e,
                "nH": len(rows),
                "gate_2e_plus_2": gate,
                "n_t_min_le_gate": n_small,
                "frac_le_gate": frac,
                "mean_t_min_pair": mean_t,
                "max_t_min_pair": max(r["t_min_pair"] for r in rows),
                "min_t_min_pair": min(r["t_min_pair"] for r in rows),
                "max_fiber": max(r["fiber"] for r in rows),
            }
            window_rows.append(rec)
            # Refute universal t_min≤2e+2 when we see a counterexample high
            if any(r["t_min_pair"] > gate for r in rows):
                refutations.append(
                    {
                        "p": p,
                        "e": e,
                        "example_t_min": max(r["t_min_pair"] for r in rows),
                        "gate": gate,
                    }
                )

    ensure(len(refutations) >= 2, "need refutations")
    # Strong e=3 refutation: frac at gate near 0
    e3 = [r for r in window_rows if r["e"] == 3]
    ensure(any(r["frac_le_gate"] < 0.05 for r in e3), "e3 mostly large t")

    # random-core expectation (exact formula)
    # E[min] for uniform m-subset of {0..n-1} = (n-m)/(m+1)
    e_min = (N - M_C) / (M_C + 1)
    ensure(abs(e_min - N_PRIME / (M_C + 1)) < 1e-9, "emin")

    return {
        "status": "PASS",
        "hierarchy_rows": hier_rows,
        "window_rows": window_rows,
        "t_gate_refutations": refutations,
        "census": {
            "n_hier": len(hier_rows),
            "n_window": len(window_rows),
            "n_refutations": len(refutations),
            "all_hier_ok": True,
        },
        "deployed": {
            "E_min_C_uniform": e_min,
            "t_min_multipad": T_MIN,
            "n_prime": N_PRIME,
            "pack_ceil": N_PRIME // E,
            "C_2e2_2": binom_int(2 * E + 2, 2),
            "C_2e3_3": binom_int(2 * E + 3, 3),
            "H2": H2,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v52",
        "title": "residual t-gate: H2 window sufficient, ambient multipad t large REFUTED",
        "status": "T_GATE_REFUTED_LARGE_T_OPEN",
        "claims": {
            "proves_Hpre_hierarchy": True,
            "proves_only_s_le_2_for_C_le_H2": True,
            "refutes_ambient_t_min_pair_le_2e_plus_2": True,
            "proves_residual_t_le_2e_plus_2": False,
            "proves_Hpre_deployed_full_window_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e": E,
            "n_prime": N_PRIME,
            "t_min": T_MIN,
            "H2": H2,
            "free_core": FREE_CORE,
            "E_min_C_uniform": (N - M_C) / (M_C + 1),
        },
        "lemmas": {
            "hierarchy": lemma_hierarchy(),
            "arith": lemma_arith_window(),
            "t_gate_refuted": lemma_t_gate_refuted(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "closed": "t≤2e+2 is only a sufficient arithmetic gate, not ambient truth",
            "next": "residual-specific |H_unt| (C_unique / free_core / filters)",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    toys = cert["toy_suite"]
    dep = toys["deployed"]
    wr = toys["window_rows"]
    tbl = "\n".join(
        f"| {r['p']} | {r['e']} | {r['nH']} | {r['gate_2e_plus_2']} | "
        f"{r['frac_le_gate']:.3f} | {r['mean_t_min_pair']:.1f} | "
        f"{r['min_t_min_pair']}–{r['max_t_min_pair']} | {r['max_fiber']} |"
        for r in wr
    )
    return f"""# KB-MCA Route-D v52: residual t-gate vs multipad windows

Status: **t≤2e+2 is a sufficient H2 gate (v51), NOT an ambient multipad law**.
REFUTED as universal multipad property; residual still OPEN.

## Hierarchy (PROVED)

```text
H_*^pre(t,e)  ≤  min( p^{{e−1}},  binom(t,2e),  ⌊binom(t,e)/2⌋ )
```

## Arithmetic H2 window (PROVED)

Deployed e={E}: only `s=t−2e ∈ {{0,1,2}}` has `binom(2e+s,s) ≤ H2={dep['H2']}`.

| s | C(2e+s,s) | ≤H2? |
|---:|---:|---|
| 2 | {dep['C_2e2_2']} | yes |
| 3 | {dep['C_2e3_3']} | no |

## REFUTED: ambient multipads have small pair-window

Define for multipad fiber `F_H`:

```text
t_min_pair(H)  =  min_{{U≠V in F_H}} (1 + max(U ∪ V))
```

**Claim (refuted):** t_min_pair(H) ≤ 2e+2 for every multipad high H.

| p | e | nH | gate | frac ≤gate | mean t_min | range | max fiber |
|---|---:|---:|---:|---:|---:|---|---:|
{tbl}

e=3 rows: almost all multipads need t_min_pair ≫ 2e+2.

⇒ Residual cannot assume t≤2e+2 from multipad geometry alone.

## Random-core aside (heuristic only)

Uniform random m_c-subset of `{{0..n−1}}` has
`E[min(C)] = (n−m_c)/(m_c+1) ≈ {dep['E_min_C_uniform']:.3f}`.
Coext multipads need t≥2e={T_MIN}, so they are atypical among all cores —
but residual **conditions** on multipad existence, so this does not force
small residual t.

## Residual card path (updated)

```text
U2e + t≤2e+2  ⇒  H*≤H2     (sufficient, rare for ambient multipads)
ambient ★_pre at t≤n'      (NOT H2-closed for e>2: p^{{e−1}} and C(n',2e) both ≫H2)
```

Need **residual-specific** bound on `|H_unt|` (C_unique, free_core, SR/H_M/Type).

## OPEN

1. C_unique theorem (v47 gap ★)
2. free_core / residual filters ⇒ `|H_unt|≤H2` without ambient small-t
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v52.py --check
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
        "# kb-qatom-route-d-v52\n\n"
        "t-gate: sufficient H2 window; ambient multipad small-t REFUTED.\n"
    )
    REPORT_PATH.write_text(
        f"# v52 report\n\nstatus: {cert['status']}\n"
        f"hierarchy: PROVED\n"
        f"ambient t_min_pair<=2e+2: REFUTED\n"
        f"OPEN residual-specific |H_unt|: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  hierarchy H*≤min(p^{e-1},C(t,2e),C(t,e)/2): PROVED")
    print("  only s≤2 gives C(2e+s,s)≤H2: PROVED")
    print(
        f"  ambient t_min_pair≤2e+2: REFUTED "
        f"({cen['n_refutations']} toy families)"
    )
    print("  OPEN: residual-specific |H_unt| (not ambient small-t)")


if __name__ == "__main__":
    main()
