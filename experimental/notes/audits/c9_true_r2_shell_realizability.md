# C9 convention, full-slice normalization, and exact-line realizability audit

## Claim

The integrated 152-support direct-Sidon packet does **not** instantiate the
active primitive-leaf interface in
`experimental/asymptotic_rs_mca_frontiers.tex`:

1. it labels the fixed-weight-plus-first-moment map as `R=2`, whereas the
   active convention counts only the nonconstant coordinates
   \((p_1,\ldots,p_R)\); and
2. it derives \(M\), \(L\), and \(\bar N\) from the 152 retained supports,
   whereas the active convention derives them from the full fixed-weight
   profile slice and uses the residual only in the counted fibers \(f_s\).

After both corrections, the stored 152-support residual satisfies the
current-frontiers full-slice image-normalized max-fiber and moment inequalities.
This is a quantitative normalization result only, not an active primitive-leaf
C9 instance.  Unrestricted arbitrary-domain algebraic realizability is not the
remaining obstruction: the same finite block row has a complete depth-one fiber
with an exact 1,052-slope MCA line, and a refined four-point construction has
complete true-depth-two Hamming-shell fibers with exponentially many exact MCA
slopes.  Realization, first-match ownership, and payment on intended
smooth/circle rows remain open.

## Status

- **FIXED:** the 152-support packet is effective \(R=1\), not
  current-frontiers-convention \(R=2\), and its residual normalization is not
  the current full-slice normalization.
- **AUDIT:** the existing
  `experimental/notes/audits/c9_r2_near_sidon_razor.md` already supplies a
  genuine full-slice \((p_1,p_2)\) Prouhet fiber.  This audit does not replace
  that packet.  The smaller shell family below independently violates the
  unrestricted full-slice image-normalized Q/Sidon inequality on separated
  arbitrary domains; it would become an active C9 obstruction only after a
  primitive first-match survival theorem.
- **OPEN GAP:** no result here proves that those witnesses survive a
  smooth/circle C1--C8 first-match atlas.  Their raw product locator architecture
  is only a higher-dimensional balanced-core stress candidate; no post-factor
  chart typing or payment theorem is proved.

No manuscript TeX statement is changed by this packet.

## Authority and consumer-backward audit

The potential consumer is the primitive prefix leaf in the frontiers paper:

\[
 \Omega_{T,m}=\{x\in\{0,1\}^T:|x|=m\},\qquad
 \Phi(x)=\sum_{t\in T}x_t(t,t^2,\ldots,t^R),
\]

\[
 M=|\Omega_{T,m}|,\qquad
 L=|\Phi(\Omega_{T,m})|,\qquad
 \bar N=M/L,
\]

while a primitive residual \(\Omega^\circ\subseteq\Omega_{T,m}\) enters only
through

\[
 F_s=\Omega^\circ\cap\Phi^{-1}(s),\qquad f_s=|F_s|.
\]

These are `eq:exact-power-sum-map`, `eq:image-ambient-scales`, and the prose
immediately preceding them.  The effective-span identities `EF0`--`EF1` also
show that a constant coordinate on a fixed-weight slice is an annihilator, not
an independent moment equation.  Complete unprofiled locator-prefix fibers---
equivalently here, after Newton-coordinate equivalence---compile at a separating
pole by `cor:exact-prefix-ray-realization`; primitive survival is separately
defined by `def:primitive-first-match-residual`.

The audited generator instead sets `R = 2` and computes

```text
(mask.bit_count(), support_sum(mask, points) mod p).
```

All 152 supports have weight ten.  Its effective Fourier span is therefore
one-dimensional, and the map is \(p_1\), not \((p_1,p_2)\).  Moreover, it sets
\(M=152\), \(L=121\), and \(\bar N=152/121\) from the residual itself.  The
current full-slice normalization was already present when that packet was
authored: it entered at `2b1a7e20654d44d0beefcd5c7d508be618b0cea1`
on 2026-07-10, while the corrected direct-Sidon packet was authored at
`38012a8b902518286f29180c4c7ec0fb0dda34bd` on 2026-07-16.  This is not later
interface drift.

## Finding 1: the stored residual passes the current quantitative bounds

Keep the stored finite parameters

\[
 k_{\rm block}=5,\quad N=20,\quad m=10,\quad Q=501,
 \quad p=505020040141.
\]

On the full ten-of-twenty slice, the realized first-moment image has

