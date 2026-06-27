# Proximity Certificate Scanner

This directory contains a standalone numerical scanner for the A/B/C/D +
`experiments.tex` reserve ledgers.

It is designed to answer: for a row

```text
C = RS[F,D,k],  |D| = n,
```

and a target `2^-lambda`, which ledgers are theorem-backed safe, theorem-backed
unsafe, or still unknown/conditional?

## What it implements

### Paper B / Paper C ledgers

- Generated-field entropy margin:

```text
(a-k) log2(q_gen) - log2 binom(n,a)
```

- Exact-divisibility quotient profile:

```text
Qprof(a,k)=max_{M | gcd(n,k), 1 <= a-k < M} log2 binom(n/M-1,k/M)
```

- Optional corrected-MCA conjectural ledger if enabled in config.

### Paper D universal cap

The scanner checks the divisor hypothesis from the universal cap theorem:

```text
N | n,
(n/N) | k,
(1-rho)N >= 3,
binom(N,rho N + 2) >= |B| (q/k + 1).
```

When active, it reports the corresponding cap

```text
delta* <= 1 - rho - 2/N
```

with status `DRAFT theorem: Paper D v5 cap under stated hypotheses; not peer reviewed`.

### experiments.tex high-agreement ledgers

For `r=n-a`, `R=n-k`:

```text
line/CA/projective exact: r+1       if r <= floor(R/3)
interleaved list exact: 1           if r <= floor(R/2)
degree-d curve envelope: <= d(r+1)  if r <= floor(R/(d+2))
```

The degree-`d` curve lower exactness is only marked exact when the multiplicative
subgroup split criterion holds.

### Paper C combined protocol ledger

The scanner composes included line, curve, and list terms and classifies the
sum as:

- `SAFE_BY_PROVED_UPPER_BOUND`
- `UNSAFE_BY_PROVED_LOWER_BOUND`
- `UNKNOWN_OR_CONDITIONAL`

## Usage

```bash
python certificate_scanner.py examples/f17_512.json \
  --json-out outputs/f17_512.report.json \
  --md-out outputs/f17_512.report.md \
  --pretty
```

```bash
python certificate_scanner.py examples/prize_rate_half_k2_40.json \
  --json-out outputs/prize_half.report.json \
  --md-out outputs/prize_half.report.md \
  --pretty
```

## Scope

This scanner does not prove:

- arbitrary-word locator local limits;
- all-line aperiodic Hankel-pencil packing;
- extension-line MCA;
- concrete deployed protocol soundness;
- protocol-specific curve sampler reductions.

It makes the theorem-backed ledgers numerically explicit and flags where the
remaining assumptions enter.
