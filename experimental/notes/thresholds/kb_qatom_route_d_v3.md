# KB-MCA Route-D v3: canonical lex-split injection

Status: `PARTIAL` — injection + double covering **PROVED**; `N_can_cores` **OPEN**.

## Theorem A — canonical lex-split injection (PROVED)

Order D as (omega^0,...,omega^{n-1}). For S in Fib_w(z) let U(S) be the e=w+1 elements of S with smallest exponents, C(S)=S\\U(S), and c(S) the constant term of the monic side locator Lambda_{U(S)}. Then phi: S |-> (C(S), c(S)) is injective on Fib_w(z).

### Proof idea

1. `U` = e smallest exponents in `S` is the unique e-subset of `S` with `max(U) < min(C)`.
2. Same `(C,c)` ⇒ both sides lie on the v2 core-pencil for `C` inside the fiber.
3. Constant-shift pencils have **unique** monic member for each constant term `c`.
4. Hence `U` and `S` are unique.

Toy suite: `inj_fail = 0` on all six rows.

## Theorem B — double covering (PROVED)

```text
|Fib_w(z)|  ≤  pack_ceil · N_can(z)
|Fib_w(z)|  ≤  p · N_can(z)
```

with deployed `pack_ceil = 17`, so the binding per-core cap is `17` (not `p`).

### Atom reduction (full-fiber form)

```text
N_can(z)  ≤  floor(target_floor / 17)  =  16166878605395467
           ≈  2^{53.84}
```

(The p-route would need `N_can ≤ 128988645 ≈ 2^{26.94}`, which is harder.)

For the residual `t·p` budget:

```text
N_can(z)  ≤  floor(t·p / 17)  =  8456648496904
           ≈  2^{42.94}
```

## Theorem C — triangular side→core prefix (PROVED)

Let Lambda_C = X^m + b_1 X^{m-1}+... and Lambda_U = X^e + u_1 X^{e-1}+...+u_e with m=j-w-1, e=w+1, and suppose Lambda_C Lambda_U has first w monic coefficients z_1..z_w. Then for each k=1..w, as long as the coefficient ranges make sense (in particular m >= w, which holds at the deployed row), b_k is uniquely determined by (z_1..z_k, u_1..u_k) via the triangular rule b_k = z_k - u_k - sum_{i=1}^{k-1} b_i u_{k-i}.

Deployed check: `m = 913632 ≥ w = 67471`.

## Remaining wall

Bound N_can_cores(z) <= 16166878605395467 (pack route, ~2^53.84) for every z, or the tighter residual budgets via t*p.

N_can_cores counts m-subsets (cores), not j-subsets, and each core carries at most pack_ceil=17 fiber members. The lex-split gives an explicit bijection Fib <-> subset of can-cores x F_p.

### Next attacks on `N_can`

- Use triangular inversion: canonical (C,U) has b_prefix determined by (z,u_prefix); cores with fixed side-prefix lie in one m-subset depth-w fiber — apply head-depth Q / packing there if w is still large.
- Show residual first-match leaves force N_can to be poly(n) or <= t*p/pack.
- Inject can-cores into D x F_p via (min(C), b_1) after residualization.

## Chain so far (v1→v3)

| Step | Result |
|---|---|
| v1 | Conditional closure `t·p+11440` ⇒ atom (~10.9 bit slack) |
| v2 | Core-pencil + `|Fib|≤17 N_active` |
| **v3** | **Lex-split injection; `|Fib|≤17 N_can`; explicit bijection Fib↔(C,c)** |
| next | Bound `N_can(z)` |

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v3.py
python3 experimental/scripts/verify_kb_qatom_route_d_v3.py --check
```

## Non-claims

- Not `U(1116048)≤B*`, not `def:q-row-atom`.
- Does not bound `N_can` yet.
- Full-fiber `n·p` bound remains false at shallow `w` (v2 counterexample).
