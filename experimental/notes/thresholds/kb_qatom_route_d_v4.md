# KB-MCA Route-D v4: residual-first N_{\mathrm{can}}^{\mathrm{prim}} (B → A)

Status: `PARTIAL` — residual lex-covering **PROVED**; N_{\mathrm{can}}^{\mathrm{prim}} bound **OPEN**.

Priority: **B then A** as requested.

## Path B - residual first

### Residual fiber (ledger)

From `kb_mca_1116048_first_match_ledger_v1.md`, after first-match assignment:

```text
R(z) = { S : |S|=j, Phi_w(S)=z, not assigned to
         generated-field / terminal quotient-planted / tangent /
         extension / sparse-Pade / M1-half-turn / contained-rank-drop }
```

Proved paid so far: generated image cells `<= t*p` and terminal quotient
`c in {65536,131072}` raw-paid. Other branches still open as payments but
are **removed from R(z) by definition** when assigned.

### Theorem B1 — residual lex-split covering (PROVED)

Let R(z) subset Fib_w(z) be any subset of the depth-w fiber (in particular the first-match residual). Define C_can, c_U on R(z) exactly as in v3 lex-split. Then phi: S |-> (C_can(S), c_U(S)) is injective on R(z), and |R(z)| <= pack_ceil * N_can_prim(z) and |R(z)| <= p * N_can_prim(z), where N_can_prim(z) = |{C_can(S) : S in R(z)}|.

### Residual core budgets (PROVED arithmetic)

```text
pack_ceil = 17
B_paid_proved = 143763495894416
K_rem = 4805007
target_floor ≈ K_rem * avg = 274836936291722953

N_can_prim  ≤  floor(target_floor / 17)  =  16166878605395467
              ≈  2^{53.84}
              ⇒  |R(z)| ≤ target_floor   (K_rem residual flatness form)

N_can_prim  ≤  floor(t*p / 17)  =  8456648496904
              ≈  2^{42.94}
              ⇒  |D_prim| ≤ t*p          (feeds v1 additive certificate)
```

### Open (B)

Prove max_z N_can_prim(z) <= 16166878605395467 (K_rem residual flatness) or <= 8456648496904 (sufficient for |D_prim| <= t*p).

## Path A — full-fiber N_{\mathrm{can}}

### Theorem A1 — m-subset routing (PROVED)

For S in Fib_w(z) with lex-split (C,U), the first w monic coefficients b of Lambda_C are the triangular function b=b(z,u) of the first w monic coefficients u of Lambda_U (v3). Consequently every canonical core C(S) lies in the m-subset depth-w fiber Fib_w^{(m)}(b(z,u(S))).

### Open (A)

Prove max_z N_can(z) <= 16166878605395467 for full fibers (harder; shallow counterexamples to crude n*p remain).

## Toy suite (B proxy + A measurements)

Residual **proxy** on toys: aperiodic supports (cyclic period n; not pure
c-quotient for any c>1). Stronger than terminal-only exclusion; good
for stress-testing covering on a residual-like set.

| p | n | j | w | max full | max R proxy | max N_can | max N_can_prim | R fraction |
|---|---|---|---|---:|---:|---:|---:|---:|
| 17 | 16 | 8 | 2 | 54 | 49 | 54 | 49 | 0.9946 |
| 17 | 16 | 8 | 3 | 7 | 5 | 7 | 5 | 0.9946 |
| 97 | 32 | 5 | 2 | 33 | 33 | 32 | 32 | 1.0000 |
| 97 | 32 | 5 | 3 | 7 | 7 | 7 | 7 | 1.0000 |
| 193 | 64 | 4 | 2 | 32 | 32 | 25 | 25 | 0.9992 |

All rows: lex-injection and pack/p coverings hold on full and residual-proxy sets.

## Chain

| Version | Result |
|---|---|
| v1 | Conditional `t*p+11440` ⇒ atom |
| v2 | Core-pencil; pack_ceil=17 |
| v3 | Lex-split injection; wall = N_can |
| **v4** | **Residual R(z) inherits lex-covering; wall = N_can_prim (B); m-subset routing for A** |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v4.py
python3 experimental/scripts/verify_kb_qatom_route_d_v4.py --check
```

## Non-claims

- Not `U(1116048)<=B*` / not `def:q-row-atom`.
- Does not bound `N_can_prim` or full `N_can`.
- Toy residual is a **proxy** (aperiodic), not the full ledger residual predicate.
