# L1 Prefix Dual Odd-Moment Hooley-Katz Import Audit

Date: 2026-06-26

## Audited Sources

1. Sudhir R. Ghorpade and Gilles Lachaud, "Etale cohomology, Lefschetz
   Theorems and Number of Points of Singular Varieties over Finite Fields",
   arXiv:0808.2169.

   Source used:

   ```text
   https://arxiv.org/abs/0808.2169
   ```

2. Guillermo Matera, Mariana Perez, and Melina Privitelli, "Explicit
   Estimates for the Number of Rational Points of Singular Complete
   Intersections over a Finite Field", arXiv:1412.7446.

   Source used:

   ```text
   https://arxiv.org/abs/1412.7446
   ```

## Ghorpade-Lachaud Theorem 6.1

The arXiv source labels the main complete-intersection estimate
`MainThm`; in the paper numbering this is Theorem 6.1.

For an irreducible complete intersection `X subset P^N` over `F_q`, of
dimension `n`, codimension `r=N-n`, multidegree `dvec`, and singular locus
dimension at most `s`, it gives

```text
||X(F_q)| - pi_n|
 <= b'_{n-s-1}(N-s-1,dvec) q^{(n+s+1)/2}
    + C_s(X) q^{(n+s)/2}.
```

If `delta=max(d_i)`, the source gives the explicit bound

```text
C_s(X) <= 9*2^r*(r*delta+3)^{N+1}.
```

The primitive Betti number is defined by the source formula

```text
b'_j(M,dvec)
 = (-1)^{j+1}(j+1)
   + (-1)^M sum_{c=r}^{M} (-1)^c binom(M+1,c+1)
       sum_{nu_i>=1, sum nu_i=c} prod_i d_i^{nu_i},
```

where `r=len(dvec)` and `M-j=r`.

## Collision Substitution

For the projective odd-moment collision variety `Y_{d,k}`:

```text
N = 2k-1,
n = 2k-d-1,
r = d,
s = d-2,
dvec = (1,3,5,...,2d-1),
delta = 2d-1.
```

The projective geometry checkpoint proves that, for `k>d` and
`char F_p > 2d-1`, `Y_{d,k}` is geometrically integral and a projective
complete intersection.  Theorem 6.1 therefore applies to full projective
`F_p`-points.

The exponent substitution is

```text
(n+s+1)/2 = k-1,
(n+s)/2 = k-3/2.
```

The exact primitive Betti coefficient is

```text
B_{d,k} = b'_{2(k-d)}(2k-d, (1,3,...,2d-1)).
```

The explicit lower-weight constant is bounded by

```text
C_{d,k} <= 9*2^d*(d(2d-1)+3)^{2k}.
```

This direct presentation is valid but not minimal because the first equation
has degree `1`.  Eliminating `F_1` gives the same projective variety embedded
in `P^{2k-2}` with codimension `d-1` and multidegree

```text
(3,5,...,2d-1).
```

The leading primitive Betti coefficient is unchanged:

```text
b'_{2(k-d)}(2k-d,(1,3,...,2d-1))
 =
b'_{2(k-d)}(2k-d-1,(3,5,...,2d-1)).
```

The lower-weight bound improves to

```text
C_{d,k}^{red}
 <= 9*2^{d-1}*((d-1)(2d-1)+3)^{2k-1}.
```

The verifier records both presentations and treats the linear-eliminated
bound as the operative Ghorpade-Lachaud lower-weight constant.

Thus

```text
||Y_{d,k}(F_p)| - pi_{2k-d-1}|
 <= B_{d,k} p^{k-1} + C_{d,k} p^{k-3/2}.
```

## Affine Cone

The affine homogeneous collision variety is the cone over `Y_{d,k}`:

```text
|X_{d,k}(F_p)| = 1 + (p-1)|Y_{d,k}(F_p)|.
```

Using `1+(p-1)pi_{2k-d-1}=p^{2k-d}`, this gives

```text
||X_{d,k}(F_p)| - p^{2k-d}|
 <= B_{d,k}p^k + C_{d,k}p^{k-1/2}.
```

This is a full-affine estimate only.

## Matera-Perez-Privitelli Theorem 4.5

The arXiv source labels the relevant theorem `th: estimate hooley`; in the
paper numbering this is Theorem 4.5.

For a projective complete intersection of dimension `r`, degree `delta`,
multidegree `dvec`, singular-locus dimension at most `s`, and

```text
D = sum_i (d_i-1),
```

the theorem assumes

```text
q > 2(s+1) D^{r-s-1} (D+r-s) delta
```

and gives

```text
||V(F_q)| - p_r|
 <= (b'_{r-s-1} + 2 sqrt(delta) + 1) q^{(r+s+1)/2}.
```

For the collision family, with projective dimension `r=2k-d-1`,
singular bound `s=d-2`, and degree product

```text
Delta = prod_{j=1}^d (2j-1) = (2d-1)!!,
D = d(d-1),
```

the field-size condition becomes

```text
p >
2(d-1) [d(d-1)]^{2(k-d)}
       (d(d-1)+2(k-d)+1)
       (2d-1)!!.
```

The exponent is favorable, but this field-size threshold is exponential in
`k-d` when `d` is fixed and worse at reserve-scale `d`.

The MPP theorem assumes `0 <= s <= r-2`; therefore the verifier does not apply
it to `d=1`, where `s=-1` and the collision variety is smooth.

## Count-Domain Boundary

The imported theorems count:

```text
FULL_AFFINE_Fp_POINTS
```

after projective-to-affine cone conversion.

They do not directly count:

```text
FULL_TORUS_Fp_POINTS
PROPER_SUBGROUP_H_POINTS
```

For proper subgroups, imposing `2k` coordinate memberships in `H` introduces
multiplicative-character twists.  A usable analogue would require a uniform
twisted Hooley-Katz theorem for the relevant Kummer sheaves or an equivalent
moment-specific character-sum argument.

## Status

IMPORTED / AUDITED:

- Ghorpade-Lachaud Theorem 6.1;
- primitive Betti composition formula;
- original lower-weight bound `9*2^r*(r delta+3)^{N+1}`;
- linear-eliminated lower-weight bound for the degree-one equation;
- Matera-Perez-Privitelli Theorem 4.5;
- MPP field-size condition.

NOT IMPORTED:

- a full-torus boundary theorem;
- any proper-subgroup twisted point-count theorem;
- any replacement for the multiplicative-character estimates.

OPEN:

- whether the GL constants leave reserve-scale margin;
- whether the MPP field-size condition is compatible with polynomial fields;
- twisted proper-subgroup analogues.
