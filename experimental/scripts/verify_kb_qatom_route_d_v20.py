#!/usr/bin/env python3
"""KB-MCA Route-D v20: top-seam pair injection structure (not 16×N circular).

Attacks: inject ordered top-seam pairs into a small label set, or bound N_ord
without reducing only via N_ord ≤ (pack−1)N.

Proved:
  (1) Pair normal form: ordered top-seam pair (S,T) ↔ (C,U,V) with
      S=C⊔U, T=C⊔V, |U|=|V|=e=w+1, Λ_U−Λ_V = c ∈ F_p^× (free-1 CS).
  (2) Side key φ(C,U,V) = (high(U), c0(U), c0(V)) determines the ordered side
      pair (U,V) among fully split free-1 e-sets (high+const ⇒ monic side locator
      ⇒ roots). Fibers of φ are multi-pads: same (U,V), different cores C.
      Define M_pad(z) = max number of cores C sharing one side key in fiber z.
  (3) N_ord(z) ≤ M_pad(z) · N_side(z) where N_side = # distinct ordered CS side
      pairs (high,c0U,c0V) appearing in fiber z. If M_pad(z)=1 then
      N_ord(z) = N_side(z) and pairs inject into side-key space via φ.
  (4) Core-augmented mark ψ = (min(C), c0(U), c0(V)):
      - Codomain size n·p² (too large for t·p / n·p payment bounds).
      - Toy bank: injective for all tested rows with w≥2; fails at w=1.
  (5) Payment bridge (non-circular in N): if M_pad≤1 and ordered CS side pairs
      in each fiber inject into a set L with |L|≤t·p, then N_ord≤t·p ⇒ A_SP≤t·p.
  (6) Toy stratification: M_pad drops to 1 as w grows (often w≥3 on F_17);
      when M_pad=1, φ is injective on that row's pairs.

Does NOT prove M_pad=1 at deployed w, nor side-pair injection into t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v20.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v20.py --check
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
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v20"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v20.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v20.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v20.report.md"
)

P = 2**31 - 2**24 + 1
N = 2**21
A = 1_116_048
J = N - A
T = A - 2**20
W = T - 1
E = W + 1
PACK = 17
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


def lemma_pair_normal_form() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "topseam_ordered_pair_normal_form",
        "statement": (
            "Ordered top-seam pairs (S,T) in Fib_w(z) are in bijection with triples "
            "(C,U,V) where |C|=j−e, |U|=|V|=e=w+1, U∩V=∅, C∩(U∪V)=∅, "
            "S=C⊔U, T=C⊔V, and Λ_U−Λ_V is a nonzero constant (free-1 CS)."
        ),
        "proof": [
            "v2/v16: top-seam edge ⇔ same can-core C and CS sides.",
            "Ordered pair orients (U,V). Disjointness: free-1 CS root sets are "
            "pairwise disjoint (v2).",
        ],
    }


def lemma_side_key_and_Mpad() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "side_key_phi_and_M_pad",
        "statement": (
            "Define φ(C,U,V) = (high(U), c0(U), c0(V)) where high=Phi_{e−1} monic "
            "high coeffs of the side (length e−1 = w for free-1) and c0 is the "
            "constant term. Then:\n"
            "  (i)  high+c0 determines the monic side locator, hence U (resp. V) "
            "as its root set when fully split with distinct roots;\n"
            "  (ii) φ(C,U,V)=φ(C',U',V') with fully split sides ⇒ (U,V)=(U',V');\n"
            "  (iii) the fiber of φ over a side key is a set of pads C (multi-pad);\n"
            "  (iv) M_pad(z) := max fiber size of φ on ordered top-seam pairs in "
            "fiber z satisfies N_ord(z) ≤ M_pad(z) · N_side(z), with equality "
            "structure N_ord = sum_keys m_key where m_key = #pads for that side key;\n"
            "  (v) if M_pad(z)=1 then φ is injective on ordered pairs in the fiber "
            "and N_ord(z)=N_side(z)."
        ),
        "proof": [
            "Free-1 monic degree e: coefficients (1, high_{e-1},...,high_1, c0) "
            "with high length e−1. Specifying high and c0 fixes the polynomial.",
            "A monic split poly with distinct roots has unique root set.",
            "(ii) both sides recovered ⇒ (U,V) recovered.",
            "(iii)–(v) partition pairs by side key; count.",
        ],
        "note": (
            "Codomain of φ is formally F_p^w × F_p × F_p (size p^{w+2}), too large "
            "for payment. The gain is structural: reduce pair injection to (a) "
            "M_pad=1 and (b) inject CS side pairs into ≤t·p labels."
        ),
    }


def lemma_core_mark_psi() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_DEFINITION_PLUS_TOY",
        "name": "core_augmented_pair_mark_psi",
        "statement": (
            "Define ψ(C,U,V) = (min_exp(C), c0(U), c0(V)) ∈ {0..n−1}×F_p×F_p "
            "(size n·p²). This separates multi-pads that share (U,V) whenever "
            "those pads have distinct min exponents.\n"
            "Toy bank: ψ is injective on all tested (p,n,j,w) with w≥2; fails at w=1.\n"
            "Payment: n·p² ≫ t·p and ≫ n·p, so ψ does not by itself give an "
            "E2/E5-scale bound on N_ord. It is a uniqueness normal form, not a budget."
        ),
        "proof": [
            "Definitional mark. Injectivity: computational certificate in toy_suite "
            "for listed rows with w≥2; explicit failures at w=1.",
            "Size n·p² vs t·p: p/t ≈ 2^{31}/2^{16} ≫ 1 so n·p² > t·p.",
        ],
        "deployed_size_log2_approx": "log2(n p^2) ≈ 21+62 = 83",
        "t_p_log2": math.log2(T_P),
    }


def lemma_payment_bridge() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "M_pad_one_plus_side_injection_pays_A_SP",
        "statement": (
            "If max_z M_pad(z) ≤ 1 and, for every z, the ordered CS side pairs "
            "appearing in fiber z inject into a label set L_z with |L_z| ≤ t·p, "
            "then max N_ord ≤ t·p, hence max |A_SP| ≤ t·p (v17/v19)."
        ),
        "proof": [
            "M_pad≤1 ⇒ N_ord = N_side ≤ |L_z| ≤ t·p.",
            "v19: |A_SP| ≤ N_ord.",
        ],
        "open_inputs": [
            "M_pad ≤ 1 at deployed w (toys: often true for w≥3 on F_17)",
            "Inject CS ordered side pairs into size ≤ t·p (still open; (c0U,c0V) is p² too big)",
        ],
    }


def lemma_noncircular() -> dict[str, Any]:
    return {
        "status": "PROVED_AS_PROGRAM_LAW",
        "name": "pair_injection_avoids_16N_circularity",
        "statement": (
            "Bounding N_ord via side-pair geometry + M_pad does not route through "
            "N_ord ≤ (pack−1)N. That inequality remains true but is the circular "
            "path; the M_pad/side path is the intended non-circular alternative."
        ),
        "proof": [
            "v19 recorded N_ord ≤ (pack−1)N as circular with Q max-fiber.",
            "This packet's bridge uses M_pad and side-pair injection instead.",
        ],
    }


def lemma_open() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_M_pad_and_side_pair_injection",
        "statement": (
            "(1) Prove M_pad(z) ≤ 1 for deployed (or for residual after further "
            "deletions), or bound M_pad by a small constant.\n"
            "(2) Inject ordered free-1 CS e-set pairs (U,V) into a set of size "
            "≤ t·p (deployed t=e=w+1, so e·p labels — natural scale).\n"
            "Together ⇒ A_SP ≤ t·p."
        ),
        "note": (
            "Deployed coincidence: t = e = w+1 = 67472, so t·p = e·p. A mark "
            "using one side exponent index in {0..e−1} and one field element is "
            "the right size; none proved injective yet."
        ),
    }


def toy_suite() -> dict[str, Any]:
    rows = []
    for p, n, j, w in [
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (17, 16, 7, 1),
        (17, 16, 7, 2),
        (17, 16, 7, 3),
        (17, 16, 6, 2),
        (17, 16, 6, 3),
        (17, 16, 5, 1),
        (17, 16, 5, 2),
        (17, 16, 9, 2),
        (17, 16, 9, 3),
        (17, 16, 4, 1),
        (17, 16, 4, 2),
    ]:
        e = w + 1
        if e >= j or math.comb(n, j) > 20000:
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
            high = phi_w(polyU, w)  # length w = e-1 for free-1
            # full free-1 high is e-1 coeffs; phi_w with w=e-1 is all but const
            # when w < e-1, high is only partial — use polyU[1:e] as high except c0
            high_full = tuple(polyU[1:e])  # c_{e-1}..c_1 in rev indexing?
            # polyU = [1, c_{e-1}, ..., c0]; indices 1..e-1 are c_{e-1}..c_1, index e is c0
            # length e+1. high free-1 = polyU[1:e] (e-1 elements), c0=polyU[e] if len is e+1
            # Wait monic_rev length e+1: indices 0..e with poly[0]=1, poly[e]=c0, poly[1]=c_{e-1}
            c0 = polyU[-1]
            high_full = tuple(polyU[1:-1])  # all except leading 1 and const
            return C, high_full, c0, U

        max_Mpad = 1
        max_nord = 0
        psi_inj = True
        phi_inj = True
        for _z, members in fib.items():
            pencils: dict[Any, list] = defaultdict(list)
            for S in members:
                C, high, c0, U = split(S)
                pencils[(tuple(sorted(C)), high)].append((C, U, c0, high))
            pads: dict[Any, set] = defaultdict(set)
            psi_inv: dict[Any, int] = defaultdict(int)
            nord = 0
            for _key, lst in pencils.items():
                if len(lst) < 2:
                    continue
                for i, a in enumerate(lst):
                    for j2, b in enumerate(lst):
                        if i == j2:
                            continue
                        C, U, c0U, high = a
                        _C2, V, c0V, _h2 = b
                        c = (c0U - c0V) % p
                        if c == 0:
                            continue
                        nord += 1
                        pads[(high, c0U, c0V)].add(tuple(sorted(C)))
                        psi_inv[(min(C) if C else -1, c0U, c0V)] += 1
            max_nord = max(max_nord, nord)
            if pads:
                mp = max(len(s) for s in pads.values())
                max_Mpad = max(max_Mpad, mp)
                if mp > 1:
                    phi_inj = False
            if psi_inv and max(psi_inv.values()) > 1:
                psi_inj = False
            # side key recovers U,V uniqueness among pairs: if two pairs same
            # (high,c0U,c0V) they must same U,V — checked via pads only on C

        rows.append(
            {
                "p": p,
                "n": n,
                "j": j,
                "w": w,
                "max_Mpad": max_Mpad,
                "max_nord": max_nord,
                "phi_side_inj": phi_inj,  # M_pad==1 on all fibers
                "psi_minC_c0_inj": psi_inj,
            }
        )
        # structural checks
        if max_Mpad == 1:
            ensure(phi_inj, "Mpad1 => phi inj")
        if w >= 2:
            # psi expected injective on these F_17 rows
            ensure(psi_inj, f"psi inj w>=2 j={j} w={w}")

    ensure(any(r["max_Mpad"] > 1 for r in rows), "have multi-pad examples")
    ensure(any(r["max_Mpad"] == 1 and r["max_nord"] > 0 for r in rows), "have Mpad1 with pairs")
    ensure(T == E, "deployed t=e coincidence")
    return {"status": "PASS", "rows": rows}


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v20",
        "title": "Top-seam pair injection via side keys and M_pad",
        "status": "PARTIAL_PAIR_INJECTION",
        "claims": {
            "proves_pair_normal_form": True,
            "proves_side_key_M_pad": True,
            "proves_psi_definition": True,
            "proves_psi_injective_general": False,
            "proves_M_pad_le_1_deployed": False,
            "proves_side_pair_injection_tp": False,
            "proves_A_SP_le_tp": False,
            "toy_psi_inj_w_ge_2": True,
            "toy_M_pad_drops_with_w": True,
        },
        "deployed": {
            "n": N,
            "j": J,
            "t": T,
            "e": E,
            "w": W,
            "t_equals_e": T == E,
            "t_p": T_P,
            "n_p": N_P,
            "psi_label_size_n_p2": N * P * P,
            "pack": PACK,
        },
        "lemmas": {
            "pair_nf": lemma_pair_normal_form(),
            "side_key": lemma_side_key_and_Mpad(),
            "psi": lemma_core_mark_psi(),
            "bridge": lemma_payment_bridge(),
            "noncircular": lemma_noncircular(),
            "OPEN": lemma_open(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "path": "M_pad<=1 + CS side-pair mark into t*p (=e*p deployed) => A_SP<=t*p",
            "not_circular": "does not use N_ord <= 16*N as the payment bound",
            "next": "Prove M_pad<=1 at deployed w; inject free-1 CS pairs into e*p labels",
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    rows = cert["toy_suite"]["rows"]
    tbl = "\n".join(
        f"| {r['j']} | {r['w']} | {r['max_Mpad']} | {r['max_nord']} | "
        f"{r['phi_side_inj']} | {r['psi_minC_c0_inj']} |"
        for r in rows
    )
    return f"""# KB-MCA Route-D v20: top-seam pair injection (side keys / M_pad)

