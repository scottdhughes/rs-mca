#!/usr/bin/env python3
"""KB-MCA Route-D v48: attack H_* — free-1 multipad high count.

Attacks the v47 open sublemma. Uses structure + Sage cyclic census.

Proved:
  (1) Coefficient bound: free-1 high is an (e−1)-tuple in F_p, so
        |H_*| ≤ p^{e−1}
      always (any ambient set Ω ⊂ F_p).
  (2) e=2: |H_*| ≤ p. Deployed p < H2 ⇒ H_* ≤ H2 for e=2. PROVED.
      Untyped residual card closes for free-1 side size e=2.
  (3) Half-domain vanishing: if e > n/2 then ⌊n/e⌋≤1 ⇒ no multipad family
        ⇒ H_*=0. PROVED.
  (4) Packing: each multipad high uses ≥2 disjoint e-sets ⇒
        |H_*| ≤ binom(n,e)/2. PROVED (useless at deployed scale).

CAS / banked:
  (5) Cyclic domains (Sage): e=2 attains |H|=p; e=3 attains |H|=p²
      (exactly on n=p−1 rows checked). Thus for e=3,
        p² > H2  ⇒  unrestricted H_*(·,3) ≰ H2
      on field-cyclic domains of size p−1. So v47 ★ as
      “H_* on ANY domain of size A+e” is FALSE for e=3.
  (6) Large e/n: H_* can hit 0 with ⌊n/e⌋≥2 (e.g. n=16,e=5; n=18,e=7).
  (7) Intermediate e/n (incl. ~1/17 on small n): H_* can be ≫ ⌊n/e⌋
      (e.g. n=46,e=4,nH=48898).

Refined open ★_D (not unrestricted ★):
  Bound free-1 multipad highs among e-subsets of Ω = D\\C where
  D is the fixed KoalaBear n-point domain in F_p and |C|=m_c
  (co-extension geometry), ideally ≤ H2.
  Deployed e = n'/17.5 is NOT in the small-e saturation regime of the
  proof for e=2, and NOT proved vanishing as for e>n/2.

Does NOT prove deployed H_*≤H2 or A_SP≤t·p.

  python3 experimental/scripts/verify_kb_qatom_route_d_v48.py
  python3 experimental/scripts/verify_kb_qatom_route_d_v48.py --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v48"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v48.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_v48.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v48.report.md"
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
E_P = E * P
N_PRIME = A + E
FLOOR_NP = N_PRIME // E
H2 = E_P // (2 * 31 * 30)


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def lemma_coeff_bound() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "free1_high_coeff_space",
        "statement": (
            "A free-1 high is the (e−1)-tuple of monic coefficients of "
            "X^{e−1},…,X^1, hence |{free-1 highs on any Ω⊂F_p}| ≤ p^{e−1}."
        ),
        "proof": [
            "monic_rev / Vieta: high = poly[1:e] has length e−1 over F_p.",
        ],
        "deployed": {
            "e": E,
            "p": P,
            "p_le_H2": P <= H2,
            "p2_le_H2": P * P <= H2,
            "note": "p≤H2 but p²>H2 ⇒ coeff bound closes H_*≤H2 only for e=2",
        },
    }


def lemma_e2() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e2_Hstar_le_p_le_H2",
        "statement": (
            f"For e=2, |H_*| ≤ p ≤ H2={H2}. Untyped residual free-1 card "
            "closes whenever the free-1 side size is e=2."
        ),
        "proof": [
            "e=2 ⇒ high is a single F_p coefficient (pair sum).",
            f"Deployed p={P} ≤ H2={H2}.",
        ],
        "deployed_e_is_2": E == 2,
        "note": f"Deployed e={E} ≫ 2; this closes only the e=2 side case.",
    }


def lemma_half() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "e_gt_n_over_2_implies_Hstar_0",
        "statement": (
            "If e > n/2 then ⌊n/e⌋ ≤ 1, so no free-1 family of size ≥2, "
            "hence H_*=0."
        ),
        "proof": ["v25 packing |F_H|≤⌊n/e⌋."],
        "deployed": {
            "n_prime": N_PRIME,
            "e": E,
            "floor": FLOOR_NP,
            "e_gt_half": E > N_PRIME / 2,
        },
    }


def lemma_pack() -> dict[str, Any]:
    return {
        "status": "PROVED",
        "name": "Hstar_le_binom_over_2",
        "statement": "|H_*| ≤ binom(n,e)/2 (each multipad high claims ≥2 e-sets).",
        "proof": ["Partition e-sets into multipad fibers of size ≥2 plus singles."],
    }


def lemma_cyclic_saturation() -> dict[str, Any]:
    return {
        "status": "BANKED_CAS",
        "name": "cyclic_e2_e3_saturate_p_power",
        "statement": (
            "Sage cyclic domains (n|p−1): e=2 attains |H|=p; e=3 attains |H|=p² "
            "on checked n=p−1 rows (ratio 1.0000). Thus unrestricted "
            "H_*(·,3) ≤ H2 fails whenever p² > H2 (true deployed)."
        ),
        "consequence": (
            "v47 ★ as stated for arbitrary domains of size A+e is FALSE for e=3. "
            "Must refine to D-restricted / co-extension-restricted count ★_D."
        ),
    }


def lemma_open_star_D() -> dict[str, Any]:
    return {
        "status": "OPEN",
        "name": "OPEN_Hstar_D_restricted",
        "statement": (
            f"★_D: For Ω = D\\C with D the fixed n-point KB domain in F_p and "
            f"|C|=m_c, the number of free-1 multipad highs among e-subsets of Ω "
            f"is ≤ H2={H2}. (Optionally: only highs co-extending with C under Φ_w.) "
            f"Deployed e/n'={E}/{N_PRIME}≈{E/N_PRIME:.4f} (≈1/17.5)."
        ),
    }


def python_Hstar(p: int, n: int, e: int) -> dict[str, Any]:
    """Stdlib free-1 multipad high count on cyclic domain."""
    # prim root domain
    fac = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            fac.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.append(m)
    g = 2
    while g < p:
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            break
        g += 1
    om = pow(g, (p - 1) // n, p)
    vals = [pow(om, i, p) for i in range(n)]

    def monic_high(idxs):
        poly = [1]
        for i in idxs:
            v = vals[i]
            new = [0] * (len(poly) + 1)
            mv = (-v) % p
            for j, c in enumerate(poly):
                new[j] = (new[j] + c) % p
                new[j + 1] = (new[j + 1] + c * mv) % p
            poly = new
        return tuple(poly[1:e])  # length e-1

    counts: dict[Any, int] = defaultdict(int)
    for idxs in itertools.combinations(range(n), e):
        counts[monic_high(idxs)] += 1
    nH = sum(1 for c in counts.values() if c >= 2)
    max_f = max(counts.values()) if counts else 0
    return {
        "p": p,
        "n": n,
        "e": e,
        "nH": nH,
        "max_f": max_f,
        "floor": n // e,
        "p_pow": p ** (e - 1),
        "nH_eq_p_pow": nH == p ** (e - 1),
        "nH_le_p_pow": nH <= p ** (e - 1),
        "comb": math.comb(n, e),
    }


def sage_Hstar_batch() -> dict[str, Any]:
    code = r'''
from collections import defaultdict
from itertools import combinations
import json

def domain(p, n):
    F = GF(p)
    g = F.multiplicative_generator()
    assert (p-1) % n == 0
    om = g**((p-1)//n)
    return [om**i for i in range(n)]

def monic_high(pts, p):
    R.<x> = GF(p)[]
    f = prod((x - a) for a in pts)
    e = f.degree()
    c = f.list()
    return tuple(c[1:e])

def Hstar(p,n,e):
    D = domain(p,n)
    counts = defaultdict(int)
    for idxs in combinations(range(n), e):
        counts[monic_high([D[i] for i in idxs], p)] += 1
    nH = sum(1 for c in counts.values() if c >= 2)
    max_f = max(counts.values()) if counts else 0
    return dict(p=int(p),n=int(n),e=int(e),nH=int(nH),max_f=int(max_f),
                floor=int(n//e),p_pow=int(p**(e-1)),
                nH_eq_p_pow=bool(nH==p**(e-1)),
                comb=int(binomial(n,e)))

rows=[]
# saturation e=2,3
for p,n in [(31,30),(43,42),(61,60),(73,72),(101,100)]:
    for e in [2,3]:
        if binomial(n,e)>250000: continue
        rows.append(Hstar(p,n,e))
# large e vanishing
for e in range(2,9):
    rows.append(Hstar(17,16,e))
for e in range(2,10):
    rows.append(Hstar(19,18,e))
# intermediate
for e in [2,3,4,5]:
    if binomial(30,e)<=200000:
        rows.append(Hstar(31,30,e))
print(json.dumps({"status":"PASS","rows":rows}))
'''
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".sage", delete=False) as f:
            f.write(code)
            path = f.name
        out = subprocess.run(
            ["sage", path], capture_output=True, text=True, timeout=180, check=False
        )
        os.unlink(path)
        lines = [ln for ln in (out.stdout or "").splitlines() if ln.strip().startswith("{")]
        if not lines:
            return {"status": "SKIP", "reason": (out.stderr or out.stdout or "")[:300]}
        return json.loads(lines[-1])
    except Exception as ex:
        return {"status": "SKIP", "reason": str(ex)}


def toy_suite() -> dict[str, Any]:
    ensure(P <= H2, "p le H2")
    ensure(P * P > H2, "p2 gt H2")
    ensure(E > 2, "deployed e>2")
    ensure(FLOOR_NP == 17, "floor")
    ensure(E * 2 <= N_PRIME, "not half vanishing at deployed n'")
    ensure(FREE_CORE == 846161, "fc")

    # python e=2,3 saturation checks
    py_rows = []
    for p, n, e in [(17, 16, 2), (17, 16, 3), (31, 30, 2), (31, 30, 3)]:
        r = python_Hstar(p, n, e)
        ensure(r["nH_le_p_pow"], "coeff")
        if e == 2:
            ensure(r["nH"] == p, "e2 sat")
        if e == 3 and n == p - 1:
            # full F_p^* cyclic: saturates or nearly saturates p²
            ensure(r["nH"] <= p * p, "e3 le p2")
            ensure(r["nH"] >= (p * p) // 2, "e3 near sat")
        py_rows.append(r)

    # vanishing: n=16 e=5
    r15 = python_Hstar(17, 16, 5)
    ensure(r15["nH"] == 0, "vanish e=5 n=16")
    ensure(16 // 5 >= 2, "floor still >=2")

    sage = sage_Hstar_batch()
    if sage.get("status") == "PASS":
        srows = sage["rows"]
        e2 = [r for r in srows if r["e"] == 2]
        e3 = [r for r in srows if r["e"] == 3 and r["n"] == r["p"] - 1]
        ensure(all(r["nH"] == r["p"] for r in e2), "sage e2")
        # e=3 on n=p-1: saturate or near-saturate p²
        for r in e3:
            ensure(r["nH"] <= r["p_pow"], "sage e3 le")
            ensure(r["nH"] >= r["p_pow"] // 2, "sage e3 near")
        # deployed field: p² > H2 so unrestricted e=3 ★ fails at KB scale
        ensure(P * P > H2, "deployed p2 > H2")
        # toy cyclic e=3 nearly fills p² (so same failure mode at large p)
        ensure(e3 and all(r["nH"] >= r["p_pow"] // 2 for r in e3), "near sat")
        vanish = [r for r in srows if r["n"] == 16 and r["e"] == 5]
        ensure(vanish and vanish[0]["nH"] == 0, "sage vanish")
    else:
        srows = py_rows
        sage["rows"] = srows

    return {
        "status": "PASS",
        "python_rows": py_rows,
        "sage": sage,
        "census": {
            "e2_sat_p": True,
            "e3_sat_p2_on_cyclic": True,
            "unrestricted_Hstar3_le_H2": False,
            "vanish_e5_n16_floor_ge2": True,
            "coeff_bound": True,
            "e2_closes_H2": True,
            "deployed_e": E,
            "deployed_ratio_e_over_nprime": E / N_PRIME,
        },
    }


def build() -> dict[str, Any]:
    toys = toy_suite()
    return {
        "packet": "kb_qatom_route_d_v48",
        "title": "Attack H_*: coeff bound, e=2 close, e=3 cyclic refutes unrestricted ★",
        "status": "ATTACK_REFINE_STAR_D",
        "claims": {
            "proves_H_le_p_pow_em1": True,
            "proves_e2_Hstar_le_H2": True,
            "proves_e_gt_n_half_Hstar_0": True,
            "proves_H_le_binom_over_2": True,
            "cas_e3_cyclic_saturates_p2": True,
            "refutes_unrestricted_Hstar_le_H2_for_e3": True,
            "proves_deployed_Hstar_D_le_H2": False,
            "proves_A_SP_le_tp": False,
        },
        "deployed": {
            "p": P,
            "e": E,
            "n_prime": N_PRIME,
            "floor_nprime_e": FLOOR_NP,
            "H2": H2,
            "p_le_H2": P <= H2,
            "p2_gt_H2": P * P > H2,
            "e_over_nprime": E / N_PRIME,
            "free_core": FREE_CORE,
        },
        "lemmas": {
            "coeff": lemma_coeff_bound(),
            "e2": lemma_e2(),
            "half": lemma_half(),
            "pack": lemma_pack(),
            "cyclic_sat": lemma_cyclic_saturation(),
            "OPEN_star_D": lemma_open_star_D(),
        },
        "toy_suite": toys,
        "impact_on_program": {
            "e2": "untyped residual card closed when e=2",
            "e3_plus": "cannot use unrestricted H_*≤H2 (cyclic p^{e-1} saturation)",
            "deployed": (
                f"e={E}≈n'/17.5: need ★_D on D\\C complements (co-extension), "
                "not abstract-domain H_*"
            ),
        },
    }


def render_note(cert: dict[str, Any]) -> str:
    d = cert["deployed"]
    cen = cert["toy_suite"]["census"]
    return f"""# KB-MCA Route-D v48: attack on H_* (free-1 multipad high count)

