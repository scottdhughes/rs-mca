# KB-MCA Route-D v57: terminal high injectivity + collisions

Status: **injectivity / collision calculus PROVED**; deployed `|T|<=H2` still OPEN.
Local packet on `scott/kb-route-d-T-bound`.

## Setup

```text
|H_unt| = |T|,   deployed n'=1183520, e=67472, n'/p≈5.555e-04
```

## Theorems

### Same high + shared root ⇒ equal sets (PROVED)
`β = φ_a(r)` is unique ⇒ unique monic `f_β` ⇒ unique root set.

### Terminal high injectivity (PROVED)
All e-sets through the terminal index have **distinct** monic highs.
So `|T| <= C(t-1,e-1)` with room to spare only combinatorially — still ≫ H2 raw.

### Partners (PROVED)
- <=1 terminal partner per non-terminal e-set  
- <= `⌊t/e⌋-1` partners per terminal e-set  
- term/nonterm free-1 pairs inject into non-terminal e-sets  

### Collisions (PROVED)
```text
coll = # ordered pairs U≠V with same high
nH <= coll/2,   |T| <= nH <= coll/2
```

## CAS

| p | e | t | T | nH | coll | maxf | term_clash | coll/exp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 61 | 4 | 32 | 444 | 1763 | 3650 | 3 | 0 | 0.64 |
| 101 | 4 | 32 | 116 | 407 | 814 | 2 | 0 | 0.65 |
| 127 | 4 | 32 | 42 | 136 | 272 | 2 | 0 | 0.43 |
| 61 | 4 | 24 | 36 | 109 | 218 | 2 | 0 | 0.44 |
| 101 | 4 | 24 | 8 | 21 | 42 | 2 | 0 | 0.38 |
| 127 | 4 | 24 | 2 | 5 | 10 | 2 | 0 | 0.18 |
| 61 | 4 | 16 | 1 | 1 | 2 | 2 | 0 | 0.14 |
| 101 | 4 | 16 | 0 | 0 | 0 | 1 | 0 | 0.00 |
| 127 | 4 | 16 | 0 | 0 | 0 | 1 | 0 | 0.00 |
| 61 | 3 | 60 | 1711 | 3721 | 288200 | 20 | 0 | 0.92 |
| 61 | 3 | 36 | 511 | 2356 | 11198 | 7 | 0 | 0.82 |
| 101 | 3 | 36 | 271 | 1530 | 3888 | 4 | 0 | 0.78 |
| 127 | 3 | 36 | 170 | 930 | 2208 | 3 | 0 | 0.70 |
| 61 | 3 | 24 | 91 | 326 | 766 | 4 | 0 | 0.70 |

- All `term_clash=0`, `shared_root_bad=0`.  
- Sparse e>=4 empty (prior + this suite).  
- `coll/exp = O(1)` when multipads exist (near-random collision rate).

## Gap to H2

Terminal injectivity embeds T into `F_p^{e-1}` but image size may still be
up to `min(C(t-1,e-1), p^{e-1})`, and for e>=3 one has `p^{e-1} ≫ H2`.
Need a **collision bound** `coll = o(p^{e-1})` or GP-specific vanishing of
size-e double fibres of `φ_a` in the sparse regime.

## OPEN

Bound `coll` or `|T|` for GP arcs with `t << p` and large e so that `|T|<=H2`
at deployed parameters (character sums / complete-split translates of monic Q).

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v57.py --check
```
