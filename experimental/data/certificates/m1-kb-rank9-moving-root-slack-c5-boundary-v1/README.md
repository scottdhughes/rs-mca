# M1 KoalaBear moving-root cofactor/slack and C5 boundary v1

This packet is an explicitly stacked successor to PR #982.  It composes the
exact rich-pencil identity

```text
|F_eta| = x + delta_eta
```

with the full-outside reduced-degree bound.  Every selected finite slope
satisfies

```text
L_F_eta | Pbar + eta Qbar
x + delta_eta <= e.
```

For

```text
r   = s - t - 1
h   = deg(H) - c
u   = e - x
ell = k - 1 - deg(H) - e
```

the exact normal form is

```text
h + u + ell = r
delta_eta <= u.
```

The zero-slack boundary `s=t+1=67,473` has `H=L_C` and two fully
base-split moving members.  Two distinct selected slopes make the fixed
translated received pair projectively base-defined, so the earlier canonical
C5 owner already removes it.  The residual becomes

```text
s >= 67,474
e >= 33,737
deg(H) <= 1,014,838
```

and the new terminal is

```text
UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67474.
```

This closes 33,736 top gcd degrees in total, 15,319 more than #982, with
incremental ledger movement zero.

## Replay

From the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --write
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py \
  --sage-parity-check
```

Predecessor replays:

```bash
python3 -B experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py --tamper-selftest
```

Expected main terminal:

```text
M1 moving-root cofactor/slack and C5 boundary: PASS
```

The Sage control works over `GF(11) subset GF(11^2)`.  It verifies one exact
zero-slack base-descent interface and representatives of the two one-slack
nonbase linear shapes.  It is toy-scale: it does not construct a complete
selector, realize deployed determinant mass or `J>=21`, or prove the theorem.

## Remaining one-slack cells

At `s=67,474`, the exact slack triples are

```text
(h,u,ell) = (1,0,0), (0,1,0), (0,0,1).
```

The last cell is C5-owned.  The two fail-closed residuals are

```text
UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR.
```

Non-full-outside source load, the image-scale/Q input, balanced-core and
sparse residuals, the complete profile envelope, and the KoalaBear row remain
open.  No Lean or rank-at-least-ten work is authorized by this packet.
