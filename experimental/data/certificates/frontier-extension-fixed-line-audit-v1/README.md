# Frontier extension fixed-line audit v1

Exact counterexample and contract-correction packet for the extension-valued
MCA lane.

The packet proves that a fixed arbitrary `F`-valued received line need not have
a Frobenius-stable bad-slope set, even at slack `t=2`.  It also distinguishes
the direct extension charge `Delta*p^e_Y` from the primitive Q-fin multiplier
`K_rem=4,807,520`.

It does not produce a deployed KoalaBear SPI chart, pay the proper-subfield
tower cells, complete the deployed first-match owner partition, or prove the
adjacent row safe.

Replay:

```bash
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --check
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.sage
```

The superseded `verify_frontier_extension_cell_targets.py` is a source-bound
historical control, not an acceptance gate for this correction.  It retains the
old ceiling semantics and currently has a pre-existing G8 reference-path
failure on the integrated tree.

Regenerate the committed JSON after an intentional source change:

```bash
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --write
```
