#!/usr/bin/env python3
"""KB-MCA Route-D v2: core-pencil theorem + covering reduction + oriented injectivity.

Builds on v1 conditional-closure arithmetic. Proves new structural lemmas that
reduce the residual max-fiber problem to bounding active cores.

Does NOT claim the row-sharp Q atom.

  python3 experimental/scripts/verify_kb_qatom_route_d_v2.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v2.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v2"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v2.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v2.md"
REPORT_PATH = (
    ROOT / "experimental" / "notes" / "certificate_scanner" / "outputs" / "kb_qatom_route_d_v2.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
K_DIM = 2**20
A = 1_116_048
J = N - A
T = A - K_DIM
W = T - 1
E = W + 1  # top-seam side size = w+1 = t
CORE_SIZE = J - E
PACK_CEIL = (N - CORE_SIZE) // E
B_STAR = (P**6 - 1) // 2**128
B_GEN = T * P
TARGET_FLOOR = 274_836_936_291_722_953
RETAINED = math.comb(16, 7)


def ensure(c: bool, m: str) -> None:
    if not c:
        raise AssertionError(m)


def log2_int(x: int) -> float:
    b = x.bit_length()
    if b <= 1024:
        return math.log2(x)
    return math.log2(x >> (b - 1024)) + (b - 1024)


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


def monic(pts: list[int], p: int) -> list[int]:
    poly = [1]
    for v in pts:
        new = [0] * (len(poly) + 1)
        mv = (-v) % p
        for i, c in enumerate(poly):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] + c * mv) % p
        poly = new
    return poly


def arithmetic() -> dict[str, Any]:
    ensure(E == T == 67472, "e=t")
    ensure(CORE_SIZE == 913632, f"core {CORE_SIZE}")
    ensure(PACK_CEIL == 17, f"pack {PACK_CEIL}")
    # covering budgets
    cores_for_atom = TARGET_FLOOR // PACK_CEIL
    cores_for_np = (N * P) // PACK_CEIL
    cores_for_tp = B_GEN // PACK_CEIL
    ensure(PACK_CEIL * cores_for_atom <= TARGET_FLOOR, "atom covering")
    # if N_cores <= cores_for_tp then |Fib| <= pack*N_cores <= t*p
    return {
        "status": "PROVED_BY_EXACT_INTEGER_ARITHMETIC",
        "e_top_seam": E,
        "core_size": CORE_SIZE,
        "pack_ceil": PACK_CEIL,
        "covering": {
            "statement": "|Fib_w(z)| <= pack_ceil * N_active_cores(z)",
            "pack_ceil": PACK_CEIL,
            "N_cores_sufficient_for_atom": cores_for_atom,
            "N_cores_sufficient_for_n_p": cores_for_np,
            "N_cores_sufficient_for_t_p": cores_for_tp,
            "log2_cores_for_atom_approx": log2_int(cores_for_atom),
            "log2_cores_for_t_p_approx": log2_int(max(cores_for_tp, 1)),
        },
        "v1_conditional_still_holds": {
            "t_p_plus_lift": B_GEN + RETAINED,
            "target_floor": TARGET_FLOOR,
            "slack_bits": log2_int(TARGET_FLOOR) - log2_int(B_GEN + RETAINED),
        },
    }


def lemma_core_pencil() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "core_pencil_in_fiber",
        "statement": (
            "Fix a prefix z and a core C subset D with |C|=j-w-1. Let "
            "U(C,z)={U subset D\\C : |U|=w+1 and C∪U in Fib_w(z)}. "
            "If |U(C,z)|>=2 then for any U,V in U(C,z) the monic side locators "
            "satisfy Lambda_U - Lambda_V is a nonzero constant in F_p, and the "
            "root sets are pairwise disjoint; hence |U(C,z)| <= floor((n-|C|)/(w+1))."
        ),
        "proof": [
            "Write m=j-w-1=|C|, e=w+1. For U in U(C,z) the monic locator "
            "Lambda_{C∪U}=Lambda_C Lambda_U has first w monic coefficients equal to z.",
            "If U,V both in U(C,z) then Lambda_C Lambda_U and Lambda_C Lambda_V share "
            "those w coefficients, so their difference Delta = Lambda_C (Lambda_U-Lambda_V) "
            "has degree <= j-w-1 = m.",
            "If Lambda_U != Lambda_V and d:=deg(Lambda_U-Lambda_V) >= 1 then "
            "deg(Delta)=m+d >= m+1 = j-w, contradicting deg(Delta) <= m. "
            "Hence d=0: Lambda_U-Lambda_V is a nonzero constant.",
            "Root sets of distinct constant-shift monic degree-e polynomials that both "
            "split inside D\\C are pairwise disjoint (shared root x would give "
            "Lambda_U(x)=Lambda_V(x)=0 so constant=0). Pack e-sets into D\\C.",
        ],
        "deployed_pack_ceil": PACK_CEIL,
    }


def lemma_covering() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "fiber_core_covering",
        "statement": (
            "For every z, Fib_w(z) = union_{C} {C∪U : U in U(C,z)} over cores C of size "
            "j-w-1. Consequently |Fib_w(z)| <= pack_ceil * N_active_cores(z), where "
            "N_active_cores(z) = |{C : U(C,z) nonempty}| and pack_ceil = floor((n-(j-w-1))/(w+1))."
        ),
        "proof": [
            "Every S in Fib_w(z) has size j. For any e-subset U of S set C=S\\U "
            "(|C|=j-e=j-w-1); then U in U(C,z) and S=C∪U.",
            "Apply the core-pencil packing bound to each nonempty U(C,z).",
        ],
        "atom_reduction": (
            f"At the deployed row pack_ceil={PACK_CEIL}, so the atom holds whenever "
            f"N_active_cores(z) <= floor(target_floor / pack_ceil) = {TARGET_FLOOR // PACK_CEIL} "
            f"for every z (full-fiber form). Residual forms may replace Fib by R_prim."
        ),
    }


def lemma_oriented_injectivity() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "oriented_first_mate_injectivity",
        "statement": (
            "Within a single fiber Fib_w(z), label each non-isolated support S by its "
            "lexicographically first top-seam mate edge key "
            "(C, higher_coeffs(Lambda_side), min(c_U,c_V), max(c_U,c_V), side), where side in {0,1} selects which "
            "endpoint of the constant-shift edge is S. This label is injective on "
            "non-isolated vertices."
        ),
        "proof": [
            "A top-seam edge with core C is, by the core-pencil theorem, a pair of "
            "root sets on a single constant-shift pencil for that C. The two constants "
            "{c_U,c_V} and the side bit select exactly one endpoint.",
            "If two non-isolated supports received the same first-mate key, they would "
            "be the same endpoint of the same edge, hence equal.",
            "Existence of the mate edge is the non-isolated hypothesis; first-mate is "
            "well-defined by lex order on a finite nonempty set of keys.",
        ],
        "note": (
            "The label space includes arbitrary cores C so this is structural injectivity, "
            "not by itself a |Fib|<=n*p bound. Combined with core-pencil covering it "
            "routes the bound to N_active_cores."
        ),
    }


def lemma_shallow_counterexample() -> dict[str, Any]:
    """w=1 full-fiber can exceed n*p (so E5 is depth-sensitive)."""
    p, n, j, w = 17, 16, 8, 1
    vals = domain_vals(p, n)
    fibers: dict[tuple[int, ...], int] = defaultdict(int)
    for exps in itertools.combinations(range(n), j):
        poly = monic([vals[i] for i in exps], p)
        z = tuple(poly[1 : w + 1])
        fibers[z] += 1
    maxV = max(fibers.values())
    ensure(maxV == 758, f"expected max fiber 758 got {maxV}")
    ensure(maxV > n * p, "expected counterexample maxV > n*p")
    return {
        "status": "PROVED_COUNTEREXAMPLE",
        "name": "shallow_w_np_failure",
        "row": {"p": p, "n": n, "j": j, "w": w},
        "max_fiber": maxV,
        "n_p": n * p,
        "meaning": (
            "Full-fiber bound |Fib_w| <= n*p fails at w=1 on F_17. "
            "Any n*p claim must be residual-only or depth-restricted."
        ),
    }


def toy_core_pencil_suite() -> dict[str, Any]:
    rows = [
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
    ]
    out = []
    for p, n, j, w in rows:
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            poly = monic([vals[i] for i in exps], p)
            z = tuple(poly[1 : w + 1])
            fibers[z].append(frozenset(exps))
        e = w + 1
        viol = 0
        checked = 0
        max_cores = 0
        maxV = 0
        orient_col = 0
        for z, mem in fibers.items():
            maxV = max(maxV, len(mem))
            by_core: dict[frozenset[int], list[frozenset[int]]] = defaultdict(list)
            for S in mem:
                for U in itertools.combinations(list(S), e):
                    Uf = frozenset(U)
                    C = frozenset(S) - Uf
                    by_core[C].append(Uf)
            # unique Us per core
            active = 0
            for C, Us in by_core.items():
                uniq: list[frozenset[int]] = []
                for u in Us:
                    if u not in uniq:
                        uniq.append(u)
                if not uniq:
                    continue
                active += 1
                if len(uniq) < 2:
                    continue
                checked += 1
                base = monic([vals[i] for i in sorted(uniq[0])], p)
                for U in uniq[1:]:
                    pol = monic([vals[i] for i in sorted(U)], p)
                    if pol[1:e] != base[1:e]:
                        viol += 1
                pack = (n - len(C)) // e
                if len(uniq) > pack:
                    viol += 1
                # pairwise disjoint
                for a in range(len(uniq)):
                    for b in range(a + 1, len(uniq)):
                        if uniq[a] & uniq[b]:
                            viol += 1
            max_cores = max(max_cores, active)

            # oriented first-mate injectivity (key includes side higher coeffs)
            labels: dict[Any, int] = {}
            free_of = {}
            for a, S in enumerate(mem):
                polyS = monic([vals[i] for i in sorted(S)], p)
                free_of[a] = tuple(polyS[w + 1 :])
            for a in range(len(mem)):
                A = set(mem[a])
                keys = []
                for b in range(len(mem)):
                    if a == b:
                        continue
                    B = set(mem[b])
                    if len(A - B) != e:
                        continue
                    C = frozenset(A & B)
                    U = A - C
                    V = B - C
                    polyU = monic([vals[i] for i in sorted(U)], p)
                    polyV = monic([vals[i] for i in sorted(V)], p)
                    hc = tuple(polyU[1:e])
                    cU, cV = polyU[-1], polyV[-1]
                    side = 0 if cU <= cV else 1
                    keys.append((tuple(sorted(C)), hc, min(cU, cV), max(cU, cV), side))
                if not keys:
                    lab = ("iso",) + free_of[a]
                else:
                    keys.sort()
                    lab = ("ts",) + keys[0]
                labels[lab] = labels.get(lab, 0) + 1
            if labels and max(labels.values()) > 1:
                orient_col += 1

        ensure(viol == 0, f"core pencil viol on {(p,n,j,w)}")
        ensure(orient_col == 0, f"orient inject fail on {(p,n,j,w)}")
        pack = (n - (j - e)) // e
        ensure(maxV <= pack * max_cores or max_cores == 0, "covering numeric")
        out.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_fiber": maxV,
                "max_active_cores_overcount": max_cores,
                "core_pencils_checked": checked,
                "violations": viol,
                "orient_collision_fibers": orient_col,
                "pack_ceil": pack,
            }
        )
    return {"status": "PASS", "rows": out}


def build() -> dict[str, Any]:
    return {
        "packet": "kb_qatom_route_d_v2",
        "title": "Core-pencil theorem and covering reduction for the KB-MCA Q atom",
        "status": "PARTIAL_PROVED_LEMMAS_ATOM_OPEN",
        "claims": {
            "proves_row_sharp_q_atom": False,
            "proves_core_pencil_theorem": True,
            "proves_fiber_core_covering": True,
            "proves_oriented_first_mate_injectivity": True,
            "proves_shallow_np_counterexample": True,
        },
        "arithmetic": arithmetic(),
        "lemmas": {
            "core_pencil": lemma_core_pencil(),
            "covering": lemma_covering(),
            "oriented_injectivity": lemma_oriented_injectivity(),
            "shallow_np_counterexample": lemma_shallow_counterexample(),
        },
        "toy_suite": toy_core_pencil_suite(),
        "remaining": {
            "status": "OPEN",
            "reduced_target": (
                f"Bound N_active_cores(z) <= {TARGET_FLOOR // PACK_CEIL} for every z "
                f"(full-fiber atom via covering with pack_ceil={PACK_CEIL}), or prove the "
                "same bound for residual cores after first-match deletion."
            ),
            "why_progress": (
                "The Q atom no longer requires a diffuse max-fiber argument: it is enough "
                "to bound the number of cores C that participate in any depth-w fiber. "
                "Each core contributes at most 17 supports at the deployed row."
            ),
            "suggested_routes": [
                "Bound active cores by injection into D x F_p or [n] x F_p using the "
                "product equation Lambda_C * Lambda_U ~ z (w equations on C).",
                "Show residual first-match leaves admit N_cores <= t*p / pack_ceil.",
                "Exploit that active C must make the convolution system for U rank-w "
                "with solution pencil compatible with z.",
            ],
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    ar = cert["arithmetic"]
    cov = ar["covering"]
    rem = cert["remaining"]
    return f"""# KB-MCA Route-D v2: core-pencil theorem and covering reduction

