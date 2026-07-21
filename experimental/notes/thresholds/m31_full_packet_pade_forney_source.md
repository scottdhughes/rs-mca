# M31 full-packet escape-Pade-bounded-Forney source

## Status

**PROVED LOCAL / CONDITIONAL PRIME-FIELD STRUCTURAL THEOREM /
INDEPENDENT HOSTILE AUDIT `ACCEPT_NARROWED` / LEDGER MOVEMENT ZERO /
OFFICIAL SCORE `0/2`.**

This note records the strongest source-valid part of R37 Role 03. It concerns
the full least-maximizing exact layer over the base field `F_p`; it is not a
whole-ball upper bound and does not compile a paid first-match owner.

The independent audit found one false non-load-bearing boundary sentence in
the repair contract. The theorem below corrects it: the official hypothesis
remains strict `>B*`, but even `>=B*` is numerically enough to force
`M>=36`. Strictness is retained because it is the source-relevant
contradiction hypothesis, not because the pigeonhole count needs it.

## Provenance

- Source base: `origin/main@18cfc199d4612f5dfc01bf6c0155a65a1eaa3832`.
- Same-author repair public text:
  `58c2601694bbaeaa080b730c20a8fe60d8bd1a4c7ce9c3649544c894885524e9`.
- Same-author repair bundle:
  `2574f6b642328f08ff0e2c0f5041b4ac5e41f28b63033048ec3d8182b1434705`.
- Independent hostile-audit packet:
  `0766a35a89a4115cb1ba3cb08f3e9b81f145bb1c1652a6a92736497b5023d97b`.
- Independent hostile-audit public text:
  `9d729b92e056b2c7e55141f8eef3a22e12739c7f6639d8b1bdd12abd7d6d7b57`.

## Theorem: full-packet escape-Pade-bounded-Forney source

Let

\[
p=2^{31}-1=2,147,483,647,\qquad
n=2^{21}=2,097,152,\qquad
K=2^{20}=1,048,576,
\]

\[
a=1,116,023,\qquad
R=n-a=981,129,\qquad
D_{\min}=K-R=67,447,
\]

and

\[
B^*=\left\lfloor\frac{p^4}{2^{100}}\right\rfloor=16,777,215,
\qquad L=B^*+1=16,777,216.
\]

Work over the **base field** \(F=\mathbb F_p\). Let \(D=Z_F(T_n)\) be the archived M31 evaluation domain of size \(n\), let

\[
C=RS_F(D,K),\qquad V=C^\perp,
\]

and let \(y\in F^D\setminus C\) be a received word. Define

\[
\ell_y(v)=\langle y,v\rangle\quad(v\in V),\qquad H_y=\ker\ell_y.
\]

For \(E\subseteq D\), put

\[
W_E=\{v\in V:\operatorname{supp}(v)\subseteq D\setminus E\},
\]

and define \(z_y(E)=1\) exactly when

\[
W_E\subseteq H_y,
\qquad
W_{E\setminus\{x\}}\not\subseteq H_y\quad\text{for every }x\in E.
\tag{1}
\]

Assume the finite above-budget hypothesis

\[
\sum_{\substack{E\subseteq D\\ |E|\le R}}z_y(E)>B^*.
\tag{2}
\]

Then all of the following hold.

### A. Exact explanations and the full same-weight layer

For every \(E\) with \(|E|\le R\), condition \(z_y(E)=1\) is equivalent to the existence of a **unique** codeword \(c_E\in C\) such that

\[
\operatorname{supp}(y-c_E)=E.
\tag{3}
\]

For each weight \(j\), let

\[
\mathcal E_j=\{E\subseteq D:|E|=j,\ z_y(E)=1\},\qquad M_j=|\mathcal E_j|.
\]

Choose \(j_*\) to be the least maximizer of \(M_j\) over

\[
K/2<j\le R.
\]

Then the **entire** exact layer

\[
\mathcal E_*:=\mathcal E_{j_*}=\{E_1,\ldots,E_M\}
\tag{4}
\]

has

\[
M=M_{j_*}\ge36.
\tag{5}
\]

