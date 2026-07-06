# Proof strategies for the active safe-side inputs of CAP25 v13

This note was originally written in the older two-input language:

**(A)** the aperiodic band / worst-case M1 local-limit upper theorem, and
**(Q)** the quotient-fiber / quotient-ledger equidistribution upper theorem.

The active CAP25 v13 raw formulation refines this into three final safe-side
inputs:

```text
Q   prefix / quotient flatness
BC  base-field-normalized split-pencil census
SP  primitive shift-pair control
```

Read the old `(A)` umbrella below as the proof-program material feeding BC and
SP, after tangent, quotient, common-GCD, extension, and bounded chart strata are
paid separately.  Q remains Q.

The active source file is `experimental/cap25_cap_v13_raw.tex`; the compact
file is only a companion summary.  Older label names in this strategy document
should be mapped to the raw v13 labels when used in a paper edit: Q is
`prob:Q` / `prob:capg-active-Q`, BC is `prob:BC` /
`prob:capg-active-BC`, and SP is `prob:SP` /
`prob:capg-active-shiftpairs`.

Throughout, $C=\mathrm{RS}[\mathbb F,D,k]$, $n=|D|$, $\rho=k/n$,
$D\subseteq\mathbb B^\times$ a multiplicative coset (or Chebyshev twin-coset
image), $\beta=\log_2|\mathbb B|$, and for an exact agreement $a$:

$$j = n-a \quad(\text{co-support size}), \qquad t = a-k \quad(\text{syndrome window}), \qquad j+t = n-k.$$

$g^*(\rho,\beta)$ is the entropy-subfield envelope, i.e. the largest $g$ with
$H_b(\rho+g)\ge\beta g$. At the deployed rate-$\tfrac12$ rows,
$g^*\approx 0.0322$, and the v13 raw exact unsafe certificates sit
within $\sim10^{-6}$ of it.

---

## 0. What exactly must be proved, and one compatibility correction

### 0.1 The active inputs, graded by strength

The active inputs Q, BC, and SP come in two genuinely different strengths, and
the strategy is different for each.

* **Asymptotic form (with reserve).** Upper bounds good to a factor $\mathrm{poly}(n)$ suffice for the frontier statement at agreements $a_0+R$ with $R\gg\log n$: a factor $n^{C}$ costs $21C$ bits at $n=2^{21}$, while the entropy ledger separates by $\Omega(R)$ bits along the reserve.
* **Finite adjacent form (deployed pair).** To pin $a_*=a_0+1$ by the one-step compiler, the complete upper ledger $U(a_0+1)$ must fit under the budget with only **22.2 / 22.0 / 3.3 / 3.1 bits** of room in the four raw-v13 rows:

  ```text
  KoalaBear MCA    a0=1116047, a1=1116048
  KoalaBear list   a0=1116046, a1=1116047
  Mersenne-31 MCA  a0=1116023, a1=1116024
  Mersenne-31 list a0=1116022, a1=1116023
  ```

  No unspecified polynomial factor survives; even a single factor of $n$ ($21$
  bits) nearly consumes a KoalaBear margin and vastly exceeds both Mersenne
  margins.

The honest program is therefore: **prove the asymptotic forms by theorems, and
reduce the finite adjacent forms to explicitly named extremality statements plus
exact integer computations.** Section Q3 and the risk register make this split
precise.

### 0.2 Proved anchors from the v13 raw package

The following items are useful because they narrow the safe-side problem; they
do **not** prove the finite adjacent safe certificates.

* **Identity-prefix unsafe edge.** The current exact deployed unsafe rows are:

  ```text
  KoalaBear MCA    delta >= 981105/2097152, a0=1116047
  KoalaBear list   delta >= 490553/1048576, a0=1116046
  Mersenne-31 MCA  delta >= 981129/2097152, a0=1116023
  Mersenne-31 list delta >= 490565/1048576, a0=1116022
  ```

  These are exact integer comparisons from the identity-prefix floor plus the
  flexible-budget deep-point conversion.  They supersede the older c=2 and
  c=16/32 experimental edges unless the identity-scale prefix floor is
  intentionally excluded.

* **Witness classification for the floor.** For the pole lines realizing these
  floors, the threshold-$m$ witness supports of the MCA-bad slopes are exactly
  prefix-fiber members.  In the coprime case $\gcd(m,n)=1$, these witnesses are
  aperiodic.  This is why the old broad aperiodic-band conjecture cannot remain
  true below the entropy-subfield envelope.

