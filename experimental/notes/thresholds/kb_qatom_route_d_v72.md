# KB-MCA Route-D v72: multipad `H` gap law

Status: **H-support gap law PROVED** (board-ready structure); deployed multipad
ban still **OPEN**. Local on `scott/kb-route-d-T-bound`.

## BOARD CLOSED (this packet)

```text
If G = P_e * H is a free-1 multipad index polynomial
(supp G = 2e, P_e full support),
then every consecutive gap in supp(H) is <= e.
```

### Proof sketch

1. If `deg G < n` and `P_e|G`, `G≠0`, then `supp(G) ≥ e+1` (Vandermonde;  
   `X^n−1` has support 2 but degree `n`, so excluded).  
2. If some consecutive gap of `supp(H)` is `≥ e+1`, split `H = H_L + H_R`.  
3. Product supports of `P_e H_L` and `P_e H_R` are **disjoint**.  
4. Each side has `deg < n` and is a nonzero multiple of `P_e` ⇒ support `≥ e+1`.  
5. Hence `supp(G) ≥ 2e+2 > 2e`, contradiction.

### Corollary

Support of `H` is an **e-chain**: diameter `<= e(s-1)` for `s = #supp(H)`.

## Separated monomials (PROVED)

If terms of `H` are spaced `>= e+1` apart:

```text
supp(P_e H) = s (e+1)   (no cancellation)
```

Cannot equal multipad `2e` for integer `s` when `e >= 2`.

## CAS

### Separated products

| p | e | s | supp(PH) | s(e+1) |
|---|---:|---:|---:|---:|
| 61 | 3 | 1 | 4 | 4 |
| 61 | 3 | 2 | 8 | 8 |
| 61 | 3 | 3 | 12 | 12 |
| 61 | 4 | 1 | 5 | 5 |
| 61 | 4 | 2 | 10 | 10 |
| 61 | 4 | 3 | 15 | 15 |
| 101 | 4 | 1 | 5 | 5 |
| 101 | 4 | 2 | 10 | 10 |
| 101 | 4 | 3 | 15 | 15 |
| 127 | 5 | 1 | 6 | 6 |
| 127 | 5 | 2 | 12 | 12 |
| 127 | 5 | 3 | 18 | 18 |

### Multipad H max consecutive gap

| p | e | t | #pairs | min maxgap | max maxgap | all <=e? |
|---|---:|---:|---:|---:|---:|---|
| 61 | 3 | 17 | 29 | 1 | 2 | Y |
| 61 | 3 | 24 | 40 | 1 | 2 | Y |
| 101 | 3 | 17 | 17 | 1 | 1 | Y |
| 101 | 4 | 21 | 3 | 1 | 1 | Y |
| 127 | 4 | 21 | 1 | 1 | 1 | Y |
| 61 | 4 | 30 | 40 | 1 | 3 | Y |

## Deployed

| | |
|---|---:|
| e | 67472 |
| gap cap for multipad H | 67472 |
| n' | 1183520 |

## OPEN (next board hit)

Use the gap law + `G` in `{-1,0,1}` with `e` pluses/minuses to **forbid**
such `H` on `{0..n'-1}` — that would be a **deployed residual board close**.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v72.py --check
```
