#!/usr/bin/env python3
"""KB-MCA Route-D v4: residual-first N_can^prim (B) then full-fiber N_can (A).

B: Apply lex-split covering to the first-match residual R(z), not the full fiber.
   |R(z)| <= pack_ceil * N_can_prim(z). Exact residual core budgets.
A: Record full-fiber N_can structure (triangular inversion, m-subset routing)
   and toy measurements; no full-fiber close.

Does not claim the atom / U(1116048)<=B*.

  python3 experimental/scripts/verify_kb_qatom_route_d_v4.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v4.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v4"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v4.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v4.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v4.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
K_DIM = 2**20
T = A - K_DIM
W = T - 1
E = W + 1
CORE_SIZE = J - E
PACK = (N - CORE_SIZE) // E
B_STAR = (P**6 - 1) // 2**128
B_GEN = T * P
B_QUOT_TERM = math.comb(32, 14) + math.comb(16, 7)  # 471435600 + 11440
B_PAID = B_GEN + B_QUOT_TERM
B_REM = B_STAR - B_PAID
K_REM = 4_805_007
TARGET = 274_836_936_291_722_953  # floor(K_rem * C / p^w) from v1/v3
RETAINED = math.comb(16, 7)


def ensure(c: bool, m: str) -> None:
    if not c:
        raise AssertionError(m)


def log2_int(x: int) -> float:
    b = x.bit_length()
    return math.log2(x) if b <= 1024 else math.log2(x >> (b - 1024)) + (b - 1024)


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


def cyclic_stabilizer_order(exps: frozenset[int], n: int) -> int:
    """Largest c|n such that S is invariant under + (n/c) on exponents.
    Returns the stabilizer size |Stab| = c if S is union of cosets of the
    subgroup of index c... Standard: period = min d>0 with S = S + d (mod n).
    Stab order = n / period if period|n else 1 for aperiodic.
    """
    if not exps:
        return n
    # find minimal d>0 with rotation by d preserves S
    for d in range(1, n + 1):
        if n % d != 0:
            continue
        # rotation by d: exp |-> exp+d
        rot = frozenset((i + d) % n for i in exps)
        if rot == exps:
            # period d means stabilizer contains rotation by d; order of stab = n/d
            # minimal positive d with S+d=S is the period
            return n // d
    return 1


def is_pure_c_quotient(exps: frozenset[int], n: int, c: int) -> bool:
    """S is a union of complete fibers of pi_c : x |-> x^c, i.e. invariant
    under multiplication by omega^{n/c} (exponent + n/c)."""
    if c <= 1 or n % c != 0:
        return False
    step = n // c
    rot = frozenset((i + step) % n for i in exps)
    return rot == exps


def arithmetic_b() -> dict[str, Any]:
    """Residual budgets after proved paid cells."""
    ensure(PACK == 17, f"pack {PACK}")
    ensure(B_QUOT_TERM == 471447040, f"quot {B_QUOT_TERM}")
    ensure(B_PAID == 143763495894416, f"paid {B_PAID}")
    # Residual atom form: |R(z)| <= K_rem * avg ≈ TARGET (same TARGET as v1 K_rem form)
    # |R| <= pack * N_can_prim => need N_can_prim <= TARGET/pack
    ncan_prim_atom = TARGET // PACK
    # t*p residual certificate form from v1: G_gen_support + D_prim <= t*p
    # After lex-split on D_prim alone: |D_prim| <= pack * N_can_prim
    # Sufficient: N_can_prim <= floor(t*p / pack)  (ignoring G_gen for upper on D only)
    ncan_prim_tp = B_GEN // PACK
    # Combined residual with retained lift already in v1
    return {
        "status": "PROVED_BY_EXACT_INTEGER_ARITHMETIC",
        "paid_proved": {
            "B_gen_le_t_p": B_GEN,
            "B_quot_terminal": B_QUOT_TERM,
            "B_paid_proved": B_PAID,
            "B_rem_proved": B_REM,
            "K_rem_proved": K_REM,
        },
        "pack_ceil": PACK,
        "residual_core_budgets": {
            "N_can_prim_for_K_rem_atom": ncan_prim_atom,
            "N_can_prim_for_t_p_D_prim": ncan_prim_tp,
            "log2_N_can_prim_atom": log2_int(ncan_prim_atom),
            "log2_N_can_prim_tp": log2_int(max(ncan_prim_tp, 1)),
            "meaning": (
                "If max_z N_can_prim(z) <= N_can_prim_for_K_rem_atom then "
                "|R(z)| <= pack * N_can_prim <= TARGET and the K_rem residual "
                "flatness form holds for the residual fiber. "
                "If N_can_prim <= N_can_prim_for_t_p_D_prim then "
                "|D_prim| <= t*p, which with G_gen_support paid separately "
                "closes the v1 additive support certificate."
            ),
        },
        "v1_conditional_additive": {
            "hypothesis": "|G_gen_support| + |D_full_rank_prim| <= t*p",
            "with_lift": B_GEN + RETAINED,
            "target_floor": TARGET,
            "slack_bits": log2_int(TARGET) - log2_int(B_GEN + RETAINED),
        },
    }


def lemma_residual_lex_covering() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_lex_split_covering",
        "statement": (
            "Let R(z) subset Fib_w(z) be any subset of the depth-w fiber (in particular "
            "the first-match residual). Define C_can, c_U on R(z) exactly as in v3 "
            "lex-split. Then phi: S |-> (C_can(S), c_U(S)) is injective on R(z), and "
            "|R(z)| <= pack_ceil * N_can_prim(z) and |R(z)| <= p * N_can_prim(z), "
            "where N_can_prim(z) = |{C_can(S) : S in R(z)}|."
        ),
        "proof": [
            "The v3 lex-split injection proof never uses that S exhausts Fib_w(z); "
            "it only uses that all S under consideration share the same prefix z "
            "(so core-pencils live inside one fiber) and the core-pencil theorem. "
            "Restricting the domain to R(z) preserves injectivity.",
            "Covering: same as v3 double covering, summed only over cores that appear "
            "from residual supports.",
        ],
        "residual_definition_source": (
            "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md "
            "§First-match branches / Remaining target: R(z) removes generated-field, "
            "terminal quotient/planted, tangent/common-line, extension-confined, "
            "sparse/Pade-Hankel, M1/half-turn, contained/rank-drop assignments."
        ),
    }


def lemma_residual_excludes_terminal_quotients() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_excludes_terminal_quotient_supports",
        "statement": (
            "Under the ledger residual definition, every S in R(z) is not assigned to "
            "terminal quotient/planted at c in {65536, 131072}. In particular R(z) "
            "contains no support that is a pure union of complete c-fibers for those "
            "terminal c (the Q0 raw-paid terminal classes)."
        ),
        "proof": [
            "By definition of R(z) in the first-match ledger (branch 4 terminal pay). "
            "This is a definitional exclusion, not a new geometric theorem.",
        ],
        "deployed_terminal_c": [65536, 131072],
        "toy_proxy": (
            "On toys we proxy 'quotient-assigned' by pure c-periodicity for all c|n, c>1 "
            "(stronger than terminal-only). Residual proxy = aperiodic supports "
            "(trivial cyclic stabilizer)."
        ),
    }


def lemma_full_fiber_m_subset_routing() -> dict[str, Any]:
    """Path A infrastructure."""
    return {
        "status": "PROVED",
        "name": "full_fiber_can_core_m_subset_routing",
        "statement": (
            "For S in Fib_w(z) with lex-split (C,U), the first w monic coefficients b of "
            "Lambda_C are the triangular function b=b(z,u) of the first w monic "
            "coefficients u of Lambda_U (v3). Consequently every canonical core C(S) "
            "lies in the m-subset depth-w fiber Fib_w^{(m)}(b(z,u(S)))."
        ),
        "proof": [
            "v3 triangular inversion under m >= w (deployed).",
            "C is an m-subset whose monic locator has prefix b(z,u).",
        ],
        "consequence": (
            "N_can(z) <= sum_{u in F_p^w} |Fib_w^{(m)}(b(z,u))|, which is tautological "
            "at worst p^w * max_m_fiber. Useful only with a sharp bound on m-subset "
            "fibers or with few u realized by residual/full sides."
        ),
        "open": (
            "Bound the number of realized side-prefixes u from residual/full S, or "
            "bound m-subset fibers at depth w with constants fitting 2^53.84."
        ),
    }


def toy_suite() -> dict[str, Any]:
    """B: aperiodic residual proxy + N_can_prim covering.
    A: full-fiber N_can measurements.
    """
    rows = [
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
    ]
    out = []
    for p, n, j, w in rows:
        e = w + 1
        ensure(e < j, f"nonempty cores {(p,n,j,w)}")
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            poly = monic([vals[i] for i in exps], p)
            z = tuple(poly[1 : w + 1])
            fibers[z].append(frozenset(exps))
        pack = (n - (j - e)) // e

        maxV = 0
        maxR = 0
        max_Ncan = 0
        max_Ncan_prim = 0
        inj_fail = 0
        covering_fail = 0
        # ratio residual/full
        sumV = 0
        sumR = 0

        for z, mem in fibers.items():
            V = len(mem)
            maxV = max(maxV, V)
            sumV += V
            # residual proxy: trivial cyclic stabilizer (aperiodic)
            R = []
            for S in mem:
                # stabilizer order 1 means period n (only full rotation)
                # minimal d|n with S+d=S; if only d=n, aperiodic in strong sense
                period = n
                for d in range(1, n):
                    if n % d == 0 and frozenset((i + d) % n for i in S) == S:
                        period = d
                        break
                # pure quotient for some c>1 iff period < n
                if period == n:
                    R.append(S)
            maxR = max(maxR, len(R))
            sumR += len(R)

            def ncan(supports: list[frozenset[int]]) -> int:
                cans: set[tuple[int, ...]] = set()
                phi: dict[Any, frozenset[int]] = {}
                nonlocal inj_fail
                for S in supports:
                    s_sorted = sorted(S)
                    U = frozenset(s_sorted[:e])
                    C = frozenset(S) - U
                    polyU = monic([vals[i] for i in sorted(U)], p)
                    c = polyU[-1]
                    key = (tuple(sorted(C)), c)
                    if key in phi and phi[key] != S:
                        inj_fail += 1
                    phi[key] = S
                    cans.add(tuple(sorted(C)))
                return len(cans)

            nc = ncan(mem)
            ncp = ncan(R) if R else 0
            max_Ncan = max(max_Ncan, nc)
            max_Ncan_prim = max(max_Ncan_prim, ncp)
            if V > pack * max(nc, 1):
                covering_fail += 1
            if R and len(R) > pack * max(ncp, 1):
                covering_fail += 1
            if R and len(R) > p * max(ncp, 1):
                covering_fail += 1

        ensure(inj_fail == 0, f"inj fail {(p,n,j,w)}")
        ensure(covering_fail == 0, f"covering fail {(p,n,j,w)}")
        out.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "pack": pack,
                "max_full_fiber": maxV,
                "max_residual_proxy_fiber": maxR,
                "max_N_can_full": max_Ncan,
                "max_N_can_prim_proxy": max_Ncan_prim,
                "total_supports": sumV,
                "total_residual_proxy": sumR,
                "residual_fraction": (sumR / sumV) if sumV else 0.0,
                "inj_fail": inj_fail,
                "covering_fail": covering_fail,
            }
        )
    return {
        "status": "PASS",
        "residual_proxy": (
            "aperiodic = trivial cyclic period n (not pure c-quotient for any c>1)"
        ),
        "rows": out,
    }


def build() -> dict[str, Any]:
    return {
        "packet": "kb_qatom_route_d_v4",
        "title": "Residual-first N_can^prim (B) and full-fiber N_can routing (A)",
        "status": "PARTIAL_PROVED_LEMMAS_ATOM_OPEN",
        "claims": {
            "proves_row_sharp_q_atom": False,
            "proves_residual_lex_covering": True,
            "proves_residual_excludes_terminal_quotients_definitional": True,
            "proves_full_fiber_m_subset_routing": True,
            "proves_N_can_prim_bound": False,
            "proves_N_can_full_bound": False,
        },
        "path_B_residual": {
            "arithmetic": arithmetic_b(),
            "lemmas": {
                "residual_lex_covering": lemma_residual_lex_covering(),
                "residual_excludes_terminal_quotients": lemma_residual_excludes_terminal_quotients(),
            },
            "open_target": (
                f"Prove max_z N_can_prim(z) <= {TARGET // PACK} (K_rem residual flatness) "
                f"or <= {B_GEN // PACK} (sufficient for |D_prim| <= t*p)."
            ),
        },
        "path_A_full_fiber": {
            "lemmas": {
                "m_subset_routing": lemma_full_fiber_m_subset_routing(),
            },
            "open_target": (
                f"Prove max_z N_can(z) <= {TARGET // PACK} for full fibers "
                "(harder; shallow counterexamples to crude n*p remain)."
            ),
        },
        "toy_suite": toy_suite(),
        "priority": "B_then_A",
    }


def render_note(cert: dict[str, Any]) -> str:
    b = cert["path_B_residual"]["arithmetic"]
    rb = b["residual_core_budgets"]
    toys = cert["toy_suite"]["rows"]
    toy_lines = "\n".join(
        f"| {r['p']} | {r['n']} | {r['j']} | {r['w']} | {r['max_full_fiber']} | "
        f"{r['max_residual_proxy_fiber']} | {r['max_N_can_full']} | "
        f"{r['max_N_can_prim_proxy']} | {r['residual_fraction']:.4f} |"
        for r in toys
    )
    return f"""# KB-MCA Route-D v4: residual-first N_{{\\mathrm{{can}}}}^{{\\mathrm{{prim}}}} (B → A)

