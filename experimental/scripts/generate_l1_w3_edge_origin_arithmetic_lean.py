#!/usr/bin/env python3
"""Generate a Lean checker for the compact W3 edge-origin arithmetic packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_INPUT = (
    "experimental/data/certificates/l1-residual-excess-classifier/"
    "w3_collapse_edge_origin_arithmetic_compact_combo012_sizes10_2_3.json"
)
DEFAULT_OUTPUT = (
    "experimental/lean/l1_threshold_ledger/L1Threshold/"
    "CollapseEdgeOriginArithmetic.lean"
)

KIND_NAMES = {
    0: "StoredKind.always",
    1: "StoredKind.never",
    2: "StoredKind.atShift",
}


def lean_row(row: list[int]) -> str:
    case_index, coset_w, a, b, kind_code, shift, intercept, slope = row
    return (
        "  row "
        f"{case_index} {coset_w} {a} {b} {KIND_NAMES[kind_code]} "
        f"{shift} {intercept} {slope}"
    )


def generate(data: dict) -> str:
    rows = data["rows"]
    row_lines = ",\n".join(lean_row(row) for row in rows)
    case_counts = [0 for _ in range(data["case_count"])]
    for row in rows:
        case_counts[int(row[0])] += 1
    case_counts_lean = ", ".join(str(x) for x in case_counts)
    return f"""namespace L1Threshold

/-!
# W3 collapse-edge origin arithmetic certificate

This generated file checks the compact edge-origin arithmetic packet
`w3_collapse_edge_origin_arithmetic_compact_combo012_sizes10_2_3.json`.

For each stored edge rule it verifies that the stored rule kind agrees with the
modular affine equation

```text
intercept + shift * slope = 0 mod 137.
```

This is still a compact arithmetic-origin certificate, not a symbolic
reconstruction of the W3 geometry and not a global L1 theorem.
-/

namespace CollapseEdgeOriginArithmetic

set_option maxRecDepth 1000000
set_option maxHeartbeats 8000000

inductive StoredKind where
  | always
  | never
  | atShift
deriving Repr, DecidableEq, BEq

structure OriginRow where
  caseIndex : Nat
  cosetW : Nat
  a : Nat
  b : Nat
  kind : StoredKind
  shift : Nat
  intercept : Nat
  slope : Nat
deriving Repr, DecidableEq, BEq

def p : Nat := {data["p"]}

def row (caseIndex cosetW a b : Nat) (kind : StoredKind)
    (shift intercept slope : Nat) : OriginRow :=
  {{
    caseIndex := caseIndex
    cosetW := cosetW
    a := a
    b := b
    kind := kind
    shift := shift
    intercept := intercept
    slope := slope
  }}

def activeAt (r : OriginRow) (t : Nat) : Bool :=
  ((r.intercept + t * r.slope) % p) == 0

def rowKindOK (r : OriginRow) : Bool :=
  match r.kind with
  | StoredKind.always =>
      r.slope == 0 && r.intercept == 0
  | StoredKind.never =>
      r.slope == 0 && r.intercept != 0
  | StoredKind.atShift =>
      r.slope != 0 && r.shift < p && activeAt r r.shift

def rowBoundsOK (r : OriginRow) : Bool :=
  r.caseIndex < {data["case_count"]}
    && r.intercept < p
    && r.slope < p
    && r.shift < p

def rowOK (r : OriginRow) : Bool :=
  rowBoundsOK r && rowKindOK r

def edgeRows : List OriginRow :=
[
{row_lines}
]

def allRowsOK : Bool := edgeRows.all rowOK

def caseRowCounts : List Nat :=
  (List.range {data["case_count"]}).map
    (fun i => (edgeRows.filter (fun r => r.caseIndex == i)).length)

theorem edgeOriginArithmeticAllRowsOK : allRowsOK = true := by
  decide

theorem edgeOriginArithmeticRowCount : edgeRows.length = {len(rows)} := by
  decide

theorem edgeOriginArithmeticCaseCounts : caseRowCounts = [{case_counts_lean}] := by
  decide

#print axioms edgeOriginArithmeticAllRowsOK
#print axioms edgeOriginArithmeticRowCount
#print axioms edgeOriginArithmeticCaseCounts

end CollapseEdgeOriginArithmetic
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
