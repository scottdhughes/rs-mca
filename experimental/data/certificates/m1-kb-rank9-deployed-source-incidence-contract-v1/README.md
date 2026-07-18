# M1 KoalaBear rank-nine deployed source-incidence contract v1

This packet freezes a deployed producer-field manifest, executes a fail-closed
readiness audit, and tests an exact toy incidence kernel for the rank-nine
rich-pencil aggregate.  It proves that the currently bound stack contains no
source-bound paying selector for every source family, row-uniform existence
theorem, or exhaustive source-family census with one paying selector each.

Replay:

~~~bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_deployed_source_incidence_contract_v1.py \
  --tamper-selftest

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_t2_core_source_coordinate_cover_v1.py \
  --check
~~~

The new checker uses exact integers and strict JSON.  Its two nonempty
small-prime declared-family fixtures, plus an empty-family edge control,
reconstruct words from raw source and graph-coordinate data, apply the declared
deficit cutoff, recompute supports, enumerate independent bases, derive graph
lines, check polynomial source lifts, and verify direct excess equals atlas
excess.  The high fixture has exact excess six; the low and empty controls have
excess zero.

The toy kernel does not validate the complete deployed producer manifest or
exhaust an eligible selector frontier.  In particular, it does not check the
deployed \(H_V\), exact-\(A\)/noncontainment, selector rank, regular locators,
complete-selector coverage, nonzero-pencil GCD/plant conditions, or global
owner deduplication.

Current terminal:

~~~text
UNBOUND_DEPLOYED_SOURCE_INCIDENCE
~~~

No ledger value moves.  The exact finite fixtures are atlas/source-equality
smoke controls, not a KoalaBear census or asymptotic argument.
