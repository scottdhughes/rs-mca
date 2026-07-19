#!/usr/bin/env python3
"""Verify the Route-D owner-typed forest-to-cell compiler v1.

The verifier checks a saturating finite compiler fixture, including the exact
all-maximal-minors owner gate, fixed-target/common-core preservation, rooted
forest edge-to-child bijection, complementary cell injections, and the final
add-back.  It also independently rebuilds the SHA-pinned raw F23 predecessor
forest and checks the sharp warning that 55 oriented edges do not inject into
2*23 cells.  No toy pivot is routed to the actual rank-drop owner.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Mapping, Sequence


P_DEPLOYED = 2_130_706_433
T_DEPLOYED = 67_472
DEPLOYED_CAPACITY = 143_763_024_447_376

SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "deletion_gap_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "deletion_gap_note_blob": "fdeabf0708cb8806feefae9322ed9002339332cf",
    "all_minors_adapter_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "all_minors_adapter_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
    "rank_owner_note_blob": "ddfce00907f34128b324a64041f4e0ec8957b7d3",
    "square_fold_commit": "f64e03a1215653eeafe3186df55269273d9f7653",
    "square_fold_note_blob": "301144d04458027131779907f7f74aa5a6682bf4",
    "square_fold_verifier_blob": "2507f09115c7eefbc86025dbaf204ea83c744283",
    "square_fold_lean_blob": "ab061b3c53a320fbb8881bab4e6fa8e573f83248",
    "complementary_charge_commit": "19c061ee094388e3261e8151e6c799826801ae12",
    "complementary_charge_note_blob": "c1bceae338a55c3f94381bf8f71d8b1584f05e95",
    "target_preserving_compatibility_commit": "fe34ed4dbbd4564d3f8af5c5de3fdf78c589e0d1",
    "target_preserving_compatibility_note_blob": "58c722cac2655aabf8ec887837607db7c79d6987",
    "target_preserving_compatibility_verifier_blob": "597524e7f639bd4abc90e12986c67eb84c7fce10",
    "target_preserving_compatibility_lean_blob": "14d2975fd4e9897748c863d7f7383bba104d51d4",
}

F23_ROWS_DIGEST = "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2"
F23_ALL_FOLD_DIGEST = "f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877"
F23_GRAPH_DIGEST = "620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5"


class CertificateError(RuntimeError):
    """Raised when any fail-closed certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def maximal_minors_2_by_3(matrix: Sequence[Sequence[int]], prime: int) -> tuple[int, int, int]:
    require(len(matrix) == 2 and all(len(row) == 3 for row in matrix),
            "owner matrix shape drift")
    return tuple(
        (matrix[0][left] * matrix[1][right]
         - matrix[0][right] * matrix[1][left]) % prime
        for left, right in itertools.combinations(range(3), 2)
    )


def all_maximal_minors_vanish(record: Mapping[str, object]) -> bool:
    matrix = record["matrix"]
    return all(value == 0 for value in maximal_minors_2_by_3(matrix, 7))


def positive_fixture_records() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    target = "zeta-fixed"
    core = (7,)
    carried = ("base-key", 11)
    rank_drop = [{
        "id": "rd0", "z": target, "G": core, "carried_base": carried, "actual_incidence": True,
        "matrix": ((1, 0, 1), (0, 0, 0)),
    }]
    endpoints = (
        ("u0", "s0"),
        ("u1", "s0"),
        ("u1", "s1"),
        ("u2", "s1"),
    )
    primitive = [{
        "id": f"d{index}", "z": target, "G": core, "carried_base": carried,
        "actual_incidence": True,
        "left": (target, core, carried, left), "right": (target, core, carried, right),
        "matrix": ((1, 0, index + 1), (0, 1, index + 2)),
    } for index, (left, right) in enumerate(endpoints)]
    routes = [{
        "source_id": "rd0", "owner": "DEEP_MCA_RANK_DROP",
        "route_count": 1, "z": target, "G": core, "carried_base": carried,
    }]
    return rank_drop, primitive, routes


