# M1 A4 uniform-atlas route cut v2

**Status:** PROVED ROUTE CUT / ROW OPEN / AUDIT.

This note records one new quantifier route cut and translates one already
proved budget wall at the KoalaBear MCA adjacent agreement

\[
A=1{,}116{,}048.
\]

It does not assign a value to \(U_A\), alter the ledger, prove the row safe, or
improve the public frontier.

## Outcome

Two routes are decided negatively.

1. A chart calculation for one fixed received pair, or any finite sample of
   pairs not backed by an exhaustive reduction theorem, cannot certify the
   row-uniform quantity
   \[
   U_A(A)\ge \sup_{f,g}
   \left|\operatorname{Bad}^{\mathrm{M1}}_{\mathrm{ap}}(f,g;A)\right|.
   \]
2. The existing all-line fixed-deficiency compiler is genuinely uniform, but
   its unrefined charge \(\binom n{d+1}\) cannot fit this row.  This budget
   wall was already proved for the same index in the saturated-BC audit; the
   present packet binds that result and translates it to the
   complete-absorption effective-deficiency language.  The deployed deficiency
   is \(d=913{,}632\), while already
   \[
   \binom n3
   =1{,}537{,}226{,}473{,}786{,}572{,}800
   >274{,}980{,}728{,}111{,}395{,}087=B_*.
   \]

The full A4 idea remains live only if a new theorem supplies a row-uniform
structural refinement: an effective-deficiency/owner collapse, a source-proved
exact root union, or the active base-field-normalized split-pencil census.

## Statement audited

The audited implication chain is

```text
one specialized or sampled (f,g) atlas
    -> a local degree/root charge
    -> U_A for the deployed row
    -> U_paid + U_Q + U_A <= B_star.
```

The first implication to a row-uniform \(U_A\) is invalid without an explicit
all-pairs bridge.  Replacing the local atlas by the current generic
fixed-deficiency envelope repairs the quantifier but fails the exact budget.

## Load-bearing sources

The machine certificate binds the exact SHA-256 digests and statement anchors
for the following sources.

- `experimental/grande_finale.tex`, `def:first-match-ledger` and
  `lem:first-match-ledger`: every received line may have its own first-match
  ledger, but every ledger must obey the same upper bound \(U\) before taking
  the maximum over lines.
- `experimental/cap25_cap_v13_raw.tex`, the first-form aperiodic contract:
  the deployed \(U_A\) bounds a supremum over \((f,g)\).
- The same file, A4: the displayed atlas inclusion and degree sum are written
  for \(\operatorname{Bad}_{\mathrm{ap}}^{\mathrm{M1}}(f,g;A)\); A4 is a
  proposed route, not a theorem providing a uniform maximum.
- The same file, `thm:capf-spi`: the eliminant theorem assumes \(t=j\) and
  explicitly leaves higher-deficiency charts unclassified.
- `tex/cs25_cap_v12.tex`, the scanner-checkable residual ledger: it assumes
  that supplied chart families cover the remaining locators and that every
  chart has the stated eliminant or projection certificate.  Paper D
  explicitly leaves the aperiodic band input open and requires the threshold
  inputs uniformly in the received line.
- `experimental/notes/thresholds/fixed_deficiency_complete_absorption.md`:
  the proved/audit complete-absorption theorem gives the all-field, all-line
  bound \(B_C^{\mathrm{MCA}}(a)\le\binom n{d+1}\) and survives arbitrary
  first-match deletion.
- `experimental/notes/thresholds/kb_mca_1116048_base_slope_universe_v2.md`:
  the current paid baseline is
  \(U_{\mathrm{paid}}=2{,}602{,}153{,}473\), leaving
  \(B_{\mathrm{rem}}=274{,}980{,}725{,}509{,}241{,}614\); both \(U_Q\) and
  \(U_A\) remain null.
- `experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md` and
  its verifier/certificate, contributed by Holm Buar in manually integrated
  PR #383: the saturated-BC audit already proves the coarse budget miss at
  \(\omega-w=913{,}633\).  Here
  \(d+1=\omega-w=913{,}633\), so the coarse miss is inherited rather than a
  new result of this packet.

The later capf layer corroborates the gap rather than repairing it: after the
fixed-line slope-elimination theorem, it explicitly asks for a census “for
every line at band agreements,” and the final active package names the
base-field-normalized split-pencil census as a residual input.

## Lemma 1: fixed-pair promotion is invalid

Let \(\mathcal X\) be the set of admissible residual received pairs and put

\[
B_x=\operatorname{Bad}^{\mathrm{M1}}_{\mathrm{ap}}(x;A)
\qquad(x\in\mathcal X).
\]

Suppose a computation for one fixed pair \(x_0\) proves \(|B_{x_0}|\le D\).
This does not imply \(\sup_x|B_x|\le D\).

### Proof

Take the abstract two-element index set
\(\mathcal X=\{x_0,x_1\}\), put \(D=1\), and define

\[
B_{x_0}=\{0\},\qquad B_{x_1}=\{0,1\}.
\]

Then \(|B_{x_0}|\le D\), but

