"""Compute integral cusp cones from the geometrically marked boundary map."""
from itertools import combinations
import json
import platform

import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


def rows(matrix):
    return [[int(value) for value in row] for row in matrix.tolist()]


def smith(matrix):
    diagonal, left, right = smith_normal_decomp(
        DomainMatrix.from_Matrix(matrix).convert_to(sp.ZZ))
    diagonal, left, right = [value.to_Matrix() for value in (diagonal, left, right)]
    assert left * matrix * right == diagonal
    assert abs(left.det()) == abs(right.det()) == 1
    factors = [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape))
               if diagonal[i, i]]
    assert all(b % a == 0 for a, b in zip(factors, factors[1:]))
    return {"matrix": rows(matrix), "shape": list(matrix.shape),
            "left": rows(left), "right": rows(right), "diagonal": rows(diagonal),
            "factors": factors, "rank": len(factors)}


def exterior(matrix, degree):
    indices = list(combinations(range(matrix.rows), degree))
    return sp.Matrix([[matrix.extract(r, c).det() for c in indices] for r in indices])


def homology(dimensions, differentials, degree):
    size = dimensions[degree]
    boundary = differentials.get(degree, sp.zeros(dimensions.get(degree - 1, 0), size))
    incoming = differentials.get(degree + 1, sp.zeros(size, dimensions.get(degree + 1, 0)))
    assert boundary * incoming == sp.zeros(boundary.rows, incoming.cols)
    boundary_certificate = smith(boundary)
    rank = boundary_certificate["rank"]
    right = sp.Matrix(boundary_certificate["right"]) if size else sp.zeros(0, 0)
    kernel_basis = right[:, rank:]
    incoming_coordinates = right.inv() * incoming
    assert incoming_coordinates[:rank, :] == sp.zeros(rank, incoming.cols)
    relation = incoming_coordinates[rank:, :]
    assert kernel_basis * relation == incoming
    relation_certificate = smith(relation)
    return {
        "kernel_basis": rows(kernel_basis),
        "incoming_in_kernel_basis": relation_certificate,
        "free_rank": kernel_basis.cols - relation_certificate["rank"],
        "torsion": [d for d in relation_certificate["factors"] if d > 1],
    }


T = sp.eye(4)
T[0, 2] = T[1, 3] = 1
L = sp.Matrix([[1, 0, 0, 0], [0, -1, 0, 0], [-1, 1, 1, 0], [0, 0, 0, 1]])
T0 = sp.Matrix([[0, -1, -1, 0], [1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
T1 = sp.Matrix([[-1, 1, -1, 2], [-1, 0, -1, 1], [1, 1, 2, -1], [0, 0, 0, 1]])
assert T0 * T1 * L * T * L.inv() == sp.eye(4)
P = {
    0: sp.ones(1, 1),
    1: sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1]]),
    2: sp.Matrix([[0, -1, 1, 1, -1, 0], [0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]),
    3: sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1]]),
    4: sp.ones(1, 1),
}
invariants = {
    0: sp.ones(1, 1),
    1: sp.eye(4)[:, :2],
    2: sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1],
                  [0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]]),
    3: sp.eye(4)[:, :2],
    4: sp.ones(1, 1),
}
invariant_checks = {}
for degree, basis in invariants.items():
    difference = exterior(T, degree) - sp.eye(basis.rows)
    assert difference * basis == sp.zeros(basis.rows, basis.cols)
    certificate = smith(basis)
    assert certificate["factors"] == [1] * basis.cols
    assert difference.rank() + basis.cols == basis.rows
    assert P[degree] * difference == sp.zeros(P[degree].rows, difference.cols)
    assert smith(P[degree])["factors"] == [1] * P[degree].rows
    invariant_checks[degree] = {"basis": certificate, "monodromy_difference": smith(difference)}

Q = sp.Matrix([[2, -1], [-1, 2]])
line_checks = []
for direction in [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1])]:
    endpoint = Q * direction / 2
    assert all(abs(value) <= 1 for value in [endpoint[0], endpoint[1], sum(endpoint)])
    assert (direction.T * endpoint)[0] == 1
    assert endpoint - Q * direction == -endpoint
    line_checks.append({"direction": rows(direction), "positive_endpoint":
                        [str(value) for value in endpoint], "seam_shift": rows(Q * direction)})

