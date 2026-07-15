# Independent review: L1 B9 boundary `(3,2,1)` dichotomy

Date: 2026-07-14

Review mode: read-only, fresh-context Codex proof audit.  The reviewer did not
edit the proof, verifier, certificates, or ledger.

## Statement reviewed

For monic pairwise-coprime locators of degrees

```text
(deg R; deg B_1, deg B_2, deg B_3)=(2;3,2,1),
```

and pairwise-distinct nonzero labels `c_i`, the moving-monic-quartic
compatibility system has at most `q` quartics when its original coefficient
matrix has rank `15`; every rank drop is affine-inconsistent.

## Verdict

**GREEN.**  No counterexample or algebraic gap was found under the printed
hypotheses.  This is a local fixed-`m=2` statement only.

The review checked independently that:

1. CRT turns the divisibility equations into the vanishing of the `X^3`,
   `X^4`, and `X^5` coefficients of `FG mod B`.
2. Since the universal fixed-unknown matrix has rank `12`, the original
   `15 x 16` moving system has rank `12` plus the rank of the reduced `3 x 4`
   compatibility map.  Reduced rank three therefore gives at most `q` monic
   quartics.
3. If reduced rank drops and the monic column is compatible, then with
   `J=G^(-1) mod B` one has `J P_2` contained in `P_4`.  The triangular top
   coefficients force `deg J<=2`; monicity forces `deg J=2`; the cubic support
   then gives `J=c_j^(-1)R`, contradicting either other distinct label and
   `gcd(B_i,R)=1`.
4. The frozen `GF(19)` target supplies every needed hypothesis: labels
   `(1,2,3)`, disjoint background and petal supports, and distinct evaluation
   points.
5. Exactly three of the `576` support patterns have order-two cyclic
   stabilizer.  They are paid by the earlier periodic first-match bucket, so
   the primitive residual contains `573` patterns and costs at most
   `573q=10,887`.

## Bookkeeping caveat

`573q` is the **post-periodic primitive residual charge**.  If this profile
were bounded in isolation instead of inside the first-match owner ledger, the
corresponding all-pattern expression would be `3+573q=10,890` at `q=19`.

## Scope and remaining risk

The exact finite Sage/Singular/Macaulay2 controls agree with the proof but are
not used as proof.  The review does not cover repeated or zero labels,
overlapping locators, `m>2`, PR `#763`, or the remaining mixed-petal add-back.
The ledger must link the number of periodic patterns to the boundary
certificate rather than silently hard-code it.
