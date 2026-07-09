# KB-MCA Route-D v63: bilinear All + high energy

Status: **factorization + energy identities PROVED**; absolute bounds still
**short** of `|S|<=√C`. Local on `scott/kb-route-d-T-bound`.

## Bilinear factorization (PROVED)

```text
Phi(u,v,w) = -l0(u+v+w) + l1(uv+uw+vw)
           = [-l0(u+v)+l1 uv] + w [-l0 + l1(u+v)]

All = sum_{i,j} psi(-l0(vi+vj)+l1 vi vj) * G(-l0 + l1(vi+vj))
G(alpha) = sum_{k<t} psi(alpha v_k)
```

## Absolute bound (PROVED, still weak)

```text
|All| <= sum_s r2(s) |G(-l0 + l1 s)|
      <= t^2 (1 + M),   M = max_{a!=0}|G(a)| <= sqrt(p t - t^2)
```

Regime vs v62 (`|All|<= p t^{3/2}`): bilinear better iff `t = o(sqrt(p))`.  
Deployed `n'/sqrt(p) ≈ 25.6` ⇒ **v62 tighter**; both ≫ √C.

## Fourth moment = energy (PROVED)

```text
sum_lambda |S|^2 = p^{e-1} sum_h m_h^2
sum_lambda |S|^4 = p^{e-1} sum_z r_m(z)^2
```

If highs injective (`sum m^2 = C`), RMS of `S` is exactly `√C` (v58 threshold).

## CAS

### Bilinear rows

| p | t | (l0,l1) | |All| | r2|G| bound | v62 | r2G/v62 | |S|/√C |
|---|---:|---|---:|---:|---:|---:|---:|
| 61 | 12 | 1,1 | 90.1 | 4.2e+02 | 2.5e+03 | 0.16 | 1.34 |
| 61 | 12 | 3,5 | 58.4 | 4.5e+02 | 2.5e+03 | 0.18 | 0.66 |
| 61 | 15 | 1,1 | 147.5 | 6.7e+02 | 3.5e+03 | 0.19 | 1.20 |
| 61 | 15 | 3,5 | 117.6 | 7.3e+02 | 3.5e+03 | 0.21 | 0.99 |
| 101 | 15 | 1,1 | 89.6 | 7.3e+02 | 5.9e+03 | 0.12 | 0.56 |
| 101 | 15 | 3,5 | 250.1 | 7.5e+02 | 5.9e+03 | 0.13 | 1.72 |
| 101 | 20 | 1,1 | 373.4 | 1.5e+03 | 9.0e+03 | 0.16 | 1.76 |
| 101 | 20 | 3,5 | 336.5 | 1.5e+03 | 9.0e+03 | 0.17 | 1.65 |

### Energy / max|S|

| p | t | C | sum m² | max m | max|S|/√C | energy/C² | RMS/√C |
|---|---:|---:|---:|---:|---:|---:|---:|
| 61 | 12 | 220 | 220 | 1 | 2.77 | 14.796 | 1.000 |
| 61 | 20 | 1140 | 1342 | 3 | 2.40 | 350.723 | 1.085 |
| 61 | 36 | 7140 | 18338 | 7 | 2.08 | 13701.357 | 1.603 |
| 101 | 15 | 455 | 477 | 2 | 2.68 | 22.259 | 1.024 |
| 101 | 24 | 2024 | 2278 | 2 | 3.03 | 403.479 | 1.061 |
| 127 | 15 | 455 | 455 | 1 | 3.27 | 14.759 | 1.000 |
| 127 | 36 | 7140 | 9348 | 3 | 2.63 | 3162.273 | 1.144 |

- factorization max err = 1.6e-11
- max S/√C = 3.27
- r2G/v62 in [0.11, 0.21]
- max bound_S/√C (bilinear) = 1.5e+01

## Link

v58 needs pointwise `|S|<=√C`. L2 already sits there.  
v60–v62 exhausted `|hat_mu|` envelopes.  
v63 reduces All to **oscillatory bilinear** `sum psi(K) G(alpha)`.

Deployed e=67472 ≫ 3 after e=3 is sharp.

## OPEN

1. Phase-sensitive bound on `sum_{i,j} psi(K(vi,vj)) G(alpha(vi,vj))`.  
2. GP structure of additive energy of free-1 highs (secondary).  
3. Stress-search for counterexample `|S|>√C` on larger sparse toys.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v63.py --check
```
