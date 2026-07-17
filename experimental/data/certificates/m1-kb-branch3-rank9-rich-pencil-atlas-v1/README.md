# M1 KoalaBear rank-nine rich-pencil atlas v1

This packet replaces the false fixed-basis cap by an exact canonical
decomposition

\[
\mathcal E_{20}
=\sum_{L:J_L\ge21}\beta_L(J_L-20).
\]

It also certifies a sharp scalar route cut: at the deployed row, the local
constraints permit \(x=M-j=1\), \(J=109\), and enough ambient independent
bases for one component to exceed \(E_{\max}\).  This is a relaxation
witness, not a deployed Reed--Solomon selector.

The Sage control replays the identity on the exact
\(\mathbb F_{2^{37}}\), \(j=20\) five-pencil predecessor.  It finds five
rich lines with basis masses

~~~text
161, 165, 165, 161, 165
~~~

and verifies

~~~text
direct excess = atlas excess = 817
valid mask-basis incidences = 51765
distinct valid bases = 35238
maximum basis multiplicity = 21
~~~

Replay:

~~~bash
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py \
  --check
~~~

The Python verifier uses exact integers and rejects duplicate keys,
non-standard constants, floats, source drift, predecessor drift, semantic
owner mutations, hostile-profile mutations, and type confusion.

No ledger value moves.  The live terminal is
UNPAID_SOURCE_BOUND_RICH_PENCIL_AGGREGATE.
