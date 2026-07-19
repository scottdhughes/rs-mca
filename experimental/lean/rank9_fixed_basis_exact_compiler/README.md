# Rank-nine fixed-basis exact compiler formalization

This standalone Lean 4.14 package formalizes the exact finite compiler in
`experimental/notes/m1/m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`
at integrated source commit `3404d21`. The source packet is by Scott Hughes.
Its status remains a proved local route cut with no ledger movement.

## Theorem map

| Source statement at `3404d21` | Lean declaration | Status |
| --- | --- | --- |
| Binomial notation in Eqs. (1.4), (4.1)--(4.5) | `factorial`, `descFactorial`, `binom` | EXACT DEFINITIONS |
| Eq. (1.4), `C(67480,8)` | `c0_value` | KERNEL-CHECKED exact integer |
| Eq. (3.1), sharp carrier threshold for every `M_B` | `large_union_threshold_iff` | KERNEL-CHECKED quantified equivalence |
| Eq. (3.2), complete low-union interval | `low_union_interval_iff` | KERNEL-CHECKED quantified equivalence |
| Eq. (4.1), cap-20 quotient | `cap20_tail_value` | KERNEL-CHECKED exact integer |
| Eq. (4.2), cap-20 target margin | `cap20_margin_value` | KERNEL-CHECKED exact integer |
| Eq. (4.3), cap-21 quotient and excess | `cap21_tail_and_excess` | KERNEL-CHECKED exact integers |
| Eq. (4.4), multiplicity sum and excess | `total`, `excess20` | EXACT DEFINITIONS |
| Eq. (4.5), aggregate allowance | `aggregate_excess_max_value` | KERNEL-CHECKED exact integer |
| Eq. (4.5), one-step quotient sharpness | `aggregate_excess_sharp` | KERNEL-CHECKED exact integers |
| Eq. (4.1), pointwise cap upper sum | `total_le_twenty_mul_length` | KERNEL-CHECKED for every finite multiplicity list |
| Eqs. (4.4)--(4.5), baseline-plus-excess upper sum | `total_le_baseline_add_excess` | KERNEL-CHECKED for every finite multiplicity list |
| Eqs. (1.6), (4.1), exact cap-20 compiler | `uniform_cap20_compiler` | KERNEL-CHECKED under the printed cap, cardinality, and incidence hypotheses |
| Eqs. (1.6), (4.4)--(4.5), aggregate compiler | `aggregate_excess_compiler` | KERNEL-CHECKED under the printed excess, cardinality, and incidence hypotheses |
| Lemma 2.1 and Eq. (2.4), affine-line geometry | none | NOT FORMALIZED |
| Eq. (5.4), five-pencil realization of multiplicity 21 | none | NOT FORMALIZED |

## Statement boundary

Every theorem docstring pins the source path, equation label, and
eight-character source SHA. `binom` is the standard descending-factorial
quotient

```text
C(m,k) = m(m-1)...(m-k+1) / k!
```

rather than a source-specific order-eight substitute. The source's carrier
threshold is formalized as an equivalence for every natural `M_B`, and its
low-union branch as the entire quantified interval.

The finite multiplicity family is represented extensionally by its list of
values. The hypotheses `counts.length <= C(n,8)`,
`forall m in counts, m <= 20`, and `excess20 counts <= E_max` are the
exact cardinality, pointwise-cap, and aggregate-excess inputs used in the
source double counts. The uniform compiler concludes the source's sharper
`17411776716968` bound; the aggregate compiler concludes the target.

## Trust and scope

Closed integer claims use kernel reduction with `decide`, not
`native_decide`. Their axiom reports are empty. The quantified arithmetic
and list theorems report only standard Lean logical infrastructure:
`propext`, `Quot.sound`, and, for the two threshold equivalences,
`Classical.choice`. No declaration reports `sorryAx`.

This package does not formalize the affine-word-line construction, MDS
row-flatness, selector completeness, actual zero-mask realization, or the
five-pencil finite-field counterexample. It does not prove that the deployed
family satisfies the aggregate-excess hypothesis. It proves no MCA/List
payment, adjacent safe row, asymptotic threshold, protocol statement, or
official score movement.

Build with the pinned toolchain:

```text
lake clean
lake build
```

Run the fail-closed source and declaration verifier from the repository root:

```text
python3 experimental/scripts/verify_rank9_fixed_basis_exact_compiler.py --check
python3 experimental/scripts/verify_rank9_fixed_basis_exact_compiler.py --tamper-selftest --check
```

The first verifier command must report `RESULT: PASS (73/73)`; the second must
also report `tamper-selftest: caught 12/12`.
