# Lean formalization of the M31 few-shell theorem

## Status

`PROVED` / Lean-certified for the explicit affine-chart statements listed
below.  The package contains no `sorry`, `admit`, or custom axioms.

This formalization targets sections 2--4 of
`experimental/notes/thresholds/cap25_v13_m31_chebyshev_entropy_inverse_shells.md`
from PR #476.  It proves the polynomial-method core, exact Boolean and signed
fixed-profile wrappers, the Chebyshev-prefix rank and kernel calculation, an
end-to-end fixed-weight Boolean prefix-fiber cap in exchange-shell language,
the one-shell cap, the deployed arithmetic, and the mass-aware moment
inequality.

## Toolchain and build

- Lean: `leanprover/lean4:v4.28.0`
- Mathlib: `v4.28.0` at
  `8f9d9cff6bd728b17a24e163c9402775d9e6a365`, matching the toolchain used for
  PR #474
- Build:

  ```text
  cd experimental/lean/m31_few_shell
  lake build
  ```

The package entry point is `M31FewShell.lean`.  Every theorem highlighted below
has a corresponding `#print axioms` command in its module.  The reports contain
only `propext`, `Classical.choice`, and `Quot.sound`; the two closed subtraction
equalities need only `propext`, while the checked strict inequality additionally
uses the same standard logical axioms as Mathlib's arithmetic tactics.

## Statement-to-declaration correspondence

| Source statement | Lean declaration(s) | Scope |
|---|---|---|
| Dimension of degree-at-most-`s` polynomials in `N` variables is `choose (N+s) s` | `M31FewShell.finrank_restrictTotalDegree` | Exact stars-and-bars equivalence and Mathlib monomial basis |
| Diagonal separator evaluations imply linear independence | `M31FewShell.linearIndependent_of_diagonal_eval` | Arbitrary field and finite family |
| Polynomial-method cardinality bound | `M31FewShell.card_le_choose_of_diagonal_eval` | `|F| <= choose (N+s) s` |
| Affine few-inner-product lemma | `M31FewShell.affine_few_inner_products` | Explicit `N`-parameter affine chart; shell factors may be indexed before field reduction |
| Fixed-weight Boolean extension, `p > n` | `M31FewShell.intersectionShells`, `M31FewShell.dot_booleanIndicator`, `M31FewShell.boolean_fixedWeight_affine_few_intersections` | Exact off-diagonal intersection shell set over `ZMod p` |
| Fixed-weight exchange shells | `M31FewShell.exchangeShells`, `M31FewShell.intersectionShell_le_weight`, `M31FewShell.exchangeShells_card_eq_intersectionShells` | Formalizes `e(A,B)=m-|A cap B|` and equality of the exchange/intersection shell counts |
| Signed fixed-profile norm and gap, `p > 2n` | `M31FewShell.SignedProfile`, `M31FewShell.signedProfile_norm`, `M31FewShell.signed_fixedNorm_gap`, `M31FewShell.signedDotShells`, `M31FewShell.signed_fixedProfile_affine_few_inner_products` | Exact integer dot-product shell set; order argument stays over `Z` until the final cast |
| Rank-`(w+1)` polynomial evaluation argument | `M31FewShell.polynomial_prefix_linearIndependent`, `M31FewShell.evaluation_linearIndependent`, `M31FewShell.evalMatrix_rank` | Any independent degree-at-most-`w` polynomial family on distinct points |
| Chebyshev-prefix rank `w+1` | `M31FewShell.chebyshev_linearIndependent`, `M31FewShell.chebyshevEvalMatrix_rank` | Assumes `2 != 0` and `w < n` |
| Prefix fiber-direction dimension `n-w-1` | `M31FewShell.chebyshevMoment_ker_finrank` | Kernel of the Chebyshev moment matrix |
| End-to-end Chebyshev few-shell specialization | `M31FewShell.chebyshevBooleanFiber_fewShell_cap`, `M31FewShell.chebyshevBooleanFiber_atMostShells_cap`, `M31FewShell.chebyshevBooleanFiber_oneShell_cap` | Builds a kernel-basis affine chart for the actual Boolean prefix fiber; proves (3.2), including empty fibers, and simplifies one shell to `n-w` |
| Conditional dimension-rewrite helpers | `M31FewShell.chebyshevPrefix_fewShell_cap_of_affineBound`, `M31FewShell.chebyshevPrefix_oneShell_cap_of_affineBound` | Auxiliary generic-field connectors only; the preceding row is the source-facing end-to-end result |
| Deployed cap, budget comparison, and headroom | `M31FewShell.m31_oneShell_cap_eq`, `M31FewShell.m31_oneShell_cap_lt_budget`, `M31FewShell.m31_oneShell_headroom` | Checks `2029705 < 16777215` and headroom `14747510` |
| Mass-aware `Gamma_l` inequality | `M31FewShell.massMoment_le_of_max`, `M31FewShell.fewShell_mass_bound` | Exact abstract probability-mass form of section 4 |

## Affine-chart formulation

The source phrases section 2 using an affine subspace `a + K` of dimension
`N`.  `affine_few_inner_products` quantifies instead over the concrete data the
proof consumes: parameters `u : F -> K^N` and ambient-coordinate polynomials of
total degree at most one whose evaluations recover every family vector.  A
basis of an `N`-dimensional affine subspace supplies this chart immediately.

This is an explicit, stated narrowing of the interface, not of the
polynomial-method conclusion.  Constructing that chart internally from
Mathlib's `AffineSubspace` API is not formalized in the generic lemma.  The
Chebyshev specialization does construct the needed chart internally: it takes
differences from a member of a nonempty fiber, proves those differences lie in
the moment-matrix kernel, expands them in `Module.finBasis`, and supplies the
resulting affine coordinate polynomials.  Its public wrapper handles an empty
fiber separately.

The separator factors are indexed by the original natural or integer shell
set and then mapped into the field.  Consequently the degree is exactly the
source shell count even if two shell labels have the same modular image.  The
conditions `p > n` and `p > 2n` are used precisely to keep diagonal factors
nonzero.

## Chebyshev-fiber formulation

`chebyshevBooleanFiber_atMostShells_cap` assumes directly that every Boolean
indicator in the indexed family has the same Chebyshev evaluation vector.  It
then combines the exact rank/nullity calculation with the affine Boolean
theorem, and uses `exchangeShells_card_eq_intersectionShells` to state the
answer in the source's exchange-shell language.  Thus an exchange-shell count
at most `s` yields exactly `choose (n-w-1+s) s`; no already-established affine
cardinality bound is assumed.

## Nonclaims

The package does not formalize the concrete Mersenne-31 twin-coset domain, the
triangular change between monomial and Chebyshev fibers, or the asymptotic
`s=o(n)` calculation.  The triangular change is not needed by the end-to-end
theorem because its fiber hypothesis is stated directly in Chebyshev moments.
The rank theorem applies to any `n` distinct field points.  The mass module
takes the pointwise mass cap as a hypothesis rather than packaging its routine
derivation from a fiber-cardinality cap.  It does not claim that unrestricted
deployed fibers have few shells.
