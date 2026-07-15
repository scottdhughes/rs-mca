# Statement correspondence

Source: `experimental/notes/l1/l1_e3_law_refuted.md`

Certificate:
`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`

Verifier: `experimental/scripts/verify_l1_e3_law_refuted.py`

The six `Witness` declarations copy the certified spectra and printed derived
invariants. `Witness.regression` recomputes the spectrum-side portions of
verifier gates i--iv: descending order, length, active `K`, `E3`, residual
`T`, pair cap/tightness, violation margin, residual-chart membership,
rank/dimension total, master identity, falsifier signature, and `n=(p-1)/ell`.

`w1_peel_preserves` and `w2_peel_preserves` cover gate v.
`unrealizable_profile_guard` covers the arithmetic boundary of gate vi and
makes the non-realizability warning explicit.
`theoremOne_boundary_regression` records gate vii's printed `E3/T` chart
separation. The two falsifier theorems lock representative tamper directions.

Lean does not reconstruct cosets, level sets, ranks, or spectra from the raw
`Gamma` vectors. Those realizability checks remain in the independent
verifier. Consequently this package is a regression lock for certified
computed inputs, not a proof that arbitrary printed spectra are realizable.
