# Pull request title

[MCA] Force rank-eleven factor synchronization from rich flats

# Pull request body

## Summary

Stacked successor to the anchored rich-flat router at exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

The predecessor pays the complete `h=42447` transverse row-space envelope at
cutoff `tau=1549` by `274,871,033,266,908,609`.  Hence an over-budget line
must carry at least `109,694,844,486,479` distinct slopes in nontransverse
row-space packets.

This PR routes each packet canonically to an immediate dimension-two or
dimension-three parent direction space.  Every parent vanishes on at least
`42,448` common actual anchor coordinates, while the exact dimension-three
pair-list cap permits at most `3,953,213,019` assigned slopes per parent.
Therefore every unsafe line has at least `27,749` distinct parents.

Exact incidence moments then force:

```text
two parents     >= 1,614 common coordinates   sum dimension <= 6
three parents   >=    62 common coordinates   sum dimension <= 9
four parents    >=     3 common coordinates   sum dimension <= 10
five parents    >=     1 common coordinate
```

The weighted theorem is stronger: a fixed `k`-coordinate set is contained in
parents carrying at least

```text
k=1    4,172,156,357,758
k=2      158,681,059,954
k=3        6,035,034,641
k=4          229,522,148
k=5            8,728,902
k=6              331,960
k=7               12,625
k=8                  481
k=9                   19
k=10                   1
```

assigned slopes.

## Scope

- result: proved structural mass and factor-synchronization router;
- active-v4 ledger movement: 0;
- rank-eleven payment: no;
- KoalaBear closure: no;
- synchronized sum-spaces are not claimed represented or independently paid.

All loads count distinct finite affine slopes.  The initial row-space packets
are disjoint, the immediate-parent rule is deterministic, and coincident
parents are merged before the pair-list cap is applied.

## Verification

- primary exact verifier: PASS
- optimized/canonical JSON mode: PASS
- hostile mutations: 8/8 PASS
- independent exact implementation: PASS
- exhaustive small unweighted set-system controls: PASS
- exhaustive small weighted set-system controls: PASS
- manifest and file hashes: PASS
- Wolfram exact replay: PASS
- independent mathematics review: GREEN
- certificate/custody review: GREEN
- literature sweep: no external theorem is load-bearing

Canonical payload is recorded in
`experimental/data/certificates/kb-mca-rank11-factor-synchronization-v1/manifest.json`.

## Dependency and next theorem

This PR must integrate after the anchored rich-flat router at
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

The strongest successor is now precise: cancel one synchronized locator into
a named chronology owner, or prove a structured Sylvester/subresultant rank
bound below the corresponding weighted assigned-slope threshold.  Independent
per-parent cancellation remains prohibited.

## Review boundary

- head repository: `scottdhughes/rs-mca`
- head branch: `codex/kb-mca-rank11-factor-synchronization-post-rich-flat`
- exact parent: `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`
