# M1 rank-nine regular locator-span shortcut refuted v1

This directory freezes the exact certificate for the generic local route cut
proved in
`experimental/notes/m1/m1_rank9_regular_locator_span_shortcut_refuted_v1.md`.

The base control is a deterministic `RS[24,13,12]` construction over
`GF(2^23)` with an explicitly declared retained 55-slope family `Gamma`.  On
that declared family it has a unique complete noncontained selector with

```text
affine rank s_* = 9
raw witness rank t = 10
carrier excess nu = kappa_* = 11
locator-vector rank = 11
```

The symbolic five-pencil construction extends to every `j >= 10` with the
first three values fixed and locator rank `j+1`.  Therefore generic local
rank, carrier, transversality, and regular Padé--Hankel hypotheses do not imply
a constant locator span or a fixed bounded cover.

The packet does not instantiate the KoalaBear domain, execute the deployed
periodic/quotient/Johnson/B11 first-match masks, move the ledger, or close
branch 3.  It does not assert that the declared `Gamma` exhausts the full
bad-slope set, and it does not refute a bridge that adds full-bad-family or
deployed first-match exhaustion as a load-bearing hypothesis.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py --check
python3 experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py --check
python3 -O experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py --tamper-selftest
HOME=/tmp /usr/local/bin/sage experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.sage
```

To regenerate the canonical JSON after an intentional packet edit:

```bash
python3 experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py --write
```

Expected terminal:

```text
GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_REFUTED
```

The KoalaBear owner-strengthened terminal remains `YELLOW_OPEN`, and the
certificate records zero ledger movement.
