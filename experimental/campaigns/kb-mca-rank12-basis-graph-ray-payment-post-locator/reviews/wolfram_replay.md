# Wolfram exact replay

A stateless Wolfram Language kernel independently reproduced the first paid
and adjacent cells.

```text
rank1_cap_at_60010 = 2,394,811

K=778,969:
  incident = 2,394,808
  core = 718,959
  r = 262,145
  4r = 1,048,580
  ray endpoints = {1,067,277, 957,884, 957,885, 262,157}

K=778,970:
  incident = 2,394,810
  core = 718,960
  r = 262,144
  4r = 1,048,576
  ray endpoints = {1,067,271, 957,882, 957,883, 262,156}
  ray cap = 1,067,271
  composed total = 5,138,218
  slack = 32,694

threshold r = 262,144
threshold core = 718,960
paid interval length = 269,607
```

It also returned the two exact second derivatives used in the endpoint
optimization:

\[
\frac{r(r+1)}{x^3},
\qquad
\frac{(K+r-2)(K+r-1)}{(K-1)y^3}.
\]

Both are nonnegative in the declared ranges. No Wolfram output is used as an
unverified premise; the Python verifiers reconstruct all values independently.
