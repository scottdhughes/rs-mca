# KB-MCA Route-D v66: incomplete GP `|G|` bound

Status: **incomplete GP bound PROVED**; soft-B for free-1 `S` still **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Theorem (PROVED)

For `omega` of order `n | (p-1)`, `1 <= t <= n`, `alpha != 0`:

```text
G_t(alpha) = sum_{k=0}^{t-1} psi(alpha omega^k)

|G_t(alpha)|  <=  (t/n)(sqrt(p)+1)  +  sqrt(p) (1 + ln n)
```

### Proof outline

1. **Dirichlet completion** on `Z/nZ`: `G_t = n^{-1} sum_m D(m) J(m,alpha)`.  
2. **`|J(0)| <= sqrt(p)+1`**, **`|J(m)| <= sqrt(p)`** (`m != 0`) by subgroup /
   mixed Gauss sums (v65 + character expansion of `1_H`).  
3. **`sum_{m!=0} |D(m)| <= n(1+ln n)`** via `|D| <= n/(2d(m))` and harmonic sums.  
4. Triangle inequality yields the bound.

## Deployed numerics (PROVED arithmetic)

| quantity | value |
|---|---:|
| n | 2097152 |
| n' | 1183520 |
| t/n | 0.5643 |
| ln n | 14.556 |
| **incomplete |G| bound** | **744113.1** |
| Plancherel √(pt−t²) | 50202917.8 |
| bound / Plancherel | 0.0148 |
| B_\* = √(2 H2) | 393171.6 |
| bound / B_\* | 1.89 |

Incomplete linear `|G|` is ~**67×** tighter than Plancherel at deployed, and within
~**1.9×** of the soft-B scale `B_\*` — but **soft-B applies to free-1 high sums `S`**,
not to linear arc sums `G`.

## CAS

| p | n | t | max|G| | bound | Plancherel | Gmax/bound |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 60 | 15 | 5.92 | 42.0 | 26.3 | 0.141 |
| 61 | 60 | 30 | 6.37 | 44.2 | 30.5 | 0.144 |
| 61 | 60 | 45 | 6.15 | 46.4 | 26.8 | 0.133 |
| 61 | 60 | 60 | 1.00 | 48.6 | 7.7 | 0.021 |
| 101 | 100 | 25 | 8.86 | 59.1 | 43.6 | 0.150 |
| 101 | 100 | 50 | 9.58 | 61.9 | 50.5 | 0.155 |
| 101 | 100 | 75 | 8.89 | 64.6 | 44.2 | 0.138 |
| 101 | 100 | 100 | 1.00 | 67.4 | 10.0 | 0.015 |
| 127 | 126 | 31 | 10.27 | 68.8 | 54.6 | 0.149 |
| 127 | 126 | 63 | 11.26 | 71.9 | 63.5 | 0.157 |
| 127 | 126 | 94 | 11.04 | 74.9 | 55.7 | 0.147 |
| 127 | 126 | 126 | 1.00 | 78.0 | 11.2 | 0.013 |
| 73 | 72 | 24 | 6.66 | 48.3 | 34.3 | 0.138 |
| 73 | 72 | 48 | 7.26 | 51.4 | 34.6 | 0.141 |
| 97 | 96 | 32 | 8.62 | 58.4 | 45.6 | 0.148 |
| 97 | 96 | 64 | 7.97 | 62.0 | 46.0 | 0.129 |

- all rows satisfy Gmax ≤ bound (max Gmax/bound = 0.157)
- Dirichlet mass checks: 7 rows OK

## Link

v65: full subgroup `|G|≤√p+1`; deployed arc incomplete.  
v66: **incomplete bound proved**.  
e=2 / bilinear e=3 can now use `|G| ≪ √(pt)`.  
Residual close still needs `max|S|≤B_\*≈393172` for free-1 highs.

## OPEN

1. **Primary:** `max_{λ≠0} |S(λ)| ≤ B_\*` at deployed `(n',e)`.  
2. Feed incomplete `|G|` into e=3 CS / energy for sharper toy bounds.  
3. Alternate `|R2|≤e·p`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v66.py --check
```
