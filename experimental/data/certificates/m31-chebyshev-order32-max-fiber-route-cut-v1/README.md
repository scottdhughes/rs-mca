# M31 order-32 Chebyshev maximum-fiber route-cut certificate

This packet certifies an exact finite result on the deployed Mersenne-31
Chebyshev quotient.  After puncturing any one of the 32 quotient labels, the
largest fiber of the 17-subset sum map has size exactly 6435.  The packet
also certifies that both the literal multiplicative-style quotient rotation
and the intrinsic (T_{31}) Chebyshev rotation are injective on these
punctured 17-subsets.

The result eliminates this complete counterexample template.  It does not
prove the M31 LIST row, a global `U_Q`, the arbitrary-unit boundary census,
or the uniform deterministic punctured-RS cap.  Ledger movement is zero.

## Lightweight replay

```bash
python3 experimental/scripts/verify_m31_chebyshev_order32_max_fiber_route_cut_v1.py --check --tamper-selftest
sage experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage --check
sage experimental/scripts/verify_m31_chebyshev_order32_rotation_injectivity_v1.sage --tamper-selftest
python3 experimental/scripts/verify_m31_chebyshev_order32_max_fiber_packet_v1.py --check --tamper-selftest
```

## Exhaustive census replay

The full replay materializes and sorts
`C(31,17)=265182525` residues for each of 16 representative punctures.  The
other punctures follow by the exact negation involution.  Four workers use
roughly 4.5 GiB at peak on the reference machine; lower `--workers` if
needed.

```bash
python3 experimental/scripts/verify_m31_chebyshev_order32_max_fiber_route_cut_v1.py \
  --full-census --workers 4
```

To replay all 32 punctures directly and sequentially:

```bash
clang++ -std=c++20 -O3 -DNDEBUG \
  experimental/scripts/verify_m31_chebyshev_order32_sum_fiber_census_v1.cpp \
  -o /tmp/m31-cheb32-census
/tmp/m31-cheb32-census --all
```

Every C++ run is exact and deterministic.  There is no sampling,
floating-point arithmetic, probabilistic hashing, or unchecked collision
compression.

## Regenerate the canonical manifest

The verifier never writes the manifest.  After an intentional source
change, inspect and regenerate it explicitly:

```bash
python3 experimental/scripts/verify_m31_chebyshev_order32_max_fiber_route_cut_v1.py \
  --print-template > /tmp/m31-cheb32-manifest.json
cmp /tmp/m31-cheb32-manifest.json \
  experimental/data/certificates/m31-chebyshev-order32-max-fiber-route-cut-v1/manifest.json
```

The manifest binds every packet source by SHA-256 and is canonical
single-line ASCII JSON.  The packet verifier checks the closed schema,
source bindings, exact subprocess reports, and hostile mutations under both
ordinary Python and `python -O`.
