# Combinatorial-trade champion Lean audit

Audit date: 2026-07-14.

## Formal claims

`MomentToMax/CombTradeChampion.lean` formalizes the proved finite mechanism
from:

- `experimental/notes/thresholds/comb_trade_champion.md`;
- `experimental/notes/thresholds/comb_trade_champion_k5.md`.

It defines the six aggregate invariants
`(W,A,C,B,D,E)` and proves that the ordinary common-shift
weight/first/second-moment signature expands exactly as

`(W, s*A+B, s^2*C+2*s*D+E)`.

A generic mixed-radix theorem proves this encoding injective on any bounded
aggregate row under the cleared separation conditions

- `maxB < s`;
- `2*s*maxD + maxE < s^2`;
- `maxE < 2*s`.

For the four-copy minimal Prouhet gadget, Lean verifies the two trade sides,
the gadget values `|G|=6`, `sum G=18`, and `sumsq G=82`, then proves that
the source threshold `219 < s` implies all three separation inequalities for
`(maxB,maxD,maxE)=(72,108,328)`. Consequently, collision of encoded common-
shift signatures is equivalent to equality of all six aggregates.

The module records the independently computed census rows for `k=2,3,4,5`
and the reported nonuniform `k=5` row. It proves the exact cleared
cross-power comparisons showing the `k=4` row beats each of the other four
reported rows, including the flat and window-max `k=5` rows. This comparison
uses only the integer products `fstar*L1` and block sizes; no floating-point
decimal enters a Lean theorem.

## Axiom result

The aggregate expansion, mixed-radix decoder, threshold compiler, and
source-shaped collision equivalence report only standard Mathlib principles
(`propext`, `Classical.choice`, and `Quot.sound`, as applicable). There
is no `sorryAx`, custom axiom, or proof placeholder.

The tiny Prouhet finite-set checks and the large exact cross-power comparisons
use `native_decide`; their reports therefore additionally include
`Lean.ofReduceBool` and `Lean.trustCompiler`. Independent Python verifiers
recompute the source census rows.

## Correspondence boundary

**PROVED:** exact local-block expansion into six aggregates; the cleared
large-shift collision characterization; the minimal Prouhet trade arithmetic;
the sufficient `s>219` threshold; and exact integer rate comparisons among
the five recorded census rows.

**COMPUTED INPUTS:** `(fstar,L1)` values
`(4,3863)`, `(23,162075)`, `(190,4192627)`,
`(2072,57376057)`, and `(760,171764913)`. Lean treats these as named census
rows and checks every downstream comparison; it does not re-run the
multi-million-key dynamic programs.

**NOT CLAIMED:** that the plateau begins at `s=48`; optimality over any
unlisted or unsearched weight sequence; the memory bound of a particular
Python representation; Fourier-mass trends; the printed decimal rates; a
local-CLT tensor limit; or any global value of the packing supremum. The
reported-row ceiling theorem is deliberately finite and does not turn the
searched-window computation into a universal theorem.

## Verification

- direct module compilation with principal theorem axiom reports: passes;
- package `lake build`: passes (8031 jobs);
- `verify_comb_trade_champion.py`: `RESULT: PASS (34/34)`;
- `verify_comb_trade_champion_k5.py --check`:
  `RESULT: PASS (40/40)` in 571 seconds, peak 1016 MB;
- `verify_comb_trade_champion_k5.py --tamper-selftest`:
  `RESULT: PASS (3/3)`.
