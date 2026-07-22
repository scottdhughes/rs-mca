# AGENTS.md — RS–MCA Resolution Protocol

> **Updated:** 2026-07-21
> **State snapshot:** `main@32a41660e3088eeeb15a16645330856794302ff0`
> **Supersedes:** all older priority lists in this file.

Edit this workboard in place. Never append another “current focus”, “highest priority”, or competing task list.

Before starting, compare the snapshot with current `main`, then read the newest entry in `experimental/agents-log.md` and the live four-row completion packet. If the state changed, update the snapshot, authority table, and workboard before doing mathematics.

## 1. Mission and resolution standard

The target is the true numerator

```text
B^MCA_{C,Gamma}(a)
  = maximum, over received lines, of the number of distinct bad slopes.
```

The repository should be driven toward a direct proof or counterexample about this quantity, not toward more summaries, theorem skeletons, or a formally checked unresolved ledger.

Grande Finale v4 is the preferred current completion architecture, but it is not the definition of truth. A uniform direct theorem may bypass it. A counterexample to one proof route need not refute the target inequality.

The primary unresolved official benchmark in the four-row packet is

```text
KoalaBear MCA, target 2^-128:
B^MCA_C(1116048) <= 274980728111395087.
```

Agreement `1116047` is already proved unsafe. Proving the displayed upper bound therefore determines the first safe agreement exactly.

A result counts as resolution progress only if it does at least one of these:

1. proves or refutes a direct benchmark inequality;
2. replaces a live `null` atom by an independently reviewed exact integer;
3. supplies the missing source-bound architecture/owner bridge;
4. proves exhaustive coverage and the correct slope/codeword projection for a live residual;
5. rigorously removes a live route and updates the residual state; or
6. completes the exact add-back and row certificate.

For a family-level or asymptotic resolution, give a matching upper/lower bracket for the true numerator on a precisely declared family. The identity-profile formula remains an identity-candidate conjecture until witness exhaustion and every payment are proved.

Protocol consumption is downstream and is not a current resolution target.

In this file, `Q` means the pruned locator-prefix maximum-fiber atom; `BC` means the balanced-core distinct-slope atom; and `U_list_int` means the arbitrary-word interior codeword atom. These are ledger names, not assumptions that the corresponding bounds are proved.

## 2. Target correction and current verified state

The nonzero-budget packet contains one official primary MCA row and three auxiliary theorem-building rows:

| Row | Role and target | Unsafe `a0` | Candidate `a+` | `B*` | Full-budget Q multiplier floor | Verdict |
|---|---|---:|---:|---:|---:|---|
| KoalaBear MCA | **primary**, `2^-128` | 1116047 | 1116048 | 274980728111395087 | 4807520 | open |
| KoalaBear list | auxiliary, `2^-128` | 1116046 | 1116047 | 274980728111395087 | 4226236 | open |
| Mersenne-31 MCA | auxiliary, `2^-100` | 1116023 | 1116024 | 16777215 | 9 | open |
| Mersenne-31 list | **analytic stress test**, `2^-100` | 1116022 | 1116023 | 16777215 | 8 | open |

**Do not misstate the target.** For the Mersenne-31 code over `F_(p^4)`, target `2^-128` has integer budget `B*=0`; its complete safe set is empty. The `B*=16777215` Mersenne rows are `2^-100` stress tests, not unresolved `2^-128` Prize rows.

At this snapshot:

- CAP25 v13.2 proves the unsafe endpoints and reusable foundation results.
- Grande Finale v4 proves many local identities, order-32/rational-atom reductions, owner localization, and spread-core incidence bounds, but no adjacent safe row.
- The live compiler returns `ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET`, not `SAFE`.
- Every deployed `U_Q` remains `null`.
- The Mersenne-31 LIST source adapter now gives one bankable v4 cell,
  `LOW_EXACT_WEIGHT_PACKING -> U_paid<=3730`, directly over `F_(p^4)`.
  Its high boundary/interior `U_new` residual remains `null`.