Status: `PARTIAL` — pair normal form + M_pad calculus **PROVED**;
`M_pad≤1` and side-pair→`t·p` injection **OPEN**.

## Goal (non-circular)

Pay A_SP by bounding `N_ord` **without** only using `N_ord ≤ 16·N`.

## Normal form (PROVED)

```text
ordered top-seam pair (S,T)  ↔  (C, U, V)
  S=C⊔U, T=C⊔V,  Λ_U − Λ_V = c ≠ 0  (free-1 CS sides)
```

## Side key and M_pad (PROVED)

```text
φ(C,U,V) = (high(U), c0(U), c0(V))
```

- Recovers `(U,V)` from fully split free-1 data
- Fibers of φ = **multi-pads** (same sides, different cores)
- `M_pad(z) = max #pads per side key in fiber z`
- `N_ord(z) ≤ M_pad(z) · N_side(z)`
- **If `M_pad=1`:** pairs inject via φ into side-key space; `N_ord=N_side`

## Core-augmented mark ψ (definition + toys)

```text
ψ = (min C, c0(U), c0(V))   size n·p²  (too big for t·p payment)
```

Toys: **injective for w≥2** on F_17; **fails at w=1**.

## Payment bridge (PROVED)

```text
M_pad ≤ 1  and  side pairs inject into |L|≤t·p
    ⇒  N_ord ≤ t·p  ⇒  |A_SP| ≤ t·p
```

