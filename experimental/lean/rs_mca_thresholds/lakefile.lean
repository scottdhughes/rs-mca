import Lake

open Lake DSL

package rsMcaThresholds where

require GrandeFinale from "../grande_finale"
require AsymptoticRsMcaFrontiers from "../asymptotic_rs_mca_frontiers"

@[default_target]
lean_lib RsMcaThresholds where
  roots := #[`RsMcaThresholds]
