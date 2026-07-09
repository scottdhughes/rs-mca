# KB-MCA Route-D v32: Helly refuted; high matching ≤⌊n/e⌋

Status: `PARTIAL` — Type S **Helly REFUTED**; **high matching ≤⌊n/e⌋≤K_max**
PROVED; Type S connectedness universal on toys (proof OPEN).

## Helly REFUTED (BANKED NEGATIVE)

There exist Type S multipads that are intersection **cliques** with **empty**
global common intersection (non-star). Full Helly cannot give uniform M_pad≤16.

## Star / maximal-common retained (PROVED)

```text
I = ⋂ Cores ≠ ∅  →  peel (v30)
|I| = free_core−1  →  M_pad ≤ ⌊A/e⌋ = 16 deployed
```

## Connectedness (TOY UNIVERSAL / PROOF OPEN)

All toy Type S multipads have **one** intersection component. mpad=2 proved
connected. General theorem OPEN.

## High matching (PROVED)

```text
ν(H) := max # highs with pairwise-disjoint representative e-sets
ν(H) ≤ ⌊n/e⌋
```

Deployed:

```text
⌊n/e⌋ = 31  ≤  K_max = 2176
```

A first-match **matching transversal** of highs fits the (κ,ι,δ) budget.
Gap: `|H_A_SP|` may exceed `ν(H)` — need thinning to a matching.

## Toys

| j | w | free_core | #S | #star | #nonstar | #clique non-Helly | max M_pad S | max nonstar | connected? | #highs | ν(H) | ⌊n/e⌋ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 4 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | None | 17 | 6 | 8 |
| 5 | 1 | 2 | 908 | 424 | 484 | 96 | 9 | 9 | True | 17 | 6 | 8 |
| 5 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | None | 110 | 4 | 5 |
| 6 | 1 | 3 | 904 | 452 | 452 | 296 | 14 | 14 | True | 17 | 5 | 8 |
| 6 | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | None | 65 | 4 | 5 |
| 6 | 3 | -1 | 0 | 0 | 0 | 0 | 1 | 1 | None | 30 | 3 | 4 |
| 7 | 1 | 4 | 620 | 384 | 236 | 232 | 17 | 17 | True | 17 | 5 | 8 |
| 7 | 2 | 2 | 4 | 4 | 0 | 0 | 2 | 1 | True | 36 | 3 | 5 |
| 7 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | None | 13 | 2 | 4 |
| 8 | 1 | 5 | 364 | 208 | 156 | 156 | 14 | 14 | True | 16 | 5 | 8 |
| 8 | 2 | 3 | 2 | 2 | 0 | 0 | 2 | 1 | True | 19 | 3 | 5 |
| 8 | 3 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | None | 5 | 2 | 4 |
| 9 | 2 | 4 | 0 | 0 | 0 | 0 | 1 | 1 | None | 8 | 2 | 5 |
| 9 | 3 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | None | 1 | 1 | 4 |

Census: Type S=2802 connected=2802;
star=1474; nonstar=1328;
clique non-Helly=780 (Helly dead);
max ν=6.

## OPEN

1. Prove Type S intersection-connectedness; bound non-Helly Type S M_pad
2. First-match thin `H_A_SP` to a matching of size ≤`31` 
   (≤`2176`)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v32.py --check
```
