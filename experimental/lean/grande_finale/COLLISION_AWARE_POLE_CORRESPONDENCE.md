# `GrandeFinale.CollisionAwarePole` correspondence

## Status

`GrandeFinale/CollisionAwarePole.lean` formalizes the collision-aware
simple-pole conversion in `experimental/asymptotic_rs_mca_frontiers.tex`,
`thm:collision-aware-pole`, including the exact natural-number ceiling in
equation (4.2).

The source-facing theorem is `collisionAwarePole_of_codewordList`. Its input is
a nonempty finite list `L` of distinct codewords in the dimension-`k+1`
Reed--Solomon evaluation code. Every member of `L` must agree with one received
word on a support of size at least `m`, where `k + 1 ≤ m`. For an injective
evaluation map `ev : D → F` and `|D| < |F|`, it proves

```text
ceilDiv (L.card * (|F| - |D|))
  ((|F| - |D|) + k * (L.card - 1))
  ≤ B_MCA (RS(ev,k)) m.
```

The theorem chooses one degree-`≤k` polynomial representative for every listed
codeword, proves that these representatives form an equally large finite set,
and applies the polynomial-family core `collisionAwarePole_le_B_MCA`.

Thus the module proves the source theorem for a supplied codeword list and
exports its direct proper-challenge composition. It does not construct that
list or assign it a prefix-fiber size.

## Manuscript correspondence

Let

```text
n = Fintype.card D,
q = Fintype.card F,
d = q - n,
L = the supplied codeword Finset.
```

The Lean conclusion is

```text
(L.card * d) ⌈/⌉ (d + k * (L.card - 1))
  ≤ B_MCA (RS(ev,k)) m,
```

which is exactly

```text
ceil (|L|(q-n) / (q-n + k(|L|-1))) ≤ B_C^MCA(m).
```

No real-valued approximation is used: `Nat.ceilDiv` is the integer ceiling in
(4.2).

| Lean content | Manuscript source | Status |
|---|---|---|
| finite dimension-`k+1` codeword list | the `L` distinct listed codewords | Supplied input |
| one degree-`≤k` polynomial representative per listed codeword | listed polynomials `P_1,...,P_L` | `PROVED`, preserving list cardinality and agreement supports |
| allowed poles `F \ ev(D)`, of cardinality `q-n` | choice of `alpha ∈ F \ D` | `PROVED` for an injective evaluation map |
| ordered off-diagonal evaluation collisions | equalities `P_i(alpha)=P_j(alpha)`, `i ≠ j` | Definition |
| at most `k` collision poles for each distinct pair | a nonzero degree-at-most-`k` difference has at most `k` roots | `PROVED` |
| total collision budget `k L(L-1)` | unordered budget `k binom(L,2)` | `PROVED`; the ordered formulation doubles both the count and budget |
| existence of a pole with low collision count | averaging over the `q-n` allowed poles | `PROVED` |
| multiplicity second-moment identity | `sum_i m_i^2 = L +` ordered off-diagonal collisions | `PROVED` |
| distinct evaluation values at the selected pole | Cauchy--Schwarz distinct-value step | `PROVED` with the exact ceiling |
| `f_alpha`, `g_alpha`, and the dimension-`k` evaluation code | simple-pole received line | Definitions |
| every representative `P` gives the bad slope `P(alpha)` | quotient `(P-P(alpha))/(X-alpha)` and the supplied agreement support | `PROVED` in support-wise MCA form |
| the pole direction cannot be explained on `k+1` points | root bound for `(X-alpha)G+1`, whose value at `alpha` is `1` | `PROVED` |
| maximum over received lines | one received line carries at least `M(L)` distinct bad slopes | `PROVED` as a lower bound for `GrandeFinale.B_MCA` |

## Main declarations

| Declaration | Content | Status |
|---|---|---|
| `collisionAwarePole_of_codewordList` | Source-exact equation-(4.2) compiler from a supplied finite dimension-`k+1` codeword list to the full-field MCA numerator | `PROVED` |
| `collisionAwarePole_challenge_of_codewordList` | Direct composition of equation (4.2) with the exact proper-challenge ceiling from `ChallengeIntersection` | `PROVED` |
| `collisionAwarePole_le_B_MCA` | Polynomial-family core: compile an explicit nonempty family of distinct degree-`≤k` polynomials and their agreement supports to the same exact numerator bound | `PROVED` |