- No row has complete active-architecture `U_paid`, exhaustive MCA balanced-core or list-interior payment, zero/exact residual, and chronology-correct add-back.
- The KoalaBear legacy M1 stack records local `U_paid=422354730332` and local remainder `274980305756664755`, but neither is banked in Grande Finale v4 because the source-bound owner/partition bridge is missing.
- Under the latest corrected direct extension charge, positive extension dimension is excluded on Mersenne-31 and dimension at least two is excluded on KoalaBear. These are route cuts, not payments or nonexistence theorems.
- The M31 LIST algebraic padding bridge and distinguished-column coloop are
  closed: the canonical Popov and masked Padé pairs have the same polynomial
  right kernel, the padding mask is recovered by a monic gcd, and every
  forced key has a simultaneous canonical rank-three frame.  Identically
  forced collision forms are now classified exactly as membership in the
  complete containment-row span, or equivalently as scaled-column equality
  in an evaluated low-degree Popov syzygy code.  A complete `GF(17)` layer
  and every 46-column marked key realize the maximum-rank
  syndrome-hyperplane branch while the natural anchor-extra forced-root
  unions retain packing five and transversal six, so forcedness alone does
  not establish a semantic owner.  The global complete-class incidence/owner refund,
  residual, and final finite-ledger terminals remain open.
- The deployed `c=2048` fixed-remainder construction is now an actual
  exact-boundary source, not just arithmetic: one base-field received word
  has a complete quartic-field ball with at least `6796405` codewords, all at
  agreement `1116023`.  Consequently `T46>=6796360`, so the flat raw cap
  `T46<=259880` fails by `6536480`.  The exact cutoff optimizer refutes every
  flat baseline `b>=28`; `b=27` is the largest source-compatible baseline,
  but its aggregate 28-column Forney data do not force a two-row degree below
  `67447`.  Two-row control first occurs at `b=29`, already source-refuted.
  Under the declared first-match convention cross-audited against upstream PR
  #1032 and the integrated QR2 normal form, the certified fixed-remainder
  subfamily is removed by or at `C1_QUOTIENT_REMAINDER`; its post-C1
  primitive-Q residual is zero.  Thus this cuts only the unqualified
  flat-raw-tail-plus-aggregate-Forney architecture, moves no atom, and leaves
  both the numerical C1 codeword payment and the variable-remainder/orientation
  residual open.  Arbitrary supports in the complete prefix fiber are not
  classified by this statement.
- The full `c=2048` exact-boundary partial-occupancy atlas is now exhaustive.
  Its `261192` profiles split into `616` C1-shaped Euclidean-remainder faces
  and `260576` bi-deep profiles; the latter split into `31712` visible-arm
  and `228864` double-strict profiles.  For every target-field received word,
  either every bi-deep profile has at most 29 codewords, giving total
  `<=7556704`, or one fixed profile contains 30 codewords and the
  field-generic coupled kernel supplies two independent rows of combined
  degree `<=65262<67447`.  This is a boundary route reduction, not an owner:
  the 30-column carrier is unpaid, the faces enter C1 for arbitrary words
  only after the missing boundary-to-prefix adapter, the conditional combined
  face/carrier target `9216781` is not a payment, high interior weights remain
  open, and no ledger atom moves.
- The two prospective easy exits from that boundary reduction are now cut
  off exactly.  A fixed-multipartial-template construction gives a separately
  realized boundary source in every feasible profile; 177 profiles have
  certified floor at least 30, including 141 bi-deep profiles; one additional
  bi-deep profile has floor 29 where 29 columns suffice, and `(u,v)=(1,1)`
  has floor `1693898`.  Thus this sufficient criterion certifies 142 separate
  source profiles: 124 at width 29 and 18 at width 30.
  Its fixed partial-error core sharpens the two-row degree to
  `65106`; on 124 certified source profiles with `u>=2`, 29 columns already
  give at most `67366<67447`.  Separately, one deployed arbitrary word has two exact
  `(0,0)` codewords with the same fixed remainder in both orientations but
  distinct agreement and error locator prefixes.  Thus no common codeword
  translation or operation leaving those supports literally fixed makes the
  pair's actual monic locators share one prefix target.  The packet-local
  boundary diagnostic now requests a fixed-syndrome multiprefix face/carrier
  owner or payment; no C1 or carrier atom moves and no global terminal is
  replaced.
