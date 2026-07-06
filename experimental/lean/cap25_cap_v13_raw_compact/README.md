# cap25_cap_v13_raw_compact Lean package

This Lean folder is the compact formalization workbench for
`experimental/cap25_cap_v13_raw_compact.tex` and the current CAP25 v13
raw/compact frontier notes.

It is meant to capture the unconditional unsafe-side core and the structural
boundary lemmas around the residual inputs.  It does not claim the final safe
side of the RS-MCA threshold.

## Module map

- `cap25_cap_v13_raw_compact.Main`: arithmetic certificates for the deployed
  identity-scale unsafe edges.
- `cap25_cap_v13_raw_compact.Floor`: Reed-Solomon words, decoding lists, and
  the identity-prefix floor.
- `cap25_cap_v13_raw_compact.Conversion`: support-wise MCA definitions and the
  simple-pole conversion.
- `cap25_cap_v13_raw_compact.Certificates`: deployed list/MCA unsafe rows
  derived from the floor and conversion.
- `cap25_cap_v13_raw_compact.BC`: base-field census floor material for the
  BC residual input.
- `cap25_cap_v13_raw_compact.SP`: shift-pair to prefix-collision structural
  reductions for the SP residual input.

## Status

This integration pass performed a source audit and module-name cleanup only.
No Lake build was run.  A contributor who wants to check the package locally
should run `lake build` from this directory.

The unsafe-side certificates and structural floor/conversion lemmas are the
formalization target here.  The matching safe side remains open and is still
organized around the residual inputs `Q`, `BC`, and `SP` from the CAP25 v13
raw/compact papers.

After changing declarations, update any TeX/Lean correspondence notes manually.
Do not rely on bulk source-scanning tools to fill theorem mappings; each
formalization claim should be compared against the relevant TeX statement.