\[
\sup_{x\in\mathcal X}|B_x|=2>D.
\]

This is a countermodel to the proposed logical implication.  It is not a
Reed--Solomon counterexample.  A finite sample has the same defect unless a
separate theorem proves that the sample is exhaustive.  \(\square\)

### Exact sufficient bridge

A common pair-independent atlas is sufficient, but is not necessary.  The
minimal useful theorem may instead say:

> For every admissible residual pair \(x=(f,g)\), there is a complete
> pair-dependent first-match atlas \(\mathfrak C_x\) covering every remaining
> support and every base- or extension-valued slope, preserving the earlier
> owner complement, such that its safe charge \(U(x)\) satisfies
> \[
> \sup_x U(x)\le U_A^*.
> \]

An exhaustive canonical reduction \(\rho:\mathcal X\to\mathcal T\) to finitely
many types also suffices if the source proves surjectivity of the classification
and one takes \(\max_{\tau\in\mathcal T}U_\tau\).  Within one pair, disjoint
first-match charges may be summed or exact roots unioned.  Across pairs or
canonical types, the operation is a supremum/maximum, never an average and
never a charge from one sample.

This proves the route cut

```text
ROUTE_CUT_FIXED_OR_SAMPLED_PAIR_AS_U_A_CERTIFICATE.
```

It does not cut a pair-dependent symbolic atlas with a proved uniform maximum.

## Lemma 2: the available local theorems do not instantiate the row

For the deployed row,

\[
\begin{aligned}
n&=2{,}097{,}152, & k&=1{,}048{,}576,\\
j=n-A&=981{,}104, & t_{\mathrm{syn}}=A-k&=67{,}472.
\end{aligned}
\]

Thus the exact-agreement syndrome pencil has shape

\[
67{,}472\times981{,}105
\]

and generic kernel dimension at least

\[
j+1-t_{\mathrm{syn}}=913{,}633.
\]

The cited SPI theorem assumes the deficiency-one shape \(t_{\mathrm{syn}}=j\),
so it is not directly applicable.  No higher-deficiency adapter is supplied in
the audited sources.

The separate uniform deep theorem also does not apply.  Its condition is

\[
3(n-A)\le n-k,
\]

whereas here

\[
3(n-A)=2{,}943{,}312>1{,}048{,}576=n-k.
\]

Therefore neither theorem can be imported as the missing deployed \(U_A\).

## Proposition 3: inherited coarse budget wall and exact corollary

The complete-absorption theorem uses the error budget

\[
\tau=n-A=981{,}104
\]

and fixed deficiency

\[
d=n+k-2A=913{,}632.
\]

Its hypotheses hold:

\[
k+1\le A\le\left\lfloor\frac{n+k-1}{2}\right\rfloor,
\qquad 1\le d<\tau.
\]

Consequently it gives the valid row-uniform bound

\[
B_C^{\mathrm{MCA}}(A)\le \binom{2{,}097{,}152}{913{,}633}.
\]

This is a rigorous upper bound, but it is not a usable adjacent certificate.
Because

\[
3\le913{,}633\le n-3,
\]

binomial unimodality gives

\[
\binom{n}{913{,}633}\ge\binom n3.
\]

Exact integer arithmetic gives

\[
\binom n3
=1{,}537{,}226{,}473{,}786{,}572{,}800,
\]

while

\[
B_*=274{,}980{,}728{,}111{,}395{,}087.
\]

The lower bound on the compiler's charge alone exceeds the entire budget by

\[
1{,}262{,}245{,}745{,}675{,}177{,}713,
\]

a factor greater than \(5.59\).  It therefore also exceeds the smaller current
budget remaining after the banked paid terms,

\[
U_{\mathrm{paid}}=2{,}602{,}153{,}473,
\qquad
B_*-U_{\mathrm{paid}}
=274{,}980{,}725{,}509{,}241{,}614.
\]

Hence the literal unrefined complete-absorption envelope cannot prove the
deployed inequality.  This does **not** show that the actual residual numerator
is large; it cuts only the use of that generic envelope as the final charge.

The saturated-BC budget audit already records this miss at index
\(\omega-w=913{,}633\).  The complete-absorption identity
\(d+1=913{,}633\) gives the exact index translation.  Thus the coarse route
cut is inherited; the following compiler-range corollary is the useful new
translation.

### Effective-deficiency corollary

The arithmetic sharpens the next target.  We have

\[
\binom n2=2{,}199{,}022{,}206{,}976
   <B_*-U_{\mathrm{paid}},
\]

but \(\binom n3>B_*>B_*-U_{\mathrm{paid}}\).  In the compiler range

\[
1\le d_{\mathrm{eff}}<\tau=981{,}104<\frac n2=1{,}048{,}576,
\]

the binomial sequence \(\binom n{d_{\mathrm{eff}}+1}\) is increasing.  Hence
the largest unrefined effective deficiency in this range that can fit is

\[
d_{\mathrm{eff}}=1.
\]

So an owner/effective-deficiency strategy must collapse

\[
913{,}632\longrightarrow d_{\mathrm{eff}}\le1
\]

