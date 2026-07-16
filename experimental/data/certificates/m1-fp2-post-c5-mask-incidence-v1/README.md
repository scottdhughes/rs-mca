# M1 F_(p^2) post-C5 mask/incidence certificate

This directory contains the machine-readable packet for
`experimental/notes/m1/m1_fp2_post_c5_mask_incidence_v1.md`.

It records:

- the missing literal adapter between KoalaBear branches 1--5 and the
  projective C1--C5 catalogue;
- the certified application of the canonical proper-projective-field C5
  refinement imported from integrated PR #660;
- the exact two-column quotient-incidence case split;
- the imported/applied rank-zero and rank-one closures from #660/#670;
- the basis-relative disjoint pivot atlas, with no deterministic
  support-to-basis adapter claimed;
- the unpaid field-full rank-two support-union route cut.

Replay:

```bash
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --check
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.sage
```

The packet has no ledger consequence.  `U_2`, `U_Q`, and `U_A` remain null.
