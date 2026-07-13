# General-R constant-Weil cycle flatness

## Claim

Let \(B_\nu\) be finite fields of odd characteristic \(p_\nu\), with
\(|B_\nu|=Q_\nu\).  Let

```text
D_nu = theta_nu H_nu subset B_nu^x,
T_nu = D_nu \ P_nu,
N_nu = |T_nu| -> infinity,
```

where \(P_\nu\) is an allowed planted exceptional set.  Choose integers
\(1\le R_\nu<p_\nu\), fix \(0<\alpha<1/2\), and take

```text
alpha <= m_nu/N_nu <= 1-alpha.
```

On \(\Omega_\nu=\binom{T_\nu}{m_\nu}\), define the polynomial-prefix map

\[
 g_\nu(t)=(t,t^2,\ldots,t^{R_\nu}),\qquad
 \Phi_\nu(S)=\sum_{t\in S}g_\nu(t)\in B_\nu^{R_\nu},\qquad
 M_\nu=\binom{N_\nu}{m_\nu}.
\]

Let \(C_0\) be the absolute mixed-Weil constant used by
`prop:weighted-weil-minor-arcs`, and put

\[
 \Lambda_\nu=C_0(R_\nu+1)\sqrt{Q_\nu}+|P_\nu|.
 \tag{1}
\]

Assume that a fixed \(\lambda<1/2\) satisfies
\(\Lambda_\nu/N_\nu\le\lambda\) eventually.  For natural-log binary entropy
\(h\), define

\[
 \delta_{\alpha,\lambda}
 =\min_{\alpha\le x\le1/2}
 \left\{
 h(x)-(x+\lambda)h\!\left(\frac{x}{x+\lambda}\right)
 \right\}>0.                                             \tag{2}
\]

For \(f_\lambda(x)=h(x)-(x+\lambda)h(x/(x+\lambda))\), direct calculation
gives \(f_\lambda''(x)=-1/(1-x)-1/(x+\lambda)<0\).  Moreover
\(f_\lambda(0)=0\), while, with \(t=2\lambda\in(0,1)\),

\[
 2f_\lambda(1/2)=t\log t-(1+t)\log(1+t)+2\log2>0,
\]

because the displayed expression decreases to zero at \(t=1\).  Strict
concavity therefore gives \(f_\lambda(x)>0\) for \(0<x\le1/2\), proving the
sign in (2).

If

\[
 \limsup_{\nu\to\infty}\left(
    \frac{R_\nu\log Q_\nu}{N_\nu}
    +\frac{3\log2}{2p_\nu}
 \right)<\delta_{\alpha,\lambda},                        \tag{3}
\]

then the effective span is the full ambient target
\(V_{g_\nu}=B_\nu^{R_\nu}\), and there is \(c>0\) such that, uniformly in
\(z\in B_\nu^{R_\nu}\),

\[
 \left|
 |\Phi_\nu^{-1}(z)|-\frac{M_\nu}{Q_\nu^{R_\nu}}
 \right|
 \le e^{-cN_\nu}\frac{M_\nu}{Q_\nu^{R_\nu}}.             \tag{4}
\]

Consequently the realized image is exactly \(B_\nu^{R_\nu}\) for all
sufficiently large rows.  Every first-match residual
\(\Omega_\nu^\circ\subseteq\Omega_\nu\) obeys

\[
 \max_z|\Omega_\nu^\circ\cap\Phi_\nu^{-1}(z)|
 \le(1+e^{-cN_\nu})\frac{M_\nu}{Q_\nu^{R_\nu}}.           \tag{5}
\]

The convenient sufficient conditions

\[
 p_\nu\to\infty,\qquad
 R_\nu\log Q_\nu=o(N_\nu),\qquad
 \Lambda_\nu/N_\nu\le\lambda<1/2                         \tag{6}
\]

therefore pay effective image-scale Fourier flatness.  Unlike the printed
shallow theorem, (3) permits \(R_\nu\sqrt{Q_\nu}\) to be a fixed positive
fraction of \(N_\nu\), provided that fraction is below the entropy gate through
(1).

## Status

**PROVED**, conditional only on the same classical mixed multiplicative-
additive Weil estimate used by the integrated weighted-Weil proposition.
The coefficient theorem, full-effective-span argument, quantitative gate, and
fixed-characteristic family below are **PROVED**.  This is a special-class
payment toward maintainer hard input 2, not a general primitive-leaf closure.

The Codex team developed and independently audited this extension; integrated
PR #718 is its direct (R=2) predecessor.

## Parameters

- Field tower: \(B_\nu\), cardinality \(Q_\nu\), odd characteristic \(p_\nu\).
- Domain: unweighted multiplicative cosets with allowed planted deletions,
  \(T_\nu=\theta_\nu H_\nu\setminus P_\nu\).
- Prefix depth: any sequence \(1\le R_\nu<p_\nu\) satisfying (1)--(3), not
  only \(R=2\).
- Slice: \(N_\nu=|T_\nu|\) and
  \(\alpha\le m_\nu/N_\nu\le1-\alpha\).
