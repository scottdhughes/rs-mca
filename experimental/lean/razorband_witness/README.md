# C9 near-Sidon razor formalization

This package retains the legacy tangent-floor executable examples and now also
formalizes the finite core of
[`experimental/notes/audits/c9_r2_near_sidon_razor.md`](../../notes/audits/c9_r2_near_sidon_razor.md).

## Proved declarations

[`RazorbandWitness/NearSidonRazor.lean`](RazorbandWitness/NearSidonRazor.lean)
contains:

- the exact six-point local sets `A={0,4,5}` and `B={1,2,6}`;
- equality of cardinality, first moment, and square moment;
- exhaustive classification of all 64 local subsets, proving this is the only
  nontrivial local signature collision;
- the distinct-signature table `[1,6,15,19,15,6,1]`;
- a separated Boolean block-choice family in one two-moment fiber;
- exact product cardinality `2^k`, ordered energy `6^k`, and normalized
  energy `(3/4)^k`;
- decay of that normalized energy to zero and the exact fixed-`c=1/2`
  countergate in squared form;
- the three-block coefficient `45907`, excess base
  `45907/32768 > 1`, and its normalized-ratio compiler;
- the repaired finite cuts: small realized image bounds the normalized fiber
  ratio, and `E^3 ≤ f^8` implies `Δ^3 ≤ 1/f`.

## Scope

**COUNTEREXAMPLE_NEW_FLOOR** applies to the unrestricted literal quantitative
interface. The Lean module does not claim that the separated-block domain is a
smooth multiplicative/circle domain, that it is an exact primitive first-match
residual, or that it survives every named algebraic routing cell. Those are the
source packet's remaining specification-gated/open boundary.

The local exhaustive facts use `native_decide`; general algebraic, product,
limit, normalization, and repaired-razor theorems do not depend on
`Lean.trustCompiler`.

## Verification

From this directory:

```bash
lake build
lake env lean RazorbandWitness/NearSidonRazor.lean
```

From the repository root:

```bash
python3 experimental/scripts/verify_c9_r2_near_sidon_razor.py --check
python3 experimental/scripts/verify_c9_r2_near_sidon_razor.py --tamper-selftest
```

Recorded on 2026-07-14: artifact check passed with `RESULT: PASS`; the tamper
self-test rejected all 11 semantic mutations.