Status: `PARTIAL` — residual lex-covering **PROVED**; N_{{\\mathrm{{can}}}}^{{\\mathrm{{prim}}}} bound **OPEN**.

Priority: **B then A** as requested.

## Path B - residual first

### Residual fiber (ledger)

From `kb_mca_1116048_first_match_ledger_v1.md`, after first-match assignment:

```text
R(z) = {{ S : |S|=j, Phi_w(S)=z, not assigned to
         generated-field / terminal quotient-planted / tangent /
         extension / sparse-Pade / M1-half-turn / contained-rank-drop }}
```

Proved paid so far: generated image cells `<= t*p` and terminal quotient
`c in {{65536,131072}}` raw-paid. Other branches still open as payments but
are **removed from R(z) by definition** when assigned.

### Theorem B1 — residual lex-split covering (PROVED)

{cert["path_B_residual"]["lemmas"]["residual_lex_covering"]["statement"]}

### Residual core budgets (PROVED arithmetic)

```text
pack_ceil = {PACK}
B_paid_proved = {b["paid_proved"]["B_paid_proved"]}
K_rem = {K_REM}
target_floor ≈ K_rem * avg = {TARGET}

N_can_prim  ≤  floor(target_floor / 17)  =  {rb["N_can_prim_for_K_rem_atom"]}
              ≈  2^{{{rb["log2_N_can_prim_atom"]:.2f}}}
              ⇒  |R(z)| ≤ target_floor   (K_rem residual flatness form)

N_can_prim  ≤  floor(t*p / 17)  =  {rb["N_can_prim_for_t_p_D_prim"]}
              ≈  2^{{{rb["log2_N_can_prim_tp"]:.2f}}}
              ⇒  |D_prim| ≤ t*p          (feeds v1 additive certificate)
```

