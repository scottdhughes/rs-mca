# AGENTS.md — RS–MCA Resolution Protocol

> **Updated:** 2026-07-22
> **State snapshot:** `main@fb6d9555339b43911c59c498373c43ed6c5cd391`
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


There is also a high-priority list-decoding objective: obtain better ordinary Reed--Solomon list-decoding bounds beyond the Johnson radius. These may come either directly from the list-side machinery in the papers and experimental notes, or indirectly from sufficiently strong CA/MCA upper bounds through the BCHKS25 and CS25 conversions surveyed in `open-proximity.tex` Theorems 5.2 and 5.3. Any such contribution must state the exact code (`C` or `C^+`), radius shifts, list-size bound, field denominator, and whether the result is theorem-level, conditional, or computational.

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
- The live Mersenne-31 LIST compiler returns `CURRENT_ARTIFACT_SET_ROUTE_CUT_CROSS_WEIGHT_THEOREM_REQUIRED`, not `SAFE`.
- Every deployed `U_Q` remains `null`.
- No row has complete active-architecture `U_paid`, exhaustive MCA balanced-core or list-interior payment, zero/exact residual, and chronology-correct add-back.
- The KoalaBear legacy M1 stack records local `U_paid=422354730332` and local remainder `274980305756664755`, but neither is banked in Grande Finale v4 because the source-bound owner/partition bridge is missing.
- Under the latest corrected direct extension charge, positive extension dimension is excluded on Mersenne-31 and dimension at least two is excluded on KoalaBear. These are route cuts, not payments or nonexistence theorems.
- The newly integrated M31 packets add local padding-bridge, masked-saturation, common-core add-back, rank-two/coloop, rooted-shell, C7--C9, and route-cut infrastructure.  These are not adjacent-row payments: source-bound owner/refund, rooted-shell completion, residual projection, and final finite-ledger terminals remain open.
- The source-bound Mersenne-31 v4 LIST adapter proves one bankable codeword payment, `U_paid<=3730`, on exact error weights through `614160`.  Its four remaining atoms `U_Q`, `U_list-int`, `U_ext`, and `U_new` are null, and its global terminal is `UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL` (refined downstream to `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`).
- The all-weight anchor-exchange packet gives an exact codeword bijection relative to any actual listed anchor.  With `t=R-j0` and `m=deg(G)-t`, every nonanchor is represented uniquely by a divisor/gcd pair satisfying `m>=67448`, `deg(b)<m-67447`, and `deg(gcd(L0,G-bV))>=m`.  Since `B*+1<q`, fresh-symbol boundary forcing reduces the remaining direct theorem exactly to `#X(V)<=16777214` for boundary anchors `t=0`, still with arbitrary unit `V`.  Every unit `V mod L0` is realizable, so one anchor plus the rank-two module cannot force quotient, periodic, rational, or low-degree structure.  This is a zero-payment route cut, not row closure.
- The boundary common-`V` full-locator route-cut packet proves the exact fixed-`G` Johnson wings and uniform excess thresholds, the nonzero pairwise Wronskian, the split-support moment, and the whole-list deep-tail cap `1001282`.  Scalar descent followed by fresh-symbol forcing over `F_p` reduces every live violation to a boundary census with all polynomial data in `F_p` and one arbitrary base-field unit `V`.  The `V=1` slice is exactly a depth-`w` locator-prefix fiber, but an exhaustive `F_7` control proves that arbitrary `V` can be strictly larger, so `V=1` is not an authorized reduction.  Any forbidden boundary list retains at least `15775933` pairs with excess at most `366886`; their locators are not proved distinct.  A literal Chebyshev support family shows that the enumerated cardinality, pairwise-intersection, fixed-weight, and `T2/T4` occupancy data permit exponentially too many abstract templates, while the unreduced quartic base-field gate has sharp worst-case codimension only `3(m-w)`.  Substituting the new deep cap into the rank-46 cutoff gives the worse baseline `17511197>B*`, so ledger movement is zero.  The live terminal is `UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE`.
- The common-`V` split-flat successor proves that every fixed-full-gcd boundary chart is an affine `d`-flat of exact codimension `w` with no rank-drop branch, while every nonempty interior chart has codimension at least `w+1` and the correct, different full-gcd quotient gate.  Below `p-1`, the individual `gcd(b_i,H_i)=1` gates and pairwise Wronskian vanishing on locator intersections/nonvanishing on symmetric differences are necessary and sufficient to reconstruct one common unit `V`; at `B*` the exact field margin is `2130706431`.  Hence there is no hidden triple-or-higher common-`V` obstruction.  A fixed-`G` slice ranges over every nowhere-zero ordinary RS received word and has nonpositive Johnson denominator throughout `72859<=m<=908270`.  This is a zero-payment route cut; the exact live terminal is `UNPAID_PAIRWISE_SPLIT_RATIONAL_FUNCTION_DIVISOR_INCIDENCE`, and the shallow upper `15775932` remains open.
- The universal fixed-`G` successor removes both residual filters from that observation.  For any ordinary base-field RS list on an `R`-subset of the deployed domain, one common constant translation avoids all received-word zeros and leaves at least `1107301=R+126172` simultaneous good numerator roots at list size `B*=16777215`; choosing one split `G` on those roots embeds all `B*` ordinary codewords plus the zero anchor into one M31 boundary ball.  Thus row safety necessarily forces the uniform deterministic punctured-RS cap `M_ord<=B*-1=16777214`; the unresolved post-Johnson interval is exactly `72859<=m<=908270`, or `5412<=d<=840823`.  This is a zero-payment route cut, not a list upper or global converse; the local terminal is `UNPAID_UNIFORM_DETERMINISTIC_PUNCTURED_RS_LIST_BOUND`, while the varying-`G` pairwise-incidence terminal also remains open.
- The varying-`G` affine-span/shortening successor proves the exact realized-codeword inequality `sum_i binom(w+s_i+r+e,r)<=binom(R+g-e,r)`, where `r` is the shallow codeword-span rank, `g` is the union of numerator-root sets, and `e` is the common denominator-zero count on `E0`.  At the forced shallow size `15775933`, ranks at most four are impossible; rank five forces `g>=874886`, rank six forces `g>=87070`, and exact worst-case excess ceilings are recorded through rank ten.  Rank seven and above remain open, with no uniform full-range cut at rank eleven.  One-coordinate agreement shortening/error puncturing also closes the two fixed-`G` endpoints, shrinking its unresolved interval to `72860<=m<=908269`, or `5413<=d<=840822`.  Exhaustive tiny cells show mixed-`G` realized amplification, so fixed-`G` is not a global proxy.  Ledger movement is zero and the live combined terminal is `UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE`.
- The marked-basis successor frees the first agreement pivot and proves colored `S0`/`E0`, cross-block, affine-line, and projective-ray refinements.  At shallow size `15775933` it excludes codeword-span ranks one through five and forces every rank-six survivor into `781458<=g<=1033227`, with exact aggregate excess ceiling `96161189784`.  A realized `GF(17)` family saturates the `E0`-marked inequality and misses total first-pivot equality only by the excluded zero-anchor basis, while an explicit nonrealized deployed scalar profile passes all present aggregate gates.  Thus this is a bankable local route cut with zero ledger movement, not row closure; the live terminal is `UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.
- The generalized-weight/codimension-one successor closes that entire rank-six window.  Retaining the actual weight hierarchy in the marked affine-line count forces `q5<=32004` and `1048581<=d5(W_c)<=1080585`.  A `d5`-minimizing hyperplane is support-saturated, and the proved MDS-soft codimension-one compiler bounds its whole rank-six affine chart by `908116`, contradicting the required `15775933` actual shallow codewords by `14867817`.  Hence every forbidden shallow family has codeword-span rank at least seven.  This is independently replayed local theorem progress with zero ledger movement, not row closure; the live terminal is `UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.
- The truncated-weight/flag successor proves the all-rank affine-fiber inequality `sum_i prod_{j=k+1}^r(d_j-R+eta+s_i)<=B_k(d_r)_(r-k)` and exhausts the first surviving rank.  At rank seven it forces `q6<=242225`, pays the common-zero Johnson flank `67454<=g<=72427`, and pays the whole-chart codimension-one flank `354999<=g<=1116023`.  The exact middle `72428<=g<=354998` remains open: `72428<=g<=72859` is a mixed-locator near-MDS terminal after fixed-`G` ownership, while `72860<=g<=354998` contains the deterministic punctured ordinary-RS middle.  This is zero-ledger route-cut progress, not rank-seven or row closure; the live terminals are `UNPAID_RANK7_MIXED_G_NEAR_MDS_LOCATOR_INCIDENCE` and `UNPAID_RANK7_FIXED_G_ORDINARY_RS_MIDDLE_OR_MIXED_G`.
- The order-32 Chebyshev maximum-fiber successor exhausts the complete scale-`65536` one-prefix counterexample template.  For every puncture of the 32-point quotient, all `C(31,17)=265182525` moving supports were censused exactly: the unique largest sum fiber has size `C(15,8)=6435`, consists of the antipode of the puncture plus eight complete antipodal pairs, and is far below the forbidden size `16777216`.  Both the literal multiplicative-style quotient rotation and the intrinsic `T31` Chebyshev rotation have exact fiber size one.  The same 6435-member family disproves the tempting dual higher-MDS specialization on this deterministic quotient.  This is a zero-payment route cut, not row safety or a global `U_Q`; the next exact quotient terminal is `UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION`.
- The older four-row v1 machine compiler is a historical Grande Finale v3 structural preflight.  It has four LIST atoms, slope/received-line units, and a stale `grande_finale.tex` source pin; it is not the live v4 Mersenne-31 LIST contract.
- A schema/hash pass is structural preflight only. The trusted-source registry is empty; parsing a manifest does not prove an atom.

