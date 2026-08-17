# Anchored correction-ray packing in affine error rank twelve

## 1. Exact inherited interface

Work on a shortened KoalaBear row

\[
(n,K,m)=(R+K,K,D+K),
\qquad R=1{,}048{,}576,
\qquad D=67{,}472,
\]

and put

\[
t=n-m=R-D=981{,}104.
\]

The repaired predecessor stack supplies a source-bound rank-two explanation family \(Z\) of

\[
|Z|=L_2=5{,}170{,}912
\]

distinct finite post-near slopes. Each slope retains one frozen exact size-\(m\) bad support, one explanation, and one minimizing pair. Every endpoint difference lies in one fixed two-dimensional Reed--Solomon direction code \(C'\).

The exact parent `ed556ccb7527e1c54e58b8d151ccefd8539000ac` proves that a proper rank-two drop at ambient dimension \(K\) produces a rank-one leaf with a source-bound full common pair core \(C\). Write

\[
c=|C|,\qquad k=K-c,\qquad r=t-c.
\]

The parent inverts the exact all-dimension rank-one capacity \(A(k)\) and thereby supplies a nondecreasing lower floor for \(c\). Before selecting a proper drop, every whole-family pair-core coordinate is repeatedly shortened. Thus no remaining coordinate belongs to the complete pair core of all slopes in \(Z\).

## 2. The support partition and its exact rank-one owner

Let \(W\le C'\) be the one-dimensional direction space of the proper-drop leaf. Every polynomial in \(W\) vanishes on \(C\). Fix one leaf minimizing pair \(e_0=(a_0,b_0)\), translate the received pair by \(e_0\), and put

\[
p_\gamma=(a_\gamma-a_0)+\gamma(b_\gamma-b_0)\in C'
\]

for every selected slope.

Partition the original slope set by its already-frozen support:

\[
Z=Z_{\rm in}\sqcup Z_{\rm out},
\]

where \(Z_{\rm in}\) consists of supports meeting \(C\).

At a coordinate \(x\in C\), evaluation on \(C'\) is nonzero; otherwise \(x\) would be a whole-family pair-core coordinate. Hence

\[
\ker(\operatorname{ev}_x|_{C'})=W.
\]

If the frozen support of \(\gamma\) meets \(C\), scalar agreement at that coordinate gives \(p_\gamma\in W\). Therefore \(Z_{\rm in}\) is one rank-one explanation family.

The effective dimension is **exactly** \(k=K-c\). Indeed, \(C\) is universal for every slope in \(Z_{\rm in}\). Conversely the original proper-drop leaf is contained in \(Z_{\rm in}\) and has at least two distinct slopes; any further scalar-universal coordinate for \(Z_{\rm in}\) would be pair-universal for that leaf, contradicting that \(C\) is its full common pair core. Consequently

\[
\boxed{|Z_{\rm in}|\le A(k)}. \tag{2.1}
\]

This exact-core observation permits the dimension-specific capacity. It does not reuse the invalid inference that a merely lower-bounded core has that exact dimension.

## 3. Fixed-anchor packing of the exceptional family

Assume \(Z_{\rm out}\) has at least three slopes and choose two distinct anchors \(\alpha,\beta\). Put

\[
X=D_K\setminus C,\qquad |X|=n-c=R+k=:N.
\]

Every exceptional support is an \(m\)-subset of \(X\), so write

\[
E_\gamma=X\setminus S_\gamma,\qquad |E_\gamma|=r.
\]

For \(\gamma\ne\alpha,\beta\), define

\[
q_\gamma=[p_\alpha,p_\beta,p_\gamma]\in C'.
\]

On \(S_\alpha\cap S_\beta\cap S_\gamma\), all three explanations agree with the translated received line and are affine in the slope. Therefore

\[
\operatorname{supp}(q_\gamma)\cap X\subseteq E_\alpha\cup E_\beta\cup E_\gamma. \tag{3.1}
\]

Throughout the proved range, \(3r<R+1\). If a nonzero \(q_\gamma\) belonged to \(W\), it would vanish on \(C\) and have total weight at most \(3r\), contradicting the Reed--Solomon minimum weight

\[
n-K+1=R+1=1{,}048{,}577.
\]

Choose a linear functional \(\varphi:C'\to\mathbb F\) with kernel \(W\), and normalize

\[
Q_\gamma=q_\gamma/\varphi(q_\gamma),\qquad \varphi(Q_\gamma)=1.
\]

Let \(Q_1,\ldots,Q_s\) be the distinct normalized values and choose one representative slope \(\gamma_i\) for each. Set

\[
F=E_\alpha\cup E_\beta,\qquad B_i=X\setminus(F\cup E_{\gamma_i}).
\]

Then \(|B_i|\ge N-|F|-r\).

### Pairwise disjointness

If \(x\in B_i\cap B_j\) with \(i\ne j\), then \(Q_i(x)=Q_j(x)=0\). Since both are normalized by \(\varphi=1\), distinct values \(Q_i,Q_j\) are linearly independent and span \(C'\). Thus every word in \(C'\) vanishes at \(x\).

The anchors also agree with the translated received scalar line at \(x\). Their two distinct slopes force both translated received endpoints to vanish at \(x\). Every endpoint difference lies in \(C'\), so \(x\) is a whole-family pair-core coordinate, contradicting the prior exhaustion. Therefore

\[
B_i\cap B_j=\varnothing\qquad(i\ne j). \tag{3.2}
\]

All \(B_i\) lie in \(X\setminus F\). Hence

\[
s(N-|F|-r)\le N-|F|.
\]

Because \(|F|\le2r\) and \(y/(y-r)\) decreases in \(y\),

\[
\boxed{s\le\left\lfloor\frac{N-2r}{N-3r}\right\rfloor} \tag{3.3}
\]

whenever \(N>3r\).

### Conversion to disjoint correction rays

For a fixed normalized value \(Q_i\), the identity

\[
[p_\alpha,p_\beta,p_\gamma]=c_\gamma Q_i
\]

integrates against the affine interpolant through \(p_\alpha,p_\beta\). Thus all slopes carrying value \(Q_i\) lie on one affine correction ray. Assign the two anchors to the first ray and every other slope according to its normalized value. This gives a disjoint partition of \(Z_{\rm out}\) into at most the number of rays in (3.3). If fewer than three exceptional slopes occur, the same conclusion is immediate.

## 4. A uniform weighted-line payment for one ray

Consider one emitted correction ray. After subtracting its affine base, the explanation at parameter \((\gamma,z)\) is \(zQ\). Let \(u\) be the number of ray-universal coordinates in \(X\), and put

\[
M=m-u,\qquad N'=|X|-u=M+r.
\]

Since \(Q\ne0\) has degree below \(K\), \(u\le K-1\), so

\[
M\ge m-(K-1)=D+1=:M_0=67{,}473. \tag{4.1}
\]

Every nonuniversal coordinate is an affine line in the parameter plane: a graph line when \(Q(x)\ne0\), or one vertical line at a nonuniversal zero of \(Q\). Equal lines are merged with their coordinate multiplicities. Every selected support uses at least \(M\) nonuniversal coordinate copies and at least two distinct line classes; otherwise it would be simultaneously explained by one codeword pair.

Apply the inherited weighted affine-line theorem. For total weight \(N'=M+r\) and threshold \(M\), put

\[
q=\lfloor M/2\rfloor,\qquad a=M-q-1.
\]

The low-dominant contribution is at most

\[
L(M,r)=\left\lfloor\frac{\binom{M+r}{2}}{q(M-q)}\right\rfloor. \tag{4.2}
\]

For \(h\) dominant line classes, if \(p\) endpoint deficiencies equal one and \(h-p\) equal \(a\), the high-dominant relaxation is

\[
H_{h,p}(M,r)=h(h-1)+W\left(p+\frac{h-p}{a}\right), \tag{4.3}
\]

where

\[
W=M+r-hM+p+(h-p)a\ge0.
\]

The inherited one-variable convexity argument shows that these endpoint profiles suffice.

### Uniformity over the unknown universal core

For fixed \(r\), the real quotient in (4.2) decreases as \(M\) increases. Writing \(M=2A+1\) and then \(M=2A+2\), the successive differences are

\[
\frac{r(2A+r+1)}{2A(A+1)^2}\ge0,
\]

and

\[
\frac{(r-1)(2A+r+2)}{2(A+1)^2(A+2)}\ge0.
\]

For (4.3), on each parity write \(W=C-(h+p-2)A\). Its second derivative in \(A\) is

\[
\frac{2(h-p)C}{A^3}\ge0.
\]

Thus each parity maximum occurs at its first allowed \(M\), or at the final feasible endpoint where \(W\) vanishes. It is enough to inspect \(M_0\), \(M_0+1\), and the finite \(W=0\) endpoints. This yields a uniform function \(U(r)\), valid for every possible ray-universal core.

The exact endpoint table gives

\[
\begin{array}{c|r}
r&U(r)\\ \hline
262{,}144&389{,}395\\
274{,}493&418{,}707\\
277{,}582&427{,}975\\
309{,}634&524{,}141\\
318{,}595&551{,}027\\
335{,}114&600{,}590\\
344{,}037&627{,}362.
\end{array} \tag{4.4}
\]

The largest table has only twelve possible dominant classes. Exact replay also proves

\[
U(r+1)-U(r)\le4\qquad(0\le r<344{,}037). \tag{4.5}
\]

## 5. Exact payment from \(K=706{,}612\)

The parent locator-floor scan and (3.3) give the exact first cell

\[
\begin{array}{c|r}
K&706{,}612\\
\text{proper-drop incident load}&2{,}280{,}364\\
k&69{,}545\\
c&637{,}067\\
r&344{,}037\\
N&1{,}118{,}121\\
N-2r&430{,}047\\
N-3r&86{,}010\\
\lfloor(N-2r)/(N-3r)\rfloor&4.
\end{array} \tag{5.1}
\]

As the actual core grows, \(r\) and \(k\) each decrease by one, and the ray count in (3.3) cannot increase. The exact all-cell scan emits at most four rays for every actual proper drop and every \(K\ge706{,}612\).

The inherited capacities satisfy

\[
A(k)-A(k+1)\ge12\qquad(1\le k<69{,}545). \tag{5.2}
\]

Together with (4.5), \(A(k)+jU(r)\) is nonincreasing in \(r\) inside every fixed ray-count interval for \(j\le3\). Scanning the exact lower endpoints of those intervals, and using separate exact extrema for the four-ray interval, gives

\[
\begin{array}{c|r|r|r|r}
\text{ray count}&\min k&\max r&\text{certified cap}&\text{slack to }L_2\\ \hline
1&1&277{,}582&4{,}460{,}342&710{,}570\\
2&1&318{,}595&4{,}908{,}361&262{,}551\\
3&35{,}142&335{,}114&4{,}425{,}931&744{,}981\\
4&57{,}259&344{,}037&4{,}937{,}277&233{,}635.
\end{array} \tag{5.3}
\]

For the four-ray row, the cap is the safe product of the separate extrema

\[
A(57{,}259)+4U(344{,}037)=2{,}427{,}829+4\cdot627{,}362=4{,}937{,}277.
\]

Therefore every proper drop satisfies

\[
|Z|\le4{,}937{,}277<5{,}170{,}912, \tag{5.4}
\]

with exact slack

\[
\boxed{233{,}635}. \tag{5.5}
\]

A proper rank-two drop is impossible throughout

\[
\boxed{706{,}612\le K\le1{,}048{,}576}. \tag{5.6}
\]

At every heavy coordinate, the only remaining outcome is a whole-family pair core. All \(5{,}170{,}912\) slopes shorten together through

\[
1{,}048{,}576-706{,}612+1=341{,}965
\]

ambient dimensions and reach

\[
\boxed{K\le706{,}611}. \tag{5.7}
\]

## 6. Exact adjacent wall

At \(K=706{,}611\), the parent floor gives

\[
k=69{,}545,\quad c=637{,}066,\quad r=344{,}038,\quad N=1{,}118{,}121.
\]

Now

\[
\left\lfloor\frac{N-2r}{N-3r}\right\rfloor=\left\lfloor\frac{430{,}045}{86{,}007}\right\rfloor=5. \tag{6.1}
\]

The present compiler permits five correction rays. Its direct five-ray envelope is

\[
A(69{,}545)+5U(344{,}038)=5{,}417{,}198,
\]

above \(L_2\) by \(246{,}286\). This is a method wall, not an unsafe certificate.

## 7. Scope

This theorem pays the complete proper-drop branch in (5.6). It does not pay affine error rank twelve, move an active-v4 ledger atom, or close KoalaBear. The next theorem must exploit interaction among five anchored correction rays rather than summing five independent weighted-line caps.
