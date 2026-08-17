# Rank-twelve four-block proper-drop payment

## Exact stack boundary

This packet is one successor to exact parent

```text
ea0541ca0cafb49ca79ff48c1285887344e1103b
```

and consumes the common-locator theorem frozen at

```text
ed556ccb7527e1c54e58b8d151ccefd8539000ac
payload edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa
```

It strengthens the parent large-locator interval from `K >= 858,619` to

```text
K >= 662,480.
```

It is a payment of the proper rank-two drop branch in that interval. It does
not pay affine error rank twelve globally, move an active-v4 ledger atom, or
claim KoalaBear closure.

## Exact result

The inherited rank-two family has

```text
L_2 = 5,170,912
```

distinct post-near slopes. For a proper drop, supports meeting the actual
common pair core form one rank-one family and cost at most

```text
4,070,947.
```

For supports avoiding the core, four slopes witness every genuinely
two-dimensional residual. Their omission sets produce four clean projective
fibers. Every further slope is assigned canonically to one of three disjoint
owner types:

1. at least three clean equations: at most four base slopes;
2. exactly two clean equations: one fixed codeword-pair owner;
3. exactly one clean equation: one universal-core-aware correction ray.

There is no identity-triplet branch: the consistency determinant is affine in
the slope and its leading coefficient is a nonzero Vandermonde determinant.

The exact compiler has three regimes:

- `FOUR_SUPPORT_RAY` when four omission sets cannot cover the shortened
  domain;
- `CLEAN_FOUR_BLOCK` when no one-block ray can reach the target;
- `DIRTY_FOUR_BLOCK` when at most two one-block rays can coexist.

The first paying cell is

```text
ambient K                     662,480
effective rank-one k           75,757
common-locator floor          586,723
omission size r               394,381
eta                            58,810
pair/triplet cap              629,630
two-ray cap                   470,330
exceptional cap             1,099,960
rank-one cap                4,070,947
proper-drop total           5,170,907
rank-two load               5,170,912
slack                                5
```

Therefore every proper rank-two drop is impossible for

```text
662,480 <= K <= 1,048,576.
```

The whole rank-two family shortens intact through all `386,097` dimensions
and reaches `K <= 662,479`.

## Adjacent wall

At `K=662,479`, the same floor-safe compiler gives

```text
exceptional cap             1,099,983
proper-drop total           5,170,930
excess over load                    18
```

This is a method wall, not an unsafe certificate. The relaxed extremal profile
contains two active one-block correction rays together with a dominant
fixed-pair owner. The next theorem must couple those owners and save at least
`19` slopes; independently sharpening one owner is unlikely to be enough.

## Replay

```bash
python3 experimental/scripts/verify_kb_mca_rank12_four_block_owner_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_four_block_owner_payment_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank12_four_block_owner_payment_v1.py
python3 experimental/scripts/verify_kb_mca_rank12_four_block_owner_payment_manifest_v1.py
```

The primary verifier checks every deployed ambient cell, exact rational ray
envelopes, finite-field triplet rigidity, and small dirty-incidence
optimizers. The independent audit reconstructs the complete ambient scan with
a separately written implementation.
