# KB-MCA Route-D v8: B1 uniqueness REFUTED

Status: `PROVED REFUTATION` — `M_m^{max} <= 1` is **FALSE** at deployed parameters.

## Main theorem

On the deployed domain `D = mu_n`, `n = 2^{21}`, set `e0 = 2^{17} = 131072` (divides `n`).

1. Cosets of the order-`e0` subgroup have locators `X^{e0} - a` and form one free-1
   pencil of size `n/e0 = 16`.
2. Padding any two such cosets with a common `R` of size `m - e0` produces two
   distinct m-subsets with **identical** depth-`w` monic prefixes for deployed `w`.
3. Therefore **`M_m^{max} >= 2`**. Uniqueness is refuted.

### Improved lower bound

```text
M_m^{max}  >=  k_max  =  1 + floor((n-m)/e0)  =  10
```

(one can keep `k_max` cosets simultaneously disjoint from a single admissible `R`).

## Proof ingredients

### Coset locator
`Lambda_{gH}(X) = X^{e0} - g^{e0}` for `|H|=e0 | n`.

### Padding
`Lambda_{R cup U} - Lambda_{R cup V} = c Lambda_R` has degree `m-e0 <= m-w-1`
when `e0 >= w+1`, so the first `w` high monic coefficients agree.

### Deployed arithmetic
```text
e0 = 131072 | n
e0 >= w+1 = 67472
m-e0 = 782560 <= m-w-1 = 846160
n-2*e0 = 1835008 >= m-e0
```

## Impact

| Previous hope | Status |
|---|---|
| B1: `M_m <= 1` | **REFUTED** |
| v5 criterion needing `M_m <= 1` | **Dead premise** |
| B2 / residual core-prefix image | Still OPEN; still the right wall |

### Revised budgets (if one only knows `M_m >= k_max` and uses `K = k_max`)

```text
U_res <= target/(17 * 10) = 1616687860539546
         ≈ 2^{50.52}
```

A tight **upper** bound on `M_m` would restore a better budget.

## Toy verification of padding

| p | n | e0 | w | m | Phi_w match | k_max |
|---|---|---|---|---|---|---|
| 17 | 16 | 4 | 2 | 6 | True | 3 |
| 17 | 16 | 4 | 2 | 8 | True | 3 |
| 97 | 32 | 8 | 5 | 12 | True | 3 |
| 97 | 32 | 8 | 3 | 20 | True | 2 |
| 193 | 64 | 16 | 10 | 40 | True | 2 |

## Next real math

1. Upper-bound `M_m` (coset pencil gives only a lower bound of 10).
2. Or bound residual can-core `Phi_w`-image (B2) without going through small `M_m`.
3. Do not spend effort proving `M_m <= 1`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v8.py
python3 experimental/scripts/verify_kb_qatom_route_d_v8.py --check
```
