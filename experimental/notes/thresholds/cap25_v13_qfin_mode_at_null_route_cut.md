# CAP25 v13 Q-fin mode-at-null route cut

Status: COUNTEREXAMPLE / ROUTE_CUT / AUDIT.

This note records a small finite obstruction to the proposed `mode-at-null`
shortcut in the CAP25 v13 Q-fin safe-side program.  It does not prove the
adjacent upper ledger and does not prove

```text
U(1116048) <= B*.
```

Its role is to replace a false null-fiber extremality target with the correct
twist-orbit max-fiber target.

## Live adjacent row

The current committee-facing CAP25 v13/v14 status memo uses the KoalaBear MCA
adjacent pair

```text
unsafe a0 = 1116047,
candidate first safe = 1116048.
```

The finite target remains

```text
U(1116048) <= B* < L(1116047).
```

The exact lower/unsafe side is replayed by the moved-frontier checker.  The
upper/safe side still needs a complete upper ledger.  In particular, the Q-fin
prefix-fiber input remains open after the route cut below.

## The false shortcut

For a multiplicative-coset domain `D = alpha * mu_n`, define the prefix moment
map on `m`-subsets by

```text
Phi_w(M) = (p_1(M), ..., p_w(M)),
p_i(M)  = sum_{x in M} x^i.
```

The shortcut under audit was the null-fiber extremality statement

```text
mode-at-null:  |Phi_w^{-1}(z)| <= |Phi_w^{-1}(0)|  for all z.
```

This is false already for one prefix over a prime-field multiplicative group.

## Exact counterpacket over F_17^*

Let

```text
D = F_17^*,   n = 16,   m = 9,   w = 1.
```

For `s in F_17`, put

```text
N_m(s) = #{ M subset F_17^* : |M| = m and sum_{x in M} x = s }.
```

Using additive characters,

```text
N_m(s)
= (1/17) sum_{lambda in F_17} psi(-lambda s)
  [T^m] product_{x in F_17^*} (1 + T psi(lambda x)).
```

For `lambda = 0`, the coefficient is `binom(16,m)`.  For
`lambda != 0`, multiplication by `lambda` permutes `F_17^*`, so

```text
product_{x in F_17^*} (1 + T psi(lambda x))
= product_{y in F_17^*} (1 + T psi(y))
= (1 + T^17)/(1 + T)
= 1 - T + T^2 - ... + T^16.
```

Thus

```text
N_m(0)      = (binom(16,m) + 16(-1)^m)/17,
N_m(s != 0) = (binom(16,m) - (-1)^m)/17.
```

For `m = 9`,

```text
binom(16,9) = 11440,
N_9(0)      = (11440 - 16)/17 = 672,
N_9(s != 0) = (11440 + 1)/17  = 673.
```

Therefore the maximum fiber is not the null fiber:

```text
max_s N_9(s) = 673 > 672 = N_9(0).
```

The nonzero values form a full primitive twist orbit under `mu_16 = F_17^*`.
So this is not a quotient-stabilized counterpacket; it is a primitive
nonzero-orbit counterpacket to mode-at-null.

## Correct invariant replacement

The true symmetry statement is orbit invariance.  If `zeta in mu_n`, then

```text
M -> zeta M
```

is a bijection on `m`-subsets of `D`, and

```text
p_i(zeta M) = zeta^i p_i(M).
```

Therefore fiber sizes are constant on twist orbits:

```text
|Phi_w^{-1}(z_1, ..., z_w)|
= |Phi_w^{-1}(zeta z_1, ..., zeta^w z_w)|.
```

If

```text
I(z) = { i <= w : z_i != 0 },
```

with the convention `gcd(n, empty set) = n`, then the target-vector stabilizer
has size

```text
|Stab(z)| = gcd(n, I(z)).
```

Primitive values are those with `gcd(n, I(z)) = 1`; they have full twist orbit
size `n`.

This stabilizer is a property of the target vector.  It does not by itself say
that every support in the fiber is a union of quotient cosets.  Stabilized
target orbits still require image-level quotient descent or another explicit
ledger payment.  Raw support-level quotient counting is far above the finite
budget at the deployed adjacent row.

## Corrected Q-fin target

The finite Q-fin input should not be stated as null-fiber extremality.  The
correct replacement is a max-over-orbits certificate:

```text
primitive max-orbit flatness:
  max_{gcd(n,I(z)) = 1} |Phi_w^{-1}(z)|
  <= K_rem * avg,

avg = binom(n,m) / |B|^w,
```

with `K_rem` equal to the exact remaining first-match upper-ledger budget after
tangent, quotient, extension, sparse/M1, L1/list, planted/divisor, and residual
cells are charged.

For nonprimitive target vectors, the required object is not a raw support
bucket.  It is a stabilized-orbit recursion at the image level, with the
per-rung losses printed in bits and replayed by exact integer certificates.

## Non-claims

This note proves only the route cut and the symmetry replacement above.  It
does not prove:

```text
U(1116048) <= B*,
primitive max-orbit flatness at the deployed row,
mode-at-null for any nontrivial Q-fin range,
or quotient payment from target-vector stabilizer alone.
```

The next exact wall is:

```text
CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048.
```

Proving or refuting that wall is the finite Q-fin task left by this route cut.