The ordering in (4) may be fixed lexicographically by incidence vectors; no 36-member truncation is made.

### B. Exact recurrence and all one-point escapes in one resultant

Choose the standard weighted-dual isomorphism

\[
\operatorname{Ev}_u:F[X]_{<K}\longrightarrow V,
\qquad f\longmapsto (u_xf(x))_{x\in D},
\]

with every \(u_x\ne0\), and put \(\widehat\ell=\ell_y\circ\operatorname{Ev}_u\). For \(E\subseteq D\), \(|E|=j<K\), define the monic squarefree locator

\[
L_E(X)=\prod_{\alpha\in E}(X-\alpha)
\]

and the polynomial divided-difference numerator

\[
\mathcal B_{\ell}(L_E)(Y)
=
\widehat\ell_X\!\left(\frac{L_E(X)-L_E(Y)}{X-Y}\right).
\tag{6}
\]

The apparent denominator in (6) is removable because the numerator is divisible by \(X-Y\). Then

\[
z_y(E)=1
\iff
\begin{cases}
\widehat\ell(X^tL_E)=0,&0\le t<K-j,\\[1mm]
\operatorname{Res}(L_E,\mathcal B_{\ell}(L_E))\ne0.
\end{cases}
\tag{7}
\]

Moreover, because \(L_E\) is monic, squarefree, and split over \(D\),

\[
\operatorname{Res}(L_E,\mathcal B_{\ell}(L_E))
=
\prod_{\alpha\in E}
\widehat\ell\!\left(\frac{L_E(X)}{X-\alpha}\right).
\tag{8}
\]

Thus (8) retains every one-point escape, including points later found in a common core.

### C. Actual common-core division and primitive full row

For the full layer (4), put

\[
C_*=\bigcap_{i=1}^{M}E_i,\qquad
c=|C_*|,\qquad
G=L_{C_*}=\gcd(L_{E_1},\ldots,L_{E_M}),
\]

\[
P_i=L_{E_i}/G,\qquad
e=j_*-c,\qquad
D_0=K-j_*,\qquad
N=K-c=e+D_0.
\tag{9}
\]

Then

\[
\gcd(P_1,\ldots,P_M)=1,
\tag{10}
\]

and pairwise MDS separation gives

\[
c\le2j_*-K-1,
\qquad
e\ge D_0+1>0.
\tag{11}
\]

Define the reduced functional

\[
\lambda(Q)=\widehat\ell(GQ),\qquad Q\in F[X]_{<N}.
\tag{12}
\]

Then \(\lambda\ne0\) and

\[
\lambda(X^tP_i)=0\qquad(1\le i\le M,\ 0\le t<D_0).
\tag{13}
\]

For each \(i\), define

\[
B_i(Y)=\lambda_X\!\left(\frac{P_i(X)-P_i(Y)}{X-Y}\right).
\tag{14}
\]

For every variable point \(\alpha\in E_i\setminus C_*\),

\[
B_i(\alpha)=\widehat\ell\!\left(\frac{L_{E_i}(X)}{X-\alpha}\right)\ne0,
\tag{15}
\]

so

\[
\operatorname{Res}(P_i,B_i)\ne0,
\qquad \gcd(P_i,B_i)=1.
\tag{16}
\]

For every core point \(x\in C_*\), set

\[
\kappa_{i,x}=\widehat\ell\!\left(\frac{L_{E_i}(X)}{X-x}\right)\ne0.
\tag{17}
\]

The global escape product factors exactly as

\[
\operatorname{Res}(L_{E_i},\mathcal B_{\ell}(L_{E_i}))
=
\operatorname{Res}(P_i,B_i)
\prod_{x\in C_*}\kappa_{i,x}.
\tag{18}
\]

Consequently the complete packet product

\[
\mathcal R_{\mathrm{full}}
=
\prod_{i=1}^{M}
\operatorname{Res}(L_{E_i},\mathcal B_{\ell}(L_{E_i}))
\tag{19}
\]

is nonzero.

### D. Exact fixed-core description, with the necessary qualification

After \(G\) has been obtained from the full layer, define

