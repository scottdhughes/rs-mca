# Aristotle Summary: Paper A Formalization

This package is the Paper A Lean formalization for
`tex/RS_disproof_v3.tex`.  The root module is `RS_disproof_v3.lean`, which
imports:

- `RS_disproof_v3.Main`
- `RS_disproof_v3.ExtensionTower`
- `RS_disproof_v3.ScalarCoset`
- `RS_disproof_v3.Verification`

## Main Content

`RS_disproof_v3.Main` formalizes the quotient-locator core:
restricted sumsets, locator polynomials, the locator decomposition,
support-wise line-MCA predicates, monotonicity, the quotient-locator lower
bound, error-one consequences from coverage, full-domain specializations, the
density-to-MCA reduction, and the list lower bound with distinct-codeword
injection.

`RS_disproof_v3.ExtensionTower` formalizes the 2-adic tower criterion used in
the extension-field tower section.

`RS_disproof_v3.ScalarCoset` formalizes the scalar-coset extension-field lift:
coset disjointness, domain cardinality, the basis-box argument, full coverage
of the extension-field restricted sumset from base-field coverage, and the
box-density lower bound.

`RS_disproof_v3.Verification` contains exact `native_decide` checks for the
small Fermat records over `F_17` and `F_257`, deployed-field DSH ladder
arithmetic, and the `F_17` pigeonhole list-size record.

## Scope

The package removes several earlier gaps: the list lower bound now includes
distinctness, the extension-field scalar-coset lift is present, and the small
finite verification records are represented as checked Lean statements.

The remaining imported inputs are exactly the external or broad
number-theoretic pieces that are not being proved here: Dias da
Silva--Hamidoune, Siegel--Walfisz / the full cyclotomic sieve, and the general
Fermat digit lemma.  Some concrete Fermat instances are instead checked by
finite computation in `Verification`.

## Local Check Status

Aristotle reported the new modules as proof-complete with no added axioms.  In
this repository, the Codex cleanup pass did not run `lake build`, because that
would fetch Mathlib.  Treat build-clean status as pending local verification in
an environment with Mathlib available.
