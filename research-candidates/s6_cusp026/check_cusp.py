"""Derive integral chains from the toric polygon and retain Smith certificates."""
from itertools import combinations
from pathlib import Path
import json
import platform

import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


def integer_rows(matrix):
    return [[int(value) for value in row] for row in matrix.tolist()]


def smith_certificate(matrix):
    domain_matrix = DomainMatrix.from_Matrix(matrix).convert_to(sp.ZZ)
    diagonal, left, right = smith_normal_decomp(domain_matrix)
    diagonal, left, right = [item.to_Matrix() for item in (diagonal, left, right)]
    assert left * matrix * right == diagonal
    assert abs(left.det()) == abs(right.det()) == 1
    factors = [abs(int(diagonal[i, i]))
               for i in range(min(diagonal.shape)) if diagonal[i, i]]
    assert all(b % a == 0 for a, b in zip(factors, factors[1:]))
    return {
        "matrix": integer_rows(matrix), "diagonal": integer_rows(diagonal),
        "left": integer_rows(left), "right": integer_rows(right),
        "factors": factors, "rank": len(factors),
        "identity": "left * matrix * right = diagonal",
    }


def exterior(matrix, degree):
    bases = list(combinations(range(matrix.rows), degree))
    return sp.Matrix([[matrix.extract(rows, columns).det()
                       for columns in bases] for rows in bases])


vertices = [sp.Matrix(v) for v in
            [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]]
Q = sp.Matrix([[2, -1], [-1, 2]])
assert Q.det() == 3
vertex_class = []
for vertex in vertices:
    match = [i for i, first in enumerate([vertices[0], vertices[1]])
             if all(value.q == 1 for value in Q.inv() * (vertex - first))]
    assert len(match) == 1
    vertex_class.append(match[0])
assert vertex_class == [0, 1, 0, 1, 0, 1]

# Each edge representative starts at A and ends at B.
edge_vertices = [(0, 1), (2, 1), (2, 3)]
edge_characters = [sp.Matrix([[-1, 1]]), sp.Matrix([[-1, 0]]),
                   sp.Matrix([[0, 1]])]
polygon_incidence = []
for i in range(6):
    start, end = vertices[i], vertices[(i + 1) % 6]
    matches = []
    for edge, (a, b) in enumerate(edge_vertices):
        for sign, first, last in [(1, a, b), (-1, b, a)]:
            displacement = Q.inv() * (start - vertices[first])
            if (all(value.q == 1 for value in displacement)
                    and end - vertices[last] == start - vertices[first]):
                matches.append((edge, sign, [int(v) for v in displacement]))
    assert len(matches) == 1
    polygon_incidence.append(matches[0])

base = {0: ["A", "B"], 1: ["e0", "e1", "e2"], 2: ["h"]}
base_d = {1: sp.zeros(2, 3), 2: sp.zeros(3, 1)}
for j, (first, last) in enumerate(edge_vertices):
    base_d[1][vertex_class[first], j] -= 1
    base_d[1][vertex_class[last], j] += 1
for edge, sign, displacement in polygon_incidence:
    base_d[2][edge, 0] += sign
assert base_d[1] * base_d[2] == sp.zeros(2, 1)

angular = [(), (0,), (1,), (0, 1)]
source = {n: [(p, b, a) for p, names in base.items() for b in names
              for a in angular if p + len(a) == n] for n in range(5)}
target = {n: [] for n in range(5)}
for p, names in base.items():
    fibre = [()] if p == 0 else ([(), ("eta",)] if p == 1 else angular)
    for b in names:
        for a in fibre:
            target[p + len(a)].append((p, b, a))

source_d, target_d, specialization = {}, {}, {}
for degree in range(1, 5):
    matrix = sp.zeros(len(source[degree - 1]), len(source[degree]))
    for column, (p, cell, angle) in enumerate(source[degree]):
        if p:
            for row_base, lower_cell in enumerate(base[p - 1]):
                coefficient = base_d[p][row_base, base[p].index(cell)]
                lower = (p - 1, lower_cell, angle)
                matrix[source[degree - 1].index(lower), column] += coefficient
    source_d[degree] = matrix
    target_d[degree] = sp.zeros(len(target[degree - 1]), len(target[degree]))
