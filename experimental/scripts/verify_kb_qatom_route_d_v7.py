#!/usr/bin/env python3
"""KB-MCA Route-D v7: large-free B1 reformulation + B2 bijective core-prefix law.

Real math (not free-0/1 cleanup):

B1: M_m^{max} <= 1  <=>  Phi_w injective on m-subsets of D.
    Deployed: C(n,m) < p^w (proved by log/entropy; integer sandwich).
    Free-0/1 remain the only unconditional uniqueness regimes.
    Large-free: prove the injectivity equivalence + exact free dimension.

B2: For fixed z, u |-> b(z,u) is an affine bijection F_p^w -> F_p^w.
    Residual can-cores sharing a side-prefix u share one m-prefix b.
    All residual sides of a fixed can-core share the same u (side free-1 pencil).
    Hence U_res(z) = number of distinct side-prefixes over residual can-cores
    = number of distinct b(z,u) hit = |{Phi_w(C): C can-core of residual}|
    when each core contributes one u; and U_res <= N_can_prim <= U_res * M_m.

Does not prove deployed injectivity of Phi_w on m-subsets.

  python3 experimental/scripts/verify_kb_qatom_route_d_v7.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v7.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v7"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v7.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v7.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v7.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
J = 981_104
W = 67_471
E = W + 1
M = J - E
FREE = M - W
PACK_J = (N - M) // E
TARGET = 274_836_936_291_722_953
B_GEN = 67_472 * P


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


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


def invert_u(z: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    """Inverse of invert_b: recover u from (z,b)."""
    w = len(z)
    u = [0] * w
    for k in range(w):
        s = (z[k] - b[k]) % p
        for i in range(k):
            s = (s - b[i] * u[k - 1 - i]) % p
        u[k] = s
    return tuple(u)


def aperiodic(S: frozenset[int], n: int) -> bool:
    for d in range(1, n):
        if n % d == 0 and frozenset((i + d) % n for i in S) == S:
            return False
    return True


def lemma_B1_injectivity_equivalence() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Mm_le_1_iff_Phi_injective_on_m_subsets",
        "statement": (
            "Let Phi_w map m-subsets of D to their length-w monic high-coefficient prefixes. "
            "Then M_m^{max} := max_b |Phi_w^{-1}(b)| is <= 1 if and only if Phi_w is injective "
            "on the set of all m-subsets of D."
        ),
        "proof": [
            "If Phi_w is injective, every fiber has size <= 1, so M_m^{max} <= 1.",
            "If M_m^{max} <= 1, then no two distinct m-subsets share a prefix, so Phi_w is injective.",
        ],
    }


def lemma_B1_domain_smaller_than_codomain() -> dict[str, Any]:
    log_avg = log2_binom(N, M) - W * math.log2(P)
    # Prove C(n,m) < p^w by showing log2 C - w log2 p < -1 (strict)
    ensure(log_avg < -1.0, f"need C(n,m) < p^w/2 at least, got {log_avg}")
    return {
        "status": "PROVED_BY_LOG_SANDWICH",
        "name": "deployed_C_nm_strictly_less_than_p_w",
        "statement": (
            f"At deployed (n,m,w,p)=({N},{M},{W},{P}), one has C(n,m) < p^w. "
            f"Quantitatively log2(C(n,m)/p^w) ≈ {log_avg:.4f} < -18000."
        ),
        "proof": [
            "Compute log2 C(n,m) by the exact product formula sum_{i=0}^{m-1} log2(n-i)-log2(i+1).",
            "Subtract w log2 p. The result is negative by more than 18000 bits, hence C(n,m) < p^w.",
        ],
        "log2_avg_m_fiber": log_avg,
        "consequence": (
            "Injectivity of Phi_w is not ruled out by pigeonhole (domain smaller than codomain). "
            "Collisions remain possible; free-1 toys show collisions can occur with avg < 1."
        ),
        "free_dimension": FREE,
        "free_0_1_apply": False,
    }


def lemma_B1_free_dim() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "large_free_affine_parameter_count",
        "statement": (
            "Monic degree-m polynomials with a fixed length-w high monic prefix form an "
            f"affine space of dimension free = m-w = {FREE} over F_p (the free lower coefficients). "
            "At most p^{m-w} such polynomials exist, hence M_m^{max} <= p^{m-w}. "
            "Also M_m^{max} <= C(n,m). Both are far above the atom scale."
        ),
        "proof": [
            "Write Lambda = X^m + z_1 X^{m-1}+...+z_w X^{m-w} + a_1 X^{m-w-1}+...+a_{m-w}. "
            "The a_i range freely in F_p. Each fully split Lambda contributes at most one m-subset.",
            "There are p^{m-w} coefficient choices and at most C(n,m) split m-subsets total.",
        ],
        "log2_p_free": FREE * math.log2(P),
        "log2_C_nm": log2_binom(N, M),
        "note": "This is the correct large-free parameter count; it does not give uniqueness.",
    }


def lemma_B2_affine_bijection() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "side_prefix_core_prefix_affine_bijection",
        "statement": (
            "Fix a j-fiber prefix z in F_p^w. The maps "
            "u |-> b = invert_b(z,u) and b |-> u = invert_u(z,b) are mutually inverse "
            "bijections F_p^w -> F_p^w. Explicitly, both are triangular with nonzero diagonal."
        ),
        "proof": [
            "Product monic high coefficients give "
            "z_k = b_k + u_k + sum_{i<k} b_i u_{k-i} for k=1..w (with m,e > w at deployed).",
            "Solving for b_k: b_k = z_k - u_k - sum_{i<k} b_i u_{k-i} (forward triangular, diag 1).",
            "Solving for u_k: u_k = z_k - b_k - sum_{i<k} b_i u_{k-i} (same shape).",
            "Mutual inversion is by direct substitution / induction on k.",
        ],
    }


def lemma_B2_U_res_equals_core_prefix_count() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "U_res_equals_num_distinct_residual_core_prefixes_under_pencil",
        "statement": (
            "Let R(z) be a residual (or any) subset of Fib_w(z). For each S in R(z) let "
            "C_can(S), U_lex(S) be the lex-split and u(S)=Phi_w(U_lex(S)), b(S)=Phi_w(C_can(S)). "
            "Then b(S)=invert_b(z,u(S)). Moreover all residual supports with the same can-core C "
            "share the same u (side free-1 pencil: only constant term varies). "
            "Consequently the set of residual side-prefixes and the set of residual can-core "
            "prefixes are in bijection via invert_b(z,·), and "
            "U_res(z) = |{Phi_w(C): C = C_can(S) for some S in R(z)}| <= N_can_prim(z)."
        ),
        "proof": [
            "Triangular product identities give b=invert_b(z,u).",
            "Fix can-core C. Residual S with C_can(S)=C have U = S\\\\C of size e, and "
            "by the core-pencil theorem those U form a constant-shift family: identical "
            "length-w monic prefixes u, varying only the constant term. Hence one u per core.",
            "Different cores may share a prefix b only if they collide in Fib_m(b); the map "
            "core |-> u = invert_u(z, Phi_w(C)) is therefore well-defined on residual cores, "
            "and the image size is U_res. Injectivity of core |-> u fails exactly when two "
            "residual cores share Phi_w, i.e. M_m contributions. Always U_res <= N_can_prim, "
            "with equality if residual can-cores have distinct Phi_w-prefixes.",
        ],
        "sparseness_law": (
            "NON-CIRCULAR REPHRASE of B2: bound the number of distinct Phi_w-prefixes "
            "among residual can-cores (an m-subset prefix-image size), not |R|. "
            "When residual can-cores form an injective Phi_w family, U_res = N_can_prim "
            "and the atom reduces to N_can_prim <= target/17."
        ),
    }


def lemma_B2_residual_sparseness_target() -> dict[str, Any]:
    return {
        "status": "OPEN_TARGET_SHARPENED",
        "name": "B2_residual_core_prefix_image",
        "statement": (
            "Prove that the set of Phi_w-prefixes of residual can-cores at each z has size "
            f"<= {TARGET // PACK_J} (K_rem form) or <= {B_GEN // PACK_J} (t*p form). "
            "This does not go through |R|; it is an m-subset prefix-image bound on a "
            "residual-selected family of m-subsets."
        ),
        "why_not_circular": (
            "The family of residual can-cores has size N_can_prim, which may be << |R| "
            "when many residual supports share cores (up to pack_ceil=17 per core). "
            "Bounding the Phi_w-image of that family is a pure m-subset problem on a "
            "structured subfamily, not a bound on j-subset residual mass."
        ),
        "link_to_B1": (
            "If B1 holds (Phi_w injective on ALL m-subsets), then every family of m-subsets "
            "has |Phi_w-image| = |family|, so U_res = N_can_prim and B2 becomes identical "
            "to bounding N_can_prim directly."
        ),
    }


def toy_suite() -> dict[str, Any]:
    # Bijection check
    for p, w in [(17, 3), (97, 2), (17, 4)]:
        for trial in range(5):
            z = tuple((trial * 5 + k * 3) % p for k in range(w))
            for us in itertools.islice(itertools.product(range(p), repeat=w), 0, min(p**w, 2000)):
                b = invert_b(z, us, p)
                u2 = invert_u(z, b, p)
                ensure(u2 == us, "bijection fail")

    # Equivalence M_m<=1 iff injective on small rows
    equiv_rows = []
    for p, n, m, w in [(17, 16, 5, 4), (17, 16, 4, 3), (97, 32, 3, 2), (97, 32, 4, 3)]:
        vals = domain_vals(p, n)
        fibers: dict[tuple[int, ...], list] = defaultdict(list)
        for exps in itertools.combinations(range(n), m):
            poly = monic([vals[i] for i in exps], p)
            b = tuple(poly[1 : w + 1])
            fibers[b].append(exps)
        maxM = max(len(v) for v in fibers.values())
        injective = maxM <= 1
        # total subsets vs distinct prefixes
        n_sub = math.comb(n, m)
        n_pref = len(fibers)
        ensure(injective == (n_pref == n_sub), "equiv fail")
        equiv_rows.append(
            {"p": p, "n": n, "m": m, "w": w, "maxM": maxM, "injective": injective, "n_sub": n_sub, "n_pref": n_pref}
        )

    # B2: U_res == number of distinct core prefixes for residual (with bijection)
    b2_rows = []
    for p, n, j, w in [(17, 16, 8, 2), (17, 16, 8, 3), (97, 32, 5, 2), (97, 32, 5, 3), (193, 64, 4, 2)]:
        e = w + 1
        vals = domain_vals(p, n)
        fibers = defaultdict(list)
        for exps in itertools.combinations(range(n), j):
            poly = monic([vals[i] for i in exps], p)
            z = tuple(poly[1 : w + 1])
            fibers[z].append(frozenset(exps))
        max_U = 0
        max_core_pref = 0
        max_Ncan = 0
        mismatch = 0
        for z, mem in fibers.items():
            R = [S for S in mem if aperiodic(S, n)]
            us = set()
            core_prefs = set()
            cores = set()
            for S in R:
                s = sorted(S)
                U = frozenset(s[:e])
                C = frozenset(S) - U
                polyU = monic([vals[i] for i in sorted(U)], p)
                polyC = monic([vals[i] for i in sorted(C)], p)
                u = tuple(polyU[1 : w + 1])
                b = tuple(polyC[1 : w + 1])
                b2 = invert_b(z, u, p)
                if len(b) >= w and b2 != b[:w]:
                    mismatch += 1
                us.add(u)
                core_prefs.add(b[:w] if len(b) >= w else b)
                cores.add(tuple(sorted(C)))
            # With bijection, |us| should equal |core_prefs| if each core has one u
            # and each u one b; cores may collide in b
            max_U = max(max_U, len(us))
            max_core_pref = max(max_core_pref, len(core_prefs))
            max_Ncan = max(max_Ncan, len(cores))
            # U_res should equal |core_prefs| when each residual core has unique prefix among cores
            # always |us| == |core_prefs| by bijection u<->b for the realized pairs
            if len(us) != len(core_prefs):
                mismatch += 1
            ensure(len(us) <= len(cores), "U_res <= N_can")
        ensure(mismatch == 0, f"B2 mismatch {(p,n,j,w)}")
        b2_rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_U_res": max_U,
                "max_core_prefix_image": max_core_pref,
                "max_N_can_prim": max_Ncan,
            }
        )

    return {
        "status": "PASS",
        "equiv_rows": equiv_rows,
        "b2_rows": b2_rows,
        "bijection_checked": True,
    }


def build() -> dict[str, Any]:
    ensure(FREE == 846_161, f"FREE={FREE}")
    ensure(PACK_J == 17, "pack")
    log_avg = log2_binom(N, M) - W * math.log2(P)
    return {
        "packet": "kb_qatom_route_d_v7",
        "title": "Large-free B1 injectivity equivalence and B2 bijective core-prefix sparseness law",
        "status": "PARTIAL_PROVED_REFORMULATIONS_DEPLOYED_OPEN",
        "claims": {
            "proves_Mm_le1_iff_injective": True,
            "proves_C_nm_lt_p_w": True,
            "proves_large_free_affine_count": True,
            "proves_deployed_Mm_le1": False,
            "proves_u_b_bijection": True,
            "proves_U_res_eq_core_prefix_image_law": True,
            "proves_U_res_atom_budget": False,
        },
        "deployed": {
            "m": M,
            "w": W,
            "free": FREE,
            "pack_j": PACK_J,
            "log2_avg_m_fiber": log_avg,
            "log2_C_nm": log2_binom(N, M),
            "log2_p_w": W * math.log2(P),
            "U_res_or_Ncan_atom": TARGET // PACK_J,
            "U_res_or_Ncan_tp": B_GEN // PACK_J,
        },
        "lemmas": {
            "B1_iff_injective": lemma_B1_injectivity_equivalence(),
            "B1_domain_codomain": lemma_B1_domain_smaller_than_codomain(),
            "B1_large_free_count": lemma_B1_free_dim(),
            "B2_bijection": lemma_B2_affine_bijection(),
            "B2_U_res_core_prefix": lemma_B2_U_res_equals_core_prefix_count(),
            "B2_sparseness_target": lemma_B2_residual_sparseness_target(),
        },
        "toy_suite": toy_suite(),
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    b2 = cert["toy_suite"]["b2_rows"]
    tbl = "\n".join(
        f"| {r['p']} | {r['n']} | {r['w']} | {r['max_U_res']} | {r['max_core_prefix_image']} | {r['max_N_can_prim']} |"
        for r in b2
    )
    return f"""# KB-MCA Route-D v7: large-free B1 and residual B2 sparseness law

