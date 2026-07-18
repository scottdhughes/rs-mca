# M1 KoalaBear rank-nine active-source matroid reindex v1

This packet verifies the exact split

```text
S_L = (Sigma \ V) disjoint_union (Sigma intersect Z_L)
```

and the sharp rank-eight matroid exchange inequality

```text
r_L * beta_0 <= (z_L - r_L - 7)_+ * beta_1.
```

It also binds the exact `GF(67^2)` cyclic rank-nine control in which all
source points lie outside the selected carrier and the universal-cell excess
is positive.  That selector is incomplete for the full toy received pair, so
the result is a local implication route cut, not a deployed KoalaBear
counterexample.

Replay from the repository root:

```bash
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_rank9_active_source_matroid_reindex_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --check

python3 -B \
  experimental/scripts/verify_m1_rank9_rank1_regular_source_load_control_v1.py \
  --check
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_rank9_rank1_regular_source_load_control_v1.sage
```

Expected Python terminal:

```text
M1 KoalaBear active-source matroid reindex: PASS
```

The certificate is strict JSON with exact integers, source hashes,
predecessor payload bindings, and rehash-aware mutation tests.  It records
zero ledger movement.  The live proof terminals are

```text
UNPAID_UNIVERSAL_SOURCE_CELL
UNBOUND_ACTIVE_SOURCE_HIT_BASIS_TAIL
UNPAID_ACTIVE_RANK1_SELECTOR_COMPLETENESS
UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR
```
