# M1 a327 mu8 block rank-feedback

Status: CANDIDATE / MU8_RANK_FEEDBACK_EXACT_RANK_PENDING / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Canonical Matrix Audit

The audit reconstructs the `mu_8` orbit matrix as a canonical matrix with the
canonical formula:

```text
(zeta^(i*r)-zeta^(a*r)) * (alpha_b*zeta^t)^r * y^ell
```

for active residues `r=1..7` and quotient degree `ell<32`. The canonical
matrix reproduces the `dd07a87` front:

```text
guard-passing schedules audited = 9
canonical shape = 264 x 224
canonical rank/nullity = 224/0
```

The proposed `Q_r -> zeta^r Q_r` equivariance was checked directly. No tested
schedule certified a row action, so block decomposition was not used. This is
important: the packet refuses to manufacture Fourier blocks without an exact
equivariance certificate.

## Rank-Feedback Front

The rank-feedback scanner mutates the nine guard-passing schedules while
preserving:

- support at least `327` per orbit codeword;
- ambient pair-autocorrelation bound at most `255`;
- the same `mu_8` orbit-polynomial ansatz.

It generated:

```text
raw guard-passing mutations = 1,737
selected for exact follow-up = 64
best ambient pair bound = 200
```

Exact rank has not yet been run on these `64` follow-up schedules. The current
packet is therefore a schedule generator plus block-audit scaffold, not a proof
record and not a route cut for the mutated schedules.

## Interpretation

The `mu_8` route remains live, but the first exact block audit shows that the
hand-seeded Sidon front is full rank and not equivariant in the checked row
presentation. The next action should run exact GF(17^32) rank on the selected
mutations in small batches, then immediately classify any nullity as:

- pair-visible;
- pair-forced;
- common-kernel-only.

That rule avoids repeating the low-rank false positive.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- impossibility of other `mu_8` orbit-invariant schedules.
