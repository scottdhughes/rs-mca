#!/usr/bin/env python3
"""KB-MCA Route-D v67: master closure board + residual theorem certificate.

Does NOT claim |T|<=H2 or A_SP<=t*p. Certifies what IS closed, the exact
conditional close, and the single remaining soft-B lemma.

Closure status (honest):
  CLOSED chain (combinatorial residual reduction):
    C_unique (v53) -> |H_unt|=|T| stars (v54) -> coll calculus (v57)
    -> Plancherel coll (v58) -> soft-B budget (v64)
  CLOSED analytic tools:
    e=2 |T|<=p<=H2; G Plancherel; incomplete GP |G|; energy; e=3 lab structure
  CONDITIONAL close:
    max_{lambda != 0} |S(lambda)| <= B_* = sqrt(2 H2)
    ==> coll <= 2 H2 ==> |T| <= H2   (at deployed n',e,p,H2)
  OPEN (sole wall on primary path):
    SoftB_Deployed: the max|S| bound above for free-1 monic highs of e-subsets
    of the length-n' GP prefix of mu_n in F_p.

Also re-verifies key packet certificates exist and claims are consistent.

  python3 experimental/scripts/verify_kb_qatom_route_d_v67_closure_board.py --check
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-qatom-route-d-v67"
CERT_PATH = CERT_DIR / "kb_qatom_route_d_v67_closure_board.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_qatom_route_d_CLOSURE.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_qatom_route_d_v67_closure_board.report.md"
)

# Deployed KoalaBear MCA constants (single source for this board)
P = 2**31 - 2**24 + 1
N = 2**21
A_DEP = 1_116_048
J = N - A_DEP
T_ROW = A_DEP - 2**20
Wdeg = T_ROW - 1
E = Wdeg + 1
M_C = J - E
FREE_CORE = M_C - Wdeg
N_PRIME = A_DEP + E
H2 = E * P // (2 * 31 * 30)
FLOOR_NP = N_PRIME // E
B_STAR = math.sqrt(2 * H2)
EP = E * P


def ensure(c: bool, msg: str) -> None:
    if not c:
        raise AssertionError(msg)


def log2_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def incomplete_G_bound(p: int, n: int, t: int) -> float:
    return (t / n) * (math.sqrt(p) + 1.0) + math.sqrt(p) * (1.0 + math.log(n))


# Packet certs required for the board (must exist on this branch)
REQUIRED_PACKETS: list[tuple[str, str]] = [
    ("v51", "kb-qatom-route-d-v51"),
    ("v53", "kb-qatom-route-d-v53"),
    ("v54", "kb-qatom-route-d-v54"),
    ("v57", "kb-qatom-route-d-v57"),
    ("v58", "kb-qatom-route-d-v58"),
    ("v59", "kb-qatom-route-d-v59"),
    ("v64", "kb-qatom-route-d-v64"),
    ("v65", "kb-qatom-route-d-v65"),
    ("v66", "kb-qatom-route-d-v66"),
]


def load_packet(dir_name: str) -> dict[str, Any]:
    # cert filenames vary slightly
    d = ROOT / "experimental" / "data" / "certificates" / dir_name
    ensure(d.is_dir(), f"missing cert dir {dir_name}")
    jsons = list(d.glob("*.json"))
    ensure(len(jsons) >= 1, f"no json in {dir_name}")
    # prefer the main kb_qatom file
    main = [j for j in jsons if "kb_qatom" in j.name]
    path = main[0] if main else jsons[0]
    return json.loads(path.read_text())


def closed_lemmas() -> list[dict[str, Any]]:
    """Machine-readable ledger of CLOSED intermediate theorems."""
    return [
        {
            "id": "C_unique",
            "packet": "v53",
            "status": "CLOSED",
            "statement": (
                "Untyped residual core is the terminal block C_*={n'..n-1}; "
                "N_C=1; |H_unt| <= H_*^{pre}(n',e)."
            ),
        },
        {
            "id": "terminal_star",
            "packet": "v54",
            "status": "CLOSED",
            "statement": (
                "Pure-untyped highs are stars through n'-1; |H_unt|=|T|."
            ),
        },
        {
            "id": "U2e",
            "packet": "v51",
            "status": "CLOSED",
            "statement": (
                "At most one free-1 bipartition of any 2e-set (char != 2)."
            ),
        },
        {
            "id": "e2_T_le_H2",
            "packet": "v48/v50",
            "status": "CLOSED",
            "statement": "For e=2: |T| <= p <= H2 at deployed constants.",
        },
        {
            "id": "terminal_high_injectivity",
            "packet": "v57",
            "status": "CLOSED",
            "statement": (
                "Terminal e-sets have pairwise distinct monic highs; "
                "|T| <= nH <= coll/2."
            ),
        },
        {
            "id": "plancherel_coll",
            "packet": "v58",
            "status": "CLOSED",
            "statement": (
                "sum_h m_h^2 = p^{-(e-1)} sum_lambda |S(lambda)|^2; "
                "if max_{lambda!=0}|S|<=B then coll <= C^2/p^{e-1} + B^2."
            ),
        },
        {
            "id": "G_plancherel",
            "packet": "v59",
            "status": "CLOSED",
            "statement": "max_{a!=0}|G(a)| <= sqrt(p t - t^2) for any t-set.",
        },
        {
            "id": "soft_B_budget",
            "packet": "v64",
            "status": "CLOSED",
            "statement": (
                "If max|S|<=B and B^2 + C^2/p^{e-1} <= 2 H2 then |T|<=H2 "
                "(via coll/2 and v57-v58)."
            ),
        },
        {
            "id": "deployed_Bstar_arithmetic",
            "packet": "v64",
            "status": "CLOSED",
            "statement": (
                "At deployed params, log2(C^2/p^{e-1}) ~ -1.34e6 (negligible), "
                "so B_*=sqrt(2 H2) is a sufficient soft-B threshold."
            ),
        },
        {
            "id": "energy_G4",
            "packet": "v65",
            "status": "CLOSED",
            "statement": "E_+(S) = p^{-1} sum |G|^4; Linf/L2 energy bound.",
        },
        {
            "id": "subgroup_G",
            "packet": "v65",
            "status": "CLOSED",
            "statement": (
                "Full multiplicative subgroup H: |sum_{x in H} psi(a x)| "
                "<= sqrt(p)+1 for a!=0."
            ),
        },
        {
            "id": "incomplete_GP_G",
            "packet": "v66",
            "status": "CLOSED",
            "statement": (
                "Prefix length t of order-n GP: |G_t(a)| <= "
                "(t/n)(sqrt(p)+1) + sqrt(p)(1+ln n) for a!=0."
            ),
        },
        {
            "id": "e3_lab_structure",
            "packet": "v60-v63",
            "status": "CLOSED",
            "statement": (
                "e=3: high formulas, diagonal All=6S+3D2+D3, triple Fourier, "
                "W_inf<=sqrt(pt), Gauss |hatH|=sqrt(p), bilinear f·G form, "
                "CS |All|<=sqrt(sum|f|^2 p t). Envelopes too weak for |S|<=sqrt(C)."
            ),
        },
    ]


def conditional_close() -> dict[str, Any]:
    return {
        "id": "conditional_T_le_H2",
        "status": "CONDITIONAL",
        "hypothesis": "SoftB_Deployed",
        "hypothesis_statement": (
            "Let S(lambda) be the free-1 monic high exponential sum over "
            f"e-subsets of the length-n'={N_PRIME} GP prefix of mu_n in F_p "
            f"(p={P}, e={E}). Then max_{{lambda != 0}} |S(lambda)| <= B_* "
            f"with B_* = sqrt(2 H2) = {B_STAR}."
        ),
        "conclusion": f"|T| <= H2 = {H2} at deployed parameters",
        "proof_chain": [
            "v53 C_unique: |H_unt| = untyped residual high count",
            "v54 star: |H_unt| = |T|",
            "v57: |T| <= coll/2",
            "v58: coll <= C^2/p^{e-1} + B^2 under max|S|<=B",
            "v64: C^2/p^{e-1} negligible; B=B_* => coll <= 2 H2 => |T|<=H2",
        ],
        "does_not_imply": [
            "A_SP <= t*p (needs residual card fully into A_SP pipeline)",
            "U <= B* / full MCA close",
        ],
    }


def open_lemmas() -> list[dict[str, Any]]:
    return [
        {
            "id": "SoftB_Deployed",
            "status": "OPEN",
            "priority": 1,
            "statement": conditional_close()["hypothesis_statement"],
            "blocks": ["conditional_T_le_H2", "primary residual card"],
            "lean_target": "RouteD.SoftBDeployed (Prop; proof future)",
        },
        {
            "id": "R2_pair_budget",
            "status": "OPEN",
            "priority": 2,
            "statement": "|R2| <= e*p alternate residual close (v45-v46 path).",
            "blocks": ["alternate residual card"],
            "lean_target": None,
        },
        {
            "id": "A_SP_le_tp",
            "status": "OPEN",
            "priority": 3,
            "statement": "A_SP <= t*p on deployed MCA (program goal; needs residual).",
            "blocks": ["prize-facing card"],
            "lean_target": None,
        },
    ]


def deployed_block() -> dict[str, Any]:
    log2C = log2_comb(N_PRIME, E)
    log2_term = 2 * log2C - (E - 1) * math.log2(P)
    g_inc = incomplete_G_bound(P, N, N_PRIME)
    g_plan = math.sqrt(P * N_PRIME - N_PRIME**2)
    return {
        "n": N,
        "p": P,
        "A": A_DEP,
        "e": E,
        "n_prime": N_PRIME,
        "free_core": FREE_CORE,
        "floor_n_prime_over_e": FLOOR_NP,
        "H2": H2,
        "e_p": EP,
        "B_star": float(B_STAR),
        "B_star_sq": float(2 * H2),
        "log2_C": float(log2C),
        "log2_C2_over_p_em1": float(log2_term),
        "C2_over_p_em1_negligible": bool(log2_term < -100),
        "incomplete_G_bound": float(g_inc),
        "plancherel_G_bound": float(g_plan),
        "incomplete_over_plancherel": float(g_inc / g_plan),
        "incomplete_G_over_B_star": float(g_inc / B_STAR),
        "n_divides_p_minus_1": bool((P - 1) % N == 0),
        "n_prime_lt_n": bool(N_PRIME < N),
    }


def scan_packets() -> dict[str, Any]:
    rows = []
    for label, dir_name in REQUIRED_PACKETS:
        cert = load_packet(dir_name)
        claims = cert.get("claims", {})
        true_claims = [k for k, v in claims.items() if v is True]
        false_claims = [k for k, v in claims.items() if v is False]
        rows.append(
            {
                "packet": label,
                "dir": dir_name,
                "status": cert.get("status"),
                "title": cert.get("title") or cert.get("packet"),
                "n_claims_true": len(true_claims),
                "n_claims_false": len(false_claims),
                "claims_true": true_claims,
                "claims_false": false_claims,
                "proves_T_le_H2": bool(claims.get("proves_T_le_H2_deployed", False)),
                "proves_A_SP": bool(claims.get("proves_A_SP_le_tp", False)),
            }
        )
        # integrity: no packet may falsely claim full close
        ensure(
            not claims.get("proves_T_le_H2_deployed", False),
            f"{label} falsely claims T<=H2",
        )
        ensure(
            not claims.get("proves_A_SP_le_tp", False),
            f"{label} falsely claims A_SP",
        )
    return {
        "n_packets": len(rows),
        "rows": rows,
        "none_claim_full_close": True,
    }


def lean_roadmap() -> dict[str, Any]:
    return {
        "package": "experimental/lean/route_d_residual/",
        "toolchain": "leanprover/lean4:v4.31.0 (match rs_mca_formalization)",
        "mathlib": "not required for arithmetic ledger; required later for SoftB",
        "phase1_stdlib_now": [
            "Deployed constants as Nat (p,n,e,n',H2)",
            "B_star_sq = 2 * H2 exact Nat inequality certificates",
            "ProofStatus + ClosureNode records",
            "ConditionalClose Prop (SoftB -> T_le_H2) as statement only",
        ],
        "phase2_mathlib_later": [
            "Finite field F_p, mu_n, incomplete GP G-bound",
            "Plancherel on F_p^{e-1}",
            "C_unique / star combinatorics on index sets",
            "SoftB_Deployed proof or certified bound",
        ],
        "policy": (
            "No sorry in phase-1 arithmetic. SoftB remains an open Prop "
            "until proved; do not mark residual CLOSED in Lean until SoftB lands."
        ),
    }


def build() -> dict[str, Any]:
    ensure(FREE_CORE == 846161, "fc")
    ensure(E == 67472, "e")
    ensure(N_PRIME == 1_183_520, "n'")
    ensure(FLOOR_NP == 17, "k")
    ensure(H2 == E * P // (2 * 31 * 30), "H2 formula")
    ensure((P - 1) % N == 0, "n|p-1")

    dep = deployed_block()
    ensure(dep["C2_over_p_em1_negligible"], "term")
    ensure(abs(dep["B_star"] ** 2 - dep["B_star_sq"]) < 1e-3, "B*^2")

    packets = scan_packets()
    closed = closed_lemmas()
    cond = conditional_close()
    opens = open_lemmas()

    board_status = "RESIDUAL_CONDITIONAL_SOFTB_OPEN"
    # honesty flags
    claims = {
        "certifies_closed_intermediate_lemmas": True,
        "certifies_conditional_T_le_H2_from_SoftB": True,
        "certifies_deployed_Bstar_arithmetic": True,
        "certifies_incomplete_G_bound_recorded": True,
        "certifies_packet_integrity_no_false_full_close": True,
        "proves_SoftB_Deployed": False,
        "proves_T_le_H2_deployed": False,
        "proves_A_SP_le_tp": False,
        "ready_for_lean_phase1_arithmetic": True,
        "ready_for_lean_phase2_SoftB": False,
    }

    return {
        "packet": "kb_qatom_route_d_v67_closure_board",
        "title": "Route-D master closure board (conditional residual; SoftB open)",
        "status": board_status,
        "claims": claims,
        "deployed": dep,
        "closed_lemmas": closed,
        "conditional_close": cond,
        "open_lemmas": opens,
        "packet_scan": packets,
        "lean_roadmap": lean_roadmap(),
        "summary": {
            "n_closed": len(closed),
            "n_open": len(opens),
            "primary_open": "SoftB_Deployed",
            "B_star": dep["B_star"],
            "H2": H2,
            "honest_full_residual_closed": False,
            "honest_conditional_path_ready": True,
        },
        "tools": {"python": "closure board + packet JSON scan"},
    }


def render_note(cert: dict[str, Any]) -> str:
    dep = cert["deployed"]
    closed = cert["closed_lemmas"]
    cond = cert["conditional_close"]
    opens = cert["open_lemmas"]
    scan = cert["packet_scan"]
    lean = cert["lean_roadmap"]

    closed_lines = "\n".join(
        f"| `{c['id']}` | {c['packet']} | {c['statement'][:80]}{'…' if len(c['statement'])>80 else ''} |"
        for c in closed
    )
    open_lines = "\n".join(
        f"| `{o['id']}` | P{o['priority']} | {o['statement'][:90]}{'…' if len(o['statement'])>90 else ''} |"
        for o in opens
    )
    pkt_lines = "\n".join(
        f"| {r['packet']} | `{r['status']}` | {r['n_claims_true']} true / {r['n_claims_false']} false |"
        for r in scan["rows"]
    )

    return f"""# KB-MCA Route-D — CLOSURE BOARD (v67)

