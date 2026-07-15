# Hostile audit 3: the original `mu_64` distance-seven gap-orbit census

## Verdict

```text
ORIGINAL OPTIMIZED REPLAY: BYTE-IDENTICAL PASS
STRUCTURALLY INDEPENDENT FULL CENSUS: PASS
DISJOINT SIZE-SEVEN EQUAL-(e1,e2) TRADE: NONE
MINIMUM ALIGNED INTERSECTION: 3
OFFICIAL SCORE CLAIM: NONE
```

The exact artifact audited here is

```text
work/explore_mu64_distance7_trade_orbits.py
SHA-256 627c01aeaa4d92b75d59611f05c7ce4ca3683c980f64878e3fc81a3fefc2a8de
```

with frozen stdout

```text
work/MU64_DISTANCE7_TRADE_ORBITS_EXPLORATION_OUTPUT.txt
SHA-256 b67a2b22536c25e09ff886b7de27befdff5fe54ab37177f8305b5f122f5b7b2f
```

The claimant-specific record digest is

```text
51f6e031f54258d177cb69fc5374abfdeb01d7f47c3846c09079a9934c77e232.
```

## 1. Completeness of cyclic-gap canonicalization

Every rotation orbit of a seven-subset of `Z/64Z` is free.  If a nonzero
translation stabilized such a subset, the translation cycles would have
power-of-two length greater than one, so an invariant subset would have even
cardinality.  This contradicts cardinality seven.

Each free orbit has exactly seven rotations containing exponent zero, one
for each selected exponent.  Their positive cyclic gap words are exactly the
seven cyclic rotations of one length-seven composition of 64.  The least
lexicographic rotation is unique: equality with a nontrivial rotation would
make the gap word periodic; because seven is prime, this would force all gaps
equal to `64/7`, impossible.  Therefore the claimant keeps exactly one member
of every orbit.  The forced count is

```text
binom(64,7)/64 = binom(63,6)/7 = 9,706,503,
```

which is exactly the completed count.

## 2. Moment equations and bucket sufficiency

Write

```text
s1(A)=sum_(a in A) a,
p2(A)=sum_(a in A) a^2.
```

Rotation by `zeta^k` sends `(s1,p2)` to
`(zeta^k s1,zeta^(2k)p2)`.  Hence

```text
(s1^64,p2^32)
```

is a necessary orbit invariant.  It is deliberately only a coarse bucket;
the program never treats it as a sufficient equality test.

For nonzero `s1`, equality of the first bucket coordinate makes the ratio of
the two first moments a unique element of `mu_64`, and the program then checks
the aligned second power sum literally.  When `s1=0,p2!=0`, equality of the
second coordinate gives the two possible lifts from `mu_32` to `mu_64`, both
of which are checked.  When both moments vanish, all 64 shifts are checked.
Thus no alignable cross-orbit pair can be omitted by the bucket.

The source target uses `(e1,e2)`, not a literal product of all seven values.
The program's `(s1,p2)` test is exactly equivalent because the deployed
characteristic is odd and

```text
p2=e1^2-2e2.
```

## 3. Cross-orbit and self-orbit coverage

Within each invariant bucket, insertion against every prior record checks
every unordered pair exactly once.  The literal rotation is applied to the
second 64-bit mask, and bitwise intersection is tested after both field
moments pass.

Self-orbit trades are also exhaustive.  If `s1!=0`, equal first moments force
shift zero.  If `s1=0,p2!=0`, only the half-turn can survive.  If both vanish,
all 63 nonidentity shifts are tested.  The independent census below in fact
finds zero first-moment orbits, but the original exceptional branches are
correct even without using that fact.

The original coarse buckets contain 52,083 record pairs.  Exact realignment
retains 51,975 of them, so the 108 coarse false collisions are filtered rather
than silently accepted.  No cross-orbit or self-orbit disjoint pair survives.

## 4. Direct replay of the original

An optimized bundled-Python replay produced stdout byte-identical to the
frozen claimant output:

```text
canonical_orbits=9,706,503
invariant_keys=9,698,491
invariant_collision_pairs=52,083
exact_rotated_collision_checks=51,975
cross_orbit_disjoint_trades=0
self_orbit_disjoint_trades=0
record_digest=51f6e031f54258d177cb69fc5374abfdeb01d7f47c3846c09079a9934c77e232
```

Replay stdout:

```text
work/HOSTILE_AUDIT2_MU64_DISTANCE7_ORIGINAL_OPTIMIZED.out
SHA-256 b67a2b22536c25e09ff886b7de27befdff5fe54ab37177f8305b5f122f5b7b2f
```

## 5. Structurally independent full replay

The independent program

```text
work/search_profile1792_h5191_size7_orbit_keys.py
SHA-256 51e24b93d60899cd4d75f99bc9252a9ad0e11ddbfc2c772c0d220f654d462b7a
```

does not use cyclic gaps, the claimant's representative, its coarse key, or
its record ordering.  It selects the unique rotation whose exponent sum is
zero, computes `e2` by Newton's identity, and uses the complete key

```text
(e1^64,e2/e1^2).
```

The full replay byte-matched its expected stdout and returned

```text
normalized_orbits=9,706,503
zero_first_moment_orbits=0
duplicate_key_groups=651
group histogram=560*{13}+90*{14}+1*{15}
aligned pairs=560*C(13,2)+90*C(14,2)+C(15,2)=51,975
minimum aligned intersection=3
result=NO_DISJOINT_TRADE.
```

Its independent table and aligned-pair digests are

```text
73d3dac37586a1570715b62954838731e6438d91d5444b78b0fc5e7bc4d4d84d
49293bad9940e67b3659a59ce020fb619566b6f2d86489ea8bd78f93f7db09dd.
```

Replay stdout is frozen at

```text
work/HOSTILE_AUDIT_REPLAY_PROFILE1792_H5191_SIZE7_ORBIT_KEYS.out
SHA-256 bfb26410dbca847f45838e93a5f0a38135f540f3a17e70c732146e86c024d574.
```

An additional independent anchored-minimum-mask implementation computes
`e2` from all 21 literal pair products and reports the same 51,975 pairs,
minimum intersection three, and zero disjoint pairs.  Its frozen audit is
`HOSTILE_AUDIT2_PROFILE1792_H5191_DISTANCE7_TRADE_EXCLUSION.md`.

## Scope

The finite theorem

```text
no disjoint A,B subset mu_64, |A|=|B|=7,
with e1(A)=e1(B), e2(A)=e2(B)
```

is accepted.  Through the separately audited Profile-1792 compiler this pays
the single `h=5,191` continuation row.  It is not an official-question proof
and does not move the official score by itself.
