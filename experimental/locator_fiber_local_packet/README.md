# Locator-Fiber Local Packet

Status: EXPERIMENTAL

This directory contains a small local packet runner that wires together the
experimental locator-fiber sweep, optional Sage cross-checks, and the
cross-check comparison report. It is evidence plumbing only. It does not assert
Reed-Solomon, list-decoding, MCA, or protocol safety, and it does not upgrade
any theorem status.

The packet runner writes:

- Python sweep JSON/CSV/Markdown output
- Sage cross-check JSON output
- Python/Sage comparison JSON/Markdown output
- a packet manifest and index Markdown

Example:

```bash
PACKET=experimental/locator_fiber_local_packet/run_locator_fiber_local_packet.py
.venv/bin/python "$PACKET" \
  --out-dir /tmp/rs-mca-locator-fiber-packet \
  --case-set tiny \
  --max-witnesses 0
```

Use `--case-set selected` for the current selected local cross-check set. Sage
must be available on `PATH` unless `--sage-command` points to another Sage
executable.
