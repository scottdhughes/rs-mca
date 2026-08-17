# Rank-twelve dimension-matched proper-drop wall

## Exact parent and scope

This packet is stacked on the uniform rank-one repair at exact parent
`8911e26e78c8d91173c413f079a13f88a04701fe`.

It is a route cut, not a payment.  It proves that an affine-error-rank-12
family cannot make its first proper rank-two drop at any ambient dimension
`K>=262,712`.  The first surviving cell is `K=262,711`, where the numerical
gap is exactly three slopes.  It moves no active-v4 ledger atom and does not
claim KoalaBear closure.

## Dimension-matched comparison

The source-bound descent supplies a rank-two explanation family of

```text
L_2 = 5,170,912
```

slopes.  At ambient dimension `K`, a proper complete-core drop guarantees

\[
I_2(K)=\left\lceil
\frac{L_2(67{,}472+K)-C_2(K)}{1{,}048{,}576+K}
\right\rceil
\]

rank-at-most-one slopes and shortens them into residual dimension `k=K-1`.
The comparison must therefore use a rank-one cap at that same `k`, not the
global maximum over all residual dimensions.

## Heavy/light stability lemma in the active window

Fix `k>=262,710`, put

\[
n=1{,}048{,}576+k,\quad m=67{,}472+k,\quad
q=\lfloor m/2\rfloor,\quad A=m-q-1.
\]

Call a weighted coordinate-line class heavy when its global weight exceeds
`q`.  If the heavy classes have effective outside deficiencies `b_i`, the
usual global resource argument gives

\[
H\le\binom h2+V\sum_i\frac1{b_i},\qquad
V=n-hm+\sum_i b_i.
\]

Coordinatewise convexity reduces the maximum to `b_i in {1,A}`.  An exact
scan of every `k` in the active window proves:

- the unique high extremal profile is `h=2`, `b_1=b_2=1`;
- every other high profile contributes at most `981,105` points;
- the light-only cross-pair cap is at most `31`.

For the extremal profile, the two heavy lines each have weight at least
`m-1`.  Let `U` be the total nonheavy weight and `c` its number of line
classes.  Points on the heavy lines are at most `1+2c`.

If there is at most one light point, the total is at most

\[
2V+2,
\qquad V=n-2(m-1).
\]

If there are at least two light points, their incident coordinate sets share
at most one line class.  Since their union has weight at most `V`, the shared
class has weight at least `2m-V`, and therefore

\[
V-c\ge2m-V-1.
\]

Combining `1+2c` with the exact cross-pair light cap is strictly smaller in
the active window.  Hence the dimension-matched rank-one cap is

\[
M_1(k)=\max\{2(1{,}048{,}576-2\cdot67{,}472-k+2)+2,\ 981{,}136\}.
\]

## Exact boundary

The exact all-cell scan gives

```text
ambient K    guaranteed I_2(K)    cap M_1(K-1)    difference
262,710          1,301,844          1,301,852          -8
262,711          1,301,847          1,301,850          -3
262,712          1,301,850          1,301,848          +2
262,713          1,301,853          1,301,846          +7
262,714          1,301,856          1,301,844         +12
```

The difference remains positive for every larger ambient dimension.  Thus a
rank-two family must whole-shorten through all `K>=262,712`; its first
possible proper drop is at `K=262,711`.  There it emits at least `1,301,847`
rank-one slopes against a cap of `1,301,850`.

The unresolved joint is now only

```text
three slopes.
```

## Strongest next theorem

Classify the near-extremal double-star configuration at `K=262,711` using its
source provenance.  The abstract weighted-line arrangement can attain the
local cap, so another pure incidence rounding improvement is not expected.
The missing input must couple the two dominant fixed-pair cores back to the
ambient rank-two family or to the active first-match chronology.
