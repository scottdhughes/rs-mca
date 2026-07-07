# L1 residual excess W3 collapse-edge pattern signature

- **Status:** EXPERIMENTAL / DERIVED SIGNATURE.
- **Script:** `experimental/scripts/extract_l1_w3_collapse_edge_pattern_signature.py`
- **Output:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_pattern_signature_combo012_sizes10_2_3.json`

## Purpose

This packet mines the integrated W3 collapse-edge Lean certificate for the
small pattern that a later symbolic lemma would need to explain. It is not a
new proof layer and does not regenerate the `GF(137)` edge arithmetic.

## Extracted signature

The six certified dangerous cases split into two quotient-family triples:

- `LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v7 / affine_83_96`
  with shifts `[67,103,111]`;
- `LAW_W3_ell17_p137_p3_combo0-1-2_sizes10-2-3_v11 / affine_105_38`
  with shifts `[17,20,121]`.

In all six cases:

- the head antecedent is `(missing,stray)=(2,1)`;
- the head coset is `10`;
- the head component-size profile is `[13,1,1,1,1]`;
- the only large alternate component is coset `37`, component `[17,36,130]`;
- the alternate contribution is exactly `1`;
- every non-survivor alternate coset has maximum component size at most `2`.

The graph-mechanism extraction sharpens the last two bullets:

- every non-survivor alternate graph is a matching (`max_degree <= 1`);
- in the survivor coset, the large component `[17,36,130]` is a triangle
  (`edge_count = 3`, degree profile `{2:3}`);
- any additional survivor-coset edges are disjoint from that triangle, so they
  only create size-2 components and add no extra contribution.

The same mechanism is also expressed as a Lean finite checker in
`L1Threshold.CollapseEdgeGraphMechanism`:

- `allNonSurvivorAlternatesMatchingOnly`;
- `allCasesHaveUniqueSurvivorTriangle`;
- `allGraphMechanismsCertified`.

The stronger rule-derived checks recompute active edges from the stored
`always / never / atShift` rules at each certified shift, rather than trusting
the stored component list:

- `allNonSurvivorRuleAlternatesMatchingOnly`;
- `allCasesHaveRuleSurvivorTriangle`;
- `allEdgeRuleMechanismsCertified`.

These are the current finite explanation of the collapse: off coset `37`, the
activated edge rules have degree at most one at every vertex, so they can only
form matchings. In coset `37`, the activated rules contain the triangle on
`[17,36,130]`, no edge connects that triangle to the rest of the coset, and the
remaining active edges are matching-only.

## Scope

The signature is a derived finite-data summary. It supports the next proof task:
look for a structural reason that the two quotient-family triples force the same
alternate-collapse pattern. The immediate structural target is now:

> explain why the dangerous head pattern forces matching-only alternate graphs
> off coset `37`, and forces exactly the coset-37 triangle `[17,36,130]`.

It does not claim a symbolic W3 lemma, a global L1 theorem, or MCA/protocol
evidence.
