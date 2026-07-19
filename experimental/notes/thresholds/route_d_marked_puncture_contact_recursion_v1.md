# Route-D marked puncture-contact recursion v1

STATUS: PROVED

## Scope

This note proves one set-theoretic recursion for locator-prefix fibers with a
fixed puncture and a fully carried marked key.  It is a reduction theorem, not
a Route-D payment.  Its exact form works with an arbitrary predicate `Q` by
pulling `Q` back to the reconstructed parent packet.  A simpler recursive
upper bound is conditional on a separately proved deletion-heredity property.

The theorem does not assert that any current first-match residual is
executable, deletion-hereditary, or invariant under scaling.  It does not
route root-blind orbit representatives, divide their number by a stabilizer,
construct a rank-drop incidence, prove the KoalaBear support certificate, or
close the deployed row.

## Locator convention and exact deconvolution

Let `F` be a field, let `D` be a finite nonempty subset of `F^*`, and fix a
depth `w >= 0`.  For a finite set `A subset D`, write

```text
L_A(X) = product_(a in A) (X-a)
       = X^|A| + a_1(A) X^(|A|-1) + ... + a_|A|(A).
```

Put `a_0(A)=1` and `a_i(A)=0` for `i>|A|`.  Thus

```text
Phi_w(A) = (a_1(A),...,a_w(A))
```

is the signed locator prefix: `a_i(A)=(-1)^i e_i(A)`.

Let `mathfrak G` be the complete marked key.  It determines a fixed set
`E=E(mathfrak G) subset D` of roots which are already present or forbidden to
the padding support.  The key may carry more information than `E`, including
the common core `G`, the reference support, cell data, or rooted incidence
data.  None of that information is discarded below.  For a padding set
`P subset D minus E`, denote the reconstructed full packet by

```text
Pkt_mathfrakG(P),
```

whose full support is `E disjoint_union P` and whose key is still exactly
`mathfrak G`.

Fix a full target `z=(z_1,...,z_w)`.  Write

```text
g_i = a_i(E),   g_0=1.
```

Define the deconvolved padding target `u=delta_E(z)` triangularly by

```text
u_0 = 1,
u_r = z_r - sum_(i=1)^min(r,|E|) g_i u_(r-i),
      1 <= r <= w.                                  (D-E)
```

The product identity `L_(E disjoint_union P)=L_E L_P` gives

```text
z_r = sum_(i=0)^r g_i a_(r-i)(P).
```

Consequently the triangular recursion is unique and proves the exact
equivalence

```text
Phi_w(E disjoint_union P)=z
  if and only if
Phi_w(P)=delta_E(z).                                (factor)
```

No primitivity assumption is used in this equivalence.  In particular,
primitivity of `z` need not descend to `u`.

For one exposed root `y`, write `delta_y(u)=v`.  Since
`L_{y}(X)=X-y`, the recursion specializes to

```text
v_0 = 1,
v_r = u_r + y v_(r-1)
    = sum_(i=0)^r y^i u_(r-i),
      1 <= r <= w.                                  (D-y)
```

Thus, for `P={y} disjoint_union R`,

```text
Phi_w(P)=u  if and only if  Phi_w(R)=delta_y(u).    (one-root-factor)
```

## Stabilizer shadow and the least-contact theorem

Let

```text
H = { h in F^* : hD=D and h^r u_r=u_r for every 1<=r<=w }.
```

This is a subgroup.  The coefficient rule

```text
a_r(hP)=h^r a_r(P)
```

shows that `H` is precisely the scalar group available from the padding
target together with the ambient domain.  Define the shadow and its boundary
by

```text
HE = {he : h in H, e in E},
partial_H E = HE minus E.
```

Fix once and for all a total order `prec` on `partial_H E`.  Let `Q` be an
arbitrary Boolean predicate on complete reconstructed packets.  For a fixed
padding size `m >= 1`, define the root-contact family

```text
C_Q(mathfrak G,z) = {
  P subset D minus E :
  |P|=m,
  Phi_w(P)=u,
  Q(Pkt_mathfrakG(P)),
  P intersect partial_H E is nonempty
}.
```

For `P` in this family, let

```text
rho(P) = min_prec(P intersect partial_H E).
```

