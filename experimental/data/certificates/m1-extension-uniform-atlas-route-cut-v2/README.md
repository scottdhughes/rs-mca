# M1 extension uniform-atlas route cut v2

This packet certifies one new route cut and replays one inherited budget wall
for the KoalaBear MCA row at
`A=1,116,048`:

- a fixed or finitely sampled received-pair atlas is not a certificate for the
  row-uniform `U_A` supremum; and
- the unrefined all-line fixed-deficiency charge `binom(n,d+1)` cannot fit the
  deployed budget at `d=913,632`, as already proved at the same binomial index
  by Holm Buar's manually integrated saturated-BC budget audit, PR #383.

The new arithmetic corollary is that, in the declared compiler range
`1 <= d_eff < 981104 < n/2`, a bare complete-absorption binomial can fit the
current remaining budget only for `d_eff <= 1`.  The packet binds the current
paid baseline `U_paid=2602153473` and remaining budget
`274980725509241614`; it does not reuse the superseded v1 ledger.

Stack dependency: the current-ledger bindings come from open PR #812.  Keep
this packet stacked on #812, or restack it only after #812 is integrated.

It leaves `U_A=null`, changes no ledger, and does not claim that the actual
residual numerator exceeds the budget.

Replay:

```bash
python3 experimental/scripts/verify_m1_extension_uniform_atlas_route_cut_v2.py --check
python3 experimental/scripts/verify_m1_extension_uniform_atlas_route_cut_v2.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --tamper-selftest
python3 experimental/scripts/verify_saturated_bc_budget_fit.py
python3 experimental/scripts/verify_saturated_bc_budget_fit.py --tamper-selftest
```

The verifier is standard-library-only.  It rejects duplicate keys,
nonstandard JSON constants, source/hash drift, quantifier promotion, theorem-
shape overclaims, incorrect budget arithmetic, and any attempt to replace the
open `U_A` by zero.