The codeword-list theorem has the manuscript-facing full-field interface. The
challenge theorem composes it with the integrated outer averaging compiler. The
polynomial-family theorem isolates the reusable collision and simple-pole core.

## Codeword representatives

| Declaration | Content | Status |
|---|---|---|
| `polynomialRepresentative` | Choose a polynomial witnessing one listed codeword’s membership in `rsEval ev (k+1)` | Definition |
| `polynomialRepresentative_spec` | The chosen polynomial has degree `< k+1` and evaluates to the listed codeword at every domain point | `PROVED` |
| `polynomialRepresentative_natDegree_le` | The chosen polynomial has natural degree at most `k` | `PROVED` |
| `polynomialRepresentative_injective` | Equal chosen representatives imply equal listed codewords | `PROVED` |
| `polynomialRepresentatives` | Duplicate-free finite set of representatives attached to the codeword list | Definition |
| `polynomialRepresentatives_card` | The representative set has exactly the codeword-list cardinality | `PROVED` |
| `exists_polynomialRepresentatives` | A nonempty codeword list yields an equally large nonempty polynomial family, preserving degree bounds and agreement supports | `PROVED` |

The representative construction does not assume that the supplied list is a
complete decoding list. It only converts its existing codewords into the
polynomial form used by the simple-pole proof.

## Collision-selection declarations

| Declaration | Content | Status |
|---|---|---|
| `collisionCount` | Ordered off-diagonal collisions among the evaluations of a finite polynomial family at one pole | Definition |
| `poly_agree_card_le` | Two distinct polynomials whose difference has degree at most `k` agree at at most `k` points of a finite pole set | `PROVED` |
| `sum_collisionCount_le` | Total ordered collision count over all allowed poles is at most `k * L * (L-1)` | `PROVED` |
| `exists_low_collision_pole` | Some allowed pole has collision count at most the average | `PROVED` |
| `sum_sq_fiber_card_pairs` | Sum of squared evaluation-fiber sizes equals the number of monochromatic ordered pairs | `PROVED` |
| `exists_eval_image_ceil` | Some pole has at least `ceilDiv (L*d) (d+k(L-1))` distinct polynomial values | `PROVED` |

The ordered collision convention matches the manuscript’s unordered convention:
each unordered colliding pair contributes two ordered pairs, while
`2 * binom(L,2) = L(L-1)`. The resulting ceiling is unchanged.

## Simple-pole declarations

| Declaration | Content | Status |
|---|---|---|
| `rsEval` | Reed--Solomon evaluation submodule of degree-`<k` polynomials along an arbitrary map `ev` | Definition |
| `mem_rsEval` | Polynomial-witness characterization of membership in `rsEval` | `PROVED` |
| `fpole` | First received word `U/(ev-alpha)` | Definition |
| `gpole` | Direction word `-1/(ev-alpha)` | Definition |
| `eval_slope_mcaBad` | A listed polynomial and its agreement support produce the support-wise MCA-bad slope `P(alpha)` | `PROVED` |

## Support-wise MCA semantics

The theorem targets the common `GrandeFinale.MCABad` predicate. A slope is
counted only when one support `S` simultaneously satisfies:

- `m ≤ S.card`;
- the line word at that slope is explained by a codeword on `S`;
- the pair `(f_alpha,g_alpha)` is not simultaneously explained on the same
  support `S`.

For a representative polynomial `P`, divisibility of

```text
P - C (P.eval alpha)
```

by

```text
X - C alpha
```

supplies a quotient of degree `< k`. Its evaluation explains the line word on
the supplied agreement support.

If `g_alpha` were also explained there by a degree-`<k` polynomial `G`, then

```text
(X - C alpha) * G + 1
```

would vanish at at least `k+1` distinct evaluation points despite having degree
at most `k` and being nonzero at `alpha`. This proves the required same-support
nontriviality.

