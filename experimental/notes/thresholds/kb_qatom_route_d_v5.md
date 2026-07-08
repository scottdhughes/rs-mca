# KB-MCA Route-D v5: residual \(N_{mathrm{can}}^{mathrm{prim}}\) via m-fiber routing

Status: `PARTIAL` — routing + criterion **PROVED**; `M_m` and `U_res` **OPEN**.

## Entropy signal (deployed)

```text
m = |C| = 913632
w = 67471
log2( avg_b |Fib_w^{(m)}(b)| )  ≈  -18820.25
log2( avg j-fiber )               ≈  35.74
```

The average m-subset depth-w fiber is about `2^(-18820)` — empty almost everywhere.
The natural finite claim is that the **max** is 0 or 1 (or tiny). Anticode is ~`2^1.69e6`
and does **not** help; this is a uniqueness-scale phenomenon.

## Theorem 1 — residual core routing (PROVED)

Let R(z) be any subset of Fib_w(z) (e.g. first-match residual). For S in R(z) let U be the e=w+1 smallest-exponent elements of S, C=S\\U, and let u be the first w monic coefficients of Lambda_U. Let b=b(z,u) be the triangular core prefix from v3. Then C lies in the m-subset fiber Fib_w^{(m)}(b). Consequently, writing U_res(z) for the number of distinct residual side-prefixes u and M_m(z) = max_u |Fib_w^{(m)}(b(z,u))|, one has N_can_prim(z) <= U_res(z) * M_m(z).

## Theorem 2 — side-prefix pencil (PROVED)

Fix w and e=w+1. The e-subsets U whose monic locators share a fixed length-w coefficient prefix u form a constant-shift family (varying only the constant term). Hence there are at most floor(n/e) such U.

Deployed side packing `floor(n/e) = 31`.

## Criterion 3 — residual atom from (M_m, U_res) (PROVED conditional)

If M_m^{max} := max_b |Fib_w^{(m)}(b)| <= 1 and max_z U_res(z) <= floor(target_floor/pack_ceil), then max_z N_can_prim(z) <= floor(target_floor/pack_ceil), hence max_z |R(z)| <= target_floor by residual lex covering (v4), which is the K_rem residual flatness form.

```text
If M_m^{max} <= 1 and U_res <= 16166878605395467:
    N_can_prim <= 16166878605395467
    |R| <= 17 * N_can_prim <= target_floor
    => K_rem residual flatness form

If M_m^{max} <= 1 and U_res <= 8456648496904:
    N_can_prim <= 8456648496904
    |D_prim| <= t*p
    => feeds v1 additive support certificate
```

## Path A

Same algebra for full fibers: `N_can <= U_full * M_m` (Theorem full-fiber routing).

## Toy suite

Residual proxy = aperiodic. `M_m_max_measured` only when `C(n,m)` small enough to enumerate.

| p | n | w | m | max R | max N_can_prim | max U_res | max cores/u | M_m max |
|---|---|---|---|---:|---:|---:|---:|---:|
| 17 | 16 | 2 | 5 | 49 | 49 | 34 | 7 | 17 |
| 17 | 16 | 3 | 4 | 5 | 5 | 5 | 2 | 4 |
| 97 | 32 | 2 | 2 | 33 | 32 | 32 | 1 | 1 |
| 97 | 32 | 3 | 1 | 7 | 7 | 7 | 1 | 1 |
| 193 | 64 | 2 | 1 | 32 | 25 | 25 | 1 | 1 |

Routing identity `N_can_prim <= U_res * max_cores_per_u` holds on all rows.

## Open program (B then A)

1. **B1:** Prove `M_m^{max}` tiny (entropy-backed uniqueness for m-subset depth-w prefixes).
2. **B2:** Bound residual side-prefix count `U_res`.
3. **A:** Repeat with full-fiber `U_full` once B is settled.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v5.py
python3 experimental/scripts/verify_kb_qatom_route_d_v5.py --check
```

## Non-claims

- Does not prove `M_m^{max} <= 1`.
- Does not prove a bound on `U_res`.
- Does not claim `U(1116048)<=B*`.
