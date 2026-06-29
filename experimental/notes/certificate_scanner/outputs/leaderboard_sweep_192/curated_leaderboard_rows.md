# Curated new leaderboard rows

These are the highest-value rows from the scanner sweep: one direct proved tangent row for the existing `F_17^32` field, one conditional Paper D row for the same field, and four exact-prime prize-scale Paper D rows near `2^192`.

| id | status | rho | n | q bits | a | delta | eta gap | numerator lower | score bits |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `prime192-rho1_16-k2^40-paperD-N17592186044416` | PROVED_PAPERD_V6_CAP | 1/16 | 17592186044416 | 192.000 | 1099511627778 | 8246337208319/8796093022208 | 1/8796093022208 | 2854495385411919762116571938898990272765493481 | 87.000 |
| `prime192-rho1_8-k2^40-paperD-N8796093022208` | PROVED_PAPERD_V6_CAP | 1/8 | 8796093022208 | 192.000 | 1099511627778 | 3848290697215/4398046511104 | 1/4398046511104 | 2854495385411919762116571938898990272765493401 | 87.000 |
| `prime192-rho1_4-k2^40-paperD-N4398046511104` | PROVED_PAPERD_V6_CAP | 1/4 | 4398046511104 | 192.000 | 1099511627778 | 1649267441663/2199023255552 | 1/2199023255552 | 2854495385411919762116571938898990272765493265 | 87.000 |
| `prime192-rho1_2-k2^40-paperD-N2199023255552` | PROVED_PAPERD_V6_CAP | 1/2 | 2199023255552 | 192.000 | 1099511627778 | 549755813887/1099511627776 | 1/1099511627776 | 2854495385411919762116571938898990272765493266 | 87.000 |
| `F17^32-n512-k256-tangent-a257` | PROVED | 1/2 | 512 | 130.799 | 257 | 255/512 | 1/512 | 256 | 5.201 |
| `F17^32-n512-k256-paperD-N512` | PROVED_PAPERD_V6_CAP | 1/2 | 512 | 130.799 | 258 | 127/256 | 1/256 | 4624827333516537589539270111954982905 | 119.000 |

## Notes

- `eta gap` is `a/n - k/n`; smaller means closer to capacity.
- `score bits = 128 + log2(numerator_lower / q_line)`.
- `PROVED` means direct moving-root support-wise MCA lower floor, no CS25 import.
- `PROVED_PAPERD_V6_CAP` means the row instantiates the Paper D v6 universal cap and the scanner verified the divisor, binomial, and field ledgers.
- The prime192 rows use exact primes `q ≡ 1 mod n` found by the sweep, so the power-of-two subgroup-order gate is field-instantiated.
