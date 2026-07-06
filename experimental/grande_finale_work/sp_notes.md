# Primitive Shift-Pair Work Notes

Status: AUDIT / partial PROVED package.

Files read:

- `experimental/grande_finale.tex`
- `experimental/cap25_cap_v13_raw.tex`, especially the active interface,
  prefix-collision rigidity, exact second-moment stratification, primitive
  shift-pair ledger, and active residual input
- `experimental/cap25_v13_missing_inputs_strategy.md`

## What the TeX packet proves

- Prefix-collision rigidity: two distinct equal-prefix `m`-sets differ in at
  least `w+1` positions on each side; equality is exactly a constant-shift
  split pair.
- Exact second-moment stratification: the `L^2` prefix-fiber mass is the
  diagonal plus ordered depth-`w` shift-pair strata.
- Anticode packing consequence: rigidity gives the unconditional
  `binom(n,m-w)/binom(m,w)` fiber cap.
- Quotient-pullback reduction: if both sides of a shift pair are pulled back at
  scale `c`, the pair descends to depth `ceil((w+1)/c)-1` on the quotient.
- Exact normalization: after first-match quotient assignment, primitive SP is
  precisely the normalized primitive contribution
  `sum_e P_e^prim / (binom(n,m) * Fbar)`.

## What remains conjectural

- The actual primitive census bound
  `sum_e P_e^prim <= R_SP(n) binom(n,m) Fbar`.
- The asymptotic target `R_SP(n)=e^{o(n)}` or an explicit polynomial loss usable
  only with reserve.
- The finite adjacent constants at the four deployed rows.  No finite row is
  proved by this packet.

## Overclaiming risks

- The exact second moment is not a worst-case max-fiber theorem.  Fixed moments
  cannot by themselves fit the adjacent margins.
- Constant-shift top-stratum pairs are classified structurally, not bounded
  primitively.  Quotient prototypes descend, but primitive `A,A-c` pairs remain
  open.
- Quotient-pullback pairs must be assigned by maximal common scale to avoid
  double counting.
- The packet treats the multiplicative coset setting.  Circle/Chebyshev
  transport would need a separate statement.

## Plausible next steps

- Classify or sharply bound primitive constant-shift pairs `A,A-c`.
- Extend the pair ledger to triple and higher collision ledgers.
- Search for an exchange-compression theorem forcing large primitive families
  into quotient, common-GCD, tangent, extension, or bounded SPI strata.
- Run small exact enumerations for primitive top-stratum pairs and quotient
  leakage before attempting deployed-row constants.