For each `y in partial_H E`, let `B_y` be the family of sets `R` satisfying

```text
|R| = m-1,
R subset D minus (E union {y}),
Phi_w(R) = delta_y(u),
R contains no b in partial_H E with b prec y,
Q(Pkt_mathfrakG({y} union R)).                     (B-y)
```

The occurrence of `mathfrak G` in the last line is literal: the complete
parent key is carried, not recomputed from an unmarked lower support.

**Theorem 1 (arbitrary-carried-`Q` least-contact bijection).**  The map

```text
beta : C_Q(mathfrak G,z) -> disjoint_union_(y in partial_H E) B_y,
beta(P) = (rho(P), P minus {rho(P)})                (least-contact)
```

is a bijection.  It preserves the full marked key `mathfrak G` as carried
data.  In particular,

```text
|C_Q(mathfrak G,z)| = sum_(y in partial_H E) |B_y|. (exact-boundary-sum)
```

**Proof.**  For `P in C_Q`, the least contact `y=rho(P)` is unique.  Put
`R=P minus {y}`.  Its size and puncture conditions are immediate.  The
least-contact definition gives the earlier-boundary exclusion in `(B-y)`,
and `(one-root-factor)` gives `Phi_w(R)=delta_y(u)`.  The predicate in `(B-y)`
is exactly the original assertion `Q(Pkt_mathfrakG(P))`; no monotonicity or
invariance of `Q` is used.

Conversely, from `(y,R) in B_y`, reconstruct `P={y} union R`.  Formula
`(one-root-factor)` gives `Phi_w(P)=u`, the explicit exclusion makes `y` the
least boundary contact, and the last line of `(B-y)` gives the original
predicate on the original marked packet.  Deletion and insertion are inverse,
and the outer tagged union makes different values of `y` disjoint.  This
proves the bijection and the cardinality identity.  QED.

The least-contact rule is essential for an exact partition.  A padding set
may contain several points of `partial_H E`; the raw families indexed by
"a contacted root" overlap.

## Conditional hereditary coarse bound

The exact theorem above does not require heredity.  To compare its boundary
families with ordinary lower-size fibers, one needs an additional hypothesis.
Say that `Q` is **deletion-hereditary with the carried key** on this recursion
if, for every relevant `y` and `R`,

```text
Q(Pkt_mathfrakG({y} union R))
  implies
Q(Pkt_mathfrakG(R)).                               (Her_Q)
```

This definition also requires `Pkt_mathfrakG(R)` to be a legal lower-size
packet with the same carried key.  It is not automatic when a mark is
recomputed after deletion.  If the natural lower mark deletes `y`, then the
boundary state must retain enough data, for example `(mathfrak G,y)`, to
recover the original key.

For a target `v`, define

```text
N_Q(E union {y},m-1,v;mathfrak G)
 = # {
   R subset D minus (E union {y}) :
   |R|=m-1,
   Phi_w(R)=v,
   Q(Pkt_mathfrakG(R))
 }.
```

**Corollary 2 (conditional hereditary boundary budget).**  Under `(Her_Q)`,

```text
|C_Q(mathfrak G,z)|
 <= sum_(y in partial_H E)
      N_Q(E union {y},m-1,delta_y(u);mathfrak G).   (boundary-budget)
```

If `partial_H E` is nonempty, this further gives

```text
|C_Q(mathfrak G,z)|
 <= |partial_H E| *
      max_(y in partial_H E)
      N_Q(E union {y},m-1,delta_y(u);mathfrak G).
```

If `partial_H E` is empty, the contact family and tagged boundary union are
empty; every displayed boundary sum is an empty sum and equals zero.

**Proof.**  In each exact boundary family `B_y`, apply `(Her_Q)` and then
forget only the least-contact exclusion.  This embeds `B_y` into the displayed
lower-size family.  Sum the disjoint exact identity from Theorem 1.  QED.

This corollary is conditional even when Theorem 1 is unconditional.  An
ordered first-match survivor predicate is not deletion-hereditary merely
because it is called first-match; heredity must be proved for the literal
executable predicates and the literal carried mark.

## Exact boundary arithmetic

The group `H` is finite.  Indeed, choose `d_0 in D`, which exists because `D`
is nonempty.  The map

