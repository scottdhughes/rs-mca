# KB-MCA Route-D v39: H_core ≤K_cap ledger + overflow enum

Status: `PARTIAL` — **H_core ≤2170** PROVED by ledger; overflow **μ_over
e·p under cardinality** PROVED; ambient **L≤70** still OPEN.

## Path A — Ledger thinning (PROVED structure)

```text
R_max = 70
H_core = highs with multi-tier FM tier < R_max
|H_core| ≤ R_max · ⌊n/e⌋ = 2170
```

- **Core pairs** (high ∈ H_core): pay with multi-tier κ + (ι,δ)
- **Overflow pairs** (high ∉ H_core): pay with μ_over enum

### Overflow enum (PROVED)

```text
order overflow pairs → rank i
μ_over = (i mod e, ⌊i/e⌋)
```

If `N_over ≤ e·p` (e.g. `|H_over|≤2170`), lands in `[e]×F_p`.

If multi-tier is allowed enough tiers to match all highs and `|H|≤K_cap`, then
`H_over=∅` and overflow is empty (v37).

## Path B — Ambient load gate (PROVED inequality, OPEN gate)

```text
|H| ≤ (n/e) · L
L ≤ 70  ⇒  |H| ≤ 2170
```

Toys: max L=51 (can exceed 70 on small fields; not a deployed refutation).

## Full A_SP sketch with ledger

```text
1. SR-cell (Type S) — μ_enum e·p if |H|≤K_cap (v38)
2. Type D residual — M_pad ≤ 2
3. Core sides — H_core tags (≤K_cap)
4. Overflow sides — μ_over e·p if N_over≤e·p
```

## Toys

| j | w | free_core | #H | L | #H_core | #H_over | #pairs core | #pairs over | over enum? | core≤cap? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 1 | 17 | 13 | 7 | 10 | 160 | 240 | True | True |
| 5 | 1 | 2 | 17 | 12 | 6 | 11 | 122 | 164 | True | True |
| 5 | 2 | 0 | 110 | 51 | 4 | 106 | 8 | 252 | True | True |
| 6 | 1 | 3 | 17 | 11 | 5 | 12 | 84 | 116 | True | True |
| 6 | 2 | 1 | 65 | 34 | 3 | 62 | 6 | 140 | True | True |
| 6 | 3 | -1 | 30 | 19 | 3 | 27 | 6 | 54 | True | True |
| 7 | 1 | 4 | 17 | 10 | 5 | 12 | 42 | 90 | True | True |
| 7 | 2 | 2 | 36 | 22 | 3 | 33 | 6 | 74 | True | True |
| 7 | 3 | 0 | 13 | 10 | 3 | 10 | 6 | 20 | True | True |
| 8 | 1 | 5 | 16 | 9 | 5 | 11 | 22 | 64 | True | True |
| 8 | 2 | 3 | 19 | 14 | 3 | 16 | 10 | 32 | True | True |
| 8 | 3 | 1 | 5 | 4 | 2 | 3 | 4 | 6 | True | True |
| 9 | 2 | 4 | 8 | 6 | 2 | 6 | 4 | 12 | True | True |
| 9 | 3 | 2 | 1 | 1 | 1 | 0 | 2 | 0 | None | True |

## OPEN

1. `L ≤ 70` at deployed A_SP
2. Show deployed A_SP highs fit in R_max tiers (H_over=∅), or bound N_over

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v39.py --check
```
