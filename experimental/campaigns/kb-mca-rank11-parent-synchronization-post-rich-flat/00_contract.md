---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804
status: PROVED_STRUCTURAL_ABUNDANCE_AND_PINNING_ROUTER
active_v4_ledger_movement: 0
---

# Contract

This packet is an exact successor to the anchored rich-flat router at parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

The parent pays every `h=42452` transverse row-space group at cutoff
`tau=1547` by

```text
274,978,720,888,758,363
```

against the deployed budget

```text
274,980,728,111,395,087.
```

Therefore an unsafe line has at least

```text
L0 = 2,007,222,636,725
```

low-margin slopes in nontransverse row-space packets.

Each such packet is assigned canonically to an exact-dimensional rich parent:
rank-one packets to a two-dimensional parent and rank-two packets to a
three-dimensional parent. Every parent has a canonical set of

```text
q = 42,453
```

actual anchor-good coordinates on which all of its direction polynomials
vanish. Parent packets are disjoint in slopes.

The exact conclusions are:

1. there are at least `508` distinct rich parents in total;
2. one fixed dimension occurs at least `478` times;
3. among `478` parents of that dimension, two common-zero sets meet in at
   least `1,530` coordinates, three meet in at least `53`, and four meet in at
   least `2`;
4. consequently an unsafe line emits either a direction space of dimension at
   least `3` with a common factor of degree at least `1,530`, or a direction
   space of dimension at least `4` with such a factor;
5. some actual anchor-good coordinate belongs to parent packets carrying at
   least `76,352,112,631` slopes. The span of those parents has dimension at
   least `5` and is divisible by that coordinate locator;
6. some actual two-coordinate set belongs to packets carrying at least
   `2,904,268,266` slopes, and their direction span has dimension at least
   `3`.

## Quantifier

Uniform over the deployed sextic KoalaBear line field, every received pair,
every selected post-near affine-error-rank-eleven family, and the exact
minimizing-pair/anchor selection inherited from the parent packet.

## Projection and ownership

All weights count distinct finite affine slopes. Each nontransverse row-space
packet is assigned once to a canonical parent, and equal parents are merged.
The resulting parent packets remain disjoint. No local factor or slope is paid
more than once.

## Exact impact

This is a structural abundance and factor-synchronization router. It makes
zero active-v4 ledger movement, does not pay error rank eleven, and does not
close KoalaBear.