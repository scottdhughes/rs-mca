# Pull request title

[MCA] Audit rank-12 descent and add a Johnson degree-three core prefix

# Pull request body

## Summary

Direct successor to the rank-eleven global-core payment at exact parent `d01c546f4dca70e256c18c142873821b3bb48ab5`.

This PR first audits the unpublished exploratory rank-12/13 branch. Its live verifier references four undefined load-bearing variables, and its proof prices only the delayed endpoint rank-drop path, not proper drops occurring at larger ambient dimension. The packet therefore withdraws those payment claims rather than stacking on them.

It then proves an exact higher-incidence replacement. At the critical complete-pair-core cell

```text
n      = 1,052,933
h      =    67,701
lambda =     4,356
```

a degree-three Johnson/Delsarte dual bounds the number of canonical core sets by

```text
54,568,751.
```

The former ordinary affine pair-list prefix at the same cell was `25,551,333,830,332`. The exact dual is supported at intersection sizes `3104`, `3105`, and `4356`; all 4,357 allowed intersection constraints are checked over the rationals.

## Scope

- proved audit and correction of the rank-12/13 proof boundary;
- proved degree-three Johnson core-prefix theorem;
- active-v4 ledger movement: `0`;
- affine error rank 12 paid: no;
- affine error rank 13 paid: no;
- KoalaBear closure: no.

The remaining load is the high-margin tail and the global early-drop forest. The next theorem must supply an ambient-dimension barrier recurrence with a valid cap at every cell used.

## Verification

- exact rational primary verifier;
- independently written dual replay;
- all 4,357 intersection constraints checked;
- exact old-prefix and slope-cap arithmetic;
- Wolfram rational replay;
- literature scope review;
- exact result certificate.

## Review boundary

- parent: `d01c546f4dca70e256c18c142873821b3bb48ab5`
- head repository: `scottdhughes/rs-mca`
- head branch: `codex/kb-mca-rank12-johnson-prefix-audit-post-rank11`
