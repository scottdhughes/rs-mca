# M1 Cycle120 ABF Counterexample Candidate

Status: CONDITIONAL / PROOF-SPINE-CHECKED / COMPUTATION-DEPENDENT / SOURCE-AUDIT.

Source PR: `#96`, DannyExperiments, head `98f1bb4`.

## Executive Conclusion

The useful result from the latest Cycle120 packet is not the generated archive.
It is the following conditional, prize-facing negative statement.

Let

```text
K = F_17^32,
H = <theta> <= K^*,
|H| = 512,
C = RS[K,H,256].
```

Assuming the Cycle84 finite count and the Cycle116 fixed-jet transfer are
correct, the printed ABF grand MCA formulation gives

```text
epsilon_mca(C,125/256)
  >= 52,747,567,092 / 17^32
  > 2^-128.
```

Thus this row is a negative counterexample candidate at `delta=125/256` under
the printed ABF formulation. It is not an accepted prize solution and it does
not determine the exact value of `delta*_C`.

Cycle119 is still useful, but the ABF-critical dependency is Cycle116:

```text
Cycle116: agreement 262, enough for ABF's closed support threshold.
Cycle119: agreement 263, a strict-ball strengthening.
```

At `n=512` and `delta=125/256`,

```text
(1-delta)n = 262.
```

ABF Definition 4.3 uses `|S| >= (1-delta)n`, so agreement `262` already meets
the printed condition. Cycle119 gives distance at most `249`, hence also meets
the stricter external convention `249 < 250 = (125/256)512`.

## What Was Checked

No PR code was run locally. The check here used:

- PR text inspected through `git show`;
- the repo's local paper definitions;
- the public Proximity Prize page;
- the ABF text extract bundled in PR #96;
- independent arithmetic;
- a direct algebra audit of the two-ended locator theorem.

The direct official ePrint download was blocked by Cloudflare in this session.
The PR-bundled ABF PDF and text extracts are internally hash-consistent, but
they should still be independently retrieved from the official source before a
public submission.

## ABF Gates

The ABF extract bundled in PR #96 states the following.

```text
RS[F,L,k] is defined over an arbitrary finite field F.
Smooth means a multiplicative coset of a subgroup of F^* of power-of-two order.
The grand MCA challenge includes rate 1/2.
Definition 4.3 samples gamma <- F.
Definition 4.3 uses the same-support event with |S| >= (1-delta)n.
```

Under that reading, the row passes the printed grand MCA gates:

```text
field:      K = F_17^32
domain:     H = <theta>, |H| = 512 = 2^9
rate:       256/512 = 1/2
envelope:   256 <= 2^40 and 17^32 < 2^256
sampler:    gamma uniformly sampled from K
predicate:  support-wise same-support MCA noncontainment
```

No separate `q_chal`, endpoint filter, quotient filter, duplicate-slope charge,
or retained-event rule appears in the grand MCA definition as extracted. Those
may matter for protocols, but they are not part of the printed grand MCA
quantity.

## Arithmetic

The denominator comparison is exact:

```text
17^32 =
2367911594760467245844106297320951247361

floor(17^32 / 2^128) = 6
52,747,567,092 > 6
```

Equivalently,

```text
52,747,567,092 / 17^32 > 2^-128.
```

Numerically this density is about `2^-95.18`.

## Cycle116 Dependency

The Cycle116 finite theorem claimed by the PR is:

```text
LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092.
```

Unpacked into ABF Definition 4.3, this means that one pair `(f1,f2)` has at
least `52,747,567,092` line parameters `gamma in K` for which there is a support
`S_gamma` with:

```text
|S_gamma| >= 262,
f1 + gamma f2 is explained by RS[K,H,256] on S_gamma,
(f1,f2) is not simultaneously explained on the same S_gamma.
```

Since `262=(1-125/256)512`, this is enough for the ABF closed threshold.

This dependency still needs independent review of the finite count and the
fixed-jet transfer. The current integration treats it as a conditional
finite-computation input, not as a main-paper theorem.

## Cycle119 Two-Ended Check

Cycle119 claims the stronger theorem:

```text
LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092.
```

The two-ended algebra checks out as a proof spine.

Abstractly, for `j`-subsets `J` with monic locators `P_J`, set

```text
r = j + sigma,
k = n - r.
```

Assume:

```text
deg(P_J - P_J') <= j - sigma + 1,
P_J(0) = c != 0 independent of J.
```

For `A(X)=a_0+...+a_{sigma-1}X^{sigma-1}`, the selected coefficients of
`P_J A` in degrees

```text
0, j+1, j+2, ..., j+sigma-1
```

recover `A` by a common invertible triangular system:

- the degree-zero coefficient is `c a_0`;
- the high selected coefficients use only the common top `sigma-1` coefficients
  of `P_J`, with monic diagonal entries.

This gives a common linear functional `ell` with

```text
ell(P_J A) = A(beta)
```

for all `J` and all `deg A < sigma`. The standard weighted Vandermonde
parity-check argument then gives one common affine line and bad slopes

```text
z_J = -P_J(beta)^(-1).
```

Support-wise noncontainment follows because if `g` were explained on `D\J`,
then the Vandermonde column at `beta` would lie in the span of the columns at
the `j` points of `J`, contradicting independence of `j+1 <= r` distinct
Vandermonde columns.

For the Cycle119 instance:

```text
n = 512,
j = 249,
sigma = 7,
r = 256,
k = 256.
```

The augmented co-support is

```text
J_T* = J_T union R*,
|J_T*| = 113 + 136 = 249,
|H \ J_T*| = 263.
```

The top condition is:

```text
deg(P_T* - P_T'*) <= 243 = j - sigma + 1.
```

The endpoint condition is:

```text
P_T*(0) = -P_R*(0) != 0.
```

The selected degrees are:

```text
0,250,251,252,253,254,255.
```

So the proof avoids the invalid naive padding multiplication and does not use
the varying hidden coefficient that previously blocked the strict-ball step.

This verifies Cycle119 as a conditional strict-ball transfer theorem, assuming
the imported Cycle84/Cycle116 finite inputs and the stated disjointness/order
facts:

```text
theta^2 = eta,
D0 = <eta> = <theta^2>,
H = D0 disjoint_union theta D0,
J_T subset D0,
R* subset theta D0,
beta notin H.
```

## Integration Decision

Integrate this cleaned note and update the experimental ledgers. Do not import
from PR #96:

```text
cycle120 packet zip
rendered PDF
PDF rendering script
raw/generated checker folders
copied ABF PDF or rendered pages
large canonical tracker rewrite
prompt/return archives
```

The next useful object is a short human-edited proof note with:

```text
1. the ABF source gates, independently fetched from the official PDF;
2. the Cycle116 finite theorem and fixed-jet transfer;
3. the optional Cycle119 strict-ball two-ended theorem;
4. exact nonclaims and authorship/provenance text.
```

## What To Ask Danny For

Ask for a minimal reviewer packet, not another generated archive:

```text
1. A human-readable proof of the Cycle84 -> Cycle116 transfer.
2. A separate human-readable proof of the Cycle119 two-ended theorem.
3. A minimal nonmutating verifier for the finite count and transfer inputs.
4. Exact ABF PDF source references with page numbers and quoted definitions.
5. No generated-checker marketing language; classify material as proof,
   computation, audit, or heuristic.
```