- Effective and realized image: both are proved to be \(B_\nu^{R_\nu}\), of
  size \(Q_\nu^{R_\nu}\).
- Source-prescribed average fiber: \(M_\nu/Q_\nu^{R_\nu}\).
- No code rate, agreement radius, list/interleaving arity, challenge
  denominator, or deployed-row parameter is changed or inferred.

## Existing paper dependency

The exact characteristic-cycle factor comes from the integrated
`experimental/notes/thresholds/r2_constant_weil_cycle_flatness.md`
(source commit `6588d8d6c393df81642dafafc82c70f565d009cf`).  PR #718, integrated
into `main` by `c23dcaa`, removes that theorem's bounded-\(N/p\) restriction
at \(R=2\).  The present theorem
extends the same exact cycle compression to every polynomial-prefix depth
\(1\le R<p\) and supplies a fixed-characteristic family for \(R\ge3\) as well.

The printed `thm:unconditional-shallow-mi-ma` already handles general \(R\)
when \(R\sqrt Q=o(N)\).  It does not cover the constant-Weil-ratio family below,
where \(R\sqrt Q/N\to R/d>0\).

The statement of `prop:weighted-weil-minor-arcs` assumes \(m<p\).  This packet
does not invoke that statement outside its scope.  It reapplies the same
classical mixed-Weil proof separately to every cycle index \(j\) with
\(p\nmid j\); cycles with \(p\mid j\) are evaluated exactly.  This is the direct
cycle-by-cycle certificate requested by `rem:small-characteristic-cycles`.

## Proof idea or experiment

Suppress \(\nu\), fix a nontrivial additive character \(\psi\) of \(B\), and
write, for \(\mathbf a=(a_1,\ldots,a_R)\ne0\),

\[
 P_{\mathbf a}(X)=\sum_{s=1}^{R}a_sX^s,\qquad
 x_t=\psi(P_{\mathbf a}(t)-P_{\mathbf a}(t_0)).
\]

The degree \(d=\deg P_{\mathbf a}\) lies in \(1\le d\le R<p\).  Its pole at
infinity has order \(d\), so \(P_{\mathbf a}\) is not Artin--Schreier.  For
\(p\nmid j\), the same is true of \(jP_{\mathbf a}\), and the multiplicative-
coset character expansion plus mixed Weil gives

\[
 \left|\sum_{t\in T}x_t^j\right|\le
 C_0(d+1)\sqrt Q+|P|\le\Lambda.                          \tag{7}
\]

For \(p\mid j\), additive-character values have \(p\)-torsion, hence

\[
 \sum_{t\in T}x_t^j=N.                                  \tag{8}
\]

The bound at \(j=1\) also proves the full effective span.  If a nontrivial
ambient character annihilated \(V_g\), then its value on every
\(g(t)-g(t_0)\) would be one, making the left side of (7) equal to \(N\).
But \(\Lambda<N\) follows eventually from \(\Lambda/N\le\lambda<1/2\), a
contradiction.  Nondegeneracy of the trace pairing therefore gives
\(V_g=B^R\).

Let \(r=\min(m,N-m)\), put

\[
 \beta=\frac{N-\Lambda}{p}>0,\qquad
 L=\left\lfloor\frac rp\right\rfloor.
\]

Newton's generating identity, (7), and (8) give

\[
 |e_r(x_t:t\in T)|\le B_r,\qquad
 B_r=[v^r](1-v)^{-\Lambda}(1-v^p)^{-(N-\Lambda)/p}.       \tag{9}
\]

Expanding (9), using monotonicity of
\(\binom{\Lambda+s-1}{s}\) for \(\Lambda\ge1\), and applying the generalized
hockey-stick identity yields

\[
\begin{aligned}
 B_r
 &\le\binom{\Lambda+r-1}{r}
      \sum_{\ell=0}^{L}\binom{\beta+\ell-1}{\ell}\\
 &=\binom{\Lambda+r-1}{r}\binom{\beta+L}{L}.              \tag{10}
\end{aligned}
\]

Moreover,

\[
 \binom{\beta+L}{L}\le2^{\lceil\beta\rceil+L}
 \le2^{1+3N/(2p)}.                                      \tag{11}
\]

For a finite row with \(1\le\Lambda<N\), define

\[
 \epsilon_{R,*}
 =\frac{Q^R-1}{\binom Nr}
   \binom{\Lambda+r-1}{r}
   \binom{\beta+\lfloor r/p\rfloor}{\lfloor r/p\rfloor}.
                                                               \tag{12}
\]

Fourier inversion on the now-proved full group \(B^R\), followed by
complementation when \(m>N/2\), gives the exact implication

\[
 \left||\Phi^{-1}(z)|-M/Q^R\right|\le\epsilon_{R,*}M/Q^R.
 \tag{13}
\]

Thus \(\epsilon_{R,*}<1\) is a finite full-image certificate.  For
\(x=r/N\in[\alpha,1/2]\), uniform Stirling comparison gives

