# Rank-nine fixed-basis exact compiler formalization

## Claim

The exact finite statements in Eqs. (1.4), (3.1)--(3.2), and (4.1)--(4.5) of
`experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at `3404d21` hold with their printed quantifiers, integer endpoints,
binomial coefficients, multiplicity sums, excess definition, hypotheses, and
conclusions.

## Status

PROVED for the mapped arithmetic and finite-list compiler statements. The
affine-line geometry, selector realization, MDS input, and five-pencil
counterexample are explicitly outside this package.

## Parameters

```text
n = 2097152
j = 981104
lowBase = 67480
target = 17907572507584
m20 = 1030160
C0 = C(67480,8)
```

Natural-number floor division and subtraction remain exactly as printed.
`binom` uses the standard descending-factorial quotient for every pair of
natural inputs.

## Existing paper dependency

This is a statement-preserving formalization of the integrated local route-cut
note by Scott Hughes, pinned to `3404d21`, not a promotion into Papers A--D.
The source note imports geometric predecessors; this package formalizes only
the exact finite compiler after their incidence and cardinality interfaces are
available.

## Proof idea or experiment

Kernel `decide` checks the closed binomial quotients, margins, and sharp
aggregate allowance. `omega` proves the all-`M_B` threshold equivalence and
the full low-union interval. Two induction lemmas prove, for every finite list
of basis multiplicities, the pointwise-cap upper sum and the exact
baseline-plus-excess upper sum. Those lemmas combine with the printed
cardinality and lower-incidence hypotheses to prove the exact cap-20 and
aggregate conclusions.

The companion verifier binds the source note by SHA-256, anchors every mapped
equation, recomputes the integers with Python's exact `math.comb`, requires
exact normalized Lean definition and theorem statements, binds the reviewed
Lean blob by SHA-256, rejects forbidden declaration and trust-bypass tokens,
verifies every theorem docstring's source pin, and includes twelve
statement/definition/comment/global-declaration tamper tests.

## Ledger impact

None. This locks the finite compiler of an already proved local route cut. It
does not prove that the deployed basis-multiplicity family meets the aggregate
excess hypothesis and therefore supplies no new branch or ledger payment.

## Constants

Lean checks the cap-20 quotient `17411776716968`, its target margin
`495795790616`, the cap-21 quotient `18282365552816`, its target excess
`374793045232`, and the sharp aggregate allowance
`5284485264881189380664190436821715347228277374`. At one more than that
allowance, the integer quotient rises from the target to the target plus one.

## Reproducibility

From `experimental/lean/rank9_fixed_basis_exact_compiler`:

```text
lake clean
lake build
```

From the repository root:

```text
python3 experimental/scripts/verify_rank9_fixed_basis_exact_compiler.py --check
python3 experimental/scripts/verify_rank9_fixed_basis_exact_compiler.py --tamper-selftest --check
```

Expected results are `RESULT: PASS (73/73)` and
`tamper-selftest: caught 12/12`.

## Nonclaims

The package does not formalize Lemma 2.1, Eq. (2.4), selector or basis
realization, the MDS row-flat proof, the five-pencil construction or Eq. (5.4),
cyclic or KoalaBear field semantics, satisfaction of Eq. (4.6), a branch
closure, a safe ledger, an MCA/List threshold, or an official score change.
