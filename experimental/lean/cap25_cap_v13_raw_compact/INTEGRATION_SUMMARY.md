# Integration summary

This folder contributes a compact Lean workbench for the CAP25 v13 raw/compact
frontier.  The useful content is:

- arithmetic certificates for the deployed identity-scale unsafe edges;
- a structural identity-prefix floor for Reed-Solomon decoding lists;
- a simple-pole conversion from floor-generated lists to support-wise MCA
  lower bounds;
- deployed list and MCA unsafe rows derived from those structural lemmas;
- BC-side base-field census floor lemmas;
- SP-side reductions from shift-pair collisions to locator-prefix collisions.

The files are organized under the module root `cap25_cap_v13_raw_compact`.

The package does not settle the final safe side.  The residual inputs `Q`, `BC`,
and `SP` remain the relevant open upper-bound targets for adjacent threshold
certificates.

This repository integration pass did not run Lake.  It checked the sources for
obvious placeholder imports/status text and leaves any TeX/Lean correspondence
updates to explicit manual audit.