\[
 M=\binom{20}{10}=184756,\qquad L=4481,\qquad
 \bar N=\frac{184756}{4481}.
\]

The stored residual's size-32 fiber therefore has

\[
 \frac{f}{\bar N}=0.7761\ldots<1.
\]

With the packet's \(q=3\) and
\(\sigma=\log(4/3)/8\), its only low-energy residual fiber contributes

\[
 \Gamma^{\rm Sid}_{3,\sigma}
 =\frac1{4481}\left(\frac{32}{184756/4481}\right)^3
 =\frac{10280632832}{98540708249269},
\]

and hence

\[
 \frac{\log\Gamma^{\rm Sid}_{3,\sigma}}{20\cdot3}
 =-0.152799\ldots .
\]

Thus the advertised finite positive-rate failure disappears under the current
full-slice normalization.  This does not establish that the residual is a
primitive first-match leaf.

The same conclusion is asymptotic along the packet's no-wrap balanced-word
extension: take \(k\) divisible by five and choose its integer base and field
modulus so that the first-moment values do not wrap.  For \(k\) four-point
blocks, the full slice has

\[
 M_{\rm full}=\binom{4k}{2k}\ge\frac{16^k}{4k+1}.
\]

A first-moment value is determined by the \(k\) block occupancies
\(c_i\in\{0,1,2,3,4\}\) and the total local offset in
\([0,6k]\).  Modular collisions only decrease the image, so

\[
 L_{\rm full}\le(6k+1)5^k.
\]

The stored residual has mass at most \(2^k+5^k\le2\cdot5^k\) and maximum
fiber \(2^k\).  Consequently

\[
 \frac{\max_s f_s}{\bar N_{\rm full}}
 \le(4k+1)(6k+1)\left(\frac58\right)^k\longrightarrow0.
\]

For every \(q\ge1\), using
\(\sum_s f_s^q\le(\max_s f_s)^{q-1}\sum_sf_s\),

\[
 \Gamma_q
 \le
 2(4k+1)\left(\frac5{16}\right)^k
 \left((4k+1)(6k+1)\left(\frac58\right)^k\right)^{q-1}.
\]

The full ordinary moment, and therefore every Sidon submoment, decays
exponentially.  The 152-support packet should not retain counterexample status
against the current-frontiers full-slice quantitative interface.

## Finding 2: a stronger finite full-fiber line exists at effective R=1

The preceding correction does not mean the block row lacks large prefix
fibers.  Let

\[
 s_*=\sum_{i=0}^4(2Q^i+3).
\]

Exact enumeration of the full slice gives

\[
 |\Phi_1^{-1}(s_*)|=1052.
\]

Every support in this fiber chooses two points in each four-point block, with
total local pair-sum 15.  The local pair-sum polynomial is

\[
 P(x)=x+x^2+2x^3+x^4+x^5,
\]

and the count is the independently checked coefficient

\[
 [x^{15}]P(x)^5=1052.
\]

Its Boolean additive energy is

\[
 E=19726716,\qquad
 \Delta=\frac{4931679}{291063152}=0.0169437\ldots,
\]

well below the same fixed cutoff.  Using the current-frontiers full-slice scale
and only this one fiber, at \(q=4\)

\[
 \frac1{4481}\left(\frac{1052}{184756/4481}\right)^4
 =\frac{430474891952689285601}{4551496773325485841},
\]

whose normalized logarithm is

\[
 0.056867910739\ldots>0.05.
\]

This complete fiber has an exact base-field MCA realization.  Put

\[
 U=X^{10}-s_*X^9,\qquad
 r_0=(U/X)|_D,\qquad r_1=(-1/X)|_D,\qquad
 C=\operatorname{RS}_{\mathbb F_p}(D,8).
\]

For a support \(S\) in the fiber, let \(Q_S=\prod_{t\in S}(X-t)\) and

\[
 \gamma_S=-Q_S(0),\qquad
 h_S=\frac{U-Q_S-\gamma_S}{X}.
\]

The common first locator coefficient gives \(\deg h_S\le7\).  On \(S\),
\(r_0+\gamma_Sr_1=h_S\), and the difference is \(Q_S/X\), so the agreement
set inside \(D\) is exactly \(S\).  The word \(-1/X\) cannot be explained by
a degree-less-than-eight polynomial on ten points.  Exhaustion verifies that
the 1,052 values \(-Q_S(0)\) are distinct modulo the stored prime.

