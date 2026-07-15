# Regression-lock correspondence

Status: **PROVED / AUDIT** for the Lean wrappers below.  This is an interface
and build-preservation packet, not a new mathematical theorem.

| Regression declaration | Existing declaration locked | Scope preserved |
|---|---|---|
| `profileEnvelope_regression_lock` | `profile_frontier_bracket` | Conditional complete-profile first-safe bracket, with every compiler input explicit |
| `staircaseDeep_regression_lock` | `deep_regime_upper` | Deep bad-slope ceiling after receipt of a `DeepPairCertificate` for every enumerated pair |
| `effectiveClosure_regression_lock` | `prefixResidualClosure_to_directRC` | Prefix/residual chart to direct `RC`, conditional on the printed size inequalities |
| `addBack_regression_lock` | `addback_sufficiency` | Global add-back bound from `ProfileNonDegen` |

The companion declarations ending in `_fixture_lock` replay, respectively,
the GF(11^2) profile census, the dense-root exact staircase, the direct-RC
arithmetic toy, and the nondegenerate add-back example.

## Nonclaims

- No wrapper discharges a hypothesis of its source theorem.
- The deep finite-field recovery-to-ledger bridge remains outside Lean here.
- The effective residual compiler and complete profile comparison remain
  conditional where their source declarations are conditional.
- The exact fixtures are smoke certificates, not asymptotic proofs.

The audit criterion is a successful default package build plus inspection of
the printed axiom reports for all eight regression declarations.
