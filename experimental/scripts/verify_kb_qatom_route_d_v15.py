#!/usr/bin/env python3
"""KB-MCA Route-D v15: ledger residual injection via top-seam / marked incidence.

Attack OPEN_RES_MASS along E2/E5 using first-match + top-seam geometry
(not multi-mate taxonomy tourism).

Proved:
  (1) Top-seam graph G_z on Fib_w(z): edges = distinct residual/full supports
      sharing can-core C with free-1 CS sides (core pencil U(C,z)).
  (2) Matching-free mass law: if R ⊆ Fib_w(z) is matching-free in G_z
      (no edge has both endpoints in R), then each active can-core has at most
      one residual support, so |R| ≤ N_can(R) ≤ |R| wait N_can ≤ |R| always,
      and |R| ≤ N_can_active — actually |R| ≤ N_can(R) with equality of
      cardinalities when every residual uses a distinct core: |R| = N_can_prim.
      Pack covering improves: |R| ≤ 1 · N_can_prim (pack_ceil drops to 1).
  (3) Under matching-free, residual supports biject with residual can-cores
      (S ↔ C_can(S)); side prefix u is determined by (z, C) via triangular
      inversion, so residual mass = core count.
  (4) Oriented first-mate injectivity on non-isolated vertices (v2 import):
      labels are structural, not E2-scale.
  (5) Marked-incidence normal form for top-seam pairs (import): with marked
      core G, seam neighbors inject into (B, c) data — image/pair form, not
      raw residual support injection.
  (6) Bridge to E2/E5: if ledger residual is matching-free (H_seam) and
      residual can-cores inject into a set of size ≤ t·p (resp. n·p), then
      |R| ≤ t·p (resp. n·p) and residual mass closes (v14 budgets).
  (7) H_seam status: SP/bc first-match deletions in the ledger residual
      definition make H_seam the intended residual seam hypothesis; it is
      NOT proved here as a theorem that every multi-member core pencil is
      fully removed from residual (needs SP payment theorem). Conditional.
  (8) Toy bank: aperiodic + seam-free proxy has |R|=N_can; naive marks
      (min S, c_U), (min U, c_U), (min C, b1) still collide per fiber —
      not E2 injections.

Does NOT prove ledger residual injection or U(1116048)≤B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v15.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v15.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v15"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v15.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v15.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v15.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20  # 67472
W = T - 1
E = W + 1
M = J - E
PACK = 17
TARGET = 274_836_936_291_722_953
N_P = N * P
T_P = T * P


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


def aperiodic(exps: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in exps) == exps:
            return False
    return True


def lemma_top_seam_graph() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "top_seam_graph_core_pencil",
        "statement": (
            "Fix z. On vertex set Fib_w(z), declare an edge between distinct "
            "S, S' when C_can(S)=C_can(S')=C and the lex sides U, U' both lie in "
            "the core pencil U(C,z). By the core-pencil theorem (v2), U(C,z) is "
            "empty or a free-1 constant-shift family, so the connected components "
            "of this graph inside each core are cliques of size |U(C,z)| ≤ "
            "floor((n-|C|)/e) = pack_ceil (deployed 17)."
        ),
        "proof": [
            "v2 Theorem 1: sides for fixed (C,z) form a CS pencil packing into D\\\\C.",
            "v3: C_can is the lex core; top-seam at e=w+1 is exactly free-1 CS.",
            "Two supports with the same can-core and sides in U(C,z) are adjacent.",
        ],
        "deployed_pack_ceil": PACK,
    }


def lemma_matching_free_mass() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matching_free_residual_mass_law",
        "statement": (
            "Let R ⊆ Fib_w(z) be matching-free in the top-seam graph G_z "
            "(no edge has both ends in R). Then for every core C, "
            "|{S ∈ R : C_can(S)=C}| ≤ 1. Consequently "
            "|R| = N_can_prim(R) := |{C_can(S): S∈R}|, "
            "and the residual lex covering improves from pack_ceil=17 to pack=1: "
            "|R| ≤ 1 · N_can_prim(R)."
        ),
        "proof": [
            "If two residual supports share C_can=C, their lex sides both lie in "
            "U(C,z) (same z, same core, both in fiber), hence form a top-seam "
            "edge, contradicting matching-free unless the supports are equal.",
            "Thus C_can is injective on R, so |R| = N_can_prim(R).",
            "Covering |R| ≤ pack · N_can with pack=1 is immediate.",
        ],
        "consequence": (
            "Under matching-free residual, residual mass reduces exactly to the "
            "residual can-core count. Atom ⇔ N_can_prim ≤ TARGET (or ≤ t·p / n·p)."
        ),
    }


def lemma_matching_free_side_determined() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "matching_free_side_determined_by_core_and_z",
        "statement": (
            "Under matching-free R ⊆ Fib_w(z), each residual S is uniquely "
            "determined by C=C_can(S): the side U is the unique member of "
            "U(C,z) that appears in R (at most one), and triangular inversion "
            "relates side prefix u to core prefix b and z (v3)."
        ),
        "proof": [
            "Matching-free ⇒ at most one residual support per core.",
            "That support is C ∪ U for the unique residual side U ∈ U(C,z) ∩ R.",
            "v3 triangular inversion: b = b(z,u) couples core and side prefixes.",
        ],
    }


def lemma_oriented_first_mate() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "oriented_first_mate_on_nonisolated",
        "statement": (
            "Within Fib_w(z), non-isolated vertices (degree ≥1 in G_z) inject into "
            "oriented first-mate edge keys "
            "(C, high_side_coeffs, min(c_U,c_V), max(c_U,c_V), side) (v2 Thm 3). "
            "This is structural bookkeeping for seam pairs; the label space is not "
            "of size t·p or n·p."
        ),
        "proof": ["Imported from v2 oriented first-mate injectivity."],
        "note": (
            "Under matching-free residual, R has no non-isolated residual vertices, "
            "so this injection is vacuous on residual — residual labels must come "
            "from isolated-support marks."
        ),
    }


def lemma_marked_incidence_normal_form() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "top_seam_marked_incidence_normal_form",
        "statement": (
            "For a top-seam pair with common core G marked, and sides A,B monic of "
            "degree e=w+1 with A−B=c ∈ F_p^×, the oriented seam neighbor injects "
            "into ordered split-translate data (B,c) (with divisor conditions "
            "B|Λ_E, B+c|Λ_{D\\\\E} up to orientation). This is a fixed-mark / "
            "pair normal form (rowsharp top-seam marked incidence; LQ top-seam "
            "audit), not a raw unmarked support bound."
        ),
        "proof": [
            "Degree bound at e=w+1 forces A−B constant (v2 core pencil / rowsharp).",
            "With G marked and orientation chosen, the free data is (B,c).",
            "Hostile audit: without mark/selector this is not a global support cap.",
        ],
        "sources": [
            "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md",
            "experimental/notes/thresholds/cap25_v13_lq_top_seam_hostile_audit.md",
            "experimental/notes/thresholds/kb_qatom_route_d_v2.md Thm 3",
        ],
    }


def lemma_H_seam() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL_HYPOTHESIS",
        "name": "H_seam_ledger_residual_matching_free",
        "statement": (
            "Hypothesis H_seam: the ledger residual R(z) (after first-match "
            "deletion of generated_field, quotient_planted, sparse_pade_hankel, "
            "m1_window_shadow, rank_drop_pivot, bc_chart, sp_shift_pair, "
            "extension_slope — v1/rowsharp) is matching-free in G_z.\n"
            "Under H_seam, |R(z)| = N_can_prim(z), and residual mass reduces to "
            "bounding residual can-cores (or injecting them / residual supports "
            "into size ≤ t·p or n·p)."
        ),
        "proof": [
            "Conditional: apply matching-free mass law once H_seam is granted.",
            "Justification sketch (not a proof): sp_shift_pair / bc_chart are "
            "named first-match deletions targeting constant-shift / chart pairs; "
            "if every multi-member top-seam pencil is assigned there, residual "
            "cannot contain both ends of a seam edge.",
            "Gap: need a theorem that SP/BC payment removes multi-member core "
            "pencils from residual support (not only image-cell charges).",
        ],
        "status_of_H_seam": "OPEN (intended by ledger branch list; not proved)",
    }


def lemma_E2_E5_bridge() -> dict[str, Any]:
    ensure(T_P < TARGET, "tp")
    ensure(N_P < TARGET, "np")
    return {
        "status": "PROVED",
        "name": "matching_free_plus_injection_closes_mass",
        "statement": (
            "Assume H_seam (so |R|=N_can_prim). Then:\n"
            "  (E5') residual can-cores inject into a set of size ≤ n·p "
            "⇒ |R| ≤ n·p ⇒ residual mass (v14);\n"
            "  (E2') residual can-cores inject into a set of size ≤ t·p "
            "⇒ |R| ≤ t·p ⇒ residual mass + E1-scale D_prim budget;\n"
            "  (E2)  residual supports inject into {0..t-1}×F_p "
            "⇒ |R| ≤ t·p (rowsharp missing theorem form);\n"
            "  (E5)  residual supports inject into D×F_p ⇒ |R| ≤ n·p.\n"
            "Under H_seam, support injection and can-core injection are equivalent "
            "cardinality problems (bijection S ↔ C_can)."
        ),
        "proof": [
            "H_seam ⇒ |R|=N_can_prim (matching-free mass law).",
            "Injection of R or of C_res into L ⇒ |R|≤|L|.",
            "v14: |R|≤t·p and |R|≤n·p both fit under TARGET.",
            "rowsharp: E2 form is marked-incidence into {0..t-1}×F_p.",
        ],
        "numbers": {
            "t_p": T_P,
            "n_p": N_P,
            "TARGET": TARGET,
            "log2_t_p": math.log2(T_P),
            "log2_n_p": math.log2(N_P),
        },
    }


def lemma_open_injection() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_LEDGER_RESIDUAL_INJECTION",
        "statement": (
            "Prove H_seam for ledger residual, AND prove one of:\n"
            "  (i)  residual supports/cores inject into {0,...,t-1}×F_p (E2),\n"
            "  (ii) residual supports/cores inject into D×F_p (E5),\n"
            "using first-match marks (generated-field style row index, marked "
            "incidence with selector, full-rank pivot certificate, …), not "
            "aperiodic proxy alone.\n"
            "Either closes residual mass at deployed row (v14/v15 bridges)."
        ),
        "falsifier": (
            "Ledger residual R(z) with a top-seam edge inside R (refutes H_seam), "
            "or |R(z)| > t·p after all named first-match deletions (refutes E2 mass)."
        ),
        "do_not": [
            "Global multi-mate taxonomy without injection",
            "Unmarked top-seam counting without core mark (hostile audit)",
            "Full-fiber n·p at shallow w (v2 counterexample)",
        ],
    }


def lemma_naive_marks_fail() -> dict[str, Any]:
    return {
        "status": "PROVED_NEGATIVE_TOY_BANK",
        "name": "naive_isolated_marks_not_E2",
        "statement": (
            "On aperiodic + seam-free residual-proxy fibers, |R|=N_can, but maps "
            "S ↦ (min S, c_U), S ↦ (min U, c_U), S ↦ (min C, b_1) are not "
            "injective (per-fiber max label fiber ≥2 on multiple toys). These "
            "marks do not prove E2/E5."
        ),
        "proof": ["Computational certificates in toy_suite."],
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    for p, n, j, w in [
        (17, 16, 9, 2),
        (17, 16, 7, 2),
        (17, 16, 10, 3),
        (17, 16, 6, 2),
        (17, 16, 9, 3),
        (17, 16, 5, 2),
    ]:
        e = w + 1
        if math.comb(n, j) > 12000:
            continue
        vals = domain_vals(p, n)
        fib: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            S = frozenset(exps)
            z = phi_w(monic_rev([vals[i] for i in sorted(S)], p), w)
            fib[z].append(S)

        def split(
            S: frozenset[int],
        ) -> tuple[frozenset[int], tuple[int, ...], int, frozenset[int]]:
            ss = sorted(S)
            U = frozenset(ss[:e])
            C = S - U
            polyU = monic_rev([vals[i] for i in sorted(U)], p)
            return C, phi_w(polyU, w), polyU[-1], U

        max_full = 0
        max_ap = 0
        max_strong = 0
        max_ncan = 0
        worst_marks = {
            "minS_cU": 1,
            "minU_cU": 1,
            "minC_b1": 1,
            "lex_CcU": 1,
        }
        for _z, members in fib.items():
            max_full = max(max_full, len(members))
            pencils: dict[Any, list] = defaultdict(list)
            splits: dict[Any, Any] = {}
            for S in members:
                C, high, c0, U = split(S)
                splits[S] = (C, high, c0, U)
                pencils[(tuple(sorted(C)), high)].append(S)
            ap = [S for S in members if aperiodic(S, n)]
            max_ap = max(max_ap, len(ap))
            # matching-free strong: aperiodic and unique in pencil
            strong = []
            for S in ap:
                C, high, c0, U = splits[S]
                if len(pencils[(tuple(sorted(C)), high)]) == 1:
                    strong.append(S)
            max_strong = max(max_strong, len(strong))
            cores = {tuple(sorted(splits[S][0])) for S in strong}
            max_ncan = max(max_ncan, len(cores))
            if strong:
                ensure(len(strong) == len(cores), "matching-free => |R|=Ncan")
                invs = {
                    "minS_cU": defaultdict(int),
                    "minU_cU": defaultdict(int),
                    "minC_b1": defaultdict(int),
                    "lex_CcU": defaultdict(int),
                }
                for S in strong:
                    C, high, c0, U = splits[S]
                    invs["minS_cU"][(min(S), c0)] += 1
                    invs["minU_cU"][(min(U), c0)] += 1
                    polyC = monic_rev([vals[i] for i in sorted(C)], p)
                    invs["minC_b1"][(min(C), polyC[1] if len(polyC) > 1 else 0)] += 1
                    invs["lex_CcU"][(tuple(sorted(C)), c0)] += 1
                ensure(max(invs["lex_CcU"].values()) == 1, "lex dual")
                for k, inv in invs.items():
                    worst_marks[k] = max(worst_marks[k], max(inv.values()))

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_full": max_full,
                "max_ap": max_ap,
                "max_strong": max_strong,
                "max_Ncan_strong": max_ncan,
                "R_eq_Ncan": max_strong == max_ncan or max_strong == 0,
                "n_p": n * p,
                "strong_fits_n_p": max_strong <= n * p,
                "worst_marks": worst_marks,
            }
        )

    ensure(all(r["R_eq_Ncan"] for r in rows), "R=Ncan")
    ensure(any(r["worst_marks"]["minS_cU"] > 1 for r in rows), "naive collide")
    ensure(T_P < TARGET and N_P < TARGET, "budgets")
    return {"status": "PASS", "rows": rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v15",
        "title": "Ledger residual injection: top-seam matching-free + E2/E5 bridges",
        "status": "PARTIAL_INJECTION_ATTACK",
        "claims": {
            "proves_top_seam_graph": True,
            "proves_matching_free_mass_law": True,
            "proves_matching_free_bijection_core": True,
            "proves_oriented_first_mate_import": True,
            "proves_marked_incidence_normal_form": True,
            "proves_H_seam": False,
            "proves_E2_injection": False,
            "proves_E5_injection": False,
            "proves_residual_mass_atom": False,
            "banks_naive_mark_failures": True,
        },
        "deployed": {
            "a_plus": A,
            "n": N,
            "j": J,
            "t": T,
            "w": W,
            "e": E,
            "m": M,
            "p": P,
            "pack_full": PACK,
            "pack_matching_free": 1,
            "TARGET": TARGET,
            "t_p": T_P,
            "n_p": N_P,
            "E2_label_space": T_P,
            "E5_label_space": N_P,
        },
        "lemmas": {
            "top_seam_graph": lemma_top_seam_graph(),
            "matching_free_mass": lemma_matching_free_mass(),
            "side_determined": lemma_matching_free_side_determined(),
            "oriented_first_mate": lemma_oriented_first_mate(),
            "marked_incidence": lemma_marked_incidence_normal_form(),
            "H_seam": lemma_H_seam(),
            "E2_E5_bridge": lemma_E2_E5_bridge(),
            "OPEN_LEDGER_RESIDUAL_INJECTION": lemma_open_injection(),
            "naive_marks": lemma_naive_marks_fail(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "reduction": (
                "H_seam + (E2 or E5 injection) => residual mass atom. "
                "H_seam turns mass into core count; injection is the remaining mark."
            ),
            "next": (
                "Prove H_seam from SP/BC first-match payment theorem; construct "
                "ledger marks into [t]×F_p or D×F_p for isolated residual supports"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['max_full']} | {r['max_ap']} | {r['max_strong']} | "
        f"{r['max_Ncan_strong']} | {r['R_eq_Ncan']} | {r['worst_marks']['minS_cU']} | "
        f"{r['worst_marks']['minU_cU']} | {r['worst_marks']['lex_CcU']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v15: ledger residual injection (top-seam / marked incidence)

Status: `PARTIAL` — matching-free mass law + E2/E5 bridges **PROVED**;
H_seam and actual injection **OPEN**.

## Attack surface (on track)

Close residual mass by **injection**, not multi-mate tourism:

```text
E2:  residual injects into {{0,...,t-1}} x F_p     size t*p = {d['t_p']}
E5:  residual injects into D x F_p                 size n*p = {d['n_p']}
```

Both fit under TARGET = {d['TARGET']} (v14).

## Top-seam graph (PROVED)

Vertices: supports in `Fib_w(z)`.
Edges: same lex can-core, sides in core pencil `U(C,z)` (free-1 CS).
Components: cliques of size ≤ pack_ceil = {d['pack_full']}.

## Matching-free mass law (PROVED)

If `R ⊆ Fib_w(z)` is **matching-free** (no seam edge inside R):

```text
|R| = N_can_prim(R)
pack covering: |R| ≤ 1 · N_can_prim
```

Residual mass = residual can-core count. Side is determined by `(z, C)`.

## H_seam (conditional / open)

Ledger residual (v1 deletions include `sp_shift_pair`, `bc_chart`) is **intended**
to be matching-free. Not proved here without an SP/BC payment theorem that
removes multi-member core pencils from residual support.

```text
H_seam  =>  |R| = N_can_prim
H_seam + E2/E5 injection  =>  residual mass atom
```

## Marked incidence (PROVED normal form, not mass)

With **marked** core G, top-seam neighbors inject into `(B, c)` split-translate
data. Unmarked counting is invalid (hostile audit). Oriented first-mate (v2)
labels non-isolated vertices — vacuous under matching-free residual.

## OPEN_LEDGER_RESIDUAL_INJECTION

1. Prove **H_seam** for ledger residual, and
2. Inject residual supports/cores into `[t] x F_p` or `D x F_p`

using first-match marks (selector, pivot row, …).

## Toy bank (aperiodic + seam-free proxy)

| j | w | max full | max ap | max strong | Ncan | R=Ncan | max(minS,cU) | max(minU,cU) | lex |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
{tbl}

Strong proxy: `|R|=N_can`. Naive D×F_p-scale marks still collide.

## Non-claims

Not `U(1116048)≤B*`. Not H_seam. Not E2/E5 injection. Not global uniqueness.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v15.py
python3 experimental/scripts/verify_kb_qatom_route_d_v15.py --check
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
        ensure(old["deployed"]["t_p"] == cert["deployed"]["t_p"], "tp drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v15\n\n"
        "Ledger residual injection: top-seam matching-free + E2/E5 bridges.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v15.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v15 report\n\nstatus: {cert['status']}\n"
        f"H_seam: OPEN\n"
        f"E2/E5 injection: OPEN\n"
        f"matching_free_mass_law: PROVED\n"
        f"toy rows: {len(cert['toy_suite']['rows'])}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  matching-free mass law: |R|=N_can (pack=1) PROVED")
    print("  H_seam (ledger residual matching-free): OPEN")
    print("  E2/E5 injection: OPEN")
    print(f"  under H_seam+E2: |R|<=t*p={T_P} closes mass")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
