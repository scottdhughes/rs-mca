# KB-MCA Route-D v62: Gauss-sharp All bound

Status: **refined All envelope PROVED** (`|All| <= sqrt(p) t W_inf <= p t^{3/2}`);
still **too weak** for √-cancel. Local on `scott/kb-route-d-T-bound`.

## Gauss flatness (PROVED)

```text
H(s) = psi(a s^2 + b s),  a != 0
|hatH(xi)| = sqrt(p)  for all xi
```

## Refined All (PROVED)

```text
All = p^{-1} sum_xi hatH(-xi) hat_mu(xi)^3
|All| <= p^{-1/2} sum |hat_mu|^3
      <= p^{-1/2} W_inf * (p t)
      = sqrt(p) * t * W_inf
      <= p * t^{3/2}          (v61 W_inf <= sqrt(p t))
```

v60/v61 used `|All| <= sqrt(p) W_inf^3 <= p^2 t^{3/2}`.  
Sparse improvement factor `~ sqrt(p/t)`.

## S envelope (PROVED, still weak)

```text
|S| <= (1/6)( sqrt(p) t W_inf + O(t^2) ) <= (1/6)( p t^{3/2} + O(t^2) )
bound / sqrt(C) ~ p / sqrt(6)  -> infinity
```

## CAS

### |All| vs bounds (sample)

| p | t | (l0,l1) | |All| | new | old (v60) | new/old |
|---|---:|---|---:|---:|---:|---:|
| 61 | 12 | 1,1 | 90.1 | 6.4e+02 | 2.5e+03 | 0.256 |
| 61 | 12 | 3,5 | 58.4 | 6.9e+02 | 3.2e+03 | 0.219 |
| 61 | 12 | 2,7 | 28.2 | 6.6e+02 | 2.7e+03 | 0.243 |
| 61 | 15 | 1,1 | 147.5 | 8.7e+02 | 3.2e+03 | 0.271 |
| 61 | 15 | 3,5 | 117.6 | 8.2e+02 | 2.7e+03 | 0.304 |
| 61 | 15 | 2,7 | 172.9 | 9.3e+02 | 3.9e+03 | 0.239 |
| 101 | 12 | 1,1 | 156.2 | 9.7e+02 | 5.2e+03 | 0.186 |
| 101 | 12 | 3,5 | 103.2 | 9.8e+02 | 5.4e+03 | 0.181 |

### max|S|

| p | t | max|S| | new bound | √C | S/√C | new/√C |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 15 | 60.0 | 4.0e+02 | 21.3 | 2.81 | 1.9e+01 |
| 61 | 24 | 97.0 | 1.0e+03 | 45.0 | 2.16 | 2.3e+01 |
| 61 | 36 | 175.5 | 2.3e+03 | 84.5 | 2.08 | 2.7e+01 |
| 101 | 15 | 57.2 | 4.8e+02 | 21.3 | 2.68 | 2.3e+01 |
| 101 | 24 | 136.2 | 1.2e+03 | 45.0 | 3.03 | 2.8e+01 |
| 101 | 36 | 221.0 | 2.8e+03 | 84.5 | 2.62 | 3.3e+01 |
| 127 | 15 | 69.8 | 5.3e+02 | 21.3 | 3.27 | 2.5e+01 |
| 127 | 24 | 127.1 | 1.4e+03 | 45.0 | 2.83 | 3.0e+01 |
| 127 | 36 | 221.8 | 3.1e+03 | 84.5 | 2.63 | 3.6e+01 |

- |hatH| flat on all 12 Gauss rows.
- new/old ratio in [0.126, 0.304] on id rows (always < 1).
- Empirical S/√C max = 3.27.
- new/√C max on toys = 3.6e+01.
- Deployed asymptotic `p/sqrt(6)` ≈ 10^8.9.

## Link

v58 needs `|S|<=√C`.  
v61 killed pure `W_inf^3` path at `p^2`.  
v62 improves to `p` but **still short**.  
Next must use **phase** of `hat_mu` on the GP arc.

Deployed e=67472 ≫ 3 after e=3 is sharp.

## OPEN

1. Oscillatory `sum_xi hatH(-xi) hat_mu(xi)^3` for GP free-1 highs.  
2. `|S|<=√C` then general e; or alternate `|R2|<=e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v62.py --check
```