## 3. Document authority

| File | Role |
|---|---|
| `experimental/notes/thresholds/m31_list_v4_global_completion_compiler.md` and `experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json` | **Live Mersenne-31 LIST completion authority:** current v4 five-atom contract, signed closure gate, enumerated zero-movement route-cut graph, and the sharp boundary-only additive/numerical insufficiency certificate. |
| `experimental/notes/thresholds/m31_list_v4_source_adapter_global_coupled_residual.md` and `experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json` | **Live Mersenne-31 LIST source/partition authority:** v4 five-atom codeword chronology, the banked low-weight payment, exact whole-list source partition, and global residual. |
| `experimental/notes/thresholds/m31_all_weight_anchor_exchange_pade_bijection_v1.md` and `experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json` | **Live all-weight diagnostic reduction:** exact actual-anchor codeword bijection, corrected interpolation-module orientation, slack-normal gcd-incidence census, fresh-symbol reduction to boundary anchors, and generic-unit-`V` route cut.  It has zero ledger movement and does not prove the M31 census bound. |
| `experimental/notes/thresholds/m31_boundary_common_v_cross_g_route_cut_v1.md` and `experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/manifest.json` | **Live boundary-census route-cut authority:** scalar descent to a base-field boundary census; exact fixed-locator, pairwise-Wronskian, split-moment, deep-tail, `V=1` nonextremality, restricted-support, and Singleton cuts; localization to at least `15775933` shallow common-`V` pairs in the full locator census; exact proof that the new tail cutoff is not a v4 rank-46 payment.  The common-`V` split-flat incidence theorem and row remain open. |
| `experimental/notes/thresholds/m31_common_v_split_flat_pairwise_crt_equivalence_v1.md` and `experimental/data/certificates/m31-common-v-split-flat-pairwise-crt-equivalence-v1/manifest.json` | **Live split-flat/CRT route-cut authority:** exact fixed-`H` boundary and interior affine charts, full-gcd orientations, individual denominator-unit gates, pairwise Wronskian necessity and sufficiency for one common `V` under the deployed field margin, exact boundary-list reconstruction, and the fixed-`G` nowhere-zero ordinary-RS embedding.  It moves no ledger atom and leaves the global pairwise split-rational incidence upper open. |
| `experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md` and `experimental/data/certificates/m31-fixed-g-universal-rs-embedding-v1/manifest.json` | **Live fixed-`G` hardness/adapter authority:** exact constant-translation removal of received-word zeros and split-numerator coprimality, simultaneous common-`G` construction with deployed margin `126172`, and threshold embedding of arbitrary base-field ordinary RS lists on deployed `R`-subsets.  It proves the necessary cap `M_ord<=16777214` for M31 safety, but neither that cap nor the varying-`G` residual, and it moves no ledger atom. |
| `experimental/notes/thresholds/m31_varying_g_affine_span_shortening_route_cut_v1.md` and `experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/manifest.json` | **Live affine-span/fixed-`G` endpoint route-cut authority:** exact excess-weighted realized-codeword basis inequality; exclusion of shallow affine ranks at most four; rank-five/rank-six union thresholds and rank-five-through-ten excess ceilings; exhaustive tiny mixed-`G` controls; and exact shortening/error-puncturing closure of the two former fixed-`G` endpoints.  It moves no ledger atom and leaves high affine rank plus the deterministic fixed-`G` middle open. |
| `experimental/notes/thresholds/m31_varying_g_first_pivot_basis_route_cut_v1.md` and `experimental/data/certificates/m31-varying-g-first-pivot-basis-route-cut-v1/manifest.json` | **Live marked-basis rank route-cut authority:** first-pivot, colored-block, cross-block, affine-line, and projective-ray inequalities; exclusion of shallow codeword-span ranks one through five; exact rank-six union window and aggregate excess ceiling; and a realized tiny sharpness family plus nonrealized deployed scalar route cut.  It moves no ledger atom and leaves rank-six fixed-syndrome split-rational incidence open. |
| `experimental/notes/thresholds/m31_rank6_generalized_weight_codim_one_closure_v1.md` and `experimental/data/certificates/m31-rank6-generalized-weight-codim1-closure-v1/manifest.json` | **Live rank-six closure authority:** generalized-weight marked-line refinement, exact `q5` and `d5` windows, support-saturated minimizing hyperplane, exact codimension-one compiler map, and the whole-chart upper `908116`.  It excludes rank six with a `14867817`-codeword gap, moves no ledger atom, and leaves rank at least seven plus the full M31 LIST row open. |
| `experimental/notes/thresholds/m31_rank7_truncated_weight_flag_route_cut_v1.md` and `experimental/data/certificates/m31-rank7-truncated-weight-flag-route-cut-v1/manifest.json` | **Live rank-seven route-cut authority:** rank-uniform truncated generalized-weight/affine-fiber theorem; exact `q6` envelope; complete common-zero Johnson and codimension-one flank payments; fixed-`G` first-match removal in the near-MDS sliver; and the exact `72428<=g<=354998` primitive interval.  It moves no ledger atom and leaves the rank-seven mixed-`G` and deterministic ordinary-RS middle, ranks at least eight, and the full M31 LIST row open. |
| `experimental/notes/thresholds/m31_chebyshev_order32_max_fiber_route_cut_v1.md` and `experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/manifest.json` | **Live order-32 Chebyshev route-cut authority:** exact lift from a quotient sum fiber to the deployed M31 LIST row, exhaustive all-puncture maximum `6435`, unique antipodal `T2` maximizing family, and injectivity of both the multiplicative-style and intrinsic `T31` quotient rotations.  It cuts only the complete scale-`65536` one-prefix template, moves no ledger atom, and leaves the order-64 two-prefix/global-Q and broad ordinary-RS terminals open. |
| `experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md` and `experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json` | **Historical v3 structural preflight:** exact row arithmetic and legacy architecture checks only; not a current v4 LIST closure authority. |
| `experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex` | **Direct problem/falsifier authority:** benchmark conjectures, exact compiler requirements, finite barriers, and separation of finite from conjectural asymptotic claims. |
| `experimental/grande_finale.tex` | **Active conditional completion architecture:** proved local theorems, order-32/rational-atom reductions, owner localization, spread-core incidence bounds, and exact completion problems. Hypotheses/problems are not row bounds. |
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

