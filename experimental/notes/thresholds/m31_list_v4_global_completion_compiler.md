---
workboard_item: M0/M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The current source-bound Grande Finale v4 Mersenne-31 LIST contract has five codeword-valued atoms, one banked payment U_paid<=3730, and exact residual target Xi_46<=259880. The historical four-row v1 compiler is incompatible with this contract. The enumerated compatible artifact graph does not close the row: it leaves the cross-weight signed excess/deficit Q-owner terminal unpaid, and its numerical hypotheses admit a forbidden-size boundary-free histogram. Boundary-only additive/numerical owner hypotheses therefore cannot close the declared occupancy relaxation without a new cross-weight or interior theorem.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
compiler_id: M31_LIST_V4_GLOBAL_COMPLETION_COMPILER_V2
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: U_paid=LOW_EXACT_WEIGHT_PACKING; U_Q, U_list-int, U_ext, and high U_new remain null; global terminal UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER
quantifier: Uniform over every received word in F_(p^4)^D; the boundary-free histogram is an exact compiler countermodel, not a received-word construction.
projection_and_unit: Distinct codewords per received word. Supports, marked keys, template lines, rays, and slopes are diagnostics unless an explicit source-bound projection and add-back theorem is supplied.
claimed_bound: U_paid<=3730; derived exact closure gate Xi_46<=259880; exact forbidden threshold Xi_46>=259881; current compatible high-residual payment movement zero; the signed gate itself is unproved.
status: PROVED COMPILER MIGRATION / PROVED CURRENT-HYPOTHESIS ROUTE CUT / ROW OPEN
impact: ARCHITECTURE_BRIDGE / ROUTE_CUT
falsifier: A compatible current-v4 five-atom source proving a different banked value, a failure of the exact occupancy identity, a current theorem excluding the boundary-free histogram through a source-bound interior/cross-weight hypothesis, or a valid codeword-unit/add-back adapter for a candidate currently classified as diagnostic only.
replay: Primary and independent Python exact-integer compilers, canonical JSON/hash checks, 172 embedded source-path/hash checks, 29 internal payload/certificate pins, predecessor terminal checks, and hostile semantic mutations.
---

# M31 v4 global LIST completion compiler v2

## Status

```text
PROVED canonical current-v4 five-atom/codeword contract
PROVED U_paid <= 3,730 on exact error weights 0..614,160
PROVED the row inequality is equivalent to the signed gate Xi_46 <= 259,880
PROVED a boundary-free arithmetic relaxation attaining equality
PROVED raw T_46 <= 259,880 is false on an actual deployed boundary source
PROVED current numerical/partition hypotheses admit a boundary-free
       forbidden-size histogram
PROVED every c=2048 post-adapter packet enumerated here is diagnostic-only
U_Q        = null
U_list-int = null
U_ext      = null
high U_new = null
row closed = false
```

This packet replaces a stale authority, not a theorem.  The checked-in
four-row v1 compiler still names Grande Finale v3, has four LIST atoms, uses
slope/received-line units globally, and pins an obsolete hash of
`experimental/grande_finale.tex`.  Grande Finale v4 and the integrated M31
source adapter instead use five LIST atoms and codewords per received word.
The old verifier now fails its active-spine gate on current `main`.

The packet also performs the maximal exact exhaustion of its declared graph.
It binds every post-adapter global and `c=2048` route cut enumerated in
`SOURCE_GRAPH` to the one source partition, preserves all null atoms, and
shows that this compiler now requires a cross-weight theorem.  Older M31
packets remain transitive or superseded provenance.  It does not promote a boundary support theorem,
template-line dichotomy, semantic slope profile, or quotient-support witness
to a codeword payment.

## 1. Deployed row and live contract

Put

```text
p       = 2^31-1           = 2,147,483,647,
q       = p^4,
n       = 2^21             = 2,097,152,
K       = 2^20             = 1,048,576,
a       = 1,116,023,
R       = n-a              = 981,129,
w       = a-K              = 67,447,
B*      = floor(q/2^100)   = 16,777,215,
L       = B*+1             = 16,777,216.
```

The code is

\[
 C=\operatorname{RS}_{\mathbb F_{p^4}}(D,K),
 \qquad D\subset\mathbb F_p,
\]

and the unit is the number of distinct codewords in one closed radius-`R`
ball.  Grande Finale v4 requires the ordered sum

\[
 U_{\rm list}
 =U_{\rm paid}+U_Q+U_{\rm list-int}+U_{\rm ext}+U_{\rm new}.
\tag{1.1}
\]

The source partition is the one proved in
`m31_list_v4_source_adapter_global_coupled_residual.md`:

