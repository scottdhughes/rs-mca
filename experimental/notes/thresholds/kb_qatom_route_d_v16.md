# KB-MCA Route-D v16: H_seam from A_SP + isolated residual marks

Status: `PARTIAL` — top-seam/SP identification + A_SP⇒H_seam **PROVED**;
unconditional H_seam and mark injectivity **OPEN**.

## 1. Top-seam pairs are depth-w shift pairs (PROVED)

If `S,S'` form a top-seam edge (same can-core, free-1 CS sides):

```text
Λ_S − Λ_{S'} = c Λ_C
deg(Λ_S − Λ_{S'}) = j − w − 1   (maximal depth-w shift stratum)
```

Deployed: `j−w−1 = 913632`.

Toy: all seam pairs satisfy the identity.

| j | w | #seam | #shift-ok |
|---|---|---:|---:|
| 9 | 2 | 47 | 47 |
| 7 | 2 | 299 | 299 |
| 6 | 2 | 465 | 465 |

## 2. Assignment rule A_SP (definition)

Assign every support incident to a top-seam edge in `G_z` to the SP/BC cell
(equivalently: delete multi-member core pencils from residual).

## 3. H_seam from A_SP (PROVED)

```text
A_SP residual  ⇒  matching-free  ⇒  |R| = N_can_prim  (pack=1)
```

## 4. Gap (PROVED as gap)

Existing SP theorems (structure + quotient sieve; **census OPEN**) do **not**
imply A_SP. Image-cell payments need not assign all supports. Unconditional
H_seam is **not** available from current SP package alone.

## 5. Isolated residual marks (definitions)

Under H_seam every residual leaf is isolated. Candidate marks:

```text
μ_E5(S)  = (min_exp(S), a_{w+1}(Λ_S))     ∈  [n] × F_p     (size n·p)
μ_E5U(S) = (min_exp(U), a_{w+1}(Λ_S))     ∈  [n] × F_p
μ_piv(S) = (i_*(S), λ_*(S))                 ∈  [t] × F_p     (size t·p)
```

`a_{w+1}` = first free monic coefficient below fixed prefix `z`.
`i_*` = first pivot row among ≤t ledger affine rows after rank-drop deletion.

**Injectivity OPEN.** If injective, residual mass closes (v14/v15).

## 6. Toy bank (A_SP + aperiodic proxy)

| j | w | max |R| | max μ_E5 fiber | max μ_E5U | max (minS,cU) |
|---|---|---:|---:|---:|---:|
| 9 | 2 | 42 | 5 | 5 | 10 |
| 7 | 2 | 42 | 4 | 4 | 7 |
| 10 | 3 | 4 | 2 | 2 | 2 |
| 6 | 2 | 31 | 3 | 3 | 5 |
| 5 | 2 | 17 | 3 | 3 | 2 |
| 9 | 3 | 5 | 2 | 2 | 2 |

Marks collide ⇒ not proofs of E2/E5.

## Bridge

```text
A_SP + injective mark  ⇒  |R| ≤ t·p or n·p  ⇒  residual mass atom
```

## OPEN

1. Prove **A_SP** (support-level SP/BC payment with cost), or equivalent.
2. Prove **injectivity** of a residual mark (μ_E5 / μ_piv / better).

## Non-claims

Not unconditional H_seam. Not mark injectivity. Not `U(1116048)≤B*`.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v16.py
python3 experimental/scripts/verify_kb_qatom_route_d_v16.py --check
```
