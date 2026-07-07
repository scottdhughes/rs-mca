#!/usr/bin/env python3
"""Generate a Lean checker for compact W3 edge-origin dot-product rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_INPUT = (
    "experimental/data/certificates/l1-residual-excess-classifier/"
    "w3_collapse_edge_origin_dot_compact_combo012_sizes10_2_3.json"
)
DEFAULT_OUTPUT = (
    "experimental/lean/l1_threshold_ledger/L1Threshold/"
    "CollapseEdgeOriginDot.lean"
)


def lean_row(row: list[int]) -> str:
    return "  row " + " ".join(str(x) for x in row)


def generate(data: dict) -> str:
    rows = data["rows"]
    row_lines = ",\n".join(lean_row(row) for row in rows)
    case_counts = [0 for _ in range(data["case_count"])]
    for row in rows:
        case_counts[int(row[0])] += 1
    case_counts_lean = ", ".join(str(x) for x in case_counts)
    return f"""namespace L1Threshold

/-!
# W3 collapse-edge origin dot-product certificate

This generated file checks the compact edge-origin dot-product packet
`w3_collapse_edge_origin_dot_compact_combo012_sizes10_2_3.json`.

For each stored edge row, Lean checks that the supplied intercept and slope are
the dot products

```text
intercept = <v(a)-v(b), quotient_base> mod 137
slope     = <v(a)-v(b), seed_coords>   mod 137
```

This still trusts the supplied endpoint evaluation vectors `v(a),v(b)`; it does
not symbolically reconstruct the W3 basis polynomials.
-/

namespace CollapseEdgeOriginDot

set_option maxRecDepth 1000000
set_option maxHeartbeats 8000000

structure DotRow where
  caseIndex : Nat
  cosetW : Nat
  a : Nat
  b : Nat
  va0 : Nat
  va1 : Nat
  va2 : Nat
  va3 : Nat
  vb0 : Nat
  vb1 : Nat
  vb2 : Nat
  vb3 : Nat
  intercept : Nat
  slope : Nat
deriving Repr, DecidableEq, BEq

def p : Nat := {data["p"]}

def row (caseIndex cosetW a b va0 va1 va2 va3 vb0 vb1 vb2 vb3 intercept slope : Nat) : DotRow :=
  {{
    caseIndex := caseIndex
    cosetW := cosetW
    a := a
    b := b
    va0 := va0
    va1 := va1
    va2 := va2
    va3 := va3
    vb0 := vb0
    vb1 := vb1
    vb2 := vb2
    vb3 := vb3
    intercept := intercept
    slope := slope
  }}

def modSub (a b : Nat) : Nat :=
  (p + a - b) % p

def dot4 (d0 d1 d2 d3 c0 c1 c2 c3 : Nat) : Nat :=
  (d0 * c0 + d1 * c1 + d2 * c2 + d3 * c3) % p

def quotient0 (_caseIndex : Nat) : Nat := 1
def quotient1 (caseIndex : Nat) : Nat :=
  if caseIndex < 3 then 83 else 105
def quotient2 (caseIndex : Nat) : Nat :=
  if caseIndex < 3 then 96 else 38
def quotient3 (_caseIndex : Nat) : Nat := 0

def seed0 (_caseIndex : Nat) : Nat := 80
def seed1 (_caseIndex : Nat) : Nat := 45
def seed2 (_caseIndex : Nat) : Nat := 64
def seed3 (_caseIndex : Nat) : Nat := 1

def diff0 (r : DotRow) : Nat := modSub r.va0 r.vb0
def diff1 (r : DotRow) : Nat := modSub r.va1 r.vb1
def diff2 (r : DotRow) : Nat := modSub r.va2 r.vb2
def diff3 (r : DotRow) : Nat := modSub r.va3 r.vb3

def rowIntercept (r : DotRow) : Nat :=
  dot4 (diff0 r) (diff1 r) (diff2 r) (diff3 r)
    (quotient0 r.caseIndex) (quotient1 r.caseIndex) (quotient2 r.caseIndex) (quotient3 r.caseIndex)

def rowSlope (r : DotRow) : Nat :=
  dot4 (diff0 r) (diff1 r) (diff2 r) (diff3 r)
    (seed0 r.caseIndex) (seed1 r.caseIndex) (seed2 r.caseIndex) (seed3 r.caseIndex)

def rowBoundsOK (r : DotRow) : Bool :=
  r.caseIndex < {data["case_count"]}
    && r.va0 < p && r.va1 < p && r.va2 < p && r.va3 < p
    && r.vb0 < p && r.vb1 < p && r.vb2 < p && r.vb3 < p
    && r.intercept < p && r.slope < p

def rowOK (r : DotRow) : Bool :=
  rowBoundsOK r && rowIntercept r == r.intercept && rowSlope r == r.slope

def edgeRows : List DotRow :=
[
{row_lines}
]

def allRowsOK : Bool := edgeRows.all rowOK

def caseRowCounts : List Nat :=
  (List.range {data["case_count"]}).map
    (fun i => (edgeRows.filter (fun r => r.caseIndex == i)).length)

theorem edgeOriginDotAllRowsOK : allRowsOK = true := by
  decide

theorem edgeOriginDotRowCount : edgeRows.length = {len(rows)} := by
  decide

theorem edgeOriginDotCaseCounts : caseRowCounts = [{case_counts_lean}] := by
  decide

#print axioms edgeOriginDotAllRowsOK
#print axioms edgeOriginDotRowCount
#print axioms edgeOriginDotCaseCounts

end CollapseEdgeOriginDot
end L1Threshold
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate(data))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