if it still intends to pay by the bare complete-absorption binomial.  Any weaker
collapse needs a strictly sharper exact-root or structural count.

This replays the inherited budget wall and proves the exact
complete-absorption corollary

```text
INHERITED_ROUTE_CUT_UNREFINED_COMPLETE_ABSORPTION_ENVELOPE_AT_LINEAR_DEFICIENCY.
```

## Current predecessor state

The v1 deployed manifest already fails closed:

- zero deployed SPI charts are represented;
- the \(67{,}472\) indices are only a capacity namespace;
- the adapter is `UNPROVEN`;
- extension slopes, raw support multiplicity, and unmapped charts are excluded;
- `row_complete=false`;
- \(U_Q=U_A=\texttt{null}\).

Its verifier correctly requires the literal status `PROVED_ROW_UNIFORM`, no
excluded or uncovered scopes, explicit charts, and no unpaid terminals before a
row may be complete.  The new packet is not another atlas schema.  It theorem-
binds why a future fixed-pair artifact may not be relabelled row-uniform,
replays the already integrated coarse budget wall, and states its exact
complete-absorption effective-deficiency corollary.

## Verdict

**GREEN as a route cut; RED as a closure.**

The following are decided:

```text
fixed/sampled received-pair atlas -> deployed U_A            CUT
direct deficiency-one SPI theorem -> deployed high-def row   CUT
uniform deep theorem -> this agreement                        CUT
bare C(n,d+1) complete-absorption envelope -> row budget      CUT (inherited)
```

The following remains open:

```text
complete per-pair atlas + one uniform maximum
exhaustive canonical reduction + maximum type bound
first-match collapse to effective deficiency <= 1
sharper exact root union after owner pruning
active base-field-normalized split-pencil census
```

## Dependencies

- **PROVEN:** the row contract takes a supremum over all received pairs.
- **PROVEN:** the abstract fixed-pair-to-supremum implication is invalid.
- **PROVEN:** the deployed arithmetic and theorem-shape failures above.
- **PROVEN / INHERITED:** the saturated-BC packet's budget miss at the same
  binomial index, with the exact translation \(d+1=\omega-w=913{,}633\).
- **CONSUMED AT `PROVED / AUDIT`:** the fixed-deficiency complete-absorption
  theorem and its first-match stability statement.
- **UNPROVEN:** a row-uniform structural refinement fitting the exact budget.
- **UNPROVEN:** the quotient term \(U_Q\); even a future \(U_A\) payment alone
  does not finish the adjacent row.

## Parameter dependence

The quantifier route cut is parameter-free.  The shape and budget cuts are
specific to the printed KoalaBear row and agreement.  No asymptotic inference is
made from the finite arithmetic.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases and notation

- A pair-independent atlas is not required; a uniformly bounded complete atlas
  may depend on \((f,g)\).
- The SPI source's \(t=A-k\) and the fixed-deficiency source's error-budget
  \(t=n-A\) are different quantities.  This packet calls the latter \(\tau\).
- First-match deletion can make the true residual far smaller than the complete
  bound.  That possibility is precisely the live structural refinement.
- The statement \(d_{\mathrm{eff}}\le1\) is only the maximum that fits in the
  declared compiler range
  \(1\le d_{\mathrm{eff}}<\tau=981{,}104<n/2\); it is not a global statement
  across complementary binomial indices.
- Extension-valued slopes and raw support coverage remain outside the v1
  deployed manifest.
- No numeric \(U_A\) is inferred from `null`, and `null` is never treated as
  zero.

## Numerical evidence

None.  All displayed comparisons are exact integer identities or inequalities.
The abstract countermodel is a logical falsifier, not empirical evidence.

## Remaining risks

The complete-absorption theorem is consumed at its repository status
`PROVED / AUDIT`; it should receive a fresh proof review before this packet is
promoted.  A new exact root-union theorem could make the actual charge much
smaller without contradicting any route cut here.  The active final source
package also contains quotient/prefix and primitive shift-pair inputs, so the
split-pencil census is not by itself a global frontier closure.

## Minimal next action

Do not extract another fixed pair merely to obtain a local eliminant.  Freeze a
source-valid first-match residual class and prove one of:

1. every residual pair in that class has effective deficiency at most one;
2. its exact parameter-root union has a uniform charge below the remaining
   budget; or
3. it is covered by the active base-field-normalized split-pencil census with a
   printed finite constant.

Then take the supremum/maximum over the exhaustive classes, restore the still
open \(U_Q\), and run the literal integer inequality.

## Replay

```sh
python3 experimental/scripts/verify_m1_extension_uniform_atlas_route_cut_v2.py --check
python3 experimental/scripts/verify_m1_extension_uniform_atlas_route_cut_v2.py --tamper-selftest
python3 experimental/scripts/verify_fixed_deficiency_complete_absorption.py --check
python3 experimental/scripts/verify_fixed_deficiency_complete_absorption.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --tamper-selftest
python3 experimental/scripts/verify_saturated_bc_budget_fit.py
python3 experimental/scripts/verify_saturated_bc_budget_fit.py --tamper-selftest
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --check
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --tamper-selftest
```
