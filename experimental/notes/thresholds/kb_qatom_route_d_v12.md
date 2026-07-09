# KB-MCA Route-D v12: trade-weight law

Status: `PARTIAL` — trade geometry **PROVED**; unconditional atom **NO**.

## Trade-weight law (PROVED, unconditional)

For multi-mates `C ≠ C'` in one `Phi_w` fiber:

```text
|C ∩ C'|  ≤  m − w − 1
|C △ C'|  =  2(m − |∩|)  ≥  2(w + 1)
```

Equality `|△| = 2(w+1)` ⇔ **tight** ⇔ free-1 CS pad of `(w+1)`-blocks.

Deployed minimum trade weight: `134944`.
v8 coset-pad trade weight: `262144` (long).

## Free regimes (PROVED)

| free | Multi-mates | Packing |
|---:|---|---|
| 0 | none | M_m ≤ 1 |
| 1 | min-weight only, pairwise disjoint CS | M_m ≤ floor(n/m) |
| ≥ 2 | long trades possible | no free packing |

Deployed free = `846161` ≫ 1. log2 avg m-fiber ≈ `-18820.25`.

## Min-weight residual criterion (PROVED conditional)

```text
residual multi-mates all min-weight
AND each residual multi-mate fiber is a pairwise-tight clique
    =>  M_m^{res,phi} ≤ k_tight = 18
    =>  U_res ≤ target/(17*18) ≈ 2^{49.67} closes atom
```

### Warning (PROVED by toy)

Tight-**graph** components can exceed `k_tight` when not cliques.
Need pairwise-tight, not mere connectivity.

## Toy free-regime table (p=17, n=16)

| m | w | free | Mm | k_tight | #min pairs | #long | max t-comp | tcomp>kt | only min |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 3 | 108 | 7 | 24024 | 72490 | 108 | True | False |
| 4 | 2 | 2 | 8 | 5 | 3520 | 1494 | 8 | True | False |
| 4 | 3 | 1 | 4 | 4 | 126 | 0 | 4 | False | True |
| 5 | 2 | 3 | 17 | 4 | 15840 | 15312 | 17 | True | False |
| 5 | 3 | 2 | 3 | 3 | 1008 | 112 | 3 | False | False |
| 5 | 4 | 1 | 1 | 3 | 0 | 0 | 1 | False | True |
| 6 | 2 | 4 | 32 | 4 | 42240 | 65112 | 32 | True | False |
| 6 | 3 | 3 | 5 | 3 | 3528 | 952 | 5 | True | False |
| 6 | 4 | 2 | 2 | 3 | 0 | 40 | 1 | False | False |
| 6 | 5 | 1 | 1 | 2 | 0 | 0 | 1 | False | True |
| 10 | 4 | 6 | 2 | 2 | 0 | 40 | 1 | False | False |
| 10 | 8 | 2 | 1 | 1 | 0 | 0 | 1 | False | True |
| 10 | 9 | 1 | 1 | 1 | 0 | 0 | 1 | False | True |

## Unconditional atom?

**No.** Structure is unconditional; atom still needs residual hypotheses
(min-weight + clique) or `K_res=1` or `U_phi` bound.

## Next real math

1. Residual forbids long trades (`|△| ≥ 2(w+2)` paid / impossible), **and**
2. Residual min-weight fibers are pairwise-tight cliques (size ≤ 18 or 1), **or**
3. Direct `U_phi` / `U_res` bound, **or**
4. `M_m^{res} ≤ 1` by other residual geometry.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v12.py
python3 experimental/scripts/verify_kb_qatom_route_d_v12.py --check
```
