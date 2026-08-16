# 2. Full-row pair-core compiler

Work in `(n,k,m)=(R+k,k,d+k)`.  Freeze each slope to one minimizing pair
`e=(a_e,b_e)`, complete core

\[
 H_e=\{x:r_0(x)=a_e(x),\ r_1(x)=b_e(x)\},
\]

and deficiency `delta_e=max(1,m-|H_e|)`.

Every owned slope has margin at least `delta_e`: on its support, scalar
agreement and `r_1=b_e` force `r_0=a_e`.  For a fixed pair, exception sets
outside `H_e` are disjoint over finite slopes, so one pair owns at most

\[
 R-d+1=981,105
\]

slopes.

Distinct pair types satisfy

\[
 |H_e\cap H_f|\le k-1,
\]

because at least one endpoint difference is a nonzero degree-`<k` polynomial.

Fix `T`, set `h=m-T`, `lambda=k-1`, and let `r` be the number of types with
`delta_e<=T`.  If `d_x` counts low cores containing coordinate `x`, then

\[
 \sum_xd_x\ge rh,\qquad
 \sum_x\binom{d_x}{2}\le\lambda\binom r2.
\]

Cauchy gives

\[
 r(h^2-n\lambda)\le n(h-\lambda).
\]

When the denominator is positive,

\[
 r\le
 \left\lfloor\frac{n(h-\lambda)}{h^2-n\lambda}\right\rfloor .
\]

Low types contribute at most `r*981,105` slopes.  Every high-type slope costs
at least `T+1` units of the pointwise resource, giving

\[
 |Z|\le r(981105)+\left\lfloor\frac{C_k(k)}{T+1}\right\rfloor .
\]

The cumulative compiler additionally intersects the Cauchy prefix with the
guarded ordinary affine pair-list prefix and fills exact deficiency slots in
increasing cost.  This is an integral relaxation because all constraints are
prefix constraints.
