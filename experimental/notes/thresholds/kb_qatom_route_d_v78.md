# KB-MCA Route-D v78: multipad factorization identity

Status: **factorization form PROVED**; deployed nonexistence **OPEN** (residual PR).  
Local on `scott/kb-route-d-T-bound`.

## BOARD identity (PROVED)

A free-1 multipad produces a 2e-set `R` of arc values and

```text
(phi - alpha)(phi - beta)  =  Pi_R(X)  :=  prod_{r in R} (X - r)

phi monic, deg e,  phi(0) = 0,  alpha != beta
```

### Corollaries (PROVED)

```text
alpha * beta  =  prod_{r in R} r
2 c_{e-1}   =  - sum_{r in R} r     (p odd)
```

where `phi = X^e + c_{e-1} X^{e-1} + ... + c_1 X`.

### Residual PR shape

```text
no arc 2e-set R admits this factorization
        =>  multipad-free
        =>  |T| = 0  ≤ H2     (v77)
```

## CAS

| p | e | t | #mp highs | #pairs checked | id OK? |
|---|---:|---:|---:|---:|---|
| 61 | 3 | 13 | 2 | 2 | Y |
| 61 | 3 | 17 | 29 | 25 | Y |
| 61 | 3 | 24 | 326 | 25 | Y |
| 101 | 3 | 9 | 1 | 1 | Y |
| 101 | 3 | 17 | 17 | 17 | Y |
| 101 | 4 | 21 | 3 | 3 | Y |
| 127 | 3 | 16 | 1 | 1 | Y |
| 127 | 4 | 21 | 1 | 1 | Y |
| 43 | 3 | 12 | 7 | 7 | Y |
| 73 | 4 | 14 | 1 | 1 | Y |

## Deployed

| | |
|---|---:|
| n' | 1183520 |
| e | 67472 |
| residual closed? | **no** (hypothesis open) |

## OPEN

Prove **no factorization** on the deployed arc — then open residual PR with `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v78.py --check
```
