# Wolfram exact replay

Wolfram Language independently evaluated the frozen integer formulas and
returned:

```text
A                    1114499
anchor overlap       131846
emitted core         42448
M2                   252
R2                   247628556
M3                   4023
R3                   3953213019
transverse total     274871033266908609
slack                109694844486478
residual load        109694844486479
parents              27749
incidences           1177889552
balanced degrees     1055 / 1056
remainder            458912
intersections        1614, 62, 3, 1
weighted loads       4172156357758, 158681059954, 6035034641,
                     229522148, 8728902, 331960, 12625, 481, 19, 1
```

The connector emitted harmless undefined-symbol/front-end warnings but the
returned exact integer association agrees with both Python implementations.
No theorem gate depends on a numerical approximation.
