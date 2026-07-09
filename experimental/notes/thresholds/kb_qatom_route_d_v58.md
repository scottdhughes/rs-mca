# KB-MCA Route-D v58: Fourier identity for `coll` + conditional √-cancel

Status: **Plancherel + conditional bounds PROVED**; square-root cancellation **OPEN**.
Local on `scott/kb-route-d-T-bound`.

## Goal

```text
|T| <= coll/2
```
Close residual if `coll/2 <= H2` at deployed scale.

## Plancherel (PROVED)

```text
sum_h m_h^2 = p^{-(e-1)} sum_lambda |S(lambda)|^2
S(lambda) = sum_{e-subsets U of I_t} psi(<lambda, high(U)>)
coll = sum m_h^2 - C,   C = binom(t,e)
```

## Conditional bound (PROVED)

If `|S(lambda)| <= B` for all `lambda != 0`:

```text
coll  <=  C^2 / p^{e-1}  +  B^2
```

### Square-root cancellation corollary (PROVED conditional)

If `B <= sqrt(C)` for all nontrivial lambda:

```text
coll  <=  C^2 / p^{e-1}
```

**Deployed:** `log2(C^2/p^{e-1}) ≈ -1344154.6` ⇒ `coll = 0` ⇒ `T = 0`.

This is the cleanest residual-card close — **if** √-cancellation is proved.

## e=2 closed form (PROVED)

```text
S(lam) = (1/2)( G(lam)^2 - G(2 lam) )
G(lam) = sum_{k < t} psi(lam * omega^k)
```

Trivial `|G|<=t` ⇒ `|S|<=(t^2+t)/2` (too weak for H2 via coll; e=2 already uses `|T|<=p`).

## CAS (numpy FFT)

### e=2

| p | t | coll | max|B| | √C | B/√C | recon err |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 16 | 176 | 18.8 | 11.0 | 1.72 | 0e+00 |
| 61 | 24 | 1054 | 16.5 | 16.6 | 0.99 | 2e-13 |
| 61 | 34 | 4696 | 20.2 | 23.7 | 0.85 | 9e-13 |
| 61 | 50 | 23442 | 24.7 | 35.0 | 0.71 | 4e-12 |
| 101 | 16 | 102 | 24.0 | 11.0 | 2.19 | 0e+00 |
| 101 | 24 | 634 | 35.6 | 16.6 | 2.15 | 3e-13 |
| 101 | 34 | 2754 | 38.7 | 23.7 | 1.64 | 5e-13 |
| 101 | 50 | 13914 | 46.2 | 35.0 | 1.32 | 5e-12 |
| 127 | 16 | 86 | 23.3 | 11.0 | 2.13 | 3e-14 |
| 127 | 24 | 522 | 35.9 | 16.6 | 2.16 | 0e+00 |
| 127 | 34 | 2260 | 50.5 | 23.7 | 2.13 | 5e-13 |
| 127 | 50 | 10956 | 41.3 | 35.0 | 1.18 | 0e+00 |

### e=3

| p | t | coll | exp | max|B| | B/√C |
|---|---:|---:|---:|---:|---:|
| 31 | 12 | 24 | 50.1 | 32.0 | 2.16 |
| 31 | 18 | 446 | 692.0 | 73.7 | 2.58 |
| 31 | 24 | 3228 | 4260.7 | 82.2 | 1.83 |
| 31 | 30 | 14250 | 17148.3 | 50.1 | 0.79 |
| 61 | 12 | 0 | 12.9 | 41.0 | 2.77 |
| 61 | 18 | 84 | 178.7 | 71.1 | 2.49 |
| 61 | 24 | 766 | 1100.4 | 97.0 | 2.16 |
| 61 | 30 | 3410 | 4428.8 | 144.0 | 2.26 |

Census: Plancherel OK; B/√C in [0.71, 8.24]
(near square-root cancellation empirically, not a proof).

## Gap

| Bound on max|S| | Enough for deployed T=0? |
|---|---|
| Trivial e=2 O(t²) | No |
| √C (random / L² folklore) | **Yes** (conditional theorem) |
| Proved √C for free-1 highs on GP | **OPEN** |

## OPEN

Prove square-root cancellation (or any sufficient B) for

```text
S(lambda) = sum_{U subset I_{n'}, |U|=e} psi(<lambda, high(U)>)
```

on the KB roots-of-unity arc — especially e≥3 sparse regime.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v58.py --check
```