* **Base-field normalization.** Challenge-field or $q$-scale census models are
  refuted by base-field prefix floors at balanced profiles.  The remaining
  census inputs must be normalized over $|\mathbb B|$ and must not spend a
  larger challenge field unless an explicit transfer theorem is present.

* **Slope elimination and split-pencil reduction.** Per non-common support, the
  finite slope is unique.  The remaining residual census is therefore a
  split-locator / split-pencil counting problem: BC handles the interior
  base-field-normalized split-pencil census, SP handles primitive shift-pair
  control, and Q is the boundary prefix-fiber profile.

* **Rigidity and moments.** Prefix collisions satisfy the stronger split
  rigidity $|M\setminus M'|\ge w+1$ on each side.  The exact second moment is
  controlled by the constant-shift split-pair census.  This is calibration and
  a structural input, not a worst-case finite adjacent certificate.

* **Head-depth Q base cases.** Two-sided prefix-fiber flatness is proved in the
  Weil/head-depth range: approximately $w\le21$--$22$ for KoalaBear and
  $w\le10$--$11$ for Mersenne-31.  The deployed band depth is around
  $6.7\cdot10^4$, so this is a genuine base case, not the deployed closure.

* **Falsifiability.** A counterexample to the envelope should exhibit either a
  super-polynomial primitive prefix fiber or a super-polynomial primitive
  split-pencil family.  Both objects are explicit enough to be certificate
  targets.

### 0.3 Compatibility correction: old `(A)` becomes BC/SP above the envelope

`prob:band` asks for a $q$-free polynomial bound on aperiodically-witnessed MCA-bad slopes throughout $k+\tfrac{2n}{N} < a < n-\lfloor\tfrac{n-k}{3}\rfloor$. As stated, this is now in tension with v13 itself:

* The identity-prefix floor produces, at the identity scale $c=1$, a received
  word $U$ with $\ge \binom nm/|\mathbb B|^w$ listed codewords whose agreement
  supports are the $m$-subsets $M$ themselves -- **generic subsets, hence
  aperiodic** ($c(S)=1$) for all but an exponentially small fraction. This is
  unlike every $c\ge2$ floor, whose witnesses are unions of complete fibers.
* Pushing this list through the deep-point conversion (`thm:A`, admissible since $n-m\le n-k-1$) and `fact:chain` produces simple-pole lines $(f_\alpha,g_\alpha)$ with exponentially many MCA-bad slopes $z=P_i(\alpha)$ whose witness supports are exactly those aperiodic $m$-subsets, at agreements $a=m$ up to $\approx k+g^*n$ — squarely inside the stated band.

Unless essentially all of these slopes accidentally acquire a second, periodic witness (no structural reason for that), the old broad band is **refuted in the sub-band $k+\tfrac{2n}N < a \lesssim k+g^*n$**, exactly as the entropy-frontier discussion anticipated when it said the left edge "moves." The first deliverable of the legacy `(A)` route is therefore editorial but essential:

> **Task A0 (band normalization).** Restate `prob:band` with left edge $a \ge k + g^*(\rho,\beta)\,n + R(n)$ (target $R=O(\log n)$; any $R = n^{o(1)}$ is progress), and record the identity-scale refutation of the old sub-band as a proposition. Verify the witness-bucket assignment of the converted slopes (that their pole-line witnesses are aperiodic-only) by the small-field enumeration culture already used for `thm:v13-first-moment` ($\mathbb F_5$, $\mathbb F_7$).

This matters strategically: it tells us the aperiodic conjecture is *only*
plausible above the envelope, i.e. exactly where the prefix-fiber mechanism runs
out of entropy. Every proof attempt below must use that.  In the v13 raw
v13 language, the old `(A)` proof attempt should land as BC and SP certificates,
not as a fourth final residual input.

### 0.4 The unifying object: split-locator flatness

Both inputs reduce to counting **split locators** (monic squarefree divisors of $X^n-1$ with roots in $D$; the set $\mathcal D_j(D)$ of the v13 Conjecture-F subsection) inside affine subspaces:

* **(Q)** is the case of *prefix-affine* spaces. Fibers of the graded-prefix map $\Phi_w:\ M \mapsto \big((-1)^je_j(M)\big)_{j\le w}$ on $m$-subsets are exactly the sets of split degree-$m$ locators with prescribed top-$w$ coefficients — split points of an affine subspace of codimension $w$.
* **(A)** is the case of *syndrome-annihilator* spaces. For a line $(f,g)$ and slope $z$, badness at exact agreement $a$ requires a split locator in
  $$W_z := \{L\in\mathbb F[X]_{\le j}:\ \textstyle\sum_x (f+zg)(x)\,x^r L(x)=0,\ 0\le r<t\},$$
  a space of codimension $\le t$ (this is the $A(\ell)+zB(\ell)=0$ condition of `sec:aperiodic-hankel-certificates`; each split locator pays for at most one slope by `lem:one-support-one-line`, so slopes are dominated by *aligned* split locators, the objects of the v13 moment calculus).

