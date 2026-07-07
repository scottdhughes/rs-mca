# Lean package for `experimental/grande_finale.tex`

This folder contains a Mathlib-based Lean formalization track for selected
self-contained parts of `experimental/grande_finale.tex`, the current
proof-audited final-input note for RS-MCA.

The Lean package is normalized as:

```text
package: RequestProject
library: RequestProject
toolchain: leanprover/lean4:v4.28.0
dependency: mathlib v4.28.0
```

The main modules are:

- `RequestProject.GrandeFinale`
- `RequestProject.BC`
- `RequestProject.SP`

Build command, in an environment where Mathlib dependencies are already
available:

```sh
cd experimental/lean/grande_finale
lake build
```

Codex did not run Lake during this source audit.

## Formalized Scope

The package formalizes theorem-level kernels from the note:

- integer budget conventions and first-match ledger counting;
- support-wise CA/MCA predicates, bad-slope numerators, monotonicity, and
  `eca <= emca`;
- Cauchy-Schwarz distinct-value counting and prefix-pigeonhole kernels;
- finite moment inequalities for the Q route;
- selected exact arithmetic anchors for the deployed MCA rows;
- BC-side slope elimination, saturation, line-ray bookkeeping, moving-root
  incidence bounds, and one-parameter pencil floor checks;
- SP-side quotient-pullback arithmetic, coefficient-scale detection,
  prefix-collision rigidity, second-moment ledger splitting, and the formal
  implication that a max-fiber Q theorem discharges the SP ledger.

## Not Formalized

This is not a complete proof of `grande_finale.tex`.

The dense-frontier safe side remains open. In particular, the package does not
prove the row-sharp Q atom theorem, does not prove the finite BC
chart-decomposition audit, and does not prove the adjacent deployed safe rows.
The large binomial derivations behind the packet numerators are also not
re-derived in Lean; the current arithmetic anchors check the integer comparisons
recorded by the packets.

The package also does not yet formalize every theorem-level local lemma in the
TeX note. For example, the composite-prefix power-map descent with multiplicity
`gcd(e,N)` is still TeX-only here and should be added before claiming full
coverage of the Q audit section.

## Audit Status

Status: `FORMALIZATION / AUDIT`.

During this repository pass, the source was inspected for obvious trust
placeholders. The scanned `.lean` files contain no `sorry`, `admit`, added
`axiom`, or `@[implemented_by]`. Several numeric anchors use `native_decide`,
which should be reviewed as executable arithmetic certificates before any claim
is advertised as Lean-certified.

Before relying on this package, run `lake build` in a controlled Mathlib-enabled
environment and inspect `#print axioms` for the declarations being cited.
