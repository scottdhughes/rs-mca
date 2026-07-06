#!/usr/bin/env python3
"""Board-format curation for the multi-rate adjacent-threshold pins.

Reads adjacent_threshold_pins.json and emits a leaderboard-style markdown table
(same shape as certificate_scanner outputs/leaderboard_sweep_192/site_candidate_rows.md):

  * Table 1 -- the tight LD_sw pins (safe-edge / open-band role). Each row's
    UNSAFE side is an exact bad-lower certificate  2^128*(B+1) > q_line  with
    score = 128 + log2(B+1) - log2(q_line)  (tiny by construction: a tight pin
    sits at the decision boundary).
  * Table 2 -- the complementary committed Paper D universal cap
    delta*_C <= 1 - rho - 2/n  (near-capacity, high margin), computed by
    importing certificate_scanner.paper_d_cap on each engineered prime field.

No new mathematics: this reformats the verified certificates and the committed
scanner's cap ledger into the board's row shape.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from math import log2
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCANNER = REPO / "experimental/notes/certificate_scanner/certificate_scanner.py"
TARGET = 128


def _load_scanner():
    spec = importlib.util.spec_from_file_location("certificate_scanner", SCANNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod   # needed so @dataclass can resolve __module__
    spec.loader.exec_module(mod)
    return mod


def curate(pins: dict, scanner) -> str:
    Row = scanner.Row
    paper_d_cap = scanner.paper_d_cap
    pin_rows, cap_rows = [], []
    for r in pins["rows"]:
        p, n, k = int(r["p"]), int(r["n"]), int(r["k"])
        rho = Fraction(k, n)
        B = int(r["budget_B"])
        bad_lower = B + 1                       # UNSAFE numerator at A_unsafe
        # exact bad-lower certificate and its margin above 2^-128
        assert bad_lower * (1 << TARGET) > p, "pin unsafe inequality must hold"
        score = TARGET + log2(bad_lower) - log2(p)
        pin_rows.append({
            "id": r["id"], "rho": f"{rho.numerator}/{rho.denominator}", "n": n,
            "a_unsafe": int(r["A_unsafe"]), "a_safe": int(r["A_safe"]),
            "delta_unsafe": r["delta_unsafe"], "delta_safe": r["delta_safe"],
            "bad_lower": bad_lower, "qbits": p.bit_length(), "score": score,
        })
        row = Row(n=n, k=k, q_gen=p, q_line=p, q_chal=p, q_base=p, rate=rho)
        cap = paper_d_cap(row, TARGET)
        c = cap.get("closest_to_capacity_cap_max_delta")
        cap_rows.append({
            "id": r["id"], "rho": f"{rho.numerator}/{rho.denominator}", "n": n,
            "status": cap["status"],
            "delta_cap": c["delta_cap_fraction"] if c else "-",
            "margin_bits": c["hyp_margin_bits"] if c else None,
        })
    out = []
    out.append("# Adjacent-threshold pins -- board-format curation")
    out.append("")
    out.append(f"Target `2^-{TARGET}`. {len(pin_rows)} admissible rows "
               "(4 grand-challenge rates x domain sizes + prize-scale k=2^40).")
    out.append("Each pin is Proth-certified and independently verified "
               "(`verify_adjacent_threshold_pins.py`).")
    out.append("")
    out.append("## Table 1 -- LD_sw threshold pins (safe-edge / open-band)")
    out.append("")
    out.append("Two-sided pin of `delta*` for the finite-slope support-wise line object, "
               "to `1/n`. `bad lower = B+1` is the exact UNSAFE numerator; "
               "`score = 128 + log2(bad lower) - log2(q_line)` (tiny by construction -- "
               "a tight pin sits at the boundary).")
    out.append("")
    out.append("| id | rho | n | safe delta | unsafe delta | bad lower | q_line bits | pin score |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for x in pin_rows:
        out.append(f"| `{x['id']}` | {x['rho']} | {x['n']} | {x['delta_safe']} | "
                   f"{x['delta_unsafe']} | {x['bad_lower']} | {x['qbits']} | {x['score']:.4f} |")
    out.append("")
    out.append("## Table 2 -- complementary Paper D near-capacity caps")
    out.append("")
    out.append("Committed universal cap `delta*_C <= 1 - rho - 2/n` on each engineered field "
               "(via `certificate_scanner.paper_d_cap`), where the divisor/binomial/subfield "
               "hypotheses pass.")
    out.append("")
    out.append("| id | rho | n | Paper D cap `delta <= 1-rho-2/N` | hyp margin bits | status |")
    out.append("|---|---:|---:|---:|---:|---|")
    for x in cap_rows:
        mb = "-" if x["margin_bits"] is None else f"{x['margin_bits']:.1f}"
        out.append(f"| `{x['id']}` | {x['rho']} | {x['n']} | {x['delta_cap']} | {mb} | {x['status']} |")
    out.append("")
    out.append("## Notes")
    out.append("")
    out.append("- Pins are tight (margin ~0): they resolve the `LD_sw` line-object threshold "
               "to `1/n`, the board's safe-edge role -- not competitors for the score leaderboard.")
    out.append("- Paper D caps are one-sided near-capacity safe bounds with large margin, a "
               "different object (full MCA) than the pins (`LD_sw` line).")
    out.append("- `NO_ACTIVE_PAPERD_V8_CAP` rows are below the cap's binomial hypothesis at that "
               "field and carry the pin only.")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path,
                    default=REPO / "experimental/data/certificates/"
                    "adjacent-threshold-pins-multirate/adjacent_threshold_pins.json")
    ap.add_argument("--md-out", type=Path, default=None)
    args = ap.parse_args(argv)
    pins = json.loads(args.json.read_text())
    scanner = _load_scanner()
    md = curate(pins, scanner)
    if args.md_out:
        args.md_out.write_text(md)
        print(f"wrote {args.md_out}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