```text
architecture id: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom order: U_paid, U_Q, U_list_int, U_ext, U_new
owner order:
  LOW_EXACT_WEIGHT_PACKING
  HIGH_BOUNDARY_EXACT_CODEWORD
  HIGH_INTERIOR_EXACT_CODEWORD
quantifier: UNIFORM_OVER_ALL_RECEIVED_WORDS
unit: DISTINCT_CODEWORDS_PER_RECEIVED_WORD
```

Only the first owner is paid:

\[
 U_{\rm paid}\le3730.
\tag{1.2}
\]

No compatible integrated source supplies a nonnegative integer for any of
the other four atoms.

## 2. Why the four-row v1 compiler is not current authority

The historical artifact has all three load-bearing incompatibilities:

| field | historical four-row v1 | live M31 v4 LIST contract |
|---|---|---|
| architecture | `GRANDE_FINALE_V3_EXACT_COMPLETION` | `GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1` |
| LIST atoms | four; no separate `U_ext` | five, in the order (1.1) |
| unit/quantifier | slopes per received line | codewords per received word |

It also pins `experimental/grande_finale.tex` at SHA-256 `f419d3...`, while
the current v4 file has SHA-256 `346189...`.  On current `main`, its normal
replay stops at

```text
[FAIL] active-spine contract missing:
U_total=U_paid+U_Q+U_BC+U_new.
```

The exact row arithmetic in that artifact remains useful provenance.  Its
candidate interface is not a v4 LIST closure interface and cannot receive a
five-atom packet by changing data alone.

## 3. Exact signed occupancy theorem

For a received word, let

\[
 M_j=\#\{c\in C:|E(c)|=j\},\qquad0\le j\le R.
\]

Keep the proved cutoff and low cap

```text
J0 = 614,160,
N_low = sum_(j<=J0) M_j <= 3,730,
H = R-J0 = 366,969.
```

For high layers define

\[
 T_{46}=\sum_{j>J_0}(M_j-45)_+,
\]

\[
 H_r=\#\{j>J_0:M_j\ge r\},
 \quad C_{\rm low}=3730-N_{\rm low},
 \quad C_r=H-H_r\quad(1\le r\le45).
\]

The finite layer-cake identity is exact:

\[
 |\mathcal L_R(y)|
 =3730+45H+\Xi_{46},
 \qquad
 \Xi_{46}=T_{46}-C_{\rm low}-\sum_{r=1}^{45}C_r.
\tag{3.1}
\]

Since

```text
45H                 = 16,513,605,
3,730+45H           = 16,517,335,
B*-(3,730+45H)      =    259,880,
L -(3,730+45H)      =    259,881,
```

the row inequality is equivalent to the one signed target

\[
 \boxed{\Xi_{46}\le259880.}
\tag{3.2}
\]

A forbidden list forces `Xi_46>=259881` and at least that many marked
rank-46 diagnostic keys.  Those keys are injectively attached to
distinguished codewords but are not first-match owners.

There is no analytic layer-cake error in (3.1).  The missing-layer and
missing-anchor credits are exact and load-bearing.  They cannot be posted as
negative v4 atoms; a valid owner theorem must retain and refund them exactly
once inside one nonnegative first-match accounting.

## 4. Boundary-free compiler extremizer

A boundary-only additive/numerical owner theorem that leaves the interior
unconstrained cannot close the row from the current source/ledger hypotheses.
The following exact run-length encoded histogram satisfies every presently
declared numerical occupancy constraint and is the first forbidden point:

```text
M_614160 = 3,730,
M_j      = 46 for 614161 <= j <= 874086,
M_j      = 45 for 874087 <= j <= 981128,
M_981129 = 0.
```

For this histogram,

```text
T_46       = 259,926,
C_low      = 0,
sum C_r    = 45,
Xi_46      = 259,881,
total mass = 16,777,216 = L,
boundary mass = 0.
```

Thus the current exact arithmetic plus any added constraint solely on `M_R`
has a forbidden-size model with an empty boundary cell.  This is an
exact **compiler countermodel**, not a received-word construction.  It proves
logical insufficiency of the current additive/numerical hypotheses and
forbids a local-to-global inference from boundary closure alone.  An actual
row proof must add at least one theorem that constrains interior mass or
couples different weights.

The threshold is sharp inside the same arithmetic relaxation.  Replacing the
`46` block by `614161 <= j <= 874085` and starting the `45` block at `874086`
gives

```text
T_46       = 259,925,
sum C_r    = 45,
Xi_46      = 259,880,
total mass = 16,777,215 = B*.
```

Both RLE fixtures explicitly retain `M_R=0`.  Neither is asserted to arise
from a received word.

A sufficient unsigned alternative, using the worst-case low cap (1.2), is

\[
 \boxed{
 \sum_{614160<j\le981129}M_j\le16773485.
 }
\tag{4.1}
\]

## 5. Why a raw excess cap is also impossible

The integrated identity-prefix construction gives one actual deployed
received word whose certified boundary subfamily has

