# Board near-capacity cap rows (MCA leaderboard candidates)

Prime-field Paper D near-capacity caps for the four grand-challenge rates, filling the sparse low-rate MCA lanes (current best cap: rho=1/2 +119, rho in {1/4,1/8,1/16} +87).

| rho | k | n | delta_cap | field | score | vs board |
|---|---:|---:|---:|---|---:|---|
| 1/2 | 128 | 256 | 63/128 | ~2^125 | +120 | 119 -> +120 |
| 1/4 | 128 | 512 | 191/256 | ~2^206 | +120 | 87 -> +120 |
| 1/8 | 64 | 512 | 223/256 | ~2^139 | +121 | 87 -> +121 |
| 1/16 | 64 | 1024 | 479/512 | ~2^173 | +121 | 87 -> +121 |

All rows are smooth (power-of-two n), admissible (rho in {1/2,1/4,1/8,1/16}, k <= 2^40, |F| < 2^256, n <= q, subgroup exists), with k at or above the site first-grid k-floor. Scanner-confirmed Paper D cap; exact-integer error floor `2^128 * N_bad > q_line`; Proth-certified primes. Independently re-derived by `verify_board_cap_certificates.py`.
