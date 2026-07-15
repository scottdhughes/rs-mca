# Hostile audit: `c=0`, `g=X^a`, `q=128`, `f=59`, singleton occupancy `b<=7`

## Verdict

```text
FROZEN CLAIMANT PINS: PASS
RESIDUAL OWNERSHIP AND UNIT CANCELLATION: PASS
FOUR NORMALIZED INVERSE-MOMENT INVARIANTS: PASS
ANTIPODAL SINGLETON/DOUBLE DECOMPOSITION: PASS
REDUCTION OF DOUBLE LABELS TO PINNED q64 CAPS: PASS
TWO-ODD-MOMENT SINGLETON CERTIFICATE, INCLUDING b=1: PASS
PROJECTIVE 128-CELL PAYMENT AND TARGET ARITHMETIC: PASS
COARSE q64 RELATION AND COARSE-FIRST DISJOINTNESS: PASS
b>=9 / q128 f=54..58 / GENERAL g / ALL c=0 / OFFICIAL PAYMENT: NOT PROVED
```

Accepted claimant pins:

```text
work/C0_Q128_F59_SINGLETON_B1_7_PAYMENT.md
90aa42d622ae074f4a7a39e9acb894873978127c1a69d51bb122e4c93c89d143

work/verify_c0_q128_f59_singleton_b1_7_payment.rb
237c6118f1c8985d58ebd387d449aaddac395acb1f31ab9a4e8e6450c4529458

work/verify_c0_q128_f59_singleton_b1_7_payment.expected.txt
b85b4ce5545e669c0c3cdb2b94f00cf488bbe12fa8ec33c9dde485c8af349511
```

The claimant verifier replays byte-for-byte against its expected output.
The pinned `q=64` three-invariant theorem and its verifier also replay
byte-for-byte.

## 1. Projective residual ownership

Write

```text
L=A(X)Q_S(X^B),
B=16,384,
deg A=14,449<B,
Q_S(Y)=q_0+q_1Y+...+Y^59.
```

Every support root lies in the multiplicative deployed domain, so `A(0)`
and `q_0` are nonzero.  If `L` and `L'` lie in one projective residue ray
modulo `X^a`, reduction modulo `X^B` gives

```text
q_0 A=c q'_0 A'.
```

Both sides have actual degree `14,449<B`.  Comparing leading coefficients
and then using monicity gives `A=A'`.  Thus the monic residual support is
owned by the projective ray; no sum over residual supports is hidden here.

The common `A` is a unit modulo `X^a`, so it may be cancelled.  Since

```text
4B=65,536<a=67,472<81,920=5B,
```

the cancellation exposes exactly the normalized quotient coefficients

```text
q_j/q_0,  1<=j<=4.
```

Expanding

```text
Q_S(Y)/q_0=product_(y in S)(1-Y/y)
```

shows that these are the first four elementary symmetric functions of the
inverse roots.  Newton identities are valid at the deployed odd prime and
therefore fix inverse power sums `p_1,p_2,p_3,p_4`.

The projective normalization does not fix `q_0`.  However

```text
q_0=(-1)^59 product_(y in S)y
```

lies in `mu_128`, so at most 128 absolute scalar cells occur.  The final
factor is 128, not `p-1`.

## 2. Antipodal reduction

Pair `mu_128` by `x <-> -x`.  If `b` pairs contribute exactly one selected
root and `d` pairs contribute both roots, then

```text
b+2d=59.
```

For each double pair use its label `z=x^2 in mu_64`; the labels form a
`d`-subset `D`.  Odd inverse moments cancel on every double pair, so the
singleton inverse-root set has fixed first and third power sums.

After a singleton set is fixed, its even-moment contributions are known.
Each double pair contributes `2z^(-1)` and `2z^(-2)` to inverse moments two
and four.  The fixed absolute coefficient `q_0`, together with the fixed
singleton product, also fixes `product_(z in D)z`; the sign `(-1)^d` is a
fixed constant.  Hence `D` lies in one fixed

```text
(product, sum z^(-1), sum z^(-2))
```

fiber.  Deleting the labels touched by singletons can only decrease its
size, so embedding in the full `mu_64` permits the independently accepted
caps

