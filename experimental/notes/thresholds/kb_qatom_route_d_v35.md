# KB-MCA Route-D v35: SR-cell Type-D residual + matching highs

Status: `PARTIAL` — **SR-cell ⇒ residual multipads Type-D-only** PROVED;
**H_M ≤⌊n/e⌋** PROVED; SR-cell e·p cost and full |H_A_SP|≤2170 **OPEN**.

## Shared-root first-match cell (PROVED)

```text
Type S multipad  →  r_* = min{ r : mult(r) ≥ 2 }
pay at domain order r_*   (SR-cell)
```

After SR-cell:

```text
remaining multipads have t = 1  (Type D)
M_pad ≤ ⌊(n−2e)/m_c⌋ = 2 deployed
```

- Pays **star and non-star** Type S (non-star still has some mult≥2 root).
- Star-only residual is **not** forced (non-star exist ambiently).
- Connectedness / Helly not required.

### SR-cell cost (OPEN)

Naive mark `(r_*, high, c0U, c0V)` **collides** on toys. Per-root through-pack
structure available (v30/v33) for a future cost bound.

## Matching-supported highs (PROVED)

```text
M = matching of active free-1 e-sets
H_M = { high(U) : U ∈ M }
|H_M| ≤ |M| ≤ ⌊n/e⌋ = 31 ≤ 2170
```

Fits multi-tier / K_max high budget.

**Banked:** pairs with both sides in M are a tiny fraction of N_ord on toys —
matching-supported A_SP alone is too thin.

## Cardinality gate (PROVED)

```text
multi-tier FM injects H into [K_max]  ⇔  |H| ≤ 2170
```

Full |H_A_SP|≤2170 still OPEN.

## Toys

| j | w | free_core | #S (SR-paid) | #star | #nonstar | #D residual | max M_pad D | Type-D only? | #H_all | |H_M| | frac pairs both in M |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 4 | 1 | 1 | 0 | 0 | 0 | 540 | 4 | True | 17 | 7 | 0.000 |
| 5 | 1 | 2 | 908 | 424 | 484 | 64 | 2 | True | 17 | 6 | 0.000 |
| 5 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | True | 110 | 4 | 0.000 |
| 6 | 1 | 3 | 904 | 452 | 452 | 0 | 1 | True | 17 | 6 | 0.000 |
| 6 | 2 | 1 | 0 | 0 | 0 | 2 | 2 | True | 65 | 3 | 0.002 |
| 6 | 3 | -1 | 0 | 0 | 0 | 0 | 1 | True | 30 | 3 | 0.000 |
| 7 | 1 | 4 | 620 | 384 | 236 | 0 | 1 | True | 17 | 5 | 0.000 |
| 7 | 2 | 2 | 4 | 4 | 0 | 0 | 1 | True | 36 | 3 | 0.003 |
| 7 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | True | 13 | 2 | 0.000 |
| 8 | 1 | 5 | 364 | 208 | 156 | 0 | 1 | True | 16 | 5 | 0.000 |
| 8 | 2 | 3 | 2 | 2 | 0 | 0 | 1 | True | 19 | 3 | 0.000 |
| 8 | 3 | 1 | 0 | 0 | 0 | 0 | 1 | True | 5 | 2 | 0.000 |
| 9 | 2 | 4 | 0 | 0 | 0 | 0 | 1 | True | 8 | 3 | 0.000 |
| 9 | 3 | 2 | 0 | 0 | 0 | 0 | 1 | True | 1 | 1 | 1.000 |

Census: S paid by SR=2802; D residual=606;
nonstar=1328; SR mark coll rows=4.

## Payment path (updated)

```text
A_SP:
  SR-cell: pay Type S multipads (cost OPEN at e·p)
  residual multipads: Type D only, M_pad ≤ 2
  sides: H_M tags free if matching-supported; else need |H|≤2170 / multi-tier
R_sing: no multipads (v29)
```

## OPEN

1. SR-cell ≤ e·p (through-pack / peel cost)
2. |H_A_SP| ≤ 2170 or viable matching-supported + residual pair cell

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v35.py --check
```
