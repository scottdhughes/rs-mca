# Cycle 18 Audit: Resonance Slope-Map Collapse Reduction

Status: BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.

This is a local reconstruction from Danny's Cycle 18 message, checked against
the banked Cycle 14--16 ledgers. No separate Cycle 18 commit, PR file, or raw
model artifact was found in the fetched repository refs when this note was
created.

## Verdict

Cycle 18 does not solve the prize problem and does not prove the corrected MCA
conjecture. It gives a useful restricted algebraic reduction for the
`F1 / t=2 / j=3` line-incidence toy window:

```text
B=F_p, F=F_{p^2}, D=F_p, t=sigma=2, j=3, off R0.
```

Bank the following restricted lemma:

```text
iota = A0(tau1,tau2) - tau3 [W]_E
mu   = B0(tau1,tau2) - tau3 b
```

with

```text
A0=p1[W]_E+p2 b,   B0=q1[W]_E+q2 b.
```

In the `F`-basis `{[W]_E,b}`, normalized so `[W]_E wedge b=1`,

```text
Delta = wedge(iota,mu)
      = (p1 - tau3)(q2 - tau3) - p2 q1.
```

Hence `Delta` is monic quadratic in `tau3`. Writing

```text
Delta = Delta0 + alpha Delta1,
Delta_i in B[tau1,tau2,tau3],
```

gives

```text
deg_tau3 Delta0 = 2, with leading coefficient 1,
deg_tau3 Delta1 <= 1.
```

This is the bankable part. It is just algebra from the already-banked Cycle 14
forms, but it sharpens the Cycle 16 `Q==0` branch.

## Recreated Algebra

Let

```text
p1=p10+alpha p11, p2=p20+alpha p21,
q1=q10+alpha q11, q2=q20+alpha q21,
alpha^2=nu in B.
```

Then

```text
Delta0 =
  tau3^2 - (p10+q20) tau3
  + p10 q20 + nu p11 q21 - p20 q10 - nu p21 q11,

Delta1 =
  -(p11+q21) tau3
  + p10 q21 + p11 q20 - p20 q11 - p21 q10.
```

The local checker

```text
experimental/2026-06-18-fable-loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py
```

verifies this formal identity without using `sympy` or other nonstandard
dependencies.

## Non-Coprime Branch

The shared-surface branch for the two base components is now small enough to
state explicitly.

Because `Delta1` has degree at most one in `tau3`, write

```text
Delta1 = s(tau1,tau2) tau3 + h(tau1,tau2).
```

If `Delta1` is identically zero, this is the base-valued resonance branch.

Otherwise, on the open locus `s != 0`, any common surface component of
`Delta0=Delta1=0` lies on the graph

```text
tau3 = -h/s.
```

The exceptional locus `s=h=0` is lower-dimensional unless the whole `Delta1`
polynomial vanishes; it belongs in the finite scanner/audit, not in the banked
collapse claim.

## Slope Map On The Graph

The landing equation `iota=z mu` gives

```text
p1 - tau3 = z q1,
p2        = z(q2 - tau3).
```

Thus, where `q1 != 0`,

```text
z = (p1 - tau3)/q1.
```

On the graph branch `tau3=-h/s`, this becomes

```text
z(tau1,tau2) = (p1 + h/s)/q1.
```

Equivalently, eliminating `tau3` gives the Cycle 14 slope quadratic

```text
q1 z^2 - (p1-q2) z - p2 = 0.
```

Up to the fixed sign convention of this quadratic, the image is controlled by
the projective coefficient map

```text
(tau1,tau2) -> [q1 : (p1-q2) : p2] in P^2(F).
```

## Exact New Wall

The residual wall should be renamed from the Cycle 16 split wall to:

```text
W-F1-AA-RES-T2J3-RESONANCE-SLOPE-MAP-COLLAPSE.
```

Question:

```text
On every source-valid non-coprime resonance stratum in this restricted toy
window, does the rational/projective slope map above have only one-dimensional
image, giving C2=O(p)=O(n), or is there a growing-prime source-valid family
with two-dimensional image and C2=Theta(p^2)=Theta(q_line)?
```

## What Not To Bank

Do not bank:

- a proof of slope-map collapse;
- a `Theta(p^2)` counterpacket;
- a proof of `conj:B` or any corrected-reserve statement;
- any `q_gen` local-limit result;
- any list, CA, MCA, line-decoding, SNARK, or protocol consequence;
- any claim outside the restricted `B=F_p`, `F=F_{p^2}`, `D=F_p`,
  `t=sigma=2`, `j=3`, off-`R0` toy window.

The regime is sub-reserve:

```text
eta = sigma/n = 2/n.
```

It is also a `q_line` toy-window statement, not a `q_gen` theorem.

## Next Checker Target

Extend the Cycle 17 scanner to record the Cycle 18 graph data.

For each candidate source-valid `Ra/Rb` or non-coprime resonance stratum:

- derive `p_i,q_i` from the Cycle 12/14 forms;
- compute `Delta0,Delta1`;
- classify `Delta1==0`, graph branch `tau3=-h/s`, and exceptional `s=h=0`;
- on split distinct triples `T subset F_p`, count distinct slopes from both
  direct landing and the graph formula;
- compute the image size of `[q1:(p1-q2):p2]` on the source-valid stratum.

Certificate fields should include:

```text
{
  p, q_gen, q_line, E, Bnum, seed,
  stratum,
  off_R0,
  Delta1_zero,
  graph_branch,
  exceptional_locus_size,
  projective_image_size,
  C2,
  split_triples_examined,
  status
}
```

Promotion rule:

- `C2=O(p)` across growing primes plus a symbolic reason for graph-image
  collapse is candidate positive evidence for this restricted wall.
- `C2/p^2` bounded below across growing primes is a sub-reserve
  counterpacket for the wall only, not a refutation of corrected-reserve MCA.
