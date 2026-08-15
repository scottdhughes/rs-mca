# KoalaBear rank-eleven six-anticode and critical-core router

Status: proved direct branch payment plus structural route cut.  Exact parent
is PR #1172 head `193b7bf99a5cc7ccea042f25677e698d9f988eee`.
Active-v4 ledger movement is zero.

## Five-cover payment

At support-margin cutoff `tau=1798`, the complete high tail is
`59265463111193010`.  One fixed-left rank-one pair anticode owns at most
`39537225656384765` low slopes.  Therefore five anticodes, the high tail, and
the near add-back total

```text
256951591393251779 < B*=274980728111395087,
```

with slack `18029136718143308`.

## Six-cover router

An unsafe six-cover must use six fixed-left anticodes.  Every one carries at
least `18029136718143309` slopes, forcing its fixed endpoint agreement set to
have size at least `1849634`.  Distinct directions have triple intersection
`1354598>K`, so all six endpoints synchronize to one global codeword pair.

Writing `q_i` for the complement of the six endpoint sets and `e` for the
union support of the global pair error gives `sum q_i>=5e`.  Exact
concave/convex extremal optimization of the six fixed-left capacities excludes
`e>=167814`.  Hence `e<=167813`.  After the already proved support prefix
through `96150`, the six-cover residual has minimum direction support only in
`96151..167813`.

## Actual order-32 common core

At cutoff `tau=3304`, every over-budget line has one 32-coordinate set lying
in the complete pair cores of at least `378013809` low slopes and at least
`385` distinct minimizing pair types.  After cancellation, endpoint variation
has dimension at least three, since the exact rank-two interleaved pair cap is
only `267`.

A complete scan finds `9675` cutoffs with this dimension-three consequence.
The same method cannot force core size 33; the closest exact cell is `203`
pair types against cap `262`.

## Residual

The next theorem must control at least seven rank-one anticodes, pay the
six-cover support window, or exploit the dimension-at-least-three family on
the synchronized order-32 core.  Per-anticode summation and another scalar
threshold scan are not sufficient.