target_d[1] = base_d[1]
target_d[2][:, 3] = base_d[2]
for angle in range(2):
    for edge, sign, displacement in polygon_incidence:
        target_d[3][edge, angle] += sign * edge_characters[edge][angle]

for degree in range(5):
    matrix = sp.zeros(len(target[degree]), len(source[degree]))
    for column, (p, cell, angle) in enumerate(source[degree]):
        if not angle or p == 2:
            matrix[target[degree].index((p, cell, angle)), column] = 1
        elif p == 1 and len(angle) == 1:
            edge = base[1].index(cell)
            row = target[degree].index((p, cell, ("eta",)))
            matrix[row, column] = edge_characters[edge][angle[0]]
    specialization[degree] = matrix
    if degree:
        assert target_d[degree] * matrix == specialization[degree - 1] * source_d[degree]
    if degree >= 2:
        assert source_d[degree - 1] * source_d[degree] == sp.zeros(
            len(source[degree - 2]), len(source[degree]))
        assert target_d[degree - 1] * target_d[degree] == sp.zeros(
            len(target[degree - 2]), len(target[degree]))


def cell_cycle(degree, terms):
    result = sp.zeros(len(source[degree]), 1)
    for cell, coefficient in terms:
        result[source[degree].index(cell)] += coefficient
    return result


def beta_cycle(index, angle=(), sign=1):
    positive, negative = [("e1", "e0"), ("e0", "e2")][index]
    return [((1, positive, angle), sign), ((1, negative, angle), -sign)]


representatives = {
    0: [[((0, "A", ()), 1)]],
    1: [[((0, "A", (0,)), 1)], [((0, "A", (1,)), 1)],
        beta_cycle(0), beta_cycle(1)],
    2: [[((0, "A", (0, 1)), 1)], beta_cycle(0, (0,), -1),
        beta_cycle(1, (0,), -1), beta_cycle(0, (1,), -1),
        beta_cycle(1, (1,), -1), [((2, "h", ()), 1)]],
    3: [beta_cycle(0, (0, 1)), beta_cycle(1, (0, 1)),
        [((2, "h", (0,)), 1)], [((2, "h", (1,)), 1)]],
    4: [[((2, "h", (0, 1)), 1)]],
}
homology_specialization = {}
for degree, cycles in representatives.items():
    inclusion = sp.Matrix.hstack(*[cell_cycle(degree, cycle) for cycle in cycles])
    if degree:
        assert source_d[degree] * inclusion == sp.zeros(
            len(source[degree - 1]), len(cycles))
    image = specialization[degree] * inclusion
    if degree == 0:
        projection = sp.Matrix([[1, 1]])
    elif degree == 1:
        projection = sp.Matrix([[0, 1, 0], [0, 0, -1]])
    else:
        projection = sp.eye(len(target[degree]))
    homology_specialization[degree] = projection * image

# Independent integer homology reduction verifies the quotient bases.
def homology_data(cells, differential, degree):
    current = len(cells[degree])
    lower = len(cells[degree - 1]) if degree else 0
    upper = len(cells[degree + 1]) if degree < 4 else 0
    boundary = differential.get(degree, sp.zeros(lower, current))
    following = differential.get(degree + 1, sp.zeros(current, upper))
    diagonal, left, right = smith_normal_decomp(
        DomainMatrix.from_Matrix(boundary).convert_to(sp.ZZ))
    diagonal, right = diagonal.to_Matrix(), right.to_Matrix()
    rank = boundary.rank()
    incoming = (right.inv() * following)[rank:, :]
    assert (right.inv() * following)[:rank, :] == sp.zeros(rank, upper)
    certificate = smith_certificate(incoming)
    torsion = [d for d in certificate["factors"] if d > 1]
    return {"free_rank": current - rank - incoming.rank(), "torsion": torsion,
            "incoming_in_kernel_basis": certificate}


