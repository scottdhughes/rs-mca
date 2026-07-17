# M1 rank-nine cyclic rich-pencil complete-selector control v1

This certificate packet binds two exact objects over the cyclic order-34
domain in \(\mathbb F_{67^2}\):

1. an incomplete 29-slope selector with affine rank nine, one 21-slope rich
   line, and direct/atlas excess 165;
2. a separate lexicographic selector exhausting all 66 noncontained slopes,
   with exact minimum affine rank two and exact minimum carrier excess one.

The second selector routes the complete toy family to
`CERTIFIED_LOW_EXCESS_COMMON_CARRIER`, with \(B_1=231\ge66\).  Its selected
supports have no Q0/periodic owner; separately, the complete witness inventory
contains 3,003 periodic \(c=2\) Q0 supports projecting onto all 66 slopes.
The carrier owner is earlier.  This is a toy closure, not a deployed KoalaBear
result, and it moves no ledger value.

Replay:

~~~bash
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --tamper-selftest
~~~

The Python checker is standard-library-only.  It rejects duplicate JSON keys,
floats, non-standard constants, source drift, predecessor drift, scope
promotion, incomplete/full-selector confusion, owner mutations, rank or
carrier drift, atlas/excess drift, and type confusion.
