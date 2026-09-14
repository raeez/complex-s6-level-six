"""Exact matrices for the actual core maps and meridian surfaces."""
from itertools import combinations
import json
import platform

import sympy as s
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


def rows(matrix):
    return [[int(x) for x in row] for row in matrix.tolist()]


def exterior(matrix, degree):
    basis = list(combinations(range(matrix.rows), degree))
    return s.Matrix([[matrix.extract(r, c).det() for c in basis] for r in basis])


def smith(matrix):
    diagonal, left, right = [x.to_Matrix() for x in smith_normal_decomp(
        DomainMatrix.from_Matrix(matrix).convert_to(s.ZZ))]
    assert left * matrix * right == diagonal
    assert abs(left.det()) == abs(right.det()) == 1
    factors = [abs(int(diagonal[i, i])) for i in range(min(matrix.shape))
               if diagonal[i, i]]
    assert all(b % a == 0 for a, b in zip(factors, factors[1:]))
    return {"matrix": rows(matrix), "left": rows(left), "right": rows(right),
            "diagonal": rows(diagonal), "factors": factors}


T0 = s.Matrix([[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]])
T1 = s.Matrix([[-1,1,-1,2],[-1,0,-1,1],[1,1,2,-1],[0,0,0,1]])
Ti = (T0*T1).inv()
B = [s.Matrix([[0,-1,-1,4],[0,0,-1,2],[1,1,1,-6],[0,0,0,1]]),
     s.Matrix([[1,1,0,-1],[0,1,0,-1],[0,-1,1,3],[0,0,0,1]])]
P = [s.Matrix([[0,0,1],[1,0,0],[0,1,0]]),
     s.Matrix([[0,-1,-1],[1,0,0],[0,0,1]])]
U = [s.ones(3,1), s.Matrix([-1,-1,2])]
degree = [3,4]
fibrecov = [s.Matrix([[1,-1,1]]), s.Matrix([[2,1,-1]])]
alpha = s.Matrix([[1,0],[0,-1],[-1,1],[0,0]])
delta = s.Matrix([-2,-1,3,0])
assert alpha*s.Matrix([-2,1]) == delta
assert Ti*alpha == alpha and T0*delta == T1*delta == delta
assert B[0].inv()*T0*B[0] == s.diag(P[0],1)
assert B[1].inv()*T1*B[1] == s.diag(P[1].inv(),1)

adapted2 = [s.Matrix([[1,-1,0,1,0,0],[0,0,-1,0,-1,-1]]),
            s.Matrix([[2,1,0,-1,0,0],[0,0,0,0,0,-2]])]
adapted1 = [s.Matrix([[1,1,1,0],[0,0,0,3]]),
            s.Matrix([[0,0,1,0],[0,0,0,4]])]
F1 = [adapted1[i]*B[i].inv() for i in range(2)]
F2 = [adapted2[i]*exterior(B[i].inv(),2) for i in range(2)]
J1 = F1[0].col_join(-F1[1])
J2 = F2[0].col_join(-F2[1])
assert J1 == s.Matrix([[0,0,1,6],[0,0,0,3],[0,-1,-1,2],[0,0,0,-4]])
assert J2 == s.Matrix([[3,1,0,-2,0,0],[0,0,0,0,0,-1],
                       [-3,-1,0,2,-3,-1],[0,0,0,0,2,2]])
certificates = {"J1": smith(J1), "J2": smith(J2)}
core_records = []
for i in range(2):
    assert B[i].det() == 1 and P[i]**degree[i] == s.eye(3)
    assert P[i]*U[i] == U[i]
    assert B[i].inv()*delta == U[i].col_join(s.zeros(1,1))
    p2 = exterior(P[i],2)
    assert fibrecov[i]*p2 == fibrecov[i]
    norm = sum((P[i]**k for k in range(degree[i])),s.zeros(3))
    weight = s.Matrix([[1,1,1]]) if i == 0 else s.Matrix([[0,0,2]])
    assert norm == U[i]*weight
    certificates[f"core{i}_one"] = smith(P[i]-s.eye(3))
    certificates[f"core{i}_two"] = smith(p2-s.eye(3))
    core_records.append({"B": rows(B[i]), "B_inverse": rows(B[i].inv()),
        "P": rows(P[i]), "exterior_two": rows(p2), "invariant_vector": rows(U[i]),
        "norm": rows(norm), "fibre_covector": rows(fibrecov[i]),
        "F1": rows(F1[i]), "F2": rows(F2[i])})

