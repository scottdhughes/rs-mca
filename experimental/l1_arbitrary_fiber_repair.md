# L1 Arbitrary-Fiber Repair Note

- **Status:** COUNTEREXAMPLE / PROVED / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-18.
- **Scope:** Paper B locator-fiber definitions and the final arbitrary-word
  locator local-limit target.  This note does not edit Papers A-D and does not
  assert Reed-Solomon list-decoding, MCA, or protocol safety.

## Summary

The raw arbitrary support fiber

```text
Fib_U(s) = {S subset H : |S| = s and deg(U mod L_S) < k}
```

is too large to be the final arbitrary-word positive object.  It counts
agreement supports, not listed codewords.  A single codeword agreeing with the
received word on `a >= s` coordinates contributes `binom(a, s)` raw supports.

Consequently the literal raw-support statements in `conj:arbitrary-local` and
`conj:final-locator`, if read as bounds for all `U` on `|Fib_U(k+sigma)|`, are
false: for `U=0`, every `s`-subset of `H` lies in `Fib_U(s)`, while the list is
only the zero codeword.

This is not a new list-decoding counterexample.  It is a counterexample to the
raw support-count route.  The list-size theorem should instead use an image,
maximal-support, or canonical-selector fiber.

## Exact Decomposition

Let `C = RS[F,H,k]`, let `U` be the interpolant of a received word, and let
`k < s <= n`.  For every degree-`<k` polynomial `P`, define its agreement set

```text
A_P(U) = {x in H : U(x) = P(x)}.
```

Then the map

```text
S |-> U mod L_S
```

sends `Fib_U(s)` onto the list

```text
List_U(s) = {P in F_{<k}[X] : |A_P(U)| >= s}
```

and its fiber over `P` has size exactly `binom(|A_P(U)|, s)`.  Therefore

```text
|Fib_U(s)| = sum_{P in List_U(s)} binom(|A_P(U)|, s).
```

This identity is elementary:

1. If `S in Fib_U(s)`, then `P_S = U mod L_S` has degree `< k` and agrees with
   `U` on every point of `S`, so `S subset A_{P_S}(U)`.
2. Conversely, if `P` has degree `< k` and `S subset A_P(U)` with `|S|=s`,
   then `U mod L_S = P`, so `S in Fib_U(s)`.
3. Since `s > k`, two degree-`<k` polynomials cannot both agree with `U` on the
   same `S`; their difference would have more than `k-1` roots.

Thus the raw fiber is a support-expanded list, not the list itself.

## Candidate Repaired Objects

### Raw Support Fiber

```text
RawFib_U(s) = Fib_U(s)
```

- **Status:** COUNTEREXAMPLE as a universal positive object.
- **List upper bound:** Yes, but very lossy.
- **Zero-word behavior:** `|RawFib_0(s)| = binom(n, s)`.
- **Problem:** Counts all `s`-subsets of one large agreement set.

This object remains useful for monomial-prefix packets because Paper B's
`prop:monomial-fiber` gives an exact bijection there.  It is not suitable for
arbitrary received words.

### Codeword-Image Fiber

```text
ImgFib_U(s) = {U mod L_S : S in Fib_U(s)}
```

- **Status:** PROVED exact list object.
- **List upper bound:** Equality with the list at agreement threshold `s`.
- **Zero-word behavior:** `|ImgFib_0(s)| = 1`.
- **Tradeoff:** This is less support-combinatorial, but it is the object the
  theorem actually needs.

Recommended repair:

```text
|ImgFib_U(k+sigma)| <= n^B
```

above the corrected entropy and quotient reserves.

### Maximal Agreement-Support Fiber

```text
MaxFib_U(s) = {A_P(U) : deg P < k and |A_P(U)| >= s}
```

- **Status:** PROVED exact list object for `s > k`.
- **List upper bound:** Equality, because `P |-> A_P(U)` is injective when
  `|A_P(U)| >= s > k`.
- **Zero-word behavior:** one maximal support, namely `H`.
- **Tradeoff:** Supports have variable sizes rather than fixed size `s`.

This is the cleanest support-level repair if variable-size supports are
acceptable.

### Exact Full-Agreement Fiber

```text
ExactFullFib_U(s) = {A_P(U) : deg P < k and |A_P(U)| = s}
```

- **Status:** AUDIT.
- **List upper bound:** No, not by itself.  Codewords agreeing on more than
  `s` points are omitted.
