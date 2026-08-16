# Frontier map

## Exact parent

Nested pinned-span head `42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08`, itself a one-commit successor to PR #1173
head `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

## Imported terminal

The parent supplies nested coordinate sets

```text
T_1 subset ... subset T_10
```

and nested direction spaces with the certified load/dimension table.  It
proves that every polynomial in the `k`th direction space vanishes on `T_k`,
but it deliberately stops before asserting that these pins can be used as
actual MCA shortening coordinates.

## New theorem

For a bad slope `gamma`, let `A_gamma` be the complete agreement domain of its
selected scalar explanation.  The original exact bad support is contained in
`A_gamma`; therefore `A_gamma` itself cannot be simultaneously explained by
a codeword pair.

Choose one polynomial pair `(p_0,p_1)` of degree `<10` interpolating the
received pair on `T_10`.  For each prefix `T_k`, subtract this pair, divide by
the squarefree locator `L_k`, and delete `T_k`.  Every shortened simultaneous
pair explanation lifts to an original pair explanation on `A_gamma`,
including `T_k`, which is impossible.

This gives ten actual shortened support-wise MCA families with unchanged
slopes and unchanged direction dimensions.

## Exact successor terminal

The first shortened row contains at least `2,843,853,816,476,423` bad slopes
and a quotient direction space of dimension at least eight.  The fourth
contains at least `101,738,094,101` bad slopes in dimension at least five.
The tenth still contains 131 bad slopes in dimension at least two.

## Next joint

Apply the relative-order-32, correction-space, or Sylvester/Wronskian
machinery to these genuine quotient families.  The next result must use the
compatible quotient relation

```text
(X-x_(k+1)) * V'_(k+1) <= V'_k
```

rather than treating the ten rows as unrelated local certificates.
