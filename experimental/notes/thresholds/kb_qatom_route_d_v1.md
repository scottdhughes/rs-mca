# KB-MCA Route-D support certificate v1

Status: `PARTIAL` — structural lemmas **PROVED**; conditional closure arithmetic **PROVED**; row-sharp Q atom / `U(1116048)<=B*` **OPEN**.

This packet attacks the single remaining support certificate that closes the KoalaBear MCA adjacent safe side at agreement `a+ = 1116048`.  It does not edit Papers A–D and does not claim the atom.

## Deployed row

```text
p = 2130706433 = 2^31-2^24+1
n = 2097152 = 2^21
k = 1048576 = 2^20
a+ = 1116048
j = n-a+ = 981104
t = a+-k = 67472
w = t-1 = 67471
B* = 274980728111395087
t*p = 143763024447376
```

## Conditional closure (PROVED arithmetic)

If for every primitive finite prefix target `z`, after first-match deletion,

```text
|G_gen_support(z)| + |D_full_rank_prim(z)|  <=  t*p
```

then with the imported exact-lift retained class bound `C(16,7)=11440`,

```text
t*p + 11440     = 143763024458816
target_floor    = 274836936291722953
integer slack   = 274693173267264137
slack bits      ≈ 10.9006675252
```

and the row-sharp Q-prefix atom inequality follows.  This replays and machine-checks the closure shape isolated in the #397 reductions packet.

## Proved lemmas

### Lemma A — fixed-core top-seam clique packing (PROVED)

For a fixed common core C of size j-(w+1), any family of top-seam mates sharing exactly that core has pairwise disjoint side sets of size e=w+1, hence size <= floor((n-|C|)/(w+1)).

Proof idea: top-seam pairs sharing exact core `C` have pairwise disjoint side sets of size `e=w+1=67472`; pack into `D\\C`.  Deployed packing ceiling `floor((n-|C|)/e) = 17`.

### Lemma B — free-coefficient filtration (PROVED)

Write Lambda_S = X^j + z_1 X^{j-1}+...+z_w X^{j-w} + a_{w+1} X^{j-w-1}+.... For fixed z=(z_1..z_w), partition Fib_w(z) by a_{w+1} in F_p. Each block is a fiber of the depth-(w+1) prefix map. Hence |Fib_w(z)| <= p * max_alpha |Fib_{w+1}(z||alpha)|.

Consequence: the atom holds if the depth-`(w+1)` max fiber is at most `128988645` (≈ `2^26.94`).  The admissible multiplier `kappa` is **self-similar** under depth shift (Lemma C), so this is not an automatic easing.

### Lemma C — kappa depth self-similarity (PROVED)

For the full-fiber form of the atom, the admissible multiplier kappa = floor(B_rem * p^w / C(n,j)) is unchanged when the prefix depth increases by 1 and the target/average are both divided by p.

### Sufficient support budgets that fit under the target (PROVED arithmetic)

| budget | value | slack bits (with +11440) |
|---|---:|---:|
| `t*p` | 143763024447376 | 10.9007 |
| `w*p` | 143760893740943 | 10.9007 |
| `n*p` | 4468415257378816 | 5.9427 |

| `p^2` alone | 4539909903627583489 | **does not fit** (gap 4.0460 bits) |

## Remaining open certificate

For every primitive finite prefix target z at KB-MCA a=1116048, after first-match deletion of generated_field / quotient_planted / sparse_pade_hankel / m1_window_shadow / rank_drop_pivot / bc_chart / sp_shift_pair / extension_slope, |G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p = 143763024447376.

Equivalent finite forms:

- **E1_additive_support**: |G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p
- **E2_marked_incidence_injection**: Residual supports inject (controlled mult <=1 after first-match) into a label space of size <= t*p, e.g. {0..t-1} x F_p or marked-incidence keys.
- **E3_large_folding_defect_transfer**: Every large signed folding defect satisfying the odd prefix equations is quotient-descended, sparse/Pade-Hankel, M1/window-shadow, rank-drop with printed pivot cost, generated-field support-paid, or lies in a primitive full-rank defect stratum of mass <= t*p.
- **E4_mu1_ceiling**: max fiber at depth w+1 is <= 128988645 (closes full N_w without additive residual split; kappa-self-similar so not obviously easier).
- **E5_np_injection**: Residual supports inject into D x F_p (size n*p) after first-match; slack ~5.94 bits with retained lift.

Falsifier: Exhibit a primitive residual leaf at a finite prefix target z with support mass > t*p after the named first-match deletions, or a full prefix fiber larger than target_floor.

## Dead ends (do not re-grind)

- lift-class keep-one payment (PR #417 refuted)
- r=2 / CS / Plancherel alone (pw2 concentration floor)
- absolute-value dual character sums (PR #398 barrier map)
- raw Delsarte distance packing (Gilbert gap ~1.37e6 bits)

## Toy suite

The verifier enumerates small dyadic rows and checks:

1. free-coeff filtration numerics,
2. top-seam constant-shift normal form on sampled edges,
3. fixed-core side-set packing.

All rows in the suite pass (see JSON).

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v1.py
python3 experimental/scripts/verify_kb_qatom_route_d_v1.py --check
```

Zero-arg, stdlib-only.  Exit 0 = all gates green.

## Non-claims

- Does not prove `U(1116048) <= B*`.
- Does not prove `prob:row-sharp-q` / `def:q-row-atom`.
- Does not pay generated-field **support** multiplicity (only image cells).
- Does not refute or prove the entropy–subfield envelope.

## Next attack steps (ordered)

1. Prove a support-level injection of the primitive residual into a space of size    `<= n*p` or `<= t*p` (forms E2/E5), using marked incidence + first-match leaves.
2. Or bound the large signed folding-defect stratum (form E3 / classical Route D).
3. Or bound depth-`(w+1)` max fibers by `128988645` (form E4) — kappa-self-similar.
4. Any success immediately upgrades this packet's conditional closure into an atom proof.

