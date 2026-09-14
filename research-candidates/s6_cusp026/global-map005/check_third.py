"""Exact degree-three maps, prism boundaries, and integral relation certificates."""
from itertools import combinations
import json
import platform
import sympy as s
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


def serialize(matrix):
    return [[int(x) if x.q == 1 else str(x) for x in row] for row in matrix.tolist()]


def ext(matrix, degree):
    r = list(combinations(range(matrix.rows), degree))
    c = list(combinations(range(matrix.cols), degree))
    return s.Matrix([[matrix.extract(i,j).det() for j in c] for i in r])


def smith(matrix):
    diagonal, left, right = [x.to_Matrix() for x in smith_normal_decomp(
        DomainMatrix.from_Matrix(matrix).convert_to(s.ZZ))]
    assert left*matrix*right == diagonal
    assert abs(left.det()) == abs(right.det()) == 1
    factors = [abs(int(diagonal[i,i])) for i in range(min(matrix.shape)) if diagonal[i,i]]
    assert all(b % a == 0 for a,b in zip(factors,factors[1:]))
    return dict(matrix=serialize(matrix),left=serialize(left),right=serialize(right),
                diagonal=serialize(diagonal),factors=factors)


T0 = s.Matrix([[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]])
T1 = s.Matrix([[-1,1,-1,2],[-1,0,-1,1],[1,1,2,-1],[0,0,0,1]])
Ti = (T0*T1).inv()
B = [s.Matrix([[0,-1,-1,4],[0,0,-1,2],[1,1,1,-6],[0,0,0,1]]),
     s.Matrix([[1,1,0,-1],[0,1,0,-1],[0,-1,1,3],[0,0,0,1]])]
P = [s.Matrix([[0,0,1],[1,0,0],[0,1,0]]),
     s.Matrix([[0,-1,-1],[1,0,0],[0,0,1]])]
R = [b.inv()[:3,:] for b in B]
omega = [s.Matrix([[1,-1,1]]),s.Matrix([[2,1,-1]])]
w = [s.Matrix([1,-1,1]),s.Matrix([1,0,0])]
d = [3,4]
certificates = {}
core_records = []
adapted3 = [s.Matrix([[1,0,0,0],[0,1,-1,1]]),
            s.Matrix([[1,0,0,0],[0,4,2,-2]])]
F3 = [adapted3[i]*ext(B[i].inv(),3) for i in range(2)]
for i in range(2):
    p2 = ext(P[i],2)
    assert p2*w[i] == w[i]
    norm = sum((p2**j for j in range(d[i])),s.zeros(3))
    weights = omega[i] if i == 0 else 2*omega[i]
    assert norm == w[i]*weights
    assert omega[i]*p2 == omega[i]
    certificates[f"core{i}_invariant_bivector"] = smith(p2-s.eye(3))
    core_records.append(dict(P=serialize(P[i]),B=serialize(B[i]),R=serialize(R[i]),
        exterior_square=serialize(p2),norm=serialize(norm),invariant_plane=serialize(w[i]),
        vertical_form=serialize(omega[i]),plane_area=serialize(omega[i]*w[i]),
        actual_fibre_three_map=serialize(F3[i])))
assert R[0]*T0.inv() == P[0].inv()*R[0]
assert R[1]*T1.inv() == P[1]*R[1]
assert T0[3,:] == T1[3,:] == s.Matrix([[0,0,0,1]])

J3 = F3[0].col_join(-F3[1])
assert J3 == s.Matrix([[1,6,2,-4],[0,3,1,-2],[-1,3,1,-1],[0,-6,-2,4]])
c = s.Matrix([0,0,0,1])
U = J3[:,[0,2,3]].row_join(c)
assert U.det() == 1
Ucoordinates = U.inv()*J3
assert Ucoordinates == s.Matrix([[1,0,0,0],[0,3,1,0],[0,0,0,1],[0,0,0,0]])
quotient = s.Matrix([[0,2,0,1]])
assert quotient*J3 == s.zeros(1,4) and quotient*c == s.Matrix([1])
certificates["J3"] = smith(J3)

J2 = s.Matrix([[3,1,0,-2,0,0],[0,0,0,0,0,-1],
               [-3,-1,0,2,-3,-1],[0,0,0,0,2,2]])
L = s.Matrix([[1,0,0,0],[0,-1,0,0],[-1,1,1,0],[0,0,0,1]])
alpha1,alpha2,beta1,beta2 = [L[:,i] for i in range(4)]
planes = [alpha1.row_join(alpha2),alpha1.row_join(beta1),
          alpha2.row_join(beta2),(alpha1+alpha2).row_join(beta1+beta2)]
V = s.Matrix.hstack(*[ext(v,2) for v in planes])
assert V == s.Matrix([[-1,0,0,0],[1,1,0,1],[0,0,0,1],
                       [-1,0,0,-1],[0,0,-1,-1],[0,0,1,0]])
infinity2 = ext(Ti,2)
assert infinity2*V == V
assert V.rank()+ (infinity2-s.eye(6)).rank() == 6
certificates["invariant_surface_basis"] = smith(V)
surface_records = []
for i,plane in enumerate(planes):
    restricted = s.eye(2) if i == 0 else s.Matrix([[1,1],[0,1]])
    assert Ti*plane == plane*restricted
    assert smith(plane)["factors"] == [1,1]
    assert R[0]*T0.inv()*plane == P[0].inv()*R[0]*plane
    assert R[1]*T1.inv()*T0.inv()*plane == R[1]*Ti*plane
    surface_records.append(dict(plane=serialize(plane),bivector=serialize(V[:,i]),
        restricted_monodromy=serialize(restricted),
        inverse_zero_surface=serialize(T0.inv()*plane)))

