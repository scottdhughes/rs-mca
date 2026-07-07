# b2 / conj:Q proof route: the Sawin-adaptation map and the irreducible crux (2026-07-07)

- **Status:** proof-route scoping. Extraction of arXiv:1809.05137 (Sawin) mapped onto the
  b2/`conj:Q` object, numerically localized to its hardest obstruction. NOT a proof.
- **Companion:** `b2_literature_pioneer_verdict.md` (pioneer verdict), `b2_primitive_core_numerics.md`
  (exact counting engine), `b2_step0_object_pinned.md` (object/regime), holmbuar
  `cap25_v13_qfin_rung_audit.md` (dead-margin ledger).

## The route (from the Sawin extraction)

**Direct re-pointing is impossible (clean negative).** Sawin's variety is cut by "first `m`
elementary symmetric functions `= c`"; the cancellation comes from a **codimension bound on a
`p`-th-power bad locus** (Lemma 2.3: log-derivative degeneracy forces `prod(1-u a_i)` to be a
polynomial in `u^p`) + Katz/QST Betti counting + Weil II — **no monodromy computation** (so the
"full `S_n`" monodromy-blindness does NOT kill this route). But adding our constraint
`g | X^n-1` (i.e. `a_i in mu_n`) collapses the variety to **dimension 0**, where Weil II is
vacuous. Sawin gives short-interval *averages* over `q^h` polynomials, never one fixed polynomial.

**The machinery transplants onto the dual Fourier family.** Since `p_j(M)` is linear in `1_M`,
```
N = q^-w sum_{t in F_q^w} T(t),   T(t) = e_m({psi(P_t(a)) : a in mu_n}),   P_t = sum_{j<=w} t_j X^j,
```
and the single-frequency Weil sum controlling everything is `pi(t) = sum_{a in mu_n} psi(P_t(a))`.
The "singular locus" analogue is the **bad set of dual variables** `B = {t : pi(t) fails to cancel}`.
This is positive-dimensional (over `A^w_t`), so Sawin/Deligne/Katz can bite here even though the
primal variety cannot.

## The sub-lemma test (b2_badlocus_codim.py) and what it found

Proposed first sub-lemma: `dim B <= w-1` (codim >= 1). Numeric result (w=2,3; primes q with
`n` = largest 2-power | q-1):
- **The EXACT-degenerate locus is `{0}`** (`|pi(t)| = n`) in every row — `dim 0`, codim `w`. So
  the exact core of the sub-lemma is *trivially* true and gives nothing.
- The "near-degenerate" count is **governed by subgroup sparsity `n/q`, not codimension**: dense
  `mu_n` (n~q) gives `#bad = 1` (only t=0); sparse `mu_n` (n<<q) blows up — but there the bad
  threshold collides with the cancellation floor `~sqrt(n w)`, a finite-size artifact. The codim
  question is not cleanly testable at feasible n (same compute wall as the counting side).

## The irreducible crux (where the whole problem bottoms out)

**Sparse-subgroup incomplete-sum cancellation of a high-degree phase, in the dense large-`w`
regime.** Concretely: bound `pi(t) = sum_{a in mu_n} psi(P_t(a))` for `deg P_t = w` a positive
fraction of `n`, over the subgroup `mu_n` which at deployment is *extraordinarily sparse*
(`n = 2^21`, `q = p^6 ~ 2^186`, `n/q ~ 2^-165`). One-variable Weil gives `w sqrt q ~ 2^93`,
which **dwarfs the trivial bound `n = 2^21`** — Weil certifies nothing. This is exactly:
- Sawin's own theorem going trivial once the interval is too short (`(k+2)^{2n-h}` overwhelms `q^{h/2}`);
- the wall Sawin–Shusterman (arXiv:2512.24080) push against (they reach `X^{1/2}` only for large `q`,
  not-too-short intervals, "no Artin–Schreier factor"; and their sums are over *intervals*, not a
  multiplicative *subgroup* — the `mu_n` compatibility is itself unverified);
- the same `sqrt(p)` barrier CAP25 Rem 16.10 names, now pinned to its precise analytic form.

