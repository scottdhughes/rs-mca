# The full-rank target |H_d(v)| ≤ p^{n/2+2} of PR #662 is false by exact computation at reachable rows

**One line.** PR #662 reduces the deployed max-fiber problem to its open full-rank estimate `|H_d(v)| ≤ p^{n/2+2}`
(its B53), and its toy census (`|signed| ≈ 31.3 < n^3 = 125` at `(11,5,1,2)`) supports it. By exact evaluation of the
same signed aggregate at larger reachable rows, B53 is **false** — `89×` over at `(97,32,2,3)`, `26.8×` at
`(97,48,1,2)`, `3.4×10^5×` at `(97,96,2,3)` (the last cross-validated against an independent subset-sum fiber count).
This is a diagnostic packet built entirely on #662's own transform, decomposition, and normalization; it refutes one
stated-open target at reachable rows and leaves the max-fiber core (`N(0) ≤ n^3`) and the deployed row open.

## 0. The target (all of this is PR #662's)
On `H = μ_n(F_p)`, `w` syndromes, `c = w+1`, `m = n/2-c`, `d = n-w-1`. PR #662 proves the exact centered rank
decomposition (its normalization-bridge note) and reduces the full-rank obstruction to a single signed aggregate:

```
  N(v) - μ  =  p^{-n} Σ_{r=r_*}^{d} T_r(v)                          [#662]
  T_d(v)    =  χ((-1)^d) g^d H_d(v),   T_d(v) = U(v) - mean_η U(η)   [#662, B52]
  OPEN target (B53):   |H_d(v)| ≤ p^{n/2+2}.                        [#662]
```

We write `A_d(v) := T_d(v)/p^d = χ((-1)^d) g^d p^{-d} H_d(v)`, so `|A_d(v)| = p^{-d/2} |H_d(v)|`; since `d = n-c`,
the two normalizations carry the **same** target: `|H_d(v)| ≤ p^{n/2+2} ⟺ |T_d(v)| ≤ p^{n-c/2+2} ⟺ |A_d(v)| ≤
p^{c/2+2}`. We evaluate `A_d(v)` exactly (the same object #662's transform produces) and read the violation of B53
directly off it. #662 itself already records that "replacing the sum by absolute values is not viable"; the present
packet shows the *signed* aggregate is over target too, so the difficulty is not merely termwise.

## 1. The refutation (exact)
Direct exact evaluation of `A_d(v)` (GPU via CRT; the evaluator is validated bit-exact against #662's own B9
full-rank oracle at `(7,6,1,2)` giving `A_d(0)=−1944/49`, and against a corrected rank-locus stratum evaluator at
`(13,12,2,3)`, `(17,16,2,3)` across all `q`; corrected `E_q` table matches #662/fixed_s3 at `p=7,13,17`):

- **`(97,32,2,3)`**: `A_d(0) = −731704492880832/912673`, so `|H_d(0)| / p^{n/2+2} = |A_d(0)| / p^{c/2+2} = 89.19`.
  **B53 fails by `89×`.**
- **`(97,48,1,2)`**: `26.82×`.
- **`(97,96,2,3)`** (confirming, `c=3`, larger `n`): `A_d(0) = −2804335939511319360/912673`, `ratio = 341833×`.
  This value was **predicted independently** from the plain subset-sum fiber count `N(v)` (`p^c·(N(0)−μ) =
  −3.104×10¹²`, ratio `3.45×10⁵`) and the GPU CRT evaluator confirmed it to `0.990 = 1+O(1/p)` — two orthogonal
  computations agree, so the `89×`-class violation is not an artifact.

These three are exact evaluations of the *full* signed aggregate `H_d` (all `(q,Z)` strata) and directly violate B53.

**A supporting finite trend (a single component, not the full aggregate).** The `q=1` stratum alone is a pure
Littlewood–Offord sign-count (no CHG machinery). On the deployed ray `(p−1)/n ≈ 1016`, `w=1`, its ratio to `p^3` at
the four primes `p = 65089, 130817, 260609, 520193` (`n = 64,128,256,512`) is:

```
 n:      64        128         256          512
q1/p^3: 2.16694   27096.7   1.00932e13   1.59065e27      (exact integer sign-counts)
```

We report this as **finite-row growth of the `q=1` component only** — it does **not** establish failure of the full
B53 aggregate along the ray, because inter-stratum cancellation is not evaluated at `n > 96` (the full aggregate is
GPU-measured only at the three rows above). Over the same finite rows the dimensionless prize-count anomaly
`z(0) = (N(0)−μ)/σ` stays modest: `+12.2, +16.4, +16.8, +17.9`. Because `T_d` is the leading (`r=d`) stratum of
#662's decomposition, `A_d(v) = p^c·(N(v)−μ)·(1+O(1/p))` (verified for all `v` at `(97,48,1,2)`,
`max_v|ratio−1| = 0.008 ≈ 1/p`), so on the measured rows B53's `p^{n/2+2}` would require `|N(0)−μ| ≤ p^{2−c/2}`, far
below the observed count deviation. We make no asymptotic or deployment-row claim: only that B53 is exact-false at the
three measured rows, and the `q=1` component grows over the four finite ray rows.

## 2. Relation to #677 (consistency, not a new route)
This corroborates #677's independent conclusion: `τ`-moments do not control the signed residual bulk, and #677
explicitly moves off the CHG normalization toward a positive band collision-energy. The present refutation is the
CHG-side exact witness of the same fact. (For completeness: the CHG aggregate does have a computable second moment,
`p^{-w} Σ_v (N(v)−μ)² = p^{-w-2c} Σ_v |A_d(v)|²·(1+O(1/p))`, verified ratio `0.990` at `(97,48,1,2)` — an alternative
to the profile-side order-two object, though #677's band route may be preferable.)

## Non-claims
- No claim about `N(0) ≤ n^3` (open) — B53 was a *sufficient* condition; its failure does not resolve the prize.
- The bound `Σ_{r<d} T_r / T_d = O(1/p)` (full-rank dominance) is verified across 13 rows and derived as the
  sub-full-rank remainder, not proved uniformly.
- All fiber data is `w ≤ 2`; deployment `w = 67471` is unmeasured. B53 is exact-false at the three GPU-measured full
  aggregate rows `(97,32,2,3)`, `(97,48,1,2)`, `(97,96,2,3)`. The deployed row `n = 2^21` is **not** evaluated (its
  `q=3` table is 34 GB) and **no deployment-row or asymptotic claim is made**. The `q=1`-component ray (`n ≤ 512`) is
  a finite trend for a single stratum, not a test of the full B53 aggregate.
- The `(97,96,2,3)` full-aggregate value rests on one GPU CRT run; it is corroborated (not exactly re-derived) by the
  independent subset-sum DP to `1+O(1/p)`. The `(97,32,2,3)` headline is corroborated the same way.

## Reproducibility
Stdlib-only, deterministic verifier (`--check` / `--tamper-selftest`): the `q=1` counterexample and the `q=1`-ray are
pure integer sign-counts (no CHG machinery); `T_d(0)=−95256` at `(7,6,1,2)` is re-derived from an independent
full-rank oracle; the **headline** `(97,32,2,3)` `|A_d(0)|/p^{c/2+2} = 89.19` is asserted and cross-checked against the
subset-sum DP prediction (`GPU/pred = 0.990`), and the tamper-selftest mutates that headline witness. The evaluator
that produced the `(97,32)`/`(97,96)` full-aggregate values reproduces `−1944/49` at `(7,6,1,2)` and all 49 exact
`T_d(v)` at `(7,6,2,3)` from an independent oracle.
