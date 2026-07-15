# Independent audit: `31321` total-degree-six reduced CRT

**Reviewer:** fresh-context Codex read-only audit.

**Verdict:** YELLOW.

**Ledger authorization:** NO.

## Statement audited

The frozen

```text
(q,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2),
(ell,d,r,t,a_i)       = (4,3,1,3,(3,2,1)),
(G2,GR)                = (3,4)
```

total-degree-six CRT packet and the proposed replacement
`21,888 -> 1,152`.

## Mathematical findings

The local proof obligation is sound under its printed hypotheses.

- The labelled support-degree permutation changes the quotient bounds to
  `3-deg(B_i)`, whose coefficient counts remain `1+2+3`.  The fixed
  `12 x 9` map is injective because a homogeneous solution forces
  `B_1B_2B_3 | V` while `deg(V)<=2<6`.
- CRT identifies compatibility with the `X^3,X^4,X^5` coefficients of
  `FG mod B`, giving the reduced affine `3 x 3` map and the displayed rank
  relations.
- On a compatible rank drop, the degree gap
  `deg(F_0V_1-F_1V_0)<=5<6=deg(B)` and Euclid's lemma force a nonconstant
  `gcd(F,V)` for every compatible monic cubic.
- With `F=L_(C\{h})`, `W=R(X-h)V`, split squarefreeness, block
  disjointness, and zero core/background data, a common root restores a
  missed core point.  The missed core is exactly `D\Z(V)` and has size at
  most two.
- An exact codeword has one labelled background-plus-petal key.  Full rank
  bounds all four possible restored points together, so there is no factor
  four.  The twelve periodic full-support refinements are correctly recorded
  but not subtracted from the aggregate charge.

The exact finite replay has 1,152 keys: 1,108 reduced-full-rank systems and
44 affine-inconsistent rank-two systems.  Thus the compatible-rank-drop
claim is vacuous in this `GF(19)` census.  The reviewed `31222` packet is a
nonvacuous total-degree-six control only, not the proof of this specialization.

The complete 75-row replay and arithmetic are correct:

```text
641,512 - 21,888 + 1,152 = 620,776,
104,914 - 21,888 + 1,152 =  84,178.
```

The dynamic next row is `(4,4,2,2,(3,3))`, `(G2,GR)=(2,3)`, with charge
`48*19^2=17,328`.

## Blocking certificate findings

1. The CRT validator did not bind several claim-bearing fields: labels, core
   size, locator and bridge hypotheses, rank-relation strings, and the
   symbolic reduced matrix.  In-memory mutations of those fields were
   accepted.
2. The ledger promotion gate was fail-open.  Setting only the linked CRT
   certificate's `banked` Boolean to true was sufficient for
   `validate_crt_certificate` to accept it; no GREEN review paths or hashes
   were required.

## Replay

- `31321` owner normal replay and all 16 mutations: PASS.
- `31321` CRT normal replay and all 23 then-current mutations: PASS.
- `31321` ledger normal replay and all 17 then-current mutations: PASS.
- Prior `31222` normal/tamper replay: PASS.
- Banked `d=4,r=0` normal/tamper replay: PASS.
- General reconstruction-collapse verifier: PASS.

Passing these suites did not cure the two fail-open paths above; both were
found by additional adversarial in-memory mutations.

## Minimal next action

Bind every claim-bearing CRT field, add the missing hypothesis mutations, and
require content-addressed GREEN independent and cross-model reviews before
either the CRT or ledger validator accepts `banked=true`.  Regenerate and
replay both certificates, then obtain a fresh review of the hardened hashes.
