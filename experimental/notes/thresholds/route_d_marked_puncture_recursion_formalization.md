# Route-D marked-puncture recursion wrapper formalization

## Claim

The three generic Lean interfaces shipped as statement targets with the
marked-puncture recursion packet are provable from their displayed hypotheses:

1. carried-`Q` erase/insert data gives an exact equivalence of the parent and
   child subtypes;
2. explicit first-contact existence and uniqueness gives the unique
   least-contact partition predicate; and
3. carried membership, deletion heredity, coarse acceptance, and the supplied
   inclusion-cardinality principle give the summed hereditary bound.

## Status

PROVED

## Parameters

Arbitrary root, parent, and child types; parent/child structural predicates;
an arbitrary carried parent predicate `Q`; marked erase/insert maps; explicit
forward and backward structural implications and inverse laws; contact,
ordering, and uniqueness predicates; arbitrary root lists and natural-valued
cardinality functions.

There are no field, row, or asymptotic parameters in these wrapper theorems.
The source packet's F_7 and F_11 finite controls remain separate executable
regressions.

## Existing paper dependency

This formalizes the abstract logical kernels corresponding to Theorem 1 and
Corollary 2 of
`experimental/notes/thresholds/route_d_marked_puncture_contact_recursion_v1.md`
from source packet PR #918 (payload `5343c587`, integrated at `3404d21`).  The
source reduction and fixtures are due to Holm Buar.

The theorem map is in
`experimental/lean/route_d_marked_puncture_contact_recursion_v1/README.md`.

## Proof idea

For the equivalence, erase a parent and transport its carried predicate along
the supplied `insertErase` equality; insert a child and reuse its already
carried `Q (insert b P)` proof.  `Subtype.ext` plus the two inverse laws proves
the equivalence laws.

For the partition, the forward direction selects the supplied first contact and
uses the supplied uniqueness theorem with the arguments in the order required
to conclude `c = b`.  The reverse direction forgets minimality but retains the
allowed and contact conjuncts.

For the hereditary sum, compose carried membership with the structural,
carried-`Q`, deletion-heredity, and coarse-acceptance hypotheses.  The supplied
inclusion-cardinality principle then gives a pointwise bound; list induction
and `Nat.add_le_add` sum it.

## Ledger impact

This removes three actual Lean placeholders from a marked first-match recursion
package and kernel-checks the generic carried-key/disjointization/cardinality
interfaces.  It supports the witness-exhaustive atlas and residual-recursion
tracks without changing any finite upper ledger or threshold.

Critical nonclaims: this does not prove signed locator deconvolution in Lean;
instantiate the abstract parent and child families; construct the tagged finite
union or its exact cardinality identity; prove the deployed first-contact
existence/uniqueness or deletion-heredity hypotheses; obtain a local recursive
bound; route a vanishing pivot; produce the root-blind owner; pay a Route-D
cell; close a deployed row; or prove an MCA threshold or prize claim.

## Constants

No new numerical constant is claimed.  The existing F_7/F_11 pins and their
source verifier are unchanged.

## Reproducibility

```sh
cd experimental/lean/route_d_marked_puncture_contact_recursion_v1
lake clean
lake build
cd ../../..
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --check
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --tamper-selftest
python3 experimental/scripts/verify_route_d_marked_puncture_recursion_formalization.py --check
python3 experimental/scripts/verify_route_d_marked_puncture_recursion_formalization.py --tamper-selftest --check
```

The expected results are a clean Lean build, `STATUS PROVED` from the original
finite verifier, all 11 original tamper mutations caught, and `RESULT: PASS`
plus complete mutation coverage from the correspondence verifier.