**Status:** intermediate lemmas **CLOSED**; residual `|T|≤H2` is **CONDITIONAL**
on `SoftB_Deployed` (**OPEN**).  
**Does NOT claim** `|T|≤H2`, `A_SP≤t·p`, or full MCA close.  
Branch: `scott/kb-route-d-T-bound` (local until PR-worthy).

---

## Deployed constants

| symbol | value |
|---|---:|
| p | {dep['p']} |
| n | {dep['n']} |
| e | {dep['e']} |
| n' | {dep['n_prime']} |
| H2 | {dep['H2']} |
| B_\\* = √(2 H2) | **{dep['B_star']:.1f}** |
| log2(C²/p^{{e-1}}) | {dep['log2_C2_over_p_em1']:.1f} |
| incomplete \\|G\\| bound | {dep['incomplete_G_bound']:.1f} |
| Plancherel \\|G\\| | {dep['plancherel_G_bound']:.1f} |

---

## Primary residual chain

```text
H_unt
  --[C_unique v53]--> |H_unt| = untyped terminal
  --[star v54]------> |H_unt| = |T|
  --[v57]-----------> |T| <= coll/2
  --[v58 Plancherel]-> coll <= C^2/p^{{e-1}} + B^2
  --[v64 soft-B]----> B <= B_* => coll <= 2 H2 => |T| <= H2
                              ^
                              |
                     SoftB_Deployed  (OPEN)
```