The bad-slope object is a `Finset F`, so repeated values `P_i(alpha)` are
deduplicated. The collision calculation controls exactly this loss of distinct
slopes; it does not count polynomial or support witnesses as separate slopes.

## Reconciliation with existing Lean modules

### `GrandeFinale.lean`

The module composes the existing arithmetic kernels
`GrandeFinale.exists_le_average`, `GrandeFinale.distinct_value_floor`, and
`GrandeFinale.nat_ceil_div_le`. Those declarations already provide the abstract
averaging, Cauchy--Schwarz, and natural-ceiling steps.

`CollisionAwarePole.lean` supplies the polynomial collision census,
codeword-to-polynomial wrapper, simple-pole support semantics, and final
`B_MCA` compiler that instantiate those kernels as equation (4.2).

### `GrandeFinale/ChallengeIntersection.lean`

The integrated challenge-intersection module formalizes the complementary
outer step.
Its theorem `challenge_floor_of_full_floor` accepts any full-field inequality
`M ≤ B_MCA C m` and transfers it to the exact proper-challenge ceiling

```text
ceilDiv (Gamma.card * M) (Fintype.card F)
  ≤ B_MCA_challenge C m Gamma.
```

`collisionAwarePole_of_codewordList` supplies precisely such a full-field
inequality for `C = rsEval ev k`, and
`collisionAwarePole_challenge_of_codewordList` records the direct composition.
The declarations keep the inner polynomial-collision argument and outer
finite-group averaging argument separate; the prefix-list construction remains
a distinct upstream input to the composed route.

### `TowardsPrize.lean`

The `TowardsPrize` package already contains closely related ingredients:
`RS`, `poleF`, `poleG`, `cs_fiber`, `eval_eq_count_le`, `poles_colFar`,
`poles_closeBy`, `exists_low_collision`, and `deep_fiber_bound`.

That track uses integer radius, its own `CAbad`/`MCAbad` predicates, and a
rational inequality serving the deep-point list upper bound.
`CollisionAwarePole.lean` presents the same conversion in the shared
`GrandeFinale.MCABad` agreement-support vocabulary and concludes with the exact
natural-number lower bound for `GrandeFinale.B_MCA`.

The two tracks are complementary: `TowardsPrize` supplies its prize-facing
radius and normalized-error interface, while `CollisionAwarePole` supplies the
frontiers paper’s agreement-indexed numerator interface and exact equation-(4.2)
ceiling.

### `cap25_cap_v13_raw_compact`

The compact package already proves the same basic simple-pole semantics in
`RSMCA.gpole_col_bound` and `RSMCA.slope_mca_bad`. Its
`RSMCA.flexible_pole_conversion` obtains `L` distinct slopes when the stronger
collision-free budget

```text
n + L(L-1)k < q
```

guarantees a pole where every listed evaluation is distinct. It is stated for a
base-field domain `D : Finset B` and concludes a normalized real-valued `emca`
bound.

The compact package also contains `RSMCA.identity_floor`,
`RSMCA.exists_poly_list`, and deployed certificate wrappers.
`CollisionAwarePole.lean` complements that conversion by allowing collisions:
when a collision-free pole is unavailable, it pays the exact collision budget
and returns the ceiling in (4.2).

The modules retain their separate interfaces and uses. The present file does
not replace the compact package’s prefix-list construction or certificate
results.

## Exact boundary and nonclaims

This module does **not** prove:

- `prop:exact-prefix-list` or its prefix-list bijection;
- the list-size lower bound
  `ceil (choose n m / |B|^(m-k-1))`, or any identity-prefix floor;
- existence of the supplied codeword list;
- that the supplied list is the complete Reed--Solomon decoding list;
- `prop:simple-pole-lower` or equation (13.3) end to end;
- quotient, Chebyshev, planted, or remainder-profile list constructions;
- a safe-side bound, asymptotic frontier, threshold location, or deployed-row
  certificate.

Accordingly, the formal boundary is exact: equation (4.2) and its
proper-challenge composition are proved for a supplied finite
dimension-`k+1` codeword list. Constructing and sizing that list remain
separate upstream inputs.
