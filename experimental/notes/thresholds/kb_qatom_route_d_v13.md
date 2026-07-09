# KB-MCA Route-D v13: block factorization of multi-mates

Status: `PARTIAL` — scale recursion **PROVED**; residual long-trade ban **OPEN**.

## Block factorization (PROVED, unconditional)

If `Phi_w(C)=Phi_w(C')`, `C ≠ C'`, set `R=C∩C'`, `U=C\\C'`, `V=C'\\C`, `s=|U|`:

```text
s ≥ w+1
Phi_w(U) = Phi_w(V)          (same depth w on blocks)
Λ_C − Λ_{C'} = Λ_R (Λ_U − Λ_V)
|C △ C'| = 2s
```

## Scale dictionary

| Block size s | Trade | Meaning |
|---:|---|---|
| s = w+1 = 67472 | min-weight | tight free-1 CS |
| s ≥ w+2 | long | free_s = s−w ≥ 2 multi-mate of blocks |
| s = 2^17 (v8) | long | coset pad |

Deployed long scales: `s ∈ [67473, 913632]`
(846160 values).

## Recursion (PROVED)

```text
long multi-mate at (m,w)
    ⇒  multi-mate at some (s,w), s ∈ [w+2, m]
padding multi-mate at (s,w)
    ⇒  multi-mate at (m,w)  (when room)
```

## Conditional criterion

```text
M_s^{max}(w) ≤ 1  for all s ∈ [w+2, m]
    ⇒  only tight multi-mates at (m,w)
    + pairwise-tight residual cliques
    ⇒  M_m^{res} ≤ k_tight = 18
    ⇒  U_res ≤ target/(17·18) ≈ 2^{49.67}
```

## Toys

### Full m-fibers (factorization checks on all pairs)

| m | w | free | Mm | #tight s | #long s | s histogram |
|---|---|---:|---:|---:|---:|---|
| 4 | 2 | 2 | 8 | 3520 | 1494 | {3: 3520, 4: 1494} |
| 5 | 2 | 3 | 17 | 15840 | 15312 | {3: 15840, 4: 11952, 5: 3360} |
| 5 | 3 | 2 | 3 | 1008 | 112 | {4: 1008, 5: 112} |
| 6 | 2 | 4 | 32 | 42240 | 65112 | {3: 42240, 4: 41832, 5: 20160, 6: 3120} |
| 6 | 3 | 3 | 5 | 3528 | 952 | {4: 3528, 5: 672, 6: 280} |
| 6 | 4 | 2 | 2 | 0 | 40 | {6: 40} |

### Residual-proxy can-cores (aperiodic j)

| j | m | w | Mm_res | #tight | #long | s hist |
|---|---|---|---:|---:|---:|---|
| 9 | 6 | 2 | 10 | 2555 | 1949 | {3: 2555, 5: 378, 4: 1550, 6: 21} |
| 7 | 4 | 2 | 5 | 511 | 155 | {3: 511, 4: 155} |
| 10 | 6 | 3 | 2 | 30 | 0 | {4: 30} |
| 6 | 3 | 2 | 3 | 73 | 0 | {3: 73} |
| 9 | 5 | 3 | 2 | 20 | 0 | {4: 20} |

## Unconditional atom?

Still **no**. But long trades are no longer an unstructured remainder:
they are multi-mates at long block scales.

## Next real math

1. Residual (or first-match payment) forbids multi-mates at scales s ≥ w+2, **or**
2. Bound max fiber at long scales after residual pruning, **or**
3. `M_m^{res} ≤ 1` / `U_phi` directly.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v13.py
python3 experimental/scripts/verify_kb_qatom_route_d_v13.py --check
```
