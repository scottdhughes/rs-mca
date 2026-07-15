# Fresh cross-model review: reduced-CRT pointwise bridge and ledger replacement

**Reviewer:** Claude Sonnet, fresh non-persistent read-only CLI session with
optional MCP servers disabled.

**Verdict:** GREEN.

**Ledger authorization:** YES.

## Statement audited

For the frozen profile

\[
(\ell,d,r,t,(a_i))=(4,3,1,3,(2,2,2)),
\]

the reduced-CRT rank dichotomy plus the direct mixed-background pointwise
bridge gives at most one exact target codeword per canonical cofactor-support
key. Thus the existing row may be replaced from `155,952` by `432` without
double charge. No global theorem, higher-`m` statement, or PR `#763`
application was reviewed or authorized.

## Files read

- `experimental/notes/l1/l1_b9_frontier_31222_reduced_crt_lemma.md`
- `experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage`
- `experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py`
- the lemma and ledger JSON certificates in
  `experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/`
- `experimental/scripts/analyze_l1_b9_frontier_31222.sage`
- `experimental/scripts/scan_l1_full_list_quotient_conjecture.py`
- `experimental/scripts/verify_l1_b9_frontier_31222_owner_partition.py` and
  its certificate
- the v4 full-rank ledger certificate and the complete 75-row profile list
  obtained by importing `build_report` from
  `experimental/scripts/verify_l1_b9_m2_full_rank_ledger.py`
- the prior YELLOW review as audit history only
- `experimental/notes/l1/l1_general_reconstruction_collapse.md`, read in full
  in the supplemental fresh-context pass below

The initial pass did not read
`experimental/notes/l1/l1_general_reconstruction_collapse.md`, correctly
observing that the revised proof does not import its background-free/full-petal
theorem. A second fresh read-only cross-model pass then read that required
upstream context in full and preserved GREEN/YES, as recorded below.

## Independent derivation

The reviewer independently checked the following implication chain.

1. The received word is zero on the core and background and equals
   `c_i L_C` on petal `i`. Exact `d=3,r=1` therefore gives unique core and
   background agreements `h,beta`. A degree-`<5` explaining polynomial
   factors as
   \[
   P=(X-\beta)(X-h)V=RHV,\qquad \deg V\le2.
   \]
2. On the exact two-point agreement set `S_i` in petal `i`, disjointness from
   the core permits cancellation of `H`, giving
   `B_i | (RV-c_iF)`. Hence every exact target enters the reduced system.
3. With `D=C\setminus\{h\}`, `F=L_D` split squarefree, `H=X-h`,
   `gcd(R,L_C)=1`, and `U|_C=0`, a factor
   `(X-alpha)|gcd(F,V)` has `alpha in D` and `alpha != h`. Therefore
   `W(alpha)=0=U(alpha)`. For every `x in D`, `R(x)H(x) != 0`, so the exact
   missed core is `D\setminus Z(V)` and has size at most two.
4. Thus compatible rank drop is empty in exact `d=3`; affine-inconsistent
   rank drop is empty; and full rank supplies at most one monic cubic for a
   fixed cofactor key.

## Disjointness and ledger arithmetic

An exact target uniquely determines its background agreement, each labelled
two-point petal support, and its restored core point. The full-rank bound is on
all monic cubics for one cofactor key, hence across all four possible restored
core points; there is no extra factor four. The reviewer confirmed 432 unique
canonical support masks and the one-row match in the 75-row v4 ledger.

The replacement arithmetic was independently checked:

\[
1{,}503{,}967-155{,}952+432=1{,}348{,}447,
\]

\[
668{,}803-155{,}952+432=513{,}283.
\]

After replacing the target row, the largest remaining row is

\[
(\ell,d,r,t,(a_i))=(4,3,2,3,(2,2,1)),\qquad (G_2,G_R)=(4,4),
\]

with charge `155,952`.

## Mutation gates replayed

The reviewer ran the verifiers rather than relying only on printed JSON:

- Sage plain replay passed; all eleven tamper checks were caught, including
  core/background overlap, nonsplit and repeated locators, `alpha=h`, and
  nonzero core data.
- The Python ledger replay passed; all five tamper checks were caught,
  including a duplicate canonical assignment with a fresh textual identifier.
- The existing-owner replay and its six tamper checks passed.

## Findings

No mathematical or ledger defect was found. The revised packet directly fills
the semantic bridge and disjointness omissions identified by the prior YELLOW.
The owner audit contains no prior partial payment to subtract: its nine
periodic full-support refinements were recorded but not banked against the
aggregate target row.

## Scope and nonclaims

This review authorizes only the local frozen-row replacement and the two
resulting integer totals. It does not authorize a global mixed-petal theorem,
an `m>2` extension, PR `#763`, Lean, or git/GitHub activity.

## Supplemental upstream-context check

**Supplement verdict:** GREEN.

**Ledger authorization remains:** YES.

A second fresh read-only Claude Sonnet session read the upstream reconstruction
note in full together with the revised lemma, this review, the concrete
analyzer, and `sunflower_word_from_blocks`. It confirmed:

- the upstream statement is explicitly background-free and full-petal;
- its agreement formula `M(E)=E\setminus Z(W_E)` supplies only a consistency
  analogy for the pointwise zero-locus principle;
- the reduced-CRT lemma covers the different mixed profile with one background
  hit and partial two-of-four petal supports;
- the mixed exhaustivity factorization and pointwise bridge are derived
  directly from the received-word and analyzer definitions, with no import of
  the narrower upstream theorem;
- the analyzer definitions of `F,H,R,V,W` match the revised lemma term for
  term; and
- no contradiction, missing hypothesis, or hidden dependency was found.

The supplemental reviewer therefore preserved the original GREEN verdict and
YES ledger authorization.

## Minimal next action

Regenerate the lemma and ledger certificates with the bank flag true and rerun
the full local verifier chain. The next mathematical attack is the
existing-owner partition for `(4,3,2,3,(2,2,1))`; no broader theorem is
authorized.