def verify_owner_partition(rank_drop: Sequence[Mapping[str, object]],
                           primitive: Sequence[Mapping[str, object]],
                           routes: Sequence[Mapping[str, object]]) -> dict[str, object]:
    records = [*rank_drop, *primitive]
    require(len({record["id"] for record in records}) == len(records),
            "owner partition ids collided")
    require(all(record["actual_incidence"] is True for record in records),
            "nonactual record entered owner partition")
    require(len({record["z"] for record in records}) == 1,
            "owner partition crossed fixed targets")
    require(len({record["G"] for record in records}) == 1,
            "owner partition crossed literal cores")
    require(len({record["carried_base"] for record in records}) == 1,
            "owner partition crossed carried keys")
    for record in primitive:
        expected_prefix = (record["z"], record["G"], record["carried_base"])
        require(tuple(record["left"][:3]) == expected_prefix,
                "primitive left endpoint lost z, G, or carried keys")
        require(tuple(record["right"][:3]) == expected_prefix,
                "primitive right endpoint lost z, G, or carried keys")
    vanishing = [record for record in records if all_maximal_minors_vanish(record)]
    full_rank = [record for record in records if not all_maximal_minors_vanish(record)]
    require([record["id"] for record in vanishing]
            == [record["id"] for record in rank_drop],
            "all-minors vanishing partition drift")
    require([record["id"] for record in full_rank]
            == [record["id"] for record in primitive],
            "full-rank primitive partition drift")
    route_by_source = {route["source_id"]: route for route in routes}
    require(len(route_by_source) == len(routes) == len(vanishing),
            "rank-drop route multiplicity drift")
    for record in vanishing:
        require(record["id"] in route_by_source, "vanishing family left unrouted")
        route = route_by_source[record["id"]]
        require(route["owner"] == "DEEP_MCA_RANK_DROP" and route["route_count"] == 1,
                "rank-drop owner/count drift")
        require(route["z"] == record["z"] and route["G"] == record["G"]
                and route["carried_base"] == record["carried_base"],
                "rank-drop route lost fixed target, literal G, or carried keys")
    require(all(route["source_id"] not in {record["id"] for record in full_rank}
                for route in routes), "full-rank record routed to rank drop")
    return {
        "actual_records": len(records),
        "all_minors_vanishing": len(vanishing),
        "full_rank_primitive": len(full_rank),
        "rank_drop_routes": len(routes),
        "route_count_each": 1,
        "fixed_target_preserved": True,
        "literal_G_preserved": True,
        "carried_keys_preserved": True,
        "primitive_endpoint_prefixes_preserved": True,
    }


Node = tuple[str, object]


def orient_forest(edges: Sequence[Mapping[str, object]]) -> dict[str, object]:
    pairs = [(edge["left"], edge["right"]) for edge in edges]
    require(len(set(pairs)) == len(edges), "primitive edge endpoint map not injective")
    adjacency: dict[Node, list[tuple[Node, str]]] = defaultdict(list)
    for edge in edges:
        left, right = ("L", edge["left"]), ("R", edge["right"])
        adjacency[left].append((right, edge["id"]))
        adjacency[right].append((left, edge["id"]))
    unseen = set(adjacency)
    roots: list[Node] = []
    child_by_edge: dict[str, Node] = {}
    component_shapes: list[tuple[int, int]] = []
    while unseen:
        component_seed = min(unseen, key=repr)
        queue = deque([(component_seed, None)])
        seen_component: set[Node] = set()
        edge_ids: set[str] = set()
        roots.append(component_seed)
        while queue:
            vertex, parent_edge = queue.popleft()
            if vertex in seen_component:
                continue
            seen_component.add(vertex)
            unseen.discard(vertex)
            for neighbor, edge_id in adjacency[vertex]:
                edge_ids.add(edge_id)
                if edge_id == parent_edge:
                    continue
                if neighbor in seen_component:
                    raise CertificateError("primitive compatibility graph has a cycle")
                if edge_id in child_by_edge:
                    raise CertificateError("forest edge acquired two children")
                child_by_edge[edge_id] = neighbor
                queue.append((neighbor, edge_id))
        component_shapes.append((len(seen_component), len(edge_ids)))
    require(len(child_by_edge) == len(edges), "forest edge-to-child map not total")
    children = tuple(child_by_edge.values())
    require(len(set(children)) == len(children), "forest child map not injective")
    vertices = set(adjacency)
    require(set(children) == vertices - set(roots),
            "forest edge-to-nonroot bijection drift")
    return {
        "vertices": len(vertices), "edges": len(edges),
        "components": len(component_shapes), "roots": len(roots),
        "nonroot_vertices": len(children),
        "component_shapes": tuple(sorted(component_shapes)),
        "child_by_edge": child_by_edge,
        "root_nodes": tuple(sorted(roots, key=repr)),
    }


