# L1 B9: Shared Auxiliary-Johnson Owner for `d=4,r=0`

## Status

PROVED-LOCAL / INDEPENDENT AND CROSS-MODEL REVIEWS GREEN / EXACT LEDGER
BANKED.

This note treats only the frozen sequential row

```text
(q,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).
```

It follows the banked 41331 shared-owner ledger and audits the complete exact
stratum

```text
d=4, r=0.
```

It does not prove a new CRT or rank lemma, combine the `r=0` and `r=1`
layers, extend to `m>2`, or apply anything to PR `#763`.

## One fixed layer

Corollary `cor:capf-pma-johnson` in
`experimental/cap25_cap_v13_raw.tex` bounds a whole fixed
`(D_0,R_0)` layer.  Here

```text
|T| = M*ell = 12,
a   = sigma+d+1-r = 8,
d   = 4,
a^2-d|T| = 64-48 = 16,
floor(|T|(a-d)/(a^2-d|T|)) = 48/16 = 3.
```

Since the four-point core is wholly missed and no background point is
retained,

```text
D_0 = {0,1,2,3},
R_0 = empty,
binom(4,4)*binom(2,0) = 1.
```

The concrete-layer hypotheses are automatic for this frozen stratum.  The
evaluation set is the disjoint union

```text
Omega = Y disjoint-union {16,17} disjoint-union T,
Y     = {0,1,2,3}.
```

Here `d=4` forces `D_0=Y`, while `r=0` means that neither background point is
an agreement.  Thus every exact row has no agreement outside `T`, exactly as
required by `def:capf-concrete-sunflower`.  Since `Y\D_0` is empty, the
injection of `prop:capf-concrete-sunflower` is simply

```text
G_P = P-P_star,        deg G_P <= 4,
```

and listedness supplies at least `sigma+d+1-r=8` agreements with the one
auxiliary word `U_{D_0}` on `T`.  This is the direct bridge from every profile
cell below to the single fixed auxiliary layer; no support-pattern choice
changes `D_0`, `R_0`, or `U_{D_0}`.

Thus the entire exact `d=4,r=0` stratum represented by the frozen profile
ledger has size at most three.

## Exact shared scope

The profile generator records nonincreasing positive petal-hit multisets.
For `d=4,r=0`, listedness requires at least eight petal agreements.  With
three petals of size four, the following eleven cells are exhaustive and
disjoint:

| `t` | `a_i` | prior route | current charge |
|---:|---|---|---:|
| 2 | `(4,4)` | full petal | 57 |
| 3 | `(4,4,4)` | full petal | 19 |
| 3 | `(4,4,3)` | global Johnson | 228 |
| 3 | `(4,4,2)` | global Johnson | 342 |
| 3 | `(4,4,1)` | global Johnson | 228 |
| 3 | `(4,3,3)` | global Johnson | 912 |
| 3 | `(4,3,2)` | global Johnson | 2,736 |
| 3 | `(4,3,1)` | unresolved | 1,824 |
| 3 | `(4,2,2)` | unresolved | 2,052 |
| 3 | `(3,3,3)` | global Johnson | 23,104 |
| 3 | `(3,3,2)` | unresolved / carrier | 103,968 |

Their profile formulas have aggregate support-pattern multiplicity 794 and
current charge `135,470`.  This is not a census of 794 realized codewords or
explicit supports.  Their unresolved-route subtotal is `107,844`.

The banked shared-envelope bookkeeping keeps one charge of three on the
unresolved `(3,3,2)` carrier and gives the other ten cells zero incremental
charge:

```text
135,470 -> 3.
```

The zeroes are not standalone profile bounds.  They mean only that those ten
disjoint cells are already covered by the common fixed-layer envelope whose
single charge is carried on `(3,3,2)`.

## Banked ledger consequence

The exact certificate replay and fresh independent and cross-model reviews
bank the ledger change

```text
all-profile: 776,979 -> 641,512,
unresolved:  212,755 -> 104,914.
```

The unresolved subtotal follows the existing convention: the shared charge
of three remains attached to an original B11-unresolved row and is included
once.

The next largest unchanged unresolved cell is

```text
(ell,d,r,t,a_i) = (4,3,1,3,(3,2,1)),
(G2,GR)          = (3,4),
support patterns = 1,152,
charge           = 1,152*19 = 21,888.
```

Its auxiliary margin is zero, so it is a separate next obligation.

## Nonclaim: no cross-`r` aggregation

The fixed-layer corollary directly authorizes the conservative cap three for
`r=0`.  It does not by itself authorize replacing the separately banked
`r=1` cap 72 and this cap three by a common cap 36.  Such a saving would need
a separately stated cross-layer injection and coverage lemma, followed by a
fresh review.  No such saving is used here.

## Reproducibility and stop conditions

The ledger verifier must reconstruct the banked 41331 rows, select exactly
the eleven `d=4,r=0` cells, content-address the prior ledger and theorem
source, charge the envelope once, and reject at least:

- duplicate, missing, or foreign profile cells;
- a changed profile order or moved envelope carrier;
- a spurious background or restored-core layer factor;
- a non-strict Johnson margin;
- multiplication of three by patterns or profiles;
- a duplicate carrier or duplicate `+3` charge;
- accidental cross-`r` aggregation;
- drift in totals, the next-largest row, the prior ledger, the scope note, or
  theorem source;
- drift in the reviewed `banked=true` status.

The deterministic scope, layer identity, independent review, and cross-model
review all pass.  This payment is a separate stacked packet after #799; it is
not part of #799 and is not a global theorem.