```text
H -> D,
h |-> h d_0
```

is injective: `h_1 d_0=h_2 d_0` implies `h_1=h_2` because `d_0` is nonzero.
Thus `|H|<=|D|`.  Multiplication by `H` acts freely on `F^*`, so every
`H`-orbit in `D` has size `|H|`.  Let

```text
c_H(E) = number of H-orbits which meet E.
```

Then `HE` is the disjoint union of those orbits.  Therefore

```text
|partial_H E| = |H| c_H(E) - |E|                  (boundary-exact)
              <= (|H|-1)|E|.
```

For a singleton puncture, the exact boundary is `|H|-1`.

At the KoalaBear minimal top seam, the side size and common-core size are

```text
m = e = w+1 = 67472,
|E| = j-e = 913632.
```

The theorem reduces the contact side size from `67472` to `67471` and carries
the exact boundary multiplier

```text
|H| c_H(E) - 913632.
```

This arithmetic is not the desired `67472 * 2130706433` payment.  No bound on
the recursive maxima in `(boundary-budget)` is proved here.

## The root-blind obligation

The complementary root-blind family consists of pads satisfying

```text
P intersect HE is empty.
```

Its ambient source `D minus HE` is `H`-stable, and `Phi_w(hP)=u` for
`h in H`.  That observation alone does not give an action on the surviving
marked family:

1. the complete marked reconstruction must be preserved;
2. `Q` must be `H`-invariant, not merely deletion-hereditary;
3. the support action must be free before division by `|H|`;
4. a count of orbit representatives still needs a proved owner.

If a nontrivial support stabilizer is identified by an executable
`quotient_planted` first-match predicate, that packet may be routed to the
corresponding existing owner.  This note does not prove that identification.
Likewise a vanishing RIM pivot may be routed to `rank_drop_pivot` only after
the actual rooted-line incidence and the field-native rank predicate required
by that owner have been constructed.  A raw algebraic pivot is not a payment.

After any such legal deletions, free root-blind orbit representatives remain.
Choosing a canonical representative proves only

```text
#(free root-blind supports) = |H| * #(orbit representatives).
```

It does not inject the representatives into a deployed owner set.  The honest
residual obligation is therefore

```text
ROOT_BLIND_ORBIT_REP_OWNER.                         (open-owner)
```

## Counterexamples to hidden hypotheses

All locator prefixes in the finite-field examples below use the signed
coefficient convention fixed above.

### 1. First-match survival need not be hereditary

Let the only earlier cell be the singleton family `{{a}}`, and let `Q` mean
"not in the earlier cell."  Then `{a,b}` satisfies `Q`, while its deletion
`{a}` does not.  Thus the complement of an ordered earlier-cell union is not
automatically deletion-hereditary.  A Route-D application of Corollary 2 must
prove `(Her_Q)` branch by branch.

### 2. Raw contact-by-root families overlap

Over `F_11` with `D=F_11^*`, take

```text
w=2,
E={1,2},
P={3,9,10}.
```

Then

```text
u=Phi_2(P)=(0,4),
H={1,10}={+1,-1},
partial_H E={9,10}.
```

The same `P` contacts both boundary roots.  Its full target is
`Phi_2(E union P)=(8,6)`, whose first coordinate is nonzero and hence has
trivial scalar stabilizer.  This shows both that primitivity can coexist with
multiple contacts and that the least-contact selector is needed for a
disjoint union.

### 3. Deletion heredity does not imply scalar invariance

Over `F_11` with `D=F_11^*`, take

```text
w=2,
E={1},
P={2,3,6},
u=Phi_2(P)=(0,3),
H={1,10}.
```

The full target is `(10,3)`, hence primitive, and `P` is root-blind because
`HE={1,10}`.  Its nontrivial translate is

```text
-P={5,8,9}.
```

The predicate

```text
Q(A) : 5 is not in A
```

is deletion-hereditary.  It accepts the packet with padding `P` and rejects
the packet with padding `-P`.  Thus heredity alone does not make the
root-blind survivor family an `H`-set.

### 4. A primitive full target does not force free padding orbits

Over `F_7` with `D=F_7^*`, take

```text
w=3,
E={3},
P={1,2,4}.
```

Here

