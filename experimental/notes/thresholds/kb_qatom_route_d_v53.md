# KB-MCA Route-D v53: C_unique PROVED

Status: **C_unique PROVED**. Untyped core is the terminal block
`C_* = {n',…,n−1}`. Pure-untyped highs share this single core (`N_C=1`).

## Setup

Free-1 with `e = w+1` (route-D). A_SP: `U` = least `e` indices of `S`,
`C = S\U`. Domain indices `{0,…,n−1}`, `n' = n − m_c = A+e`.

## Lemma — free-1 fiber auto-match (PROVED)

If `U,V` free-1 (`e_i` match for `i=1..e−1`) and `max(U∪V) < min(C)`, then

```text
e_k(C⊔U) = e_k(C⊔V)   for all k = 1..w
```

because `w = e−1` and

```text
e_k(C⊔U) − e_k(C⊔V) = e_{k−e}(C) · (e_e(U) − e_e(V))
```

vanishes for `k < e`.

## Lemma — core count (PROVED)

For free-1 `(U,V)`, A_SP cores are the `m_c`-subsets of
`{max(U∪V)+1, …, n−1}`:

```text
#cores(U,V)  =  binom(n − 1 − max(U∪V), m_c)
```

## Theorem — untyped ⇔ terminal core (PROVED)

```text
untyped  ⇔  #cores = 1
         ⇔  n − 1 − max(U∪V) = m_c
         ⇔  max(U∪V) = n' − 1
         ⇔  unique core C_* = {n', n'+1, …, n−1}
```

## Theorem C_unique (PROVED)

Every untyped free-1 CS pair has core `C_*`. A pure-untyped high therefore has
unique core `C_*`.

## Corollary — N_C = 1 (PROVED)

```text
|H_unt|  =  |H_unt(C_*)|  ≤  H_*^pre(n', e)
```

Upgrades v47 (`N_C · H_*`) by killing the `N_C` factor.

Deployed: `n'=1183520`, `C_* = {1183520..2097151}`, `⌊n'/e⌋=17`.

## Toys

| p | j | w | n_unt | n_mp | n_pure_cores | C_unique |
|---|---:|---:|---:|---:|---:|---|
| 17 | 3 | 1 | 73 | 200 | 0 | True |
| 17 | 4 | 1 | 57 | 143 | 0 | True |
| 17 | 4 | 2 | 90 | 130 | 1 | True |
| 17 | 5 | 1 | 43 | 100 | 0 | True |
| 17 | 5 | 2 | 57 | 73 | 1 | True |
| 17 | 5 | 3 | 33 | 30 | 1 | True |
| 17 | 6 | 1 | 34 | 66 | 0 | True |
| 17 | 6 | 2 | 33 | 40 | 1 | True |
| 17 | 6 | 3 | 17 | 13 | 1 | True |
| 17 | 7 | 1 | 23 | 43 | 1 | True |
| 17 | 7 | 2 | 19 | 21 | 1 | True |
| 17 | 7 | 3 | 8 | 5 | 1 | True |

Census: rows=52; unt=6716; mp=29919;
all C_unique; all N_C≤1; core counts match binom.

## Residual card path (updated)

```text
C_unique + N_C=1
  ⇒  |H_unt| ≤ H_*^pre(n', e)
  ⇒  residual card if H_*^pre(n',e) ≤ H2
```

e=2: `H_*^pre ≤ p ≤ H2` (v48). e>2: OPEN.

## OPEN

1. `H_*^pre(n',e) ≤ H2` at deployed e=67472 (★_pre wall)
2. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v53.py --check
```