For completeness of the slope count, invoke `thm:exact-list-line-bijection`:
any other agreement-ten slope would give a monic locator
\(Q=U-\gamma-Xh\).  Since \(\deg h<8\), its \(X^9\) coefficient is
\(-s_*\), so its support belongs to the complete first-moment fiber above and
\(\gamma=-Q(0)\).  Thus no additional agreement-ten bad slope exists.  This
line has exactly 1,052 bad slopes and retained-support occupancy one.

This repairs algebraic realizability and full-slice normalization, but it does
not prove that the complete fiber is a primitive residual after C1--C8.

## Finding 3: complete true-R=2 shell fibers with exact MCA slopes

The existing six-point construction in
`c9_r2_near_sidon_razor.md` already proves that its Prouhet family is a
complete depth-two prefix fiber of the full slice.  Applying
`cor:exact-prefix-ray-realization` to that fiber gives an exact MCA line after
choosing a separating pole.  Thus exact RS/MCA realizability of an unrestricted
true-\(R=2\) Prouhet fiber already follows from integrated results, even though
the existing note does not spell out that consumer connection.  The
four-point shell below is an independent repair with a smaller local trade and
an explicit base-field locator line.

The following independent construction gives a true
\((p_1,p_2)\)-fiber and avoids counting fixed weight as a prefix equation.

Fix the integer radix \(b=16\).  Let \(d_0\) be the least positive odd integer
with \(b^{d_0}>14k\), put

\[
 d_i=d_0+2i,\qquad a_i=b^{d_i},\qquad
 T_i=\{a_i,a_i+1,a_i+2,a_i+3\},\qquad
 D_k=\coprod_{i=0}^{k-1}T_i.
\]

Choose a prime

\[
 p_k>\sum_{t\in D_k}t^3.
\]

Bertrand's postulate gives such a prime with \(\log p_k=O(k)\).  Work on the
full \(2k\)-of-\(4k\) slice and define

\[
 \Phi_2(S)=\left(\sum_{t\in S}t,\sum_{t\in S}t^2\right)\in\mathbb F_{p_k}^2.
\]

In block \(i\), write

\[
 A_i=\{a_i,a_i+3\},\qquad B_i=\{a_i+1,a_i+2\}.
\]

Both pairs have sum \(2a_i+3\), while their square sums differ by four.
For \(0\le h\le k\), put

\[
 F_{k,h}=\left\{\coprod_iU_i:
 U_i\in\{A_i,B_i\},\quad |\{i:U_i=B_i\}|=h\right\}.
\]

### Complete-fiber proof

For an arbitrary block subset let \(c_i\) be its size, \(s_i\) its offset
sum, and \(q_i\) its offset-square sum.  Because the \(d_i\) are odd,
the exponent sets \(\{d_i\}\) and \(\{2d_i\}\) are disjoint.  The inequalities
\(b^{d_0}>14k\), \(c_i\le4\), and \(2s_i\le12<b\) make the base-\(b\)
decompositions

\[
 p_1=\sum_i c_i b^{d_i}+\sum_i s_i,
\]

\[
 p_2=\sum_i c_i b^{2d_i}+2\sum_i s_i b^{d_i}+\sum_iq_i
\]

carry-free and unique.  Equality with the target of \(F_{k,h}\) forces
\(c_i=2\), \(s_i=3\) in every block, and
\(\sum_iq_i=9k-4h\).  The only two-element offset sets with sum three are
\(\{0,3\}\) and \(\{1,2\}\), with square sums nine and five.  Therefore

\[
 \boxed{\Phi_2^{-1}(\Phi_2(F_{k,h}))=F_{k,h}},
 \qquad |F_{k,h}|=\binom kh.
\]

The verifier exhausts the complete full slices for \(k=2,3,4,5\), including
the exact \(k=5\) shell profile

```text
1, 5, 10, 10, 5, 1
```

and independently matches power-sum and elementary-symmetric partitions.

### Exact realized-image normalization (not FI)

For one block, the numbers of distinct \((c_i,s_i)\) states by weight are

\[
 1,4,5,4,1,\qquad
 F(x)=1+4x+5x^2+4x^3+x^4.
\]

Only the state \((c_i,s_i)=(2,3)\) has two possible square sums.  If it occurs
in \(r\) blocks, their total square sum has \(r+1\) values.  Hence

\[
 M_k=\binom{4k}{2k},
\]

