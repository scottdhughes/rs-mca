# Statement correspondence

Sources:

- `experimental/notes/thresholds/championship_census_b19_26.md`
- `experimental/notes/thresholds/corridor_interior_hunt.md`

Verifiers:

- `experimental/scripts/verify_championship_census_b19_26.py`
- `experimental/scripts/verify_corridor_interior_hunt.py`

`championshipRows` copies the eight exact `(b,fstar,L1)` rows from the
championship table. `championship_null_guard` proves by exact integer
cross-powers that none beats the `b=18` row; it does not encode the rounded
decimal `rho`.

`corridorRows` copies the four lacunary/dense rows, five grid rows, two F13
rows, three larger modular rows, and the direct anneal row used by the corridor
hunt's overall null summary. `corridor_hunt_null_guard` proves each stored row
lies strictly below both `2^(4/3)` and the known champion.

The falsifiers make strictness load-bearing. The search methodology,
finite subset-sum recomputation, witness construction, and claimed search
coverage remain the responsibility of the independent verifiers. In
particular, this package is not an exhaustive classification of integer blocks.
