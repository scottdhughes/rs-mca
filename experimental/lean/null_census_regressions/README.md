# Null-census regressions

This stdlib-only package locks denominator-cleared comparisons for two computed
search packets:

- the eight `b=19..26` championship rows;
- the fifteen explicit rows in the corridor-interior hunt.

The comparison `belowChampion` avoids floating point by cross-powering
`(fL)^(1/b)` against the `b=18` record. `belowCorridor` similarly clears
the threshold `2^(4/3)`.

Build and replay with:

```sh
lake build
python3 ../../scripts/verify_championship_census_b19_26.py
python3 ../../scripts/verify_corridor_interior_hunt.py
```

These are guards for stored computed rows. They do not claim that either search
was exhaustive outside the exact subclasses stated in the source notes, and
they do not prove global nonexistence of a better or corridor-interior block.
