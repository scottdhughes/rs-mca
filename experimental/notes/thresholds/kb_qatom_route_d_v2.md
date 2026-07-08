# KB-MCA Route-D v2: core-pencil theorem and covering reduction

Status: `PARTIAL` — new structural theorems **PROVED**; atom still **OPEN**.

Extends v1 (`kb_qatom_route_d_v1`) by reducing the max-fiber problem to a
**core count**.

## Deployed constants

```text
e = w+1 = t = 67472
core size |C| = j-e = 913632
pack_ceil = floor((n-|C|)/e) = 17
```

## Theorem 1 — core pencil in a fiber (PROVED)

Fix a prefix z and a core C subset D with |C|=j-w-1. Let U(C,z)={U subset D\C : |U|=w+1 and C∪U in Fib_w(z)}. If |U(C,z)|>=2 then for any U,V in U(C,z) the monic side locators satisfy Lambda_U - Lambda_V is a nonzero constant in F_p, and the root sets are pairwise disjoint; hence |U(C,z)| <= floor((n-|C|)/(w+1)).

### Proof

1. For `U ∈ U(C,z)`, `Λ_{C∪U} = Λ_C Λ_U` has first `w` monic coefficients equal to `z`.
2. If `U,V` both lie in `U(C,z)`, the difference `Λ_C(Λ_U−Λ_V)` has degree `≤ j−w−1 = |C|`.
3. If `deg(Λ_U−Λ_V) ≥ 1` then the difference has degree `≥ |C|+1 = j−w`, contradiction.
   Hence `Λ_U−Λ_V` is a nonzero constant.
4. Distinct fully split constant-shift monic degree-`e` polynomials have pairwise
   disjoint root sets inside `D\C`; pack to get
   `|U(C,z)| ≤ floor((n-|C|)/e)`.

Toy suite: 0 violations on all checked core pencils.

## Theorem 2 — fiber covering (PROVED)

For every z, Fib_w(z) = union_{C} {C∪U : U in U(C,z)} over cores C of size j-w-1. Consequently |Fib_w(z)| <= pack_ceil * N_active_cores(z), where N_active_cores(z) = |{C : U(C,z) nonempty}| and pack_ceil = floor((n-(j-w-1))/(w+1)).

### Deployed consequence

```text
|Fib_w(z)|  ≤  17 · N_active_cores(z)
```

Therefore the full-fiber form of the atom holds as soon as

```text
N_active_cores(z)  ≤  floor(target_floor / 17)  =  16166878605395467
```

for every prefix `z`.  Bit scale: about `2^{53.84}`.

For the stronger `t·p` residual budget:

```text
N_active_cores(z)  ≤  floor(t·p / 17)  =  8456648496904
```

## Theorem 3 — oriented first-mate injectivity (PROVED)

Within a single fiber Fib_w(z), label each non-isolated support S by its lexicographically first top-seam mate edge key (C, higher_coeffs(Lambda_side), min(c_U,c_V), max(c_U,c_V), side), where side in {0,1} selects which endpoint of the constant-shift edge is S. This label is injective on non-isolated vertices.

This is structural (labels involve cores). It confirms the top-seam graph is a
clean constant-shift edge geometry and pairs with Theorem 1.

## Counterexample — shallow `n·p` bound (PROVED)

On `F_17`, `n=16`, `j=8`, `w=1`:

```text
max fiber = 758  >  n·p = 272
```

So **E5 (`|Fib| ≤ n·p`) is false for full fibers at shallow depth**. Any `n·p`
claim must be residual-only or depth-restricted. (At `w ≥ 2` on the same toy
family, max fibers fit under `n·p`, but that is evidence only.)

## Remaining open target

Bound N_active_cores(z) <= 16166878605395467 for every z (full-fiber atom via covering with pack_ceil=17), or prove the same bound for residual cores after first-match deletion.

Why this is progress: The Q atom no longer requires a diffuse max-fiber argument: it is enough to bound the number of cores C that participate in any depth-w fiber. Each core contributes at most 17 supports at the deployed row.

Suggested routes:
- Bound active cores by injection into D x F_p or [n] x F_p using the product equation Lambda_C * Lambda_U ~ z (w equations on C).
- Show residual first-match leaves admit N_cores <= t*p / pack_ceil.
- Exploit that active C must make the convolution system for U rank-w with solution pencil compatible with z.

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v2.py
python3 experimental/scripts/verify_kb_qatom_route_d_v2.py --check
```

## Non-claims

- Does not prove `U(1116048) ≤ B*` or `def:q-row-atom`.
- Does not bound `N_active_cores` yet — that is the reduced open problem.
- Does not restore a full-fiber `n·p` bound at shallow depth.

## Relation to v1

v1 isolated the support certificate and proved filtration / fixed-core packing
/ conditional closure arithmetic. v2 upgrades fixed-core packing to a
**fiber-relative core pencil** (any two sides in the same fiber+core are
constant-shifts — not only top-seam-sampled pairs) and gives the covering
reduction with deployed constant `pack_ceil = 17`.