The current all-weight direct coordinate is exact, and fresh-symbol forcing
reduces row closure to boundary anchors.  Relative to every boundary anchor,
prove

```text
#X(V) <= 16777214
```

uniformly over the full divisor/gcd census, or produce an actual boundary
anchor triple exceeding it.  Here `t=0`, `m=deg(G)`, and the gates are
`67448<=m<=981129`, `deg(b)<m-67447`, and
`deg(gcd(L0,G-bV))>=m`.  Do not specialize to `V=1`, return to one fixed
weight, or count supports in place of codewords unless an exhaustive,
disjoint bridge back to this census is proved.

The current exact route cuts force any forbidden boundary list to retain at
least `15775933` pairs with excess `0<=s<=366886`.  This is a full-locator
census, not proof that the surviving pairs use distinct `G` values.  Their
codeword span has rank at least seven.  The predecessor inequality
`sum_i binom(w+s_i+r+e,r)<=binom(R+g-e,r)` is strengthened by marked
first-pivot and split-block counts: rank five is excluded, and the parent
traps rank six in `781458<=g<=1033227`.  The generalized-weight successor
then forces `q5<=32004`, chooses a support-saturated `d5`-minimizing
hyperplane, and applies the whole-chart codimension-one compiler to obtain
the exact upper `908116<15775933`; rank six is therefore impossible.  The
truncated-weight successor then pays rank seven for `g<=72427` and
`g>=354999`, leaving exactly `72428<=g<=354998` with explicit `q1/q6`
compiler-failure gates.  Its first 432 union sizes are a mixed-locator
near-MDS terminal after fixed-`G` first match; the remaining interval contains
the deterministic ordinary-RS middle.  Ranks at least eight also remain
unpaid, and rank twelve receives no uniform first-pivot cut over the full
shallow range.  The next varying-`G` theorem must therefore pay the exact
rank-seven middle without assuming locator variation, then extend to a
rank-at-least-eight positive-`w` fixed-syndrome secant or split-rational
incidence theorem.  After
the individual `gcd(b_i,H_i)=1` gates, the common arbitrary base-field `V`
has been eliminated exactly: pairwise Wronskian vanishing on `H`
intersections and nonvanishing on symmetric differences is both necessary
and sufficient.  Prove that every canonical shallow family satisfying those
gates has size at most `15775932`, or construct `15775933` members.  The
family may concentrate on one `G`; fixed-`G` already embeds every ordinary
base-field RS received word after one common translation.  One-coordinate
peeling closes its former endpoints, but the uniform deterministic interval
`72860<=m<=908269` remains open.  The translation
also makes every numerator coprime to one split `G`, so neither nonvanishing
nor denominator coprimality can supply a generic saving.  Therefore a
closure must prove the uniform deterministic punctured-RS cap on the
fixed-`G` subclass and also control varying `G`, or give an exhaustive
source-bound quotient/Chebyshev/CA owner bridge that pays both.  Do not
return to another fixed-locator rank calculation or assume cross-`G`
variation.

