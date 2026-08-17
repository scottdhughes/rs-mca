# Uniform weighted-line repair of the rank-eleven descent

## Status and exact parent

This is a successor to exact parent
`d01c546f4dca70e256c18c142873821b3bb48ab5`.

It repairs one omitted terminal branch in the parent global-core descent. It
makes zero active-v4 ledger movement, does not pay affine error rank twelve,
and does not claim KoalaBear closure.

## Gap found by hostile cross-check

The parent descent forces a rank-one explanation family of `5,201,865`
post-near slopes. Its printed endpoint proof shortens that family to ambient
dimension one. At an earlier ambient dimension, however, a heavy core
coordinate can have incident direction span zero, leaving a fixed-pair
subfamily. Exact replay gives only `334,710` to `2,768,286` slopes in that
subfamily, so an endpoint-only fixed-pair argument does not close every branch.

## Uniform theorem

Let a source-bound rank-one explanation family lie in

\[
c_0+\langle P\rangle,
\qquad h_\gamma=c_0+t_\gamma P,
\]

inside a degree-`<K` Reed--Solomon code. At a coordinate `x`, put

\[
E_x(\gamma)=r_0(x)+\gamma r_1(x)-c_0(x).
\]

If `P(x) != 0`, agreement is the affine graph line

\[
t=E_x(\gamma)/P(x).
\]

If `P(x)=0` and `E_x` is nonzero, it is a vertical line at the unique root of
`E_x`. Equal lines are merged with their coordinate multiplicities. If both
are identically zero, the coordinate is universal.

Let `u` be the number of universal coordinates and put

\[
k=K-u,\qquad n=1{,}048{,}576+k,\qquad m=67{,}472+k.
\]

Any exact support still uses at least `m` nonuniversal coordinate copies; no
claim that it contains every universal coordinate is made. Every selected
point uses at least two distinct line classes. One graph class together with
universal coordinates would give a simultaneous codeword pair; all vertical
coordinates together have weight at most `k-1<m`.

### Weighted affine-line bound

For a weighted affine-line arrangement of total weight `n`, count finite
points incident to weight at least `m` and using at least two classes. Put

\[
q=\lfloor m/2\rfloor,\qquad A=m-q-1.
\]

If no class contributes more than `q`, each selected `m`-multiset contains at
least `q(m-q)` cross-class coordinate pairs. Distinct affine lines meet at
at most one point, hence

\[
L_{\rm low}\le\left\lfloor\frac{\binom n2}{q(m-q)}\right\rfloor.
\]

For points with a unique dominant class, let `h` classes be capable of
dominating and let

\[
a_i=\max\{1,m-\min(w_i,m-1)\},\qquad
W=n-hm+\sum_i a_i.
\]

On a fixed dominant line, at most `h-1` points meet another dominant line;
every remaining point consumes at least `a_i` globally disjoint outside
weight. Therefore

\[
L_{\rm high}\le h(h-1)+W\sum_i\frac1{a_i}.
\]

Holding the other deficiencies fixed gives

\[
f(a)=(C+a)(Q+1/a).
\]

If `C>=0`, then `f''(a)=2C/a^3>=0`; if `C<0`, then
`f'(a)=Q-C/a^2>0`. Thus every maximizer has `a_i in {1,A}`. If `p` of the
`h` deficiencies equal one, the exact remaining expression is

\[
h(h-1)+\bigl(n-hm+p+(h-p)A\bigr)
\left(p+\frac{h-p}{A}\right).
\]

The verifier scans every residual dimension `1<=k<=1,048,576`. The total cap
is nonincreasing and has exact maximum at `k=1`:

```text
low branch                 483
high branch          4,070,464
--------------------------------
uniform cap          4,070,947
```

The high extremizer in the relaxation has eight dominant classes, all with
unit outside deficiency, and outside weight `508,801`.

Since

\[
5{,}201{,}865>4{,}070{,}947,
\]

the whole rank-one family is impossible at whatever ambient dimension it
first appears. The exact contradiction slack is `1,130,918`. This repairs
the parent terminal implication without following an early drop to a fixed
pair.

## Exact next wall

Starting one nominal rank higher, the same descent reaches a rank-two family
of `5,170,912` slopes. Across all ambient dimensions, a proper rank-two drop
guarantees at most `2,751,700` rank-one slopes. That is `1,319,247` below the
uniform cap. The first open implication is therefore an aggregate rank-two
proper-drop forest theorem, not another rank-one endpoint estimate.

## Verification

```bash
python3 experimental/scripts/verify_kb_mca_rank11_uniform_line_repair_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_uniform_line_repair_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank11_uniform_line_repair_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_uniform_line_repair_manifest_v1.py
```

The primary verifier checks all `1,048,576` residual dimensions and all
`10,485,705` rank-twelve early-drop cells. The independent audit uses a
separate implementation, directly enumerates deficiency endpoints at six
selected dimensions, and exhausts `1,334` finite convexity controls. Wolfram
independently reproduced the endpoint, neighboring, full-row, and rank-twelve
boundary values. Delsarte and Ray--Chaudhuri--Wilson were reviewed for
context; no external theorem is load-bearing.
