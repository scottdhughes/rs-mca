# KB-MCA Route-D v59: Plancherel bound on arc sums `G`

Status: **`max|G| <= sqrt(p t - t^2)` PROVED**; e=2 `S` bound from `G` PROVED;
that bound **does not** yield √-cancellation for `S` when `t << p`. Local packet.

## Arc sum G (PROVED)

For any `t`-set `S_arc ⊂ F_p` (GP arc included):

```text
G(a) = sum_{x in S_arc} psi(a x)
sum_{a != 0} |G(a)|^2 = p t - t^2
max_{a != 0} |G(a)|  <=  sqrt(p t - t^2)  <= sqrt(p t)
```

### CAS

| p | t | max|G| | bound | Plancherel err |
|---|---:|---:|---:|---:|
| 61 | 20 | 5.90 | 28.64 | 0.0e+00 |
| 61 | 40 | 6.10 | 28.98 | 2.3e-13 |
| 61 | 50 | 6.75 | 23.45 | 0.0e+00 |
| 101 | 20 | 7.27 | 40.25 | 2.3e-13 |
| 101 | 40 | 7.43 | 49.40 | 4.5e-13 |
| 101 | 50 | 9.58 | 50.50 | 4.5e-13 |
| 127 | 20 | 8.09 | 46.26 | 4.5e-13 |
| 127 | 40 | 9.99 | 58.99 | 9.1e-13 |
| 127 | 50 | 8.85 | 62.05 | 9.1e-13 |
| 127 | 100 | 8.48 | 51.96 | 9.1e-13 |

## e=2: S from G (PROVED)

```text
S(lam) = (1/2)(G(lam)^2 - G(2 lam))
|S| <= (1/2)(M^2 + M),  M = sqrt(p t - t^2)
```

| p | t | max|S| | B_S thm | √C | S/√C | thm⇒√-cancel? |
|---|---:|---:|---:|---:|---:|---|
| 61 | 20 | 17.7 | 4.2e+02 | 13.8 | 1.28 | False |
| 61 | 34 | 20.2 | 4.7e+02 | 23.7 | 0.85 | False |
| 61 | 50 | 24.7 | 2.9e+02 | 35.0 | 0.71 | False |
| 101 | 20 | 26.3 | 8.3e+02 | 13.8 | 1.91 | False |
| 101 | 34 | 38.7 | 1.2e+03 | 23.7 | 1.64 | False |
| 101 | 50 | 46.2 | 1.3e+03 | 35.0 | 1.32 | False |
| 10007 | 20 | 87.8 | 1.0e+05 | 13.8 | 6.37 | False |
| 10007 | 34 | 195.2 | 1.7e+05 | 23.7 | 8.24 | False |
| 10007 | 50 | 196.8 | 2.5e+05 | 35.0 | 5.62 | False |

Sparse large `p`: thm **fails** to imply √-cancel (`B_S thm >> √C`), while
empirical `S/√C` stays moderate. Need a sharper `S` estimate than composing
the `G` bound.

### Full multiplicative group (PROVED)

`S_arc = F_p^x` ⇒ `G(a)=-1` (`a!=0`) ⇒ e=2 `|S|=1`.

## e=3 empirical

| p | t | max|S| | √C | S/√C |
|---|---:|---:|---:|---:|
| 61 | 18 | 71.1 | 28.6 | 2.49 |
| 61 | 30 | 144.0 | 63.7 | 2.26 |
| 61 | 51 | 245.0 | 144.3 | 1.70 |
| 101 | 18 | 83.9 | 28.6 | 2.94 |
| 101 | 30 | 181.7 | 63.7 | 2.85 |
| 101 | 51 | 311.9 | 144.3 | 2.16 |

## Link to residual card (v58)

```text
sqrt-cancel |S|<=√C  ⇒  coll <= C^2/p^{e-1}  ⇒  T=0 at deployed
```

v59 gives tools for e=2 `G`/`S` but **not** yet √-cancel for general free-1 highs.

Deployed e=2 card path remains `|T|<=p<=H2` (v48/v54), not this coll bound.

## OPEN

1. Prove `|S(lambda)| <= √C` for free-1 highs on GP arcs (e≥3 primary).  
2. Sharpen e=2 `S` beyond `O(p t)` composition (optional).  
3. Multilinear / hybrid sum expression for e≥3 analogous to e=2 `G`-formula.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v59.py --check
```
