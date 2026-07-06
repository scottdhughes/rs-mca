# Adjacent-threshold pins -- board-format curation

Target `2^-128`. 28 admissible rows (4 grand-challenge rates x domain sizes + prize-scale k=2^40).
Each pin is Proth-certified and independently verified (`verify_adjacent_threshold_pins.py`).

## Table 1 -- LD_sw threshold pins (safe-edge / open-band)

Two-sided pin of `delta*` for the finite-slope support-wise line object, to `1/n`. `bad lower = B+1` is the exact UNSAFE numerator; `score = 128 + log2(bad lower) - log2(q_line)` (tiny by construction -- a tight pin sits at the boundary).

| id | rho | n | safe delta | unsafe delta | bad lower | q_line bits | pin score |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rho1_2-n2^9-k256` | 1/2 | 512 | 85/512 | 86/512 | 87 | 135 | 0.0167 |
| `rho1_2-n2^11-k1024` | 1/2 | 2048 | 341/2048 | 342/2048 | 343 | 137 | 0.0042 |
| `rho1_2-n2^13-k4096` | 1/2 | 8192 | 1365/8192 | 1366/8192 | 1367 | 139 | 0.0011 |
| `rho1_2-n2^15-k16384` | 1/2 | 32768 | 5461/32768 | 5462/32768 | 5463 | 141 | 0.0003 |
| `rho1_2-n2^17-k65536` | 1/2 | 131072 | 21845/131072 | 21846/131072 | 21847 | 143 | 0.0001 |
| `rho1_2-n2^19-k262144` | 1/2 | 524288 | 87381/524288 | 87382/524288 | 87383 | 145 | 0.0000 |
| `prize-rho1_2-k2^40` | 1/2 | 2199023255552 | 366503875925/2199023255552 | 366503875926/2199023255552 | 366503875927 | 167 | 0.0000 |
| `rho1_4-n2^9-k128` | 1/4 | 512 | 128/512 | 129/512 | 130 | 136 | 0.0111 |
| `rho1_4-n2^11-k512` | 1/4 | 2048 | 512/2048 | 513/2048 | 514 | 138 | 0.0028 |
| `rho1_4-n2^13-k2048` | 1/4 | 8192 | 2048/8192 | 2049/8192 | 2050 | 140 | 0.0007 |
| `rho1_4-n2^15-k8192` | 1/4 | 32768 | 8192/32768 | 8193/32768 | 8194 | 142 | 0.0002 |
| `rho1_4-n2^17-k32768` | 1/4 | 131072 | 32768/131072 | 32769/131072 | 32770 | 144 | 0.0000 |
| `rho1_4-n2^19-k131072` | 1/4 | 524288 | 131072/524288 | 131073/524288 | 131074 | 146 | 0.0000 |
| `prize-rho1_4-k2^40` | 1/4 | 4398046511104 | 1099511627776/4398046511104 | 1099511627777/4398046511104 | 1099511627778 | 169 | 0.0000 |
| `rho1_8-n2^9-k64` | 1/8 | 512 | 149/512 | 150/512 | 151 | 136 | 0.0096 |
| `rho1_8-n2^11-k256` | 1/8 | 2048 | 597/2048 | 598/2048 | 599 | 138 | 0.0024 |
| `rho1_8-n2^13-k1024` | 1/8 | 8192 | 2389/8192 | 2390/8192 | 2391 | 140 | 0.0006 |
| `rho1_8-n2^15-k4096` | 1/8 | 32768 | 9557/32768 | 9558/32768 | 9559 | 142 | 0.0002 |
| `rho1_8-n2^17-k16384` | 1/8 | 131072 | 38229/131072 | 38230/131072 | 38231 | 144 | 0.0000 |
| `rho1_8-n2^19-k65536` | 1/8 | 524288 | 152917/524288 | 152918/524288 | 152919 | 146 | 0.0000 |
| `prize-rho1_8-k2^40` | 1/8 | 8796093022208 | 2565527131477/8796093022208 | 2565527131478/8796093022208 | 2565527131479 | 170 | 0.0000 |
| `rho1_16-n2^9-k32` | 1/16 | 512 | 160/512 | 161/512 | 162 | 136 | 0.0089 |
| `rho1_16-n2^11-k128` | 1/16 | 2048 | 640/2048 | 641/2048 | 642 | 138 | 0.0022 |
| `rho1_16-n2^13-k512` | 1/16 | 8192 | 2560/8192 | 2561/8192 | 2562 | 140 | 0.0006 |
| `rho1_16-n2^15-k2048` | 1/16 | 32768 | 10240/32768 | 10241/32768 | 10242 | 142 | 0.0001 |
| `rho1_16-n2^17-k8192` | 1/16 | 131072 | 40960/131072 | 40961/131072 | 40962 | 144 | 0.0000 |
| `rho1_16-n2^19-k32768` | 1/16 | 524288 | 163840/524288 | 163841/524288 | 163842 | 146 | 0.0000 |
| `prize-rho1_16-k2^40` | 1/16 | 17592186044416 | 5497558138880/17592186044416 | 5497558138881/17592186044416 | 5497558138882 | 171 | 0.0000 |

## Table 2 -- complementary Paper D near-capacity caps

Committed universal cap `delta*_C <= 1 - rho - 2/n` on each engineered field (via `certificate_scanner.paper_d_cap`), where the divisor/binomial/subfield hypotheses pass.

| id | rho | n | Paper D cap `delta <= 1-rho-2/N` | hyp margin bits | status |
|---|---:|---:|---:|---:|---|
| `rho1_2-n2^9-k256` | 1/2 | 512 | 127/256 | 246.3 | PROVED_PAPERD_V8_CAP |
| `rho1_2-n2^11-k1024` | 1/2 | 2048 | 511/1024 | 1779.3 | PROVED_PAPERD_V8_CAP |
| `rho1_2-n2^13-k4096` | 1/2 | 8192 | 2047/4096 | 7920.3 | PROVED_PAPERD_V8_CAP |
| `rho1_2-n2^15-k16384` | 1/2 | 32768 | 8191/16384 | 32493.3 | PROVED_PAPERD_V8_CAP |
| `rho1_2-n2^17-k65536` | 1/2 | 131072 | 32767/65536 | 130794.3 | PROVED_PAPERD_V8_CAP |
| `rho1_2-n2^19-k262144` | 1/2 | 524288 | 131071/262144 | 524007.3 | PROVED_PAPERD_V8_CAP |
| `prize-rho1_2-k2^40` | 1/2 | 2199023255552 | 549755813887/1099511627776 | 2199023255238.4 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^9-k128` | 1/4 | 512 | 191/256 | 150.9 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^11-k512` | 1/4 | 2048 | 767/1024 | 1394.0 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^13-k2048` | 1/4 | 8192 | 3071/4096 | 6375.5 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^15-k8192` | 1/4 | 32768 | 12287/16384 | 26310.5 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^17-k32768` | 1/4 | 131072 | 49151/65536 | 106059.4 | PROVED_PAPERD_V8_CAP |
| `rho1_4-n2^19-k131072` | 1/4 | 524288 | 196607/262144 | 425063.9 | PROVED_PAPERD_V8_CAP |
| `prize-rho1_4-k2^40` | 1/4 | 4398046511104 | 1649267441663/2199023255552 | 3568038924498.6 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^9-k64` | 1/8 | 512 | 223/256 | 15.2 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^11-k256` | 1/8 | 2048 | 895/1024 | 847.1 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^13-k1024` | 1/8 | 8192 | 3583/4096 | 4183.8 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^15-k4096` | 1/8 | 32768 | 14335/16384 | 17539.5 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^17-k16384` | 1/8 | 131072 | 57343/65536 | 70971.0 | PROVED_PAPERD_V8_CAP |
| `rho1_8-n2^19-k65536` | 1/8 | 524288 | 229375/262144 | 284706.3 | PROVED_PAPERD_V8_CAP |
| `prize-rho1_8-k2^40` | 1/8 | 8796093022208 | 3848290697215/4398046511104 | 4781243405634.3 | PROVED_PAPERD_V8_CAP |
| `rho1_16-n2^9-k32` | 1/16 | 512 | - | - | NO_ACTIVE_PAPERD_V8_CAP |
| `rho1_16-n2^11-k128` | 1/16 | 2048 | 959/1024 | 426.1 | PROVED_PAPERD_V8_CAP |
| `rho1_16-n2^13-k512` | 1/16 | 8192 | 3839/4096 | 2495.5 | PROVED_PAPERD_V8_CAP |
| `rho1_16-n2^15-k2048` | 1/16 | 32768 | 15359/16384 | 10781.7 | PROVED_PAPERD_V8_CAP |
| `rho1_16-n2^17-k8192` | 1/16 | 131072 | 61439/65536 | 43935.7 | PROVED_PAPERD_V8_CAP |
| `rho1_16-n2^19-k32768` | 1/16 | 524288 | 245759/262144 | 176560.5 | PROVED_PAPERD_V8_CAP |
| `prize-rho1_16-k2^40` | 1/16 | 17592186044416 | 8246337208319/8796093022208 | 5933669602545.9 | PROVED_PAPERD_V8_CAP |

## Notes

- Pins are tight (margin ~0): they resolve the `LD_sw` line-object threshold to `1/n`, the board's safe-edge role -- not competitors for the score leaderboard.
- Paper D caps are one-sided near-capacity safe bounds with large margin, a different object (full MCA) than the pins (`LD_sw` line).
- `NO_ACTIVE_PAPERD_V8_CAP` rows are below the cap's binomial hypothesis at that field and carry the pin only.