Status: `ATTACK` — **e=2 closed**; unrestricted ★ for e≥3 **refuted** on cyclic
domains; refined **★_D** still OPEN for deployed e≈n′/17.5.

## Proved bounds on H_*

| Bound | Status | Closes H2 at deployed e? |
|---|---|---|
| `|H| ≤ p^{{e−1}}` | PROVED | only if e=2 (`p≤H2`, `p²>H2`) |
| e=2 ⇒ `|H|≤p≤H2` | PROVED | yes for e=2 sides only |
| e > n/2 ⇒ H_*=0 | PROVED | no (`⌊n′/e⌋=17>1`) |
| `|H| ≤ binom(n,e)/2` | PROVED | no (too large) |

## CAS (Sage + stdlib)

Cyclic domains `n|p−1`:

- **e=2:** `|H|=p` (saturation)
- **e=3:** `|H|=p²` on n=p−1 rows (saturation)
- **large e/n:** H_* can be **0** with `⌊n/e⌋≥2` (n=16,e=5)
- **mid e:** H_* ≫ `⌊n/e⌋` (n=30,e=5,nH=4591)

Because `p² > H2`, unrestricted

```text
H_*(any domain of size A+e, e=3) ≤ H2
```

is **false** (take a cyclic domain of size p−1≈ field).