e=2 is **unconditionally CLOSED** (`|T|≤p≤H2`).

---

## CLOSED lemmas ({len(closed)})

| id | packet | statement |
|---|---|---|
{closed_lines}

---

## CONDITIONAL close

**Hypothesis (`{cond['hypothesis']}`):**  
{cond['hypothesis_statement']}

**Conclusion:** {cond['conclusion']}

**Proof chain:**  
{chr(10).join('- ' + s for s in cond['proof_chain'])}

**Does not imply:** {', '.join(cond['does_not_imply'])}

---

## OPEN ({len(opens)})

| id | pri | statement |
|---|---|---|
{open_lines}

---

## Packet integrity scan

| packet | status | claims |
|---|---|---|
{pkt_lines}

All scanned packets: **no false claim** of `|T|≤H2` or `A_SP≤t·p`.

---

## Path to completion

1. **Prove `SoftB_Deployed`** (analytic / character-sum bound on free-1 highs).  
2. Compose with CLOSED chain ⇒ **certificate of `|T|≤H2`**.  
3. Feed residual card into A_SP pipeline ⇒ program goal (separate).  
4. **Lean phase 1 (now):** arithmetic + status ledger (stdlib).  
5. **Lean phase 2 (after SoftB or in parallel tools):** Mathlib FF + GP sums.