c = s.Matrix([0,-1,0,1])
unimodular = J2[:,[1,4,5]].row_join(c)
assert unimodular.det() == 1
coordinates = unimodular.inv()*J2
assert coordinates[3,:] == s.zeros(1,6)
assert coordinates[:,[1,4,5]] == s.eye(4)[:,:3]
q = s.Matrix([[2,4,2,3]])
assert q*J2 == s.zeros(1,6) and q*c == s.Matrix([-1])
assert J1[:,0] == s.zeros(4,1) and J1.rank() == 3
assert certificates["J1"]["factors"] == [1,1,1]
assert certificates["J2"]["factors"] == [1,1,1]

chain_records = []
for j in range(2):
    a = alpha[:,j]
    a_next = T0.inv()*a
    assert T1.inv()*a_next == a
    r0, r1 = B[0].inv()[:3,:], B[1].inv()[:3,:]
    assert P[0].inv()*r0*a == r0*a_next
    assert P[1]*r1*a_next == r1*a
    connecting = a-a_next
    assert connecting == (j+1)*s.eye(4)[:,0]
    assert J1*connecting == s.zeros(4,1)
    # dQ0=f0(l_next-l_a), dQ1=f1(l_a-l_next), b=l_a-l_next.
    # Columns are coefficients of distinct normalized singular loop symbols.
    core_boundary0 = s.Matrix([[-1,1]])
    core_boundary1 = s.Matrix([[1,-1]])
    shifted_chain = s.Matrix([[1,-1]])
    assert core_boundary0+shifted_chain == s.zeros(1,2)
    assert core_boundary1-shifted_chain == s.zeros(1,2)
    chain_records.append({"a": rows(a), "after_inverse_zero": rows(a_next),
        "Q0_bottom": rows(r0*a), "Q0_top": rows(P[0].inv()*r0*a),
        "Q1_bottom": rows(r1*a_next), "Q1_top": rows(P[1]*r1*a_next),
        "connecting": rows(connecting),
        "loop_symbol_order": ["ell(a)","ell(T0_inverse*a)"],
        "core_zero_boundary_coefficients": rows(core_boundary0),
        "core_one_boundary_coefficients": rows(core_boundary1),
        "shifted_loop_chain_coefficients": rows(shifted_chain)})
attachment = s.Matrix([[1,2],[0,1]])
assert attachment*s.Matrix([-2,1]) == s.Matrix([0,1])
certificates["meridian_attachment"] = smith(attachment)
one = s.Matrix([[0,12,-1],[-1,0,0],[0,-1,0]])
assert one.det() == -1
certificates["cusp_degree_one"] = smith(one)
quotient1 = s.Matrix([[0,4,0,3]])
assert quotient1*J1 == s.zeros(1,4)
assert quotient1*s.Matrix([0,-1,0,1]) == s.Matrix([-1])
assert quotient1[:,:2]*F1[0] == s.Matrix([[0,0,0,12]])

print(json.dumps({"python": platform.python_version(), "sympy": s.__version__,
    "arithmetic": "Exact integers; rational inverses of unimodular matrices",
    "core_maps": core_records, "smith_certificates": certificates,
    "global_relation_basis": rows(unimodular),
    "global_relation_basis_inverse": rows(unimodular.inv()),
    "relations_in_integral_basis": rows(coordinates),
    "primitive_quotient_row": rows(q), "core_generator_c": rows(c),
    "actual_cusp_chains": chain_records, "delta": rows(delta),
    "meridian_attachment": rows(attachment),
    "results": {"H2_W": "Z^2", "meridian_image": "H2(W)",
        "meridian_kernel": "0", "meridian_determinant": 1,
        "H2_Y": "0 under the marked cusp hypotheses"},
    "scope": "Exact integral relation and geometric-square certificates; the topological comparison and core basis proofs are in meridian-tori.tex."}, indent=2))