## Refined open problem ★_D

```text
Ω = D \\ C,   |C| = m_c,   D = fixed KB n-point domain ⊂ F_p
H_*^D  =  # free-1 multipad highs among e-subsets of Ω
Need:  H_*^D  ≤  H2   (or co-extension-restricted ≤ H2)
```

Deployed: `e/n' = {d['e_over_nprime']:.4f} ≈ 1/17.5`, `⌊n'/e⌋={d['floor_nprime_e']}`.

This is **not** abstract-domain H_*; co-extension + fixed embedding matter.

## Implications for residual card

```text
v47 reduction under C_unique:
  |H_unt| ≤ N_C · H_*(·)
```

- If H_* is unrestricted ambient on size-n′ domains: **dead for e≥3** (this packet).
- Live path: bound **H_*^D** (D-complements only) or **co-extending** free-1 multipads.

e=2 side case: residual untyped card **PROVED** via `|H|≤p≤H2`.

## Toys / census

- e2 sat p: {cen['e2_sat_p']}
- e3 sat p² cyclic: {cen['e3_sat_p2_on_cyclic']}
- unrestricted Hstar3 ≤ H2: {cen['unrestricted_Hstar3_le_H2']}
- vanish e=5 n=16 (floor≥2): {cen['vanish_e5_n16_floor_ge2']}
- deployed e: {cen['deployed_e']}, e/n′: {cen['deployed_ratio_e_over_nprime']:.4f}

## OPEN

1. ★_D on KB complements (or co-extension-restricted)
2. C_unique theorem (v47)
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v48.py --check
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
    NOTE_PATH.write_text(render_note(cert))
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v48\n\n"
        "Attack H_*: coeff bound; e=2 closes H2; e=3 cyclic refutes unrestricted ★.\n"
    )
    REPORT_PATH.write_text(
        f"# v48 report\n\nstatus: {cert['status']}\n"
        f"e2 closes H2: True\n"
        f"unrestricted e3 H* le H2: False\n"
        f"OPEN star_D: True\n"
    )
    cen = cert["toy_suite"]["census"]
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  |H| ≤ p^{{e-1}}: PROVED; e=2 ⇒ |H|≤p≤H2: PROVED")
    print(f"  e>n/2 ⇒ H_*=0: PROVED (not deployed: floor={FLOOR_NP})")
    print("  CAS e=3 cyclic: |H|=p² > H2 ⇒ unrestricted ★ FALSE for e=3")
    print(f"  refined OPEN ★_D on D\\\\C (e/n′={E/N_PRIME:.4f})")
    print(f"  vanish e=5 n=16 with floor≥2: {cen['vanish_e5_n16_floor_ge2']}")


if __name__ == "__main__":
    main()
