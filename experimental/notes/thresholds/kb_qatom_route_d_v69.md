# KB-MCA Route-D v69: multipads disjoint; `t < 2e` injectivity

Status: **disjointness + threshold injectivity PROVED**; deployed GP multipad ban
**OPEN**. Local on `scott/kb-route-d-T-bound`.

## Multipads are disjoint (PROVED, ambient-independent)

```text
f_U - f_V = delta != 0  (same free-1 high)
r in U cap V  =>  f_U(r)=f_V(r)=0  =>  delta=0  contradiction
=>  U cap V = empty,  |U cup V| = 2e
f_U' = f_V'
```

## Threshold injectivity (PROVED)

```text
t < 2e  =>  no two disjoint e-subsets
        =>  no multipads
        =>  free-1 high injective
        =>  coll = 0  =>  |T| = 0     (v68)
```

## Deployed numbers

| symbol | value |
|---|---:|
| e | 67472 |
| 2e | 134944 |
| n' | 1183520 |
| n' >= 2e? | **yes** (threshold does not close) |
| floor(n'/e) | 17 |

## GP index form (PROVED)

```text
U = { omega^a : a in A }
p_k(U) = sum_{a in A} omega^{a k}
multipad <=> disjoint A,B size e with equal moments k=1..e-1
```

## CAS

| p | e | t | t&lt;2e? | inj? | #mp pairs | max m | coll |
|---|---:|---:|---|---|---:|---:|---:|
| 61 | 3 | 3 | Y | Y | 0 | 1 | 0 |
| 61 | 3 | 4 | Y | Y | 0 | 1 | 0 |
| 61 | 3 | 5 | Y | Y | 0 | 1 | 0 |
| 61 | 4 | 4 | Y | Y | 0 | 1 | 0 |
| 61 | 4 | 5 | Y | Y | 0 | 1 | 0 |
| 61 | 4 | 7 | Y | Y | 0 | 1 | 0 |
| 61 | 5 | 5 | Y | Y | 0 | 1 | 0 |
| 61 | 5 | 6 | Y | Y | 0 | 1 | 0 |
| 61 | 5 | 9 | Y | Y | 0 | 1 | 0 |
| 101 | 3 | 3 | Y | Y | 0 | 1 | 0 |
| 101 | 3 | 4 | Y | Y | 0 | 1 | 0 |
| 101 | 3 | 5 | Y | Y | 0 | 1 | 0 |
| 101 | 4 | 4 | Y | Y | 0 | 1 | 0 |
| 101 | 4 | 5 | Y | Y | 0 | 1 | 0 |
| 101 | 4 | 7 | Y | Y | 0 | 1 | 0 |
| 101 | 5 | 5 | Y | Y | 0 | 1 | 0 |
| 101 | 5 | 6 | Y | Y | 0 | 1 | 0 |
| 101 | 5 | 9 | Y | Y | 0 | 1 | 0 |
| 127 | 3 | 3 | Y | Y | 0 | 1 | 0 |
| 127 | 3 | 4 | Y | Y | 0 | 1 | 0 |
| 127 | 3 | 5 | Y | Y | 0 | 1 | 0 |
| 127 | 4 | 4 | Y | Y | 0 | 1 | 0 |
| 127 | 4 | 5 | Y | Y | 0 | 1 | 0 |
| 127 | 4 | 7 | Y | Y | 0 | 1 | 0 |
| 127 | 5 | 5 | Y | Y | 0 | 1 | 0 |
| 127 | 5 | 6 | Y | Y | 0 | 1 | 0 |
| 127 | 5 | 9 | Y | Y | 0 | 1 | 0 |
| 61 | 3 | 17 | n | n | 29 | 2 | 58 |
| 61 | 3 | 24 | n | n | 383 | 4 | 766 |
| 101 | 3 | 17 | n | n | 17 | 2 | 34 |
| 101 | 4 | 21 | n | n | 3 | 2 | 6 |
| 127 | 3 | 18 | n | n | 5 | 2 | 10 |
| 127 | 4 | 21 | n | n | 1 | 2 | 2 |
| 61 | 4 | 21 | n | n | 29 | 2 | 58 |

- all `t < 2e` rows injective
- all multipad pairs disjoint with cup size 2e
- level-set identity checked on sample multipads

## Link

| result | status |
|---|---|
| injectivity => \|T\|=0 | CLOSED (v68) |
| **t &lt; 2e => injectivity** | **CLOSED (v69)** |
| multipads disjoint | CLOSED (v69) |
| deployed injectivity | OPEN (n' &gt; 2e) |
| SoftB fallback | OPEN |

## OPEN

Forbid disjoint index multipads on `{0..n'-1}` with matching GP power sums
`k=1..e-1` at deployed parameters (or SoftB).

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v69.py --check
```
