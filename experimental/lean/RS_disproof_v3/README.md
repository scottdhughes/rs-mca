# Paper A Lean Formalization

This package formalizes a substantial part of `tex/RS_disproof_v3.tex`
(Paper A).  The root module is `RS_disproof_v3.lean`; the implementation is
split across:

- `RS_disproof_v3/Main.lean`
- `RS_disproof_v3/ExtensionTower.lean`
- `RS_disproof_v3/ScalarCoset.lean`
- `RS_disproof_v3/Verification.lean`

The package was edited by [Aristotle](https://aristotle.harmonic.fun).

## Formalized

- Restricted sumsets and the quotient locator polynomial.
- The locator decomposition
  `locator A a = X^(k+a) + (-sum A) X^k + R`, with `degree R < k`.
- The support-wise line-MCA predicates `RSagrees`, `badAt`, `badSet`, and
  `epsMca`.
- The no-low-degree explanation step for `x^k`.
- Monotonicity of `epsMca` in the radius.
- The quotient-locator lower bound
  `epsMca >= |ell^wedge Q| / |F|` under the smooth-quotient fiber hypothesis.
- The error-one consequence from a restricted-sumset coverage hypothesis.
- Full-domain specializations for `a = 1`.
- The list-side pigeonhole lower bound, including the distinct-codeword
  injection needed to turn witnessing subsets into distinct RS codewords.
- The density-to-MCA reduction for the cyclotomic-sieve branch, stated with the
  sieve density conclusion as an explicit hypothesis.
- The 2-adic extension-tower criterion.
- The scalar-coset extension-field lift, including the full-density and
  box-density extension-field MCA consequences from base-field restricted-sum
  hypotheses.
- Exact checked records for the small Fermat instances over `F_17` and
  `F_257`, deployed-field DSH ladder side conditions, and the `F_17`
  pigeonhole list-size record, via `native_decide`.

## Still Imported Or Missing

This is still not a complete formalization of every theorem in Paper A.

- Dias da Silva--Hamidoune is not formalized; the relevant restricted-sum
  coverage and density outputs are passed as hypotheses.
- Siegel--Walfisz and the full cyclotomic sieve theorem are not formalized;
  only the reduction from the resulting density statement to MCA is formalized.
- The Fermat digit lemma is not formalized as a general theorem.  The small
  Fermat coverage records included here are checked by exact computation.
- The extension-field smooth-tower consequences are formalized from abstract
  basis and restricted-sum hypotheses; the full finite-field instantiation
  tying those hypotheses to every named tower still depends on the imported
  number-theoretic coverage inputs.

## Verification Note

I did not run `lake build` in this repository during the Codex cleanup pass, to
avoid fetching Mathlib.  Source scans show no `sorry`, `axiom`, or `admit`
tokens outside explanatory comments.  The `Verification` module intentionally
uses `native_decide`, so its checked records rely on Lean's native reduction
path as indicated in the file.
