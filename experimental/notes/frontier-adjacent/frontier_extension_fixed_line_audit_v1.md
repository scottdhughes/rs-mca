# Fixed-line extension audit: Frobenius and budget corrections

**Status:** COUNTEREXAMPLE / AUDIT.  The fixed-line Frobenius-orbit claim in
`frontier_extension_cell_targets_v1.md` is false as stated, and its number
`4,807,520` is not the direct extension-chart degree ceiling.  This note does
not refute a zero-dimensional extension bound, does not instantiate a deployed
KoalaBear SPI chart, and does not prove a safe row.

## Statements audited

The v1 extension target made two load-bearing assertions for a fixed arbitrary
`F`-valued received line:

1. its genuinely full-field bad slopes form complete Frobenius orbits; and
2. the KoalaBear MCA extension projection must be zero-dimensional with total
   degree at most `4,807,520`.

Both require correction.  The first confuses Galois descent of a base-defined
universal incidence or component orbit with the fiber over one arbitrary
`F`-valued received pair.  The second imports a primitive prefix-fiber
multiplier into a direct slope-numerator cell.

## Exact band-regime counterexample

Let

```text
B = F_7,
F = F_(7^6) = F_7[a]/(a^6+2),
D = F_7^x = {1,2,3,4,5,6} subset B^x,
C = RS[F,D,3],
A = 5,
t = A-k = 2.
```

Thus `C` is a rate-`1/2` Reed--Solomon code on the multiplicative-coset domain
`B^x`, and the example lies in the `t=2` regime, not the excluded minimal-slack
`t=1` boundary.  It is still a toy, not a deployed KoalaBear witness.  Define
the received line

```text
f = (-a,0,0,0,0,1),
g = ( 1,0,0,0,0,0).
```

This pair is genuinely `F`-valued even up to common scaling: the nonzero unit
coordinate of `g` forces any scalar making `g` base-valued to lie in `B`, while
no nonzero base scalar sends `a` into `B`.

At slope `z`,

```text
f+zg = (z-a,0,0,0,0,1).
```

Every five-coordinate support contains at least three of the four middle zero
coordinates.  A polynomial of degree less than three that vanishes at those
three distinct domain points is zero.  Hence a five-support is explainable
only when all its displayed values are zero.  This occurs exactly at `z=a`, on
coordinate indices `{0,1,2,3,4}`, corresponding to domain support
`{1,2,3,4,5}`.  Therefore

```text
Bad(f,g;A=5) = {a}.
```

The witness is not a global codeword (`f+ag=(0,0,0,0,0,1)`).  On the unique
support, neither `f` nor `g` is the restriction of a degree-less-than-three
polynomial: each has at least three zero values but also one nonzero value.
Thus the support is noncontained.  The element `a` has minimal field degree
six, while `a^7` is not bad.  Therefore the full-degree bad-slope count is one,
not a multiple of six, and the fixed-line bad set is not Frobenius stable.

This does **not** refute finiteness or zero-dimensionality: the bad set has one
point.  It refutes only the claimed automatic orbit closure for a fixed
arbitrary received line.  The example has not been passed through the deployed
branch-1--5 first-match owner partition and is not claimed to be a surviving
branch-6 KoalaBear residual.

## What remains true about a base-defined eliminant

If a separately certified envelope is cut out by a nonzero polynomial
`E(Z) in F_p[Z]`, put

```text
g_d = gcd(E, Z^(p^d)-Z),    d in {1,2,3,6}.
```

Then the number of distinct roots of minimal field degree exactly six is

```text
N_6 = deg(g_6)-deg(g_3)-deg(g_2)+deg(g_1).
```

This is ordinary inclusion--exclusion: the two maximal proper subfields are
`F_(p^2)` and `F_(p^3)`, whose intersection is `F_p`.  These roots do form
complete six-element Frobenius orbits.  The conclusion belongs to the
**base-defined root envelope**, not automatically to the actual fixed-line bad
set.  If the first eliminant lies in `F[Z]`, a coefficient norm can produce a
base polynomial, generally with up to a factor-six degree loss and extra
conjugate roots.

