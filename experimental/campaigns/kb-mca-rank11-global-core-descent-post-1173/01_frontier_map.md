# Frontier map

## Exact parent

PR #1173 head `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

## Imported interface

After the reversible rank-eleven gauge, the selected post-near explanations
lie in an affine translate of a Reed--Solomon direction code `C'` of dimension
at most ten.  Every selected slope has one exact size-`m`, same-support
pair-noncontained record and one frozen minimizing pair.  The inherited
pointwise theorem gives

```text
sum_gamma theta_gamma <= C_s(K)
```

on every shortened row `(R+K,K,d+K)`, while its complete pair core has size at
least `d+K-theta_gamma`.

## New attack

Double count incidences between slopes and their complete pair cores.  At a
heavy coordinate `x`, span all endpoint differences among the incident
minimizing pairs.

- If this span is the full current direction code, every direction vanishes at
  `x`; hence every selected minimizing pair equals the received pair at `x`.
  The coordinate is global for the complete selected family and can be
  shortened once.
- If the span is proper, gauge by one incident pair and shorten the incident
  subfamily.  Its direction dimension drops by at least one.

The complete scalar agreement domain is used in both cases, so pair
noncontainment lifts through locator division.  No arbitrary support swap is
used.

## Finite descent

For load `L`, direction rank `s`, and shortened code dimension `K`, the heavy
incidence is

```text
I_s(K,L)=ceil((L(d+K)-C_s(K))/(R+K)).
```

The exact certificate checks every cell `s<=K<=1,048,576` for `2<=s<=10` and
proves that `I_s(K,L_s)` is nondecreasing in `K`.  Therefore the weakest rank
drop occurs at `K=s`, yielding the printed rank `10 -> ... -> 1` load table.

## Endpoint

At `K=1`, coordinates are weighted affine lines in the `(slope,constant)`
plane.  Exact pair counting pays points with no majority clone class.  A
separate dominant-line resource bound pays the remaining points after a
coordinatewise convex endpoint reduction.  The endpoint cap is `4,070,947`,
below the forced `5,201,865`.

## Successor frontier

This pays one mathematical branch but does not regenerate the active-v4
first-match ledger.  The strongest next theorem is the affine-error-rank-twelve
analogue: its first descent produces rank-ten hyperplane families whose
common-core provenance must be exploited jointly; importing the generic
rank-ten split is insufficient.