Status: `PARTIAL` — new structural theorems **PROVED**; atom still **OPEN**.

Extends v1 (`kb_qatom_route_d_v1`) by reducing the max-fiber problem to a
**core count**.

## Deployed constants

```text
e = w+1 = t = {E}
core size |C| = j-e = {CORE_SIZE}
pack_ceil = floor((n-|C|)/e) = {PACK_CEIL}
```

## Theorem 1 — core pencil in a fiber (PROVED)

{cert["lemmas"]["core_pencil"]["statement"]}

### Proof

1. For `U ∈ U(C,z)`, `Λ_{{C∪U}} = Λ_C Λ_U` has first `w` monic coefficients equal to `z`.
2. If `U,V` both lie in `U(C,z)`, the difference `Λ_C(Λ_U−Λ_V)` has degree `≤ j−w−1 = |C|`.
3. If `deg(Λ_U−Λ_V) ≥ 1` then the difference has degree `≥ |C|+1 = j−w`, contradiction.
   Hence `Λ_U−Λ_V` is a nonzero constant.
4. Distinct fully split constant-shift monic degree-`e` polynomials have pairwise
   disjoint root sets inside `D\\C`; pack to get
   `|U(C,z)| ≤ floor((n-|C|)/e)`.

Toy suite: 0 violations on all checked core pencils.