\[
\begin{aligned}
\mathcal A_{\ell,G,j_*}=\{P:\;&GP\text{ is monic, squarefree, }D\text{-split, and }\deg(GP)=j_*,\\
&\widehat\ell(X^tGP)=0\quad(0\le t<D_0),\\
&\operatorname{Res}(GP,\mathcal B_{\ell}(GP))\ne0\}.
\end{aligned}
\tag{20}
\]

Then

\[
\mathcal A_{\ell,G,j_*}=\{P_1,\ldots,P_M\}.
\tag{21}
\]

Equation (21) is an exact **post-extraction algebraic characterization**. It is not an efficient independent algorithm for discovering \(G\), and it is not an owner compiler or a payment map.

### E. Common Padé source

Let

\[
m_r=\lambda(X^r)\quad(0\le r<N),
\qquad
S_\lambda(Z)=\sum_{r=0}^{N-1}m_rZ^{-r-1}.
\tag{22}
\]

Then for every \(i\),

\[
B_i(Z)=[P_i(Z)S_\lambda(Z)]_{\ge0},
\tag{23}
\]

\[
P_i(Z)S_\lambda(Z)-B_i(Z)=O(Z^{-D_0-1}),
\tag{24}
\]

and, because \(P_i\) is monic of degree \(e\),

\[
S_\lambda(Z)-\frac{B_i(Z)}{P_i(Z)}=O(Z^{-N-1}).
\tag{25}
\]

The fractions are reduced by (16). This is a formal Laurent-series statement at infinity; no value at a root of \(P_i\) is taken.

### F. Bounded-degree full-packet Forney source

Let

\[
\operatorname{Syz}(P_1,\ldots,P_M)
=
\{(A_1,\ldots,A_M)\in F[X]^M:\sum_iA_iP_i=0\}.
\]

It is free of rank \(M-1\). Let

\[
0\le\mu_1\le\cdots\le\mu_{M-1}
\tag{26}
\]

be the row degrees of a row-reduced polynomial basis. Then

\[
\sum_{r=1}^{M-1}\mu_r=e.
\tag{27}
\]

For \(D\ge0\), define

\[
\Theta_D:\bigoplus_{i=1}^{M}F[X]_{<D}\longrightarrow F[X]_{<e+D},
\qquad(H_i)_i\longmapsto\sum_iH_iP_i.
\tag{28}
\]

The exact cokernel formula is

\[
\dim_F\operatorname{coker}\Theta_D
=
\sum_{r=1}^{M-1}\max(0,\mu_r-D).
\tag{29}
\]

The nonzero functional \(\lambda\) annihilates \(\operatorname{im}\Theta_{D_0}\), so \(\Theta_{D_0}\) is not onto. Hence

\[
\mu_{M-1}\ge D_0+1.
\tag{30}
\]

Combining (27), (30), and (11),

\[
\sum_{r=1}^{M-2}\mu_r
\le e-D_0-1
=2j_*-K-c-1
\le2R-K-1
=913,681.
\tag{31}
\]

Therefore

\[
\mu_1+\mu_2
\le
\left\lfloor\frac{2(2j_*-K-c-1)}{M-2}\right\rfloor
\le53,745
<D_0,
\tag{32}
\]

and at least

\[
M-15
\tag{33}
\]

of the \(M-1\) minimal rows have degree strictly less than \(D_0\). In particular, when \(M=36\), at least 21 minimal rows are below the cutoff.

No nonzero syzygy supported on only two columns can have vector degree below \(D_0\). Thus the first two minimal rows form an independent \(2\times M\) bounded-degree frame with at least one nonzero \(2\times2\) minor of degree at most \(53,745\), but that frame is not classified or paid.

### G. Exact scope

This theorem is:

- finite, not asymptotic;
- over \(\mathbb F_p\), not over \(\mathbb F_{p^4}\);
- conditional on the hypothetical strict inequality (2);
- source-preserving at the level of the actual received word \(y\), its functional \(\ell_y\), the full exact layer, its unique codeword explanations, all variable escapes, and all core escapes;
- owner-free and payment-free.

It does **not** establish the adjacent safe endpoint \(a=1,116,023\). The archived unsafe-side statement at \(a_0=1,116,022\) is inherited context and is not reproved here. No scalar descent to the deployed quartic field is invoked.

