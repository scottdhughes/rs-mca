# M1 rank-nine t=2 source-compatible cyclic control v1

This exact toy packet binds two three-coordinate source controls.  In each
row the full finite frontier is all field slopes and splits exactly into two
weight-two zero-polynomial slopes paid by the extended deep owner and a
post-deep nonzero-locator inventory:

1. `n=35, k=13` over `GF(29^2)`: a 21-plus-8 affine-rank-nine local
   family, two deep slopes plus an exhaustive 839-slope post-deep inventory,
   a structural carrier-excess bound of ten for every nonzero-locator
   selector, and a lexicographic post-deep selector of excess seven;
2. `n=36, k=14` over `GF(17^2)`: the smallest row in the ansatz capable of
   selected carrier excess eleven, together with two deep slopes plus an
   exhaustive 287-slope fixed-root post-deep selector of excess five.

The Sage verifier derives the three-coordinate compatibility equation and
classifies nonzero witnesses.  It proves uniform support-wise noncontainment,
checks the exact RS words, affine/raw ranks, rich GCDs, actual supports,
rank-two Hankel matrices, MDS transversality, and Frobenius rank.  For each
special zero-polynomial slope it also checks the exact-A support, full
agreement set, restricted-generator noncontainment rank, actual weight-two
support, Hankel rank two, and deep threshold seven.  Its compact post-deep
inventories store only two `2^16` half tables; they do not materialize
`C(32,12)` root sets.

The strict standard-library Python checker binds the Sage payload, the
extended-deep-owner note and certificate, exact fixtures, predecessor packets,
source hashes, full/deep/post-deep partition, selected-versus-complete
quantifiers, low-carrier arithmetic, first-match wording, and nonclaims.  Its
mutation suite rejects parser, type, rank, field, exceptional-slope,
inventory, selector, first-match, scope, source, and ledger drift.

Replay:

~~~bash
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --tamper-selftest
~~~

The exact conclusion is `DEEP_OR_AT_OR_BEFORE_LOW_CARRIER` for both toy
received pairs.  The packet does not instantiate or move any deployed
KoalaBear ledger, and neither 29-slope local family is a complete selector.