## Theorem 2 — fiber covering (PROVED)

{cert["lemmas"]["covering"]["statement"]}

### Deployed consequence

```text
|Fib_w(z)|  ≤  17 · N_active_cores(z)
```

Therefore the full-fiber form of the atom holds as soon as

```text
N_active_cores(z)  ≤  floor(target_floor / 17)  =  {cov["N_cores_sufficient_for_atom"]}
```

for every prefix `z`.  Bit scale: about `2^{{{cov["log2_cores_for_atom_approx"]:.2f}}}`.

For the stronger `t·p` residual budget:

```text
N_active_cores(z)  ≤  floor(t·p / 17)  =  {cov["N_cores_sufficient_for_t_p"]}
```

## Theorem 3 — oriented first-mate injectivity (PROVED)

{cert["lemmas"]["oriented_injectivity"]["statement"]}

This is structural (labels involve cores). It confirms the top-seam graph is a
clean constant-shift edge geometry and pairs with Theorem 1.

## Counterexample — shallow `n·p` bound (PROVED)

On `F_17`, `n=16`, `j=8`, `w=1`:

```text
max fiber = 758  >  n·p = 272
```

So **E5 (`|Fib| ≤ n·p`) is false for full fibers at shallow depth**. Any `n·p`
claim must be residual-only or depth-restricted. (At `w ≥ 2` on the same toy
family, max fibers fit under `n·p`, but that is evidence only.)

