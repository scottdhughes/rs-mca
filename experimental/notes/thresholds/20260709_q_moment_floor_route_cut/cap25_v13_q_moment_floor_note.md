# CAP25 v13 row-sharp Q: mass-sensitive moment floor and orbit route cut

Status: **BANKABLE_LEMMA / ROUTE_CUT / PR_READY narrow note**
Scope: `def:q-row-atom`, `prob:row-sharp-q`, and the finite moment route through `thm:moment-q` / `prop:moment-sandwich` in `grande_finale.tex`.

## Claim

Let a prefix or first-match residual Q family have counts `N(z)` over prefix values `z in B^w`. Normalize against the full-row average

\[
\overline N=\binom n m |B|^{-w},\qquad R(z)=N(z)/\overline N,
\]

and define the normalized moment

\[
\Gamma_r=|B|^{-w}\sum_z R(z)^r.
\]

Suppose the residual family is constant on a symmetry orbit `O(z)` of length `L(z)`; for the full multiplicative prefix fibers this is the twist orbit of `prop:twist-orbit`, with

\[
L(z)=n/s(z),\qquad s(z)=\gcd(n,\{j:z_j\ne0\}).
\]

Then, for every integer `r >= 2`,

\[
\Gamma_r\ge {L(z)\over |B|^w} R(z)^r.
\]

Consequently any moment-only proof of the row atom bound `R(z) <= 2^Delta` from an upper estimate `Gamma_r <= G_r` must satisfy

\[
\log_2 G_r+w\log_2|B|-\log_2L(z)\le r\Delta. \tag{1}
\]

If the only available structural input is that the residual family has total normalized mass fraction

\[
\theta={\sum_zN(z)\over\binom n m},
\]

then the Holder lower bound `Gamma_r >= theta^r` gives the necessary best-case floor

\[
 r\ge {w\log_2|B|-\log_2L(z)\over \Delta-\log_2\theta}. \tag{2}
\]

For the full, unpruned prefix fibers `theta=1`. For non-equivariant first-match pruning there is no legitimate orbit gain, so take `L(z)=1` unless equivariance of the residual assignment is separately proved.

## Proof

The orbit contribution alone gives

\[
\Gamma_r
=|B|^{-w}\sum_yR(y)^r
\ge |B|^{-w}\sum_{y\in O(z)}R(y)^r
=|B|^{-w}L(z)R(z)^r,
\]

because `R` is constant on the orbit. If a moment theorem proves `Gamma_r <= G_r`, rearranging gives

\[
R(z)\le \left({G_r|B|^w\over L(z)}\right)^{1/r}.
\]

To force `R(z)<=2^Delta`, inequality (1) is necessary. If only the residual mass fraction `theta` is known, convexity gives the sharp lower bound

\[
\Gamma_r=|B|^{-w}\sum_zR(z)^r\ge
|B|^{-w}\cdot |B|^w\left({\sum_zR(z)\over |B|^w}\right)^r
=\theta^r,
\]

and substituting `G_r >= theta^r` into (1) gives (2).

## Active-row arithmetic

Using the live rows in `CURRENT_STATE.md` and `grande_finale.tex`, with `n=2^21`, `k=2^20`, `K=k+1` on MCA rows and `K=k` on list rows:

| row | w | ceil average | B* | Delta bits | full-fiber r floor | theorem-facing orbit length | orbit floor |
|---|---:|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA | 67471 | 57198030366 | 274980728111395087 | 22.196861710167 | 94196 | 2097152 | 94195 |
| KoalaBear list | 67471 | 65065153468 | 274980728111395087 | 22.010942085180 | 94991 | 2097152 | 94990 |
| Mersenne-31 MCA | 67447 | 1752700 | 16777215 | 3.258852879284 | 641593 | 1 | 641593 |
| Mersenne-31 list | 67447 | 1993678 | 16777215 | 3.072999572381 | 680397 | 1 | 680397 |

Interpretation:

* The multiplicative KoalaBear twist orbit saves only one moment order at the active rows.
* The Mersenne-31 line-round binding row is an x-coordinate twin-coset row, not a multiplicative subgroup row for `prop:twist-orbit`; no multiplicative orbit gain is available in the theorem-facing Q statement unless a separate Chebyshev-equivariant prefix action is proved. The safe value is `L=1`.
* Even a hypothetical full orbit of length `2^21` for the Mersenne-31 list row would only reduce the floor from `680397` to `680390`, so orbit amplification is not a finite solution mechanism.

For the binding Mersenne-31 list row with no orbit gain, the residual mass fraction needed before selected moment orders could possibly fit is:

| r | required log2(theta) upper bound |
|---:|---:|
| 2 | -1045425.426977771916 |
| 3 | -696949.260318657150 |
| 4 | -522711.176989099768 |
| 10 | -209082.626995896484 |
| 100 | -20905.496999974504 |
| 1000 | -2087.784000382307 |
| 10000 | -206.012700423087 |
| 100000 | -17.835570427166 |
| 200000 | -7.381285427392 |
| 500000 | -1.108714427528 |
| 680397 | 0.000003953714 |

Thus a `100000`-moment theorem could fit the binding row only if first-match removals had already reduced the residual Q mass below about `2^-17.8356`, and fixed or low moments would require astronomically small residual mass. This does not prove row-sharp Q; it rules out a class of finite proof shortcuts unless they print a residual mass deletion or a direct max-fiber certificate.

## Nonclaims

This note does **not** prove `U(a0+1) <= B*` for any deployed row. It does **not** prove the row-sharp Q atom. It does **not** assert that the Mersenne-31 x-coordinate prefix problem has a twist orbit. It only gives the exact finite accounting that any moment/orbit route must satisfy before it can be read as a row-sharp Q certificate.

## PR recommendation

Open as a narrow audit note under `experimental/` if the repository wants route cuts in-tree. Suggested title:

> `experimental: mass-sensitive moment floor for row-sharp Q`

Suggested bullet claims:

* Adds the orbit-amplified moment criterion with explicit residual-mass parameter `theta`.
* Replays the four active v13 row constants and shows orbit amplification does not materially lower the finite moment hierarchy.
* Records that the Mersenne-31 list binding row has no theorem-facing multiplicative orbit gain under the present hypotheses.
* Nonclaim: no finite adjacent safe row is proved.