# LOAD_BEARING_STEPS

## 1. Orthogonal support bridge

Let \(U_S\subseteq F^D\) denote the coordinate subspace supported on \(S\). Since

\[
W_E=V\cap U_{D\setminus E},
\]

finite-dimensional orthogonality gives

\[
W_E^\perp=V^\perp+U_{D\setminus E}^\perp=C+U_E.
\tag{34}
\]

For \(H_y=\ker(v\mapsto\langle y,v\rangle)\),

\[
W_E\subseteq H_y
\iff y\in W_E^\perp
\iff y\in C+U_E.
\tag{35}
\]

Thus containment is exactly the existence of an explanation \(y=c+e\) with \(c\in C\) and \(\operatorname{supp}(e)\subseteq E\). If two codewords explained the same \(E\), their nonzero difference would be a codeword supported on at most \(|E|\le R<K+1=d(C)\), impossible. Hence the explanation is unique. If its error support omitted \(x\in E\), then \(y\in C+U_{E\setminus\{x\}}\), contradicting the escape in (1). This proves (3) self-containedly.

## 2. Weighted-dual locator bridge

The archived generalized-RS dual description supplies nonzero weights \(u_x\) and the isomorphism \(\operatorname{Ev}_u\). A degree-\(<K\) polynomial vanishes at every point of \(E\) iff it is divisible by the squarefree locator \(L_E\). Therefore

\[
W_E=\operatorname{Ev}_u\bigl(L_EF[X]_{<K-j}\bigr).
\tag{36}
\]

Applying \(\ell_y\) to the monomial basis of the multiplier space proves the recurrence part of (7). No genericity assumption is used.

## 3. One-point quotient and escape value

For \(\alpha\in E\),

\[
W_{E\setminus\{\alpha\}}
=
\operatorname{Ev}_u\left(\frac{L_E}{X-\alpha}F[X]_{<K-j+1}\right).
\]

Every multiplier has the unique form

\[
A(X)=A(\alpha)+(X-\alpha)Q(X),\qquad \deg Q<K-j.
\]

Modulo \(W_E\), the one-point extension is therefore one-dimensional and represented by \(L_E/(X-\alpha)\). Assuming containment,

\[
W_{E\setminus\{\alpha\}}\not\subseteq H_y
\iff
\widehat\ell\left(\frac{L_E}{X-\alpha}\right)\ne0.
\tag{37}
\]

## 4. Divided difference and resultant

Since \(L_E(\alpha)=0\), substituting \(Y=\alpha\) into (6) gives exactly the value in (37). A monic squarefree split polynomial satisfies

\[
\operatorname{Res}(L_E,Q)=\prod_{\alpha\in E}Q(\alpha).
\]

This proves (7)–(8). Squarefreeness is load-bearing; the falsification section gives a repeated-root counterexample to the naive version.

## 5. Pigeonhole extraction of the complete layer

For any fixed \(1\le j\le K/2\), there is at most one exact support: two would give two errors for the same received word whose difference is a nonzero codeword supported on at most \(2j\le K<d(C)=K+1\). The zero layer is absent because \(y\notin C\). Thus at most

\[
K/2=524,288
\]

supports lie at low weights. Under (2), at least

\[
16,777,216-524,288=16,252,928
\]

supports lie in the

\[
R-K/2=456,841
\]

weights \(K/2<j\le R\). Hence one complete layer has size at least

\[
\left\lceil\frac{16,252,928}{456,841}\right\rceil=36.
\]

Selecting the least maximizer fixes \(j_*\) without discarding multiplicity.

## 6. Pairwise MDS separation and common core

For distinct exact supports, the difference of the unique errors is a nonzero codeword supported in \(E_i\cup E_k\). Therefore

\[
|E_i\cup E_k|\ge K+1,
\qquad |E_i\cap E_k|\le2j_*-K-1.
\tag{38}
\]

The gcd of squarefree split locators is exactly the locator of the intersection of their root sets, proving the formula for \(G\). Dividing the full common gcd leaves a primitive row, proving (10). Since \(C_*\subseteq E_i\cap E_k\), (11) follows from (38).

