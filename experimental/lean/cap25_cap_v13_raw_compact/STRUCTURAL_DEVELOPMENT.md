# Structural development of the RS-MCA unsafe side

This note records what the compact CAP25 v13 Lean package is intended to
formalize.  The files live under the module root
`cap25_cap_v13_raw_compact`.

## Files

### `cap25_cap_v13_raw_compact/Floor.lean`

- `RSMCA.RS D K`: Reed-Solomon codewords as evaluation words `D -> F` of
  degree-`< K` polynomials, with the evaluation domain `D` in a base field
  `B` and codewords over an ambient finite field `F`.
- `RSMCA.listSet D K m U`: decoding lists at agreement threshold `m`.
- `RSMCA.identity_floor`: the identity-prefix floor, producing a `B`-valued
  received word whose list has size at least
  `Nat.choose n m / |B|^(m-K)`.

### `cap25_cap_v13_raw_compact/Conversion.lean`

- `RSMCA.emca D K m`: support-wise MCA error at integer agreement threshold
  `m`, expressed as the maximum bad-slope fraction.
- `RSMCA.flexible_pole_conversion`: converts a sufficiently large decoding
  list, together with the simple-pole slope budget, into an MCA lower bound.
- `RSMCA.exists_poly_list` and `RSMCA.emca_ge_of_floor`: bridge the
  identity-prefix floor into the polynomial list consumed by the conversion.

### `cap25_cap_v13_raw_compact/Certificates.lean`

- `list_unsafe_of_floor`, `koalabear_list_unsafe`, and
  `mersenne31_list_unsafe`: list unsafe rows from the identity-prefix floor.
- `koalabear_mca_unsafe` and `mersenne31_mca_unsafe`: MCA unsafe rows from the
  floor plus the simple-pole conversion.

### `cap25_cap_v13_raw_compact/BC.lean`

- `RSMCA.census`: the binomial-moment census used by the split-pencil problem.
- `RSMCA.bc_census_floor` and `RSMCA.bc_boundary_census_floor`: base-field
  census floors showing why the BC residual input must be normalized at the
  base-field scale.

### `cap25_cap_v13_raw_compact/SP.lean`

- `RSMCA.psumF` and `RSMCA.shiftPairColl`: power-sum and shift-pair objects.
- `RSMCA.newton_field`: Newton identity specialized to finite sets.
- `RSMCA.shiftpair_prefix_collision` and `RSMCA.shiftpair_same_prefix`: equal
  power sums force equal locator prefixes under the characteristic hypotheses.

## Scope

This package targets the unconditional unsafe side and structural reductions
around the residual inputs.  It does not prove the final adjacent safe
certificates.  The safe-side frontier remains dependent on exact upper-ledger
work for the residual inputs `Q`, `BC`, and `SP`.

This integration pass did not run a Lake build; it only inspected and organized
the sources.
