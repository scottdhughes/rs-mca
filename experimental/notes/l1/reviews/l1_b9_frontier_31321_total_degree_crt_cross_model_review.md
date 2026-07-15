# Cross-model hardened-packet review: `31321`

**Reviewer:** fresh-context Claude Fable 5 read-only CLI audit, 2026-07-15.

Verdict: GREEN

Ledger authorization: YES

No blocker was found.  The repository was byte-identical before and after the
review; independent harnesses were run only in `/tmp`.

## Hash-pinned input

The reviewer matched the four declared unbanked hashes:

| artifact | SHA-256 |
|---|---|
| Sage verifier | `874e10d33b0a4dc502321550b77c8a73b346d5d2144b09cba52cf22c5fc4b4d3` |
| CRT certificate | `16254b97da0d5ae590ab79bc2e679a9ad61c347cd13dcf8da75aee1108d2a4dd` |
| ledger verifier | `ca1b00e97894527213c2c890b5f95c0607a222fb2ac3df664c13396d32ca1875` |
| ledger certificate | `4b9d0d44aefd5db143b0d01c8e121f78f5f066961fecd620cd71fe0ff1ee2108` |

All twelve then-present certificate links matched.  The two final banking
review paths were absent, consistently leaving the reviewed artifacts
unbanked.  The broad first attempt is retained separately with no verdict.

## Independent mathematical derivation

The reviewer independently confirmed:

1. The fixed equations give twelve coefficient rows and nine columns:
   three coefficients of `V` plus `1+2+3` quotient coefficients.  A
   homogeneous solution forces `B|V`, so the map has rank nine.
2. CRT gives the unique residue `V=FG mod B`.  Compatibility is precisely the
   vanishing of its `X^3,X^4,X^5` coefficients, an affine `3 x 3` system in
   `(f_0,f_1,f_2)`.  The ordinary and augmented rank relations follow.
3. On compatible rank drop,
   `B | F_0V_1-F_1V_0` and the cross-polynomial has degree at most five.
   Since `deg(B)=6`, it vanishes; Euclid's lemma then forces a nonconstant
   `gcd(F,V)`.
4. With `W=R(X-h)V`, split `F=L_D`, zero core/background data, and disjoint
   blocks, the common root gives another core agreement and the missed core
   is `D\Z(V)`.  Exact `d=3` is impossible on compatible rank drop.
5. The reduced system is indexed by the aggregate cofactor key and bounds all
   restored-core points jointly.  There is no factor four.  Refinement-level
   periodic payments cannot be subtracted without a disjoint refined
   injection.

The arithmetic was also independently checked:

```text
2*6*4*6*4 = 1,152
641,512 - 20,736 = 620,776
104,914 - 20,736 = 84,178
48*19^2 = 17,328
```

## Independent computations

Two fresh `/tmp` programs shared no code with the packet.

- A from-scratch `GF(19)` polynomial census reproduced all 1,152 keys, fixed
  rank histogram `{9:1152}`, reduced ranks `{(2,3):44,(3,3):1108}`, monic
  solution counts `{0:44,1:1108}`, zero compatible rank drops, and one actual
  split-core incidence on a full-rank key.
- A SymPy derivation reproduced the certificate's symbolic `M`, `u`, and
  determinant, verified the affine compatibility identity, and found generic
  cross-polynomial degree five.

The compatible-rank-drop finite check is therefore vacuous in this row and is
not presented as evidence for the universal implication.  The `31222` packet
is used only as a nonvacuous control.

## Replay and adversarial checks

```text
owner replay: PASS; 16/16 mutations caught
Sage CRT replay: PASS; 37/37 mutations caught
ledger replay: PASS; 18/18 mutations caught
```

Additional attacks against the actual validators all failed closed, including
mutations of labels, hypotheses, symbolic `M` and `u`, determinant, rank
relations, proof steps, bridge roots/data, key hashes, profile totals, and a
fully self-consistent forged banked certificate.

The decisive architectural property is that each validation call recomputes
the review gate from disk.  Internally consistent fake GREEN strings and
certificate hashes therefore do not substitute for the two declared files.

## Promotion simulation

The reviewer replayed the gate end to end in a sandbox:

1. one GREEN/YES review: still unbanked;
2. two files with one missing the exact authorization sentinel: still
   unbanked;
3. two exact GREEN/YES files: CRT and ledger bank, and the ledger directly
   links both review hashes;
4. a one-byte post-bank review edit: both verifiers fail until restored.

## Authorization and scope

This review authorizes adding the two genuine GREEN review files at the
declared paths, regenerating both certificates, replaying normal and tamper
modes, and banking only the frozen local `21,888 -> 1,152` replacement.  It
does not authorize a factor four, periodic subtraction, `m>2`, PR `#763`,
Lean, cross-`r` aggregation, or a global mixed-petal theorem.