T = sp.eye(4)
T[0, 2] = T[1, 3] = 1
L = sp.Matrix([[1, 0, 0, 0], [0, -1, 0, 0], [-1, 1, 1, 0], [0, 0, 0, 1]])
monodromy_certificates, specialization_certificates = {}, {}
for degree, matrix in homology_specialization.items():
    monodromy_difference = exterior(T, degree) - sp.eye(matrix.cols)
    assert matrix * monodromy_difference == sp.zeros(matrix.rows, matrix.cols)
    pc = smith_certificate(matrix)
    nc = smith_certificate(monodromy_difference)
    assert pc["factors"] == [1] * matrix.rows
    assert nc["factors"] == [1] * (matrix.cols - matrix.rows)
    specialization_certificates[degree] = pc
    monodromy_certificates[degree] = nc

# Cone, edge, and seam checks derive from the lattice coordinates.
cone_determinants = []
for triangle in [[(0, 0), (1, 0), (1, 1)], [(0, 0), (1, 1), (0, 1)]]:
    cone = sp.Matrix.hstack(*[sp.Matrix([*vertex, 1]) for vertex in triangle])
    cone_determinants.append(int(cone.det()))
    assert cone.det() == 1
    assert (sp.Matrix([[0, 0, 1]]) * cone) == sp.ones(1, 3)

t, ratio = sp.symbols("t ratio", real=True)
seams = []
for edge in range(3):
    a, b = vertices[edge], vertices[edge + 1]
    tangent = b - a
    normal = sp.Matrix([tangent[1], -tangent[0]])
    normal = normal / sp.gcd(*normal)
    shift = Q * normal
    assert a - shift == vertices[(edge + 4) % 6]
    assert b - shift == vertices[(edge + 3) % 6]
    assert (edge_characters[edge] * normal)[0] == 0
    moment = (a + ratio * b) / (1 + ratio)
    opposite = (a - shift + ratio * (b - shift)) / (1 + ratio)
    assert sp.simplify(moment - opposite - shift) == sp.zeros(2, 1)
    assert -t * normal - t * Q.inv() * (-shift) == sp.zeros(2, 1)
    seams.append({"normal": list(map(int, normal)), "shift": list(map(int, shift))})

source_homology = {degree: homology_data(source, source_d, degree) for degree in range(5)}
target_homology = {degree: homology_data(target, target_d, degree) for degree in range(5)}
assert [target_homology[n]["free_rank"] for n in range(5)] == [1, 2, 4, 2, 1]
assert all(not item["torsion"] for item in target_homology.values())
result = {
    "scope": "The toric hexagon and its actual cellular quotient. The geometric comparison is proved in the accompanying mathematical text.",
    "python": platform.python_version(), "sympy": sp.__version__,
    "polygon_vertices": [list(map(int, v)) for v in vertices],
    "vertex_classes": vertex_class, "oriented_polygon_incidence": polygon_incidence,
    "seams": seams, "cone_determinants": cone_determinants,
    "source_cells": source, "target_cells": target,
    "source_boundary_certificates": {n: smith_certificate(m) for n, m in source_d.items()},
    "target_boundary_certificates": {n: smith_certificate(m) for n, m in target_d.items()},
    "source_homology": source_homology, "target_homology": target_homology,
    "cellular_specialization": {n: integer_rows(m) for n, m in specialization.items()},
    "specialization_certificates": specialization_certificates,
    "monodromy_difference_certificates": monodromy_certificates,
    "homology_specialization_e": {n: integer_rows(m * exterior(L.inv(), n))
                                  for n, m in homology_specialization.items()},
    "monodromy_alpha_beta": integer_rows(T), "monodromy_e": integer_rows(L * T * L.inv()),
    "result": "All exact assertions passed. Every Smith decomposition has verified unimodular left and right matrices.",
}
print(json.dumps(result, indent=2))
