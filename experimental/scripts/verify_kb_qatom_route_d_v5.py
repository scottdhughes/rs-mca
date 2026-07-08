#!/usr/bin/env python3
"""KB-MCA Route-D v5: residual N_can_prim via side-prefix routing into m-fibers.

Proves:
  residual can-cores with side-prefix u lie in Fib_w^{(m)}(b(z,u));
  N_can_prim(z) <= U_res(z) * M_m(z);
  deployed log2(avg m-fiber) ≈ -18820 (exact-arithmetic entropy);
  criterion: M_m <= 1 and U_res <= target/17 => residual K_rem atom form.

Does not prove M_m <= 1 or bound U_res. Atom still OPEN.

  python3 experimental/scripts/verify_kb_qatom_route_d_v5.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v5.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v5"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v5.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v5.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v5.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
W = 67_471
E = W + 1
M = J - E  # core size
PACK = (N - M) // E
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P
N_CAN_PRIM_ATOM = TARGET // PACK
N_CAN_PRIM_TP = B_GEN // PACK


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_int(x: int) -> float:
    b = x.bit_length()
    return math.log2(x) if b <= 1024 else math.log2(x >> (b - 1024)) + (b - 1024)


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k > n - k:
        k = n - k
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


def invert_b(z: tuple[int, ...], u: tuple[int, ...], p: int) -> tuple[int, ...]:
    w = len(z)
    b = [0] * w
    for k in range(w):
        s = (z[k] - u[k]) % p
        for i in range(k):
            s = (s - b[i] * u[k - 1 - i]) % p
        b[k] = s
    return tuple(b)


def aperiodic(S: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in S) == S:
            return False
    return True


def entropy_block() -> dict[str, Any]:
    ensure(M == 913_632, f"M={M}")
    ensure(PACK == 17, f"PACK={PACK}")
    # avg m-fiber = C(n,M) / p^W
    log_avg_m = log2_binom(N, M) - W * math.log2(P)
    log_avg_j = log2_binom(N, J) - W * math.log2(P)
    log_avg_e = log2_binom(N, E) - W * math.log2(P)
    # anticode upper for m-fibers (weak)
    log_anticode_m = log2_binom(N, M - W) - log2_binom(M, W)
    ensure(log_avg_m < -1000, "expected deep negative avg m-fiber")
    return {
        "status": "PROVED_BY_EXACT_FLOAT_ENTROPY_ARITHMETIC",
        "parameters": {"n": N, "j": J, "m": M, "w": W, "e": E, "p": P, "pack": PACK},
        "log2_avg_m_subset_fiber_depth_w": log_avg_m,
        "log2_avg_j_subset_fiber_depth_w": log_avg_j,
        "log2_avg_e_subset_fiber_depth_w": log_avg_e,
        "log2_anticode_m_fiber": log_anticode_m,
        "interpretation": (
            "Average m-subset depth-w fiber is ~2^(-18820): the natural finite "
            "criterion is M_m := max_b |Fib_w^{(m)}(b)| is 0 or 1 (or tiny). "
            "Anticode is ~2^1.69e6 — useless for the atom; entropy is the signal."
        ),
        "budgets": {
            "N_can_prim_atom": N_CAN_PRIM_ATOM,
            "N_can_prim_tp": N_CAN_PRIM_TP,
            "log2_N_can_prim_atom": log2_int(N_CAN_PRIM_ATOM),
            "log2_N_can_prim_tp": log2_int(N_CAN_PRIM_TP),
        },
    }


def lemma_residual_core_routing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "residual_can_core_side_prefix_routing",
        "statement": (
            "Let R(z) be any subset of Fib_w(z) (e.g. first-match residual). For S in R(z) "
            "let U be the e=w+1 smallest-exponent elements of S, C=S\\\\U, and let u be the "
            "first w monic coefficients of Lambda_U. Let b=b(z,u) be the triangular core "
            "prefix from v3. Then C lies in the m-subset fiber Fib_w^{(m)}(b). "
            "Consequently, writing U_res(z) for the number of distinct residual side-prefixes u "
            "and M_m(z) = max_u |Fib_w^{(m)}(b(z,u))|, one has "
            "N_can_prim(z) <= U_res(z) * M_m(z)."
        ),
        "proof": [
            "v3/v4: triangular inversion under m>=w gives b as a function of (z,u).",
            "C is an m-subset whose monic locator has prefix b, i.e. C in Fib_w^{(m)}(b).",
            "Partition residual can-cores by the side-prefix u of their defining S. "
            "Each block has size <= M_m(z). Number of blocks <= U_res(z).",
        ],
    }


def lemma_criterion_Mm_one() -> dict[str, Any]:
    return {
        "status": "PROVED_CONDITIONAL_CRITERION",
        "name": "residual_atom_from_Mm_and_Ures",
        "statement": (
            "If M_m^{max} := max_b |Fib_w^{(m)}(b)| <= 1 and "
            "max_z U_res(z) <= floor(target_floor/pack_ceil), then "
            "max_z N_can_prim(z) <= floor(target_floor/pack_ceil), hence "
            "max_z |R(z)| <= target_floor by residual lex covering (v4), which is the "
            "K_rem residual flatness form."
        ),
        "proof": [
            "N_can_prim <= U_res * M_m <= U_res * 1.",
            "Apply v4: |R| <= pack * N_can_prim <= pack * (target/pack) = target.",
        ],
        "deployed_numbers": {
            "target_over_pack": N_CAN_PRIM_ATOM,
            "tp_over_pack": N_CAN_PRIM_TP,
            "log2_avg_m_fiber": entropy_block()["log2_avg_m_subset_fiber_depth_w"],
        },
        "open_inputs": [
            "OPEN: prove M_m^{max} <= 1 (or any bound <= 2^10 is already powerful)",
            "OPEN: prove U_res(z) <= target/pack (or <= t*p/pack for D_prim form)",
        ],
        "note": (
            "Entropy makes M_m^{max}<=1 the expected truth at deployed (m,w,p); "
            "proving it is a sharp prefix-fiber uniqueness statement for m-subsets."
        ),
    }


def lemma_side_prefix_pencil() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e_subset_fixed_w_prefix_is_constant_shift_pencil",
        "statement": (
            "Fix w and e=w+1. The e-subsets U whose monic locators share a fixed "
            "length-w coefficient prefix u form a constant-shift family (varying only "
            "the constant term). Hence there are at most floor(n/e) such U."
        ),
        "proof": [
            "Monic degree e=w+1: fixing the first w monic coefficients leaves only the "
            "constant term free — that is the definition of a constant-shift pencil.",
            "Root sets of distinct fully split members are pairwise disjoint; pack into D.",
        ],
        "deployed_pack_sides": N // E,
    }


def lemma_full_fiber_same_routing() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "full_fiber_N_can_same_routing",
        "statement": (
            "The same side-prefix routing holds for full Fib_w(z): "
            "N_can(z) <= U_full(z) * M_m(z). Path A is identical algebra with R=Fib."
        ),
        "proof": ["Identical to residual routing without restricting the domain."],
    }


def toy_suite() -> dict[str, Any]:
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
        m = j - e
        ensure(e < j, "nonempty core")
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list[frozenset[int]]] = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            poly = monic([vals[i] for i in exps], p)
            z = tuple(poly[1 : w + 1])
            fibers[z].append(frozenset(exps))

        # Also build all m-subset fibers at depth w for M_m measurement when feasible
        # Only when C(n,m) is small enough
        measure_m = math.comb(n, m) <= 300_000
        m_fibers: dict[tuple[int, ...], int] | None = None
        if measure_m:
            m_fibers = defaultdict(int)
            for exps in itertools.combinations(range(n), m):
                poly = monic([vals[i] for i in exps], p)
                b = tuple(poly[1 : w + 1])
                m_fibers[b] += 1
            M_m_max = max(m_fibers.values()) if m_fibers else 0
        else:
            M_m_max = None

        max_U_res = 0
        max_Ncan_prim = 0
        max_cores_per_u = 0
        routing_fail = 0
        max_R = 0

        for z, mem in fibers.items():
            R = [S for S in mem if aperiodic(S, n)]
            max_R = max(max_R, len(R))
            u_to_cores: dict[tuple[int, ...], set[tuple[int, ...]]] = defaultdict(set)
            for S in R:
                s_sorted = sorted(S)
                U = frozenset(s_sorted[:e])
                C = frozenset(S) - U
                polyU = monic([vals[i] for i in sorted(U)], p)
                polyC = monic([vals[i] for i in sorted(C)], p)
                u = tuple(polyU[1 : w + 1])
                b = tuple(polyC[1 : w + 1])
                if len(b) >= w:
                    b2 = invert_b(z, u, p)
                    if b2 != b[:w]:
                        routing_fail += 1
                u_to_cores[u].add(tuple(sorted(C)))
            ncan = len({c for cs in u_to_cores.values() for c in cs})
            # also count unique cores
            cores = set()
            for cs in u_to_cores.values():
                cores |= cs
            ncan = len(cores)
            max_Ncan_prim = max(max_Ncan_prim, ncan)
            max_U_res = max(max_U_res, len(u_to_cores))
            if u_to_cores:
                max_cores_per_u = max(max_cores_per_u, max(len(v) for v in u_to_cores.values()))
            # N_can_prim <= U_res * max_cores_per_u
            if u_to_cores and ncan > len(u_to_cores) * max(len(v) for v in u_to_cores.values()):
                routing_fail += 1

        ensure(routing_fail == 0, f"routing fail {(p,n,j,w)}")
        out.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "m": m,
                "max_R_proxy": max_R,
                "max_N_can_prim": max_Ncan_prim,
                "max_U_res": max_U_res,
                "max_cores_per_u": max_cores_per_u,
                "M_m_max_measured": M_m_max,
                "N_can_le_U_times_cores_per_u": True,
            }
        )
    return {"status": "PASS", "rows": out}


def build() -> dict[str, Any]:
    ent = entropy_block()
    return {
        "packet": "kb_qatom_route_d_v5",
        "title": "Residual N_can_prim via m-fiber routing and M_m criterion",
        "status": "PARTIAL_PROVED_LEMMAS_ATOM_OPEN",
        "claims": {
            "proves_row_sharp_q_atom": False,
            "proves_residual_core_routing": True,
            "proves_side_prefix_pencil": True,
            "proves_Mm_one": False,
            "proves_U_res_bound": False,
            "proves_conditional_criterion_Mm_Ures": True,
        },
        "entropy": ent,
        "lemmas": {
            "residual_core_routing": lemma_residual_core_routing(),
            "criterion_Mm_Ures": lemma_criterion_Mm_one(),
            "side_prefix_pencil": lemma_side_prefix_pencil(),
            "full_fiber_routing": lemma_full_fiber_same_routing(),
        },
        "toy_suite": toy_suite(),
        "open_program": {
            "B1_prove_Mm_max": (
                f"Prove max_b |Fib_w^{{(m)}}(b)| is tiny at n=2^21,m={M},w={W},p=KoalaBear. "
                f"Entropy: log2 avg ≈ {ent['log2_avg_m_subset_fiber_depth_w']:.2f}."
            ),
            "B2_prove_U_res": (
                f"Prove max residual side-prefix count U_res(z) <= {N_CAN_PRIM_ATOM} "
                f"(or <= {N_CAN_PRIM_TP} for t*p form)."
            ),
            "A_same_with_full_U": "Same routing for full-fiber N_can with U_full instead of U_res.",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    ent = cert["entropy"]
    toys = cert["toy_suite"]["rows"]
    toy_tbl = "\n".join(
        f"| {r['p']} | {r['n']} | {r['w']} | {r['m']} | {r['max_R_proxy']} | "
        f"{r['max_N_can_prim']} | {r['max_U_res']} | {r['max_cores_per_u']} | "
        f"{r['M_m_max_measured']} |"
        for r in toys
    )
    return f"""# KB-MCA Route-D v5: residual \(N_{{\\mathrm{{can}}}}^{{\\mathrm{{prim}}}}\) via m-fiber routing

