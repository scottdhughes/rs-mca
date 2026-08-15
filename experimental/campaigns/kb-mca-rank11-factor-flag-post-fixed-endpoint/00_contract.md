---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 193b7bf99a5cc7ccea042f25677e698d9f988eee
status: PROVED_STRUCTURAL_ROUTER
active_v4_ledger_movement: 0
---

# Contract

This packet is a one-commit successor to the fixed-endpoint rank-one payment
at exact parent `193b7bf99a5cc7ccea042f25677e698d9f988eee`.
It attacks the first surviving rank-eleven joint: many low-margin minimizing
pairs whose endpoint-difference row spaces need not have pairwise rank one.

Freeze one minimizing pair for every post-near record once, before any cutoff
is chosen.  The parent nonuniform-margin theorem at cutoff `1795` supplies an
actual dense center pair `e_*` with at least `200632` owned slopes and complete
pair-core deficiency at most four.  Choose a fixed `1116044`-subset `G_*` of
that core.

At the new cutoff `tau=1936`, every low-margin pair `e` has a complete pair
core of size at least `1114112`; therefore the two endpoint differences from
`e_*` vanish simultaneously on at least `133004` coordinates of `G_*`.
Their row space is a one- or two-dimensional subcode `U_e` of the fixed
explanation-direction code `C'`, whose dimension is at most ten.

The packet proves a two-level support-flag theorem.  Unless some actual
`U_e` is contained in a three-dimensional subcode of `C'` having at least
`23354` common zeros in `G_*`, all low pair types can be assigned to:

- at most `8415196932` terminal one-dimensional direction containers, each
  carrying at most `15` pair types; or
- at most `382360905` two-dimensional direction containers, each carrying
  at most `255` pair types.

After the exact fixed-pair slope projection, high-margin tail, and disjoint
near-rational add-back, the resulting total is

```text
low-margin family        219,935,524,214,538,240
high-margin tail          55,043,143,075,392,992
near-rational add-back                 134,944
-------------------------------------------------
total                     274,978,667,290,066,176
budget                    274,980,728,111,395,087
slack                           2,060,821,328,911
```

Hence every over-budget affine-error-rank-eleven line forces a source-bound
three-dimensional direction subcode containing an actual pair-difference row
space and sharing at least `23354` deployed zeros inside the dense center core.

## Quantifier

Uniform over the deployed sextic KoalaBear line field, every received pair,
every gauged post-near explanation flat of affine dimension at most ten, and
the globally frozen minimizing-pair selection used by the parent margin
compiler.

## Projection

All counts are distinct finite affine slopes.  Pair types are first assigned
canonically to one direction container.  The parent same-support exception
map bounds every pair type by `n-(m-tau)=983040` slopes.  No per-container or
per-edge charge is summed without a disjoint assignment.

## Exact impact

- replaces an arbitrary rank-two pair edge by a dimension-three common-factor
  direction-subcode terminal;
- forces a squarefree deployed-coordinate factor of degree at least `23354`
  common to every word in that subcode;
- makes zero active-v4 ledger movement;
- does not pay affine error rank eleven or close KoalaBear.