- **Zero-word behavior:** empty unless `s=n`.
- **Use:** Useful for shell decompositions, but a radius-`1-s/n` list theorem
  needs the cumulative union over agreement sizes `>= s`.

### Canonical Selector Fiber

Fix a total order on `H`.  For each `P in List_U(s)`, let `sel_s(A_P(U))` be
the lexicographically first `s`-subset of its agreement set.

```text
CanFib_U(s) = {sel_s(A_P(U)) : P in List_U(s)}
```

- **Status:** PROVED exact list object after choosing the order.
- **List upper bound:** Equality with the list.
- **Zero-word behavior:** one selected support.
- **Tradeoff:** Depends on an arbitrary order, but remains a fixed-size support
  object contained in `RawFib_U(s)`.

This object is useful when a proof method needs fixed-weight supports but must
not count every sub-support.

## Evidence Checks

The finite verifier

```text
experimental/verify_l1_arbitrary_fiber_repair.py
```

checks the decomposition identity directly on tiny prime-field cases by
enumerating all `s`-subsets, grouping valid raw supports by the interpolated
degree-`<k` polynomial, and then verifying that each group has size
`binom(|A_P(U)|, s)`.

The default verifier run passed all five cases:

| case | raw support fiber | image/max/canonical fiber | exact-full shell |
|---|---:|---:|---:|
| `p=5,n=4,k=2,s=3`, zero | 4 | 1 | 0 |
| `p=5,n=4,k=2,s=3`, monomial | 0 | 0 | 0 |
| `p=17,n=16,k=8,s=9`, zero | 11440 | 1 | 0 |
| `p=17,n=16,k=8,s=9`, monomial | 0 | 0 | 0 |
| `p=17,n=16,k=8,s=9`, random seed 0 | 651 | 471 | 451 |

For every row, the verifier checks

```text
raw support fiber size = sum_P binom(|A_P(U)|, s)
```

and that the image, maximal-support, and canonical-selector repairs have the
same cardinality.

### Current-main locator sweep

Running the current experimental locator sweep at

```text
p=17, n=16, k=8, s=9
```

gave:

| template | supports checked | raw fiber size |
|---|---:|---:|
| zero | 11440 | 11440 |
| monomial `x^k` | 11440 | 0 |
| random seed 0 | 11440 | 651 |

Here `11440 = binom(16,9)`.  The zero row is the raw-support overcount: the
list contains the zero codeword, while `RawFib_0(9)` contains every 9-subset.

### Submitted local packet runner

The local packet runner from PR #77 was run on its tiny case set.  It reported
two Python/Sage matched cases, no mismatches, and all matched cases agreeing.
The tiny packet includes:

| p | n | k | s | template | raw fiber size | supports checked |
|---:|---:|---:|---:|---|---:|---:|
| 5 | 4 | 2 | 3 | zero | 4 | 4 |
| 5 | 4 | 2 | 3 | monomial | 0 | 4 |

Again, the zero row is a raw-support multiplicity effect, not a large list.

### PR #74 monomial-prefix collision packet

The open PR #74 verifier was run in a temporary worktree.  It reports the
finite packet

```text
p=17, n=16, k=6, sigma=4, s=10
total supports: 8008
distinct prefix values: 7968
fiber histogram: {1: 7928, 2: 40}
maximum fiber size: 2
active quotient cores: []
all collision fibers aperiodic for orders [8, 16]: True
```

This packet is not undermined by the repair.  In the monomial-prefix setting,
Paper B's `prop:monomial-fiber` identifies prefix fibers with listed codewords:
`S |-> U_c - L_S` is injective.  Therefore `RawFib`, `ImgFib`, maximal-support,
and canonical-selector counts agree for those monomial-prefix fibers unless
there is an extra-agreement enlargement, which the exact monomial-prefix
identity rules out on `H`.

## Proposed Replacement Statement

A safer replacement for the arbitrary-word local limit is:

```text
For every fixed rho in (0,1) and every B, eps > 0, there is C such that
for generated-field smooth H <= F_q^* of order n=2^m, k=rho n + O(1),
and every deg U < n,

    |ImgFib_U(k+sigma)| <= n^B

whenever sigma >= C n/log n, the generated-field entropy inequality holds,
and active quotient-core contributions are absent or separately budgeted.
```

