# M1 KoalaBear pair-global source--Möbius owner splice v1

This packet upgrades the full-outside maximal-gcd synchronization theorem to
an intrinsic, selector-free first-match owner for one received pair and one
fixed SP3 translation.

Every qualifying maximal-gcd line from every selector agrees with the same
source labels on at least 18,419 base inputs.  Three-point rigidity gives one
common Möbius map, and the moving-root bridge places every selected finite
slope in the finite image of `D \ Sigma`.  Thus the global-once owner has cap

```text
n - 18,419 = 2,078,733.
```

The owner is inserted after canonical projective-base C5 and before the
residual extension/base cells.  The base-projective C5 case and the nonbase
source-Möbius-plus-base case are alternatives, so the joint block is

```text
max(p+1, p+n-18,419) = p+n-18,419 = 2,132,785,166.
```

It replaces the old `p+1` block.  Exact ledger movement is `2,078,732`, not
the full owner cap and not a sum over selectors or cases.

Generate and replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py \
  --write
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.sage
```

Predecessor replays:

```bash
python3 -B experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py --tamper-selftest
```

Expected main terminal:

```text
M1 pair-global source-Mobius owner splice: PASS
```

The Sage replay is an exact toy control over `GF(5^6)/GF(5)`.  It checks two
selector-carrier proxies with distinct carriers and polynomial pairs, a
different-source-map proxy for the forbidden cross-translation union, a
two-affine-anchor countercontrol, incompatible source labels, a forbidden
source root, and a projective pole.  It constructs neither complete selector
witness assignments nor rich-line `beta/J` predicates.  It is not a deployed
selector census and is not used as the proof of the symbolic theorem.

The packet closes only the full-outside, coefficient-rank-two,
full-gcd-degree-`k-2` cell.  Lower-gcd maps, non-full-outside source load,
`U_Q`, residual `U_A`, and the KoalaBear row remain open.
