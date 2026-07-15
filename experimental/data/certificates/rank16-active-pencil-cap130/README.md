# Rank-16 active-pencil cap-130 certificate

This packet proves the local theorem recorded in
`experimental/notes/l2/rank16_active_pencil_cap130.md`.

## Source objects

- `RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md`
- `RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md`
- three hostile audits of the DPW/extactic input

The earlier cap-139 packet and its downstream projective-mass arithmetic are
not dependencies of this source-normalized theorem.

## Replays

```bash
DIR=experimental/data/certificates/rank16-active-pencil-cap130
PY=/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3

diff -u "$DIR/verify_rank16_weighted_grid_extactic_dpw_cap130.expected.txt" \
  <($PY -B "$DIR/verify_rank16_weighted_grid_extactic_dpw_cap130.py")
diff -u "$DIR/verify_rank16_weighted_grid_extactic_dpw_cap130.expected.txt" \
  <($PY -O -B "$DIR/verify_rank16_weighted_grid_extactic_dpw_cap130.py")
diff -u "$DIR/audit4_dch_rank16_weighted_grid_extactic_dpw_cap130.expected.txt" \
  <(/usr/bin/ruby --disable-gems -w \
    "$DIR/audit4_dch_rank16_weighted_grid_extactic_dpw_cap130.rb")
```

All files are covered by `SHA256SUMS.txt`.
