import Lake
open Lake DSL

package «rank9_fixed_basis_exact_compiler» where

@[default_target]
lean_lib «Rank9FixedBasisExactCompiler» where
  roots := #[`Rank9FixedBasisExactCompiler]