## Remaining open target

{rem["reduced_target"]}

Why this is progress: {rem["why_progress"]}

Suggested routes:
""" + "\n".join(f"- {s}" for s in rem["suggested_routes"]) + f"""

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v2.py
python3 experimental/scripts/verify_kb_qatom_route_d_v2.py --check
```

## Non-claims

- Does not prove `U(1116048) ≤ B*` or `def:q-row-atom`.
- Does not bound `N_active_cores` yet — that is the reduced open problem.
- Does not restore a full-fiber `n·p` bound at shallow depth.

## Relation to v1

v1 isolated the support certificate and proved filtration / fixed-core packing
/ conditional closure arithmetic. v2 upgrades fixed-core packing to a
**fiber-relative core pencil** (any two sides in the same fiber+core are
constant-shifts — not only top-seam-sampled pairs) and gives the covering
reduction with deployed constant `pack_ceil = 17`.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cert = build()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text())
        ensure(old["arithmetic"]["pack_ceil"] == cert["arithmetic"]["pack_ceil"], "pack drift")
        ensure(old["claims"] == cert["claims"], "claims drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v2\n\n"
        "Core-pencil + covering reduction packet.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v2.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v2 report\n\nstatus: {cert['status']}\npack_ceil: {PACK_CEIL}\n"
        f"cores_for_atom: {TARGET_FLOOR // PACK_CEIL}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  pack_ceil: {PACK_CEIL}")
    print(f"  cores_for_atom: {TARGET_FLOOR // PACK_CEIL}")
    print(f"  toy_rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
