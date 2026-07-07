#!/usr/bin/env python3
"""Curate the smooth low-rate adjacent-threshold pins as board EXACT-GATE rows
for rho in {1/4,1/8,1/16} -- the low-rate leaderboard lanes currently have no
exact-gate/tangent rows (only rho=1/2 does, e.g. prime-a425-a426-adjacent-gate).
Each pin is an exact adjacent unsafe/safe gate pinning delta* for LD_sw to 1/n.
"""
import argparse, json
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PINS = REPO / "experimental/data/certificates/adjacent-threshold-pins-multirate/adjacent_threshold_pins.json"
# representative smooth low-rate pins (one or two n per low rate)
WANT = {"rho1_4-n2^9-k128", "rho1_4-n2^11-k512",
        "rho1_8-n2^9-k64", "rho1_8-n2^11-k256",
        "rho1_16-n2^10-k64", "rho1_16-n2^12-k256"}


def gate_row(r):
    n, k = int(r["n"]), int(r["k"])
    rate = Fraction(k, n)
    B = int(r["budget_B"])
    return {
        "id": f"prime-adjacent-gate-{rate.numerator}-{rate.denominator}-n{n}-k{k}",
        "title": f"Prime adjacent LD_sw exact gate, rho={rate.numerator}/{rate.denominator}",
        "rho": f"{rate.numerator}/{rate.denominator}",
        "track": "mca", "trackLabel": "support-wise MCA",
        "direction": "exact-gate",
        "n": str(n), "k": str(k),
        "field": f"prime p ~ 2^{r['field_bitlength']}",
        "fieldSizeLog2": round(r["field_bitlength"] - 0.0, 3),
        "domainKind": "multiplicative-subgroup", "smoothPowerOfTwo": True,
        "agreementA": f"{r['A_unsafe']} unsafe / {r['A_safe']} safe",
        "sigma": f"{int(r['A_unsafe'])-k} / {int(r['A_safe'])-k}",
        "deltaExact": r["delta_unsafe"],
        "deltaApprox": round(int(r["delta_unsafe"].split("/")[0]) / n, 9),
        "qGen": str(r["p"]), "qLine": str(r["p"]), "qChal": "not protocol-bound",
        "marginLabel": f"exact {B}/{B+1} gate",
        "failureMarginBits": "exact-gate",
        "prizeBox": {"rate": True, "smoothDomain": True, "kBound": True,
                     "fieldBound": True, "denominatorAudited": True,
                     "endpointConvention": True, "publicSource": True,
                     "conditionalImport": False, "rhoNIntegral": True,
                     "powerOfTwoQuotient": True,
                     "quotientDivisor": "adjacent tangent-exact gate (a425/a426 type)"},
        "status": "PROVED_ADJACENT_THRESHOLD_ROW",
        "statusLabel": "proved adjacent LD_sw exact gate",
        "source": "pin_certificate_generator.py (Proth-certified prime; verify_adjacent_threshold_pins.py)",
        "sourceHref": "https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/certificate_scanner/adjacent_threshold_pins_multirate.md",
        "nonClaims": [
            "Finite-slope support-wise LD_sw exact gate: SAFE at A_safe (high-agreement exact), UNSAFE at A_unsafe (tangent floor); pins delta* for LD_sw to 1/n.",
            "Extends the a425/a426 gate type (previously only rho=1/2) to the low rates; not a new theorem beyond the committed tangent floor + high-agreement exact.",
            "Proth-certified prime field with n | (q-1); the deep (two-core) variant pushes the gate one step further."],
        "authors": "adjacent-threshold pins / Codex + Sage cross-check",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-out", type=Path, default=None)
    args = ap.parse_args(argv)
    pins = json.loads(PINS.read_text())
    rows = [gate_row(r) for r in pins["rows"] if r["id"] in WANT]
    rows.sort(key=lambda x: (int(x["rho"].split("/")[1]), int(x["n"])))
    out = {"track": "mca", "rows": rows}
    if args.rows_out:
        args.rows_out.write_text(json.dumps(out, indent=2))
    for r in rows:
        print(f"  {r['rho']:5} n={r['n']:5} k={r['k']:4} gate: {r['agreementA']}  ({r['marginLabel']})")
    print(f"\n{len(rows)} low-rate exact-gate board rows emitted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
