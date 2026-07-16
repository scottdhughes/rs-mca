# M1 A4 SPI atlas manifest v1 certificates

This directory contains two deterministic manifests checked by
`experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py`.

- `kb_mca_a1116048_base_generated_family.json` is a deployed-row **partial**
  manifest.  It imports the already-proved global-once paid baseline, records
  the `67,472`-index generated-collision capacity namespace, and leaves its
  chart adapter `UNPROVEN`.  It represents zero SPI charts and does not decide
  the target inequality.
- `gf19_442233_machinery_control.json` exhaustively lists the 48 support
  patterns in the frozen GF(19) control row.  All 48 are
  `UNPAID_PRIMITIVE`.  Its `17,328` charge is control-only and is not banked.

`eliminant_identity_control.json` is not a research manifest.  It is a pinned
synthetic equation source used only by the verifier's positive and adversarial
tests for ideal-combination identities, chart-key binding, small-field exact
roots, and large-field degree charging.

The shared schema is
`experimental/data/schemas/m1_a4_spi_atlas_manifest_v1.schema.json`.  All
object schemas are closed with `additionalProperties: false`; the verifier
also enforces cross-field semantics that JSON Schema alone cannot express.
Compressed families are capacity-only in v1.  Explicit eliminants require a
replayed source-bound polynomial ideal identity and use exhaustive small-field
root enumeration or a safe large-field degree charge, aggregated as a
disjoint chart sum.  Owner policies declare their final unpaid fallback; paid
terminals cannot use that fallback and must reference a registered charge for
the same owner.  The two imported KoalaBear charges are checked against an
exact row-specific registry so source-theorem aliases cannot be recharged.

Run:

```sh
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --check
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --tamper-selftest
```

Neither artifact proves the KoalaBear `A=1,116,048` safe row or changes a
leaderboard entry.
