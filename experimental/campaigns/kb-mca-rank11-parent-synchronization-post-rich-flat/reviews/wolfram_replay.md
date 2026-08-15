# Independent Wolfram replay

Date: 2026-08-15

Wolfram Language independently replayed the exact integer packet from the
literal constants

```text
L0 = 2,007,222,636,725
q  = 42,453
m  = 1,116,048
R2 = 247,628,052
R3 = 3,953,204,973
Q4 = 63,993
mu = 982,651
```

and returned:

```text
total parent minimum              508
fixed-dimension parent minimum    478
balanced degree split             18 with remainder 203,670
pair intersection floor           1,530
triple intersection floor         53
fourfold intersection floor       2
one-coordinate pinned load        76,352,112,631
dimension-four load cap           62,882,785,443
one-pin strict margin             13,469,327,188
```

The weighted pin table through order nine was also reproduced exactly:

```text
76,352,112,631; 2,904,268,266; 110,469,544; 4,201,831;
159,818; 6,079; 232; 9; 1.
```

No floating-point comparison decides a gate.