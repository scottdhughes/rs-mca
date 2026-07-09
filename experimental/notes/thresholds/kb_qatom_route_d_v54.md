# KB-MCA Route-D v54: pack-k + pure-untyped terminal star

Status: **star structure PROVED**; pack-k alone **refuted** as H2 strategy;
`|H_unt|=|T|` bounds PROVED but still ≫ H2 for e>2.

## Setup (v53)

```text
|H_unt| ≤ H_*^pre(n', e),   t = n' = 1183520,   k = ⌊n'/e⌋ = 17
```

## Pack-k census (not an H2 close)

| p | e | k | t | nH | p^{e−1} | nH/p^{e−1} |
|---|---:|---:|---:|---:|---:|---:|
| 31 | 2 | 2 | 4 | 0 | 31 | 0.0000 |
| 61 | 2 | 2 | 4 | 0 | 61 | 0.0000 |
| 101 | 2 | 2 | 4 | 0 | 101 | 0.0000 |
| 127 | 2 | 2 | 4 | 0 | 127 | 0.0000 |
| 31 | 2 | 5 | 10 | 13 | 31 | 0.4194 |
| 61 | 2 | 5 | 10 | 10 | 61 | 0.1639 |
| 101 | 2 | 5 | 10 | 3 | 101 | 0.0297 |
| 127 | 2 | 5 | 10 | 1 | 127 | 0.0079 |
| 61 | 2 | 17 | 34 | 61 | 61 | 1.0000 |
| 101 | 2 | 17 | 34 | 100 | 101 | 0.9901 |
| 127 | 2 | 17 | 34 | 119 | 127 | 0.9370 |
| 31 | 3 | 2 | 6 | 0 | 961 | 0.0000 |
| 61 | 3 | 2 | 6 | 0 | 3721 | 0.0000 |
| 101 | 3 | 2 | 6 | 0 | 10201 | 0.0000 |
| 127 | 3 | 2 | 6 | 0 | 16129 | 0.0000 |
| 31 | 3 | 5 | 15 | 49 | 961 | 0.0510 |
| 61 | 3 | 5 | 15 | 9 | 3721 | 0.0024 |
| 101 | 3 | 5 | 15 | 11 | 10201 | 0.0011 |

- **k=2:** nH=0 on all checked rows.
- **e=3, k=17:** nH can approach p² (max nH/p² ≈ 0.999).
- ⇒ no H2-bound depending only on k=17.

## Theorem — pure-untyped star (PROVED)

Every pure-untyped multipad high H has unique center `U_* ∈ F_H` with
`n'−1 ∈ U_*`, and every untyped pair is `(U_*, V)`.

Proof: v53 forces `max(U∪V)=n'−1` on untyped pairs; v25 disjointness ⇒ unique
holder of `n'−1` in `F_H`.

## Corollary — injection into T (PROVED)

```text
H ↦ U_*   injects   H_unt  ↪  T
|H_unt| = |T| ≤ binom(n'−1, e−1)
```

where `T = {U ⊆ I_{n'} : n'−1 ∈ U, U has a free-1 partner}`.

Marked U2e:

```text
|H_unt| ≤ binom(n'−1, 2e−1)   (= plain C(n',2e) · 2e/n' ≈ C(n',2e)/8.77)
```

Deployed: `n'−2e = 1048576 = 2^{20}`. Both binomials ≫ H2.

## Star toys

| p | e | t | nH_term | star_ok | star_fail | has_partner | rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| 61 | 4 | 32 | 444 | 444 | 0 | 444 | 0.099 |
| 101 | 4 | 32 | 116 | 116 | 0 | 116 | 0.026 |
| 31 | 4 | 30 | 1774 | 1774 | 0 | 1774 | 0.485 |
| 31 | 4 | 20 | 75 | 75 | 0 | 75 | 0.077 |
| 61 | 4 | 20 | 8 | 8 | 0 | 8 | 0.008 |
| 101 | 4 | 20 | 1 | 1 | 0 | 1 | 0.001 |
| 31 | 4 | 16 | 13 | 13 | 0 | 13 | 0.029 |
| 61 | 4 | 16 | 1 | 1 | 0 | 1 | 0.002 |
| 101 | 4 | 16 | 0 | 0 | 0 | 0 | 0.000 |
| 31 | 4 | 12 | 0 | 0 | 0 | 0 | 0.000 |
| 61 | 4 | 12 | 0 | 0 | 0 | 0 | 0.000 |
| 101 | 4 | 12 | 0 | 0 | 0 | 0 | 0.000 |
| 31 | 3 | 24 | 226 | 226 | 0 | 226 | 0.893 |
| 61 | 3 | 24 | 91 | 91 | 0 | 91 | 0.360 |

All `star_fail=0`; `nH_term = has_partner` when terminal multipads exist.

## Residual card path (updated)

```text
|H_unt| = |T|   (terminal free-1 partner count)
e=2: |T|≤p≤H2 ✓
e>2: need |T|≤H2 or |R2|≤e·p
```

## OPEN

1. **|T| ≤ H2** at deployed (n',e) — free-1 partners of terminal e-sets on GP
2. Alternate: residual pair budget |R2|≤e·p
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v54.py --check
```
