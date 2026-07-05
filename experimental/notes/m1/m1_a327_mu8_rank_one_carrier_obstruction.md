# M1 a327 mu8 rank-one carrier obstruction

Status: CONSTRUCTION_FAIL / MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, and not a global Reed-Solomon list-decoding theorem.

## Statement

For a rank-one `mu_8` carrier

```text
q(Y) = u f(Y),   deg f < 32,
```

assume the seven orbit codewords are pairwise distinct. The common-zero set of
`f(X^8)` has at most:

```text
8 * 31 = 248
```

coordinates of `H`.

At those coordinates, all seven codewords may agree. Outside that set, each
pair difference has the form:

```text
f(X^8) g_ij(X),   deg g_ij <= 7,
```

and pairwise distinctness makes every `g_ij` nonzero. Thus all `21` pairs
contribute at most:

```text
21 * 7 = 147
```

outside-zero pair-equality points.

If `c_x` is the selected equality-class size, then:

```text
sum_x c_x <= 7|Z| + (512 - |Z|) + 147
          = 512 + 6|Z| + 147
          <= 512 + 6*248 + 147
          = 2147.
```

But an `a=327`, list-size-7 witness requires:

```text
7 * 327 = 2289
```

selected incidences. Since `2147 < 2289`, no pair-visible rank-one `mu_8`
carrier can produce the target witness.

## Scope

This only cuts the rank-one carrier construction. It does not rule out
rank-2 carriers, other `mu_8` orbit schedules, or any global `a=327` witness.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