## 7. Reduced functional is nonzero and retains every escape

Equation (13) is the original recurrence after factoring \(G\). By (11), every \(P_i\) has at least one root \(\alpha\). Exact escape gives

\[
\lambda\left(\frac{P_i}{X-\alpha}\right)
=
\widehat\ell\left(\frac{L_{E_i}}{X-\alpha}\right)\ne0,
\]

so \(\lambda\ne0\). Evaluating the reduced divided difference at variable roots proves (15). Evaluating the global divided difference at the disjoint root sets of \(G\) and \(P_i\) proves (18) without dropping core factors.

## 8. Exact fixed-core characterization

Every actual \(P_i\) satisfies (20). Conversely, a polynomial in (20) gives a unique size-\(j_*\) support from the roots of \(GP\). Equations (7) and (20) make that support exact for the same received word, so it belongs to the complete layer by definition. This proves (21). The argument uses \(G\) already extracted from the complete layer; it does not discover \(G\).

## 9. Padé coefficient identity

Write \(P_i(Z)=\sum_{k=0}^{e}p_{i,k}Z^k\). The polynomial identity

\[
\frac{X^k-Y^k}{X-Y}=\sum_{h=0}^{k-1}X^{k-1-h}Y^h
\]

shows that the coefficient of \(Z^h\) in (14) is

\[
\sum_{k=h+1}^{e}p_{i,k}m_{k-h-1},
\]

which is exactly the nonnegative-power coefficient of \(P_iS_\lambda\). The coefficient of \(Z^{-t-1}\) is

\[
\sum_{k=0}^{e}p_{i,k}m_{k+t}=\lambda(X^tP_i),
\]

and vanishes for \(0\le t<D_0\) by (13). This proves (23)–(24). Division by a monic degree-\(e\) polynomial shifts the order by \(e\), and \(e+D_0=N\), proving (25).

## 10. Syzygy rank and exact index sum

Let \(R_0=F[X]\) and \(P=(P_1,\ldots,P_M)\). Primitivity gives a Bézout identity \(\sum A_iP_i=1\), so the map \(R_0^M\to R_0\), \(A\mapsto A\cdot P\), is split-surjective. Its kernel is therefore a free direct summand of rank \(M-1\).

Choose a row-reduced basis matrix \(S\) of the kernel, with row degrees \(\mu_r\). Let \(\Delta_i\) be the signed maximal minor obtained by deleting column \(i\). The cofactor vector \(\Delta\) spans the one-dimensional right nullspace of \(S\) over \(F(X)\), so \(\Delta=qP\). Because \(\gcd(P_i)=1\), a Bézout combination shows \(q\in F[X]\). Because the row module is a direct summand, adjoining a splitting vector to the rows of \(S\) gives a unimodular matrix; Laplace expansion then says the maximal minors generate the unit ideal. Hence \(q\in F^\times\).

Row-reducedness means the leading coefficient rows are independent. Every maximal minor has degree at most \(\sum\mu_r\), and at least one leading maximal minor is nonzero, so

\[
\max_i\deg\Delta_i=\sum_r\mu_r.
\]

Since \(\Delta=qP\) and every \(P_i\) has degree \(e\), (27) follows.

## 11. Predictable-degree and cokernel formula

For a row-reduced basis, independence of the leading rows gives

\[
\deg\left(\sum_r q_rS_r\right)=\max_r(\deg q_r+\mu_r)
\]

for every nonzero coefficient tuple. Thus a syzygy lies in \((F[X]_{<D})^M\) exactly when \(\deg q_r<D-\mu_r\) for each \(r\). Therefore

\[
\dim\ker\Theta_D=\sum_r\max(0,D-\mu_r).
\]

Subtracting rank from the target dimension \(e+D\), using a domain dimension \(MD\) and (27), gives (29) by direct algebra.

## 12. Non-surjectivity and bounded rows

For \(D=D_0\), every term \(H_iP_i\) with \(\deg H_i<D_0\) is annihilated by \(\lambda\), while \(\lambda\ne0\) on the target \(F[X]_{<e+D_0}\). Hence \(\Theta_{D_0}\) is not onto. Formula (29) then proves (30). Equations (31)–(32) are exact integer consequences.

