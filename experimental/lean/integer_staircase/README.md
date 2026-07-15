# Integer staircase Lean package

This stdlib-only Lean 4.14 package contains two independent finite
formalizations:

- `IntegerStaircase.lean` checks the identity-profile scale examples.
- `IntegerStaircase/F17AdjacentList.lean` checks the complete numerical
  `F₁₇` adjacent-list packet from
  `experimental/notes/frontier-adjacent/toy_complete_adjacent_list_staircase_v1.md`.

For the `F₁₇` row, Lean enumerates all `choose 16 10 = 8008` supports,
proves that the exact largest depth-two prefix fibre is `32` at prefix
`(0,0)`, reconstructs 32 pairwise-distinct degree-`< 8` codewords with
exact agreement 10 against `X^10`, computes the list denominator
`17^8 = 6975757441` and budget `12`, and checks the Johnson specialization
`L * 9 ≤ 64`, hence `L ≤ 7`.  The unconditional numeric window is therefore
`32 > 12 ≥ 7`. Lean also checks the average prefix floor `28`, null-prefix
excess `4`, the companion maximum `L(11) = 3`, and unique-decoding cap
`U(12) = 1` for both companion budgets `1` and `2`.

The exported semantic compiler deliberately exposes three standard inputs:
the prefix-witness lower bridge, the cross-multiplied all-words Johnson cell,
and antitonicity of the true list numerator.  The module does not disguise
those imported mathematical links as finite computation.

Build with:

```sh
cd experimental/lean/integer_staircase
lake build
```