- The complete exact-boundary atlas now has two budget-aligned carrier
  triggers.  A combined face/carrier charge above `9216781` forces 36
  codewords in one profile; direct low-plus-boundary excess above `B*` forces
  65, because `3730+64*261192=16720018<B*` by `57197`.  On 65 columns the
  sharp cumulative coupled-index ladder is
  `(14502,29004,43506,58008)`, at least 50 module rows lie below the cutoff,
  and a basis-relative two-column minor of degree at most `29004` is fixed on
  at least `38444` variable roots of each nonanchor locator.  Exactly 156
  separately realized source profiles already contain 65 codewords, so a
  cap of 64 is false.  Over the actual coefficient field `F_(p^4)`, the
  proper-hyperplane deformation bound covers every budget-sized prescribed
  packet (and in fact widths through `6823032369902110`).  Thus low rank plus
  profile pigeonhole cannot force a collision owner unless a collision form
  vanishes identically or complete-layer incidence supplies new information.
  The anchor ladder is basis-relative and nonnested, not a canonical owner;
  no atom moves.
- The whole fixed-partial-template class now has an exact interleaved
  quotient-RS upper theorem.  For profile `(u,v)`, a fixed partial template
  has at most one codeword when `v>=512`; otherwise, with `kappa=512-v`, its
  complete family is at most
  `floor(C(1023-u-v,kappa)/C(544-v,kappa))`.  This fits `B*` on 25767 of
  261192 profiles but fails on 235425, including `(0,0)`.  Locator depth-w
  jets and normalized-cofactor depth-w jets are in fiber-preserving
  bijection.  One fixed `(0,0)` template attains at least 15 different such
  targets, and one received word has two same-profile codewords with
  different partial templates.  Thus the legal object is the disjoint sum
  over profiles, exact partial templates, and attained cofactor jets; neither
  a maximum prefix fiber nor one common template can replace it.  The exact
  residual is `UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`; no atom moves.
- The conditional strong-subspace-design route is now localized exactly.
  For a fixed template, every family above `Lambda_SD(u,v)` contains a
  Chen--Zhang minimal bad subfamily whose free-`F[phi]` difference matrix
  has smaller `F(T)`-rank than `F`-affine dimension.  The determinant-
  valuation bound on the full-module-rank stratum is
  `sum_b dim(W intersect H_b)<=deg(delta_ell)<=ell(D-1)+min(ell,137)`.
  The exact conditional thresholds have maximum 17 and sum to `1988814`
  over all 261192 profiles.  They are not unconditional caps: separately
  realized fixed-multipartial-template rank-one sources exceed them in 193
  profiles, including floors `6796405` at `(0,0)` and `1693898` at `(1,1)`;
  these floors are not simultaneous around one received word.
  The nested diagnostic subterminal is
  `UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP`; the packet-local boundary
  subterminal stays `UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`, while the
  active global M1 terminal stays
  `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER` and the partition is unchanged.
  Rank-drop classification, cross-template guarded incidence, high interior,
  and every ledger payment remain open; no atom moves.
- The complete `c=2048` varying-template boundary family is now reindexed as
  one exact target-field syndrome incidence with guarded shortened-dual
  flats.  After the fixed-template caps are imposed, the uniform boundary
  bound `U` is equivalent whenever `p^4>(U+1)981129` to `VT(U)`: every
  cap-respecting `U+1` support family either spans the full dual or its span
  absorbs a one-point escape.  Failure of both alternatives constructs an
  actual target-field received word with every support exact.  The live gates
  hold for `U=9216781`, `U=B*-3730=16773485`, and `U=B*=16777215`.
  Shifted locators make 16 the first containment-rank gate; a compatible
  16-packet has row-syzygy dimension at least `30577`.  A fixed-template
  block above its conditional `Lambda_SD` threshold contains a module-rank
  deficient subfamily, but that module span is not the shortened-flat span.
  `VT(U)` itself remains unproved, no boundary or interior atom moves, and
  the active global M1 terminal remains
  `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`.
- The maximal current-hypothesis `VT` stratification is now exact.  Boundary
  locators occupy two degree-filtered `F`-vector-space slices inside the
  rank-2048 free module `F[T]^2048`; these slices are not `F[T]`-submodules.
  A primitive `F(T)` locator line is exactly one positional partial-template
  block.  For two supports and `x in E minus F`, the inverse residue is
  `B(x)^(-1)A_x` of degree `d-1`, so pairwise escape absorption occurs exactly
  for `d<=w`; a common-root escape is never pairwise absorbed.  Distinct exact
  supports in one received-word boundary list have `d>=w+1`, their shortened
  flats intersect trivially, and every useful escape/dependency is therefore
  genuinely higher-order.  A failed live `VT` packet either contains an
  unpaid fixed-template module-rank-drop block or uses at least `542164`,
  `986676`, or `986896` primitive lines at the three live gates.  Canonical
  depth-32 `H=1` source cosets with `v+v'<=32` are injectively separated, so
  the five largest separately realized floors cannot be summed despite their
  formal `429716` excess over `B*`.  The remaining diagnostic is
  `UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE`; no atom moves.
