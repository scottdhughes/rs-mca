# M31 rank-six generalized-weight/codimension-one closure packet

This packet certifies a source-bound closure of the rank-six branch in the
Mersenne-31 LIST direct boundary route.

The parent packet supplies 15,775,933 distinct actual base-field shallow
codewords and, at affine codeword-span rank six, the exact numerator-union
window

```text
781,458 <= g <= 1,033,227.
```

The new generalized-weight marked-line inequality forces

```text
q_5 <= 32,004,
1,048,581 <= d_5(W_c) <= 1,080,585.
```

A `d_5`-minimizing five-dimensional hyperplane is support-saturated.  The
proved MDS-soft codimension-one compiler then counts the whole rank-six
affine chart, with the exact conservative bound

```text
whole rank-six chart <= 908,116.
```

The gap to the required shallow family is 14,867,817, so rank six is
impossible.  Together with the parent, ranks one through six are excluded.

This is a direct route cut, not a Grande Finale v4 payment.  The M31 LIST row
and every rank at least seven remain open, and ledger movement is zero.  The
live terminal is
`UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.

The Sage `GF(7)` census is an exact orientation/falsification control only;
it is not deployed evidence.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.py
python3 -O experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.py
python3 experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.sage
python3 experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_v1.py --check
python3 experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_packet_v1.py
python3 experimental/scripts/verify_m31_rank6_generalized_weight_codim1_closure_packet_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py
```

The primary verifier uses only exact standard-library arithmetic and explicit
exceptions, so normal and optimized Python have identical semantics.  The
packet verifier rejects duplicate JSON keys, floating-point values,
noncanonical bytes, source aliases and traversal, stale hashes, payload
substitution, theorem-note drift, predecessor drift, and proof-critical
semantic mutations.
