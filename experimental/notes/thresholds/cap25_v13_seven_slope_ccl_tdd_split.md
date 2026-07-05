# CAP25 v13 seven-slope CCL/TDD split

Status: PROVED / AUDIT / EXACT_NEW_WALL.

This note records a compact branch split for the deployed CAP25 v13 row.  It is
not a CAP25 closure and does not prove the residual numerator bound.  Its role
is to separate seven retained slopes into either a small common-code-line
residual cell or a genuine triple-distance-defect branch.

## Deployed row

Work over

```text
F = F_{17^32},   H = mu_512,   C = RS[F,H,256].
```

Thus `n = 512`, `k = 256`, and the Reed-Solomon minimum distance is

```text
d(C) = n - k + 1 = 257.
```

At agreement `A = 384`, write `j = n - A = 128`.

Let `gamma_1,...,gamma_7` be seven distinct finite retained slopes.  For each
`i`, suppose

```text
y_i = f_0 + gamma_i f_1 = c_i + e_i,
c_i in C,
E_i = supp(e_i),
|E_i| = 128.
```

The retained full-rank split-locator hypotheses are used only to justify these
exact degree-128 split supports.  The proof below uses the displayed
decompositions, distinct finite slopes, and the RS minimum distance.

## The split

For each triple define the affine-collinearity defect

```text
Delta_ijk =
  (gamma_j - gamma_k)c_i
  + (gamma_k - gamma_i)c_j
  + (gamma_i - gamma_j)c_k.
```

Then

```text
Delta_ijk in C.
```

The same affine combination kills the received affine line:

```text
(gamma_j - gamma_k)y_i
+ (gamma_k - gamma_i)y_j
+ (gamma_i - gamma_j)y_k = 0.
```

Therefore

```text
Delta_ijk =
-[(gamma_j - gamma_k)e_i
  + (gamma_k - gamma_i)e_j
  + (gamma_i - gamma_j)e_k],
```

and hence

```text
supp(Delta_ijk) subset E_i union E_j union E_k.
```

If some `Delta_ijk` is nonzero, then it is a nonzero codeword of `C`, so

```text
257 <= wt(Delta_ijk) <= |E_i union E_j union E_k|.
```

This is the triple-distance-defect branch:

```text
TDD257:
  some Delta_ijk != 0 with
  supp(Delta_ijk) subset E_i union E_j union E_k.
```

The inequality `|E_i union E_j union E_k| >= 257` is the minimum-distance
consequence, not the definition.

Now suppose no `TDD257` occurs, so all `Delta_ijk` vanish.  Fix
`gamma_1 != gamma_2` and set

```text
q = (c_2 - c_1)/(gamma_2 - gamma_1),
p = c_1 - gamma_1 q.
```

Then `p,q in C`, and `Delta_12m = 0` gives

```text
c_m = p + gamma_m q
```

for every retained slope.  Thus all seven decoded words lie on one affine RS
code-line.

Subtract this code-line:

```text
a = f_0 - p,   b = f_1 - q,
W = supp(a) union supp(b),   w = |W|.
```

For each retained slope,

```text
e_i = a + gamma_i b,   |supp(e_i)| = 128.
```

At any coordinate `x in W`, the equation

```text
a(x) + gamma b(x) = 0
```

has at most one finite solution `gamma`, since `(a(x),b(x)) != (0,0)`.  Hence a
coordinate of `W` can cancel for at most one of the seven retained finite
slopes.  Therefore

```text
7(w - 128) <= w,
```

so

```text
w <= 149.
```

This is the common-code-line branch:

```text
CCL_149:
  c_i = p + gamma_i q for all seven retained slopes, and
  |supp(f_0 - p) union supp(f_1 - q)| <= 149.
```

Therefore:

```text
seven retained full-rank degree-128 split slopes at A=384
imply CCL_149 or TDD257.
```

## CCL_149 common-GCD repair

Inside the `CCL_149` branch, the seven finite slopes also force a common
error-locator factor.  Keep the notation above and define

```text
E_i = supp(a + gamma_i b),     W = supp(a) union supp(b),     w = |W|.
```

