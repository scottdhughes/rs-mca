# M1 KoalaBear adaptive pair-global source--rational owner splice v1

This packet widens the pair-global source--Möbius owner from #962 to every
qualifying full-outside rank-two record whose full-gcd-reduced projective
rational map has degree

```text
e <= E(s) = floor((s-1)/2),  where s = |Sigma|.
```

All such maps agree with the same fixed source labels at all `s` anchors.  The
cross polynomial of two maps has degree at most `2E(s) < s`, so the maps are
identical.  Every selected finite slope is therefore in one pair-global image
of `D \ Sigma`, with exact cap

```text
n - s <= n - 18,419 = 2,078,733.
```

The new owner replaces the source--Möbius owner at the same first-match index.
It does not add a second cap.  Consequently the joint C5/source/base cap,
`U_paid`, `B_remaining`, and the rank-nine gate are unchanged; incremental
ledger movement is exactly zero.

The adaptive residual is sharper than the uniform `e >= 9,210` statement.  A
surviving full-outside rank-two record satisfies

```text
e >= ceil(s/2)
e <= s + x - t - 1
x <= 49,055
```

and hence

```text
s >= 36,836
e >= 18,418
deg gcd(P,Q) <= 1,030,157.
```

Generate and replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --write
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --tamper-selftest
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.py \
  --sage-parity-check
```

Predecessor replays:

```bash
python3 -B experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_projective_source_load_v1.py --tamper-selftest
python3 -B experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py --check
python3 -B experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py --tamper-selftest
```

Expected main terminal:

```text
M1 adaptive source-rational owner splice: PASS
```

The Sage replay is an exact toy control, not a deployed selector census and
not the proof of rational-map rigidity.  The parity mode copies the source to
a temporary directory, runs both ordinary Sage and its optimized generated
Python form, and requires both transcripts to match the source-bound JSON.
The ignored `*.sage.py` file Sage may create during an ad hoc direct run is a
temporary build product and is not a packet artifact.  The control checks the
sharp `2e+1` threshold,
distinct full-gcd proxies with one common reduced map, moving roots outside the
source, collisions, a projective pole, exclusion of infinity from the finite
owner, incompatible source labels, and the sharp `2e` countercontrol.  It
constructs neither complete selector witness assignments nor rich-line
`beta/J` predicates.

The packet leaves the following route cut explicit:

```text
UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418
```

Non-full-outside source load, `U_Q`, residual `U_A`, rank-nine closure, and the
KoalaBear row remain open.
