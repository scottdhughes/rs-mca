# KB-MCA Route-D v75: multipad span `≥ 2e`

Status: **span ≥ 2e + AP-union ban PROVED**; large-t / deployed ban still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
multipad  =>  t >= 2e+1
          =>  span(G) >= 2e
          =>  W = A cup B is not a contiguous 2e-block
          =>  W is not an AP of length 2e with ord(omega^d) > 2e
          =>  W has a hole in [min,max]
```

### Why span ≥ 2e

|W|=2e. Span = 2e−1 ⇒ W contiguous (AP, d=1) ⇒ rescale to pure GP of length 2e  
⇒ forbidden by v74 when n > 2e. Hence span ≥ 2e.

## Deployed

| | |
|---|---:|
| 2e | 134944 |
| min span if multipad | ≥ 134944 |
| n' | 1183520 |
| n'/e | 17.54 |

Necessary conditions only — **not** a residual close.

## CAS

### Multipad geometry

| p | e | t | #pairs | min span | max span | #contig | #bad AP |
|---|---:|---:|---:|---:|---:|---:|---:|
| 61 | 3 | 13 | 2 | 12 | 12 | 0 | 0 |
| 61 | 3 | 17 | 29 | 12 | 16 | 0 | 0 |
| 61 | 3 | 24 | 383 | 12 | 23 | 0 | 0 |
| 101 | 3 | 9 | 1 | 8 | 8 | 0 | 0 |
| 101 | 3 | 17 | 17 | 8 | 14 | 0 | 0 |
| 101 | 4 | 21 | 3 | 19 | 20 | 0 | 0 |
| 127 | 3 | 16 | 1 | 15 | 15 | 0 | 0 |
| 127 | 4 | 21 | 1 | 20 | 20 | 0 | 0 |
| 43 | 3 | 12 | 7 | 7 | 10 | 0 | 0 |
| 73 | 4 | 14 | 1 | 13 | 13 | 0 | 0 |

### First multipad t

| p | e | first t | 2e | t/e |
|---|---:|---:|---:|---:|
| 61 | 3 | 13 | 6 | 4.33 |
| 61 | 4 | 16 | 8 | 4.00 |
| 61 | 5 | None | 10 | - |
| 73 | 3 | 11 | 6 | 3.67 |
| 73 | 4 | 14 | 8 | 3.50 |
| 73 | 5 | None | 10 | - |
| 101 | 3 | 9 | 6 | 3.00 |
| 101 | 4 | 20 | 8 | 5.00 |
| 101 | 5 | None | 10 | - |
| 127 | 3 | 16 | 6 | 5.33 |
| 127 | 4 | 21 | 8 | 5.25 |
| 127 | 5 | None | 10 | - |
| 43 | 3 | 8 | 6 | 2.67 |
| 43 | 4 | 16 | 8 | 4.00 |
| 43 | 5 | 17 | 10 | 3.40 |

## OPEN

Large-t multipad ban up to n', or SoftB — next residual-board hit.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v75.py --check
```