```text
u=Phi_3(P)=(0,0,6),
H={1,2,4},
Phi_3(E union P)=(4,0,6).
```

The full target is primitive because its first coordinate is nonzero.
Moreover `HE={3,5,6}`, so `P` is root-blind, but

```text
hP=P for every h in H.
```

The root-blind orbit has size one, not `|H|`.  Therefore even an invariant
predicate and a fully carried fixed key do not justify orbit division without
first removing or separately paying support stabilizers.

## Provenance and ownership

Two proved predecessors supply the proof pattern, not a Route-D payment:

- `experimental/notes/m1/m1_width_one_fixedroot_closure.md` and
  `experimental/lean/rs_mca_formalization/RsMca/WidthOneLedger.lean` provide
  the canonical first-root/least-root partition used here in a new punctured
  locator-prefix setting.  Both are cited at immutable commit
  `abddc1f6e92525bd138954bccc47652b8e127649`;
- `experimental/notes/m1/conjecture_f_reduction_lemmas.md`, especially its
  common-GCD reduction, provides the fixed-divisor division principle behind
  `(D-E)` and `(factor)`.  It is cited at immutable commit
  `ffc284f875ffc2d2c9112799a24c0686e4d2c860`.

The following are Route-D context only and are not consumed as payments:

- `experimental/notes/x1/x1_quotient_reduction.md` at
  `9385f54eed1544df2b2e57bba9d059d1802f9108`;
- `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md` at
  `0fa9427044fcd0a9e2fffade54dcb0c3f08253ca`;
- `experimental/notes/thresholds/cap25_v13_qfin_primitive_wall_synthesis.md`
  at `ddea8ad48652964e7a20a9ddd54f2a3b3dfa55e6`;
- `experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md` at
  `e83962ae5ad7bacb391b691ffd37f0abef977b83`;
- `experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md` at
  `0955594bf354b6a396574b65fbb242715edd3267`;
- `experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md` at
  `c23dcaa0514c72d195f1c5eb163500150ff637bd`;
- `experimental/notes/thresholds/cap25_v13_route_d_barrier_map.md`, read in
  the immutable upstream snapshot
  `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
- pending #910, the marked-pivot obstruction packet, at exact head
  `5ead2bb5e13bc0cde3f5f2b9c5eb4b6fdffb6bb0`;
- pending #913, the rooted-emission and punctured-padding no-go packet, at
  exact head `7a5036e718bb8d1f87343e9ff9a1861918d4ae7b`.

In particular, this note does not upgrade any `REDUCED_NOT_PROVED` Route-D
certificate, does not implement the eight named first-match projectors, and
does not consume the distinct-slope rank-drop owner per support or per pivot.

## Reproduction and formalization status

The deterministic verifier is

```text
experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py
```

Run its normal, optimized, and tamper modes with

```bash
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --check
python3 -O experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --check
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --tamper-selftest
```

The required standalone Lean companion uses

```text
experimental/lean/route_d_marked_puncture_contact_recursion_v1/
experimental/lean/route_d_marked_puncture_contact_recursion_v1/RouteDMarkedPunctureContactRecursionV1.lean
```

and is built with

```bash
cd experimental/lean/route_d_marked_puncture_contact_recursion_v1
lake build
```

It provides theorem-shaped generic carried-`Q`, least-contact, and hereditary
sum interfaces plus kernel-checked finite-fixture pins.  The three generic
logical/cardinality wrappers are now proved from their explicit structural,
existence/uniqueness, heredity, and inclusion-cardinality hypotheses; see the
package `README.md` for the exact theorem map.  Those hypotheses do not
instantiate the signed locator recursion or a deployed residual.  No
GrandeFinale module is claimed here.

## Nonclaims

- No executable Route-D first-match predicate is supplied.
- No deletion-heredity or scalar-invariance theorem for a deployed residual
  is supplied.
- No support payment, orbit-representative payment, or stabilizer division is
  supplied.
- No RIM-to-field-native-rank adapter is supplied.
- No primitive target is proved to exceed, or to satisfy, the deployed bound.
- No KoalaBear row-sharp atom inequality or adjacent-row closure is claimed.
- The common core and every other component of the marked key remain carried
  throughout; no unmarked side-pair count is substituted.