\[
 L_k=[x^{2k}]\left(F(x)^k+kx^2F(x)^{k-1}\right).
\]

Since \(F(1)=15\) and its coefficients are symmetric and log-concave,

\[
 \log M_k=k\log16+O(\log k),\qquad
 \log L_k=k\log15+O(\log k),
\]

so

\[
 \log\bar N_k=k\log(16/15)+O(\log k).
\]

This family lies outside the image-scale frontier
\(\log(M_k/L_k)=o(4k)\), and it does not satisfy the frontiers hypothesis
`FI`: the construction field is much larger than this realized two-moment
image.  Nevertheless, realized-image normalization does not pay the family,
because the normalized fiber size below still has positive exponential rate.
An earlier routing/refinement theorem is therefore required before the
primitive-leaf inequality could apply.

### Energy and Sidon rate

The block-choice map identifies \(F_{k,h}\) with the weight-\(h\) Boolean
slice.  A difference having \(d\) positive and \(d\) negative coordinates has
\(\binom{k-2d}{h-d}\) representations, so

\[
 E(F_{k,h})=
 \sum_{d=0}^{\min(h,k-h)}
 \binom kd\binom{k-d}d\binom{k-2d}{h-d}^2.
\]

For \(k\) divisible by six and \(h=k/2\), the full-cube upper bound and the
single \(d=k/6\) term give

\[
 \log E(F_{k,k/2})=k\log6+O(\log k),
\]

and therefore

\[
 \log\Delta(F_{k,k/2})=k\log(3/4)+O(\log k).
\]

Thus the central fiber is below the fixed cutoff
\(\sigma=\log(4/3)/8\) for all sufficiently large \(k\).  Moreover

\[
 \frac{|F_{k,k/2}|}{\bar N_k}
 =\exp\left(k\log(15/8)-O(\log k)\right).
\]

With \(q_k=\lceil\log(4k)\rceil\), one fiber alone gives

\[
 \liminf_{k\to\infty}
 \frac{\log\Gamma^{\rm Sid}_{q_k,\sigma}}{(4k)q_k}
 \ge\frac14\log(15/8)
 =0.157152164855\ldots>0.05.
\]

The same order satisfies \(\log L_k/q_k=o(4k)\).  This violates the
unrestricted full-slice realized-image-normalized Q/Sidon inequality on the
separated arbitrary domains.  It is not a primitive-leaf C9 obstruction unless
it survives the earlier first-match atlas.

### Exact locator-line realization

For \(S\in F_{k,h}\), let

\[
 Q_S=\prod_{t\in S}(X-t)
 =X^{2k}-e_1X^{2k-1}+e_2X^{2k-2}-e_3(S)X^{2k-3}+\cdots.
\]

The first two coefficients are constant on the complete fiber.  If
\(b_i\in\{0,1\}\) records the choice \(A_i/B_i\), then on a fixed shell

\[
 e_3(b)-e_3(b')=-4\sum_i(b_i-b_i')a_i.
\]

Base-\(b\) uniqueness and the no-wrap prime choice make the \(e_3(S)\)
pairwise distinct.  Put

\[
 U=X^{2k}-e_1X^{2k-1}+e_2X^{2k-2},\qquad
 V=X^{2k-3},\qquad
 C_k=\operatorname{RS}_{\mathbb F_{p_k}}(D_k,2k-3).
\]

For \(S\in F_{k,h}\), define

\[
 \gamma_S=-e_3(S),\qquad h_S=U+\gamma_SV-Q_S.
\]

Then \(\deg h_S\le2k-4<2k-3\), and on \(S\),
\(h_S=(U+\gamma_SV)|_S\).  The difference is exactly \(Q_S\), so the
agreement set in \(D_k\) is exactly \(S\).  The direction \(V\) cannot be
explained by a polynomial of degree less than \(2k-3\) on \(2k\) distinct
points.

Conversely, any agreement-\(2k\) explanation at a slope \(\gamma\) makes
\(U+\gamma V-h\) a monic degree-\(2k\) locator.  Its first two elementary
coefficients are the fixed \(e_1,e_2\), and its next coefficient gives
\(e_3=-\gamma\).  Newton-coordinate equivalence and completeness of the shell
fiber therefore force its support into \(F_{k,h}\).  Hence one received line
has exactly

\[
 \binom kh
\]

