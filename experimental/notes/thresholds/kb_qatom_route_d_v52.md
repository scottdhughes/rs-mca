# KB-MCA Route-D v52: residual t-gate vs multipad windows

Status: **t≤2e+2 is a sufficient H2 gate (v51), NOT an ambient multipad law**.
REFUTED as universal multipad property; residual still OPEN.

## Hierarchy (PROVED)

```text
H_*^pre(t,e)  ≤  min( p^{e−1},  binom(t,2e),  ⌊binom(t,e)/2⌋ )
```

## Arithmetic H2 window (PROVED)

Deployed e=67472: only `s=t−2e ∈ {0,1,2}` has `binom(2e+s,s) ≤ H2=77291948627`.

| s | C(2e+s,s) | ≤H2? |
|---:|---:|---|
| 2 | 9105143985 | yes |
| 3 | 409570621781265 | no |

## REFUTED: ambient multipads have small pair-window

Define for multipad fiber `F_H`:

```text
t_min_pair(H)  =  min_{U≠V in F_H} (1 + max(U ∪ V))
```

**Claim (refuted):** t_min_pair(H) ≤ 2e+2 for every multipad high H.

| p | e | nH | gate | frac ≤gate | mean t_min | range | max fiber |
|---|---:|---:|---:|---:|---:|---|---:|
| 17 | 2 | 17 | 6 | 0.118 | 8.2 | 6–11 | 8 |
| 17 | 3 | 224 | 8 | 0.004 | 14.2 | 8–16 | 3 |
| 31 | 2 | 31 | 6 | 0.097 | 10.6 | 5–17 | 15 |
| 31 | 3 | 961 | 8 | 0.000 | 22.0 | 10–29 | 10 |
| 61 | 2 | 61 | 6 | 0.000 | 14.6 | 7–32 | 30 |
| 61 | 3 | 3721 | 8 | 0.000 | 34.0 | 13–54 | 20 |

e=3 rows: almost all multipads need t_min_pair ≫ 2e+2.

⇒ Residual cannot assume t≤2e+2 from multipad geometry alone.

## Random-core aside (heuristic only)

Uniform random m_c-subset of `{0..n−1}` has
`E[min(C)] = (n−m_c)/(m_c+1) ≈ 1.295`.
Coext multipads need t≥2e=134944, so they are atypical among all cores —
but residual **conditions** on multipad existence, so this does not force
small residual t.

## Residual card path (updated)

```text
U2e + t≤2e+2  ⇒  H*≤H2     (sufficient, rare for ambient multipads)
ambient ★_pre at t≤n'      (NOT H2-closed for e>2: p^{e−1} and C(n',2e) both ≫H2)
```

Need **residual-specific** bound on `|H_unt|` (C_unique, free_core, SR/H_M/Type).

## OPEN

1. C_unique theorem (v47 gap ★)
2. free_core / residual filters ⇒ `|H_unt|≤H2` without ambient small-t
3. A_SP ≤ t·p

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v52.py --check
```
