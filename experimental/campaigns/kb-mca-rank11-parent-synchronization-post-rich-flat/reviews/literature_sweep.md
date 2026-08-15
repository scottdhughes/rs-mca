# Targeted literature sweep

Date: 2026-08-15

Question: does the literature provide a directly applicable theorem that turns
many received-line-dependent low-dimensional polynomial subspaces, each with a
large common evaluation-zero set, into one chronology-safe common-factor owner?

Primary conceptual neighbors inspected include:

- V. Guruswami and S. Kopparty, *Explicit Subspace Designs*, FOCS 2013;
  Combinatorica 36 (2016), 161--185.
- Standard dependent-random-choice and convex degree-moment arguments for
  finding common neighborhoods in dense set systems.
- Sylvester/subresultant rank criteria for polynomial common divisors.

The subspace-design work proves strong intersection bounds for specially
constructed evaluation or multiplicity subspaces by Wronskian methods. The
present parents are instead arbitrary subspaces selected by one actual
received line. Its numerical design bounds cannot be imported without a new
source-specific theorem.

Dependent random choice motivates the weighted pinning step, but the theorem
used here is the exact elementary identity

```text
sum_T load(T) = sum_P load(P) * C(|J_P|,|T|)
```

and requires no external result. Likewise, the pair/triple/fourfold
intersection floors follow from convexity of `C(degree,k)`.

Sylvester and generalized subresultant theory confirms that large common
divisors are structured rank-deficiency conditions, but supplies no direct
population bound for this received-line-dependent family.

Verdict: no external theorem is load-bearing. The closest serious successor is
a Pluecker/Wronskian theorem for the actual `478` rich parents or a typed
shortening owner for the pinned dimension-five subfamily.