- A schema/hash pass is structural preflight only. The legacy four-row compiler trusted-source registry is empty; the new M31 adapter hash-binds its theorem sources, but parsing either manifest does not itself prove an atom.

## 3. Document authority

| File | Role |
|---|---|
| `experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md` and `experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json` | **Live status authority:** current null atoms, route cuts, architecture IDs, exact row arithmetic, and replay contract. |
| `experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex` | **Direct problem/falsifier authority:** benchmark conjectures, exact compiler requirements, finite barriers, and separation of finite from conjectural asymptotic claims. |
| `experimental/grande_finale.tex` | **Active conditional completion architecture:** proved local theorems, order-32/rational-atom reductions, owner localization, spread-core incidence bounds, and exact completion problems. Hypotheses/problems are not row bounds. |
| `experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md` and `experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json` | **M1 target-source adapter authority:** direct quartic exact-layer lift, bankable low-weight cell, exact global occupancy, coupled rank-46 diagnostic, and explicit unpaid high residual. It does not close the row. |
| `experimental/notes/thresholds/m31_canonical_masked_pade_global_route_cut.md` and `experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json` | **M1 canonical-mask authority:** target-field Popov–Padé right-kernel bridge, exact padding/error classifier, simultaneous rank-three/no-coloop theorem, conditional target-field deformation dichotomy, and exhaustive natural-collision regression. It moves no atom and leaves the row open. |
| `experimental/notes/thresholds/m31_full_span_forced_collision_route_cut.md` and `experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json` | **M1 forced-collision authority:** exact annihilator/quotient-column/Popov evaluation criterion, graph-to-common-zero interface, maximum-rank syndrome-hyperplane route cut, and exhaustive full-span regression. It moves no atom and leaves the row open. |
| `experimental/notes/thresholds/m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut.md` and `experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json` | **M1 exact realized C1-boundary source authority:** general fixed-remainder polynomial-fold lemma, deployed `c=2048` list floor `6796405`, exact declared QR2/C1 route of the structured subfamily, raw signed chronology specialization, exhaustive flat-baseline optimizer, and aggregate-Forney route cut. It proves no numerical C1 or Q upper payment and moves no atom. |
| `experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md` and `experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json` | **M1 exact boundary-atlas authority:** exhaustive `c=2048` occupancy parameterization, C1-shaped/bi-deep/visible-arm/core partition, target-field arbitrary-subpacket lift, and the exact `7556704`-or-30-carrier dichotomy. The carrier owner, arbitrary-word C1 adapter/payment, and high interior remain open; ledger movement is zero. |
| `experimental/notes/thresholds/m31_c2048_multiprefix_30carrier_activation_route_cut.md` and `experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json` | **M1 boundary successor authority:** separately realized fixed-multipartial exact sources in every occupancy profile, the exact 177/141 certified-floor census and 142-profile sufficient-criterion width census, the source-specific 30/29-column determinantal-divisor sharpening, the deployed same-remainder literal-locator multiprefix obstruction, and the arbitrary-word `Y-P=L_S H` replacement. It proves no universal carrier theorem or C1/carrier payment and moves no atom. |
| `experimental/notes/thresholds/m31_c2048_65column_fixed_anchor_boundary_route_cut.md` and `experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json` | **M1 whole-boundary carrier authority:** exact width-36 combined-gate and width-65 direct-boundary triggers, sharp cumulative kernel-index ladder, 50-row/cutoff Hilbert floor, basis-relative fixed-anchor incidences, 156-profile source nonemptiness, and target-field proper-component deformation route cut through every budget-sized packet. The anchor is not canonical, the identically forced branch is unpaid, high interior remains open, and no atom moves. |
| `experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md` and `experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json` | **M1 fixed-template quotient authority:** exact interleaved quotient-RS cap for every profile/template, complete 25767/235425 budget census, locator/cofactor jet bijection, 15-target fixed-template construction, and varying-template gluing cut. The complete profile/template/attained-jet sum remains unpaid, high interior remains open, and no atom moves. |
| `experimental/notes/thresholds/m31_c2048_fixed_template_module_rank_route_cut.md` and `experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json` | **M1 fixed-template module-rank authority:** direct determinantal-divisor/Smith bound on module-regular difference spans, localized Chen--Zhang minimal-sublist dichotomy, exact conditional threshold histogram/sum, and the 193-profile rank-one source obstruction. Module-rank drop and varying-template aggregation remain unpaid; the conditional threshold sum is not a ledger charge and no atom moves. |
| `experimental/notes/thresholds/m31_c2048_guarded_support_flat_separator.md` and `experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json` | **M1 whole-boundary separator authority:** exact target-field syndrome/support-flat reindexing, guarded one-point escapes, forward/converse `VT(U)` equivalence at all live union gates, and the shifted-locator 15/16 interface. `VT(U)`, high interior, and the global terminal remain open; no atom moves. |
| `experimental/notes/thresholds/m31_c2048_vt_multitemplate_global_rank_route_cut.md` and `experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1/manifest.json` | **M1 maximal current-hypothesis VT route-cut authority:** exact global locator slices, primitive-line/template equivalence, pairwise inverse-residue and flat-intersection formulas, heavy-line/many-line dichotomy, and canonical depth-32 source-coset separation. Both terminal branches and the genuinely higher-order guarded multitemplate incidence remain unpaid; no atom moves. |
| `tex/cs25_cap_v13_2.tex` | **Foundation/unsafe authority:** exact unsafe endpoints, field/domain conventions, reductions, and certificate grammar. |
| `RS_MCA_Paving_v9.2.tex` | **Fixed ePrint basis for unconditional paving results:** shortening, MDS circuit, exact finite, exponential-budget, and conditional Sidon-to-flatness results from ePrint 2026/1463. It does not solve the subexponential near-capacity frontier. |
| `experimental/rs_mca_thresholds.tex` | **Exact-regime/exposition source:** staircases, below-half-distance results, syndrome geometry, and examples; not unrestricted near-capacity closure authority. |
| `tex/RS_disproof_v3.tex`, `tex/slackMCA_v4.tex`, `tex/snarks_v5.tex` | Stable background for no-slack obstructions, reserve/quotient theory, and later protocol accounting. |
| `archived/` predecessors | Provenance only. Never bank an archived owner or charge without an explicit source-bound bridge. |