\[
 M_R\ge1993678.
\]

Consequently

\[
 T_{46}\ge M_R-45\ge1993633
 =259880+1733753.
\tag{5.1}
\]

The construction does not prove that the complete list is over budget.
It does prove that a row-uniform raw bound `T_46<=259880` is false.  The
certified subfamily is boundary-only, but the complete center's low and
interior codewords, hence its `C_low` and `C_r`, are unknown.  If that center
is safe, the exact identity (3.1) forces its complete credits to offset the
raw excess.  The next theorem must therefore be signed, chronology-valid,
and source-bound; it cannot simply bound the number of excess keys.

## 6. Current-artifact source graph

The compiler binds the following exact chain.

| packet | compatible consequence | payment |
|---|---|---:|
| v4 source adapter | exhaustive target-codeword weight partition; (1.2); (3.1) | `3730` |
| canonical masked Padé bridge | simultaneous canonical rank-three frame on every forced key | `0` |
| full-span forced collision cut | raw `T_46` cap refuted; signed cross-weight terminal isolated | `0` |
| `c=2048` boundary source/occupancy/carrier stack | exact boundary source families and carrier route cuts | `0` |
| fixed-template quotient/module stack | fixed-template caps and heavy module-rank-drop terminal | `0` |
| guarded VT and multitemplate stack | heavy-line or at least `986676` template lines at the post-`U_paid` gate | `0` |

The boundary stack ends in two unpaid branches:

```text
UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP
UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE
```

Its boundary subterminal remains
`UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`; the global terminal remains

```text
UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER.
```

The boundary packets count supports, template lines, or diagnostic columns.
They do not change the v4 codeword partition or its digest.

## 7. Open-PR compatibility gates

The live upstream audit found two relevant open packets.  Neither is imported
as a proof dependency here.

### PR #1047

The near-rational and primitive one-pencil constructors cap distinct slopes
per received line.  The v4 LIST adapter counts distinct codewords per received
word.  No source-defined codeword-to-line/ray/slope injection, realized-key
multiplicity, owner-ID map, refund, or all-pencil add-back theorem is supplied.
The exact finite `F_241` semantic regression is useful but toy-scale.
Therefore #1047 cannot currently enter `U_paid`.

### PR #1048

The pinned `(u,v)=(0,1)` quotient-support witness proves that the ambient
coefficient-four rooted-shell inequality fails with additive intercept
`b=3,4,5`: one anchor has six deficiency-64 same-prefix neighbors and
`4H_64<p^32`.  It supplies no received word, codeword realization,
first-match survival, or owner map.  It is a mandatory route-cut regression,
not a `U_Q` value.  A replacement may delete every such swap by a proved
earlier owner, use an actually proved intercept at least six, or replace the
pointwise shell premise.

### PR #1051

The cyclic quotient-rotation packet is an existential LIST lower construction
on a different row (`n=2^41`, `k=2^40`) and a multiplicative-coset domain.
It has no Chebyshev-domain adapter, first-match owner, all-weight refund, or
signed `Xi_46` theorem, so its M31 ledger movement is zero.  Its core formula
already appears in
`experimental/scripts/verify_quotient_cell_prefix_fiber_floor.py`; the PR is
a self-contained proof and replay hardening of that prior audit result.  The
large quotient fiber is nevertheless a useful falsifier: a future
domain-uniform exchange theorem must route that family to a quotient owner or
use a genuinely fixed-Chebyshev hypothesis.

## 8. Exact compiler verdict

The only compatible current atom vector is

```text
U_paid     = 3,730
U_Q        = null
U_list-int = null
U_ext      = null
U_new      = null
known sum  = 3,730
available high allowance = 16,773,485
```

Closure fails closed because four atoms are null and both the global
cross-weight terminal and the two boundary VT branches remain unpaid.  The
compiler terminal is

```text
CURRENT_ARTIFACT_SET_ROUTE_CUT_CROSS_WEIGHT_THEOREM_REQUIRED.
```

This is not `SAFE`, a counterexample, or an official-row movement.

The compiler accepts exactly two completion modes.  The additive mode must
supply all five exact nonnegative source-partition atoms, empty the residual,
and fit their sum under `B*`.  The direct mode may instead prove the uniform
codeword-valued signed theorem (3.2).  A direct signed proof closes the row but
does not fabricate values for the four null atoms and does not create a
negative-refund ledger interface.

## 9. Maximal successor theorem

A closing successor must be one source-bound theorem over the complete
target-field list.  It may prove (4.1) directly, prove (3.2) with exact
first-match refunds, or emit exact nonnegative values for all five atoms.
If it uses the present route, it must simultaneously:

1. retain every exact weight and the signed occupancy credits;
2. map boundary codewords to an attained `U_Q` target and interior codewords
   to a source-defined `U_list-int` chart, or keep them in a named `U_new`;
