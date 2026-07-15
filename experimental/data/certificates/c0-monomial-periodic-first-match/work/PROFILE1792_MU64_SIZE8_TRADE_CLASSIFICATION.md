# Complete deployed-`mu_64` size-eight two-moment trade classification

## Theorem

Let

```text
p=2,130,706,433,
Omega=mu_64 subset F_p^*.
```

If `A,B subset Omega` are disjoint, `|A|=|B|=8`, and

```text
e_1(A)=e_1(B),       e_2(A)=e_2(B),
```

then each of `A` and `B` is a union of two distinct `mu_4` cosets.  In
particular their two moments are both zero.  Conversely, every two disjoint
unions of two `mu_4` cosets give such a trade.

There are exactly

```text
3*binom(16,4)=5,460
```

unordered deployed trades.  The result is an exhaustive finite-field
classification, not a heuristic sample.

## 1. One representative of every rotation orbit

Write an eight-subset in exponent form relative to the deployed primitive
root `zeta=1,548,376,985`.  Starting at one selected exponent, its eight
positive cyclic gaps sum to 64.  Subtracting one from every gap gives a
nonnegative cyclic word

```text
(b_1,...,b_8),       sum b_i=56.
```

Cyclic rotation of this word is exactly multiplication of the subset by an
element of `mu_64`.  The verifier uses the standard prefix-period necklace
recursion: at position `t` it first copies position `t-period`, then branches
over every larger symbol and resets the candidate period to `t`; a leaf is
retained exactly when its sum is 56 and its period divides eight.  Thus one
and only one representative of every rotation orbit is emitted, including
periodic words.

Burnside's lemma independently gives the required orbit count

```text
[binom(64,8)+binom(32,4)+2binom(16,2)+4binom(8,1)]/64
 =69,159,400.
```

The generated count agrees exactly.

## 2. Complete moment keys, including zero branches

For a representative `A`, put

```text
s(A)=e_1(A),       t(A)=e_2(A).
```

Under rotation by `u in mu_64`,

```text
s -> us,       t -> u^2t.                             (1)
```

If `s!=0`, use the invariant key

```text
K(A)=(s(A)^64, t(A)/s(A)^2).                          (2)
```

This key is complete.  Equality of the first coordinate says that
`s(A)/s(B)` is the unique aligning element of `mu_64`; equality of the
second then aligns `t` as well.

If `s=0,t!=0`, use the tagged key `t^32`.  Equal keys give exactly two
alignments in `mu_64`, differing by `-1`, and the verifier checks both.  If
`s=t=0`, every one of the 64 rotations is checked.  All aligned masks are
deduplicated before pair comparison, so nontrivial orbit stabilizers neither
lose cases nor create multiplicity.  A nonzero-first-moment singleton key
cannot contain an untested within-orbit trade, because (1) makes its aligning
rotation unique and equal to the identity.

The exact sorted table has

```text
69,159,400 orbit records,
69,047,318 invariant-key groups,
9,936 repeated groups,
maximum group size 14.
```

After expanding the exceptional alignments, the verifier checks `696,465`
literal aligned unordered mask pairs.

## 3. Exhaustive disjointness and block test

Exactly `5,460` aligned pairs are disjoint.  For each side the verifier tests
all sixteen literal cosets

```text
{zeta^(r+16k):0<=k<4},       0<=r<16,
```

and accepts the block form only when precisely two whole cosets occur and no
partial coset occurs.  Every one of the 5,460 disjoint pairs passes this test;
there are zero exotic pairs.

There are `binom(16,2)=120` two-block unions.  Two such unions are disjoint
exactly when their four block labels are distinct, giving

```text
binom(16,4)*3=5,460,
```

which independently closes the converse count.  Each `mu_4` coset has
`e_1=e_2=0`, so every counted block pair indeed has equal zero moments.

The deterministic sorted-record and aligned-trade digests are

```text
sorted records:
42b987eb5405cc47dbb818380104c66549b7d7f22f4116bdec8e33bd86be7247

aligned trades:
bee467b5c3587a8cf989a6479020a0a189fd7be61a81be4ef56b7c67dab2ec0d
```

## Consequence and nonclaims

In a fixed-low Profile 1792 completion family, every distance-eight edge now
exchanges two selected full `mu_4` blocks with two empty full `mu_4` blocks.
This is the exact analogue of the accepted one-block classification for
distance four.  A separate family/weight argument is still required before
assigning a new layer cap or a root-excess aggregate payment.

This classification alone does not pay an entire source stratum, recurrence
parent, or official question.

## Replay

```text
python3 -B work/census_mu64_size8_two_moment_trades.py --generate-only
python3 -B work/census_mu64_size8_two_moment_trades.py --analyze-only
```

The second command must byte-match
`work/MU64_SIZE8_TWO_MOMENT_TRADE_CENSUS_OUTPUT.txt` on standard output.
