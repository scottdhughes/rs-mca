import Lake
open Lake DSL

package «l1_counterexample_regressions» where

@[default_target]
lean_lib «L1CounterexampleRegressions» where
  roots := #[`L1CounterexampleRegressions]
