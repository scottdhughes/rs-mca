#!/usr/bin/env python3
"""KB-MCA Route-D v38: SR enum mark → e·p under |H| gate + load bound on |H|.

Attacks factor-p removal from μ₂ and |H_A_SP|≤2170.

Proved:
  (1) SR enumeration mark: order Type S side keys by (r_*, c0U, c0V) lex
      (r_* domain order, then field order on c0U, c0V). Let i(sk)∈{0..N_S−1}
      be the rank. Define
        μ_enum(sk) = (i mod e,  ⌊i/e⌋) ∈ [e] × {{0,1,...,⌊(N_S−1)/e⌋}}.
      This is injective. If N_S ≤ e·p then ⌊i/e⌋ < p, so μ_enum lands in
      [e]×F_p (identify {{0..p−1}}⊂F_p), size ≤ e·p.
  (2) Under |H|≤K_cap=2170: N_S ≤ 2170·31·30 = 2018100 ≤ e·p deployed
      (v36), hence μ_enum is a size-e·p injection of SR-events. PROVED.
  (3) Local pure compressions of μ₂ without global rank — (r_* mod e, δ),
      (r_* mod e, c0U), (ι,δ) — still collide (v37 bank).
  (4) Load bound on highs: let L = max_r |{{ H ∈ H_A_SP : r ∈ cover(H) }}|
      where cover(H)=⋃ active U of high H. Then |H_A_SP| ≤ (n/e)·L
      (since |cover(H)|≥e and covers pack with load ≤L). Deployed:
      |H| ≤ 31 L, so L≤70 ⇒ |H|≤2170.
  (5) Within high, each r lies in at most one active U (v25), so L equals the
      max number of A_SP-active free-1 e-sets through a single domain point.
  (6) Optional ledger thinning: H^{≤R_max} := highs matched in multi-tier FM
      with tier < R_max=70 has |H^{≤R_max}|≤K_cap by construction (v34).
  (7) Toy bank: μ_enum inj; μ₂ inj; e·p local compressions collide when n_S large;
      load L measured; 31L bounds |H|.

Does NOT prove L≤70 at deployed scale, nor ambient |H|≤2170 without the load gate.

  python3 experimental/scripts/verify_kb_qatom_route_d_v38.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v38.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v38"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v38.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v38.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v38.report.md"
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
L_GATE = K_CAP // FLOOR_N_OVER_E  # 70
N_S_UNDER_HCAP = K_CAP * FLOOR_N_OVER_E * (FLOOR_N_OVER_E - 1)  # 2018100


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


def lemma_enum_mark() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "SR_enumeration_mark_ep_under_NS_le_ep",
        "statement": (
            "Order Type S side keys by (r_*, c0U, c0V) lexicographically. "
            "Let i(sk) be the rank in {{0,...,N_S−1}}. Set "
            "μ_enum(sk)=(i mod e, ⌊i/e⌋). Then μ_enum is injective. "
            "If N_S ≤ e·p then ⌊i/e⌋ ≤ p−1, so μ_enum injects into [e]×F_p."
        ),
        "proof": [
            "Lex rank is a bijection from the finite set of Type S keys to "
            "{{0,...,N_S−1}}.",
            "Map i ↦ (i mod e, ⌊i/e⌋) is injective on {{0,...,N_S−1}} "
            "(standard mixed radix).",
            "If N_S ≤ e·p then ⌊i/e⌋ ≤ ⌊(e·p−1)/e⌋ = p−1, embed into F_p.",
        ],
        "with_Hcap": (
            f"Under |H|≤{K_CAP}: N_S≤{N_S_UNDER_HCAP}≤e·p={E_P} (v36) ⇒ "
            "μ_enum is a size-e·p SR injection. PROVED conditional on |H|≤K_cap."
        ),
    }


def lemma_load_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "high_load_bound",
        "statement": (
            "Let cover(H)=⋃{{U active free-1 e-set of high H}}. "
            "Let L=max_r |{{H: r∈cover(H)}}|. Then |H_A_SP| ≤ (n·L)/e. "
            f"Deployed: |H| ≤ {FLOOR_N_OVER_E}·L, so L≤{L_GATE} ⇒ |H|≤{K_CAP}."
        ),
        "proof": [
            "Within one high, active U's are pairwise disjoint (v25) ⇒ "
            "|cover(H)| = e·|# active U of H| ≥ e if H has ≥1 active U.",
            "sum_H |cover(H)| = sum_r load(r) ≤ n·L.",
            "sum_H |cover(H)| ≥ e·|H| ⇒ |H| ≤ n·L/e.",
            "Also load(r) = # active free-1 e-sets containing r "
            "(at most one U per high through r).",
        ],
        "deployed_gate": {"L_max_for_Hcap": L_GATE, "K_cap": K_CAP},
        "open": f"Prove L≤{L_GATE} at deployed A_SP activity.",
    }


def lemma_optional_thinning() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "optional_FM_tier_thinning_to_Kcap",
        "statement": (
            f"Define H^{{≤R}} as highs matched by multi-tier FM with tier < R. "
            f"Then |H^{{≤R}}| ≤ R·⌊n/e⌋. Taking R=R_max={K_CAP // FLOOR_N_OVER_E} "
            f"gives |H^{{≤R}}| ≤ {K_CAP}. This is a ledger definition forcing the "
            "high gate; pairs whose highs have tier ≥R need a residual cell."
        ),
        "proof": ["v34 multi-tier size per tier ≤⌊n/e⌋."],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_L_gate_or_ambient_Hcap",
        "statement": (
            f"(1) Prove L≤{L_GATE} (max A_SP free-1 e-sets through one domain point) "
            f"⇒ |H|≤{K_CAP}.\n"
            "(2) Or adopt H^{≤R_max} thinning as the A_SP high set and pay "
            "overflow pairs in a residual cell."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    n_S_rows = 0
    n_enum_inj = 0
    n_mu2_inj = 0
    n_ep_local_coll = 0
    max_L_seen = 0

    ensure(N_S_UNDER_HCAP <= E_P, "NS room")
    ensure(L_GATE == 70, "Lgate")
    ensure(K_CAP == 2170, "Kcap")
    # enum fits: max second coord
    max_i = N_S_UNDER_HCAP - 1
    ensure(max_i // E < P, "floor i/e < p")

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

        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        sk_rstar: dict[Any, int] = {}
        high_Us: dict[Any, list] = defaultdict(list)
        seen_U: dict[Any, set] = defaultdict(set)
        pairs: list = []
        pt_highs: dict[int, set] = defaultdict(set)

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
                        if ut not in seen_U[high]:
                            seen_U[high].add(ut)
                            high_Us[high].append(U)
                            for x in U:
                                pt_highs[x].add(high)

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

        nH = len(high_Us)
        loads = [len(s) for s in pt_highs.values()]
        L = max(loads) if loads else 0
        max_L_seen = max(max_L_seen, L)
        # |H| <= n*L/e
        if nH > 0 and L > 0:
            ensure(nH * e <= n * L + e, "load bound soft")  # allow tiny slack
            # strict: sum cover >= e*nH, sum cover = sum load <= n*L
            sum_cover = sum(e * len(us) for us in high_Us.values())
            sum_load = sum(loads)
            # each point counted once per high in cover - load is |highs through r|
            # sum_H |cover H| = sum_r load(r)
            sum_cover_exact = sum(len(set().union(*[set(u) for u in us])) for us in high_Us.values())
            # use exact covers
            covers = {
                h: set().union(*[set(u) for u in us]) if us else set()
                for h, us in high_Us.items()
            }
            sum_c = sum(len(c) for c in covers.values())
            pt_h2: dict[int, set] = defaultdict(set)
            for h, cset in covers.items():
                for r in cset:
                    pt_h2[r].add(h)
            L2 = max((len(s) for s in pt_h2.values()), default=0)
            ensure(sum_c == sum(len(s) for s in pt_h2.values()), "double count")
            ensure(all(len(covers[h]) == e * len(high_Us[h]) for h in high_Us), "disj cover")
            ensure(nH * e <= n * L2, f"H load bound {nH}*e > n*{L2}")
            L = L2

        # μ_enum
        enum_inj = None
        mu2_inj = None
        ep_local_coll = None
        if sk_rstar:
            n_S_rows += 1
            ordered = sorted(
                sk_rstar.keys(),
                key=lambda sk: (sk_rstar[sk], sk[1], sk[2], repr(sk[0])),
            )
            rank = {sk: i for i, sk in enumerate(ordered)}
            # enum mark
            buckets_e: dict[Any, list] = defaultdict(list)
            for sk, i in rank.items():
                lab = (i % e, i // e)
                buckets_e[lab].append(sk)
            enum_inj = (
                all(len(set(v)) == 1 for v in buckets_e.values())
                and len(buckets_e) == len(sk_rstar)
            )
            ensure(enum_inj, "enum inj")
            n_enum_inj += 1
            # second coord fits in F_p iff N_S ≤ e·p
            max_second = max(i // e for i in rank.values())
            if len(sk_rstar) <= e * p:
                ensure(max_second < p, "second < p when NS≤e·p")
            # deployed-scale gate uses |H|≤K_cap ⇒ NS≪e·p

            # μ2
            buckets2: dict[Any, list] = defaultdict(list)
            for sk, r_star in sk_rstar.items():
                high, c0U, c0V = sk
                lab = (r_star % e, c0U, (c0U - c0V) % p)
                buckets2[lab].append(sk)
            mu2_inj = (
                all(len(set(v)) == 1 for v in buckets2.values())
                and len(buckets2) == len(sk_rstar)
            )
            ensure(mu2_inj, "mu2 inj")
            n_mu2_inj += 1

            # e·p local
            for fn in [
                lambda sk: (sk_rstar[sk] % e, (sk[1] - sk[2]) % p),
                lambda sk: (sk_rstar[sk] % e, sk[1]),
            ]:
                b = defaultdict(list)
                for sk in sk_rstar:
                    b[fn(sk)].append(sk)
                if any(len(set(v)) >= 2 for v in b.values()):
                    ep_local_coll = True
            if ep_local_coll:
                n_ep_local_coll += 1

        H_bound = (n * L) // e if L else 0
        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "e": e,
                "free_core": free_core,
                "n_S": len(sk_rstar),
                "n_H": nH,
                "L": L,
                "H_bound_nL_over_e": H_bound,
                "H_le_bound": nH <= H_bound if L else True,
                "L_le_gate_toy": L <= L_GATE,
                "enum_inj": enum_inj,
                "mu2_inj": mu2_inj,
                "ep_local_coll": ep_local_coll,
                "H_le_Kcap": nH <= K_CAP,
            }
        )

    ensure(n_S_rows > 0, "S")
    ensure(n_enum_inj == n_S_rows, "enum")
    ensure(n_mu2_inj == n_S_rows, "mu2")
    ensure(n_ep_local_coll > 0, "ep coll")
    ensure(FREE_CORE == 846161, "fc")
    ensure(N_S_UNDER_HCAP <= E_P, "room")
    # under Hcap, max second coord of enum
    ensure((N_S_UNDER_HCAP - 1) // E < P, "deployed enum fits F_p")
    ensure(T == E, "t=e")

    return {
        "status": "PASS",
        "rows": rows,
        "census": {
            "n_S_rows": n_S_rows,
            "n_enum_inj": n_enum_inj,
            "n_mu2_inj": n_mu2_inj,
            "n_ep_local_coll": n_ep_local_coll,
            "max_L_seen": max_L_seen,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v38",
        "title": "SR enum mark e·p under |H| gate + load bound |H|≤(n/e)L",
        "status": "PARTIAL_ENUM_SR_LOAD_H",
        "claims": {
            "proves_SR_enum_mark_ep_under_NS_le_ep": True,
            "proves_SR_enum_under_Hcap": True,
            "proves_local_ep_compression_from_mu2": False,
            "banks_local_ep_negative": True,
            "proves_load_bound_H_le_nL_over_e": True,
            "proves_L_le_70_deployed": False,
            "proves_H_le_Kcap_ambient": False,
            "proves_optional_tier_thinning_Kcap": True,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "e_p": E_P,
            "K_cap": K_CAP,
            "L_gate": L_GATE,
            "floor_n_over_e": FLOOR_N_OVER_E,
            "N_S_under_Hcap": N_S_UNDER_HCAP,
            "enum_second_max_under_Hcap": (N_S_UNDER_HCAP - 1) // E,
            "free_core": FREE_CORE,
            "t_p": T_P,
        },
        "lemmas": {
            "enum_mark": lemma_enum_mark(),
            "load_bound": lemma_load_bound(),
            "thinning": lemma_optional_thinning(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "SR": (
                "μ_enum gives constructive e·p SR injection whenever N_S≤e·p "
                f"(ensured by |H|≤{K_CAP}). Local drop of c0U from μ₂ still fails."
            ),
            "H": (
                f"|H|≤(n/e)L; need L≤{L_GATE} for |H|≤{K_CAP}, or use tier thinning"
            ),
            "next": (
                f"Prove L≤{L_GATE} at deployed A_SP, or adopt H^{{≤R_max}} as A_SP highs"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    cen = cert["toy_suite"]["census"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['free_core']} | {r['n_S']} | {r['n_H']} | "
        f"{r['L']} | {r['H_bound_nL_over_e']} | {r['enum_inj']} | {r['mu2_inj']} | "
        f"{r['ep_local_coll']} | {r['H_le_Kcap']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v38: SR enum → e·p under |H| gate + load bound on |H|

Status: `PARTIAL` — **μ_enum SR mark size e·p under |H|≤K_cap** PROVED;
**|H|≤(n/e)L** PROVED; L≤70 / ambient |H|≤2170 still **OPEN**.

## SR enumeration mark (PROVED)

Order Type S side keys by `(r_*, c0U, c0V)` lex. Rank `i ∈ {{0..N_S−1}}`:

```text
μ_enum = (i mod e,  ⌊i/e⌋)
```

Injective. If `N_S ≤ e·p` then `⌊i/e⌋ < p` ⇒ lands in `[e]×F_p`.

### Under |H|≤K_cap={d['K_cap']}

```text
N_S ≤ {d['N_S_under_Hcap']} ≤ e·p
⇒ μ_enum is a size-e·p constructive SR injection
```

Local drop of `c0U` from μ₂ (no global rank) still collides on toys.

## Load bound on |H| (PROVED)

```text
L = max_r  #{{ A_SP highs whose cover contains r }}
|H_A_SP|  ≤  (n/e) · L
```

Deployed: `|H| ≤ 31·L`. Gate: **`L ≤ {d['L_gate']}` ⇒ `|H| ≤ {d['K_cap']}`**.

Optional ledger: `H^{{≤R_max}}` from multi-tier FM has size ≤K_cap by definition.

## Path

```text
L ≤ 70  (or H thinning)
  ⇒ |H| ≤ 2170
  ⇒ μ_enum : SR → e·p
  ⇒ multi-tier sides
  ⇒ Type D residual M_pad ≤ 2
  ⇒ A_SP ≤ t·p path
```

## Toys

| j | w | free_core | #S | #H | L | (n/e)L | enum inj? | μ₂ inj? | ep local coll? | H≤Kcap? |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|
{tbl}

Census: enum inj={cen['n_enum_inj']}/{cen['n_S_rows']}; max L={cen['max_L_seen']}.

## OPEN

1. Prove `L ≤ {d['L_gate']}` at deployed A_SP (or accept tier thinning)
2. Prefer local SR mark without global enumeration if possible

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v38.py --check
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
        "# kb-qatom-route-d-v38\n\n"
        "SR enum mark e·p under |H| gate + load bound on |H|.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v38 report\n\nstatus: {cert['status']}\n"
        f"mu_enum e·p under |H|≤{K_CAP}: PROVED\n"
        f"|H|≤(n/e)L: PROVED; L≤{L_GATE} for Hcap: OPEN\n"
        f"local ep drop c0U: banked negative\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(
        f"  μ_enum SR → e·p under |H|≤{K_CAP} (N_S≤{N_S_UNDER_HCAP}≤e·p): PROVED"
    )
    print("  local drop of c0U from μ₂: still collides (banked)")
    print(f"  |H| ≤ (n/e)·L; L≤{L_GATE} ⇒ |H|≤{K_CAP}: PROVED gate")
    print(
        f"  toys: enum inj={cen['n_enum_inj']}/{cen['n_S_rows']}; "
        f"max L={cen['max_L_seen']}"
    )


if __name__ == "__main__":
    main()
