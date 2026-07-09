# KB-MCA Route-D v65: energy via `|G|^4`; subgroup `|G|≤√p+1`

Status: **energy identity + subgroup Gauss bound PROVED**; incomplete GP / soft-B
still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## Energy identity (PROVED, any t-set)

```text
G(α) = sum_{x in S} psi(α x)
r(s) = |S ∩ (s-S)|            (ordered pair count)
E_+(S) = sum_s r(s)^2 = p^{-1} sum_α |G(α)|^4
```

## L∞/L2 energy bound (PROVED)

```text
E_+(S) <= t^2 ( t^2 + (p-t)^2 ) / p
```

## Multiplicative subgroup (PROVED)

If `H ≤ F_p^*` has order `t | (p-1)` and `a ≠ 0`:

```text
|sum_{x in H} psi(a x)| <= sqrt(p) + t/(p-1) <= sqrt(p) + 1
E_+(H) <= t^4/p + (sqrt(p)+1)^4
```

Proof: expand `1_H` in multiplicative characters trivial on `H`; Gauss sums.

## Deployed geometry (PROVED)

```text
n = 2^21 | (p-1),   n' = 1183520 < n
residual arc = length-n' *prefix* of mu_n  (incomplete GP)
```

Subgroup bound applies to **full** order-`t` subgroups, not automatically to
the incomplete prefix. Soft-B bar remains `B_* = √(2 H2) ≈ 393171.6`.

## CAS

### Full subgroups

| p | t | max|G| | √p | ratio | E_+ | E_+/t² |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 3 | 2.79 | 7.81 | 0.36 | 15.0 | 1.67 |
| 61 | 4 | 3.68 | 7.81 | 0.47 | 36.0 | 2.25 |
| 61 | 5 | 3.27 | 7.81 | 0.42 | 45.0 | 1.80 |
| 61 | 6 | 4.77 | 7.81 | 0.61 | 90.0 | 2.50 |
| 61 | 10 | 5.09 | 7.81 | 0.65 | 310.0 | 3.10 |
| 61 | 12 | 4.85 | 7.81 | 0.62 | 540.0 | 3.75 |
| 61 | 15 | 3.92 | 7.81 | 0.50 | 975.0 | 4.33 |
| 61 | 20 | 4.79 | 7.81 | 0.61 | 2900.0 | 7.25 |
| 61 | 30 | 4.41 | 7.81 | 0.56 | 13530.0 | 15.03 |
| 73 | 3 | 2.82 | 8.54 | 0.33 | 15.0 | 1.67 |

### Incomplete GP prefixes (empirical)

| p | t | max|G| | √p | ratio | E_+ | ≤√p+1? |
|---|---:|---:|---:|---:|---:|---|
| 61 | 12 | 5.00 | 7.81 | 0.64 | 492.0 | Y |
| 61 | 15 | 5.92 | 7.81 | 0.76 | 1055.0 | Y |
| 61 | 30 | 6.37 | 7.81 | 0.82 | 13686.0 | Y |
| 101 | 20 | 7.27 | 10.05 | 0.72 | 2028.0 | Y |
| 101 | 40 | 7.43 | 10.05 | 0.74 | 26116.0 | Y |
| 127 | 18 | 7.59 | 11.27 | 0.67 | 1262.0 | Y |
| 127 | 36 | 10.31 | 11.27 | 0.92 | 14512.0 | Y |
| 127 | 63 | 11.26 | 11.27 | 1.00 | 125899.0 | Y |

- energy id max err = 5.8e-11
- subgroup max G/√p = 0.77
- incomplete max G/√p = 1.00
- fraction incomplete with Gmax≤√p+1 = 1.00

## Link

v64: e=3 `|All| ≤ √(E_+ p t)`; soft-B needs `max|S|≤B_*` at deployed.  
v65: controls `E_+` via `|G|^4` and proves the √p-law on **full** subgroups.  
Next: incomplete prefix estimates, or a direct soft-B attack on free-1 highs.

## OPEN

1. `|G|` for incomplete GP of length `n'` inside `mu_n` (deployed).  
2. `max|S| ≤ B_* ≈ 393172` at deployed `(n',e)`.  
3. Alternate `|R2|≤e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v65.py --check
```