To obtain (33), at most

\[
\left\lfloor\frac{913,681}{67,447}\right\rfloor=13
\]

of the first \(M-2\) indices can be at least \(D_0\); including the exceptional largest index gives at most 14 such indices among \(M-1\), leaving at least \(M-15\) below the cutoff.

## 13. Two-column obstruction

Suppose \(AP_i+BP_k=0\). Let \(Q=\gcd(P_i,P_k)\) and write \(P_i=QR_i\), \(P_k=QR_k\) with \(\gcd(R_i,R_k)=1\). Then \(R_i\mid B\) and \(R_k\mid A\). If

\[
q=\deg Q=|(E_i\cap E_k)\setminus C_*|,
\]

then (38) gives

\[
e-q\ge K+1-j_*=D_0+1.
\]

Thus every nonzero two-column syzygy has vector degree at least \(D_0+1\), proving the final assertion in F.

# FALSIFICATION_ATTEMPTS

## Boundary and endpoint tests

- The official source hypothesis is `> B*`, hence the integer mass is at least `B*+1=16,777,216`. Numerically, replacing it by `>=B*` would still force `M>=36`: the exact pigeonhole threshold is `16,513,724`. We retain strictness only because it is the source-relevant violation hypothesis.
- The zero layer contributes nothing for a nonzero syndrome because `W_empty=V` is not contained in a proper hyperplane.
- At the boundary `j=K/2`, the two-error union has size at most `K`, still below the MDS distance `K+1`; the low-layer cap is therefore valid inclusively.
- At `j=R`, `D0=K-R=67,447`, so the strict numerical separation `53,745<D0` remains valid.
- The budget was recomputed with integer arithmetic as `floor(p^4/2^100)=16,777,215`; changing it by one is rejected by the repair verifier.

## Recurrence off-by-one

The final recurrence equation is necessary. In the verifier’s \(F_7\), \(K=3\) witness, moments \((m_0,m_1,m_2)=(1,0,1)\) and locator \(L=X\) satisfy

\[
\lambda(L)=0,\qquad \lambda(XL)=1,
\]

while the escape numerator is nonzero. Omitting the last equation would falsely accept this support.

## Sign and normalization

The sign in (6) is fixed by

\[
(X^k-Y^k)/(X-Y)=\sum X^{k-1-h}Y^h.
\]

Reversing the numerator changes \(B_i\) to \(-B_i\) and breaks the Padé polynomial-part identity, although nonvanishing of a resultant alone would not detect the sign. Multiplying \(\ell_y\) by any nonzero scalar multiplies every numerator and escape value by that scalar and each size-\(j\) resultant by its \(j\)-th power; all accepted supports and nonvanishing statements remain unchanged. The verifier checks all nonzero scalings in its \(F_{11}\) fixture.

## Zero denominators

- The weighted-dual factors \(u_x\) are nonzero by the generalized-RS dual construction on distinct evaluation points.
- `(L(X)-L(Y))/(X-Y)` is a polynomial identity, not evaluation at a zero denominator.
- The Padé fraction is a formal expansion at infinity, where a monic polynomial is invertible as a Laurent series.
- At finite roots, the theorem uses resultants and escape values, not division by \(P_i(\alpha)=0\).

## Repeated roots

Squarefreeness cannot be omitted. Over \(F_7\) with \(K=3\), take

\[
L=X^2,\qquad (m_0,m_1,m_2)=(0,1,0).
\]

Then the only containment equation gives \(\lambda(L)=0\), while the divided-difference numerator is \(1\) at the repeated root, so the naive resultant is nonzero. But \(X^2\) is not the locator of a two-point support. This is an exact counterexample to a repeated-root version of (7), and it is why “monic squarefree \(D\)-split” is explicit in every packet definition.

## Common-core escape omission

Reduced variable escapes do not replace core escapes. Over \(F_7\), \(K=3\), with moments \((1,0,0)\) and

\[
L=X(X-1),
\]