The master statement both would follow from, in its cleanest speculative form:

> **Master flatness (target).** There is $P$ with: for every $1\le s\le j$ and every affine subspace $\mathcal A$ of the monic degree-$j$ polynomials over $\mathbb B$ of codimension $s$,
> $$\left|\{L\in\mathcal A:\ L\mid X^n-1\}\right|\ \le\ P(n)\Big(\binom nj |\mathbb B|^{-s} + 1\Big).$$

The first term is the density heuristic ("linear conditions on split locators behave like random conditions, up to poly"); it crosses $1$ exactly at the entropy–subfield envelope, which is why this single statement simultaneously gives (Q) asymptotically (apply to prefix spaces; the poly is absorbed by the reserve) and the per-slope half of (A) above the envelope. It is a growing-dimensional local limit theorem at critical density — the file's phrase "aperiodic M1 local limit" is exactly this. It will not fall to one blow; the routes below carve it up.

---

## 1. Strategy for legacy `(A)`, now feeding BC and SP

### 1.1 Regime split, and what is already covered

With `thm:mca-from-ca` (MCA $=$ CA $+$ explicit tangent term for $2r\le n-k$, i.e. $a\ge\lceil(n+k)/2\rceil$) and the pencil shape $t\ \lessgtr\ j$ (overdetermined iff $2a\ge n+k+1$), the band splits into:

| region (rate $\tfrac12$) | status |
|---|---|
| $a\ge n-\lfloor(n-k)/3\rfloor$ ($\delta\le\tfrac16$) | closed unconditionally, `thm:deep-mca` |
| $\lceil(n+k)/2\rceil \le a$ ($\delta\le\tfrac14$) | CA-form by `cor:band-reduction`; poly numerators from the BCIKS import on the Johnson range; self-contained via `thm:elementary-ca` below half-Johnson |
| $k+g^*n+R < a < \lceil(n+k)/2\rceil$ ($\delta\in(\tfrac14, 0.4679)$) | **the true kernel**: underdetermined pencils, $t<j$, beyond Johnson |
| $a \le k+g^*n$ | *unsafe*, exponential aperiodic mass (Task A0) — nothing to prove |

So (A) decomposes into: **(A-I)** finishing the chart atlas in the overdetermined half so the CA-reduction becomes airtight and self-contained, and **(A-II)** the underdetermined band, which is the genuinely new mathematics.

### 1.2 (A-I) Finishing the overdetermined atlas: two lemmas that are provable now

**Lemma A.1 (identically-split top charts collapse to tangent pairs).** *Claim: in case (b) of `thm:v13-spi` (all pseudo-division remainders $R_m\equiv0$), the pair $(f,g)$ is a tangent pair off a fixed co-support $T^*$ of size $j$, and hence contributes at most $j$ MCA-bad slopes at any agreement $\ge a$ in the overdetermined range.*

*Proof sketch.* On the top chart $\{c_j\ne0\}\subseteq\mathbb A^1_{\bar{\mathbb F}}$ (cofinite, hence irreducible and connected), $z\mapsto \widehat L_z := L_z/c_j(z)$ is a regular map whose image lies, by hypothesis (b), inside the *finite* set of monic split divisors of $X^n-1$. A morphism from an irreducible variety to a finite set is constant, so $\widehat L_z\equiv L^*$ for a single split $L^*$ with root set $T^*$, $|T^*|=j$. Evaluating the kernel identity $\big(H(u)+zH(v)\big)\widetilde\ell^*=0$ at two $\mathbb F$-points of the chart (available since $q>\deg c_j$) gives $H(u)\widetilde\ell^*=H(v)\widetilde\ell^*=0$ separately. By the exact kernel identification $S_R(w)=0\iff w\in C\oplus\mathbb F^R$ (the Vandermonde surjectivity computation inside the proof of `thm:v13-first-moment`, valid because $t\ge j$ here), both $f$ and $g$ agree with codewords off $T^*$. The tangent-slope count is then Step 3 of `thm:deep-mca` / part (a) of `thm:mca-from-ca`, whose hypothesis $2j\le n-k$ holds throughout the overdetermined half. $\square$

This closes a **named residual branch** — exactly the "identically split top charts … must be retained as a named residual branch" caveat of `thm:v13-spi` — by pure connectedness, with no counting. It should be the first thing written up; it is also a template: *any* chart whose locator family is forced to be split identically collapses the same way.