3. classify the heavy fixed-template module-rank-drop branch;
4. classify the dispersed higher-order multitemplate incidence branch;
5. handle the #1048 `T_64` family as an owner or retained residual;
6. give a codeword-unit extension projection payment rather than treating
   scalar descent as `U_ext=0`;
7. prove disjoint add-back with no unresolved primitive component; and
8. compare the resulting exact integer sum with `16,777,215`.

Another boundary-only, fixed-width, fixed-template, support-only, or
line-slope computation cannot discharge this theorem.

### 9.1 Primary-literature route audit

No checked general theorem supplies this successor for the fixed Chebyshev
domain.  The generic/higher-order-MDS capacity theorem of
[Brakensiek--Gopi--Makam](https://arxiv.org/abs/2206.05256) concerns generic
evaluation points, while this row freezes one highly structured domain.  The
directly matching subfield-evaluation interpolation of
[Guruswami--Xing](https://arxiv.org/abs/1708.01070) is limited here by the
extension degree four: its displayed radius reaches at most
`floor(4(n-K)/5)=838860`, which is `142269` errors short of `R=981129`.
Standard folded Reed--Solomon results such as
[Guruswami--Rudra](https://arxiv.org/abs/cs/0511072) and the later
[folded-Wronskian list bound](https://arxiv.org/abs/2410.09031) use block
Hamming distance on multiplicative folds; they do not transfer to scalar
Hamming distance on the fixed Chebyshev fibers.

The credible literature-guided route is therefore a new weighted
Chebyshev-folded affine-containment/Wronskian theorem that retains arbitrary
partial-fiber errors and the signed credits in (3.1).  A complete-fiber or
block-metric estimate alone is another route cut, not a source-bound payment.

## 10. Proof-audit summary

Statement audited:

The implication from the source adapter, every post-adapter route cut
enumerated in `SOURCE_GRAPH`, and open PR #1047/#1048/#1051 to the v4 LIST inequality
`B^list_C(1116023)<=16777215`.

Files/sections read:

Grande Finale v4 final LIST ledger; the historical four-row v1 compiler;
the v4 source adapter; canonical masked/full-span route cuts; the complete
enumerated `c=2048` fixed-template/VT stack; and the open-PR diffs/artifacts
for #1047/#1048/#1051.  The applicability audit also read the primary generic-RS,
subfield-evaluation, and folded-RS theorem statements linked in Section 9.1.

Dependencies:

- PROVEN: row constants, v4 source partition, low cap, signed identity,
  forced-key frame, integrated route cuts, and narrow #1048 counterexample.
- PROVEN LOCAL: #1046 boundary stratification and #1047 profile constructors.
- UNPROVEN: every codeword-unit owner/projection/add-back theorem named in
  Section 9.
- INAPPLICABLE WITHOUT A NEW ADAPTER: generic-domain and folded block-metric
  capacity theorems.
- BROKEN AS CURRENT AUTHORITY: historical four-row v1 contract and source
  pin.

Parameter dependence:

All statements are finite at the exact row in Section 1.  There are no hidden
asymptotic constants.

Layer-cake / dyadic summability:

Equation (3.1) is a finite exact identity with no error term.  Dyadic
summability is not applicable.

Moment / Markov / Chebyshev:

Not applicable.  `Chebyshev` names the fold.

Edge cases / notation:

Boundary is exactly `j=R`; interior is `J0<j<R`.  A boundary support is not
automatically `U_Q`; an interior support is not automatically `U_list-int`;
scalar descent is not `U_ext=0`; marked keys and template lines are not
owners; and the boundary-free histogram is not a received-word witness.

Numerical evidence:

All displayed arithmetic is exact.  Small-field fixtures in predecessor
packets test algebraic implications only and are not deployed evidence.

Verdict:

YELLOW - the canonical current contract and sharp route cut are proved, but
the global list inequality remains unresolved; do not authorize a closure
claim.

Remaining risks:

The cross-weight incidence theorem may require new mathematics; neither
boundary VT branch is paid; signed credits have no standalone negative atom;
and a candidate owner can fail through unit, quantifier, target-map, or
add-back mismatch.

Minimal next action:

The requested action is maximal: prove the complete-list theorem in Section
9 or terminate with a new source-valid primitive/counterexample.  Do not
return to another isolated boundary packet.

## 11. Replay

From the repository root:

```text
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --check
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --check
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler.py --tamper-selftest
python3 experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py --check
python3 -O experimental/scripts/verify_m31_list_v4_global_completion_compiler_independent.py --check
```

The compiler uses exact integers only.  Passing it certifies the architecture
migration, all 172 source bindings and 29 internal pins in the enumerated
post-adapter graph, the arithmetic route cut, and the fail-closed null state.
It does not prove the missing cross-weight theorem.