`experimental/agents-log.md` is a coordination record, not proof authority.

## 4. The one live workboard

Work on exactly one item below. Every contribution must name its row, direct target, item ID, quantifier, projection, and exact impact.

### Lane K — close or refute KoalaBear MCA at `2^-128`

#### K0. Freeze one active row contract

Maintain one canonical manifest containing fields, domain, `n`, `k`, target, endpoint convention, challenge denominator, active architecture ID, partition digest, owner order, object `MCA`, unit “distinct bad slopes per received line”, and exact budget. Every candidate atom binds to it.

#### K1. Make existing KoalaBear work bankable

Either:

- prove a source-bound, owner-by-owner bridge from the legacy M1 partition into the active Grande Finale v4 first-match partition, including inherited charge and exhaustive scope; or
- re-prove the useful local payments directly inside the active partition.

Do not add more legacy-local charges unless they independently prove the direct numerator inequality or include this bridge. Matching parameters and similar cell names are not a composition theorem.

#### K2. Prove the exact pruned row-sharp Q atom

Prove one joint maximum over the frozen first-match residual, using the actual domain, attained image, target map, orientation transport, support-to-parameter coalescing, and a uniform received-line quantifier. Output an exact integer `U_Q`.

The factor `4807520` is only a full-budget calibration before other atoms consume reserve. A shell bound, average, lower floor, target value, separately normalized residual, or conditional allocation is not `U_Q`.

#### K3. Pay MCA projection and residual geometry

Produce exhaustive balanced-core coverage in units of distinct affine slopes. The moving-root theorem pays only charts proved to be genuine pencils. A line-by-line decomposition also needs an exact count of relevant lines. Higher-dimensional cores require a proved ray/slope compiler with exact multiplicities.

#### K4. Close algebraic routing and add-back

Pay or eliminate quotient, extension, periodic/descent, rank, padding, common-core, planted, sparse, shortened, interleaved-list, and every other named cell in the same first-match chronology. Prove `U_new=0` or give an exact integer for each survivor.

#### K5. Emit the row certificate

Prove with exact integers

```text
U_total = U_paid + U_Q + U_BC + U_new
        <= 274980728111395087.
```