containment holds. If `1` is treated as a core point and `0` as variable, the variable escape is \(\lambda(X-1)=-1\ne0\), but the core escape is \(\lambda(X)=0\). A variable-only reduced resultant would accept falsely. Equation (18) prevents that omission.

## Full-packet truncation

The verifier’s \(F_{11}\), \(n=8\), \(K=4\) fixture with moments \((1,0,1,4)\) has the exact weight-three layer

\[
\{\{0,1,3\},\{1,2,4\},\{1,5,7\}\},
\]

with common core \(\{1\}\). Deleting one member breaks the exact equality in (21). This mutation checks that “full layer” is not silently replaced by a convenient subpacket.

## Wrong-field substitution

The algebraic divided-difference identities make sense over many fields, but the deployed structural theorem above is tied to the archived \(\mathbb F_p\) domain, dual weights, MDS row, and prime-field hyperplane target. Replacing \(F_p\) by \(F_{p^4}\) is not a harmless substitution: the list row’s field denominator is \(p^4\), and a scalar-descent/source multiplicity theorem is needed. No such transfer is proved here. The verifier therefore treats `F_{p^4}` as an unsupported scope mutation.

## First-match, owner, add-back, and ledger tests

No first-match owner is constructed, so no collision or disjointness theorem can be tested positively. The repaired artifact instead fails closed: owner is `NONE`, add-back is `UNCLAIMED`, and ledger movement is zero. A mutation asserting a nonzero owner/payment is rejected. The common core is algebraically restored in (18), but no combinatorial multiplicity add-back or padded-source transfer is claimed.


# Novelty and overlap boundary

The MDS same-weight extraction, the conclusion `M>=36`, the warning that an
arbitrary bounded packet need not contain the desired face, the Forney-index
strategy, and the conditional four-face/CRT/Plucker calculations after face
selection are inherited from pinned source or live work.

The self-contained delta recorded here is:

1. the exact explanation/support bridge;
2. retention of the entire complete same-weight layer, with no 36-member
   truncation;
3. the exact recurrence and all one-point escapes in one resultant;
4. division by the true common core while retaining both core and variable
   escapes;
5. the exact post-extraction fixed-core characterization;
6. the common Pade source;
7. syzygy rank, index-sum, and cokernel formulas for the full packet;
8. the deployed bounded-Forney consequences; and
9. the exact two-column obstruction below `D0`.

Live PR #1021 concerns a different conditional masked-diagonal-saturation
exact sequence. Its theorem and files do not duplicate this full-packet
escape-Pade result.

# Audit and replay

The independent hostile-proof audit returned `ACCEPT_NARROWED` for theorem
parts A-G. The director independently checked the archive manifests, inspected
the standard-library-only verifier before execution, and reproduced:

```text
python3 experimental/scripts/verify_m31_full_packet_pade_forney.py --check \
  --expected experimental/data/certificates/m31-full-packet-pade-forney/expected.txt
python3 -O experimental/scripts/verify_m31_full_packet_pade_forney.py --check \
  --expected experimental/data/certificates/m31-full-packet-pade-forney/expected.txt
python3 experimental/scripts/verify_m31_full_packet_pade_forney.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_full_packet_pade_forney.py --tamper-selftest
```

Normal and optimized check outputs were byte-identical and matched the frozen
expected output. Normal and optimized tamper outputs were byte-identical and
detected all eight semantic mutations.

The archived route-cut, Sidon, and whole-ball verifiers are not proof
dependencies. In the compact packet they terminate at missing hash-gated
source files; their environment-dependent traceback hashes are not portable
replay invariants.

# Remaining wall

To close the M31 list row, one still needs at least one source-valid terminal:

1. a direct count proving the actual escape-Pade-bounded-Forney packet cannot
   exceed `B*`;
2. a source-selected collision-bearing factorized face from that actual
   packet; or
3. a globally disjoint first-match paid owner with every required add-back.

# Nonclaims

This note proves no whole-ball inequality, adjacent safe endpoint, actual
above-budget received word, factorized collision face, first-match owner,
common-core add-back, payment, scalar descent, quartic-field transfer, full
list upper bound, recurrence, or official theorem. Ledger movement is zero and
the official score remains `0/2`.