def verify_cell_charge(primitive: Sequence[Mapping[str, object]],
                       forest: Mapping[str, object],
                       generated_charge: Mapping[str, tuple[int, int]],
                       marked_cells: set[tuple[int, int]],
                       vertex_charge: Mapping[Node, tuple[int, int]],
                       t: int, p: int) -> dict[str, object]:
    universe = {(row, scalar) for row in range(t) for scalar in range(p)}
    require(marked_cells <= universe, "generated marked cells left universe")
    require(len(set(generated_charge.values())) == len(generated_charge),
            "generated support charge not injective")
    require(set(generated_charge.values()) <= marked_cells,
            "generated support charge left E_z")
    children = set(forest["child_by_edge"].values())
    require(set(vertex_charge) == children, "nonroot charge domain drift")
    require(len(set(vertex_charge.values())) == len(vertex_charge),
            "nonroot complement charge not injective")
    require(set(vertex_charge.values()) <= universe - marked_cells,
            "nonroot charge entered E_z")
    primitive_charge = {
        edge["id"]: vertex_charge[forest["child_by_edge"][edge["id"]]]
        for edge in primitive
    }
    require(len(set(primitive_charge.values())) == len(primitive_charge),
            "primitive composed charge not injective")
    combined = {("generated", key): value for key, value in generated_charge.items()}
    combined.update({("primitive", key): value for key, value in primitive_charge.items()})
    require(len(set(combined.values())) == len(combined),
            "complementary combined charge not injective")
    require(len(combined) <= t * p, "complementary cell capacity exceeded")
    return {
        "t": t, "p": p, "cell_capacity": t * p,
        "E_z_size": len(marked_cells),
        "generated_supports": len(generated_charge),
        "primitive_edges": len(primitive),
        "nonroot_vertices": len(vertex_charge),
        "complement_size": len(universe - marked_cells),
        "combined_supports": len(combined),
        "saturates_capacity": len(combined) == t * p,
        "generated_in_E_z": True,
        "primitive_in_complement": True,
        "combined_injective": True,
    }


def positive_fixture() -> dict[str, object]:
    rank_drop, primitive, routes = positive_fixture_records()
    records = [*rank_drop, *primitive]
    fixed_z = records[0]["z"]
    literal_G = records[0]["G"]
    carried_base = records[0]["carried_base"]
    require(fixed_z == "zeta-fixed", "positive fixture target pin drift")
    require(literal_G == (7,), "positive fixture literal G pin drift")
    require(carried_base == ("base-key", 11),
            "positive fixture carried-key pin drift")
    owner = verify_owner_partition(rank_drop, primitive, routes)
    require(len({edge["z"] for edge in primitive}) == 1,
            "primitive graph crossed fixed targets")
    require(len({edge["G"] for edge in primitive}) == 1,
            "primitive graph crossed literal cores")
    forest = orient_forest(primitive)
    require(forest["component_shapes"] == ((5, 4),),
            "positive fixture forest shape drift")
    generated_charge = {"g0": (0, 0), "g1": (0, 1)}
    marked_cells = {(0, 0), (0, 1)}
    nonroots = sorted(set(forest["child_by_edge"].values()), key=repr)
    complement = ((0, 2), (1, 0), (1, 1), (1, 2))
    vertex_charge = dict(zip(nonroots, complement, strict=True))
    charge = verify_cell_charge(
        primitive, forest, generated_charge, marked_cells, vertex_charge, 2, 3)
    return {
        "owner_partition": owner,
        "fixed_z": fixed_z, "literal_G": list(literal_G),
        "carried_base": list(carried_base),
        "forest": {
            "vertices": forest["vertices"], "edges": forest["edges"],
            "components": forest["components"], "roots": forest["roots"],
            "nonroot_vertices": forest["nonroot_vertices"],
            "component_shapes": [list(shape) for shape in forest["component_shapes"]],
            "edge_to_nonroot_bijection": True,
        },
        "charge": charge,
        "schema_fixture_only": True,
        "deployed_owner_claim": False,
    }


