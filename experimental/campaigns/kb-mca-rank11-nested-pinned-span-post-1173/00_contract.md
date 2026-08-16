---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804
included_predecessor_packet: kb-mca-rank11-factor-synchronization-v1
status: PROVED_STRUCTURAL_MASS_SYNCHRONIZATION_AND_NESTED_PINNING_ROUTER
active_v4_ledger_movement: 0
---

# Contract

This is a one-commit successor to PR #1173 at exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.  The commit incorporates the
weighted factor-synchronization packet and then sharpens its weighted terminal
to one nested coordinate/direction flag.

The first stage proves that an unsafe line has at least `27,749` immediate
dimension-two or dimension-three parent spaces, each with `42,448` common
actual anchor coordinates, together with the pair/triple/quadruple
synchronization and weighted loads recorded in
`kb-mca-rank11-factor-synchronization-v1`.

The new stage uses the legal anchored-rich-flat cell

```text
tau = 1,937
h   = 36,775
q   = h+1 = 36,776
```

whose complete transverse envelope is

```text
rank-one groups         37,134,751,224,667,296
rank-two groups         96,528,283,806,245,790
anchor pair                            983,041
high-margin tail         55,014,741,040,782,366
near-rational add-back                  134,944
-------------------------------------------------
total                   188,677,776,072,813,437
budget                  274,980,728,111,395,087
slack                    86,302,952,038,581,650
```

Thus an unsafe line has at least

```text
L = 86,302,952,038,581,651
```

distinct slopes in nontransverse row-space packets.  Route each packet
canonically to an immediate parent `W` of dimension two or three and choose
one `q`-subset of its common actual anchor-zero set.

A weighted greedy argument now produces a *single nested coordinate chain*

```text
T_1 < T_2 < ... < T_10,   |T_k|=k,
```

and nested parent families.  If `V_k` is the sum of the parents containing
`T_k`, then

```text
V_10 <= ... <= V_2 <= V_1 <= C',
T_k is a common-zero set of V_k,
```

and the exact assigned slope loads and dimension floors are

```text
k   assigned load             dim(V_k) at least
1   2,843,853,816,476,423      8
2      93,708,171,878,891      7
3       3,087,708,134,499      6
4         101,738,094,101      5
5           3,352,119,806      3
6             110,444,488      2
7               3,638,792      2
8                 119,884      2
9                   3,950      2
10                    131      2
```

The dimension conclusions use the exact affine RS pair-list caps at
`A=1,114,111`, the fixed-pair owner multiplier `983,041`, and the actual
sextic field guard through dimension ten.

## Quantifier and ownership

Uniform over the deployed sextic KoalaBear line field, every received pair,
every selected post-near affine-error-rank-eleven family, every explanation
direction space of dimension at most ten, and the actual minimizing-pair and
anchor choices frozen by the predecessor stack.

All loads count distinct finite affine slopes.  The anchor-relative row-space
packets are disjoint.  Immediate parents are chosen deterministically and
merged before charging.  The nested parent families are obtained only by
restriction, so no slope is duplicated.

## Exact impact

- upgrades weighted factor synchronization to a nested source-level
  coordinate/direction flag;
- forces a dimension-at-least-eight common-root direction family on one actual
  coordinate;
- forces dimensions at least seven, six, and five on nested two-, three-, and
  four-coordinate common locators;
- makes zero active-v4 ledger movement;
- does not pay rank eleven or close KoalaBear.
