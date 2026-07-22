# M31 varying-G first-pivot basis route-cut packet

This packet certifies exact marked-basis consequences for the reconstructed
base-field boundary shallow family in the Mersenne-31 LIST row at target
`2^-100`, agreement `1,116,023`, and budget `B*=16,777,215` distinct
codewords per received word.

For shallow codeword-span rank `r`, union size `g`, common denominator-zero
count `e`, and individual excesses `s_i`, the primary theorem includes the
first-pivot inequality

```text
sum_i (g+s_i)*(w+s_i+r+e-1)_(r-1) <= (R+g-e)_r
```

together with its marked-`E`, marked-`S`, cross-block, affine-line, and
balanced pair-incidence refinements.  The affine-line multiplicity is exactly
`15`, the projective-ray multiplicity is exactly `14`, and a forbidden
shallow family would determine at least `1,126,853` projective directions.

At the inherited shallow cardinality `15,775,933`, these inequalities exclude
ranks one through five.  At rank six they force the exact surviving union
window

```text
781,458 <= g <= 1,033,227.
```

The optimized combined rank-six excess ceiling is `96,161,189,784`.  This is
an aggregate constraint, not a LIST payment.  In particular, the packet's
explicit scalar profile satisfies every aggregate inequality but is not
asserted to arise from a polynomial family.  It therefore cuts the enumerated
aggregate basis/second-incidence route; it is neither a row counterexample nor
deployed evidence.

The exact `GF(17)` family is a toy sharpness control only.  It does not prove a
deployed bound or justify extrapolation to the Mersenne-31 parameters.

This packet moves no Grande Finale v4 atom and does not close or pay rank six.
Its live terminal is
`UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.py
python3 -O experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.py
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.sage
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py
python3 experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py --tamper-selftest
```

The primary verifier uses explicit exceptions under normal and optimized
Python, checks the sealed predecessor payload and every bound source hash, and
detects proof-critical hostile mutations.  The Sage replay recomputes the
deployed arithmetic independently of the Python implementation.  The packet
verifier checks the closed schema, replays the predecessor packet, verifies
fresh source bindings, and repeats the zero-ledger and open-row scope guards.
