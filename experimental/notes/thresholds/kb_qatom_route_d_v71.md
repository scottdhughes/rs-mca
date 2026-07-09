# KB-MCA Route-D v71: full support of `P_e`

Status: **`P_e` full support PROVED** (`e < ord ω`); multipad = cancelled multiple
with `supp=2e` **OPEN** to ban at deployed. Local on `scott/kb-route-d-T-bound`.

## q-binomial / nonvanishing (PROVED)

For `ord(ω)=n` and `1 ≤ e < n`:

```text
e_j(1,ω,...,ω^{e-1}) = ω^{j(j-1)/2} * binom(e,j)_ω
binom(e,j)_ω = prod_{i=0}^{j-1} (ω^{e-i}-1)/(ω^{i+1}-1)
```

All factors nonzero because `ω^m ≠ 1` for `1 ≤ m ≤ e < n`.  
Hence every `e_j ≠ 0`.

## Full support (PROVED)

```text
P_e(X) = prod_{k=0}^{e-1} (X - ω^k)
       = sum_j (-1)^{e-j} e_{e-j} X^j
supp(P_e) = e+1 = deg(P_e)+1
```

Deployed: `e=67472 < n=2097152` ⇒ **`supp(P_e) = e+1 = 67473`**.

## Multipad constraint (PROVED)

```text
G = P_e * H,   supp(G) = 2e = 134944
e >= 2  ⇒  2e > e+1  ⇒  deg H >= 1   (not a scalar multiple of P_e)
```

Multipads require **cancellation** in the product down to support `2e`.

## CAS

### P_e formula / support (sample)

| p | e | supp(P_e) | full? | formula? |
|---|---:|---:|---|---|
| 61 | 2 | 3 | Y | Y |
| 61 | 3 | 4 | Y | Y |
| 61 | 4 | 5 | Y | Y |
| 61 | 5 | 6 | Y | Y |
| 61 | 6 | 7 | Y | Y |
| 61 | 7 | 8 | Y | Y |
| 61 | 8 | 9 | Y | Y |
| 61 | 9 | 10 | Y | Y |
| 61 | 10 | 11 | Y | Y |
| 61 | 11 | 12 | Y | Y |
| 61 | 12 | 13 | Y | Y |
| 61 | 13 | 14 | Y | Y |

### Multipad G

| p | e | t | supp(P_e) | #pairs | min degH | max degH |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 3 | 17 | 4 | 20 | 9 | 13 |
| 61 | 3 | 24 | 4 | 20 | 9 | 20 |
| 101 | 3 | 17 | 4 | 17 | 5 | 13 |
| 101 | 4 | 21 | 5 | 3 | 15 | 16 |
| 127 | 4 | 21 | 5 | 1 | 16 | 16 |
| 61 | 4 | 21 | 5 | 20 | 11 | 16 |

### Random multiples (sample)

| p | e | degH | min supp | med | max | 2e |
|---|---:|---:|---:|---:|---:|---:|
| 61 | 3 | 0 | 4 | 4 | 4 | 6 |
| 61 | 3 | 2 | 4 | 6 | 6 | 6 |
| 61 | 3 | 5 | 7 | 9 | 9 | 6 |
| 61 | 3 | 8 | 10 | 12 | 12 | 6 |
| 61 | 5 | 0 | 6 | 6 | 6 | 10 |
| 61 | 5 | 2 | 7 | 8 | 8 | 10 |
| 61 | 5 | 5 | 9 | 11 | 11 | 10 |
| 61 | 5 | 8 | 12 | 14 | 14 | 10 |
| 101 | 4 | 0 | 5 | 5 | 5 | 8 |
| 101 | 4 | 2 | 6 | 7 | 7 | 8 |
| 101 | 4 | 5 | 9 | 10 | 10 | 8 |
| 101 | 4 | 8 | 12 | 13 | 13 | 8 |
| 127 | 5 | 0 | 6 | 6 | 6 | 10 |
| 127 | 5 | 2 | 7 | 8 | 8 | 10 |
| 127 | 5 | 5 | 10 | 11 | 11 | 10 |
| 127 | 5 | 8 | 13 | 14 | 14 | 10 |

Random `P_e H` support grows with `degH`; multipads sit on the rare cancelled locus.

## Link

| item | status |
|---|---|
| G = P_e H structure | CLOSED (v70) |
| **P_e full support** | **CLOSED (v71)** |
| multipad needs degH≥1 | CLOSED (v71) |
| ban cancelled supp=2e at deployed | OPEN |
| SoftB fallback | OPEN |

## OPEN

Prove no `H` yields multipad-shaped `P_e H` on `{0..n'-1}` at deployed  
(or SoftB). Mathlib: Gaussian binomials / cyclotomic; AXLE for certs.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v71.py --check
```
