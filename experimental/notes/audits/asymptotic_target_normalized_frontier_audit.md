# Asymptotic target-normalized frontier audit

Date: 2026-07-10

## Verdict

`REPAIR / EXACT_NEW_WALL / PR_READY_NARROW`.

This note audits the target normalization in the compact asymptotic RS-MCA
frontier proof.  It is not a proof of any finite deployed adjacent row and it
does not discharge the C9, B1/image-normalization, or A6/add-back gaps currently
tracked by open PRs.

## Board anchor

Anchored at `origin/main` commit `eb42b82`.  The relevant sources are:

- `experimental/asymptotic_rs_mca.tex`, especially `thm:frontier` and its proof.
- `experimental/grande_finale.tex`, especially `lem:entropy-bookkeeping`,
  `thm:unsafe-envelope`, and `thm:asymptotic-rs-mca-closure-combined`.
- Open PRs `#435` and `#442`.

The duplicate check is:

- PR `#442` repairs the lower-side collision loss by rerouting through the
  collision-free identity-prefix floor.  It does not state the moving
  target-rate crossing.
- PR `#435` audits the in-paper proof and treats the entropy algebra as sound
  under the paper's fixed challenge normalization.  It does not add the
  target-normalized compiler theorem below.
- `grande_finale.tex` already contains the local target-numerator inequalities
  in `lem:entropy-bookkeeping`; the compact asymptotic statement still concludes
  with the zero-level crossing `g^*(rho,beta)`.

## Exact issue

The compact theorem currently states a target-independent frontier for every
target sequence with `log_2(1/eps_n)=O(n)` and fixed challenge normalization:

```tex
delta^*_{C_n}(eps_n) = 1 - rho - g^*(rho,beta) + o(1).
```

The proof then compares

```tex
log_2 barN_{n,a_n}
  = n(H_2(rho+g)-beta g)+o(n)
```

with zero.  This is correct only when the effective target numerator is
subexponential on the `n` scale.

For a general target numerator

```tex
B_n^* = floor(eps_n Q_n),
```

the relevant rate is

```tex
b_n = (1/n) log_2 max(1,B_n^*).
```

Exponential abundance of bad slopes is not enough to beat an exponential target
budget.  The correct comparison is with `b_n`, not with zero.

## Corrected compiler theorem

Let

```tex
K_n = k_n + O(1),    rho_n = K_n/n,
beta_n = log_2 |B_n|,
varphi_n(g) = H_2(rho_n+g) - beta_n g,
b_n = (1/n) log_2 max(1,B_n^*).
```

Assume the closed-ledger upper estimate and the identity-prefix lower estimate
hold uniformly near the crossing, with only `2^{o(n)}` losses and with the
separation hypotheses required by the lower route.  Define

```tex
g_n^dagger =
  sup { g in [0,1-rho_n] : varphi_n(g) >= b_n }.
```

If this last `b_n`-level crossing is isolated up to an `o(1)` corridor, then the
target-normalized frontier is

```tex
delta^*_{C_n}(eps_n) = 1 - rho_n - g_n^dagger + o(1).
```

Equivalently:

- the safe-side upper estimate needs `varphi_n(g) < b_n` with enough reserve to
  absorb the `o(n)` ledger overhead;
- the unsafe-side lower estimate needs `varphi_n(g) > b_n` with enough reserve
  to exceed `B_n^*`.

The target-independent formula with `g^*(rho,beta)` is recovered as the
corollary when

```tex
b_n -> 0,
```

that is, when the effective target numerator is subexponential.

## First false line / ambiguous line

The theorem-facing ambiguity is `experimental/asymptotic_rs_mca.tex:136`, where
the statement quantifies over target sequences with `log_2(1/eps_n)=O(n)` and
then concludes with the zero-level crossing.

The first proof inference that must be read with the extra `b_n -> 0` hypothesis
is `experimental/asymptotic_rs_mca.tex:295`, where the lower side says that
exponentially many bad slopes make the target fail.  The correct lower-side
criterion is `n varphi_n(g) > log_2 B_n^* + o(n)`.

## Relation to Grande Finale

`experimental/grande_finale.tex` already prints the local form of the correct
inequalities in `lem:entropy-bookkeeping`:

```tex
R(n) 2^{Xi_K(a)} <= B_n^*
```

and

```tex
2^{Xi_K(a)} > B_n^*.
```

The repair needed in the compact asymptotic proof is therefore a compiler-level
normalization: either explicitly restrict `thm:frontier` to the subexponential
target-numerator regime, or state the moving `b_n` crossing theorem.

## Nonclaims

This note does not claim:

- a proof of any finite deployed safe row;
- a discharge of `prob:row-sharp-q`;
- a discharge of C9 major-arc localization;
- a discharge of A6/first-match add-back;
- a replacement for the lower-side collision-free reroute in PR `#442`;
- a contradiction to PR `#435` under its fixed-normalization interpretation.

## Next exact action

For promotion, choose one of two theorem statements:

1. **Restricted compact frontier.**  Add the hypothesis
   `log_2 max(1,B_n^*)=o(n)` to the compact theorem and keep
   `g^*(rho,beta)`.
2. **Target-normalized frontier.**  Replace the zero-level crossing by
   `g_n^dagger` and keep the local inequalities from
   `lem:entropy-bookkeeping` as the compiler.

The second statement is more general and matches the local Grande Finale
bookkeeping, but the first is the smallest possible repair if the compact paper
only intends the fixed-normalization / subexponential-budget regime.