**Lemma A.2 (Kronecker / Berlekamp–Massey normal form for the singular buckets).** The kernel of a finite Hankel section $H_{t,j}(y)$ is a degree-truncated module over $\mathbb F[X]$ with at most two canonical generators (the Padé/BM minimal pair of the syndrome sequence); an identically rank-deficient pencil (`lem:singular-pencil` class (0)) is classified by the Kronecker minimal indices of $M(Z)$, and its per-slope kernel is spanned by specializations of finitely many polynomial vectors $v^{(i)}(Z)$ of degrees $\varepsilon_i$. Consequences to extract:

* *Bounded corank:* if the generic corank $d_0$ is $O(1)$, `thm:v13-fixeddim` bounds split points per slope by $\binom{n}{d_0}=\mathrm{poly}$, and the rank-drop slopes are finitely many (roots of the gcd of the nonvanishing minors, per the canonical rank-drop gcd machinery of v12). Deliverable: an explicit corank-stratified ledger extending `thm:v13-spi` past deficiency one.
* *Deep corank:* deep Hankel corank means small linear complexity of the syndrome sequence, i.e. a low-degree minimal annihilator $\Lambda_{\min}(z)$, and the kernel is $\Lambda_{\min}\cdot\mathbb F[X]_{\le j-\lambda}$ plus a bounded correction. Split members then factor as $\Lambda_{\min}\cdot(\text{split cofactor})$, so either $\Lambda_{\min}$ is itself split — a *tangent-type* charge, feeding Lemma A.1's mechanism — or the bucket is empty. Deliverable: "deep-corank dichotomy" lemma. References to mine: Heinig–Rost on Hankel/Toeplitz kernel structure; Kronecker pencil theory; the BM two-generator theorem.

**Task A.3 (annulus MCA-from-CA).** Extend `thm:mca-from-ca` slightly below half distance by replacing the single explanation pair with the *explanation cluster*: at column radius $\delta$ with $2r>n-k$, distinct pair-explanations differ by codeword pairs of column weight $\le 2r$, and the cluster size is bounded by the interleaved Johnson list `thm:johnson-list` as long as $n-2r > \sqrt{(k-1)n}$. Conjectured shape: $\varepsilon_{\rm mca}\le \varepsilon_{\rm ca} + |{\rm cluster}|\cdot r/q$. This buys the MCA layer on $(\sqrt{kn},\,(n+k)/2)$ agreements and cleanly isolates the CA question as the only remaining one down to the Johnson agreement. Low risk, moderate value.

### 1.3 (A-II) The underdetermined band: three routes to the master flatness

Here $t<j$; per slope, $W_z$ has positive dimension $d\approx n+k-2a$ (growing), and badness needs an *aligned* split locator. Three complementary attacks; run them in parallel, they share infrastructure with (Q).

**Route α — analytic local limit theorem (power-sum linearization).**

1. *Newton dictionary.* For $\mathrm{char}\,\mathbb B = p > w$ (deployed: $p\approx2^{31} > w\approx 6.75\cdot10^4$; state it as a standing hypothesis), the top-$w$ coefficient prefix of $\Lambda_M$ is triangularly equivalent to the first $w$ power sums $p_i(M)=\sum_{x\in M}x^i$. The prefix map becomes the **moment map** $M\mapsto \sum_{x\in M}\gamma(x)$, $\gamma(x)=(x,x^2,\dots,x^w)$: a sum, over a uniform $m$-slice without replacement, of points on the moment curve over the multiplicative coset. Crucially these are *degree-one statistics of the slice* — the exact setting of the Johnson-scheme tools v13 pre-positioned (`prop:v13-johnson-exchange`, checklist item 9).
2. *Exact ensemble identity.*
 $$N_w(z) = |\mathbb B|^{-w}\sum_{\lambda\in\mathbb B^w}\psi(-\lambda\cdot z)\,[T^m]\prod_{x\in D}\big(1+T\,\psi(f_\lambda(x))\big),\qquad f_\lambda=\textstyle\sum_i\lambda_i X^i.$$
 Major arc $\lambda=0$ gives the density term. Minor arcs need a per-frequency saving governed by the *value-distribution defect* of $f_\lambda$ on $D$: an "Esseen/Halász for slice sums" lemma of the shape $\big|[T^m]\prod(1+T\psi)\big| \le \binom nm e^{-c\,m\,\delta_\lambda}$ with $\delta_\lambda$ the concentration defect of $\{f_\lambda(x)\}_{x\in D}$.
