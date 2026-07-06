# Finite Adjacent Audit Notes

Status: AUDIT / code-and-artifact inspection only. I did not re-run the
frontier verifiers because the task asked for lightweight inspection and no
heavy computations.

## Sources Read

- `experimental/grande_finale.tex`
- `experimental/cap25_cap_v13_raw.tex`, especially:
  - `prop:capg-moved-frontier`
  - `cor:capg-adjacent-pairs`
  - the finite moment/order calibration
  - the final active Q/BC/SP package
- `experimental/data/certificates/frontier-adjacent/{kb_mca,kb_list,m31_mca,m31_list}_v1.packet.json`
- `experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json`
- `experimental/data/certificates/frontier-adjacent/README.md`
- `experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md`
- `experimental/notes/frontier-adjacent/frontier_extension_cell_targets_v1.md`
- verifier scripts:
  - `experimental/scripts/verify_frontier_adjacent_v13_rows.py`
  - `experimental/scripts/verify_frontier_extension_cell_targets.py`
  - `experimental/scripts/verify_koalabear_frontier_adjacent.py`

## Extracted Active Rows

The active finite adjacent pairs are:

| row | target | budget | unsafe `a0` | candidate safe `a0+1` | margin at `a0+1` |
| --- | --- | ---: | ---: | ---: | ---: |
| KoalaBear MCA | `2^-128` | `274980728111395087` | `1116047` | `1116048` | `22.1969` bits |
| KoalaBear list | `2^-128` | `274980728111395087` | `1116046` | `1116047` | `22.0109` bits |
| Mersenne-31 MCA | `2^-100` | `16777215` | `1116023` | `1116024` | `3.2589` bits |
| Mersenne-31 list | `2^-100` | `16777215` | `1116022` | `1116023` | `3.0730` bits |

For the two MCA packet JSONs, the active pairs are in
`v13_raw_moved_pair`, not in the older `agreement_interval.one_step_target`.

## Already Checked by Existing Artifacts

- Exact budgets and row constants are represented in the packet JSONs and
  recomputed by `verify_frontier_adjacent_v13_rows.py`.
- Unsafe lower certificates at `a0` are exact:
  - list rows use identity-prefix list floors directly against `B*`;
  - MCA rows use the quantitative deep-list conversion at the moved pair.
- The lower route fails at `a0+1` in all four rows. This is not a safe proof.
- The full dyadic rung audit reports no frontier-covering firing rung at the
  active `a0+1` values.
- Mersenne-31 MCA has a non-firing tight watch item:
  `Gceil c=2048`, exact mass `12769758` versus `B*=16777215`, margin
  `-0.3938` bit.
- The extension-cell artifact forces the full-extension branch to be
  zero-dimensional and gives exact degree ceilings:
  `4807520`, `4226236`, `9`, `8` in the row order above.

## Open Finite Closure Inputs

- Refresh MCA row packets so every safe-cell table is printed at the active
  moved pair, not only in an addendum.
- Build the quotient image upper ledger; the current rung audit is a lower-floor
  non-inversion audit, not an upper bound.
- Prove finite Q prefix max-fiber constants.
- Prove finite BC split-pencil census constants.
- Prove finite SP primitive shift-pair constants.
- Pay the extension `K=F` branch by a zero-dimensional certificate meeting the
  degree ceilings.
- Pay sparse/plain-CA and list/interleaved residual cells.
- Print a first-match deduplication theorem or certified safe sum before
  forming `U(a0+1)`.

## Overclaiming Risks

- Reading `GREEN` in the rung audit as `U(a0+1) <= B*`.
- Reading lower-route failure at `a0+1` as safety.
- Using the historical MCA packet `agreement_interval` instead of
  `v13_raw_moved_pair`.
- Treating extension-cell targets as a paid extension cell.
- Applying the universal `2^-128` target to Mersenne-31 rows.
