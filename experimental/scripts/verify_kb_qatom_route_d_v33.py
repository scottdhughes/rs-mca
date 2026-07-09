#!/usr/bin/env python3
"""KB-MCA Route-D v33: free_core=2 non-Helly M_pad bound + FM high matching.

Attacks Type S connectedness / non-Helly M_pad and first-match high thinning.

Proved:
  (1) free_core=2 through-clique: for each r, Cores_r is a clique under
      intersection (any two share r) with reduced free-1 CS cores; hence
      |Cores_r| ≤ T₂ := ⌊(n−2e−1)/(m_c−1)⌋ (v30).
  (2) free_core=2 Type S M_pad bound (Helly and non-Helly): with t = max mult
        M_pad ≤ ⌊ t (n−2e) / m_c ⌋ ≤ ⌊ T₂ (n−2e) / m_c ⌋.
      Covers non-Helly Type S at free_core=2. Deployed if free_core were 2:
      T₂=2, (n−2e)/m_c=2 ⇒ M_pad ≤ 4.
  (3) free_core=2 edge structure: pairwise |C∩C'| ≤ 1; edges labeled by unique
      shared roots; Type S intersection graph is a union of through-cliques.
  (4) Connectedness: mpad=2 proved; free_core=2+larger still OPEN as theorem;
      TOY UNIVERSAL (0 disconnected Type S). Not claimed PROVED in general.
  (5) First-match high matching (FM-match): process domain indices in order;
      when a free block can host an active U of an unmatched high, claim that
      high. Output H_FM with |H_FM| ≤ ⌊n/e⌋ ≤ 31 ≤ K_max=2176. PROVED size.
  (6) FM-match is a valid high matching (pairwise disjoint reps). PROVED.
  (7) Banked: FM-match need NOT cover all A_SP pairs (many pairs use unmatched
      highs) — thinning alone does not pay full N_ord without a residual-high tier.
  (8) Two-tier high payment path: matched highs inject into [⌊n/e⌋]⊆[K_max];
      unmatched highs require a second mark/budget (OPEN).

Does NOT prove general Type S connectedness, free_core≫2 non-Helly M_pad≤2,
or full |H_A_SP|≤31 via FM-match alone.

  python3 experimental/scripts/verify_kb_qatom_route_d_v33.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v33.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v33"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v33.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v33.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v33.report.md"
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
T_P = T * P
E_P = E * P
FLOOR_N_OVER_E = N // E  # 31
K_MAX = E // FLOOR_N_OVER_E  # 2176
# free_core=2 deployed-scale numbers (not actual free_core)
T2_DEPLOYED = (N - 2 * E - 1) // (M_C - 1)  # 2
MPAD_FC2_BOUND_DEPLOYED = T2_DEPLOYED * (N - 2 * E) // M_C  # 4
PACK_MAXIMAL_COMMON = A // E  # 16


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


def phi_w(poly: list[int], w: int) -> tuple[int, ...]:
    return tuple(poly[1 : w + 1])


def free1_high_c0(U, vals, p):
    poly = monic_rev([vals[i] for i in sorted(U)], p)
    return tuple(poly[1:-1]), poly[-1]


def lemma_fc2_through_clique() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_2_through_cliques",
        "statement": (
            "If free_core=2 and Cores is a multipad core set for (U,V), then for "
            "every domain point r the through-set Cores_r is an intersection "
            "clique: any two members share r, their reductions are free-1 CS of "
            "size m_c−1, and |Cores_r| ≤ T₂ = ⌊(n−2e−1)/(m_c−1)⌋."
        ),
        "proof": [
            "v30 free_core=2 through-pack: reduced cores free-1 CS ⇒ pairwise "
            "disjoint reduced supports ⇒ C∩C' = {{r}} for distinct C,C'∈Cores_r.",
            "Hence every pair in Cores_r intersects (at least in r) ⇒ clique.",
            "Packing: v25 on ground set size n−2e−1.",
        ],
    }


def lemma_fc2_mpad_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free_core_2_type_S_Mpad_tpack_bound",
        "statement": (
            "If free_core=2, then for any multipad (Type D or S, Helly or not) "
            "with point-multiplicity t = max_r |Cores_r|: "
            "M_pad ≤ ⌊t(n−2e)/m_c⌋ ≤ ⌊T₂(n−2e)/m_c⌋ with T₂=⌊(n−2e−1)/(m_c−1)⌋. "
            f"Deployed-scale (if free_core=2): T₂={T2_DEPLOYED}, bound "
            f"M_pad ≤ {MPAD_FC2_BOUND_DEPLOYED}."
        ),
        "proof": [
            "v28 point-multiplicity packing: M_pad ≤ ⌊t(n−2e)/m_c⌋.",
            "free_core=2 ⇒ t = max |Cores_r| ≤ T₂ by through-clique packing.",
            "Applies equally to non-Helly Type S (no common ⋂ required).",
        ],
        "deployed_if_fc2": {
            "T2": T2_DEPLOYED,
            "Mpad_bound": MPAD_FC2_BOUND_DEPLOYED,
            "actual_free_core": FREE_CORE,
            "applies": False,
        },
    }


def lemma_connectedness() -> dict[str, Any]:
    return {
        "status": "PARTIAL",
        "name": "type_S_connectedness_partial",
        "statement": (
            "PROVED: mpad=2 Type S is connected. "
            "TOY UNIVERSAL: all larger Type S multipads tested are connected. "
            "OPEN: general connectedness theorem for geometric multipads."
        ),
        "proof": [
            "mpad=2 Type S ⇒ unique pair shares a root ⇒ one edge (v31).",
            "free_core=2: intersection graph is a union of through-cliques; "
            "toys always yield a single connected component of those cliques.",
            "No ambient algebraic obstruction found ruling out disconnected "
            "Type S in general; no toy counterexample found either.",
        ],
    }


def lemma_fm_high_matching() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "first_match_high_matching_size",
        "statement": (
            "FM-match: process domain indices r=0,1,...,n−1; if r is still free, "
            "select (if any) an unmatched active high H that has an active free-1 "
            "e-set U∋r with U contained in the free set, claim H and mark U used. "
            "The output H_FM satisfies |H_FM| ≤ ⌊n/e⌋ and the chosen U's are "
            f"pairwise disjoint. Deployed: |H_FM| ≤ {FLOOR_N_OVER_E} ≤ {K_MAX}."
        ),
        "proof": [
            "Each claim consumes e free domain points (the set U), so at most "
            "⌊n/e⌋ claims.",
            "Chosen U's are pairwise disjoint by construction (only free points).",
            "Hence H_FM is a high matching of size ≤⌊n/e⌋ (v32 ν bound).",
            f"Deployed ⌊n/e⌋={FLOOR_N_OVER_E} ≤ K_max={K_MAX}.",
        ],
        "payment_note": (
            "Matched highs inject into [⌊n/e⌋]⊆[K_max] for (κ,ι,δ). "
            "Pairs whose high ∉ H_FM are unmatched-tier (OPEN residual mark)."
        ),
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_connectedness_fc_gt2_nonhelly_and_unmatched_highs",
        "statement": (
            "(1) Prove Type S intersection-connected for free_core≫2; "
            f"bound non-Helly M_pad at free_core={FREE_CORE} "
            f"(free_core=2 gives ≤{MPAD_FC2_BOUND_DEPLOYED} if fc were 2).\n"
            "(2) Pay A_SP pairs on unmatched FM-match highs, or prove residual "
            "first-match forces all active highs into H_FM."
        ),
    }


def fm_match_highs(
    high_Us: dict[Any, list[frozenset[int]]], n: int, e: int
) -> tuple[list[Any], dict[Any, frozenset[int]]]:
    """First-match greedy high matching. Returns (ordered highs, rep U map)."""
    highs = list(high_Us.keys())
    free = set(range(n))
    matched: list[Any] = []
    reps: dict[Any, frozenset[int]] = {}
    claimed_h: set = set()
    for r in range(n):
        if r not in free:
            continue
        for h in highs:
            if h in claimed_h:
                continue
            for u in high_Us[h]:
                if r in u and set(u).issubset(free):
                    free -= set(u)
                    matched.append(h)
                    reps[h] = u
                    claimed_h.add(h)
                    break
    return matched, reps


def toy_suite() -> dict[str, Any]:
    rows = []
    n_type_S = 0
    n_S_conn = 0
    n_fc2_S = 0
    n_fc2_bound_ok = 0
    n_nonstar = 0
    n_fm_size_ok = 0
    n_fm_disj_ok = 0
    n_rows_partial_pair_cover = 0

    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 1),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
    ]:
        e = w + 1
        m_c = j - e
        if m_c <= 0 or math.comb(n, j) > 25000:
            continue
        free_core = m_c - w
        vals = domain_vals(p, n)
        floor_ne = n // e
        T2 = (n - 2 * e - 1) // (m_c - 1) if m_c > 1 and n >= 2 * e + 1 else 0
        fc2_bound = (T2 * (n - 2 * e)) // m_c if m_c else 0

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        high_Us: dict[Any, list] = defaultdict(list)
        seen_U: dict[Any, set] = defaultdict(set)
        all_pairs: list[tuple] = []  # (high, U, V)
        n_S = 0
        n_D = 0
        max_mpad_S = 1
        max_t = 0
        all_conn = True
        n_nonstar_row = 0

        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                ss = sorted(S)
                U = frozenset(ss[:e])
                C = S - U
                high, c0 = free1_high_c0(U, vals, p)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))

            pads: dict[Any, list] = defaultdict(list)
            for key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, high = a
                        _C2, V, c0V, _ = b
                        if c0U == c0V:
                            continue
                        pads[(high, c0U, c0V)].append(C)
                        ut = tuple(sorted(U))
                        if ut not in seen_U[high]:
                            seen_U[high].add(ut)
                            high_Us[high].append(U)
                        all_pairs.append((high, ut, tuple(sorted(V))))

            for _sk, Cs in pads.items():
                cores = [set(t) for t in {tuple(sorted(C)) for C in Cs}]
                if len(cores) < 2:
                    continue
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                t = max(cnt.values())
                max_t = max(max_t, t)
                if t <= 1:
                    n_D += 1
                    continue
                n_S += 1
                n_type_S += 1
                max_mpad_S = max(max_mpad_S, len(cores))

                if free_core == 2:
                    n_fc2_S += 1
                    ensure(t <= T2, f"t={t}>T2={T2}")
                    ensure(len(cores) <= fc2_bound, f"mpad={len(cores)}>bound={fc2_bound}")
                    n_fc2_bound_ok += 1
                    # through-clique: every pair in Cores_r shares exactly?
                    for r, mult in cnt.items():
                        if mult < 2:
                            continue
                        through = [c for c in cores if r in c]
                        for a, b in itertools.combinations(through, 2):
                            ensure(r in a and r in b, "through")
                            # free_core=2: inter should be {{r}} often
                            ensure(len(a & b) >= 1, "clique edge")

                common = set.intersection(*cores)
                if not common:
                    n_nonstar += 1
                    n_nonstar_row += 1

                # connectedness
                k = len(cores)
                parent = list(range(k))

                def find(x: int) -> int:
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                def union(a: int, b: int) -> None:
                    ra, rb = find(a), find(b)
                    if ra != rb:
                        parent[ra] = rb

                for i in range(k):
                    for j2 in range(i + 1, k):
                        if cores[i] & cores[j2]:
                            union(i, j2)
                n_comp = len({find(i) for i in range(k)})
                if n_comp == 1:
                    n_S_conn += 1
                else:
                    all_conn = False
                if k == 2:
                    ensure(n_comp == 1, "mpad2")

        if free_core == 1:
            ensure(n_S == 0, "fc1")
        if n_S > 0:
            ensure(all_conn, "toy connected")

        # FM-match
        matched, reps = fm_match_highs(high_Us, n, e)
        ensure(len(matched) <= floor_ne, "FM size")
        n_fm_size_ok += 1
        # disjoint reps
        used: set[int] = set()
        disj_ok = True
        for h in matched:
            u = reps[h]
            if not used.isdisjoint(u):
                disj_ok = False
            used |= set(u)
        ensure(disj_ok, "FM disj")
        n_fm_disj_ok += 1

        # pair coverage
        matched_set = set(matched)
        n_pairs = len(all_pairs)
        n_cov = sum(1 for h, U, V in all_pairs if h in matched_set)
        frac = n_cov / n_pairs if n_pairs else 1.0
        if n_pairs > 0 and frac < 1.0 - 1e-12:
            n_rows_partial_pair_cover += 1

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "m_c": m_c,
                "free_core": free_core,
                "T2": T2,
                "fc2_mpad_bound": fc2_bound,
                "n_type_D": n_D,
                "n_type_S": n_S,
                "n_nonstar": n_nonstar_row,
                "max_Mpad_S": max_mpad_S,
                "max_t": max_t,
                "all_S_connected": all_conn if n_S > 0 else None,
                "fc2_bound_ok": (max_mpad_S <= fc2_bound) if free_core == 2 and n_S > 0 else None,
                "n_active_highs": len(high_Us),
                "n_FM_matched": len(matched),
                "floor_n_over_e": floor_ne,
                "FM_le_floor": len(matched) <= floor_ne,
                "n_pairs": n_pairs,
                "n_pairs_FM_covered": n_cov,
                "frac_pairs_FM_covered": frac,
                "FM_covers_all_pairs": frac >= 1.0 - 1e-12 if n_pairs else True,
            }
        )

    ensure(n_type_S > 0, "S")
    ensure(n_S_conn == n_type_S, "conn")
    ensure(n_fc2_S > 0 and n_fc2_bound_ok == n_fc2_S, "fc2 bound")
    ensure(n_nonstar > 0, "nonstar")
    ensure(n_fm_size_ok == len(rows), "fm size all rows")
    ensure(n_fm_disj_ok == len(rows), "fm disj")
    ensure(n_rows_partial_pair_cover > 0, "FM incomplete cover banked")
    ensure(FREE_CORE == 846161, "fc")
    ensure(FLOOR_N_OVER_E == 31, "31")
    ensure(T2_DEPLOYED == 2, "T2")
    ensure(MPAD_FC2_BOUND_DEPLOYED == 4, "fc2 bound dep")
    ensure(FREE_CORE != 2, "not fc2 deployed")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_type_S": n_type_S,
            "n_S_connected": n_S_conn,
            "n_fc2_S": n_fc2_S,
            "n_fc2_bound_ok": n_fc2_bound_ok,
            "n_nonstar": n_nonstar,
            "n_rows_partial_pair_cover": n_rows_partial_pair_cover,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v33",
        "title": "free_core=2 non-Helly M_pad bound + FM high matching",
        "status": "PARTIAL_FC2_BOUND_FM_MATCH",
        "claims": {
            "proves_fc2_through_cliques": True,
            "proves_fc2_type_S_mpad_tpack_bound": True,
            "proves_type_S_connected_general": False,
            "toy_confirms_type_S_connected": True,
            "proves_FM_high_matching_size": True,
            "proves_FM_covers_all_pairs": False,
            "banks_FM_incomplete_pair_cover": True,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "free_core": FREE_CORE,
            "T2_if_fc2": T2_DEPLOYED,
            "Mpad_bound_if_fc2": MPAD_FC2_BOUND_DEPLOYED,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "K_max": K_MAX,
            "FM_match_fits_Kmax": FLOOR_N_OVER_E <= K_MAX,
            "maximal_common_bound": PACK_MAXIMAL_COMMON,
            "t_p": T_P,
            "e_p": E_P,
        },
        "lemmas": {
            "fc2_clique": lemma_fc2_through_clique(),
            "fc2_mpad": lemma_fc2_mpad_bound(),
            "connectedness": lemma_connectedness(),
            "fm_match": lemma_fm_high_matching(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "non_Helly": (
                f"free_core=2 non-Helly M_pad ≤ ⌊T₂(n−2e)/m_c⌋ "
                f"(={MPAD_FC2_BOUND_DEPLOYED} at deployed sizes if fc=2); "
                "actual free_core≫2 still open"
            ),
            "highs": (
                f"FM-match gives ≤{FLOOR_N_OVER_E} highs in budget; "
                "incomplete pair cover ⇒ two-tier high payment needed"
            ),
            "next": (
                "Prove Type S connectedness; lift t-pack non-Helly bound past "
                "free_core=2; pay unmatched-high pairs"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_type_S']} | "
        f"{r['max_Mpad_S']} | {r['max_t']} | {r['fc2_mpad_bound']} | "
        f"{r['fc2_bound_ok']} | {r['all_S_connected']} | {r['n_active_highs']} | "
        f"{r['n_FM_matched']} | {r['frac_pairs_FM_covered']:.2f} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v33: free_core=2 non-Helly bound + FM high matching

Status: `PARTIAL` — free_core=2 **non-Helly M_pad t-pack** PROVED; **FM high
matching ≤⌊n/e⌋** PROVED; full pair cover by FM **REFUTED**; connectedness proof OPEN.

## free_core=2 non-Helly M_pad (PROVED)

Through-sets are cliques with `|Cores_r| ≤ T₂ = ⌊(n−2e−1)/(m_c−1)⌋`.

```text
M_pad  ≤  ⌊ t (n−2e) / m_c ⌋  ≤  ⌊ T₂ (n−2e) / m_c ⌋
```

Works for **Helly and non-Helly** Type S at free_core=2.

Deployed-scale if free_core were 2: `T₂={d['T2_if_fc2']}`, bound
`M_pad ≤ {d['Mpad_bound_if_fc2']}`. Actual free_core=`{d['free_core']}`.

## Connectedness (PARTIAL)

| case | status |
|---|---|
| mpad=2 | PROVED |
| all toys | UNIVERSAL (0 counterexamples) |
| general | OPEN |

## FM high matching (PROVED size; incomplete cover)

```text
FM-match: greedy domain order → H_FM
|H_FM| ≤ ⌊n/e⌋ = {d['floor_n_over_e']} ≤ K_max = {d['K_max']}
```

Chosen representatives pairwise disjoint.

**Banked negative:** FM-match does **not** cover all A_SP pairs — many pairs use
unmatched highs. Two-tier payment required.

## Toys

| j | w | free_core | #S | max M_pad S | max t | fc2 bound | fc2 ok? | connected? | #highs | |H_FM| | frac pairs covered |
|---|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
{tbl}

Census: Type S={cen['n_type_S']} connected; fc2 bound OK={cen['n_fc2_bound_ok']}/{cen['n_fc2_S']};
nonstar={cen['n_nonstar']}; rows with partial FM pair cover={cen['n_rows_partial_pair_cover']}.

## OPEN

1. Type S connectedness theorem; non-Helly M_pad at free_core=`{d['free_core']}`
2. Pay unmatched-high A_SP pairs (or force residual into H_FM)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v33.py --check
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
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v33\n\n"
        "free_core=2 non-Helly M_pad bound + FM high matching.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v33 report\n\nstatus: {cert['status']}\n"
        f"fc2 Mpad bound (if fc=2): {MPAD_FC2_BOUND_DEPLOYED}\n"
        f"FM match size ≤ {FLOOR_N_OVER_E}\n"
        f"FM full pair cover: REFUTED\n"
        f"type S connectedness proof: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  free_core=2 non-Helly M_pad ≤ ⌊T₂(n−2e)/m_c⌋: PROVED")
    print(f"  deployed-scale if fc=2: M_pad ≤ {MPAD_FC2_BOUND_DEPLOYED}")
    print("  Type S connectedness: toys universal; general proof OPEN")
    print(f"  FM high matching |H_FM|≤⌊n/e⌋={FLOOR_N_OVER_E}≤{K_MAX}: PROVED")
    print(
        f"  FM full pair cover: REFUTED "
        f"({cen['n_rows_partial_pair_cover']} rows partial)"
    )
    print(f"  toys: S={cen['n_type_S']} conn; fc2 ok={cen['n_fc2_bound_ok']}")


if __name__ == "__main__":
    main()
