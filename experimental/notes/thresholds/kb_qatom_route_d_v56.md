# KB-MCA Route-D v56: free-1 multipads on GP — regime split

Status: **algebraic dictionary PROVED**; **dense vs sparse regime** diagnosed;
deployed `|T|≤H2` still **OPEN** (local packet, not on `main`).

## Setup

```text
|H_unt| = |T|   (v54 star)
deployed: n'=1183520, e=67472, n'/p ≈ 5.555e-04, k=17
H2/p ≈ 36.2753
```

## Dictionary (PROVED)

### Power sums
For char `p > e`: free-1 monic high ⇔ equal power sums `p_1..p_{e−1}` (Newton).

### φ-fibres
For high coeffs `a`, on arc values `S`:

```text
φ_a(r) = −(r^e + a_{e−1} r^{e−1} + ⋯ + a_1 r)
```

Multipad highs = those `a` with **≥2 fibres of size e**.  
`T` = such `a` with an e-fibre containing the terminal value.

### Trivial vanish
`t < 2e` ⇒ `T = ∅`.

## Regime split (CAS)

| Regime | Example | Multipads |
|---|---|---|
| **Dense** `t ∼ p` | p=101, e=5, t=85 (k=17) | nH∼3.6e6, T∼4.4e5 (huge) |
| **Sparse** `t ≪ p` | p∼10^4, t/p∼0.003–0.005 | e≥4: **empty**; e=3 k=17: **rare** T∈{0,1,2,…} |

Dense failure of the random model: `C(t,e)/p^{e−1} = O(1)`.  
Deployed `n'/p ∼ 5.5e-4` is **sparse**; entropy (v55) predicts empty.

### Sparse sample (this suite)

| p | e | t | t/p | nH | T | C/p^{e−1} |
|---|---:|---:|---:|---:|---:|---:|
| 10007 | 3 | 51 | 0.0051 | 0 | 0 | 2.08e-04 |
| 10007 | 4 | 32 | 0.0032 | 0 | 0 | 3.59e-08 |
| 10007 | 4 | 40 | 0.0040 | 0 | 0 | 9.12e-08 |
| 10007 | 5 | 30 | 0.0030 | 0 | 0 | 1.42e-11 |
| 10009 | 3 | 51 | 0.0051 | 1 | 1 | 2.08e-04 |
| 10009 | 4 | 32 | 0.0032 | 0 | 0 | 3.59e-08 |
| 10009 | 4 | 40 | 0.0040 | 0 | 0 | 9.11e-08 |
| 10009 | 5 | 30 | 0.0030 | 0 | 0 | 1.42e-11 |
| 10037 | 3 | 51 | 0.0051 | 0 | 0 | 2.07e-04 |
| 10037 | 4 | 32 | 0.0032 | 0 | 0 | 3.56e-08 |
| 10037 | 4 | 40 | 0.0040 | 0 | 0 | 9.04e-08 |
| 10037 | 5 | 30 | 0.0030 | 0 | 0 | 1.40e-11 |

Census: sparse e≥4 all zero = True;  
sparse e=3 any T = True;  
dense e=3 example T=406 on p=31.

### Structure
Multipad pairs are **not** pure index-translates (0 on struct suite).  
Monic-high partitions = power-sum partitions on checked rows.

## What this does *not* prove

- Not `T=∅` at deployed e (e=3 still has rare sparse multipads on toys).
- Not `|T|≤H2` by `p^{e−1}` (for e≥3, `p^{e−1} ≫ H2`).
- Not residual card / `A_SP≤t·p`.

## OPEN

Prove in the **sparse** regime (or at deployed parameters) that
`T=∅` or `|T|≤H2`, using the φ-fibre / power-sum dictionary — especially
controlling e=3-type rare events at large e.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v56.py --check
```