3. *Where it is hard, precisely.* Weil/twisted complete sums control $\delta_\lambda$ only for $\deg f_\lambda \lesssim n/\sqrt p$ ($\approx 2^{5.5}$ at deployed sizes) — a vanishing sliver of the $w\approx2^{16}$ frequencies. Worse, the problem sits at *critical density*: the total entropy $\log_2\binom nm\approx m\cdot1.876$ bits barely exceeds $w\log_2 p$, so a lossless LLT is exactly as strong as the frontier conjecture itself. **Therefore Route α should target only the reserve form**: max-fiber $\le$ average $\cdot\,\mathrm{poly}(n)$, consumed at $a_0+R$, $R=\Theta(\log n)$, as in the v13 raw conditional closure theorem. The model results to adapt are the inverse Littlewood–Offord theory (Halász over $\mathbb F_p^d$, Nguyen–Vu / Tao–Vu inverse theorems) pushed to growing $d=w$, with the structural conclusion ("the increments live in a small generalized progression") checked against the only structures the moment curve over a multiplicative coset admits — subgroup/quotient strata — via sum-product inputs (Bourgain–Glibichuk–Konyagin, Shkredov; note $n\approx p^{0.68}$, a *large* subgroup, the favorable regime).
4. *Second moment for free.* The $L^2$ input of this route is exactly the collision ledger Q1 below — write it once.

**Route β — inverse theorem via incidence geometry and compression ("exchange-rigidity").**

By `lem:v13-concurrency`, split points of $\mathbb P(W)$ are the points lying on $\ge j$ hyperplanes of the arrangement $\{E_x\}_{x\in D}$ — and the normals $(1,x,\dots,x^j)$ make this the **moment-curve (osculating) arrangement**, the most generic one: any $\dim+1$ of the $E_x$ are independent (Vandermonde). The fixed-dimensional theorem `thm:v13-fixeddim` is the base camp: its drop-set injection $[L]\mapsto S_0$, $|S_0|=d$, is lossless but ignores that drop-sets of different rich points cannot pack freely. The program:

* *Step β1 (packing upgrade).* After gcd-trivialization (`lem:v13-gcd`), two split points of $W$ with root sets $R\ne R'$ satisfy structured intersection constraints; feed the drop-set family into the anticode bound `prop:v13-anticode` and the Johnson-exchange spectral bound `prop:v13-johnson-exchange` to replace $\binom nd$ by $\binom nd/\binom{j-\text{overlap}}{\cdot}$-type ratios. This will not reach poly alone but quantifies how far the moment-curve rigidity carries.
* *Step β2 (compression / extremality).* Define exchange operators on families of split locators (one root swapped along the Johnson graph) and attempt a rearrangement principle: **exchanges toward graded/periodic configurations do not decrease the number of split points compatible with a codimension-$s$ condition.** If true, the extremizers of the master flatness are exactly the prefix-affine and quotient-pulled-back spaces — i.e. the strata already charged to the reserve and to the quotient ledger — and the primitive remainder is poly (in fact the constant comes out sharp). This is the file's "exchange-rigidity input" made precise. Flag prominently: *the finite form of this extremality statement is essentially equivalent to the finite frontier conjecture* of the v13 raw manuscript; a counterexample to compression is a construction beating $g^*$, i.e. a refutation of the frontier — either outcome is decisive, so the search is not wasted in any world (see experiments, §3).

**Route γ — dyadic renormalization (deployed rows only, but poly-friendly).**

For $n=2^{21}$, $k=2^{20}$: $\gcd(n,k)=k$, so *every* dyadic seam is rate-preserving by `lem:v13-gap2`, and splitness is the iterated-squaring condition $X^{2^{21}}\equiv1 \pmod L$ — a $21$-rung tower. The key arithmetic observation: **a multiplicative loss of $C$ per rung compounds to only $C^{\log_2 n}=n^{\log_2 C}$ — polynomial.** So a rung-transfer inequality of the shape

$$\left|\{\text{aperiodic bad slopes at }(n,k,a)\}\right|\ \le\ C\cdot\left|\{\text{bad slopes at }(n/2,k/2,\lceil a/2\rceil)\}\right|\ +\ \mathrm{poly}(n)$$

suffices for the asymptotic (A) on these rows, with `thm:fiber-descent` supplying the exact periodic part of the transfer and the planted machinery (`thm:v13-planted`, `prop:v13-dyadic-planted`) the small-defect strata. The obstruction is definitional — aperiodic supports do not descend — so the content is a *stability* step: witnesses that survive folding by $\mu_2$ ($x\mapsto x^2$ fibers $\{x,-x\}$) are near-periodic and chargeable; witnesses destroyed by folding must be shown to inject, with controlled multiplicity, into a rung-below problem via their folded multiset plus a defect certificate. Speculative, but it is the route most consonant with the paper's dyadic, exact-certificate culture, and the only one where "constant loss per step" is good enough.

