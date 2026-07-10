# C9 major-arc structure: large signed-`e_m` = small value set = an exp(Θ(n)) family (2026-07-10)

Status: `MEASURED` (structure map, self-checking verifier) / `SCOPING` (an explicit major-arc predicate + a
structural explanation of why literal C9 fails). NOT a proof of C9 (literal C9 is refuted, avdeevvadim #444).
Verifier: `experimental/scripts/c9_major_arc_valueset_structure.py` (self-checking; 3 configs, asserts the
value-set bound, the small-`k` enrichment, and the invariance-depth monotonicity). Lane: L1 terminal, the C9
(Fourier/Sidon) large-values question, downstream of the `#448` reconciliation `mu_hat(c) = e_m(v_c)/C`.

## Context

C9 (`def:sidon-paid`) needs the large-`|mu_hat(c)|` = large-`|e_m(v_c)|` directions — the **major arcs** — to be
"algebraic" and routed to cells C1–C8; only the minor arcs are paid by Fourier flatness. From `#448`,
`mu_hat(c) = e_m(v_c)/C` (`C = C(n,m)`), so the major arcs are the large values of the signed elementary
symmetric `e_m(v_c) = [x^m] prod_{a in mu_n}(1 + x e_p(f_c(a)))`. This note maps that large-values structure.

## Findings (verified)

1. **Major arc = small value set.** Sorting `c` by `|e_m(v_c)|`, the top directions concentrate sharply on small
   value set `k(c) = |{f_c(a) mod p : a in mu_n}|`: top-1% is `5–18x` enriched for `k <= n/2` vs baseline, and
   the extreme arcs sit at `k = 2,3,4`. (`|e_m|` is governed by the full value-set multiplicity profile and the
   phase arrangement, not `k` alone; small `k` is the dominant driver, not a strict dichotomy.)

2. **Structural families.** The cleanest small-value-set family is `mu_d`-invariant `f_c`:
   `f_c(omega a)=f_c(a)` for `omega in mu_d` (`d | n`) `<=> support(c) subset {j : d|j} <=> f_c = g(a^d)`, value
   set `<= n/d`. Mean `|e_m|/sqrt(C)` climbs monotonically with the invariance depth `d` (verified:
   `d=1,2,3,4,6 -> 0.5, 2.0, 3.5, 5.2, 11.7` at `p=13,n=12`). This is the paper's **quotient/descent** arc. A
   second, non-invariant minimal-value-set family also exists (some full-support `c` with small `k` — the
   **dihedral/ramification** arcs); `k(c)` is the robust invariant and subgroup-invariance is a sufficient
   sub-case.

3. **The major arcs are exponentially many.** `#{mu_d-invariant c} = p^{#{j in exps : d|j}} ~ p^{w/d}`, which at
   the deployed row (`w = 67471`, `p = 2^31`, `n = 2^21`) is `exp(Θ(n))` for every fixed `d >= 2`
   (`d=2 -> 2^{1.05e6}`). **So the major-arc family is NOT `exp(o(N))`-few.** "Route major arcs to C1–C8"
   therefore cannot be a counting/measure bound — C1–C8 must STRUCTURALLY cover an exponentially large family.

## Consequences and placement

- **Why literal C9 is refuted (avdeevvadim #444).** #444's `COUNTEREXAMPLE_NEW_FLOOR` exhibits a heavy-fiber
  (= large-`e_m` = small-value-set) family satisfying the stated hypotheses but violating C9. Finding (3)
  explains it structurally: heavy fibers are small-value-set `c`, and these form an `exp(Θ(n))` family, so no
  counting bound pays them; only an explicit "surviving C1–C8" predicate can. Our `k(c) <= k_0` / `mu_d`-
  invariance gives a concrete candidate for that predicate (#444's specification blocker).
- **Complementary to DannyExperiments #451.** #451 bounds the FIBER size by the Frobenius-defect / cyclic-code
  dimension. The `mu_d`-invariant classification here is the same object from the `e_m`/value-set side:
  `f_c = g(a^d) <=> f_c`-fiber is a `mu_d`-coset union `<=> ` Frobenius-closed zero-interval. Our
  Lean-verified x4b reciprocal-gap theorem (`PowersumRigidity.mersenne_reciprocal_gap`, zero-sorry) is a
  rigorous instance of exactly the "standard cyclic-code dimension" step #451 invokes.
- **Honest scope.** This maps the major-arc structure and quantifies why C9 is not a soft preliminary (it is
  `<=>` the max-fiber theorem, per #444). It does not prove C9 (refuted as literal) and does not resolve the
  minor-arc payment. Its value is the explicit small-value-set major-arc predicate + the `exp(Θ(n))`-count
  diagnosis + the reciprocal-gap bridge to #451.