Moreover, the degree-two and degree-three roots may be removed from the
extension charge only after their lower-arity cells have exact named payments.
`f1_minimal_field_descent.md` and `ef_galois_stabilizer_descent.md` classify and
route these cases; they do not themselves supply deployed finite charges.
Their present status is therefore `UNPAID_TOWER`, not `PAID_BY_THEOREM`.

## Correct direct KoalaBear budget

After the proved base-slope replacement,

```text
p              = 2,130,706,433,
B_star         = 274,980,728,111,395,087,
U_paid         = 2,602,153,473,
B_rem          = 274,980,725,509,241,614,
U_Q            = null,
U_A            = null.
```

The extension dimension--degree theorem charges a chart directly by

```text
Delta * p^e_Y.
```

It does not multiply or divide this slope count by the average prefix-fiber
size.  The extension charge is a component of the aperiodic numerator `U_A`,
not an additional cell outside it.  The full remaining inequality is

```text
U_Q + U_A <= B_rem.
```

After a certified disjoint decomposition

```text
U_A = U_ext + U_A_other,
```

the component reserve is `B_rem-U_Q-U_A_other`.  Consequently, before
reserving anything for the still-unknown `U_Q` and `U_A_other`, the provisional
all-remainder allocations are

```text
e_Y = 0:  Delta <= 274,980,725,509,241,614,
e_Y = 1:  Delta <= floor(B_rem/p) = 129,056,129,
e_Y >= 2: impossible for positive Delta because p^2 > B_rem.
```

The exact number

```text
4,807,520 = floor(B_rem * p^w / binom(n,j))
```

is `K_rem`, the primitive Q-fin max-fiber multiplier relative to the prefix
average.  It can be adopted as a voluntarily conservative engineering reserve,
but it is not an exact extension degree ceiling without a new bridge theorem.
The actual available extension-component reserve is

```text
B_rem - U_Q - U_A_other,
```

so no final extension allocation can be banked while `U_Q`, the rest of `U_A`,
or the required disjoint decomposition is unknown.

## Deployed chart provenance gate

The stacked #810 manifest still contains

```text
charts = [],
represented_units = 0,
locator_chart_id = UNMAPPED_SPI_CHART,
rank_s = null,
pivot_rows = pivot_cols = [].
```

It also explicitly excludes extension-valued slopes.  The repository therefore
does not presently supply a source-derived deployed branch-6 chart.  Instantiating
`rank_s`, a pivot, first defect, locator patch, field basis, or branch-1--5
complement by hand would invent theorem data.  The required terminal is
`UNPAID_PRIMITIVE` until a source adapter emits those objects.

## Verification

The standard-library verifier exhausts all `7^6=117,649` slopes, checks the
irreducible sextic by Rabin's criterion, validates the witness support and
noncontainment, replays the current KoalaBear integer ledger, binds every source
hash, and runs parser and semantic mutations:

```bash
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --check
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.sage
```

These three commands are the correction packet's acceptance gates.  The
superseded `verify_frontier_extension_cell_targets.py` is source-bound for
provenance but is deliberately non-gating: it still verifies the old ceiling
semantics, and on the current integrated tree its G1--G7 and G9--G10 controls
pass while G8 fails because it references the absent historical path
`experimental/cap25_v13_experimental.tex`.

## Verdict and next action

**RED for the old combined extension target; GREEN for this correction.**

The next implementation must first create a v2 chart-binding contract with:

1. a hash-bound fixed received pair or a genuinely uniform symbolic pair;
2. a pinned `F_(p^6)` modulus and basis;
3. source-derived locator-patch, rank, pivot, first-defect, and earlier-owner
   complement data;
4. a localized eliminant identity or a Weil-restricted projection
   dimension--degree certificate; and
5. separate `UNPAID_TOWER`, actual fixed-line count, and base-eliminant-envelope
   fields.

If no such source chart can be emitted, preserve its equations and retain
`UNPAID_PRIMITIVE`.  Do not restore the fixed-line orbit-divisibility check or
label `K_rem` as an extension ceiling.
