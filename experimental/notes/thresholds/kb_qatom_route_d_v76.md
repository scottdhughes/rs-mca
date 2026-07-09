# KB-MCA Route-D v76: `coll ≤ 2 C(t,2e)`

Status: **union collision bound PROVED**; residual still **OPEN**.  
Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED

```text
coll  <=  2 * binom(t, 2e)     (t >= 2e)
coll  <=  min( (⌊t/e⌋-1) C(t,e) ,  2 C(t,2e) )
```

### Why

- Each unordered multipad pair `{A,B}` has unique `W=A∪B` of size `2e`.  
- Each `W` hosts **at most one** such pair (packing on a 2e-set: `m_h ≤ 2`).  
- Hence `#unordered pairs ≤ C(t,2e)`, so `coll = 2 · #unordered ≤ 2 C(t,2e)`.

Near `t ~ 2e` this dominates packing; at larger `t/e` packing often wins.

## Deployed

| | |
|---|---|
| bound | `min(16 · C(n',e), 2 · C(n',2e))` |
| vs `2 H2` | still far larger |
| residual close alone? | **no** |

## CAS

| p | e | t | coll | 2 C(t,2e) | (K-1)C | min | tighter |
|---|---:|---:|---:|---:|---:|---:|---|
| 61 | 3 | 5 | 0 | 0 | 0 | 0 | - |
| 61 | 3 | 6 | 0 | 2 | 20 | 2 | U |
| 61 | 4 | 7 | 0 | 0 | 0 | 0 | - |
| 61 | 4 | 8 | 0 | 2 | 70 | 2 | U |
| 101 | 3 | 5 | 0 | 0 | 0 | 0 | - |
| 101 | 3 | 6 | 0 | 2 | 20 | 2 | U |
| 101 | 4 | 7 | 0 | 0 | 0 | 0 | - |
| 101 | 4 | 8 | 0 | 2 | 70 | 2 | U |
| 127 | 3 | 5 | 0 | 0 | 0 | 0 | - |
| 127 | 3 | 6 | 0 | 2 | 20 | 2 | U |
| 127 | 4 | 7 | 0 | 0 | 0 | 0 | - |
| 127 | 4 | 8 | 0 | 2 | 70 | 2 | U |
| 61 | 3 | 13 | 4 | 3432 | 858 | 858 | P |
| 61 | 3 | 17 | 58 | 24752 | 2720 | 2720 | P |
| 61 | 3 | 20 | 202 | 77520 | 5700 | 5700 | P |
| 61 | 3 | 24 | 766 | 269192 | 14168 | 14168 | P |
| 61 | 4 | 16 | 2 | 25740 | 5460 | 5460 | P |
| 101 | 3 | 9 | 2 | 168 | 168 | 168 | P |
| 101 | 3 | 15 | 22 | 10010 | 1820 | 1820 | P |
| 101 | 3 | 17 | 34 | 24752 | 2720 | 2720 | P |

(U = union tighter, P = packing tighter)

## OPEN

Drive `coll → 0` at `t=n'` or SoftB — residual PR material.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v76.py --check
```
