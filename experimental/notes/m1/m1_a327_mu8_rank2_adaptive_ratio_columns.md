# M1 a=327 mu8 Rank-2 Adaptive Ratio Columns

Status: `EXACT_EXTRACTION_NO_A327 / MU8_RANK2_ADAPTIVE_WIDTH_IMPROVES_SUPPORT / PARTIAL / EXPERIMENTAL`.

This remains an `INTERLEAVED_LIST` experiment for `RS[F_17^32,H,256]`.
The denominator is `17^32`, and `mca_counted=false`. This is not an MCA,
protocol, or global list-decoding claim; specifically, this is not an MCA row.

## Purpose

The `14684a5` width-ablation checkpoint showed that menu width matters:
the rank-2 CP-SAT front reached min support `313` and total selected
incidence `2193`, but no support/pair-passing schedule. This branch adds
adaptive ratio-column generation: omitted ratio options are scored against
the current label deficits, pair-cap slack, row cost, and repeated ratio-line
supports below the degree-32 threshold.

## Result

The adaptive scan solved `64` carrier planes with a start width of `8` and
a ratio menu rebuilt up to width `32`. Short-budget width-8 active-set solves
often returned `UNKNOWN`, so the script uses a width-4 seed as an incumbent
and hint source rather than treating `UNKNOWN` as infeasibility.

Best adaptive frontier:

- best min support: `314`
- best selected incidence total: `2202`
- near-front candidates stored: `1`
- support/pair-passing candidates: `0`

The best stored near-front candidate was `rank2_plane_0148_adaptive_seed_w04`.
It has pair cap max `255`, min support `314`, total incidence `2202`, and row
cost `92`.

## Exact Diagnostic

The near-front candidate was audited over `GF(17^32)`.

- matrix shape: `92 x 64`
- rank/nullity: `64 / 0`
- forced global ratio lines: none
- max ratio-line support: `4`
- rank-one collapse risk: false

This diagnostic is not witness-relevant because the candidate does not meet
the support target. It says the nearest adaptive front in this batch was also
interpolation-full-rank.

## Interpretation

This is not a rank-2 route cut. It is a stronger scheduler/frontier
checkpoint:

- Adaptive ratio-column scoring improved the frontier from `313/2193` to
  `314/2202`.
- The remaining gap is `13` on the weakest label and `87` selected
  incidences.
- No support/pair-passing schedule was produced, so no exact witness
  extraction was attempted.
- The one near-front diagnostic was exact full rank, so simply repairing
  support around that local schedule is unlikely to expose nullity without
  changing ratio-line structure.

## Next Step

The next useful move is to make the adaptive loop solver-aware rather than
only option-aware: persist width-4 incumbent choices as CP-SAT hints, cache
exact menus per candidate plane, and target carrier-plane synthesis at the
labels still under-supported in the `314/2202` front.
