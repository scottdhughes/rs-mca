# Route-D rooted-emission cardinality wrapper formalization

## Claim

The final finite-cardinality consequence in the source packet's “Minimal
viable rooted-emission lemma” is provable from its displayed interface: if the
fixed-line residual is duplicate-free and the supplied emission is injective
on that residual, then its length is at most `t*p`.

## Status

PROVED

## Parameters

Natural numbers `t` and `p`; an arbitrary locator-prefix target; eight named
Boolean deletion predicates; line and target maps; ambient and residual lists
of marked supports; exact-residual data; an emission into `Fin t × Fin p`; a
mark decoder; mark preservation; and residual injectivity.

There is no field implementation, deployed row, or asymptotic parameter in the
proof.  `Fin p` and `Fin t` are finite indexing envelopes in the statement,
not formalized copies of a field or of a rank-drop slope set.

## Existing paper dependency

This formalizes only the final inequality in “Minimal viable rooted-emission
lemma” of
`experimental/notes/thresholds/route_d_rooted_emission_no_go.md`, from Holm
Buar's source packet PR #913 (payload `7a5036e7`, integrated at `3404d21`).
The governing rank-drop owner contract is due to Scott Hughes, and the marked
top-seam packet interface cited by the source note is due to Vadim Avdeev.

The exact statement map is in
`experimental/lean/kb_rowsharp_route_d_rooted_emission_no_go/README.md`.

## Proof idea

Encode a pair `(i,j) : Fin t × Fin p` as `p*i + j`.  Remainder modulo `p`
recovers `j`, and cancellation of the positive factor `p` then recovers `i`.
The supplied residual injection therefore makes the encoded residual
duplicate-free.  Every code lies below `t*p`, so a small `eraseP` induction
bounds its length by that of `List.range (t*p)`.

The load-bearing Lean hypotheses are exactly `hExact.1`, which supplies
`residual.Nodup`, and `hInjective`.  The residual characterization
`hExact.2` and `hMarkPreserving` are deliberately carried in the theorem
signature for integrated-stub continuity and boundary visibility, but are
proof-unused.

## Ledger impact

This removes the package's sole explicit Lean placeholder and kernel-checks a
generic finite-envelope cardinality consequence.  It does not repair the
source packet's rooted-incidence interface gap and does not change any finite
upper ledger or threshold.

Critical nonclaims: this does not construct or validate the emission; build
the received line, slope, agreement support, explaining codeword, or actual
error support; prove noncontainment or the owner Hankel rank predicate; show
that the first coordinate is an actual rank-drop owner label or that there are
at most `t` such labels; implement the eight named first-match deletions; prove
that an arbitrary target is primitive or deployed; decode the complete marked
packet key; pay a global Route-D support cell; close a deployed row; or prove an
MCA threshold or prize claim.

## Constants

No new numerical constant is claimed.  The existing `F_17` counterexamples,
fiber sizes, matrix ranks, and `t*p` obstruction comparisons are unchanged.

## Reproducibility

```sh
cd experimental/lean/kb_rowsharp_route_d_rooted_emission_no_go
lake clean
lake build
cd ../../..
python3 experimental/scripts/verify_route_d_rooted_emission_no_go.py --check --self-test
python3 experimental/scripts/verify_route_d_rooted_emission_cardinality_formalization.py --check
python3 experimental/scripts/verify_route_d_rooted_emission_cardinality_formalization.py --tamper-selftest --check
```

Expected results are a clean Lean build, the original verifier's
`STATUS COUNTEREXAMPLE` with all 22 mutations caught, and `RESULT: PASS` plus
complete mutation coverage from the correspondence verifier.
