# KB-MCA Route-D v30: Type S free_core peel + high budget

Status: `PARTIAL` — Type S **free_core peel** and free_core=2 **through-pack**
PROVED; global Type S M_pad≤2 and highs≤K_max still **OPEN**.

## Type S root reduction (PROVED)

If multipad cores share `r`:

```text
Λ_C = (X−r) M,   Λ_{C'} = (X−r) M'
Phi_w(M)=Phi_w(M'),   deg(M−M') ≤ free_core−2
free_core' = free_core−1   (size m_c−1, same depth w)
```

## free_core=2 through-pack (PROVED)

```text
|Cores_r|  ≤  ⌊(n−2e−1)/(m_c−1)⌋
```

(reduced free-1 CS / Type D). Deployed value if free_core were 2:
`2` (actual free_core=`846161` ≠ 2).

## Peel process (PROVED)

```text
Type S  --peel max-mult root-->  free_core−1 family  -->  …  -->  Type D
```

≤ `free_core−1` peels. Final Type D packs on the residual ground set.
Shared-root first-match cell = charge Type S along peel-root witnesses.

## High budget (PROVED criteria)

```text
(κ,ι,δ) size = K · ⌊n/e⌋ · p
M_pad≤1:  K ≤ ⌊e/⌊n/e⌋⌋ = 2176
M_pad≤2:  K ≤ ⌊e/(2⌊n/e⌋)⌋ = 1088  (if N_ord≤2 N_side via same mark)
```

## Toys

| j | w | free_core | #D | #S | max M_pad S | max peels | max through | #highs | max H/fib | K1 | peel ok? | fc2 pack? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 4 | 1 | 1 | 540 | 0 | 1 | 0 | 0 | 17 | 17 | 0 | None | None |
| 5 | 1 | 2 | 64 | 908 | 9 | 1 | 4 | 17 | 17 | 0 | True | True |
| 5 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 110 | 5 | 0 | None | None |
| 6 | 1 | 3 | 0 | 904 | 14 | 2 | 0 | 17 | 17 | 0 | True | None |
| 6 | 2 | 1 | 2 | 0 | 1 | 0 | 0 | 65 | 6 | 0 | None | None |
| 6 | 3 | -1 | 0 | 0 | 1 | 0 | 0 | 30 | 1 | 1 | None | None |
| 7 | 1 | 4 | 0 | 620 | 17 | 3 | 0 | 17 | 16 | 0 | True | None |
| 7 | 2 | 2 | 0 | 4 | 2 | 1 | 2 | 36 | 5 | 0 | True | True |
| 7 | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 13 | 1 | 1 | None | None |
| 8 | 1 | 5 | 0 | 364 | 14 | 4 | 0 | 16 | 12 | 0 | True | None |
| 8 | 2 | 3 | 0 | 2 | 2 | 2 | 0 | 19 | 3 | 0 | True | None |
| 8 | 3 | 1 | 0 | 0 | 1 | 0 | 0 | 5 | 1 | 1 | None | None |
| 9 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | 8 | 2 | 0 | None | None |
| 9 | 3 | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | None | None |

Census: Type S peels OK=2802/2802; max peels
seen=4; fc2 through-pack checks=2548.

## OPEN

1. Global Type S `M_pad≤2` at free_core=`846161` (peel structure alone
   does not bound the union of through-sets tightly enough)
2. `|A_SP highs| ≤ 2176` (or constructive κ)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v30.py --check
```