### 1.4 Deliverable ladder for legacy `(A)` / BC-SP

1. **Now:** Task A0 (band normalization + identity-scale refutation write-up); Lemma A.1 (split-top-chart collapse); rung-margin audit (shared with Q0).
2. **Short term:** Lemma A.2 (Kronecker/BM atlas, corank ledger); Task A.3 (annulus MCA-from-CA); the exact collision ledger (Q1).
3. **Main effort:** Route α reserve-form flatness (asymptotic (A) above envelope $+\,n^{o(1)}$ reserve); Route β compression program with small-$n$ falsification search; Route γ rung-transfer for the deployed rows.
4. **Stretch:** master flatness with $O(\log n)$ reserve and explicit constants (feeds Q3).

---

## 2. Strategy for (Q)

### 2.1 (Q0) Formal target and two immediate audits

**Target.** Let $\Phi_w$ be the graded-prefix (equivalently, moment) map on $m$-subsets of $D$, $\mathrm{avg}:=\binom Nm/|\mathbb B|^w$ per `prop:graded-prefix-floor` conventions (and its $c=1$, planted, and remainder variants). Define

* **(Q-fin)** $\max_z |\Phi_w^{-1}(z)| \le \kappa\cdot\mathrm{avg}$ with $\kappa\le 2^{\text{fail margin}}$ (roughly $2^{22.2}$ for KoalaBear MCA, $2^{22.0}$ for KoalaBear list, $2^{3.3}$ for Mersenne-31 MCA, and $2^{3.1}$ for Mersenne-31 list), **plus** the same for the whole divisor-lattice/planted union at $a_0+1$;
* **(Q-asy)** the same with $\kappa=\mathrm{poly}(n)$, consumed at reserve $R\gg\log n$.

**Audit 1 (rung margins — pure exact arithmetic, do first).** The upper ledger at $a_0+1$ is a union over scales $c\mid n$ and slack profiles. Each rung's own floor/budget comparison lives at $\sim1/c$ of the identity row's bit scale, so rung fail margins can shrink toward sub-bit values. Compute, by the existing exact-integer scanner, every rung's comparison at $a_0+1$ for all four rows. If any rung is tight or inverted, the adjacent-pair conjecture is threatened from the *periodic* side — a cheap potential refutation that must be excluded before investing in the analytic work. The v13 raw exact certificates already show the proposed `c=2` and planted rows are dominated at the moved unsafe edge; the audit extends this one step up, over all $c$.

**Audit 2 (support vs image).** The intrinsic periodic support count at $a_0+1$ is astronomically above budget ($\sim10^6$ bits against a $58$-bit MCA budget), so the quotient bucket **cannot** be paid at support level; it must be paid at image level by descent, i.e. as a recursion down the divisor lattice whose per-rung losses *add in bits*. With $21$ rungs and only $3.1$--$3.3$ bits on the Mersenne rows, finite quotient descent must be extremely close to lossless; with the $22$-bit KoalaBear margins it still cannot tolerate a hidden factor of $n$. Conclusion to record: **(Q-fin) demands a near-lossless recursion**, which forces the hybrid design of §2.4: exact enumeration below a cut scale, theorems above it.

### 2.2 (Q1) The exact collision ledger — provable now, shared with Route α

**Rigidity lemma (distance of the prefix code).** If $M\ne M'$ are $m$-subsets with $\Phi_w(M)=\Phi_w(M')$, write $\Lambda_M=GA$, $\Lambda_{M'}=GB$ with $G=\gcd$ split and $A,B$ coprime split of degree $e$. Equal monic-plus-$w$ prefixes give $\deg(\Lambda_M-\Lambda_{M'})\le m-w-1$, hence $\deg(A-B)\le e-(w+1)$: so $e\ge w+1$, i.e. **colliding subsets differ in at least $w+1$ points on each side** — strictly stronger than the BCH bound $e\ge w/2+1$ for this $\{0,1\}$-restricted problem, because both locators are split. Minimal collisions ($e=w+1$) satisfy $A-B=\text{const}$: "constant-shift split pairs," whose prototypes $X^{w+1}-c$ vs $X^{w+1}-c'$ exist iff $(w+1)\mid n$ — the quotient stratum, as it must be.

