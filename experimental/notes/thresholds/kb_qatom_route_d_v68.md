# KB-MCA Route-D v68: injectivity close path

Status: **injectivity ⇒ |T|=0 PROVED** as implication; deployed injectivity
**OPEN**. Local on `scott/kb-route-d-T-bound`.

## Preferred completion path

```text
free-1 high injective on e-subsets of I_{n'}
        =>  coll = 0
        =>  |T| = 0  <= H2     (v57)
```

This is stronger than soft-B (v64/v67): no Fourier bound needed if injectivity holds.

## S = e_e(u) (PROVED)

For power-sum / free-1 phase with `u_i = psi(Q(v_i))`:

```text
S = sum_{|U|=e} psi(sum_{x in U} Q(x)) = e_e(u_0,...,u_{t-1})
```

## Multipad criterion (PROVED)

`U ≠ V` share a free-1 high iff monic `f_U - f_V` is a nonzero constant.

## Deployed counting room (PROVED arithmetic)

| quantity | value |
|---|---:|
| log2 C | 373341.48 |
| log2 p^{e-1} | 2090837.54 |
| log2(p^{e-1}/C) | 1717496.06 |
| log2 E[coll] (random) | -1344154.6 |

No pigeonhole obstruction; random model predicts **empty coll**.

## CAS

| p | e | t | C | distinct | max m | coll | term_clash | inj? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 61 | 3 | 5 | 10 | 10 | 1 | 0 | 0 | Y |
| 61 | 3 | 6 | 20 | 20 | 1 | 0 | 0 | Y |
| 61 | 3 | 9 | 84 | 84 | 1 | 0 | 0 | Y |
| 61 | 3 | 12 | 220 | 220 | 1 | 0 | 0 | Y |
| 61 | 4 | 6 | 15 | 15 | 1 | 0 | 0 | Y |
| 61 | 4 | 8 | 70 | 70 | 1 | 0 | 0 | Y |
| 61 | 4 | 12 | 495 | 495 | 1 | 0 | 0 | Y |
| 61 | 4 | 16 | 1820 | 1819 | 2 | 2 | 0 | n |
| 61 | 5 | 7 | 21 | 21 | 1 | 0 | 0 | Y |
| 61 | 5 | 10 | 252 | 252 | 1 | 0 | 0 | Y |
| 61 | 5 | 15 | 3003 | 3003 | 1 | 0 | 0 | Y |
| 61 | 5 | 20 | 15504 | 15504 | 1 | 0 | 0 | Y |
| 101 | 3 | 5 | 10 | 10 | 1 | 0 | 0 | Y |
| 101 | 3 | 6 | 20 | 20 | 1 | 0 | 0 | Y |
| 101 | 3 | 9 | 84 | 83 | 2 | 2 | 0 | n |
| 101 | 3 | 12 | 220 | 216 | 2 | 8 | 0 | n |
| 101 | 4 | 6 | 15 | 15 | 1 | 0 | 0 | Y |
| 101 | 4 | 8 | 70 | 70 | 1 | 0 | 0 | Y |
| 101 | 4 | 12 | 495 | 495 | 1 | 0 | 0 | Y |
| 101 | 4 | 16 | 1820 | 1820 | 1 | 0 | 0 | Y |
| 101 | 5 | 7 | 21 | 21 | 1 | 0 | 0 | Y |
| 101 | 5 | 10 | 252 | 252 | 1 | 0 | 0 | Y |
| 101 | 5 | 15 | 3003 | 3003 | 1 | 0 | 0 | Y |
| 101 | 5 | 20 | 15504 | 15504 | 1 | 0 | 0 | Y |
| 127 | 3 | 5 | 10 | 10 | 1 | 0 | 0 | Y |
| 127 | 3 | 6 | 20 | 20 | 1 | 0 | 0 | Y |
| 127 | 3 | 9 | 84 | 84 | 1 | 0 | 0 | Y |
| 127 | 3 | 12 | 220 | 220 | 1 | 0 | 0 | Y |
| 127 | 4 | 6 | 15 | 15 | 1 | 0 | 0 | Y |
| 127 | 4 | 8 | 70 | 70 | 1 | 0 | 0 | Y |
| 127 | 4 | 12 | 495 | 495 | 1 | 0 | 0 | Y |
| 127 | 4 | 16 | 1820 | 1820 | 1 | 0 | 0 | Y |
| 127 | 5 | 7 | 21 | 21 | 1 | 0 | 0 | Y |
| 127 | 5 | 10 | 252 | 252 | 1 | 0 | 0 | Y |
| 127 | 5 | 15 | 3003 | 3003 | 1 | 0 | 0 | Y |
| 127 | 5 | 20 | 15504 | 15504 | 1 | 0 | 0 | Y |

- e_e identity rows: 10 (all OK)
- injective rows: 33 / 36
- all terminal clash = 0
- sparse e=4 at t~2e: injective on tested primes

## Link to closure board (v67)

| path | status |
|---|---|
| SoftB_Deployed => |T|<=H2 | CONDITIONAL (v64–v67) |
| **Injectivity => |T|=0** | **implication CLOSED (v68)** |
| Deployed injectivity / SoftB | **OPEN** |

B_\* ≈ 393171.6 remains a fallback sufficient bound.

## OPEN

1. Prove free-1 high **injectivity** on the deployed GP prefix of length n'.  
2. Or prove SoftB_Deployed.  
3. Either yields residual certificate `|T|≤H2`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v68.py --check
```