distinct support-wise MCA-bad slopes, with retained-support occupancy one.  The
general converse is the symbolic locator argument above.  The verifier checks
the full finite-field polynomial identity over an explicit 64-bit prime at
\(k=2\), and checks the integer coefficient and fiber identities exhaustively
through \(k=5\).

## First-match consequence and remaining wall

The refined locator family has the explicit block form

\[
 Q_b(X)=\prod_i(A_i(X)+2b_i),\qquad
 A_i(X)=(X-a_i)(X-a_i-3).
\]

The raw locator family is not a single pencil in the checked characteristic-zero
affine hulls: its rational coefficient ranks at \(k=3,4,5\) are respectively
\(2,5,8\).  These computations certify only the product architecture before
reduction.  This is a C8 stress candidate, not a C8 ownership theorem: no
post-factor balanced-core chart, field-valued projective-rank theorem,
first-match ownership, or exclusion of a subexponential pencil decomposition
is proved.  The executable finite-field line check is supplied only at
\(k=2\); no claim is made that the rational ranks persist at every reduction
prime.  An earlier C1--C7 owner may also fire once a complete smooth/circle
received line is fixed.

Accordingly, the exact remaining question is:

> On an intended smooth/circle row, either prove that a complete true-prefix
> product/trade family survives every earlier first-match cell, or assign all
> its received-line witnesses to an earlier cell and prove that cell's
> profile census and distinct-slope payment.

This is an atlas ownership-and-payment statement; `RC` applies only after
post-factor C8 typing.  It is not repaired by another support-only energy
computation, and it cannot be decided from the 152 selected supports without
the complete full-slice and received-line semantics.

## Ledger impact

- **Hard input 2:** retracts the stale 152-support packet as a live C9
  falsifier; supplies a full-slice-normalized true-\(R=2\) stress family whose
  active relevance remains conditional on primitive first-match survival.
- **Hard inputs 1 and 3:** leaves first-match ownership open; if the family is
  proved to yield a post-factor higher-dimensional balanced-core chart, its
  resulting ray payment is then an input-3 obligation.
- **Finite rows:** supplies an exact 1,052-slope arbitrary-domain finite line,
  but no deployed-row certificate or budget comparison.
- **Profile envelope:** records the additional realized-image floor
  \(\log\bar N_k=(\log(16/15)/4)N+o(N)\), outside `FI`; it does not compare
  that floor with any target or lower reserve.

## Reproducibility

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experimental/scripts/verify_c9_true_r2_shell_realizability.py
PYTHONDONTWRITEBYTECODE=1 python3 experimental/scripts/verify_c9_true_r2_shell_realizability.py --json
PYTHONDONTWRITEBYTECODE=1 python3 experimental/scripts/verify_c9_true_r2_shell_realizability.py --tamper-selftest
```

The verifier uses only the Python standard library.  It:

1. pins exact SHA-256 digests plus defining phrases for the frontiers source,
   the stale generator, and the existing true-\(R=2\) audit;
2. recomputes the 152-point true-\(R=2\) finite profile;
3. exhausts all \(\binom{20}{10}=184756\) supports for the corrected full
   \(R=1\) fiber and its pole slopes;
4. exhausts the refined true-\(R=2\) full slices for \(k=2,3,4,5\);
5. checks the exact image coefficient, slice-energy, locator-rank, and
   base-field line identities; and
6. evaluates exact asymptotic certificates through \(k=384\).

Observed:

```text
RESULT: PASS
status: FIXED / AUDIT / OPEN GAP
finite full-R1: M=184756 L=4481 fiber=1052 slopes=1052 rate=0.056867910739
true-R2 limit: log(15/8)/4=0.157152164856
payload_sha256: dad350df3efb84d95edb5aa3a4983b32952fd9d9430ba50af20af591b26cba75
TAMPER SELF-TEST: PASS (9/9)
```

## Nonclaims

- The separated block domains are not multiplicative cosets or circle domains.
- No C1--C8 survival, absorption, or payment theorem is claimed.
- No unrestricted profile-envelope theorem is refuted: the true-\(R=2\)
  family lies outside the image-scale frontier and still fails unrestricted Q
  at realized-image scale; current-row relevance depends on an earlier
  routing/refinement theorem.
- No `MI`, `MA`, `FI`, `RC`, target comparison, lower reserve, deployed
  threshold, or protocol statement follows.
- The finite \(q=4\) row is an audit certificate, not an asymptotic
  logarithmic-moment theorem.