```text
d=29: 25,307,496
d=28: 20,826,085
d=27: 14,641,173
d=26: 10,193,410.
```

The exact pinned input is

```text
work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md
99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b
```

with byte-matching verifier and expected output pins

```text
baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5
28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1.
```

## 3. Two-odd-moment certificate

Let `U` be the inverse singleton set and fix

```text
sum_(u in U)u,       sum_(u in U)u^3.
```

For `b>=3`, a `(b-2)`-subset `W` leaves an omitted unordered pair `{u,v}`.
The two fixed moments determine

```text
s=u+v,
h=u^3+v^3.
```

The no-antipodal condition gives `s!=0`.  Since the deployed
characteristic is not three,

```text
uv=(s^3-h)/(3s).
```

Thus `{u,v}` is the unique root multiset of
`Z^2-sZ+uv`.  Two different singleton sets in the same moment fiber cannot
share a `(b-2)`-certificate.  Counting certificates yields

```text
H_b<=floor(binomial(128,b-2)/binomial(b,2)).
```

At `b=1` the certificate formula is not invoked: the fixed first moment is
the singleton itself, so `H_1=1`.  The exact caps are

```text
H_1=1,
H_3=42,
H_5=34,137,
H_7=12,598,400.
```

The independent replay also exhausts no-antipodal subsets of `mu_16` over
`F_257` at all four values and independently checks omitted-pair uniqueness,
including the `s=0` guard.

## 4. Exact arithmetic

Multiplying singleton and double-label caps inside each disjoint occupancy
cell gives

```text
b=1:           25,307,496
b=3:          874,695,570
b=5:      499,805,722,701
b=7:  128,420,656,544,000
```

Their absolute-cell sum is

```text
128,921,362,269,767.
```

After the 128 possible quotient constants, the complete `b=1,3,5,7`
population in one projective ray is bounded by

```text
16,501,934,370,530,176
<274,854,110,496,187,592,
```

with exact margin

```text
258,352,176,125,657,416.
```

## 5. Exact coarse-first routing

A pair of antipodal complete `q=128` children is one complete `q=64`
fiber.  A singleton child is not complete at the coarser scale.  The
original residual has only `14,449<B` roots, so it cannot fill even one
missing `q=128` child.  Therefore the canonical coarse full-fiber count is
exactly `d`, while the coarse residual degree is

```text
14,449+bB.
```

Consequently

```text
b=1 -> q64 f=29, residual 30,833,
b=3 -> q64 f=28, residual 63,601,
b=5 -> q64 f=27, residual 96,369,
b=7 -> q64 f=26, residual 129,137.
```

The accepted complete coarse `f=29` and `f=28` payments are pinned by

```text
work/C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md
704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5

work/HOSTILE_AUDIT_C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md
c1e4bdef06b71d881df7a35477e4d364f4d84692ac011ee5443bb4178d3e3225

work/C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md
9c0142793a738513f8a83801ff2536cd2a463b8f377a34be716ca5744b1f4709

work/HOSTILE_AUDIT_C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md
8f6870c1f834f06507823fa60101c75230b4610588bad8bb9c5451b46c3488f6.
```

Under the stated coarse-first rule, `b=1,3` have already been deleted and
must not be added again.  The genuinely new disjoint `b=5,7` payment is

```text
16,501,819,170,137,728<T,
margin=258,352,291,326,049,864.
```

No `b>=9` cell is deleted by this argument.  No `q=128,f=54..58` stratum,
general monic modulus, complete `c=0` branch, or official question is paid.

## Independent replay

```text
work/audit_c0_q128_f59_singleton_b1_7_payment.rb
sha256=2e7effaad5b125e3ac005a7f8c0ad83b423f6bd4d002699bac1c13d091776f2a

work/audit_c0_q128_f59_singleton_b1_7_payment.expected.txt
sha256=34a0899be01bc84e5f22531490bd02dacd07e860cc9fade379a5d175e7a7851e
```

Run with

```bash
ruby --disable-gems -w work/audit_c0_q128_f59_singleton_b1_7_payment.rb
```