The complete scale-`65536`, order-32, one-prefix Chebyshev construction is
now closed as a counterexample route: every puncture has exact maximum sum
fiber `6435`, with a unique antipodal `T2` owner, while both the literal and
intrinsic `T31` rotated prefix maps are injective.  Do not rerun this rung,
infer a global `U_Q`, or specialize a generic higher-MDS theorem to it.  The
next quotient rung, if used, must be the scale-`32768`, order-64, two-prefix
map with exhaustive
owner routing; its terminal is
`UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION`.

#### M2. Transfer the theorem or record a new floor

If true, isolate exactly what transfers to KoalaBear Q or other list/MCA cells, with field and projection hypotheses explicit. If false, record the witness mechanism, update the benchmark conjecture/lower floor, and remove every invalidated closure route.

Never describe this auxiliary `2^-100` row as an unresolved `2^-128` Prize row.

### Lane L — improve ordinary RS list decoding beyond Johnson

Produce a theorem, conditional theorem, or exact computational certificate giving a better ordinary Reed--Solomon list-size bound at a radius beyond the Johnson radius. This lane is separate from MCA: the output unit is codewords in a Hamming ball around one received word.

Valid routes include:

- direct list-side proofs from the locator-prefix, shortening, prefix-fiber, affine-span, rank-flat, or interior-list machinery in `slackMCA_v4.tex`, `RS_MCA_Paving_v9.2.tex`, `tex/cs25_cap_v13_2.tex`, and `experimental/grande_finale.tex`;
- computational certificates for exact finite list-size upper bounds or counterexamples at declared rows;
- indirect derivations from a proved CA/MCA upper bound using `open-proximity.tex` Theorem 5.2 (BCHKS25) or Theorem 5.3 (CS25), with the theorem's radius shift, intrinsic-radius condition, and `C` versus `C^+` code shift printed explicitly.

A useful list-decoding packet must print:

```text
row:                 (F, D, k, n, rho)
object:              ordinary LIST, not MCA
radius/agreement:    exact delta and integer agreement
Johnson comparison:  exact Johnson radius and post-Johnson gap
bound:               exact list-size upper bound, or exact lower counterexample
route:               DIRECT_LIST / BCHKS_CA_TO_LIST / CS_CA_TO_LIST / COMPUTATIONAL
CA_or_MCA_input:     exact epsilon bound if using a conversion
code_shift:          C or C^+ = RS(k+1)
status:              PROVED / CONDITIONAL / EXPERIMENTAL / COUNTEREXAMPLE / AUDIT
```

Do not claim an MCA bad-slope numerator as a list bound. Conversely, if a list lower bound is converted into MCA failure by a simple-pole or deep-point argument, record it under the MCA row as a lower/unsafe result, not as list safety.

### Lane T — cross-row theorems only when they specialize to a live integer

A Sidon/Fourier, entropy, incidence, shortening, or ray theorem belongs here only if it supplies:

- a bankable exact atom in Lane K, L, or M;
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
