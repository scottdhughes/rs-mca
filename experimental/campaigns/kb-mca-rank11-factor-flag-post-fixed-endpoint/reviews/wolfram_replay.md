# Wolfram exact replay

Wolfram Language independently evaluated the deployed integer profile at

```text
tau=1936, Z2=117731, Z3=23354.
```

It returned:

```text
A               1114112
H0              1116044
h                133004
owner            983040
Q1                   15
Q2                  255
c12               15274
c13              109651
c23               94378
N1           8415196932
N2            382360905
low   219935524214538240
high   55043143075392992
total 274978667290066176
slack      2060821328911
```

For the adjacent threshold `Z3=23355`, exact optimization returned
`Z2=117731`, total `274995846032030976`, and excess
`15117920635889`.

All quantities are exact integers; no numerical approximation is used.