# Exact raw F23 predecessor replay from the SHA-pinned square-fold packet.
P23 = 23
DOMAIN23 = tuple(range(1, P23))


def add_weight(weight: dict[int, int], root: int, coefficient: int) -> None:
    value = weight.get(root, 0) + coefficient
    if value:
        weight[root] = value
    else:
        weight.pop(root, None)


def signed_weight(*terms: tuple[Iterable[int], int]) -> dict[int, int]:
    weight: dict[int, int] = {}
    for roots, coefficient in terms:
        for root in roots:
            add_weight(weight, root, coefficient)
    return weight


def locator_pair(roots: Sequence[int]) -> tuple[int, int, int]:
    left, right = sorted(roots)
    return ((left * right) % P23, (-(left + right)) % P23, 1)


def polynomial_roots(poly: Sequence[int]) -> tuple[int, ...]:
    return tuple(point for point in DOMAIN23
                 if sum(coefficient * pow(point, degree, P23)
                        for degree, coefficient in enumerate(poly)) % P23 == 0)


def weight_moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coefficient * pow(root, degree, P23)
               for root, coefficient in weight.items()) % P23


def projectively_primitive(weight: Mapping[int, int]) -> bool:
    for scalar in DOMAIN23:
        for sign in (1, -1):
            if (scalar, sign) == (1, 1):
                continue
            transformed: dict[int, int] = {}
            for root, coefficient in weight.items():
                add_weight(transformed, scalar * root % P23, sign * coefficient)
            if transformed == weight:
                return False
    return True


def square_fibers_23() -> tuple[tuple[int, int, int], ...]:
    seen: set[int] = set()
    fibers = []
    for root in DOMAIN23:
        image = root * root % P23
        if image in seen:
            continue
        seen.add(image)
        chosen = min(root, P23 - root)
        fibers.append((image, chosen, P23 - chosen))
    return tuple(sorted(fibers))


def fold_weight(weight: Mapping[int, int]) -> tuple[tuple[int, int, int], ...]:
    return tuple((image, weight.get(root, 0) + weight.get(negative, 0),
                  weight.get(root, 0) - weight.get(negative, 0))
                 for image, root, negative in square_fibers_23())


