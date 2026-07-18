#!/usr/bin/env sage
"""Independent GF(11^2) control for the tangent owner splice."""


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


F.<u> = GF(11^2)

# Repeated base and extension-valued tangent ratios.
ratios = [F(1), F(1), u, u, u + 1, u + 1]
epsilon_0 = [-eta for eta in ratios] + [F(0), F(0)]
epsilon_1 = [F(1) for _ in ratios] + [F(0), F(0)]
sigma = {
    index
    for index, pair in enumerate(zip(epsilon_0, epsilon_1))
    if pair != (F(0), F(0))
}
tangent_image = {
    -epsilon_0[index] / epsilon_1[index]
    for index in sigma
    if epsilon_1[index] != 0
}

require(len(sigma) == 6, "source support size drift")
require(tangent_image == {F(1), u, u + 1}, "deduplicated tangent image drift")
require(len(tangent_image) <= len(sigma), "tangent cap failed")

# The earlier owner removes u.  Tangent is applied before the later base owner.
bad_slopes = {F(1), u, u + 1, F(2), F(3)}
earlier_owner = {u}
incoming = bad_slopes.difference(earlier_owner)
tangent_cell = incoming.intersection(tangent_image)
outgoing = incoming.difference(tangent_cell)
base_slopes = {F(value) for value in range(11)}
later_base_cell = outgoing.intersection(base_slopes)

require(tangent_cell == {F(1), u + 1}, "first-match tangent cell drift")
require(outgoing == {F(2), F(3)}, "outgoing set difference drift")
require(later_base_cell == {F(2), F(3)}, "later base cell drift")
require(not tangent_cell.intersection(later_base_cell), "tangent/base double charge")

zero_witness_slopes = {F(1), u, u + 1}
require(zero_witness_slopes.issubset(tangent_image), "zero witness escaped tangent image")
require(not outgoing.intersection(zero_witness_slopes), "zero witness survived deletion")

# Restrict one complete selector and recompute affine rank from scratch.
selector_order = [F(1), u + 1, F(2), F(3)]
selector = {
    F(1): vector(F, [1, 0, 0, 0]),
    u + 1: vector(F, [0, 1, 0, 0]),
    F(2): vector(F, [0, 0, 1, 0]),
    F(3): vector(F, [0, 0, 0, 1]),
}
require(set(selector) == incoming, "incoming selector is incomplete")


def affine_rank(order):
    if len(order) <= 1:
        return 0
    anchor = selector[order[0]]
    return Matrix(F, [selector[eta] - anchor for eta in order[1:]]).rank()


incoming_rank = affine_rank(selector_order)
outgoing_order = [F(2), F(3)]
outgoing_rank = affine_rank(outgoing_order)
require(incoming_rank == 3, "incoming affine rank drift")
require(outgoing_rank == 1, "outgoing affine rank drift")
require(outgoing_rank <= incoming_rank, "rank increased after restriction")
require(affine_rank([]) == affine_rank([F(2)]) == 0, "small-family convention drift")

print("M1 tangent-owner GF(11^2) control: PASS")
print("  |Sigma|=6; |tangent image|=3; repeated ratios deduplicated")
print("  incoming affine rank=3; outgoing affine rank=1")
print("  tangent applied before residual base owner; zero pencils removed")