# The geometric proof identifies these cycles with the kernel of the actual k.
target_dimensions = dict(enumerate([1, 2, 4, 2, 1]))
boundary_dimensions = {}
K = {}
for degree in range(6):
    target_size = target_dimensions.get(degree, 0)
    invariant_size = invariants[degree - 1].cols if degree else 0
    boundary_dimensions[degree] = target_size + invariant_size
    K[degree] = sp.eye(target_size).row_join(sp.zeros(target_size, invariant_size))
assert list(boundary_dimensions.values()) == [1, 3, 6, 6, 3, 1]

cone_dimensions = {degree: target_dimensions.get(degree, 0)
                   + boundary_dimensions.get(degree - 1, 0) for degree in range(7)}
cone_differentials = {}
for degree in range(1, 7):
    matrix = sp.zeros(cone_dimensions[degree - 1], cone_dimensions[degree])
    offset = target_dimensions.get(degree, 0)
    matrix[:target_dimensions.get(degree - 1, 0), offset:] = K[degree - 1]
    cone_differentials[degree] = matrix
local_homology = {n: homology(cone_dimensions, cone_differentials, n) for n in range(7)}
assert [local_homology[n]["free_rank"] for n in range(7)] == [0, 0, 1, 2, 4, 2, 1]
assert all(not item["torsion"] for item in local_homology.values())

relations = sp.Matrix([[-1, 3, 0], [1, 0, 4]])
assert relations * sp.Matrix([12, 4, -3]) == sp.zeros(2, 1)
assert smith(relations)["factors"] == [1, 1]
monodromy_relations = (T0 - sp.eye(4)).row_join(T1 - sp.eye(4))
assert monodromy_relations[3, :] == sp.zeros(1, 8)
assert smith(monodromy_relations[:3, :])["factors"] == [1, 1, 1]

boundary_to_W = sp.Matrix([[0, 12, -1]])
boundary_to_Z = sp.Matrix([[1, 0, 0], [0, 1, 0]])
global_first_map = boundary_to_W.col_join(-boundary_to_Z)
assert global_first_map.det() == -1
assert global_first_map == sp.Matrix([[0, 12, -1], [-1, 0, 0], [0, -1, 0]])

# This presentation computes degrees zero and one by the cone exact sequence.
# It is not a claim to enumerate the higher-dimensional global complex.
first_dimensions = {0: 2, 1: 4, 2: 3}
first_d1 = sp.zeros(2, 4)
first_d1[:, 3] = sp.Matrix([1, -1])
first_d2 = global_first_map.col_join(sp.zeros(1, 3))
first_differentials = {1: first_d1, 2: first_d2}
first_homology = {n: homology(first_dimensions, first_differentials, n) for n in [0, 1]}
assert first_homology[0]["free_rank"] == 1
assert first_homology[1]["free_rank"] == 0
assert all(not item["torsion"] for item in first_homology.values())

result = {
    "scope": "All local relative cone homology and degrees zero and one of the specified global attachment. Higher global degrees are not computed.",
    "python": platform.python_version(), "sympy": sp.__version__,
    "invariant_cycles": invariant_checks,
    "geometric_line_seams": line_checks,
    "degree_two_specialization": rows(P[2]), "degree_three_specialization": rows(P[3]),
    "degree_two_specialization_e": rows(P[2] * exterior(L.inv(), 2)),
    "degree_three_specialization_e": rows(P[3] * exterior(L.inv(), 3)),
    "boundary_dimensions": boundary_dimensions,
    "cusp_homology_maps": {n: smith(matrix) for n, matrix in K.items()},
    "local_cone_dimensions": cone_dimensions,
    "local_cone_differentials": {n: smith(matrix) for n, matrix in cone_differentials.items()},
    "local_cone_homology": local_homology,
    "finite_abelian_relations": smith(relations),
    "global_first_map": smith(global_first_map),
    "first_presentation_dimensions": first_dimensions,
    "first_presentation_differentials": {n: smith(matrix) for n, matrix in first_differentials.items()},
    "first_global_homology": first_homology,
    "next_global_map": "Z^2 -> H_2(W), with columns b_infinity*[M(<alpha_1>)] and b_infinity*[M(<alpha_2>)]",
    "result": "Every exact chain, kernel-coordinate, Smith, invariant-lattice, and orientation-product assertion passed.",
}
print(json.dumps(result, indent=2))