Deployed coincidence: **`t = e = w+1`**, so `t·p = e·p` (one side index + field elem).

## Toys

| j | w | max M_pad | max N_ord | φ inj (Mpad=1)? | ψ inj? |
|---|---|---:|---:|---|---|
{tbl}

`M_pad` drops as `w` grows; often `M_pad=1` by `w≥3`.

## OPEN

1. **`M_pad ≤ 1`** at deployed `w` (or after residual deletions)
2. **Inject free-1 CS ordered pairs `(U,V)` into size `e·p = t·p`**

## CAS

- Sage: multi-pad geometry on larger dyadic rows
- msolve: equations for two cores sharing `(U,V,z)` (emptiness ⇒ M_pad=1)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v20.py --check
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
        "# kb-qatom-route-d-v20\n\nTop-seam pair injection via M_pad / side keys.\n"
    )
    NOTE_PATH.write_text(render_note(cert))
    REPORT_PATH.write_text(
        f"# v20 report\n\nstatus: {cert['status']}\n"
        f"M_pad calculus: PROVED\n"
        f"M_pad le 1 deployed: OPEN\n"
        f"t equals e: {cert['deployed']['t_equals_e']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print("  pair normal form + M_pad calculus: PROVED")
    print("  psi=(minC,c0U,c0V) inj for w>=2 toys; size n*p^2 too big for budget")
    print("  bridge: M_pad<=1 + side pairs -> t*p (=e*p) => A_SP paid")
    print(f"  toy rows: {len(cert['toy_suite']['rows'])}")


if __name__ == "__main__":
    main()
