# Proposed title

`[MCA] Force a rank-three common-factor direction subcode`

## Stack and review boundary

This is a parallel one-commit successor to #1172 at exact parent
`193b7bf99a5cc7ccea042f25677e698d9f988eee`.

Review the changes on branch
`scottdhughes:codex/kb-mca-rank11-factor-flag-post-fixed-endpoint`
after that exact parent. This is an alternative structural route from #1172
and does not depend on #1173.

## Exact result

Freeze one actual minimizing pair for every post-near record before choosing
any cutoff. The parent nonuniform-margin theorem at cutoff `1795` supplies an
actual dense center pair `e_*` owning at least `200,632` slopes with complete
pair-core deficiency at most four. Fix a `1,116,044`-coordinate subset `G_*`
of that core.

At cutoff `tau=1936`, every low-margin minimizing pair `e` has complete pair
core of size at least `1,114,112`. Therefore both endpoint differences from
`e_*` vanish simultaneously on at least `133,004` coordinates of `G_*`.
Their row space is a one- or two-dimensional subcode `U_e` of the fixed
explanation-direction code `C'`, with `dim C' <= 10`.

The packet proves a two-level support-flag theorem. Unless some actual `U_e`
is contained in a three-dimensional subcode of `C'` with at least `23,354`
common zeros in `G_*`, all low pair types admit a disjoint canonical assignment
to:

- at most `8,415,196,932` terminal one-dimensional direction containers, each
  containing at most `15` pair types; or
- at most `382,360,905` two-dimensional direction containers, each containing
  at most `255` pair types.

After the fixed-pair slope projection, high-margin tail, and disjoint
near-rational add-back, the exact total is

```text
low-margin family        219,935,524,214,538,240
high-margin tail          55,043,143,075,392,992
near-rational add-back                 134,944
-------------------------------------------------
total                     274,978,667,290,066,176
budget                    274,980,728,111,395,087
slack                           2,060,821,328,911
```

Thus every over-budget affine-error-rank-eleven line forces a source-bound
three-dimensional direction subcode containing an actual pair-difference row
space and sharing at least `23,354` deployed zeros inside the dense center
core.

The adjacent threshold `23,355` fails even after optimizing the intermediate
two-plane threshold: its best total is `274,995,846,032,030,976`, over budget
by `15,117,920,635,889`. Hence `23,354` is the exact adjacent wall for this
declared two-level profile.

## Scope and ownership

- proves a structural rank-three common-factor router;
- active-v4 ledger movement: `0`;
- error-rank-eleven payment: no;
- KoalaBear closure: no.

All quantities count distinct finite affine slopes. Pair types are assigned
canonically to one direction container before any per-container cap is summed.
Every fixed pair owns at most `983,040` slopes. No edgewise factor cancellation
or overlapping local charge is used.

## Verification

- canonical payload SHA-256:
  `4d2b1d85a7374f51dd8c66c053acc47616617c5f48cd34018c3a4fca53e13ee0`
- exact primary verifier: PASS
- independent arithmetic audit: PASS
- full dimension table `s=1,...,10`: PASS
- exhaustive adjacent-threshold optimization: PASS
- finite-field interleaving guards: PASS
- independent mathematics review: GREEN
- independent certificate review: GREEN
- targeted literature sweep and Wolfram replay: PASS

## Dependency and next theorem

This PR must integrate after #1172. It is parallel to #1173 rather than
stacked on it.

The next load-bearing theorem is a classification or payment of the forced
three-dimensional common-factor subcode while preserving the actual center
pair, the contained pair-difference row space, and first-match slope ownership.
Separate cancellation of many local factors is not chronology-safe.
