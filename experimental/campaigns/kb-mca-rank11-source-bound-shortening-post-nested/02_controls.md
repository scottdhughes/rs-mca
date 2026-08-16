# Controls

## Positive controls

1. `A_gamma` is the complete scalar agreement domain and contains the original
   bad witness support.
2. Pair noncontainment is asserted on `A_gamma`, not inferred for an arbitrary
   replacement support.
3. One interpolation pair on `T_10` is used for every prefix.
4. Locator division is polynomial only for codewords and direction
   polynomials; received words are divided coordinatewise off the deleted set.
5. A shortened pair explanation is lifted by multiplication with the locator
   and addition of the interpolation pair.
6. The quotient map on a direction space is injective, hence dimension
   preserving.
7. Slopes are unchanged and no slope is duplicated between families.

## Hostile controls

1. Arbitrary coordinate replacement inside an exact bad support is forbidden.
2. Puncturing without first forcing zero values is not called shortening.
3. Pair noncontainment of only the selected minimizing pair is insufficient;
   the proof uses noncontainment by every codeword pair on the complete domain.
4. The ten quotient families are nested in slope and coordinate data but are
   not summed as disjoint charges.
5. Preserving the three row gaps does not itself pay rank eleven.

## Finite controls

The verifier exhausts the degree-`<2` codewords in a `GF(5)` support-replacement
counterexample, and separately checks the locator quotient/lift bijection for
all degree-`<3` polynomials constrained on two coordinates.
