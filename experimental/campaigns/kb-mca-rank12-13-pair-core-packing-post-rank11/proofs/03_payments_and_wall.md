# 3. Payments and first wall

## Error rank twelve

The descent reaches `K=3` with `80,415,635` slopes.  At `T=5761`:

```text
h=61,714
intersection ceiling=2
Cauchy denominator=3,806,520,638
low pair types=16
low slopes=15,697,680
high slopes=682,998
total=16,380,678
```

The contradiction slack is `64,034,957`.

## Error rank thirteen

The descent reaches `K=4` with `73,640,859` slopes.  At `T=12233`:

```text
h=55,243
intersection ceiling=3
Cauchy denominator=3,048,643,309
low pair types=18
low slopes=17,659,890
high slopes=4,998,923
total=22,658,813
```

The contradiction slack is `50,982,046`.

## Cumulative compiler

Coupling every exact deficiency layer to the cumulative Cauchy and guarded
ordinary pair-list prefixes gives:

```text
K=3 cap 14,778,066
K=4 cap 15,649,594
```

For error rank fourteen, capped descent reaches `K=8` with
`39,342,841,453` slopes, while the cumulative endpoint compiler gives only

```text
55,071,795,746.
```

The missing improvement is `15,728,954,293`.

Thus ranks twelve and thirteen are paid; rank fourteen and KoalaBear remain
open.