### Open (B)

{cert["path_B_residual"]["open_target"]}

## Path A — full-fiber N_{{\\mathrm{{can}}}}

### Theorem A1 — m-subset routing (PROVED)

{cert["path_A_full_fiber"]["lemmas"]["m_subset_routing"]["statement"]}

### Open (A)

{cert["path_A_full_fiber"]["open_target"]}

## Toy suite (B proxy + A measurements)

Residual **proxy** on toys: aperiodic supports (cyclic period n; not pure
c-quotient for any c>1). Stronger than terminal-only exclusion; good
for stress-testing covering on a residual-like set.

| p | n | j | w | max full | max R proxy | max N_can | max N_can_prim | R fraction |
|---|---|---|---|---:|---:|---:|---:|---:|
{toy_lines}

All rows: lex-injection and pack/p coverings hold on full and residual-proxy sets.

## Chain

| Version | Result |
|---|---|
| v1 | Conditional `t*p+11440` ⇒ atom |
| v2 | Core-pencil; pack_ceil=17 |
| v3 | Lex-split injection; wall = N_can |
| **v4** | **Residual R(z) inherits lex-covering; wall = N_can_prim (B); m-subset routing for A** |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v4.py
python3 experimental/scripts/verify_kb_qatom_route_d_v4.py --check
```

## Non-claims

- Not `U(1116048)<=B*` / not `def:q-row-atom`.
- Does not bound `N_can_prim` or full `N_can`.
- Toy residual is a **proxy** (aperiodic), not the full ledger residual predicate.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cert = build()
    if args.check and CERT_PATH.exists():
        old = json.loads(CERT_PATH.read_text())
        ensure(
            old["path_B_residual"]["arithmetic"]["pack_ceil"]
            == cert["path_B_residual"]["arithmetic"]["pack_ceil"],
            "pack drift",
        )
        ensure(old["claims"] == cert["claims"], "claims drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v4\n\nResidual-first N_can_prim (B→A).\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v4.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    rb = cert["path_B_residual"]["arithmetic"]["residual_core_budgets"]
    REPORT_PATH.write_text(
        f"# v4 report\n\nstatus: {cert['status']}\n"
        f"N_can_prim_atom: {rb['N_can_prim_for_K_rem_atom']}\n"
        f"N_can_prim_tp: {rb['N_can_prim_for_t_p_D_prim']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  N_can_prim for K_rem atom: {rb['N_can_prim_for_K_rem_atom']}")
    print(f"  N_can_prim for t*p D_prim: {rb['N_can_prim_for_t_p_D_prim']}")
    print(f"  toy_rows: {len(cert['toy_suite']['rows'])}")
    for r in cert["toy_suite"]["rows"]:
        print(
            f"    p={r['p']} w={r['w']}: full={r['max_full_fiber']} "
            f"R={r['max_residual_proxy_fiber']} "
            f"Ncan={r['max_N_can_full']} Ncan_prim={r['max_N_can_prim_proxy']} "
            f"Rfrac={r['residual_fraction']:.3f}"
        )


if __name__ == "__main__":
    main()