**Verdict:** beating this barrier in the dense regime is a **genuinely new idea (open even over
Z)** — a research-frontier problem, not a near-term theorem. All obvious routes are closed:
BGK (wrong regime), geometric monodromy (blind), Sawin-direct (dimension 0), moments/packing/
head-flatness (over budget, holmbuar #366), codim sub-lemma (trivially true, useless).

## Barrier-beating attack, prong 1: fiber concentration REDUCES the conjecture (2026-07-07)

`b2_fiber_concentration.py` computes the full fiber array `f(z) = #{M : Phi_w(M)=z}` exactly
(numpy DP) and its energy `E2 = sum_z f(z)^2`. Result (power-of-two n, dense regime):

| n | w | mean=C(n,m)/q^w | max f | conc=maxf/mean | E2/flat (avg flatness) |
|---|---|---|---|---|---|
| 16 | 1 | 673 | 673 | 1.00 | 1.000 |
| 16 | 2 | 27.7 | 32 | 1.15 | 1.004 |
| 16 | 3 | 0.89 | 3 | 3.37 | 1.702 |
| 32 | 2 | 5.0e4 | 51160 | 1.02 | 1.000 |
| 32 | 3 | 381 | 520 | 1.37 | 1.003 |
| 64 | 2 | 4.35e13 | 4.35e13 | 1.00 | 1.000 |

**Reading.** Concentration `conc` blows up ONLY as the mean fiber drops below ~1 (object going
sparse); while mean `>> 1` (dense) the fibers are near-perfectly flat (`E2/flat - 1 ~ 0.003` =
tiny relative variance). **The deployed regime is dense** (mean ~ `2^35.7`), and `n^3 = 2^63 >>`
mean, so IF `conc = f(0)/mean` stays `poly(n)` the conjecture holds with room to spare. Strong
evidence it is **true**.

**The precise reduction.** `f(0) = q^{-w}[C(n,m) + sum_{t != 0} T(t)]`, so
`extras <= n^3` follows from **cancellation of `sum_{t != 0} T(t)`**, i.e. equidistribution of
the moment map `Phi_w` at the special target `z=0`. This is a clean, single analytic statement.

**Why the 2nd moment cannot close it (confirms holmbuar #366).** `sum_t |T(t)|^2 = q^w E2` IS the
shift-pair count `sp_w` (holmbuar two-locator joint rank / Danny's SP). It controls only the
*average* flatness `Var(f)/mean^2` (tiny), NOT the specific-point fiber `f(0)`: Cauchy-Schwarz
gives fluctuation `<= mean * q^{w/2}` (the barrier, useless). So the barrier-beating idea must be
**cohomological, not moment-counting** — the naive moment hierarchy is dead (holmbuar's `r=5886`).

**The idea, crystallized:** prove subgroup equidistribution of the degree-`w` phase `P_t` on
`mu_n` via a **Sawin-Shusterman-type short-trace-function bound** (arXiv:2512.24080), generic-`t`
non-degeneracy supported by the bad-locus = {0} finding. Pivotal open question (under active
deep-read): does their bound survive on a MULTIPLICATIVE SUBGROUP (vs an interval), possibly after
completing the subgroup sum via the `(q-1)/n` characters trivial on `mu_n`?

## Sawin-Shusterman verdict: NO, and the redirect to the RIGHT object (2026-07-07)

Deep-read of arXiv:2512.24080 (Thm 1.3, 4 hypotheses verbatim): their short-trace-sum bound does
**NOT** prove our cancellation, over-determined:
- **Hypothesis 4 (slopes <= 1 at infinity) FAILS**: our phase `L_psi(P_t)` has slope
  `= deg P_t = w ~ 67471 >> 1`. This is their "most restrictive" hypothesis, and it is
  STRUCTURAL — their vanishing-cycles/translation-invariance engine is an equivalence of
  categories on the slope>1 part (line 1926), so the method breaks, not merely weakens.
- Wrong index set (short interval of polynomials, not a multiplicative subgroup); character
  completion `pi(t) = (n/(q-1)) sum_{chi in mu_n^perp} S(chi,t)` gives complete Weil sums `w sqrt q`
  (no gain) + a Mellin/vertical residual their theorem does not touch.
- **Hypothesis 3 (no Artin-Schreier factor) HOLDS for all t != 0** — matches our bad-locus = {0}.

**The redirect (the key output).** The object we need is NOT a horizontal short-sum bound but a
**vertical / big-monodromy equidistribution** of the family `{ L_psi(P_t) }_t` restricted to `mu_n`
(Katz-style) — a framework that CAN tolerate high slope. The precise missing lemma has three parts:
(1) multiplicative-SUBGROUP index (roots of `X^n-1`, the `G_m`/subgroup analogue of a short interval);
(2) HIGH-SLOPE tolerance (slope `= w >> 1`, a wild Artin-Schreier phase — new slope>1 cohomological
vanishing); (3) FAMILY uniformity over `t` to control `sum_{t != 0} T(t)`.

**Two live candidate frameworks (both handle the exact crux):**
- **(a) Katz big-monodromy** of the dual additive family `{L_psi(P_t)}_t` on `mu_n` (vertical/AG
  equidistribution). Distinct from the earlier BLIND pencil monodromy — this is the Fourier family.
- **(b) Bourgain-Chang / BGK sum-product** for polynomial phases on the sparse subgroup `mu_n`.
  Crucially NOT the L1 tiny-subgroup regime: `|mu_n| = q^{0.113} >= q^gamma`, so BGK-type is IN regime
  (the earlier "BGK wrong-regime" dismissal was for L1's tiny `ell`, not b2). Directly attacks the
  sparse-subgroup incomplete sum. Numerics already confirm generic-`t` cancellation (`|pi(t)| ~ sqrt(n w)`).

Which framework is viable + the precise first lemma: under comparative deep-read.

## What is banked (reusable for the community conj:Q effort)

Exact validated tooling (`b2_dense_extras.py`, `b2_primitive_core_scaling.py`,
`b2_badlocus_codim.py`), the pioneer literature map, the Sawin-adaptation analysis (primal
dim-0 obstruction + dual Fourier re-hosting), and the crux pinned to sparse-subgroup incomplete
sums. The next genuine step is inventing the barrier-beating idea (or importing one from a future
Sawin–Shusterman-type subgroup result) — long-horizon, coordinated on holmbuar's ledger.
