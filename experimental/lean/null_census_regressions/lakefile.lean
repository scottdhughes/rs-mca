import Lake
open Lake DSL

package «null_census_regressions» where

@[default_target]
lean_lib «NullCensusRegressions» where
  roots := #[`NullCensusRegressions]