Replay it with independent implementations and mutation tests. Then state:

```text
first safe agreement       = 1116048
largest safe grid radius   = 981104/2097152
real safe set              = [0, 981105/2097152)
real supremum              = 981105/2097152, not attained
```

A direct uniform proof of `B^MCA_C(1116048)<=B*` may replace K1-K5, but it must still provide independently checkable constants and endpoint conversion.

### Lane M — use Mersenne-31 list at `2^-100` as the tight falsification test

#### M0. Decide the direct inequality

Prove or refute

```text
B^list_C(1116023) <= 16777215.
```

This is a codeword-count statement; the MCA ray compiler is inapplicable.

#### M1. Resolve the binding primitive-fiber/list-interior problem

The full-budget target is only about `8.4152` times the full-slice average, and the true allowance is smaller after other payments. Prove a realized-image, frozen-residual maximum or construct a received word exceeding the budget. Existing one-shell and rooted-shell packets are local reductions, not exhaustive row bounds.

Current source-bound status: the v4 adapter lifts the complete exact-support,
common-core, Padé, and coupled-kernel chain directly to the deployed
quartic field.  The fixed low-weight predicate is bankable as
`U_paid<=3730`.  Every remaining target codeword lies in one explicit
boundary or interior `U_new` residual.  Any hypothetical forbidden list
forces at least `259881` distinct marked target-codeword keys, and every key
has three independent simultaneous canonical Popov--Padé rows of combined
degree at most `62295<67447`.  The discarded-agreement mask and actual error
locator are recovered exactly by a monic gcd; fixed-layer transport obeys an
exact diagonal-saturation law; and deleting the distinguished column cannot
drop the rank.  The conditional target-field deformation dichotomy proves
that selected-family cardinality cannot force a collision unless a collision
form is identically zero on the common containment space.  An exhaustive
same-received-word `GF(17)` layer has disjoint-packing optimum five and
natural collision-root transversal number six, so the local coupled data do
not force packing at most four or a four-point transversal for those natural
unions.  The exact forced-form classifier is
now proved: a collision form is identically zero exactly when its normalized
escape columns agree modulo the complete containment-row span, equivalently
when a two-column vector lies in the evaluated low-degree Popov syzygy code.
At maximum containment rank, this says only that the original codewords
collide.  The same complete `GF(17)` layer and all 92 individual 46-column
marked keys have locator-span rank `K-1`; all marked keys have identically
forced collisions, and the exact natural-union packing/transversal
obstruction persists.  Complete-class connectivity can legally feed
common-zero/rank-flat/puncturing owners, but no current theorem forces enough
connectivity or supplies a chronology-valid codeword charge/refund.
`U_Q`, `U_list-int`, `U_ext`, and the high `U_new` value remain null.  The
global terminal is `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`; its local
scaled-column subterminal is `UNPAID_SPLIT_LOCATOR_HYPERPLANE_OWNER_REFUND`,
with primitive subterminal `UNPAID_PRIMITIVE_FORCED_ESCAPE_COLUMN_COLLISION`.
The stronger deployed `c=2048` fixed-remainder source has
`M_R>=6796405`; its complete ball is boundary-only and base-field-valued.
Its certified structured subfamily has agreement profile `(544,1911)` and
complement profile `(479,137)`, since
`981129=479*2048+137`.  Both sides satisfy QR2.  Under the upstream #1032
first-match convention this subfamily is removed by or at C1 and contributes
zero to primitive Q; this does not classify arbitrary supports in
the complete prefix fiber or provide a numerical C1 upper payment.
Hence `T46>=6796360`, refuting the raw cap by `6536480`.  More generally, the
exact moving-cutoff optimizer makes `b=27` the largest flat raw baseline not
refuted by this source.  At `b=27`, the current aggregate Forney theorem gives
first-two index sum at most `70282>67447`; two-row control first appears at
`b=29`, but every `b>=28` is already source-incompatible.  Thus no flat raw
baseline can combine the present source and aggregate Forney ingredients to
close the row.  On this exact-boundary center
`Xi46=M_R-16517335`, so `Xi46<=259880` is exactly the row-sharp Q bound
`M_R<=B*`; it is not a cheaper occupancy lemma, and the v4 grammar has no
negative-refund interface.

