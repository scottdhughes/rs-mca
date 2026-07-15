# Subfield Confinement Correspondence

Status: **PROVED** for the support-wise transfer and MCA confinement theorem.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:subfield-confinement-full`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Embed a base-valued received word into the extension | `GrandeFinale.SubfieldConfinement.liftWord` |
| Finite coefficient-vector presentation of the base-domain RS code | `GrandeFinale.SubfieldConfinement.baseDomainRSEval` |
| Identification with the existing polynomial RS submodule | `GrandeFinale.SubfieldConfinement.baseDomainRSEval_eq_rsEval` |
| Base and nonbase coordinate functionals for a nonbase slope | `GrandeFinale.SubfieldConfinement.exists_baseCoordinateFunctionals` |
| Coefficientwise projection preserves RS membership | `GrandeFinale.SubfieldConfinement.baseDomainRSEval_projection` |
| Nonbase explanation forces pair explanation on the same support | `GrandeFinale.SubfieldConfinement.rsEval_explainedPair_of_nonbase` |
| Every MCA-bad slope of a base-valued line lies in the base field | `GrandeFinale.SubfieldConfinement.rsEval_mcaBad_slope_mem_base` |
| Finite bad-slope count is at most the base-field size | `GrandeFinale.SubfieldConfinement.rsEval_mcaBadSlopes_card_le_base` |

## Statement comparison

The inclusion `B subset F` is represented by fields `B`, `F`, and an
`Algebra B F` structure. Membership in the base field is therefore membership
in the range of `algebraMap B F`. The hypothesis `D subset B` is represented
directly by an evaluation map `D -> B`, which is embedded into `F`.

The same-support theorem and individual-slope confinement hold for arbitrary
field extensions; no finiteness or finite-dimensionality assumption is needed.
Finiteness is introduced only for the cardinality corollary. The finite
coefficient-vector code is proved equal to
`CollisionAwarePole.rsEval`, so the exported confinement theorem uses the
package's existing degree-less-than-`k` Reed--Solomon submodule.

## Scope boundaries

The theorem concerns base-valued received lines on base-field evaluation
domains. It does not classify extension-valued lines or assert confinement
when either the received words or evaluation points leave the base field. The
source theorem likewise makes no injectivity assumption on the evaluation
map, and none is added here.

## Verification

```text
lake env lean GrandeFinale/SubfieldConfinement.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