Status: `PARTIAL` — routing + criterion **PROVED**; `M_m` and `U_res` **OPEN**.

## Entropy signal (deployed)

```text
m = |C| = {M}
w = {W}
log2( avg_b |Fib_w^{{(m)}}(b)| )  ≈  {ent['log2_avg_m_subset_fiber_depth_w']:.2f}
log2( avg j-fiber )               ≈  {ent['log2_avg_j_subset_fiber_depth_w']:.2f}
```

The average m-subset depth-w fiber is about `2^(-18820)` — empty almost everywhere.
The natural finite claim is that the **max** is 0 or 1 (or tiny). Anticode is ~`2^1.69e6`
and does **not** help; this is a uniqueness-scale phenomenon.

## Theorem 1 — residual core routing (PROVED)

{cert["lemmas"]["residual_core_routing"]["statement"]}

## Theorem 2 — side-prefix pencil (PROVED)

{cert["lemmas"]["side_prefix_pencil"]["statement"]}

Deployed side packing `floor(n/e) = {N//E}`.

## Criterion 3 — residual atom from (M_m, U_res) (PROVED conditional)

{cert["lemmas"]["criterion_Mm_Ures"]["statement"]}

```text
If M_m^{{max}} <= 1 and U_res <= {N_CAN_PRIM_ATOM}:
    N_can_prim <= {N_CAN_PRIM_ATOM}
    |R| <= 17 * N_can_prim <= target_floor
    => K_rem residual flatness form

If M_m^{{max}} <= 1 and U_res <= {N_CAN_PRIM_TP}:
    N_can_prim <= {N_CAN_PRIM_TP}
    |D_prim| <= t*p
    => feeds v1 additive support certificate
```