**Deliverable.** The exact second moment $\sum_z N_w(z)^2$ (equivalently, the number of prefix-collision pairs), stratified by $e=|M\setminus M'|$ and by the periodicity scale of the difference, computed by the same gcd/quotient reductions (`lem:v13-gcd`, `lem:v13-quot-pullback`) and verified by small-field enumeration. This is the *fixed-weight, without-replacement* analog of `thm:v13-second-moment`/`cor:v13-exact-variance` — the file's moment calculus one level up — and it yields immediately:

* an $L^2$ flatness constant, hence a **typical-$z$ equidistribution theorem** (most fibers within $1\pm\varepsilon$ of average). Not worst-case, but it calibrates every constant downstream, powers the moment ladder, and already upgrades any average-case or randomized reading of the ledger;
* the second-moment input of Route α.

### 2.3 (Q2) Heavy-fiber symmetry descent — the main architecture for worst-case

Bounded moments alone cannot finish: from $r$-th moments, $\max_z N \le \mathrm{avg}\cdot O\!\big(|\mathbb B|^{w/r}\big)$, and $|\mathbb B|^{w/r}$ is enormous for any computable $r$ — record this **moment barrier** explicitly so nobody chases it. The way moments *do* contribute is by making heavy fibers *few*, and then symmetry converts fewness into structure:

