# Wolfram exact replay

Wolfram independently evaluated all ten shortened triples and returned

```text
(n_k,K_k,m_k)=(2097152-k,1048576-k,1116048-k)
```

for `1<=k<=10`, with

```text
n_k-K_k = 1048576
m_k-K_k = 67472
n_k-m_k = 981104
```

in every row.  It also reproduced the ten certified loads, dimension floors,
degree ceilings `K-k`, strict load decrease, and nonincreasing dimension
floors.  No floating-point quantity is used.