The packet-local maximal `c=2048` exact-boundary diagnostic subterminal inside
`HIGH_BOUNDARY_EXACT_CODEWORD` / `U_new` is now
`UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`.  The fixed-template interleaved
quotient cap fits the full-row budget individually for every fixed template
in 25767 profile shapes, but it is not a first-match payment and leaves
235425 shapes above budget.  Its exact locator/cofactor bridge shows that the complete
object is the disjoint sum over profile, exact partial template, and attained
normalized cofactor jet.  One fixed template attains at least 15 targets, and
two same-profile codewords can have different templates, so neither inner sum
may be erased.  The next maximal attack must bound this complete attained
incidence sum, route a disjoint portion into row-sharp Q with an exact
codeword charge, and classify the varying-template residual; every component
must yield a chronology-valid paid owner, a budget-fitting attained-image
sum, or an explicit primitive route cut.  The combined disjoint face/carrier
payment must be no smaller than the realized `6796405` floor and no larger
than `9216781`.  This target still does not pay the high interior: a full row
proof must handle `U_list-int`, `U_ext`, and the remaining high `U_new` mass.
All five v4 atoms, global M1 terminals, and high-interior obligations remain
unchanged.  Do not return to a standalone fixed-width carrier, replace the
attained sum by one maximum fiber, or invoke QR2 directly for a general
partial template whose degree can exceed 2048.

#### M2. Transfer the theorem or record a new floor

If true, isolate exactly what transfers to KoalaBear Q or other list/MCA cells, with field and projection hypotheses explicit. If false, record the witness mechanism, update the benchmark conjecture/lower floor, and remove every invalidated closure route.

Never describe this auxiliary `2^-100` row as an unresolved `2^-128` Prize row.

### Lane T — cross-row theorems only when they specialize to a live integer

A Sidon/Fourier, entropy, incidence, shortening, or ray theorem belongs here only if it supplies:

- a bankable exact atom in Lane K or M;
- a direct benchmark upper theorem;
- a direct benchmark counterexample; or
- a rigorous route cut that updates the compiler residual.

An `exp(o(n))` bound, unspecified polynomial loss, fixed low moment, heuristic, or theorem skeleton does not decide the few-bit Mersenne margins and does not automatically fit KoalaBear.

## 5. Exact bankability contract

For Grande Finale v4, every bad object enters one declared, non-oracular, witness-exhaustive first-match partition.

```text
MCA:  U_total = U_paid + U_Q + U_BC       + U_new
LIST: U_total = U_paid + U_Q + U_list_int + U_ext + U_new
```

Every atom shares the same row/target, object, architecture ID, partition digest, owner order, received-line/word quantifier, unit, and source-bound dependencies. Every value is an exact nonnegative integer.

No atom may consume the full budget unless all other atoms are proved zero. Lower bounds, capacities, headrooms, averages, and allocations are not upper payments.

A direct theorem outside the compiler is welcome, but it must state the same row, object, uniform quantifier, unit, and exact target inequality.

Every note, audit, script packet, or PR begins with:

```yaml
workboard_item: K0/K1/K2/K3/K4/K5/M0/M1/M2/T
row: exact row name
object: MCA/LIST/CA/LINE/OTHER
target_epsilon: exact value
agreement: exact integer
B_star: exact integer
direct_statement: exact theorem or inequality
architecture: DIRECT or exact architecture id
partition_digest: required unless DIRECT
atom_or_cell: exact owner/atom, or DIRECT
quantifier: exact maximum/uniform statement
projection_and_unit: slopes/rays/codewords/supports/pairs
claimed_bound: exact integer or symbolic theorem
status: PROVED/CONDITIONAL/CONJECTURAL/EXPERIMENTAL/AUDIT/COUNTEREXAMPLE
impact: ROW_CLOSURE/ROW_COUNTEREXAMPLE/BANKABLE_ATOM/ARCHITECTURE_BRIDGE/ROUTE_CUT/LOCAL_ONLY
falsifier: explicit invalidating condition or witness
replay: commands and source hashes, when computational
```

`PROVED LOCAL` is not automatically `BANKABLE_ATOM`. State the remaining bridge to the row numerator.

## 6. Stop rules

The following do not count by themselves as resolution progress:

```text
new theorem statements without proofs;
Lean stubs, axiomatized global conjectures, or correspondence names;
new survey or “final” paper drafts;
theorem-label maps and clean rewrites;
toy examples not testing a live claim;
random-fiber heuristics or small scans without a lifting theorem;
structural JSON/schema acceptance;
proofs inside an unmapped archived architecture;
a lower construction falling below budget;
a shell, pencil, or chart silently treated as exhaustive;
an asymptotic loss substituted for an exact finite reserve.
```

