# Experimental Workspace

Status: EXPERIMENTAL / AUDIT.

This directory is the staging area for material that is not yet promoted into
the main papers. Keep new work here first, and keep Papers A-D unchanged unless
a task explicitly asks for a main-paper patch.

## Current Layout

- `SUMMARY.md` gives the high-level research picture.
- `agents-log.md` records agent additions and cleanup decisions.
- `experiments.tex` and `experiments.pdf` are the compiled experimental note.
- `notes/` contains human-readable notes, audits, PR triage, and proof sketches
  grouped by target: `f1`, `l1`, `l2`, `m1`, `m2`, `x1`, `domain`,
  `certificates`, `audits`, and `protocol`.
- `scripts/` contains runnable Python/Sage/Lean-adjacent experimental scripts.
  Top-level Python scripts were intentionally kept together so local imports
  like `from mca_slope_scan import ...` still work when run by path.
- `scripts/locator/` contains the locator-fiber sweep, cross-check, local
  packet, and Sage cross-check tools.
- `data/` contains JSON/CSV certificates, witness fixtures, and schemas.
- `lean/` contains the current Lean formalization stub.

## What Was Removed

During the 2026-06-19 cleanup, generated `__pycache__` files and raw/prompt
transcript dumps from dated AI-loop folders were removed. The audited summaries,
compact review indexes, local checks, and verifier scripts were kept.

## Adding New Material

Put new material in the narrowest existing bucket:

- proof sketches and audit notes: `notes/<target>/`;
- scripts and verifiers: `scripts/`;
- certificate data and fixtures: `data/`;
- Lean experiments: `lean/`;
- coordination notes: append to `agents-log.md`.

Do not add raw model transcripts, generated caches, or bulky run archives unless
they are the only reproducibility artifact for a result. Prefer a compact audit
note plus a deterministic script or JSON certificate.

For PRs that add GitHub Actions workflows or executable artifact bundles, first
bank an inert audit note under `notes/` and record the security/relevance
decision in `notes/triage/`. Do not merge live workflows from experimental PRs
unless a human explicitly asks for repository-side replay infrastructure.
