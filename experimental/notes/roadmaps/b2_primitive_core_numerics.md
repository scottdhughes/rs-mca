# b2 / conj:Q primitive-core numerics: exact engine + honest inconclusive verdict (2026-07-07)

- **Status:** numeric attack (Phase-0). Exact engine, 4-way cross-checked, Codex-green.
  Verdict on the conjecture: **INCONCLUSIVE** (deployed regime numerically unreachable).
- **Object:** `extras(n,m,w)` = #{ m-subsets M of mu_n : p_1(M)=...=p_w(M)=0, M has trivial
  stabilizer } = holmbuar's **subset-primitive core** of `conj:Q` (= the b2/`u2c_giant_tnull`
  object), for **power-of-two n** (deployed shape n=2^21). Conjecture: `extras <= n^3`.

## The engine (validated)

Two scripts, `experimental/scripts/`:
- `b2_dense_extras.py` — exact MITM count + coset-union (structured) split; the ground-truth
  cross-check. Codex-reviewed to green (prime-field guard, seeded mechanism sampling,
  overflow-safe log2 fiber, O(w(q-1)log q) primitive root).
- `b2_primitive_core_scaling.py` — the scaling engine. Two exact ingredients:
  1. `total_wnull(q,n,m,w)` via an exact **numpy DP over the power-sum residue vector**
     (state = (#chosen, (p_1..p_w) mod q); adding a point = a fixed index permutation).
     Breaks the 2^(n/2) MITM ceiling: O(n * m * q^w) time, **poly in n**.
  2. **Descent identity** (holmbuar `cap25_v13_qfin_rung_audit.md` (D)): for power-of-two n a
     nontrivial-stabilizer w-null M is mu_2-symmetric (odd moments auto-vanish, even ones
     descend), so `structured(n,m,w) = total_wnull(n/2, m/2, floor(w/2))` and
     `extras = total - structured`.

**Cross-checks (all exact-match):** DP total == MITM total and descent extras == MITM extras
at n=32 for w=1,2,3 (`5832096`, `50688/50624`, `512`); PARI independent count; sympy Newton
`e<->p`; Codex independent brute + signed-Fourier reconstruction. Four engines agree.

## The data and the wall

| n | q | w*(n) = min w with extras <= n^3 | note |
|---|---|---|---|
| 16 | 97 | 1 | object too small |
| 32 | 97 | 3 | extras 5.8e6 -> 5.1e4 -> 512 as w=1,2,3 |
| 64 | 193 | > 3 | extras still 1.9e11 >> n^3=2.6e5 at w=3 |

The crossover depth `w*(n)` **grows with n**. But `w*(64) > 3` is unreachable: the DP is
`q^w` in memory, and `w=4` at `q=193` is `1.4e9` states. w-null is a density-`q^{-w}` event,
so Monte-Carlo hits the same wall. **The exact primitive-core count is exponential in w, and
`w*(n)` grows — so the crossover cannot be pinned for `n >= 64`.**

## Honest verdict

- **INCONCLUSIVE on `extras <= n^3`.** Three tiny points at mixed `q` cannot be extrapolated to
  `n = 2^21`. The deployed regime (`w = 67471`, `w/n ~ 0.032`, `w >> w_0 ~ 21`, mean fiber
  ~2^35) is numerically unreachable. Reporting `w*` growth as "conjecture false" would repeat
  the E_3 over-extrapolation error (refused).
- **What is solid:** the engine and the object identification (extras == holmbuar's primitive
  core, exact-matched); the fact that the count is exp-in-w and `w*(n)` grows — an independent
  confirmation, from the counting side, that `conj:Q` is genuinely hard (matches holmbuar's
  three dead-margin routes in #366 and the `b2_literature_pioneer_verdict.md` pioneer verdict).
- **Numeric role:** a validated tool + supporting color for the community's `conj:Q` work, NOT
  a resolution. The box does not help: the wall is `q^w` (w), not `n`/RAM.

## Next (the real attack)

The proof route is the **positive** one nobody is running: adapt **Sawin's singular-locus
square-root-cancellation** (arXiv:1809.05137) to bound the primitive-core count of the fixed
polynomial `X^n-1` (a divisor-SET object, unlike Sawin's divisor-function short sums), and
confront small characteristic. Informed by holmbuar's exact dead-margin ledger (the bars to
beat) and this engine (for checking any sub-claim on toys). This is `pioneer` (open even over
Z), a long-horizon effort — coordinated on holmbuar's `conj:Q` ledger, complementary to the
negative/audit work he and DannyExperiments are doing.
