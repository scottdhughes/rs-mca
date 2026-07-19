# Rank-16 finite owner-prefix source theorem

**Status:** Conditional finite deployed-field theorem. The official score
remains `0/2`.

**Source floor:**
`origin/main@3404d21b64c876c6d9b995ad3e29d7120ab27a54`. The literal scalar residual
stage depends on PR #890 head
`a5b98c75d0e3732e9659d8fd220c821329e572e4`, whose frozen patch has SHA-256
`d967f805d1e70074eced0599a0e70e261d3317047e10ec78e419059156642307`.

**Audits:** The repaired-proof packet
`f81b88257b0630bbf326b8a621db53f8acedefaf76a11ecbea9afb213705bd5a`
and the independent source/compiler packet
`fe564be3814b3b86f210c0a4b45a402d0f96655a4abb6a9c57bf5a04fffb4e75`
both returned `ACCEPT_NARROWED`. Their frozen public records have SHA-256
`40793334976e80353213cdf2c6ebb9a54eb7f37a1a79fa75925ef21f18bb3d0e`
and `45b19d9e79f7ec2e3c14faacadb6906971111d67c48e11acdbbe1723fa6393c7`.

## Exact statement

Work over the deployed field with

`p=2,130,706,433`, `n=2,097,152`, `K=1,048,576`, `m=1,116,047`,
`B=32,768`, and `T=274,854,110,496,187,592`.

For each normalized word `U:H->F_p`, let `S_P` be the canonical first exactly
`m` agreement set of each degree-`<K` listed polynomial `P`. Apply the
inherited sequential first-match owner through `J48`. On its current residual,
append in order:

1. every exact A in profile `(31,14,7,0,0,0), f64=27`, capacity `432,442`;
2. every exact A in profile `(31,15,6,2,1,0), f64=27`, capacity `432,442`;
3. source A-ranks `1..14,645` in profile `(31,15,6,3,1,0), f64=26`,
   capacity `5,812,512` per exact A;
4. exact-F ranks `1..4,152,808` at source A-rank `14,646`, capacity five;
5. literally
   `O5(U)={P in Residual_4(U): C0 subset S_P}`, capacity 15, where `C0` is
   the fixed `(K-1)`-coordinate core at the pinned PR #890 head.

Call the resulting owner `O0(U)`. The inherited theorem and source-generated
capacity arithmetic give `|O0(U)|<=T-1`.

Restrict the post-owner residual to the single branch
`(31,15,6,3,1,0), f64=26`. In this branch define pairwise disjoint sets:

- `R0(U)`: source A-rank `14,646`, exact-F rank greater than `4,152,808`;
- `R1(U)`: source A-rank `14,647`;
- `R2(U)`: source A-rank `14,648`;
- `R3(U)`: source A-rank `14,649`, exact-F rank at most `665,301`.

Put `R_flow(U)=R0(U) disjoint-union R1(U) disjoint-union R2(U)
disjoint-union R3(U)`. If `x_F(U)` is the actual stage-4 occupancy, set

`d_F(U)=20,764,040-x_F(U)` and `d_0(U)=(T-1)-|O0(U)|`.

Then

`|R_flow(U)|-1 <= d_F(U) <= d_0(U)`,

and therefore

`|O0(U)|+|R_flow(U)| <= T`.

This is an abstract cardinality matching to generic unused stage-4 capacity
units plus one allowance vertex. It does not assign a residual polynomial to
a source-incidence-compatible fixed-F bucket.

The prefix through key `(14,649,665,300)` leaves four stage-4 vacancies. At
most one candidate at `(14,649,665,301)` uses the allowance. The next
worst-case unpaid key is `(14,649,665,302)`.

Source A-rank `14,646` is ordinary lexicographic rank `592,047` inside its
exact profile. It is not rank `14,646` in unrestricted lexicographic
`31`-subsets of `64`. Exact-F ranks are one-based ordinary lexicographic ranks
among `26`-subsets of the relevant `33`-label complement.

## Proof

After 31 complete agreement blocks, each listed candidate has
`a=m-31B=100,239` remaining agreements, while two distinct candidates share
at most `b=K-1-31B=32,767` of them.

For a fixed 25-block core, 12 candidates on `8B=262,144` points force
`2,190,032` pair collisions, greater than
`binom(12,2)b=2,162,622`. Thus the local cap is 11. For a fixed 26-block core,
six candidates on `7B=229,376` points force `514,740` pair collisions, greater
than `binom(6,2)b=491,505`. Thus the exact-F cap is five.

The pinned congruence-cover recurrence gives
`L_{5,2}(33,23,20)=647,885` and `L_{3,1}(33,24,22)=721,232`. The fixed-27
deficit is `938,574`, giving exact-A cap `432,442`; the fixed-26 deficit is
`1,600,404`, giving exact-A cap `5,812,512`.

The source dyadic census gives profile counts `6,684,672`, `7,833,600`, and
`783,360`. Replaying the inherited source compiler gives subtotal
`274,847,747,040,605,072`. The first three appended charges and the scalar
packet leave exactly `20,764,040=5*4,152,808` units for stage 4, so the
exact-F prefix is derived rather than selected independently. The endpoint
identity

`3*5,812,512 + 5*665,301 - 1 = 20,764,040`

then derives terminal F-rank `665,301`.

Because `R0(U)` and the occupied stage-4 buckets are disjoint subsets of the
same exact-A cell,

`|R0(U)|+x_F(U) <= 5,812,512`.

The other three branch-local caps give

`|R_flow(U)| <= 3*5,812,512 - x_F(U) + 5*665,301`.

Subtracting one and using the endpoint identity yields
`|R_flow(U)|-1<=d_F(U)`. Any unused capacity in earlier stages only increases
`d_0(U)`, so `d_F(U)<=d_0(U)`. Adding the allowance proves the statement.

## Replay record

The Python-standard-library verifier reconstructs the two collision caps, the
two congruence-cover bounds, all three profile counts, the recursive source
A-pattern, its profile-restricted lexicographic rank, the inherited subtotal,
the exact-F prefix, the terminal key, and all endpoint margins. The inherited
compiler is hash-pinned and executed as source rather than replaced by a
transcribed subtotal.

Normal Python and `python -O` match the checked-in expected output exactly.
Seven semantic mutations are caught: A-order, rank domain, both collision
caps, recurrence, owner total, and residual identity.

## Nonclaims

This theorem does not bound the full list, the complete complement
`L(U)\O0(U)`, or any source cell after `(14,649,665,301)`. It does not assert
endpoint attainment, construct a source-incidence payment map, prove the full
Role-10 Hall flow, close the rank-16 parent, prove an all-rank or asymptotic
theorem, Grand List, Grand MCA, or either official prize theorem. The
replacement owner through `O0` is inherited. The official score remains
`0/2`.

## Remaining wall

The first exact arithmetic wall is source key `(14,649,665,302)`, which
overflows the generic vacancies plus allowance by five. A continuation must
either pay that cell with a new source-valid owner/add-back mechanism or
replace cardinality accounting by a genuine source-incidence theorem, and
then control every later residual cell.
