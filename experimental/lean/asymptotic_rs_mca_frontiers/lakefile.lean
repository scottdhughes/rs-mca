import Lake

open Lake DSL

package asymptoticRsMcaFrontiers where

require GrandeFinale from "../grande_finale"
require «cs25_cap_v12» from "../cs25_cap_v12"

@[default_target]
lean_lib AsymptoticRsMcaFrontiers where
  roots := #[`AsymptoticRsMcaFrontiers]