\[
 \frac1N\log\epsilon_{R,*}\le
 -\left[h(x)-(x+\lambda)h\!\left(\frac{x}{x+\lambda}\right)\right]
 +\frac{R\log Q}{N}+\frac{3\log2}{2p}+o(1).              \tag{14}
\]

Equations (2)--(3) prove (4), and deletion cannot enlarge a full-slice fiber,
which proves (5).

### Fixed-characteristic extension tower

Fix \(\alpha\), an integer \(R\ge1\), and an integer

\[
 d>2C_0(R+1),\qquad
 \lambda_0=\frac{C_0(R+1)}d<\frac12.                    \tag{15}
\]

Dirichlet's theorem supplies arbitrarily large odd primes \(p\equiv1\pmod d\).
Choose one such prime, once and for all, so that

\[
 p>R,\qquad
 \frac{3\log2}{2p}<\delta_{\alpha,\lambda_0}.             \tag{16}
\]

For \(e\to\infty\), take

\[
 B_e=\mathbb F_{p^{2e}},\qquad
 Q_e=p^{2e},\qquad
 |H_e|=N_e=d(p^e+1),\qquad
 T_e=\theta_eH_e,\qquad P_e=\varnothing.                 \tag{17}
\]

Because \(d\mid p-1\mid p^e-1\), the order \(d(p^e+1)\) divides
\(p^{2e}-1\), so \(H_e\) exists.  The characteristic \(p\) is fixed along the
entire row sequence, while

\[
 \frac{\Lambda_e}{N_e}
 =\lambda_0\frac{p^e}{p^e+1}<\lambda_0,\qquad
 \frac{R\log Q_e}{N_e}\to0.                              \tag{18}
\]

Thus (16) makes (3) hold.  At the same time,

\[
 \frac{N_e}{p}\sim d\,p^{e-1}\to\infty,\qquad
 \frac{R\sqrt{Q_e}}{N_e}\to\frac Rd>0.                   \tag{19}
\]

This family is outside both the old bounded-\(N/p\) theorem and the shallow
\(R\sqrt Q=o(N)\) theorem.  It is not a proper-subfield disguise: the largest
proper subfield of \(\mathbb F_{p^{2e}}\) has at most \(p^e\) elements, whereas
\(|H_e|>p^e-1\).

## Ledger impact

- **Hard input 2:** pays effective image-scale MI with empty MA for the stated
  unweighted polynomial-prefix class at every \(1\le R<p\).
- **C9:** rules out positive exponential max-fiber excess on these leaves
  before a Sidon-energy split.
- **Small-characteristic cycles:** replaces an \(m<p\) blanket restriction by
  the exact characteristic penalty in (3) and (12).
- **Field ledger:** exhibits genuine fixed-characteristic extension towers,
  not only growing-prime rows.
- No first-match atlas, signed local-minority profile, C7 projection degree,
  balanced-core ray compiler, complete profile envelope, or lower reserve is
  claimed.

## Constants

- The exact finite certificate is \(\epsilon_{R,*}\) in (12).
- The entropy margin is \(\delta_{\alpha,\lambda}\) in (2).
- Any positive constant below
  \[
   \delta_{\alpha,\lambda}
   -\limsup\left(R\log Q/N+3\log2/(2p)\right)
  \]
  is an admissible decay exponent after one reduction to absorb uniform
  Stirling error.
- The fixed-characteristic construction keeps \(C_0\) symbolic.  Conditions
  (15)--(16), rather than any sampled numerical \(d\), are the theorem
  certificate.

## Reproducibility

```bash
python3 experimental/scripts/verify_general_r_constant_weil_cycle_flatness.py --check
python3 experimental/scripts/verify_general_r_constant_weil_cycle_flatness.py --tamper-selftest
(cd experimental/lean/grande_finale && lake env lean GrandeFinale/GeneralRConstantWeilCycleFlatness.lean)
```

The Lean companion is intentionally an unproved statement target.  Its clean
type-check certifies the transcription and package integration, not the proof.

The verifier checks (9)--(12) with exact `Fraction` arithmetic across varying
\(R\), including \(p\nmid N\), and replays the \(Q^R-1\) Fourier multiplier.  It
also checks prime-field effective-span examples and the subgroup, proper-
subfield, unbounded-\(N/p\), and non-shallow arithmetic of sample fixed-
characteristic towers.  Because \(C_0\) is unspecified, those samples are
arithmetic controls only; (15)--(16) remain explicit symbolic hypotheses in
the machine-readable certificate.

## Nonclaims

- No weighted rational chart or circle/twin-coset theorem is claimed.
- No claim is made for \(R\ge p\), where Artin--Schreier/Frobenius modes need a
  different coordinate system or a separate certificate.
- No automatic theorem for every fixed characteristic is claimed; the chosen
  prime must satisfy the explicit entropy gate (16).
- No deployed finite leaf, power-of-two prize row, finite threshold, Grand MCA,
  Grand List, or paper-TeX change is claimed.
