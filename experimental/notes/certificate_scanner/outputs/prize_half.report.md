# Proximity certificate scan

- Security target: `2^-128`
- Row: `n=2199023255552`, `k=1099511627776`, `rho=1/2`
- Fields: `q_gen=18446744073709551616`, `q_line=6277101735386680763835789423207666416102355444464034512896`, `q_chal=6277101735386680763835789423207666416102355444464034512896`, `q_base=18446744073709551616`
- Budgets: `floor(q_line/2^lambda)=18446744073709551616`, `floor(q_chal/2^lambda)=18446744073709551616`

## Agreement scans

| a | sigma | r | entropy margin bits | Qprof bits | line exact | list unique | combined verdict |
|---:|---:|---:|---:|---:|---|---|---|
| 1099511627777 | 1 | 1099511627775 | -2199023255467.177 | 1099511627754.675 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1099511628288 | 512 | 1099511627264 | -2199023222763.183 | 2147483631.174 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1099511628800 | 1024 | 1099511626752 | -2199023189995.177 | 1073741807.674 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1099512676352 | 1048576 | 1099510579200 | -2198956146665.740 | 1048564.674 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1116691496960 | 17179869184 | 1082331758592 | -1099124341494.390 | 59.669 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1466015503701 | 366503875925 | 733007751851 | 21436894164658.059 | 1.585 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNKNOWN_OR_CONDITIONAL |
| 1649267441664 | 549755813888 | 549755813888 | 33400352626446.375 | 0.000 | UNKNOWN outside r <= floor((n-k)/3) | PROVED exact list size 1 for every arity mu in high-agreement range | UNKNOWN_OR_CONDITIONAL |
| 1832519379627 | 733007751851 | 366503875925 | 45483081696650.211 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | UNKNOWN_OR_CONDITIONAL |
| 2199023254552 | 1099511626776 | 1000 | 70368744081193.398 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 2199023255542 | 1099511627766 | 10 | 70368744176635.789 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 2199023255551 | 1099511627775 | 1 | 70368744177559.008 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 2199023255552 | 1099511627776 | 0 | 70368744177664.000 | — | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |

## Paper D universal cap scan

- Status: PROVED_PAPERD_V6_CAP
- Active caps: 34
- Strongest active cap: `N=256`, gap `1/128`, delta cap `63/128`, margin `35.628` bits

## Notes

- `SAFE_BY_PROVED_UPPER_BOUND` means all included protocol terms have theorem-backed upper numerators below the target.
- `UNSAFE_BY_PROVED_LOWER_BOUND` means theorem-backed lower numerators already exceed the target.
- `UNKNOWN_OR_CONDITIONAL` means at least one consumed term is outside a proved range, or only a conditional Paper B/C assumption is enabled.
- The scanner does not prove extension-line MCA, arbitrary-word locator local limits, or aperiodic Hankel-pencil packing; it flags those gaps.