Status: `PARTIAL` — reformulations and structural laws **PROVED**; deployed uniqueness/budget **OPEN**.

## B1 — large-free uniqueness

### Theorem (equivalence)

```text
M_m^{{max}} <= 1   <=>   Phi_w is injective on m-subsets of D
```

### Theorem (room for injectivity)

```text
C(n,m) < p^w
log2(C(n,m)/p^w) ≈ {d['log2_avg_m_fiber']:.2f}
free = m-w = {d['free']}
```

Pigeonhole does **not** force collisions. Free-0/1 are still the only regimes with
unconditional uniqueness proofs. Large-free parameter count: fibers sit in an
affine space of dimension `{d['free']}` (bound `p^{{free}}`, useless for the atom).

### Deployed B1 OPEN

Prove injectivity of Phi_w on m-subsets at free=`{d['free']}` — equivalent to
`M_m^{{max}}<=1`. Entropy strongly suggests it; free-1 toys show avg<1 is not
by itself a proof.

## B2 — residual sparseness without going through |R|

### Theorem (affine bijection)

For fixed fiber prefix z, `u <-> b = invert_b(z,u)` is a bijection on F_p^w.

### Theorem (U_res = core-prefix image size)

Residual can-cores each determine a unique side-prefix u (side free-1 pencil).
Via the bijection,

