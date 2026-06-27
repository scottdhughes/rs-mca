# High-agreement promoted notes

These notes split the stable high-agreement material out of `experimental/experiments.tex`.
They are TeX fragments intended to be included from `experimental/experiments.tex` or promoted into Papers B/C.

## Files

- `tangent_staircase.tex`
  Moving-root tangent floor and exact finite-slope support-wise line staircase in the range `3a-2n >= k`.

- `line_ca_projective.tex`
  No-loss CA and projective-slope line ledger in the same high-agreement range.

- `curve_mca_ca.tex`
  Finite-parameter degree-`d` power-curve MCA/CA high-agreement staircase. This is an RS/evaluation-domain statement for the lower construction; protocol-specific curve samplers still need a sampler-to-model theorem.

- `interleaved_uniqueness.tex`
  MDS interleaved-list uniqueness when `2a-n >= k`.

- `current_row_protocol_ledger.tex`
  Conditional high-agreement ledger for the `F_17^32`, `n=512`, `k=256` row. This is a coding numerator ledger, not a deployed protocol theorem.

- `general_threshold_compiler.tex`
  Row-independent high-agreement threshold compiler and prize-rate applicability discussion.

## Integration note

The patch `promote_high_agreement_notes.patch` replaces the bulky high-agreement sections of `experiments.tex` with `\input{notes/high_agreement/...}` calls and fixes the missing backslash in the following `Towards-Prize` section header.

## Caveats

- Line, projective-line, CA, and interleaved uniqueness statements are stable in the displayed high-agreement ranges.
- Curve lower constructions use the finite-parameter power-curve/evaluation-domain model. They should not be cited as an arbitrary protocol curve-sampler theorem without a sampler-to-model conversion.
- Protocol statements are conditional ledgers: field denominators, folding/query errors, and actual reductions remain separate.
