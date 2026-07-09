# KB-MCA Route-D v28: ledger/fiber-native κ + multipad locus

Status: `PARTIAL` — Newton-native high witness + multipad locus + t-packing
**PROVED**; residual `t=1` and κ→`[K_max]` still **OPEN**.

## Ledger-native high witness (PROVED)

On each free-1 family `F_H`:

```text
high[0]  =  −p_1(U)   for every U ∈ F_H
```

(Newton / monic convention). So `κ_raw = high[0]` is the **first Newton
coordinate** of the free-1 high — the natural ledger invariant, not a mod-hash.

- **e=2:** high is 1-dimensional; `high[0] ↔ p_1` bijective among highs.
- **Budget:** `(high[0], ι, δ)` has size `p·⌊n/e⌋·p` ≫ `e·p`; need compress
  `high[0]` into `[2176]` or ≤`2176` residual highs.

## Multipad locus (PROVED)

```text
multipads  ⇒  free-1 CS pairs  ⇒  only on multi-pencil / A_SP-type fibers
R_sing / no CS pair  ⇒  N_ord = 0, M_pad = 1 vacuous
```

## Point-multiplicity packing (PROVED)

```text
M_pad  ≤  ⌊ t (n−2e) / m_c ⌋
t = max_r  (number of multipad cores containing r)
```

| t | bound |
|---:|---|
| 1 | `⌊(n−2e)/m_c⌋` = **2 deployed** |
| free_core=1 | t=1 forced (v27) |
| free_core≥2 | t≥2 possible (toys) |

**Deployed win condition:** residual A_SP multipads have **t=1** ⇒ `M_pad≤2`.

## Fiber exclusive cover (defined)

`r` exclusive to `Cover(H)` in a fiber is a fiber-native high witness; existence
and global uniqueness not guaranteed (toys).

## κ census

| mark | tested | inj rows | coll rows |
|---|---:|---:|---:|
| `high0_iota_delta` | 12 | 8 | 4 |
| `high0_mod_K_iota_delta` | 12 | 2 | 10 |
| `min_family_iota_delta` | 12 | 2 | 10 |
| `min_family_mod_K_iota_delta` | 12 | 2 | 10 |
| `min_fiber_cover_iota_delta` | 12 | 2 | 10 |
| `min_fiber_cover_mod_K_iota_delta` | 12 | 2 | 10 |
| `min_excl_iota_delta` | 12 | 2 | 10 |
| `full_high_iota_delta` | 12 | 12 | 0 |

## Toys

| j | w | free_core | max M_pad | max t | pack if t=1 | #no-pair fib | #pair fib | high0 inj? | high0 mod K? | min family inj? |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 4 | 1 | 1 | 4 | 1 | 6 | 0 | 17 | True | False | False |
| 5 | 1 | 2 | 9 | 4 | 4 | 0 | 17 | True | False | False |
| 5 | 2 | 0 | 1 | 0 | 5 | 28 | 261 | False | False | False |
| 6 | 1 | 3 | 14 | 7 | 3 | 0 | 17 | True | False | False |
| 6 | 2 | 1 | 2 | 1 | 3 | 54 | 235 | False | False | False |
| 6 | 3 | -1 | 1 | 0 | 4 | 4405 | 75 | False | False | False |
| 7 | 2 | 2 | 2 | 2 | 2 | 105 | 184 | False | False | False |
| 7 | 3 | 0 | 1 | 0 | 2 | 4782 | 34 | True | False | False |
| 8 | 2 | 3 | 2 | 2 | 2 | 181 | 108 | True | False | False |
| 8 | 3 | 1 | 1 | 0 | 2 | 4872 | 9 | True | False | False |
| 9 | 2 | 4 | 1 | 0 | 1 | 245 | 44 | True | True | True |
| 9 | 3 | 2 | 1 | 0 | 1 | 4815 | 1 | True | True | True |

Newton checks: 8263/8263. e=2 bijective:
3 rows. R_sing fibers: 19487.

## OPEN

1. Compress Newton/first-match high witness into `[2176]` on residual, or
   prove ≤`2176` residual highs
2. Residual A_SP multipad **t=1** at free_core=`846161` ⇒ M_pad≤`2`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v28.py --check
```
