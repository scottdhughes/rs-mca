# KB-MCA Route-D v61: `W_inf <= sqrt(p t)` PROVED; envelope dead for √-cancel

Status: **W_inf bound PROVED**; e=3 absolute envelope **too weak** (structural);
oscillatory triple-Fourier path **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Per-A Plancherel (PROVED)

For any t-set `S_arc subset F_p` and any `A`:

```text
W(A,B) = sum_{x in S_arc} psi(A x^2 + B x)
f_A(x) = 1_S(x) psi(A x^2)
sum_B |W(A,B)|^2 = p sum_x |f_A|^2 = p t
=> max_B |W(A,B)| <= sqrt(p t)
=> W_inf := max_{A,B} |W| <= sqrt(p t)
```

No GP hypothesis: holds for every t-set.

## e=3 envelope (PROVED, and dead)

Combine with v60 `|All| <= sqrt(p) W_inf^3`:

```text
|All| <= p^2 t^{3/2}
|S|   <= (1/6)( p^2 t^{3/2} + 3t(t-1)+t )
bound / sqrt(C) ~ p^2 / sqrt(6)  -> infinity
```

Even the optimistic typical size `W_inf ~ sqrt(t)` only yields ratio `~ sqrt(p)`.
Absolute-value estimates on the triple Fourier sum **cannot** force v58 √-cancel.

## CAS

### Plancherel / W_inf

| p | t | W_inf (sample) | √(pt) | ratio | Plancherel rel err |
|---|---:|---:|---:|---:|---:|
| 61 | 12 | 12.0 | 27.1 | 0.44 | 3.1e-16 |
| 61 | 24 | 24.0 | 38.3 | 0.63 | 3.1e-16 |
| 61 | 36 | 36.0 | 46.9 | 0.77 | 4.1e-16 |
| 101 | 15 | 15.0 | 38.9 | 0.39 | 3.0e-16 |
| 101 | 36 | 36.0 | 60.3 | 0.60 | 2.5e-16 |
| 127 | 15 | 15.0 | 43.6 | 0.34 | 4.8e-16 |
| 127 | 36 | 36.0 | 67.6 | 0.53 | 6.0e-16 |

### e=3 max|S| vs envelope

| p | t | max|S| | envelope | √C | S/√C | env/√C |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 15 | 60.0 | 3.6e+04 | 21.3 | 2.81 | 1.7e+03 |
| 61 | 24 | 97.0 | 7.3e+04 | 45.0 | 2.16 | 1.6e+03 |
| 61 | 36 | 175.5 | 1.3e+05 | 84.5 | 2.08 | 1.6e+03 |
| 101 | 15 | 57.2 | 9.9e+04 | 21.3 | 2.68 | 4.6e+03 |
| 101 | 24 | 136.2 | 2.0e+05 | 45.0 | 3.03 | 4.4e+03 |
| 101 | 36 | 221.0 | 3.7e+05 | 84.5 | 2.62 | 4.4e+03 |
| 127 | 15 | 69.8 | 1.6e+05 | 21.3 | 3.27 | 7.3e+03 |
| 127 | 24 | 127.1 | 3.2e+05 | 45.0 | 2.83 | 7.0e+03 |
| 127 | 36 | 221.8 | 5.8e+05 | 84.5 | 2.63 | 6.9e+03 |

- Plancherel max rel err = 6.0e-16.
- max W_inf/√(pt) = 0.77.
- Empirical S/√C max = 3.27.
- Envelope/√C max on toys = 7.3e+03.
- Deployed asymptotic factor `p^2/sqrt(6)` ≈ 10^18.3.

## Link to residual card

v58 needs `|S|<=√C` ⇒ `T=0` at deployed.  
v60 reduced e=3 to `W_inf`.  
v61 **closes** `W_inf<=√(pt)` and **kills** the pure-envelope path.  
Next: phase cancellation in `All = p^{-1} sum hatH(-xi) hat_mu(xi)^3`.

Deployed e=67472 ≫ 3 needs general-e after e=3 is sharp.

## OPEN

1. Oscillatory bound on the triple Fourier sum for free-1 e=3 on GP arcs.  
2. Reach `|S|<=√C` sparsely for e=3, then general e.  
3. Alternate residual close `|R2|<=e·p` if exp-sums stall.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v61.py --check
```
