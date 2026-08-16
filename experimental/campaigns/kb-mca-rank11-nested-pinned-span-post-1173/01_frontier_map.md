# Frontier map

## Exact parent

PR #1173 head `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

## Included first stage

The included weighted factor-synchronization packet converts the predecessor's
nontransverse residual into disjoint immediate parents of dimension two or
three.  One profile retains `42,448` common coordinates per parent and forces
at least `27,749` parents, with exact intersection and weighted-incidence
moments.

## New joint

The weighted incidence theorem previously selected a useful coordinate set
separately for each cardinality.  That loses compatibility between successive
cancellations.

The new theorem retains the conditioning history.  Starting with all residual
parent load, choose one coordinate of maximum incident load.  Restrict to the
parents containing it, choose a second coordinate of maximum conditional load,
and continue.  Because every parent begins with exactly `q` selected common
zeros, the conditional average at step `j` is exactly

```text
(q-j)/(m-j).
```

This produces one nested chain rather than unrelated pins.

## Dimension extraction

For the parent sum-space `V_k`, every assigned pair lies in one affine product

```text
(a_0+V_k) x (b_0+V_k).
```

If `dim V_k=r`, the ordinary affine RS list cap is

```text
M_r=floor(C(n-K+r,r)/C(A-K+r,r)).
```

The proved sub-square interleaving collapse bounds ordered pair types by
`M_r`; each pair type owns at most `n-A` slopes.  Comparing the nested loads
with `(n-A)M_r` gives the dimension ladder `8,7,6,5,3,2`.

## Successor terminal

The strongest next theorem should cancel the nested locator chain once, with
one source-bound first-match owner.  In particular, the one-coordinate family
has more than `2.84e15` slopes and direction dimension at least eight.  A
per-parent or per-coordinate independent charge remains forbidden.