Equivalently, one may use `MaxFib_U(k+sigma)` or `CanFib_U(k+sigma)`, since
all three repaired objects have cardinality equal to the list at the same
agreement threshold.

If the paper wants to retain `RawFib_U(s)`, then it needs an explicit
multiplicity ledger:

```text
|RawFib_U(s)| = sum_P binom(|A_P(U)|, s).
```

That is a strictly stronger theorem and is false for arbitrary received words
without excluding or quotienting codewords with agreement `> s`.

## Patch-Ready Repaired Package

If this audit is promoted into Paper B, the least disruptive repair is to keep
the existing raw `Fib_U(s)` definition as a support-enumeration object, then add
one image object and use that object in the arbitrary-word conjectures.

Suggested definition:

```text
ImgFib_U(s) = { U mod L_S : S subset H, |S|=s, deg(U mod L_S) < k }.
```

Suggested proposition:

```text
For k < s <= n,

    ImgFib_U(s)
      = { P in F_{<k}[X] : |{x in H : U(x)=P(x)}| >= s }.

In particular, |ImgFib_U(s)| is exactly the list size at radius 1-s/n.
Moreover,

    |Fib_U(s)| = sum_{P in ImgFib_U(s)} binom(a_P, s),

where a_P = |{x in H : U(x)=P(x)}|.
```

Suggested repaired local-limit statement:

```text
Under the same entropy and quotient-profile hypotheses as the current
arbitrary local-limit conjecture,

    |ImgFib_U(k+sigma)| <= n^B

for every deg U < n.
```

Optional support-level equivalent:

```text
MaxFib_U(s) = { {x in H : U(x)=P(x)} :
                deg P < k and |{x in H : U(x)=P(x)}| >= s }.
```

For `s > k`, the map `P -> A_P(U)` is injective, so `MaxFib_U(s)` and
`ImgFib_U(s)` have the same cardinality.  If a fixed-size support interface is
needed, choose a fixed total order on `H` and use the canonical selector
`CanFib_U(s)`; this also has the same cardinality as `ImgFib_U(s)`.

The main paper should not replace monomial-prefix prefix fibers by `ImgFib`:
there the existing exact bijection in `prop:monomial-fiber` is sharper and
support-level counting is legitimate.

## Theorem / Counterexample Ledger

| Item | Status | Evidence | Consequence |
|---|---|---|---|
| Raw support decomposition | PROVED | Elementary argument in this note; verifier checks finite cases. | Raw `Fib_U(s)` is a support-expanded list. |
| Raw arbitrary local-limit statement | COUNTEREXAMPLE | `U=0` gives `|Fib_0(s)|=binom(n,s)` for every `k<s<=n`. | Literal `|Fib_U(k+sigma)|<=n^B` cannot be the final arbitrary-word theorem. |
| `ImgFib_U(s)` list equality | PROVED | By definition plus uniqueness of `U mod L_S`; if `s>k`, each support selects a unique degree-`<k` polynomial. | This is the natural repaired list object. |
| `MaxFib_U(s)` list equality | PROVED for `s>k` | Distinct degree-`<k` polynomials cannot agree on more than `k-1` points. | Gives a support-level repaired object. |
| `ExactFullFib_U(s)` as list object | AUDIT / INSUFFICIENT | Omits codewords agreeing on more than `s` points. | Useful only as an exact-shell decomposition. |
| `CanFib_U(s)` list equality | PROVED after choosing an order on `H` | Select one canonical `s`-subset of each maximal agreement set. | Gives a fixed-weight repaired support object. |
| Monomial-prefix prefix fibers | PROVED in Paper B, not repaired here | `prop:monomial-fiber` gives exact bijection with listed codewords. | PR #74-style prefix collision work remains valid. |
| Finite verifier | EXPERIMENTAL / AUDIT | `verify_l1_arbitrary_fiber_repair.py` passes default cases. | Regression guard for the repair logic; not an asymptotic theorem. |

## Consequence For The L1 Attack

The next L1 proof target should not try to prove raw arbitrary-support
injectivity or raw arbitrary-support polynomiality.  The productive targets are:

1. Prove the image/maximal/canonical repaired local limit.
2. Separately bound monomial-prefix support fibers, where support counting is
   exact and PR #74 gives a useful aperiodic collision packet.
3. Develop a shell or multiplicity ledger only when raw support counts are
   intentionally needed for a stronger statement.

This keeps the final list theorem aligned with the actual list size and avoids
spending effort on a false raw-support route.
