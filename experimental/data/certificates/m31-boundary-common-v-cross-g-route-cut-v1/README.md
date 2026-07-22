# M31 boundary common-V cross-G route-cut packet

This packet certifies exact route cuts for the boundary-anchor divisor/gcd
census left by `M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1`.

It proves:

- the exact fixed-locator Johnson formula and all deployed endpoint gates;
- the nonzero pairwise Wronskian and its insufficient root threshold;
- the split-support global moment and its exact (366886/366887) gate;
- the direct whole-list cap of `1,001,282` on excess at least `366,887`;
- the resulting residual of at least `15,775,933` shallow nonanchor pairs in
  any forbidden boundary list;
- the composition of scalar descent with prime-field fresh-symbol boundary
  forcing, which reduces every live violation to a boundary census with all
  polynomial data in `F_p` and one arbitrary base-field unit `V`;
- the exact `17,511,197` rank-46 substituted baseline, proving that this
  direct tail cap is not a bankable replacement for the parent cutoff;
- the sharp (m-w) base-field scalarization limit;
- the exact `V=1` locator-prefix identity, deployed source floor, and an
  exhaustive `F_7` counterexample to arbitrary-`V` -> `V=1` extremality;
- a literal Chebyshev-fibre abstract support family showing that the listed
  pairwise/support/occupancy data cannot close the row; and
- the irrelevance of elementary Singleton packing at the live radius.

The support family is deliberately not a received-word or common-(V)
construction.  The packet therefore localizes, but does not solve, the
remaining theorem: a base-field common-(V), cross-(G) coefficient-incidence
bound.  The reduction does not authorize the specialization `V=1`.

Ledger movement is zero.  The M31 LIST row remains open, and `U_Q`,
`U_list-int`, `U_ext`, and `U_new` remain null.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py
python3 -O experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py
python3 experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1_independent.py
python3 -O experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1_independent.py
python3 experimental/scripts/verify_m31_boundary_cross_g_route_cut_v1_independent.py --self-test
python3 experimental/scripts/verify_prefix_staircase_extremality_counterexamples.py
python3 experimental/scripts/verify_m31_chebyshev_fixed_remainder_c1_boundary_source_route_cut_v1.py
python3 experimental/scripts/verify_m31_boundary_common_v_cross_g_route_cut_packet_v1.py
python3 -O experimental/scripts/verify_m31_boundary_common_v_cross_g_route_cut_packet_v1.py
```

The primary and independent arithmetic replays share no implementation code.
The packet verifier checks the closed schema, source hashes, internal payload
hash, predecessor payload pins, theorem-contract anchors, exact result
objects, and proof-critical mutations.
