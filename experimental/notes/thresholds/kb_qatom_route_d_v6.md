# KB-MCA Route-D v6: B1 free-regime uniqueness and B2 U_res structure

Status: `PARTIAL` — free-0/free-1 uniqueness **PROVED**; deployed B1 **OPEN**; B2 structure **PROVED**, absolute budget **OPEN**.

## B1 — M_m uniqueness

### Theorem B1.0 — free = 0 (PROVED)

If `w >= m`, then `M_m^{max} <= 1`.

Proof: full monic coefficient vector determined; unique roots.

### Theorem B1.1 — free = 1 (PROVED)

If `w = m-1`, then `M_m^{max} <= floor(n/m)` by constant-shift packing.

### Theorem B1.side — e = w+1 always free = 1 (PROVED)

Depth-w fibers of e-subsets have size `<= floor(n/e) = 31` at deployed.

### Deployed B1 status (AUDIT)

```text
m = 913632
w = 67471
free = m-w = 846161
log2(avg m-fiber) ≈ -18820.25
```

Deployed is **far** from free-0 (`w=m`) and free-1 (`w=m-1=913631`): gap in w is `846160`.
Entropy still says max is typically 0/1; unconditional uniqueness at free=`846161` remains OPEN.

## B2 — U_res bounds

### Theorem B2.structure (PROVED)

1. `U_res(z) <= |R(z)|`
2. Each side-prefix u has `<= floor(n/e)` realizing e-subsets
3. `N_can_prim <= U_res * M_m^{max}`
4. If `M_m^{max} <= 1` then `N_can_prim <= U_res`

### Budgets if M_m = 1

```text
U_res <= 16166878605395467  (~2^{53.84}) for K_rem atom form
U_res <= 8456648496904   (~2^{42.94}) for |D_prim|<=t*p
```

Absolute (non-circular) atom-scale bound on `U_res` is still OPEN.

## Combined criterion (PROVED conditional)

If `M_m^{max} <= K` and `U_res <= floor(target/(17 K))`, then `|R| <= target`.

## Toy suite

Free-0/free-1: 44 checks, all OK.

Residual structure:

| p | n | w | max R | max U_res | max U/u | max S/u | floor(n/e) |
|---|---|---|---:|---:|---:|---:|---:|
| 17 | 16 | 2 | 49 | 34 | 3 | 7 | 5 |
| 17 | 16 | 3 | 5 | 5 | 2 | 2 | 4 |
| 97 | 32 | 2 | 33 | 32 | 3 | 3 | 10 |
| 97 | 32 | 3 | 7 | 7 | 7 | 7 | 8 |
| 193 | 64 | 2 | 32 | 25 | 4 | 4 | 21 |

## What closes the atom

| Piece | Status |
|---|---|
| free-0 / free-1 uniqueness | PROVED (wrong free for deployed m) |
| side free-1 packing | PROVED (deployed) |
| residual routing N_can_prim <= U_res M_m | PROVED |
| deployed M_m^{max} <= 1 | **OPEN (B1)** |
| U_res <= target/17 | **OPEN (B2)** |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v6.py
python3 experimental/scripts/verify_kb_qatom_route_d_v6.py --check
```