def reconstruct_folded(folded: Sequence[tuple[int, int, int]]) -> dict[int, int]:
    by_image = {image: (root, negative)
                for image, root, negative in square_fibers_23()}
    recovered: dict[int, int] = {}
    for image, even, odd in folded:
        require((even + odd) % 2 == 0 and (even - odd) % 2 == 0,
                "F23 fold parity drift")
        root, negative = by_image[image]
        add_weight(recovered, root, (even + odd) // 2)
        add_weight(recovered, negative, (even - odd) // 2)
    return recovered


def toy_pivot(weight: Mapping[int, int]) -> int:
    support = sorted(weight)
    require(len(support) >= 3, "F23 toy pivot support too small")
    columns = [(weight[root] % P23, weight[root] * root % P23,
                weight[root] * root * root % P23) for root in support[:3]]
    matrix = [[columns[column][row] for column in range(3)] for row in range(3)]
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P23


def f23_packets() -> list[dict[str, object]]:
    packets = []
    for side_a in itertools.combinations(DOMAIN23, 2):
        core = (10 - sum(side_a)) % P23
        if core == 0 or core in side_a:
            continue
        locator_u = locator_pair(side_a)
        locator_v = ((locator_u[0] - 17) % P23, locator_u[1], 1)
        side_r = polynomial_roots(locator_v)
        if len(side_r) != 2 or core in side_r:
            continue
        require(set(side_a).isdisjoint(side_r), "F23 packet sides meet")
        packets.append({
            "S": tuple(sorted((core, *side_a))),
            "S_prime": tuple(sorted((core, *side_r))),
            "G": (core,), "A": tuple(sorted(side_a)), "R": side_r,
            "U": locator_u,
        })
    packets.sort(key=lambda packet: (packet["S"], packet["S_prime"]))
    require(len(packets) == 75 and len({packet["U"] for packet in packets}) == 75,
            "F23 packet census drift")
    return packets


def f23_h_roots(representative: Mapping[str, object],
                packet: Mapping[str, object]) -> tuple[int, ...]:
    return tuple(sorted((set(representative["A"]) & set(packet["A"]))
                        | (set(representative["R"]) & set(packet["R"]))))


def f23_rows_digest(rows: Sequence[Mapping[str, object]]) -> str:
    serializable = [{
        "G": row["G"], "A": row["A"], "R": row["R"], "U": row["U"],
        "lambda_weight": row["lambda"], "mu3": row["mu3"],
        "support": row["support"], "profile": row["profile"],
    } for row in rows]
    return sha256_json(serializable)


def build_f23_rows() -> list[dict[str, object]]:
    packets = f23_packets()
    representative = packets[0]
    require(representative == {
        "S": (1, 2, 7), "S_prime": (1, 4, 5), "G": (1,),
        "A": (2, 7), "R": (4, 5), "U": (14, 14, 1),
    }, "F23 representative drift")
    a0, r0 = set(representative["A"]), set(representative["R"])
    rows = []
    h_one = extension = 0
    for packet_index, packet in enumerate(packets[1:], start=1):
        if f23_h_roots(representative, packet):
            continue
        h_one += 1
        core, side_a, side_r = set(packet["G"]), set(packet["A"]), set(packet["R"])
        mu = signed_weight((a0, 1), (side_r, 1), (r0, -1), (side_a, -1))
        require(all(weight_moment(mu, degree) == 0 for degree in range(3)),
                "F23 Rule-2 moment drift")
        mu3 = weight_moment(mu, 3)
        if mu3 == 0:
            extension += 1
            continue
        contact = signed_weight((a0 & core, 1), (r0 & core, -1))
        off_core = dict(mu)
        for root, coefficient in contact.items():
            add_weight(off_core, root, -coefficient)
        require(set(off_core).isdisjoint(core), "F23 literal G lost")
        folded = fold_weight(off_core)
        require(reconstruct_folded(folded) == off_core, "F23 fold reconstruction drift")
        require(len(off_core) >= 5 and projectively_primitive(mu)
                and projectively_primitive(off_core), "F23 primitive/full-rank drift")
        rows.append({
            "packet_index": packet_index,
            "G": packet["G"], "A": packet["A"], "R": packet["R"],
            "U": packet["U"],
            "profile": (len(a0 & core), len(r0 & core)),
            "mu": tuple(sorted(mu.items())), "lambda": tuple(sorted(off_core.items())),
            "even": tuple((image, even) for image, even, _ in folded if even),
            "odd": tuple((image, odd) for image, _, odd in folded if odd),
            "pivot": toy_pivot(off_core), "support": len(off_core), "mu3": mu3,
        })
    require(h_one == 56 and extension == 1 and len(rows) == 55,
            "F23 75/56/55 census drift")
    require(f23_rows_digest(rows) == F23_ROWS_DIGEST, "F23 predecessor row digest drift")
    require(sha256_json(rows) == F23_ALL_FOLD_DIGEST, "F23 fold-row digest drift")
    return rows


def f23_negative_control() -> dict[str, object]:
    rows = build_f23_rows()
    analogue_betas = {((sum(row["G"]) + sum(row["A"])) % P23,) for row in rows}
    require(analogue_betas == {(10,)}, "F23 fixed analogue beta drift")
    literal_core_histogram = Counter(row["G"] for row in rows)
    require(len(literal_core_histogram) == 21
            and max(literal_core_histogram.values()) == 5,
            "F23 fixed literal-core slice drift")
    serialized_edges = []
    adjacency: dict[Node, set[Node]] = defaultdict(set)
    for row in rows:
        left, right = (row["G"], row["even"]), (row["G"], row["odd"])
        serialized_edges.append((row["packet_index"], left, right))
        left_node, right_node = ("L", left), ("R", right)
        adjacency[left_node].add(right_node)
        adjacency[right_node].add(left_node)
    require(sha256_json(serialized_edges) == F23_GRAPH_DIGEST,
            "F23 ordered graph digest drift")
    left_vertices = {edge[1] for edge in serialized_edges}
    right_vertices = {edge[2] for edge in serialized_edges}
    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        queue = deque([next(iter(unseen))])
        while queue:
            vertex = queue.popleft()
            if vertex not in unseen:
                continue
            unseen.remove(vertex)
            queue.extend(adjacency[vertex])
    edge_count = len({(edge[1], edge[2]) for edge in serialized_edges})
    cycle_rank = edge_count - len(left_vertices) - len(right_vertices) + components
    left_degrees = Counter(len(adjacency[("L", vertex)]) for vertex in left_vertices)
    right_degrees = Counter(len(adjacency[("R", vertex)]) for vertex in right_vertices)
    require(edge_count == 55 and len(left_vertices) == 55 and len(right_vertices) == 52
            and components == 52 and cycle_rank == 0,
            "F23 raw forest census drift")
    require(left_degrees == {1: 55} and right_degrees == {1: 51, 4: 1},
            "F23 raw forest degree drift")
    require(len(left_vertices) == edge_count, "F23 left orientation not injective")
    require(edge_count > 2 * P23, "F23 raw cell-capacity obstruction disappeared")
    require(all(row["pivot"] != 0 for row in rows), "F23 toy pivot vanished")
    return {
        "field": "F_23", "analogue_t": 2, "cell_capacity": 2 * P23,
        "primitive_nonextension_edges": edge_count,
        "left_vertices": len(left_vertices), "right_vertices": len(right_vertices),
        "components": components, "cycle_rank": cycle_rank,
        "left_degree_histogram": {str(key): value for key, value in sorted(left_degrees.items())},
        "right_degree_histogram": {str(key): value for key, value in sorted(right_degrees.items())},
        "orientation_exists": True,
        "edge_count_exceeds_cell_capacity": edge_count - 2 * P23,
        "ordered_graph_sha256": sha256_json(serialized_edges),
        "all_fold_rows_sha256": sha256_json(rows),
        "raw_pre_first_match": True,
        "fixed_analogue_beta": list(next(iter(analogue_betas))),
        "fixed_analogue_beta_all_rows": True,
        "is_deployed_prefix_target": False,
        "incomplete_printed_key": "(r,c,U0,H,beta)",
        "printed_key_includes_literal_G": False,
        "distinct_literal_G": len(literal_core_histogram),
        "maximum_fixed_complete_base_fiber": max(literal_core_histogram.values()),
        "fixed_complete_base_exceeds_cell_capacity":
            max(literal_core_histogram.values()) > 2 * P23,
        "actual_incidence_constructed": False,
        "toy_pivot_routed": False,
        "rank_drop_routes": 0,
    }


def summarize() -> dict[str, object]:
    require(T_DEPLOYED * P_DEPLOYED == DEPLOYED_CAPACITY,
            "deployed capacity arithmetic drift")
    positive = positive_fixture()
    negative = f23_negative_control()
    return {
        "status": "PROVED",
        "theorem_id": "ROUTE_D_OWNER_TYPED_FOREST_TO_COMPLEMENTARY_CELL_COMPILER",
        "provenance": SOURCE_PINS,
        "deployed": {
            "t": T_DEPLOYED, "p": P_DEPLOYED,
            "capacity": DEPLOYED_CAPACITY,
            "conclusion": "|G_gen(z)|+|D_prim(z)| <= t*p",
            "application_status": "CONDITIONAL_ON_EXPLICIT_MISSING_INTERFACES",
        },
        "abstract_compiler": {
            "rank_drop_gate": "actual incidence and all maximal minors vanish",
            "rank_drop_route": "DEEP_MCA_RANK_DROP exactly once with z,G,carriedBase preserved",
            "primitive_domain": "fixed-z full-rank survivor edges",
            "edge_condition": "endpoint-pair injective compatibility forest",
            "forest_transfer": "one root per component; edges biject nonroot vertices",
            "cell_transfer": "generated injects into E_z; nonroots inject into complement",
            "addback": "complementary cell charge",
            "literal_common_core_preserved": True,
            "complete_carried_keys_preserved": True,
        },
        "positive_saturating_fixture": positive,
        "raw_f23_negative_control": negative,
        "missing_deployed_interfaces": [
            "exact named first-match deletion executor",
            "Route-D survivor-to-actual-incidence compiler",
            "post-deletion fixed-z compatibility-forest theorem",
            "generated-support injection into E_z",
            "nonroot marked-vertex injection into the cell complement",
        ],
        "nonclaims": {
            "deployed_certificate_proved": False,
            "toy_pivot_used_as_actual": False,
            "unrouted_actual_vanishing_family": False,
            "forbidden_shortcut_used": False,
        },
    }


EXPECTED_CERTIFICATE_SHA256 = "5c8f78389d70f8703c731c0c10000a2a899621a9cf69a1db5642dde8bba19406"


def validate(certificate: Mapping[str, object]) -> None:
    require(sha256_json(certificate) == EXPECTED_CERTIFICATE_SHA256,
            "certificate digest differs from fail-closed expected object")


def leaf_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaf_paths(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaf_paths(child, (*path, index))
    else:
        yield path


def mutate_leaf(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "!"
    raise CertificateError(f"unsupported leaf type {type(value).__name__}")


def expect_rejection(action) -> None:
    try:
        action()
    except CertificateError:
        return
    raise CertificateError("targeted tamper was accepted")


def targeted_tamper_selftest() -> int:
    rank_drop, primitive, routes = positive_fixture_records()
    records = [*rank_drop, *primitive]
    fixed_z = records[0]["z"]
    literal_G = records[0]["G"]
    carried_base = records[0]["carried_base"]
    require(fixed_z == "zeta-fixed", "positive fixture target pin drift")
    require(literal_G == (7,), "positive fixture literal G pin drift")
    require(carried_base == ("base-key", 11),
            "positive fixture carried-key pin drift")
    trials = 0

    broken_cycle = copy.deepcopy(primitive)
    broken_cycle.append({**broken_cycle[0], "id": "cycle", "left": primitive[3]["left"],
                         "right": primitive[0]["right"]})
    expect_rejection(lambda: orient_forest(broken_cycle)); trials += 1

    duplicate_edge = copy.deepcopy(primitive)
    duplicate_edge.append({**duplicate_edge[0], "id": "duplicate"})
    expect_rejection(lambda: orient_forest(duplicate_edge)); trials += 1

    expect_rejection(lambda: verify_owner_partition(rank_drop, primitive, [])); trials += 1

    bad_route = copy.deepcopy(routes)
    bad_route[0]["G"] = (8,)
    expect_rejection(lambda: verify_owner_partition(rank_drop, primitive, bad_route)); trials += 1
    for field, replacement in (("z", "other-z"), ("G", (8,)),
                               ("carried_base", ("other-key", 99))):
        crossed_rank_drop = copy.deepcopy(rank_drop)
        crossed_routes = copy.deepcopy(routes)
        crossed_rank_drop[0][field] = replacement
        crossed_routes[0][field] = replacement
        expect_rejection(lambda rd=crossed_rank_drop, rs=crossed_routes:
                         verify_owner_partition(rd, primitive, rs))
        trials += 1

    erased_prefix = copy.deepcopy(primitive)
    for index in (1, 2):
        erased_prefix[index]["left"] = erased_prefix[index]["left"][1:]
    require(orient_forest(erased_prefix)["component_shapes"] == ((5, 4),),
            "endpoint-erasure tamper changed forest shape")
    expect_rejection(lambda: verify_owner_partition(
        rank_drop, erased_prefix, routes)); trials += 1

    forest = orient_forest(primitive)
    nonroots = sorted(set(forest["child_by_edge"].values()), key=repr)
    duplicate_cells = {node: (1, 0) for node in nonroots}
    expect_rejection(lambda: verify_cell_charge(
        primitive, forest, {"g0": (0, 0)}, {(0, 0)}, duplicate_cells, 2, 3)); trials += 1
    return trials


def tamper_selftest(certificate: dict[str, object]) -> int:
    paths = tuple(leaf_paths(certificate))
    caught = 0
    for path in paths:
        broken = copy.deepcopy(certificate)
        cursor: object = broken
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        cursor[path[-1]] = mutate_leaf(cursor[path[-1]])  # type: ignore[index]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    for operation in ("extra", "missing"):
        broken = copy.deepcopy(certificate)
        if operation == "extra":
            broken["unexpected"] = True
        else:
            del broken["nonclaims"]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    require(caught == len(paths) + 2, "certificate tamper suite failed open")
    return caught + targeted_tamper_selftest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", action="store_true")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        print(f"TAMPER: PASS ({tamper_selftest(certificate)} mutations rejected)")
    else:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
