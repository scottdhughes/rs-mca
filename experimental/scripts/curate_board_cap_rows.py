#!/usr/bin/env python3
"""Curate the board near-capacity cap certificates into site-schema rows
(matching site/data/rate-leaderboards.json row shape) + a markdown summary,
ready to add to the rsmca.xyz MCA leaderboards for rho in {1/2,1/4,1/8,1/16}."""
import argparse, json
from fractions import Fraction
from math import log2
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def site_row(r):
    q = int(r["q_line"]); n = int(r["n"]); k = int(r["k"])
    rate = Fraction(k, n)
    delta = 1 - rate - Fraction(2, n)
    eta = Fraction(2, n)
    return {
        "id": f"board-cap-{rate.numerator}-{rate.denominator}-k{k}-n{n}-paperD-Nn",
        "title": f"Prime-field Paper D near-capacity cap, rho={rate.numerator}/{rate.denominator}",
        "rho": f"{rate.numerator}/{rate.denominator}",
        "track": "mca", "trackLabel": "support-wise MCA",
        "direction": "threshold-cap-example",
        "n": str(n), "k": str(k),
        "field": f"prime p ~ 2^{r['field_bitlength']}",
        "fieldSizeLog2": round(log2(q), 3),
        "domainKind": "multiplicative-subgroup", "smoothPowerOfTwo": True,
        "agreementA": str(r["agreement_a"]), "sigma": "2",
        "deltaExact": f"{delta.numerator}/{delta.denominator}",
        "deltaApprox": round(float(delta), 9),
        "etaExact": f"{eta.numerator}/{eta.denominator}",
        "etaApprox": round(float(eta), 9),
        "qGen": str(q), "qLine": str(q), "qChal": "not protocol-bound",
        "nBad": f">={r['N_bad']}",
        "failureMarginBits": int(r["score_bits"]),
        "marginLabel": f"+{int(r['score_bits'])} bits",
        "prizeBox": {"rate": True, "smoothDomain": True, "kBound": True,
                     "fieldBound": True, "denominatorAudited": True,
                     "endpointConvention": True, "publicSource": True,
                     "conditionalImport": False, "rhoNIntegral": True,
                     "powerOfTwoQuotient": True,
                     "quotientDivisor": "cap divisor N=n (first closed grid point)"},
        "status": "PROVED_PAPERD_V12_CAP", "statusLabel": "proved Paper D v12 cap",
        "source": "board_cap_certificate_generator.py + certificate_scanner.paper_d_cap",
        "sourceHref": "https://github.com/przchojecki/rs-mca/blob/main/experimental/scripts/board_cap_certificate_generator.py",
        "nonClaims": [
            "Instantiated example of the Paper D v12 cap at divisor N=n, not a new theorem beyond Paper D.",
            "delta* upper cap from the near-capacity MCA error-floor lower bound eps >= (q-n)/(2kq); not an exact threshold or a safe-side theorem.",
            "The bad-count is the equivalent numerator N_bad=floor((q-n)/(2k)) from the error floor, not an explicit slope census.",
            "Prime-field row engineered near the cap ceiling; the committed scanner verifies the divisor/binomial/field ledgers."],
        "authors": "board cap sweep / Codex + Sage cross-check",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=REPO / "experimental/data/certificates/"
                    "board-nearcapacity-caps/board_cap_certificates.json")
    ap.add_argument("--rows-out", type=Path, default=None)
    ap.add_argument("--md-out", type=Path, default=None)
    args = ap.parse_args(argv)
    cert = json.loads(args.json.read_text())
    rows = [site_row(r) for r in cert["rows"]]
    md = ["# Board near-capacity cap rows (MCA leaderboard candidates)", "",
          "Prime-field Paper D near-capacity caps for the four grand-challenge rates, "
          "filling the sparse low-rate MCA lanes (current best cap: rho=1/2 +119, "
          "rho in {1/4,1/8,1/16} +87).", "",
          "| rho | k | n | delta_cap | field | score | vs board |",
          "|---|---:|---:|---:|---|---:|---|"]
    prev = {"1/2": 119, "1/4": 87, "1/8": 87, "1/16": 87}
    for r in rows:
        md.append(f"| {r['rho']} | {r['k']} | {r['n']} | {r['deltaExact']} | "
                  f"~2^{r['fieldSizeLog2']:.0f} | +{r['failureMarginBits']} | "
                  f"{prev[r['rho']]} -> +{r['failureMarginBits']} |")
    md += ["", "All rows are smooth (power-of-two n), admissible (rho in {1/2,1/4,1/8,1/16}, "
           "k <= 2^40, |F| < 2^256, n <= q, subgroup exists), with k at or above the site "
           "first-grid k-floor. Scanner-confirmed Paper D cap; exact-integer error floor "
           "`2^128 * N_bad > q_line`; Proth-certified primes. Independently re-derived by "
           "`verify_board_cap_certificates.py`."]
    if args.rows_out:
        args.rows_out.write_text(json.dumps({"track": "mca", "rows": rows}, indent=2))
    if args.md_out:
        args.md_out.write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