### Lean roadmap

- Package: `{lean['package']}`
- Toolchain: `{lean['toolchain']}`
- Phase 1: {', '.join(lean['phase1_stdlib_now'])}
- Phase 2: {', '.join(lean['phase2_mathlib_later'])}
- Policy: {lean['policy']}

---

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v67_closure_board.py --check
# optional deep re-check of tip packets:
python3 experimental/scripts/verify_kb_qatom_route_d_v66.py --check
python3 experimental/scripts/verify_kb_qatom_route_d_v64.py --check
```

Lean (phase 1):

```bash
cd experimental/lean/route_d_residual && lake build
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
        ensure(
            old["summary"]["honest_full_residual_closed"] is False,
            "must not claim full close",
        )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    NOTE_PATH.write_text(render_note(cert))
    (CERT_DIR / "README.md").write_text(
        "# kb-qatom-route-d-v67 closure board\n\n"
        "Master closure board: CLOSED intermediates + CONDITIONAL residual "
        "on SoftB_Deployed (OPEN). Does not claim |T|<=H2.\n"
    )
    s = cert["summary"]
    REPORT_PATH.write_text(
        f"# v67 closure board report\n\n"
        f"status: {cert['status']}\n"
        f"closed lemmas: {s['n_closed']}\n"
        f"open lemmas: {s['n_open']}\n"
        f"primary open: {s['primary_open']}\n"
        f"full residual closed: {s['honest_full_residual_closed']}\n"
        f"B_*: {s['B_star']}\n"
    )
    print("RESULT: PASS")
    print(f"  status: {cert['status']}")
    print(f"  CLOSED intermediate lemmas: {s['n_closed']}")
    print(f"  CONDITIONAL: SoftB_Deployed => |T|<=H2")
    print(f"  OPEN primary: {s['primary_open']} (B_*={s['B_star']:.1f})")
    print(f"  honest full residual closed: {s['honest_full_residual_closed']}")
    print(f"  packet scan: {cert['packet_scan']['n_packets']} certs, no false full-close")
    print("  Lean phase-1 arithmetic: ready; SoftB not ready")
    print("  NOTE: experimental/notes/thresholds/kb_qatom_route_d_CLOSURE.md")


if __name__ == "__main__":
    main()
