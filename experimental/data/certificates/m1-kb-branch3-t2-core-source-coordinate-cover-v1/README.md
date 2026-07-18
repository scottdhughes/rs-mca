# M1 branch-3 t=2 core-source coordinate-cover census v1

This packet exhausts every 12-root core product state and every 13-root
nonzero-locator product state in the cyclic

```text
(n,k,R,j,A,t) = (36,14,22,20,16,2)
F = GF(17^2)
```

toy row.

Exact outcome:

- all `82,944 = (289-1)^2` nonzero core-derived source lines occur;
- every line has all 287 post-deep slopes;
- every one of the 33 nonsource coordinates is available in a compatible
  locator at every post-deep slope;
- all 82,944 lines therefore exit at or before the existing low-carrier owner;
- no empty-cover line survives inside this toy ansatz.

The LOW implication is safe under any earlier first-match deletion.  This is
not a deployed or KoalaBear claim, and the ledger remains unchanged.

Replay:

```bash
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py \
  --tamper-selftest
```

The Sage replay independently checks field arithmetic, a brute-force reduced
fixture, coordinate-order invariance, frozen census hashes, and the canonical
fixed-root constants from the predecessor packet.  The Python checker binds
the sources and predecessor payload, rechecks all integer implications, and
rejects semantic and parser mutations.
