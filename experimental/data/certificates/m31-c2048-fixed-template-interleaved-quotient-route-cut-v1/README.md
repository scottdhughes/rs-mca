# M31 c=2048 fixed-template interleaved quotient certificate

This packet is the source-bound successor to the whole-boundary 65-column
route cut in PR #1042.

## Certified results

- For one received word, one occupancy profile `(u,v)`, and one fixed
  partial agreement template, the complete exact-boundary family has size at
  most one when `v>=512`.
- When `v<=511`, putting `kappa=512-v`, the family has size at most

      floor(binomial(1023-u-v,kappa) / binomial(544-v,kappa)).

- The proof is an exact 2,048-component interleaved quotient-RS reduction:
  137 components have degree at most `511-v`, and 1,911 components have
  degree at most `510-v`.
- The cap fits `B*=16,777,215` on 25,767 of the 261,192 profiles. It exceeds
  budget on the other 235,425 profiles, including `(0,0)`.
- For every nonempty exact-boundary family, depth-`w` monic locator jets and
  depth-`w` normalized-cofactor reciprocal jets are in a fiber-preserving
  bijection.
- One symbolic deployed `(0,0)` fixed template has 15 exact codewords in 15
  distinct quotient, locator, and cofactor targets.
- One exact gluing construction has two same-profile `(0,0)` codewords with
  different partial templates.

The legal exact-boundary expression is therefore a sum over profiles,
partial templates, and attained normalized cofactor jets. The packet proves
no bound for that complete sum and moves no ledger atom.

The successor terminal is

    UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER

inside `HIGH_BOUNDARY_EXACT_CODEWORD` / `U_new`.

## Replay

From the repository root:

    python3 experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py --check
    python3 -O experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py --check
    python3 experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.py --tamper-selftest
    HOME=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_m31_c2048_fixed_template_interleaved_quotient_route_cut_v1.sage

The Python verifier recomputes every profile cap using exact integers, seals
all load-bearing sources, and rejects semantic mutations. Sage independently
replays the complete cap census, the free-module degree split, the reciprocal
cofactor bridge, the 15-target interpolation/factorization, and a complete
finite-field varying-template gluing fixture.

## Dependency state

Mechanical parent:

    PR #1042 head 464091b7a3b85048b6646dded6b7455e471cd0f7
    payload 1474cf06d7a058a010462ca06758df0576de9464441fa9245ddaf1b8e7d23245

At preparation, upstream `main` remained
`32a41660e3088eeeb15a16645330856794302ff0`. The packet is a separate stacked
successor and should integrate after #1042 or be manually replayed with its
exact feature commit.

## Nonclaims

- no complete exact-boundary or combined-allowance payment;
- no bound for the number of simultaneously attained partial templates;
- no one-target or four-target coalescence;
- no direct use of QR2 for general partial templates of degree at least 2048;
- no row-sharp Q, high-interior, extension, or remaining `U_new` payment;
- no full-row closure, endpoint, score, stable-paper, or Lean change.
