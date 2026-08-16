---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_pr: 1173
parent_commit: 2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804
status: PROVED_AFFINE_ERROR_RANK_ELEVEN_PAYMENT
active_v4_ledger_movement: 0
---

# Contract

This packet is a one-commit successor to PR #1173 at exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

It proves that the complete KoalaBear affine-error-rank-eleven branch fits the
row budget.  The proof does not sum the rich-flat terminals emitted by #1173.
Instead it returns to the inherited pointwise support-margin resource, double
counts complete minimizing-pair cores, and iterates a source-bound dichotomy:

1. a heavy coordinate is a whole-family pair-core coordinate and the complete
   family shortens without losing a slope or direction dimension; or
2. the heavy incident subfamily has strictly smaller pair-difference direction
   span and shortens to the next rank.

Exact monotonicity over every shortened dimension shows that delaying a rank
drop until the full-code endpoint is the worst case.  The resulting forced
loads are

```text
rank 10  274,980,728,111,260,144
rank  9   17,695,628,624,859,819
rank  8    1,138,737,729,126,327
rank  7       73,278,302,796,469
rank  6        4,715,427,489,703
rank  5          303,431,536,894
rank  4           19,525,148,223
rank  3            1,256,382,675
rank  2               80,843,204
rank  1                5,201,865
```

At the final row `(n,K,m)=(1,048,577,1,67,473)`, a weighted affine-line
argument bounds every pair-noncontained rank-one family by

```text
low-dominant points       483
high-dominant points 4,070,464
--------------------------------
total                 4,070,947.
```

The contradiction has exact slack `1,130,918`.

## Quantifier

Uniform over the deployed sextic KoalaBear line field, every received pair,
every fixed selected post-near affine-error-rank-eleven family, every exact
same-support noncontained record supplied by the predecessor stack, and every
legal sequence of complete-core shortenings and rank drops.

## Exact impact

- post-near affine error rank eleven: paid;
- disjoint near-rational add-back: `134,944`;
- complete affine error rank eleven branch: paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.