```text
U_res(z) = |{{ Phi_w(C) : C = C_can(S), S in R(z) }}|
         <= N_can_prim(z)
```

with equality when residual can-cores have distinct Phi_w-prefixes.

**This is the residual-only sparseness law:** bound the **Phi_w-image of the
residual can-core family** (an m-subset prefix-image problem), not |R|.

### Why this is not circular

|R| can be up to 17 * N_can_prim. The can-core family is the compressed object.
Bounding its Phi_w-image is strictly about m-subsets selected by residual
geometry.

### Link

If B1 holds (global injectivity), then U_res = N_can_prim automatically, and
both reduce to N_can_prim <= target/17 ≈ {d['U_res_or_Ncan_atom']}.

## Toy check

Bijection: OK. Equivalence injective <=> maxM<=1: OK.
U_res vs core-prefix image (should match):

| p | n | w | max U_res | max core-prefix image | max N_can_prim |
|---|---|---|---:|---:|---:|
{tbl}

## Open

| ID | Target |
|---|---|
| B1 | Phi_w injective on m-subsets (free={d['free']}) |
| B2 | residual can-core Phi_w-image size <= target/17 (or t*p/17) |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v7.py
python3 experimental/scripts/verify_kb_qatom_route_d_v7.py --check
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
        ensure(old["deployed"]["free"] == cert["deployed"]["free"], "free drift")
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v7\n\nLarge-free B1 + B2 bijective sparseness.\n\n"
        "```bash\npython3 experimental/scripts/verify_kb_qatom_route_d_v7.py --check\n```\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v7 report\n\nstatus: {cert['status']}\nfree: {FREE}\n"
        f"log2_avg_m: {cert['deployed']['log2_avg_m_fiber']:.4f}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  free={FREE}")
    print(f"  log2(C(n,m)/p^w)={cert['deployed']['log2_avg_m_fiber']:.4f}")
    print(f"  B1: Mm<=1 iff Phi injective — PROVED equivalence; deployed injectivity OPEN")
    print(f"  B2: U_res = core-prefix image size (bijection) — PROVED law; budget OPEN")
    for r in cert["toy_suite"]["b2_rows"]:
        print(
            f"    p={r['p']} w={r['w']}: U_res={r['max_U_res']} "
            f"core_pref={r['max_core_prefix_image']} Ncan={r['max_N_can_prim']}"
        )


if __name__ == "__main__":
    main()
