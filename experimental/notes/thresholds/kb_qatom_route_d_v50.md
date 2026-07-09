# KB-MCA Route-D v50: ★_pre attack — bipartitions and C(t,2e)

Status: `PARTIAL` — **e=2 bipartition uniqueness + H2 close PROVED**;
**conditional** `H_*^pre ≤ binom(t,2e)` PROVED; full deployed window **OPEN**.

## Setup (v49)

`H_*^pre(t,e)` = free-1 multipad highs on index prefix `I_t` of KB domain.
Coext multipads use some `t = min(C) ∈ [2e, n']`.

## e=2 bipartition uniqueness (PROVED)

Four distinct field elements: at most one equal-sum pair-partition (char≠2).
⇒ e=2 free-1 multipad highs inject via pair-cover into 4-subsets, and
`H_*^pre(t,2) ≤ p ≤ H2`.

## Conditional bound for general e (PROVED)

**Hypothesis U2e:** every 2e-subset of `I_t` has at most one free-1 bipartition.

Then each multipad high H determines a unique 2e-set `W = U∪V` (any free-1 pair
in `F_H`), and

```text
H_*^pre(t,e)  ≤  binom(t, 2e)
```

Toys: U2e holds on all checked rows; pair-map injective; nH ≤ binom(t,2e).

## Arithmetic gate (PROVED)

Deployed e=67472:

| s | binom(2e+s, s) | ≤ H2? |
|---:|---:|---|
| 0 | 1 | yes |
| 1 | 134945 | yes |
| 2 | 9105143985 | yes |
| 3 | 409570621781265 | **no** |

Hence under U2e:

```text
t ≤ 2e+2  ⇒  H_*^pre(t,e) ≤ H2
```

## Residual card path (conditional)

```text
U2e + residual pure-untyped windows satisfy t ≤ 2e+2
  ⇒  |H_unt| ≤ H2
  ⇒  residual free-1 card (v45–v47)
```

OR prove U2e and a better large-t bound than binom(t,2e).

## CAS notes

- e/t ≈ 1/17 still has **large** nH for e=2,3 (ratio does not vanish multipads).
- Vanishing seen near e/t ≥ 1/3, not at 1/17.
- Deployed e/n′ ≈ 0.057 is the hard mid-ratio, large-e regime.

## Toys (sample)

| p | e | t | nH | C(t,2e) | map inj? | nH≤C? | multi bip W |
|---|---:|---:|---:|---:|---|---|---:|
| 17 | 4 | 16 | 89 | 12870 | True | True | 0 |
| 31 | 4 | 16 | 24 | 12870 | True | True | 0 |
| 61 | 4 | 16 | 1 | 12870 | True | True | 0 |
| 73 | 4 | 16 | 6 | 12870 | True | True | 0 |
| 101 | 4 | 16 | 0 | 12870 | True | True | 0 |
| 17 | 4 | 15 | 53 | 6435 | True | True | 0 |
| 31 | 4 | 15 | 11 | 6435 | True | True | 0 |
| 61 | 4 | 15 | 0 | 6435 | True | True | 0 |
| 73 | 4 | 15 | 3 | 6435 | True | True | 0 |
| 101 | 4 | 15 | 0 | 6435 | True | True | 0 |
| 17 | 4 | 14 | 30 | 3003 | True | True | 0 |
| 31 | 4 | 14 | 4 | 3003 | True | True | 0 |
| 61 | 4 | 14 | 0 | 3003 | True | True | 0 |
| 73 | 4 | 14 | 1 | 3003 | True | True | 0 |
| 101 | 4 | 14 | 0 | 3003 | True | True | 0 |
| 17 | 4 | 13 | 13 | 1287 | True | True | 0 |
| 31 | 4 | 13 | 1 | 1287 | True | True | 0 |
| 61 | 4 | 13 | 0 | 1287 | True | True | 0 |

Census: rows=105; all injective; all nH≤C(t,2e); bip unique on checked W.

## OPEN

1. **U2e for e>2** (geometric progression free-1 bipartitions)
2. **Residual t ≤ 2e+2** or replace C(t,2e) for t up to n′
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v50.py --check
```
