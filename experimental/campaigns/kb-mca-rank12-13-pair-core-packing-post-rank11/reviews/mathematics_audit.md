# Adversarial mathematics audit

The proof was checked against the following failure modes.

1. The complete-core lower bound has the correct sign and uses the frozen
   minimizing direction.
2. Fixed-pair exception sets are disjoint only outside the complete core; the
   proof uses exactly that statement.
3. Distinct pair types have core intersection at most `k-1`, even when one
   endpoint difference vanishes.
4. The Cauchy denominator is required positive before division.
5. Pair types, not slopes, are bounded by the Fisher inequality; the sharp
   fixed-pair multiplier is applied afterward.
6. High slopes use their own pair deficiencies and the pointwise resource.
7. Slope ownership is frozen once, preventing duplicate charges.
8. Delayed descent uses exact global minima.  Rank 13 has local decreases, so
   no pointwise monotonicity is claimed.
9. Capped descent is a weakening and is used only for the rank-14 route cut.
10. The cumulative deficiency compiler uses nested prefix constraints and an
    integral cheapest-first fill.

Verdict: GREEN for the rank-12 and rank-13 payments; OPEN for rank 14.
