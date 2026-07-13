import Lake
open Lake DSL

package «first_match_signed_gain» where

@[default_target]
lean_lib «FirstMatchSignedGain» where
  roots := #[`FirstMatchSignedGain]