1. **Few heavy fibers.** Exact $r=3,4$ collision ledgers (triples/quadruples of split locators with pairwise deep prefix agreement — the pairwise-gcd lattice is literally the sunflower geometry of `sec:v13-l1`, reusable as-is) give $\left|\{z: N_w(z)\ge T\cdot\mathrm{avg}\}\right| \le (\text{excess})/T^r$.
2. **Symmetry forces structure on heavy $z$.** For $\zeta\in\mu_n$, $M\mapsto\zeta M$ is a slice bijection with $p_i(\zeta M)=\zeta^i p_i(M)$: the twist action $z_i\mapsto\zeta^i z_i$ **permutes fibers preserving sizes**. If heavy fibers number fewer than the generic orbit size, each heavy $z$ has twist-stabilizer $\mu_{M_0}$ with $M_0=\gcd(n,\{i\le w: z_i\ne0\})$ large — i.e. **$z$ is supported on $M_0$-divisible indices: a quotient-pulled-back prefix**, precisely the `lem:v13-quot-pullback` shape. Frobenius $x\mapsto x^p$ (permuting $\mu_n$, acting on the index set) and inversion/complementation ($\Lambda_{D\setminus M}=(X^n-1)/\Lambda_M$, exchanging prefixes and tails) give further, independent constraints; catalogue them once.
3. **Divisor descent.** A stabilized heavy fiber is an *almost-periodic moment fiber*: conditions $p_i(M)=0$ for $M_0\nmid i$, $i\le w$, plus a genuine prefix condition at scale $n/M_0$. This is not a clean bijection onto the quotient rung (only $w$ of the $n$ vanishing conditions are imposed), so stratify by folding defect: small defect goes to the quotient rung plus planted charts (`thm:v13-planted` again); large defect re-imposes an aperiodicity-type constraint one rung down — renormalize (Route γ's transfer inequality reappears; per-rung constant losses are poly-acceptable in the asymptotic reading and must be tracked in bits for the finite one).
4. **Base of the recursion.** The fully stabilized fiber is $z=0$: subsets with vanishing first $w$ power sums — weight-$m$ $\{0,1\}$-words in the cyclic code with zeros $\zeta,\dots,\zeta^w$ (a BCH-dual weight-enumerator problem). This is a useful terminal cell, but it is **not** automatically the global maximum: the `F_17^*`, `m=9`, `w=1` counterpacket has nonzero primitive fibers of size `673` and the null fiber of size `672`.

The corrected output of Q2, if it goes through: **worst-case flatness reduces to primitive max-orbit flatness plus stabilized-orbit descent**, with the null fiber only one terminal cell. That is still a concrete symmetric object, but the maximum must be taken over primitive twist orbits rather than assumed at zero.

### 2.4 (Q3) The finite adjacent pair: extremality or repositioning

Two honest facts frame the endgame:

* Constant-factor flatness at the Mersenne margins ($\kappa<10$) cannot come from moments (§2.3 barrier) nor from any soft LLT at critical density (§1.3, Route α, point 3). Even the KoalaBear margins require printed constants, not an unspecified polynomial. The finite route therefore requires an **exact extremality statement** or a very tight certified partition.
* The raw **mode-at-null** shortcut is false: over `D=F_17^*`, `m=9`, `w=1`, the first-power-sum fibers have `N_9(0)=672` and `N_9(s)=673` for every `s≠0`. The correct finite candidate is **primitive max-orbit flatness**: after quotient-stabilized target vectors are routed to their rungs, the maximum over primitive twist orbits is at most `κ·avg` with the printed row margin. A Route β compression theorem may still prove this, but it must control primitive orbits, not merely push mass to the null fiber.

Recommended posture, matching the v13 raw asymptotic-versus-finite split:

1. Prove (Q-asy) via Q1+Q2 (+Route α second moments) — this, with the asymptotic BC/SP package, closes the **asymptotic frontier** with logarithmic reserve.
2. Reduce (Q-fin) to: (i) primitive max-orbit flatness (or a Route β compression statement implying it after quotient routing), and (ii) explicit stabilized-orbit descent bounds for nonprimitive targets. State both as named conjectures with the printed margins as acceptance thresholds, exactly in the paper's certificate grammar (`sec:v13-packet-schema`: named residuals, never point estimates).
3. Prioritize the two KoalaBear rows first (`22.2` and `22.0` bits of next-step room), because they are the most forgiving finite constants. The Mersenne-31 rows (`3.3` and `3.1` bits) should be assumed out of reach of anything but exact extremality or a very tight certified partition.

---

## 3. Shared infrastructure, experiments, integration

**Write-once components.** The collision ledger (Q1) is simultaneously Route α's second moment and the calibration of Route β's compression tests. The rung-transfer machinery (Route γ) is the same recursion as Q2's divisor descent. The symmetry catalogue (twist, Frobenius, inversion/complementation) serves both.

**Experiments (all within the paper's exact-enumeration culture, extending the $\mathbb F_5/\mathbb F_7/\mathbb F_{13}/\mathbb F_{17}$ verifications):**

1. *Max-fiber tables.* For small $n$ (say $n\le 40$, all divisors, several $(m,w)$), enumerate $N_w(z)$ for all $z$: measure $\max/\mathrm{avg}$ against $\binom Nm/|\mathbb B|^w$, classify the heavy fibers by twist stabilizer, and keep the `F_17^*`, `m=9`, `w=1` mode-at-null failure as a regression test.
2. *Compression falsification search.* Random and structured exchange sequences on split families under codimension-$s$ conditions, watching for count decreases toward graded configurations. A robust violation is a candidate construction beating $g^*$ — i.e. progress on refuting the frontier conjecture rather than proving it; either way decisive.
3. *Rung-margin audit* at deployed sizes (Q0, Audit 1) — no new mathematics, potentially veto-level information.
4. *Witness-bucket check* for Task A0 (aperiodicity of the converted pole-line witnesses) at small fields.

**Integration map.** Lemma A.1 and A.2 discharge residual split-pencil branches and sharpen the overdetermined half of BC; Task A.3 upgrades the MCA-from-CA annulus; Route α/β/γ outputs enter as the upper staircase \(U\) used by the v13 raw finite adjacent compiler; Q1/Q2 populate the quotient/prefix ledger at image level; the finite-pair conjectures of Q3 replace any "unspecified polynomial factor" with named, margin-quantified inputs. The final v13 raw closure consumes Q, BC, and SP only.

**Risk register.**

| item | risk | failure meaning |
|---|---|---|
| A0, A.1, audits | low | — |
| A.2, A.3, Q1 | low–medium | technical only |
| Route α reserve-form | high | LLT in growing dim beyond current inverse-LO technology → fall back to $n^{o(1)}$-reserve or typical-$z$ statements |
| Route β compression | high | violation ⇒ frontier conjecture false ⇒ new unsafe mass beyond $g^*$ (publishable refutation) |
| Route γ transfer | medium–high | defect strata may not inject with bounded multiplicity |
| Q2 descent | medium | defect expansion may leak poly factors per rung — fatal only for (Q-fin) |
| (Q-fin) primitive max-orbit flatness | open conjecture | finite pair stays conditional; reposition closing as asymptotic theorem + certified-computation program |

**Bottom line.** Both missing inputs are shadows of one object — flatness of split-locator counts against affine conditions at the entropy–subfield critical density — with the quotient/graded strata as the expected extremizers and primitive twist orbits as the finite Q battleground. The asymptotic forms are attackable now along three mutually reinforcing routes whose first rungs (A0, A.1, A.2, Q1, the audits) are provable with the machinery already in v12/v13. The finite adjacent pair is *not* an analytic problem: it is an extremality problem, and the strategy above names the exact statement (primitive max-orbit flatness / exchange-compression) whose proof — or whose small-$n$ refutation — decides it.