Do not start protocol accounting, broad end-to-end formalization, or another grand synthesis paper while the direct benchmark and live atoms remain open.

## 7. Audit, replay, and Lean

### Adversarial audits

Test witness exhaustion, first-match chronology, uniformity, attained-image normalization, projection to slopes/codewords, field/orbit/rank/degree multiplicities, owner composition, integer rounding, endpoints, and any local-to-exhaustive jump.

End every audit with exactly one verdict:

```text
NO ISSUE
FIXED
OPEN GAP
COUNTEREXAMPLE_NEW_FLOOR
```

An `OPEN GAP` names the workboard item and smallest missing theorem/integer. A counterexample updates the direct target, compiler residual, or obstruction floor.

### Computational packets

A closing packet includes exact inputs, source labels and hashes, integer-only gates, canonical JSON, human-readable proof summary, an independently written verifier, optimized/non-optimized replay where relevant, mutation tests, and explicit nonclaims. Floating point never decides a gate. A stale source pin is a failed provenance gate.

### Lean policy

Lean verifies frozen mathematics; it is not a substitute for missing mathematics. High-value targets are proved local theorems used by live atoms, first-match/add-back kernels, endpoint/integer conversion, final row certificates, and counterexample correspondence.

A declaration is certified only after the package builds and its statement is manually matched to the proof source. An axiom, `sorry`, theorem target, or skeleton is not a proof or success criterion. Do not formalize Grande Finale v4 “end to end” while its global inputs remain hypotheses.

## 8. Stable invariants

- Keep base/coefficient field, ambient/code field, line field, challenge field, and every denominator distinct unless a theorem transfers them.
- Keep list, CA, support-wise MCA, line decoding, supports, pairs, rays, and affine slopes distinct.
- MCA counts each affine slope once; an enormous support census may represent one slope.
- Use exact integer budgets and closed-ball endpoint conventions.
- Do not use an extension field to pay a base-field image/entropy deficit without a transfer theorem.
- Do not call a residual predicate a payment or a first-match list exhaustive merely because its last cell is “other”.
- Do not merge atoms from different partitions, owner orders, normalizations, or quantifiers.
- Keep Papers A-D stable unless the maintainer requests edits; new work starts in `experimental/`.
- Log every material experimental change in `experimental/agents-log.md`.
- Preserve status labels; never promote conditional, experimental, or local results to proved row statements.

## 9. Minimal reading path and promotion

1. Live four-row compiler note and canonical JSON.
2. Introduction, exact compiler, finite benchmark, and finite-closure problem in `Conjectures_and_Barriers_RS_MCA_v4_1.tex`.
3. Audited-status, finite-Q barrier, and exact-completion sections of `grande_finale.tex`.
4. Exact unsafe-row/certificate sections of `cs25_cap_v13_2.tex`.
5. Main theorem/status sections of root-level `RS_MCA_Paving_v9.2.tex` (ePrint 2026/1463).
6. Only then, row-specific notes and scripts named by the live compiler.
7. Use `rs_mca_thresholds.tex` for solved exact regimes; use archives only for provenance.

Do not begin by reading every historical note. Start from the direct inequality and follow only dependencies that can change its truth or exact bound.

Promote a result only after its direct statement and quantifiers are frozen, dependencies are source-bound, finite specialization is replayed, projection/ownership is audited, status is proved, and the workboard is updated. Close or refute a row before writing the paper that calls it a resolution.

## 10. Definition of done

The primary finite program is done when one of these is checked in and independently audited:

### KoalaBear safe resolution

```text
B^MCA_C(1116047) > 274980728111395087
B^MCA_C(1116048) <= 274980728111395087
```

with the exact half-open safe set and endpoint data from K5.

### KoalaBear counterexample/new floor

An explicit received line has more than `274980728111395087` bad slopes at agreement `1116048`, together with the resulting later unsafe edge or obstruction mechanism.

### Uniform theorem

A proved theorem specializes to the KoalaBear inequality and states exactly whether and how it transfers to the auxiliary list and Mersenne stress rows.

For the broader RS-MCA problem, “done” means a direct, peer-auditable classification of the true numerator or safe set on the declared family, not completion of a chosen ledger, a conditional identity profile, or a formalized conjecture.
