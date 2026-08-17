# Wolfram exact replay

Wolfram Language independently reproduced the load-bearing boundary values:

```text
K=706612: numerator 430047, denominator 86010, floor 4
K=706611: numerator 430045, denominator 86007, floor 5
ray bounds: 427975, 551027, 600590, 627362
branch caps: 4498922, 4908361, 4655278, 4937277
maximum cap: 4937277
slack: 233635
```

It also returned the exact successive low-term differences

\[
\frac{r(2A+r+1)}{2A(A+1)^2}
\]

and

\[
\frac{(r-1)(2A+r+2)}{2(A+1)^2(A+2)},
\]

which certify monotonicity across the odd/even threshold sequence. The third displayed branch cap is a safe separate-extrema diagnostic; the primary lower-envelope scan sharpens the actual three-ray cap to `4,425,931`.