Let

```text
Z_i = W \ E_i = {x in W : a(x) + gamma_i b(x) = 0}.
```

For distinct finite slopes, the sets `Z_i` are pairwise disjoint: if the same
`x in W` canceled for both `gamma_i` and `gamma_j`, then subtracting the two
linear equations gives `b(x)=0`, and hence also `a(x)=0`, contradicting
`x in W`.  Since `E_i subset W` and `|E_i|=128`,

```text
|Z_i| = w - 128.
```

Therefore

```text
|E_1 cap ... cap E_7|
  = w - sum_i |Z_i|
  = w - 7(w - 128)
  = 896 - 6w.
```

In particular, the `CCL_149` inequality `w <= 149` gives

```text
|E_1 cap ... cap E_7| >= 2.
```

Equivalently, if

```text
L_i(X) = prod_{x in E_i}(X - x)
```

are the monic error-root locators, then

```text
deg gcd(L_1,...,L_7) >= 2.
```

This is a repair of the branch ledger, not a payment of `TDD257`.  It says that
the common-code-line side is already charged once the ledger includes the
all-seven common error-locator divisor `ALL7_COMMON_GCD_2`.

## Sharpness and reality of the two branches

The bound `149` is sharp for this cancellation argument.  Choose a 149-point
set `W subset H`, partition 147 of its points into seven disjoint 21-point
blocks `G_i`, and leave two points unused.  Taking a residual pair `(a,b)` with
`b=1` on `W` and `a=-gamma_i` on `G_i` gives seven slopes whose residual
supports have size `149 - 21 = 128`.

The common-GCD bound is sharp for the same example: the two unused points in
`W` are precisely the common intersection `E_1 cap ... cap E_7`, so the forced
common error-locator divisor has degree exactly `2`.

The `TDD257` branch is also real.  For any 257-point set `U subset H`, let
`K in C` be a minimum-weight RS codeword supported on `U`; equivalently, take a
degree-255 polynomial vanishing on `H \ U`.  One can define a received affine
line so that six selected slopes decode to `0`, one selected slope decodes to
`K`, and every selected residual support has size 128.  Then a triple involving
two zero-decoded slopes and the `K`-decoded slope has nonzero defect supported
on `U`, so the triple union has size exactly 257.

Thus `TDD257` is not a cosmetic support-count artifact.  It is the first
surviving branch after the seven-slope common-code-line split.

## Relation to existing CAP25 v13 branches

The existing CAP25 v13 tangent/common-code-line cell does not already pay the
`CCL_149` branch at `A=384`.  That cell requires

```text
3(n-A) <= n-k.
```

Here `n-A = 128` and `n-k = 256`, so `3(n-A) = 384 > 256`.

The SPI deficiency-one eliminant framework supplies the surrounding top-chart
context, but it does not contain the seven-slope `CCL_149` / `TDD257`
dichotomy.

## Remaining wall

After the common-GCD repair, the `CCL_149` side is no longer a primitive
surviving branch once `ALL7_COMMON_GCD_2` is charged.  The next exact target is:

```text
CAP25-v13 TDD257-PAYMENT-OR-EXCLUSION.
```

Equivalently, the remaining wall is the nonzero triple-distance-defect side:

```text
TDD257.
```

One must prove that, after rank-drop, low-chart, strict-contained, quotient,
subfield, common-GCD, identically-split, `CCL_149`, and `ALL7_COMMON_GCD_2`
removals, every surviving seven-slope packet with a nonzero defect `Delta_ijk`
is already paid by an existing branch, or else give a new explicit TDD257
support/image ledger with deduplicated contribution at most the deployed
budget.

## Non-claims

This note is not an official prize solve.  It is not protocol soundness
failure.  It is not ordinary list decoding unless separately proved.  It does
not determine the exact `delta_C^*`.  It does not refute Paper B's corrected
positive theory above its full reserve.  It is not evidence that no reserve
theorem exists.  It is not a reason to ignore the distinctions between
`q_gen`, `q_line`, `q_code`, and `q_chal`.
