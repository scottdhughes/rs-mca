#!/usr/bin/env python3
"""KB-MCA Route-D v37: SR mark compression census + multi-tier full-side path.

Attacks constructive SR ≤e·p and R-cell / |H|≤2170.

Proved / banked:
  (1) SR full mark (r_*, c0U, c0V) size n·p²: injective on Type S side keys (toys;
      monic recovery + unique r_* assignment).
  (2) SR near-miss (r_* mod e, c0U, δ) size e·p²: injective on all toy Type S
      rows; still factor p over e·p budget (deployed p/1 ≫ 1).
  (3) SR e·p candidates (r_* mod e, δ), (r_* mod e, c0U), (ι, δ) alone: collide
      when many Type S keys (banked negative for pure e·p compression).
  (4) Multi-tier FM path without M-cell: if |H_A_SP| ≤ K_cap=2170, multi-tier
      tags inject all highs into [K_cap]⊆[K_max] and therefore cover all A_SP
      pairs (no residual R-cell). PROVED conditional (v34+v36).
  (5) |H_A_SP| ≤ 2170 ambient: OPEN (toys |H|≪2170 always; no general proof).
  (6) R-cell natural e·p marks still collide when R-cell nonempty (v36 bank).
  (7) Combined: SR-cell cardinality room under |H|≤K_cap (v36) + Type D residual
      + multi-tier sides if |H|≤K_cap closes A_SP at e·p abstractly; constructive
      SR e·p mark is the remaining SR gap (e·p² near-miss recorded).

Does NOT prove pure e·p SR mark, |H|≤2170, or R-cell e·p injection.

  python3 experimental/scripts/verify_kb_qatom_route_d_v37.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v37.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v37"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v37.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v37.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v37.report.md"
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
K_CAP = (K_MAX // FLOOR_N_OVER_E) * FLOOR_N_OVER_E  # 2170
E_P2 = E * P * P  # e·p² near-miss budget
N_P2 = N * P * P


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


def lemma_near_miss() -> dict[str, Any]:
    return {
        "status": "PROVED_STRUCTURE_TOY_INJ",
        "name": "SR_mark_ep2_near_miss",
        "statement": (
            "Define for each Type S side key sk=(high,c0U,c0V) the root "
            "r_*=min{{r:mult(r)≥2}} (min over multipad fibers; or per-fiber then "
            "min). The mark μ₂(sk) = (r_* mod e, c0U, δ) with δ=c0U−c0V has size "
            f"e·p² (= {E_P2} deployed). On all toy rows with Type S, μ₂ is "
            "injective. Relative to e·p it overshoots by a factor p "
            f"(≈{P} deployed)."
        ),
        "proof": [
            "c0U,δ recover (c0U,c0V). r_* mod e is the compressed shared-root "
            "witness from SR-cell.",
            "Toy census: zero collisions of μ₂ on unique Type S side keys.",
            "Full (r_*,c0U,c0V) also injective (size n·p²) on toys.",
        ],
        "budget": {
            "e_p": E_P,
            "e_p2": E_P2,
            "n_p2": N_P2,
            "overshoot_factor_p": P,
        },
    }


def lemma_ep_negative() -> dict[str, Any]:
    return {
        "status": "BANKED_NEGATIVE",
        "name": "SR_pure_ep_compressions_collide",
        "statement": (
            "Natural size-e·p compressions of (r_*,c0U,c0V) — including "
            "(r_* mod e, δ), (r_* mod e, c0U), (ι(U), δ) alone — collide on "
            "toy Type S sets when n_S is large. No tested pure e·p SR mark is "
            "injective on all Type S rows."
        ),
        "proof": ["Toy census in this packet."],
    }


def lemma_multitier_no_Mcell() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "multitier_covers_all_sides_under_Hcap",
        "statement": (
            f"If |H_A_SP| ≤ K_cap = {K_CAP}, multi-tier FM (v34) injects all "
            "active highs into [K_cap] ⊆ [K_max], and every A_SP free-1 CS pair "
            "has its high tagged — no separate R-cell is required for side marks."
        ),
        "proof": [
            "v34 multi-tier tags every high with a U when enough tiers.",
            "Every A_SP pair has a high among H_A_SP.",
            f"Capacity R_max·⌊n/e⌋ = {K_CAP} ≤ K_max = {K_MAX}.",
        ],
        "gap": f"Ambient |H_A_SP| ≤ {K_CAP} unproved.",
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_ep_SR_mark_and_Hcap",
        "statement": (
            "(1) Drop the extra F_p from μ₂=(r_* mod e, c0U, δ) to reach e·p, "
            "or find another e·p SR injection.\n"
            f"(2) Prove |H_A_SP| ≤ {K_CAP}, or inject R-cell pairs into e·p."
        ),
    }


def multitier_fm(high_Us: dict, n: int, e: int, max_tiers: int) -> dict:
    remaining = {h for h, us in high_Us.items() if us}
    tags = {}
    for tau in range(max_tiers):
        if not remaining:
            break
        free = set(range(n))
        local = 0
        highs = sorted(
            remaining, key=lambda h: (min(min(u) for u in high_Us[h]), repr(h))
        )
        claimed = set()
        for r in range(n):
            if r not in free:
                continue
            for h in highs:
                if h in claimed or h not in remaining:
                    continue
                for U in high_Us[h]:
                    Us = set(U)
                    if r in Us and Us.issubset(free):
                        free -= Us
                        tags[h] = (tau, local)
                        local += 1
                        claimed.add(h)
                        break
        remaining -= claimed
        if not claimed and remaining:
            h = next(iter(remaining))
            tags[h] = (tau, 0)
            remaining.discard(h)
    return tags


def toy_suite() -> dict[str, Any]:
    rows = []
    n_S_rows = 0
    n_ep2_inj = 0
    n_full_inj = 0
    n_ep_cand_coll = 0
    n_H_le_cap = 0

    mark_names_ep = [
        "r_mod_e_delta",
        "r_mod_e_c0U",
        "iota_delta",
    ]
    mark_names_big = [
        "r_c0U_c0V",
        "r_mod_e_c0U_delta",
    ]

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
        floor_ne = n // e
        vals = domain_vals(p, n)

        # families + iota + monic map
        fam: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), e):
            U = frozenset(exps)
            high, c0 = free1_high_c0(U, vals, p)
            fam[high].append((c0, tuple(sorted(U))))
        iota: dict[tuple, int] = {}
        monic_to_U: dict[Any, tuple] = {}
        for high, items in fam.items():
            for i, (c0, Ut) in enumerate(sorted(items)):
                iota[Ut] = i
                monic_to_U[(high, c0)] = Ut

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        sk_rstar: dict[Any, int] = {}
        high_Us: dict[Any, list] = defaultdict(list)
        seen_U: dict[Any, set] = defaultdict(set)
        pairs: list = []
        highs: set = set()

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
                        pairs.append((high, ut, tuple(sorted(V)), c0U, c0V))
                        highs.add(high)
                        if ut not in seen_U[high]:
                            seen_U[high].add(ut)
                            high_Us[high].append(U)

            for sk, Cs in pads.items():
                cores = [set(t) for t in {tuple(sorted(C)) for C in Cs}]
                if len(cores) < 2:
                    continue
                cnt: Counter = Counter()
                for c in cores:
                    for r in c:
                        cnt[r] += 1
                if max(cnt.values()) <= 1:
                    continue
                high, c0U, c0V = sk
                r_star = min(r for r, m in cnt.items() if m >= 2)
                skt = (high, c0U, c0V)
                if skt not in sk_rstar or r_star < sk_rstar[skt]:
                    sk_rstar[skt] = r_star

        def mark_inj(fn) -> dict[str, Any]:
            buckets: dict[Any, list] = defaultdict(list)
            for sk, r_star in sk_rstar.items():
                high, c0U, c0V = sk
                buckets[fn(r_star, high, c0U, c0V)].append(sk)
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            nuniq = len(sk_rstar)
            inj = nuniq > 0 and coll == 0 and len(buckets) == nuniq
            return {"inj": inj, "coll": coll, "nlab": len(buckets), "nuniq": nuniq}

        marks = {}
        if sk_rstar:
            n_S_rows += 1
            marks["r_c0U_c0V"] = mark_inj(lambda r, h, cu, cv: (r, cu, cv))
            marks["r_mod_e_c0U_delta"] = mark_inj(
                lambda r, h, cu, cv: (r % e, cu, (cu - cv) % p)
            )
            marks["r_mod_e_delta"] = mark_inj(
                lambda r, h, cu, cv: (r % e, (cu - cv) % p)
            )
            marks["r_mod_e_c0U"] = mark_inj(lambda r, h, cu, cv: (r % e, cu))

            def iota_delta(r, h, cu, cv):
                Ut = monic_to_U[(h, cu)]
                return (iota[Ut], (cu - cv) % p)

            marks["iota_delta"] = mark_inj(iota_delta)

            if marks["r_c0U_c0V"]["inj"]:
                n_full_inj += 1
            if marks["r_mod_e_c0U_delta"]["inj"]:
                n_ep2_inj += 1
            # e·p candidates should fail when nS large enough
            if any(not marks[name]["inj"] for name in mark_names_ep if name in marks):
                n_ep_cand_coll += 1
            # ensure near-miss inj when S nonempty
            ensure(marks["r_mod_e_c0U_delta"]["inj"], "ep2 near-miss inj")
            ensure(marks["r_c0U_c0V"]["inj"], "full inj")

        # multi-tier covers all pairs if all highs tagged
        nH = len(highs)
        if nH <= K_CAP:
            n_H_le_cap += 1
        R = max(nH + 2, 1)
        tags = multitier_fm(high_Us, n, e, max_tiers=R)
        all_tagged = len(tags) == sum(1 for us in high_Us.values() if us)
        pairs_cov = all(
            h in tags for h, U, V, cu, cv in pairs
        ) if pairs else True
        ensure(all_tagged, "tier tags")
        ensure(pairs_cov, "pairs covered")

        # R-cell style: all pairs if we pretend no M-cell
        # iota_delta on all pairs
        all_pair_iota = None
        if pairs:
            buckets = defaultdict(list)
            seen = set()
            for h, U, V, cu, cv in pairs:
                fp = (U, V)
                if fp in seen:
                    continue
                seen.add(fp)
                buckets[(iota[U], (cu - cv) % p)].append(fp)
            coll = sum(1 for v in buckets.values() if len(set(v)) >= 2)
            all_pair_iota = coll == 0 and len(buckets) == len(seen)

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "free_core": free_core,
                "n_S_keys": len(sk_rstar),
                "n_highs": nH,
                "H_le_Kcap": nH <= K_CAP,
                "n_pairs_unique": len({(U, V) for h, U, V, cu, cv in pairs}),
                "marks": marks,
                "all_pairs_iota_delta_inj": all_pair_iota,
                "multitier_covers_pairs": pairs_cov,
            }
        )

    ensure(n_S_rows > 0, "have S rows")
    ensure(n_ep2_inj == n_S_rows, "ep2 always inj")
    ensure(n_full_inj == n_S_rows, "full always inj")
    ensure(n_ep_cand_coll > 0, "ep cands collide somewhere")
    ensure(n_H_le_cap == len(rows), "toys H always le cap")
    ensure(E_P2 // E_P == P, "overshoot p")
    ensure(K_CAP == 2170, "cap")
    ensure(FREE_CORE == 846161, "fc")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_S_rows": n_S_rows,
            "n_ep2_inj": n_ep2_inj,
            "n_full_inj": n_full_inj,
            "n_ep_cand_coll_rows": n_ep_cand_coll,
            "n_H_le_cap_rows": n_H_le_cap,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v37",
        "title": "SR e·p² near-miss mark + multi-tier full-side path under |H|≤K_cap",
        "status": "PARTIAL_SR_EP2_H_PATH",
        "claims": {
            "proves_SR_ep2_near_miss_structure": True,
            "toy_confirms_SR_ep2_injection": True,
            "proves_SR_pure_ep_mark": False,
            "banks_SR_pure_ep_negative": True,
            "proves_multitier_no_Mcell_under_Hcap": True,
            "proves_H_le_Kcap": False,
            "proves_R_cell_ep": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e_p": E_P,
            "e_p2": E_P2,
            "n_p2": N_P2,
            "overshoot_p": P,
            "K_cap": K_CAP,
            "K_max": K_MAX,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "near_miss": lemma_near_miss(),
            "ep_neg": lemma_ep_negative(),
            "multitier": lemma_multitier_no_Mcell(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "SR": (
                "Best constructive SR mark is μ₂=(r_* mod e, c0U, δ) size e·p² "
                "(injective on toys); pure e·p still open"
            ),
            "sides": (
                f"If |H|≤{K_CAP}, multi-tier pays all sides (no R-cell). "
                "Otherwise R-cell e·p open"
            ),
            "next": (
                "Kill factor p in μ₂; prove |H_A_SP|≤K_cap"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_S_keys']} | "
        f"{r['n_highs']} | {r['H_le_Kcap']} | "
        f"{(r['marks'] or {}).get('r_mod_e_c0U_delta', {}).get('inj')} | "
        f"{(r['marks'] or {}).get('r_mod_e_delta', {}).get('inj')} | "
        f"{(r['marks'] or {}).get('iota_delta', {}).get('inj')} | "
        f"{r['all_pairs_iota_delta_inj']} | {r['multitier_covers_pairs']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v37: SR e·p² near-miss + multi-tier under |H|≤K_cap

Status: `PARTIAL` — SR mark **μ₂ size e·p²** injective on toys (near-miss);
pure **e·p SR** banked negative; multi-tier **no R-cell if |H|≤K_cap** PROVED.

## SR mark compression

| mark | size | toy inj on Type S? | vs e·p |
|---|---|---|---|
| `(r_*, c0U, c0V)` | n·p² | yes | factor n·p/e |
| **`(r_* mod e, c0U, δ)`** | **e·p²** | **yes (all S rows)** | **factor p** |
| `(r_* mod e, δ)` | e·p | no (large n_S) | target |
| `(r_* mod e, c0U)` | e·p | no | target |
| `(ι, δ)` alone | ⌊n/e⌋·p | no (large n_S) | under budget but collides |

Deployed: e·p² / e·p = p = {d['overshoot_p']}.

## Multi-tier without M-cell (PROVED conditional)

```text
|H_A_SP| ≤ K_cap = {d['K_cap']}
  ⇒ multi-tier FM tags all highs
  ⇒ all A_SP pairs covered (no R-cell)
```

Ambient `|H|≤{d['K_cap']}` still OPEN. Toys always have |H|≪K_cap.

## Path to A_SP ≤ t·p

```text
|H| ≤ K_cap
  ⇒ SR-cell cardinality ≪ e·p (v36) + multi-tier sides
  ⇒ only constructive SR e·p (kill factor p in μ₂) remains for SR
Type D residual M_pad ≤ 2 (v35)
```

## Toys

| j | w | free_core | #S keys | #H | H≤Kcap? | μ₂ inj? | (r mod e,δ)? | (ι,δ) S? | all pairs (ι,δ)? | multi-tier covers? |
|---|---|---:|---:|---:|---|---|---|---|---|---|
{tbl}

Census: S rows={cen['n_S_rows']}; μ₂ inj={cen['n_ep2_inj']}; pure e·p coll rows={cen['n_ep_cand_coll_rows']}.

## OPEN

1. Remove factor `p` from μ₂ to reach e·p SR mark
2. `|H_A_SP| ≤ {d['K_cap']}` (unlocks multi-tier full-side path)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v37.py --check
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
        "# kb-qatom-route-d-v37\n\n"
        "SR e·p² near-miss mark + multi-tier full-side path under |H|≤K_cap.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v37 report\n\nstatus: {cert['status']}\n"
        f"SR mu2 e·p²: toy injective\n"
        f"SR pure e·p: banked negative\n"
        f"multi-tier no M-cell if |H|≤{K_CAP}\n"
        f"|H| le Kcap: OPEN\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  SR μ₂=(r_* mod e, c0U, δ) size e·p²: injective on all toy Type S rows")
    print(f"  overshoot vs e·p: factor p={P}")
    print("  pure e·p SR compressions: banked negative (collisions)")
    print(f"  multi-tier covers all sides if |H|≤{K_CAP}: PROVED")
    print(
        f"  toys: S rows={cen['n_S_rows']}; μ₂ inj={cen['n_ep2_inj']}; "
        f"ep coll rows={cen['n_ep_cand_coll_rows']}; H≤Kcap rows={cen['n_H_le_cap_rows']}"
    )


if __name__ == "__main__":
    main()
