# KB-MCA Route-D v31: Type S common packing + high census

Status: `PARTIAL` — maximal-common Type S packing **M_pad≤16** deployed PROVED;
Type S always connected on toys; highs≤K_max still **OPEN**.

## Global common intersection (PROVED)

```text
|⋂_{C ∈ Cores} C|  ≤  free_core − 1
```

## Maximal-common packing (PROVED)

If the multipad achieves `|I| = free_core − 1`:

```text
reduced cores are free-1 CS of size m_c − |I|
M_pad  ≤  ⌊(n − 2e − |I|) / (m_c − |I|)⌋
```

### Deployed arithmetic

```text
|I| = free_core − 1 = 846160
m_c − |I| = e = 67472
n − 2e − |I| = A = 1116048
M_pad ≤ ⌊A/e⌋ = 16
```

Note: `16` is one below `pack_ceil = 17`
used in A_SP cost `|A_SP| ≤ 17·P_multi`.

## mpad=2 Type S (PROVED)

Single intersecting pair; `1 ≤ |C∩C'| ≤ free_core−1`.

## High counting (PROVED)

```text
|H_A_SP|  ≤  N_side  ≤  N_ord
|H_A_SP(z)|  ≤  N_ord(z)
```

Targets: `|H_A_SP| ≤ 2176` (M_pad1) or ≤ `1088` (M_pad2 half).

## Toys

| j | w | free_core | #S | max M_pad S | max |I| | #S with I≠∅ | #S maximal I | connected? | #highs | max H/fib | K1 | highs≤K1? |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|
| 4 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | None | 17 | 17 | 0 | False |
| 5 | 1 | 2 | 908 | 9 | 1 | 424 | 424 | True | 17 | 17 | 0 | False |
| 5 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | None | 110 | 5 | 0 | False |
| 6 | 1 | 3 | 904 | 14 | 2 | 452 | 308 | True | 17 | 17 | 0 | False |
| 6 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | None | 65 | 6 | 0 | False |
| 6 | 3 | -1 | 0 | 1 | 0 | 0 | 0 | None | 30 | 1 | 1 | False |
| 7 | 1 | 4 | 620 | 17 | 3 | 384 | 176 | True | 17 | 16 | 0 | False |
| 7 | 2 | 2 | 4 | 2 | 1 | 4 | 4 | True | 36 | 5 | 0 | False |
| 7 | 3 | 0 | 0 | 1 | 0 | 0 | 0 | None | 13 | 1 | 1 | False |
| 8 | 1 | 5 | 364 | 14 | 4 | 208 | 128 | True | 16 | 12 | 0 | False |
| 8 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | True | 19 | 3 | 0 | False |
| 8 | 3 | 1 | 0 | 1 | 0 | 0 | 0 | None | 5 | 1 | 1 | False |
| 9 | 2 | 4 | 0 | 1 | 0 | 0 | 0 | None | 8 | 2 | 0 | False |
| 9 | 3 | 2 | 0 | 1 | 0 | 0 | 0 | None | 1 | 1 | 1 | True |

Census: Type S=2802 all connected=2802;
with common=1474; maximal common=1042;
mpad2=1090.

## OPEN

1. Type S always intersection-connected (toys yes) + Helly/common often enough
   for M_pad≤16; or better union bound ⇒ M_pad≤2
2. `|H_A_SP| ≤ 2176` at deployed scale

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v31.py --check
```