D = (s.eye(6)-ext(T0.inv(),2))*V
assert D == s.Matrix([[-1,0,0,-1],[3,2,0,3],[0,0,2,3],
                      [0,1,0,0],[0,0,0,0],[0,0,0,0]])
K = s.Matrix.hstack(D[:,0],D[:,1],D[:,2]-D[:,3])
assert J2*K == s.zeros(4,3)
assert K.extract([0,2,3],[0,1,2]).det() == -1
assert K.cols + J2.rank() == 6
r = s.Matrix([-2,0,-3,2])
assert D*r == s.zeros(6,1)
E = s.eye(4)
domain_basis = s.Matrix.hstack(E[:,0],E[:,1],E[:,2]-E[:,3],r)
assert domain_basis.det() == -1
assert D*domain_basis == K.row_join(s.zeros(6,1))
certificates["J2"] = smith(J2)
certificates["connecting"] = smith(D)
certificates["integral_kernel_basis"] = smith(K)
certificates["source_relation_basis"] = smith(domain_basis)

# Literal prism boundaries use independent surface-chain symbols u, u_minus, Tu.
# d a = Tu-u. Cone cycle is (Q0, Q1-f1 a, u-u_minus).
boundary_q0 = s.Matrix([[-1,1,0]])
boundary_q1 = s.Matrix([[0,-1,1]])
boundary_a = s.Matrix([[-1,0,1]])
boundary_shifted = s.Matrix([[1,-1,0]])
assert boundary_q0+boundary_shifted == s.zeros(1,3)
assert boundary_q1-boundary_a-boundary_shifted == s.zeros(1,3)

theta0_pullback = 2*adapted3[0][1,:]*ext(B[0].inv(),3)
theta1_pullback = adapted3[1][1,:]*ext(B[1].inv(),3)
eta = s.Matrix([[0,6,2,-4]])
assert theta0_pullback == theta1_pullback == eta
evaluation = -s.Rational(2,3)*omega[0]*ext(R[0],2)+s.Rational(1,2)*omega[1]*ext(R[1]*T0.inv(),2)
assert evaluation == s.Matrix([[-s.Rational(1,2),-s.Rational(1,6),-s.Rational(3,2),s.Rational(1,3),0,-1]])
values = evaluation*V
assert values == s.Matrix([[0,-s.Rational(1,6),-1,-2]])
assert values*r == s.Matrix([-1])
assert eta*ext(L,3) == s.Matrix([[0,0,2,4]])

M = s.Matrix([[1,0,-2,-2],[0,1,0,0],[0,0,-2,-3],[0,0,1,1]])
assert K*M[:3,:] == D
assert M*r == s.Matrix([0,0,0,-1])
assert M.det() == 1
full = s.zeros(6)
full[:4,:4] = M
full[3,4], full[3,5] = 2,4
full[4,4], full[5,5] = -1,-1
assert full.det() == 1
certificates["meridian_matrix"] = smith(M)
certificates["full_degree_three"] = smith(full)
assert certificates["full_degree_three"]["factors"] == [1]*6

# The prior degree-two injection uses the same actual relation matrix.
c2 = s.Matrix([0,-1,0,1])
assert J2[:,[1,4,5]].row_join(c2).det() == 1
assert (s.eye(4)-T0.inv())*L[:,:2] == s.Matrix([[1,2],[0,0],[0,0],[0,0]])
delta = L[:,1]-2*L[:,0]
assert T0*delta == T1*delta == delta

print(json.dumps(dict(python=platform.python_version(),sympy=s.__version__,
    arithmetic="Exact integers and rational numbers",core_records=core_records,
    smith_certificates=certificates,J3_relation_basis=serialize(U),
    J3_relation_basis_inverse=serialize(U.inv()),J3_coordinates=serialize(Ucoordinates),
    core_quotient_row=serialize(quotient),core_generator=serialize(c),
    surface_records=surface_records,connecting_matrix=serialize(D),
    integral_kernel_basis=serialize(K),source_relation=serialize(r),
    domain_basis=serialize(domain_basis),
    literal_chain_boundaries=dict(surface_symbols=["u","T0_inverse_u","T_infinity_u"],
        Q0=serialize(boundary_q0),Q1=serialize(boundary_q1),
        seam_correction=serialize(boundary_a),shifted=serialize(boundary_shifted)),
    common_three_form=serialize(eta),evaluation_row=serialize(evaluation),
    evaluations=serialize(values),relation_evaluation=-1,
    fibre_evaluations=[2,4],meridian_matrix=serialize(M),full_matrix=serialize(full),
    full_inverse=serialize(full.inv()),
    results=dict(H3_W="Z^4",degree_three_kernel="0",degree_three_cokernel="0",
        H3_Y="0 for the stated actual marked cusp data",torsion=[]),
    scope="Exact actual-map homology matrices and prism boundary certificates; geometric comparison and cochain pairing are proved in the TeX source."),indent=2))
