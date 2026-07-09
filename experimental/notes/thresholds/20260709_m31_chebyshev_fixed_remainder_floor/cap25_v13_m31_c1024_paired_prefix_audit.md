# CAP25 v13 M31 c=1024 paired-prefix audit

Status: BANKABLE_LEMMA / ROUTE_CUT / EXACT_NEW_WALL / AUDIT.

This note records a narrow hostile audit of the M31 `c=1024` paired-prefix
packet following the M31 Chebyshev fixed-remainder floor audit. It is not a
proof of the deployed safe row, and it does not prove
`U(1116023) <= B*`.

## Board anchor

The live finite target remains the M31 list adjacent certificate:

```text
U(1116023) <= B* < L(1116022),
B* = 16777215.
```

The unsafe side is already exact. The safe side still requires the remaining
finite upper-ledger cells, with the primitive Q atom as the binding obstruction.

## Repaired c=1024 conventions

For the M31 multiplicative row, the `c=1024` quotient should be read with the
following conventions.

```text
Q1 = T_1024(D) = Z(T_2048),
Q1 = -Q1,
0 notin Q1,
T_2 fibers over Q1 are antipodal pairs.
```

The reserved planted point is `-eta`. The phrase "same at every dyadic scale"
must be range-qualified to the dyadic quotient levels actually used in the
M31 paired-prefix audit; it is not a terminal-scale statement.

The fixed `1911` remainder decomposition is also a convention of the
paired-prefix packet, not a consequence of the identity `1911 = 1024 + 887`
alone: the packet fixes one whole `T_1024` fiber plus an `887`-element subset
of the remaining quotient layer.

## Small-core rigidity

Let `core(S) = S \ (-S)` be the antipodal defect core after removing paired
points, and let the paired-prefix equations match the planted support through
the odd prefix window.

The hostile audits agree on the following bankable repair:

```text
CAP25-V13-M31-C1024-SMALL-CORE-RIGIDITY.
Under the paired-prefix conventions above, if a residual c=1024 support has
|core(S)| <= 65 and satisfies the paired-prefix equations, then its defect
core is the planted singleton {eta}. Hence its contribution is contained in
the factor-through c=2048 part of the paired-prefix fiber.
```

This is a local rigidity theorem for the paired-prefix packet. It is not a
global row-sharp Q estimate.

## First unresolved defect size

The first non-factor-through defect size is `67`. In that case the odd-core
part has the repaired divisor normal form

```text
F(Y) = (Y + eta) prod_{b in core(S)} (Y - b)
     = E(Y^2) + lambda Y,

D(Z) = E(Z)^2 - lambda^2 Z,
D(Z) | T_1024(2Z - 1),
D(eta^2) = 0,
lambda != 0.
```

This is only a necessary odd-core condition. It is not a full support count:
the full paired-prefix support still has to satisfy the even completion
equations, including the residual choice of `511` out of the `956` remaining
antipodal pairs.

The surviving named wall is therefore

```text
CAP25-V13-M31-T2048-EVEN-DEFECT-DIVISOR-COUNT.
```

Equivalently: either the degree-34 divisor wall has no admissible oriented
completion, or its admissible completions must be paid by a new finite cell.

## Payment audit

The `m=67` divisor family is not paid by the existing one-parameter
moving-root split-pencil cell. The printed `cor:bc-one-pencil` pays a fixed
one-parameter pencil after the required normalization; it does not pay the
union over degree-34 divisors `D(Z) | T_1024(2Z - 1)` with the orientation and
even-completion constraints still open.

Thus the correct outcome is not "c=1024 solved", but:

```text
small-core c=1024 defects collapse to the c=2048 factor-through floor;
the first live non-factor-through wall is the m=67 even-defect divisor count.
```

## Corrections to the raw packet

The following raw-packet phrasings should not be reused without repair.

- "Size-67 cores" means odd-defect core candidates, not full paired-prefix
  supports.
- "FT" means the factor-through part satisfying the paired-prefix equations,
  not the unrestricted factor-through family.
- The claimed checker file was not present in the packet and is not replayed
  by this note.
- The `1911 = 1024 + 887` identity does not itself force the whole
  `T_1024` quotient fiber; that is a packet convention.
- No additive stacking or co-location theorem is claimed.

## Nonclaims

This note does not prove any of the following.

- `U(1116023) <= B*`.
- The full M31 list adjacent safe row.
- Row-sharp Q.
- Emptiness of the `m=67` divisor wall.
- A count of the 32-even-completion layer.
- A payment of all `m >= 69` non-factor-through defects.

## Next exact checks

The next useful finite checks are:

1. prove or refute admissibility of the `m=67` divisor normal form;
2. if admissible, bound the 32-even-completion layer sharply enough for the
   M31 list budget;
3. extend the odd-core normal form to `m >= 69` and decide whether those
   defects have a common finite payment or need separate named cells.
