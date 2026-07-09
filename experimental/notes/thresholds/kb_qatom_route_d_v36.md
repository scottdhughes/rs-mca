# KB-MCA Route-D v36: SR-cell e·p cardinality + M/R side split

Status: `PARTIAL` — SR-cell has **e·p room under |H|≤K_cap** PROVED; M/R side
split PROVED; constructive SR/R marks and |H|≤K_cap still **OPEN**.

## SR-cell cardinality (PROVED)

```text
N_S ≤ N_side ≤ |H| · ⌊n/e⌋ · (⌊n/e⌋ − 1)
```

If `|H| ≤ K_cap = 2170`:

```text
N_S ≤ 2018100  ≪  e·p = 143763024447376
```

⇒ abstract injection of SR-events into e·p exists.

Type-D residual after SR: `M_pad ≤ 2` deployed.

### Constructive mark (OPEN / toy)

Toys: `(r_*, c0U, c0V)` injects Type S side keys (size `n·p²`, not `e·p`).

## M-cell / R-cell side split (PROVED)

```text
M = matching of active free-1 e-sets
M-cell: both sides in M, |H_M| ≤ ⌊n/e⌋ ≤ K_cap
R-cell: remaining pairs
```

Toys: R-cell is ~98–100% of pairs; natural R-cell e·p marks collide.

## Combined path

```text
1. SR-cell: Type S multipads     (e·p room if |H|≤K_cap; constructive OPEN)
2. Type D residual multipads     (M_pad ≤ 2)
3. M-cell sides                  (high tags free)
4. R-cell sides                  (e·p mark OPEN)
```

Closes full A_SP at e·p if |H|≤K_cap and R-cell injects.

## Toys

| j | w | free_core | #S | #D | #H | #pairs | #M-pairs | #R-pairs | frac R | (r*,c0) inj? | R minU mod e? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 1 | 0 | 540 | 17 | 3170 | 0 | 3170 | 1.00 | True | False |
| 5 | 1 | 2 | 86 | 64 | 17 | 4386 | 0 | 4386 | 1.00 | True | False |
| 5 | 2 | 0 | 0 | 0 | 110 | 1090 | 0 | 1090 | 1.00 | True | False |
| 6 | 1 | 3 | 86 | 0 | 17 | 4616 | 0 | 4616 | 1.00 | True | False |
| 6 | 2 | 1 | 0 | 2 | 65 | 930 | 2 | 928 | 1.00 | True | False |
| 6 | 3 | -1 | 0 | 0 | 30 | 150 | 0 | 150 | 1.00 | True | False |
| 7 | 1 | 4 | 52 | 0 | 17 | 3666 | 0 | 3666 | 1.00 | True | False |
| 7 | 2 | 2 | 2 | 0 | 36 | 598 | 2 | 596 | 1.00 | True | False |
| 7 | 3 | 0 | 0 | 0 | 13 | 68 | 0 | 68 | 1.00 | True | False |
| 8 | 1 | 5 | 28 | 0 | 16 | 2162 | 0 | 2162 | 1.00 | True | False |
| 8 | 2 | 3 | 2 | 0 | 19 | 282 | 0 | 282 | 1.00 | True | False |
| 8 | 3 | 1 | 0 | 0 | 5 | 18 | 0 | 18 | 1.00 | True | False |
| 9 | 2 | 4 | 0 | 0 | 8 | 94 | 0 | 94 | 1.00 | True | False |
| 9 | 3 | 2 | 0 | 0 | 1 | 2 | 2 | 0 | 0.00 | True | None |

Census: S=256; D=606; (r*,c0) inj rows=6/6.

## OPEN

1. Constructive SR mark size ≤e·p
2. R-cell e·p injection
3. `|H_A_SP| ≤ 2170`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v36.py --check
```
