# L1 PMA Auxiliary-List And Johnson Regime

## Status

PROVED-COMPILER.  The reduction cites Lemma 2 (`Sunflower Core-Defect
Reduction`) in `experimental/notes/l1/l1_full_list_quotient_proof_program.md`.
The coarse Johnson payment cites Theorem J there; the sharper payment used by
the current frontier scanner and add-back ledger is
`thm:capf-johnson-list` / `cor:capf-pma-johnson` in
`experimental/cap25_cap_v13_raw.tex`.

This note packages two roadmap nodes:

- `pma_aux_list_reduction`;
- `pma_johnson_regime`.

It does not prove mixed-petal sunflower amplification.  It isolates the
few-petal part that is already covered by ordinary Reed--Solomon list-decoding
packing.

## Auxiliary Reduction

Use the sunflower notation of Lemma 2.  Fix:

```text
D subset C,        |D| = d,
R_0 subset R,      |R_0| = r.
```

Let `L_D` be the missed-core locator and define the auxiliary petal word on
the union of petals `T = T_1 union ... union T_M` by

```text
U_D(x) = c_i L_D(x)        for x in T_i.
```

For any non-planted listed codeword in this fixed `D,R_0` layer, Lemma 2 gives
a unique polynomial `W_P` with

```text
deg W_P <= d,
W_P(x)=0                  for x in R_0,
W_P(x)=c_i L_D(x)         for x in S_i subset T_i.
```

The list condition gives

```text
sum_i |S_i| >= sigma + d + 1 - r.
```

Therefore the map

```text
P -> W_P
```

injects the fixed `D,R_0` mixed-petal layer into the auxiliary degree-`<=d`
Reed--Solomon list on the petal domain `T`, at agreement

```text
a = sigma + d + 1 - r.
```

Dropping the extra constraints `W_P=0` on `R_0` and exact nonagreement on `D`
only enlarges this auxiliary list, so it is safe for upper bounds.

### Layer scope is not profile scope

For fixed exact `(D,R_0)`, the injection is defined on the union of all
petal-support and occupancy profiles in that layer.  Consequently a Johnson
bound for the auxiliary list is charged once to that union.  It must not be
multiplied by the number of support patterns or attached independently to
several disjoint `t,(a_i)` cells and then added.

The frozen `GF(19)` coordinates `d=4,r=1` provide the first load-bearing
ledger use of this distinction.  Fifteen profile cells share one missed-core
choice and two retained-background layers, each bounded by `36`; their common
conservative envelope is therefore `72` once.  The exact regrouping and
mutation tests are in
`experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py`.

The next frozen layer, `d=4,r=0`, has the same full-core miss and the unique
empty retained-background set.  Exactness excludes both background
agreements, so all eleven occupancy cells lie in one concrete auxiliary layer
with `a=8`.  The sharp bound is `3`, charged once across the whole layer.  The
content-addressed replay and its no-cross-`r` guard are in
`experimental/scripts/verify_l1_b9_d4r0_shared_auxiliary_ledger.py`.

## Johnson Regime

The auxiliary petal domain has size

```text
|T| = M(sigma+1).
```

The auxiliary code has effective dimension `d+1`.  By Theorem J, if

```text
a^2 > |T| d,
```

then the fixed `D,R_0` auxiliary list has size at most

```text
|T|(|T|-d) / (a^2-|T|d).
```

Equivalently, for `d>0`, the few-petal Johnson-covered region is

```text
M <= floor((a^2-1)/(d(sigma+1))).
```

Theorem J gives the valid coarse bound

```text
|T|(|T|-d) / (a^2-|T|d).
```

The later proved `kappa`-intersecting agreement bound
`thm:capf-johnson-list` sharpens the numerator, giving

```text
|T|(a-d) / (a^2-|T|d).
```

The strict Johnson region is the same for both bounds.  The scanner and the
`m=2` full-rank ledger use the sharper bound and take its integer floor.

Thus the mixed-petal amplification problem only starts after this
sub-Johnson boundary.  Below the boundary, the ordinary list-decoding packing
theorem handles the fixed `D,R_0` layer before any sunflower-specific
amplification argument is needed.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py \
  --check experimental/data/certificates/l1-pma-auxiliary-johnson/l1_pma_auxiliary_johnson.json
```

The legacy verifier records exact parameter translations, the coarse Theorem
J bound, the few-petal threshold table, and a small finite-field toy replay.
The sharp numerator and fixed-layer add-back are independently replayed by
`experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py`.
