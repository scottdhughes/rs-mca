# M31 common-V split-flat pairwise CRT equivalence packet

This packet certifies two exact structural results for the base-field boundary
census isolated by the parent `M31_BOUNDARY_COMMON_V_CROSS_G_ROUTE_CUT_V1`
packet.

It proves:

- every fixed-full-gcd-locator chart is an explicit affine split flat;
- a boundary chart has codimension exactly `w` and no rank-drop stratum;
- every nonempty interior chart has codimension at least `w+1`;
- the displayed boundary and interior full-gcd gates have the correct,
  different quotient orientations;
- for fewer than `p-1` pairwise-distinct reduced pairs `(G_i,b_i)` decorated
  with split locators `H_i`, one common unit `V` realizes all declared full
  gcds if and only if every individual gate `gcd(b_i,H_i)=1` holds and every
  pairwise Wronskian vanishes on the intersection locator and is nonzero on
  the symmetric-difference locator;
- at the deployed family size `B_star=16,777,215`, the uncovered-point unit
  table has exact margin `p-1-B_star=2,130,706,431`;
- the strict field-size hypothesis is sharp at family size `p-1`; and
- the fixed-`G` slice is an arbitrary-nonzero-word Reed--Solomon list census,
  whose ordinary Johnson denominator is nonpositive for
  `72,859 <= m <= 908,270`.

The individual denominator-unit gates together with the pairwise conditions
are sufficient: there is no hidden triple-or-higher common-`V` compatibility
obstruction at the deployed list size.  The abstract CRT theorem does not
assume `deg(H)>=deg(G)`; the canonical M31 degree gates enter only in the
boundary-list reconstruction corollary.  This is a route cut, not a count.
The remaining theorem is the global incidence bound for split rational
functions satisfying every individual denominator-unit gate and every
pairwise compatibility gate.  Ledger movement is zero; the M31 LIST row and
all four null v4 atoms remain open.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.py
python3 -O experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.py
python3 experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_common_v_pairwise_crt_equivalence_v1.sage
python3 experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py
python3 -O experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py
python3 experimental/scripts/verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py --tamper-selftest
```

The packet verifier independently replays the primary verifier in normal and
optimized modes, runs its hostile mutations, runs the Sage finite-field
control, checks the closed schema and canonical manifest, refreshes every
source hash, checks the internal payload and predecessor pin, and tests its
own proof-critical mutations.
