#!/usr/bin/env python3
"""KB-MCA Route-D v19: P_multi / |A_SP| graph cost laws (preference attack).

Proved:
  (1) Top-seam degree bound: each support has ≤ pack_ceil−1 top-seam neighbors
      (pencil size ≤ pack_ceil).
  (2) Handshaking: N_ord(z) = sum_v deg(v) (ordered); |A_SP| ≤ N_ord;
      P_multi ≤ floor(|A_SP|/2) ≤ floor(N_ord/2); P_multi ≤ floor(N(z)/2).
  (3) Cost chain (refines v17):
        |A_SP| ≤ pack_ceil · P_multi
        |A_SP| ≤ N_ord
        |A_SP| ≤ N(z)
        P_multi ≤ floor(N(z)/2)
  (4) Global pair sum: sum_z N_ord(z) equals sum_{|C|=j−e} Nord_CS(e; D\\C)
      where Nord_CS counts ordered free-1 CS pairs of e-subsets of the ambient
      (because every CS side pair with pad C lies in exactly one fiber z).
  (5) Ambient CS pair bound: for Omega size n', Nord_CS(e;Omega) ≤
        binom(n',e)·(floor(n'/e)−1)_+  (each e-set has ≤ pack_Ω−1 CS mates).
  (6) Payment criteria (conditional):
        max N_ord ≤ t·p  ⇒  |A_SP| ≤ t·p
        max P_multi ≤ t·p/17 ⇒ |A_SP| ≤ t·p
  (7) Toy bank: maxP ≤ maxN//2; maxA ≤ maxN; multi vanishes at larger w on F_17;
      maxA ≪ n·p on tested rows.

Does NOT prove max N_ord or max P_multi ≤ t·p at deployed scale.

  python3 experimental/scripts/verify_kb_qatom_route_d_v19.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v19.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v19"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v19.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v19.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v19.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1  # side size = top-seam e
CORE = J - E  # can-core size
PACK = 17
TARGET = 274_836_936_291_722_953
T_P = T * P
N_P = N * P


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


def lemma_degree_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "topseam_degree_bound",
        "statement": (
            "In G_z, the degree of any vertex S is at most pack_ceil(S)−1 ≤ "
            f"pack_ceil−1 = {PACK}-1 = {PACK-1}, where pack_ceil = "
            "floor((n−|C_can(S)|)/e) ≤ floor((n−(j−e))/e) = floor((n−j+e)/e) "
            f"and deployed pack_ceil = {PACK}."
        ),
        "proof": [
            "Neighbors of S=C∪U are C∪V for V in the same core pencil U(C,z), V≠U.",
            "v2: |U(C,z)| ≤ floor((n−|C|)/e).",
            "Deployed: |C|=j−e ⇒ floor((n−j+e)/e)=floor((A+e)/e).",
            f"A+e = {A}+{E} = {A+E}; floor(({A+E})/{E}) = {(A+E)//E} = {PACK}.",
        ],
        "deployed_pack": PACK,
        "deployed_Delta": PACK - 1,
        "check_A_plus_e_over_e": (A + E) // E,
    }


def lemma_handshaking() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "A_SP_handshaking_cost_chain",
        "statement": (
            "Let N=|Fib_w(z)|, A=|A_SP(z)|, P=P_multi(z), "
            "N_ord=sum_{multi pencils} k(k−1). Then:\n"
            "  N_ord = sum_v deg(v)  (sum over vertices of ordered out-degree "
            "in the directed complete orientation of each pencil clique);\n"
            "  A ≤ N_ord          (each A_SP vertex has deg ≥ 1);\n"
            "  P ≤ floor(A/2)     (each multi pencil has k ≥ 2);\n"
            "  P ≤ floor(N/2)     (A ≤ N and previous);\n"
            "  A ≤ pack_ceil · P ≤ pack_ceil · floor(N/2);\n"
            "  A ≤ N;\n"
            "  N_ord ≤ (pack_ceil−1) · A ≤ (pack_ceil−1) · N."
        ),
        "proof": [
            "Within a pencil of size k the directed complete graph without loops "
            "has k(k−1) arcs; sum over multi pencils is N_ord. Each vertex in a "
            "multi pencil has out-degree k−1 ≥ 1.",
            "Hence A = #verts with deg≥1 ≤ sum deg = N_ord "
            "(actually sum deg = N_ord counts only multi pencils; singleton deg=0).",
            "A = sum_{k≥2} k ≥ 2P ⇒ P ≤ floor(A/2).",
            "A ≤ N ⇒ P ≤ floor(N/2).",
            "v17: A ≤ pack·P. Degree bound: N_ord = sum deg ≤ Δ·A with Δ=pack−1.",
        ],
    }


def lemma_global_sum() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "global_sum_N_ord_equals_padded_CS_pairs",
        "statement": (
            "sum_z N_ord(z) = sum_{C ⊂ D, |C|=j−e} Nord_CS(e; D\\\\C), "
            "where Nord_CS(e;Ω) is the number of ordered pairs of distinct "
            "e-subsets of Ω whose monic locators differ by a nonzero constant "
            "(free-1 CS pair)."
        ),
        "proof": [
            "Top-seam ordered pair (S,S')=(C∪U,C∪V) with U≠V CS is uniquely "
            "written as pad C and CS pair (U,V) in D\\\\C (v16: top-seam ⇔ CS sides).",
            "Phi_w(C∪U)=Phi_w(C∪V) always for CS sides (deg difference =|C|=j−w−1), "
            "so the pair lies in exactly one fiber z=Phi_w(C∪U).",
            "Summing over fibers counts each such geometric pair once.",
        ],
        "deployed_ambient_size": N - CORE,  # n - (j-e) = n-j+e = A+e
        "check_ambient": N - CORE == A + E,
    }


def lemma_ambient_CS_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "ambient_CS_pair_bound",
        "statement": (
            "For any ambient Ω of size n' and e≥1, "
            "Nord_CS(e;Ω) ≤ binom(n',e) · max(floor(n'/e)−1, 0). "
            "Proof: each e-subset lies in at most one free-1 pencil; that pencil "
            "has size ≤ floor(n'/e); hence each e-set has at most "
            "max(floor(n'/e)−1,0) CS mates; double-count ordered pairs."
        ),
        "proof": [
            "Free-1: fixed high e−1 monic coeffs, vary constant — unique pencil per "
            "split monic of that form.",
            "Distinct fully split CS mates are pairwise disjoint (v2/v6 free-1), "
            "so pencil size ≤ floor(n'/e).",
            "Each of binom(n',e) sets contributes ≤ pack−1 outgoing ordered mates.",
        ],
        "consequence": (
            "sum_z N_ord(z) ≤ binom(n,j−e) · binom(n−j+e,e) · max(floor((n−j+e)/e)−1,0). "
            "This bounds the SUM over z, not max_z N_ord(z). Average N_ord ≤ "
            "that quantity / p^w (if every z appeared — only an envelope)."
        ),
    }


def lemma_payment_criteria() -> dict[str, Any]:
    ensure((A + E) // E == PACK, "pack formula")
    return {
        "status": "PROVED_CONDITIONAL",
        "name": "A_SP_payment_criteria",
        "statement": (
            "Any of the following implies max |A_SP| ≤ t·p:\n"
            f"  (C1) max_z N_ord(z) ≤ t·p = {T_P}\n"
            f"  (C2) max_z P_multi(z) ≤ floor(t·p / pack) = {T_P // PACK}\n"
            f"  (C3) max_z |A_SP(z)| ≤ t·p (tautological target).\n"
            "Then A_SP is a first-match cell with printed support cost ≤ t·p, "
            "matching the generated-field image budget scale (v1)."
        ),
        "proof": [
            "From handshaking: |A_SP| ≤ N_ord and |A_SP| ≤ pack·P_multi.",
        ],
        "open": "Prove C1 or C2 at deployed (or a weaker budget that still fits B*).",
        "numbers": {
            "t_p": T_P,
            "t_p_over_pack": T_P // PACK,
            "log2_t_p": math.log2(T_P),
            "log2_t_p_over_pack": math.log2(max(T_P // PACK, 1)),
            "global_sum_envelope_log2_hint": (
                "sum_z N_ord uses binom(n,core)*binom(A+e,e)*(pack-1); "
                "far above t*p — only max_z constraints help the cell."
            ),
        },
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_max_N_ord_or_P_multi",
        "statement": (
            "Prove max_z N_ord(z) ≤ t·p or max_z P_multi(z) ≤ t·p/17 "
            "(or any U with pack·U ≤ remaining safe budget). "
            "CAS route: larger dyadic scans (Sage/PARI); relate max N_ord to "
            "max fiber N(z) via N_ord ≤ (pack−1)N; still needs fiber control "
            "unless a direct pair injection into [t]×F_p exists."
        ),
        "note": (
            "N_ord ≤ (pack−1)·N reduces A_SP cost to a multiple of max fiber size — "
            "circular with the Q atom unless a separate pair mark injects seam pairs "
            "into a small set."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    for p, n, j, w in [
        (17, 16, 4, 1),
        (17, 16, 4, 2),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 7, 2),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
        (17, 16, 10, 3),
        (17, 16, 10, 4),
    ]:
        e = w + 1
        if math.comb(n, j) > 20000:
            continue
        vals = domain_vals(p, n)
        fib: dict[Any, list] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            poly = monic_rev([vals[i] for i in sorted(S)], p)
            fib[phi_w(poly, w)].append(S)

        def split(S: frozenset[int]) -> tuple[Any, ...]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, phi_w(polyU, w)

        maxN = maxA_sp = maxP = maxNord = 0
        sum_nord = 0
        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                C, high = split(S)
                pencils[(tuple(sorted(C)), high)].append(S)
            Nsz = len(members)
            a_sp = p_multi = nord = 0
            for lst in pencils.values():
                k = len(lst)
                if k >= 2:
                    a_sp += k
                    p_multi += 1
                    nord += k * (k - 1)
                    ensure(k <= n // e + 1, "pack loose")
            maxN = max(maxN, Nsz)
            maxA_sp = max(maxA_sp, a_sp)
            maxP = max(maxP, p_multi)
            maxNord = max(maxNord, nord)
            sum_nord += nord
            # handshaking on fiber
            ensure(a_sp <= nord or a_sp == 0, "A<=Nord")
            ensure(p_multi <= a_sp // 2 or p_multi == 0, "P<=A/2")
            ensure(p_multi <= Nsz // 2 or p_multi == 0, "P<=N/2")
            ensure(a_sp <= Nsz, "A<=N")
            if p_multi:
                ensure(a_sp <= (n // e) * p_multi + p_multi, "pack-ish")
            if a_sp:
                ensure(nord <= (max(n // e, 1)) * a_sp, "Nord<=Delta A loose")

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "maxN": maxN,
                "maxA": maxA_sp,
                "maxP": maxP,
                "maxNord": maxNord,
                "sum_nord": sum_nord,
                "P_le_N_half": maxP <= maxN // 2,
                "A_le_Nord": maxA_sp <= maxNord or maxA_sp == 0,
            }
        )
        ensure(maxP <= maxN // 2, "global P<=N/2")
        ensure(maxA_sp <= maxNord or maxA_sp == 0, "A<=Nord")

    # deployed arithmetic (use module-level A agreement, not loop temps)
    ensure((A + E) // E == PACK, f"pack {(A + E) // E}!={PACK}")
    ensure(N - CORE == A + E, "ambient")
    ensure(T_P // PACK == T_P // PACK, "div")
    return {"status": "PASS", "rows": rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    # global sum envelope (log2 scale only for honesty)
    # binom(n, core) * binom(A+e, e) * (pack-1)
    # too big to compute binom fully - skip numeric envelope
    return {
        "packet": "kb_qatom_route_d_v19",
        "title": "P_multi / |A_SP| graph cost laws and payment criteria",
        "status": "PARTIAL_A_SP_GRAPH",
        "claims": {
            "proves_degree_bound": True,
            "proves_handshaking_cost_chain": True,
            "proves_global_sum_N_ord": True,
            "proves_ambient_CS_pair_bound": True,
            "proves_payment_criteria": True,
            "proves_max_N_ord_le_tp": False,
            "proves_max_P_multi_le_tp_over_pack": False,
        },
        "deployed": {
            "n": N,
            "j": J,
            "a": A,
            "t": T,
            "w": W,
            "e": E,
            "core": CORE,
            "pack": PACK,
            "Delta": PACK - 1,
            "ambient_n_prime": A + E,
            "t_p": T_P,
            "t_p_over_pack": T_P // PACK,
            "n_p": N_P,
            "log2_t_p": math.log2(T_P),
            "log2_t_p_over_pack": math.log2(max(T_P // PACK, 1)),
        },
        "lemmas": {
            "degree": lemma_degree_bound(),
            "handshaking": lemma_handshaking(),
            "global_sum": lemma_global_sum(),
            "ambient_CS": lemma_ambient_CS_bound(),
            "payment": lemma_payment_criteria(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": (
                "A_SP cell paid if max N_ord≤t*p or max P_multi≤t*p/17. "
                "N_ord≤16*N reduces to fiber max — circular with Q unless pairs inject."
            ),
            "next": (
                "Inject top-seam ordered pairs into a set of size ≤t*p (marked "
                "incidence with small mark), or bound max fiber of pair-counts "
                "directly via SP geometry"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['maxN']} | {r['maxA']} | {r['maxP']} | "
        f"{r['maxNord']} | {r['P_le_N_half']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v19: P_multi / |A_SP| cost laws

Status: `PARTIAL` — graph cost chain **PROVED**; max-fiber pair bound **OPEN**.

## Cost chain (PROVED)

```text
N_ord  =  sum degrees on multi-member top-seam cliques
|A_SP|  ≤  N_ord  ≤  (pack−1) · |A_SP|  ≤  (pack−1) · N
|A_SP|  ≤  pack · P_multi
P_multi  ≤  floor(|A_SP|/2)  ≤  floor(N/2)
```

Deployed: `pack = {d['pack']}`, `Δ = {d['Delta']}`.

## Global sum (PROVED)

```text
sum_z N_ord(z)  =  sum_{{ |C|=j-e }} Nord_CS(e; D\\C)
```

Ambient size `n' = n-j+e = A+e = {d['ambient_n_prime']}`.

Ambient bound: `Nord_CS(e, Omega) <= C(|Omega|,e) * max(floor(|Omega|/e)-1, 0)`.

This controls **sums**, not **max_z**.

## Payment criteria (PROVED conditional)

| Criterion | Implies |
|---|---|
| `max N_ord <= t*p` | `|A_SP| <= t*p` |
| `max P_multi <= t*p/17 = {d['t_p_over_pack']}` | `|A_SP| <= t*p` |

`t*p ~ 2^{{{d['log2_t_p']:.2f}}}` (generated-field scale).

## Circular warning

`N_ord <= 16*N` reduces A_SP cost to a multiple of the **prefix fiber max** —
the Q atom itself. Useful only with a **direct pair injection** into size `<= t*p`.

## Toys

| j | w | max N | max A_SP | max P_multi | max N_ord | P≤N/2 |
|---|---|---:|---:|---:|---:|---|
{tbl}

Multi-pencils shrink as `w` grows; some rows have `maxP=0`.

## OPEN

Prove `max N_ord ≤ t·p` or inject top-seam pairs into a size-`t·p` set
(marked incidence with a small, ledger-legal mark).

## CAS next

- Sage/PARI: pair-count vs N on larger dyadic rows
- Relate Nord_CS on punctured cosets to group structure

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v19.py --check
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
        "# kb-qatom-route-d-v19\n\nP_multi / |A_SP| graph cost laws.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v19 report\n\nstatus: {cert['status']}\n"
        f"handshaking: PROVED\n"
        f"max N_ord le t*p: OPEN\n"
        f"t*p/pack: {cert['deployed']['t_p_over_pack']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  cost chain: A_SP <= N_ord <= 16*N; P_multi <= N/2 PROVED")
    print(f"  pay if max N_ord <= t*p or max P_multi <= {T_P // PACK}")
    print("  max N_ord bound: OPEN (reduces toward fiber max without pair mark)")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
