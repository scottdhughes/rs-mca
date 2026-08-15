# Certificate review

Status: GREEN.

The result certificate is integer-only and binds to exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

The primary verifier:

- recomputes all affine/interleaved list caps from binomial coefficients;
- checks the exact residual, parent capacities, abundance floors, balanced
  intersection moments, and weighted pin table;
- exhausts small set-system controls for the convexity inequality;
- rejects seven hostile mutations.

The independent audit uses separate product formulas and `Fraction` arithmetic.
It does not import the primary verifier.

Claims are explicitly limited to parent abundance, factor synchronization, and
weighted pinning. The certificate fields for rank-eleven payment, KoalaBear
closure, and active-v4 ledger movement remain `false`, `false`, and `0`.