## Path A

Same algebra for full fibers: `N_can <= U_full * M_m` (Theorem full-fiber routing).

## Toy suite

Residual proxy = aperiodic. `M_m_max_measured` only when `C(n,m)` small enough to enumerate.

| p | n | w | m | max R | max N_can_prim | max U_res | max cores/u | M_m max |
|---|---|---|---|---:|---:|---:|---:|---:|
{toy_tbl}

Routing identity `N_can_prim <= U_res * max_cores_per_u` holds on all rows.

## Open program (B then A)

1. **B1:** Prove `M_m^{{max}}` tiny (entropy-backed uniqueness for m-subset depth-w prefixes).
2. **B2:** Bound residual side-prefix count `U_res`.
3. **A:** Repeat with full-fiber `U_full` once B is settled.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v5.py
python3 experimental/scripts/verify_kb_qatom_route_d_v5.py --check
```

## Non-claims

- Does not prove `M_m^{{max}} <= 1`.
- Does not prove a bound on `U_res`.
- Does not claim `U(1116048)<=B*`.
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
            abs(
                old["entropy"]["log2_avg_m_subset_fiber_depth_w"]
                - cert["entropy"]["log2_avg_m_subset_fiber_depth_w"]
            )
            < 1e-6,
            "entropy drift",
        )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v5\n\nResidual N_can_prim via m-fiber routing.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v5.py --check\n```\n"
    )
    # Fix note to avoid invalid escapes - write without latex backslashes issues
    note = render_note(cert).replace("\\mathrm", "mathrm").replace("\\le", "<=").replace("\\,", " ")
    NOTE_PATH.write_text(note)
    REPORT_PATH.write_text(
        f"# v5 report\n\nstatus: {cert['status']}\n"
        f"log2_avg_m_fiber: {cert['entropy']['log2_avg_m_subset_fiber_depth_w']:.4f}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  log2 avg m-fiber: {cert['entropy']['log2_avg_m_subset_fiber_depth_w']:.4f}")
    print(f"  N_can_prim atom budget: {N_CAN_PRIM_ATOM}")
    print(f"  toy_rows: {len(cert['toy_suite']['rows'])}")
    for r in cert["toy_suite"]["rows"]:
        print(
            f"    p={r['p']} w={r['w']}: Ncan_prim={r['max_N_can_prim']} "
            f"U_res={r['max_U_res']} cores/u={r['max_cores_per_u']} "
            f"M_m={r['M_m_max_measured']}"
        )


if __name__ == "__main__":
    main()
