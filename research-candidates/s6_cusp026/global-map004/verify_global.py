"""Verify the integral certificate with independent standard-library arithmetic."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
import platform


def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def det(a):
    if not a:
        return 1
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
               for j in range(len(a)))


def inverse(a):
    n = len(a)
    result = [[Fraction(v) for v in row]+[Fraction(i==j) for j in range(n)]
              for i,row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j,n) if result[i][j])
        result[j],result[pivot] = result[pivot],result[j]
        scale = result[j][j]
        result[j] = [v/scale for v in result[j]]
        for i in range(n):
            if i != j:
                scale = result[i][j]
                result[i] = [x-scale*y for x,y in zip(result[i],result[j])]
    output = [row[n:] for row in result]
    assert all(x.denominator == 1 for row in output for x in row)
    return [[int(x) for x in row] for row in output]


def ext2(a):
    pairs = list(combinations(range(len(a)),2))
    return [[a[i][k]*a[j][l]-a[i][l]*a[j][k]
             for k,l in pairs] for i,j in pairs]


report = Path(__file__).resolve().parents[3]/"reports/research/s6_cusp026/global-map004"
data = json.loads((report/"exact-checks.json").read_text())
for name,certificate in data["smith_certificates"].items():
    m,left,right,d = [certificate[k] for k in ["matrix","left","right","diagonal"]]
    assert mul(mul(left,m),right) == d, name
    assert abs(det(left)) == abs(det(right)) == 1, name
    assert all(not x or i == j for i,row in enumerate(d) for j,x in enumerate(row)), name
    factors = [abs(d[i][i]) for i in range(min(len(d),len(d[0]))) if d[i][i]]
    assert factors == certificate["factors"]
    assert all(b%a == 0 for a,b in zip(factors,factors[1:]))

B0 = [[0,-1,-1,4],[0,0,-1,2],[1,1,1,-6],[0,0,0,1]]
B1 = [[1,1,0,-1],[0,1,0,-1],[0,-1,1,3],[0,0,0,1]]
local = [[[1,-1,0,1,0,0],[0,0,-1,0,-1,-1]],
         [[2,1,0,-1,0,0],[0,0,0,0,0,-2]]]
computed = [mul(local[i],ext2(inverse(b))) for i,b in enumerate([B0,B1])]
J2 = computed[0]+[[-v for v in row] for row in computed[1]]
assert J2 == data["smith_certificates"]["J2"]["matrix"]
u = data["global_relation_basis"]
assert det(u) == 1
assert inverse(u) == data["global_relation_basis_inverse"]
coords = mul(inverse(u),J2)
assert coords == [[3,1,0,-2,0,0],[0,0,0,0,1,0],
                  [0,0,0,0,0,1],[0,0,0,0,0,0]]
assert mul([[2,4,2,3]],J2) == [[0]*6]
assert mul([[2,4,2,3]],[[0],[-1],[0],[1]]) == [[-1]]

T0 = [[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]]
T1 = [[-1,1,-1,2],[-1,0,-1,1],[1,1,2,-1],[0,0,0,1]]
alpha = [[[1],[0],[-1],[0]],[[0],[-1],[1],[0]]]
for j,a in enumerate(alpha):
    a_next = mul(inverse(T0),a)
    assert mul(inverse(T1),a_next) == a
    difference = [[a[i][0]-a_next[i][0]] for i in range(4)]
    assert difference == [[j+1],[0],[0],[0]]
    assert difference == data["actual_cusp_chains"][j]["connecting"]
assert [[alpha[1][i][0]-2*alpha[0][i][0]] for i in range(4)] == [[-2],[-1],[3],[0]]
assert det(data["meridian_attachment"]) == 1
print(json.dumps({"python":platform.python_version(),
    "arithmetic":"Standard-library integers and fractions",
    "certificates_verified":len(data["smith_certificates"]),
    "covering_maps_recomputed_from_coordinate_bases":True,
    "primitive_relation_lattice_verified":True,
    "meridian_connecting_vectors_recomputed":True,
    "scope":"Finite arithmetic verification; geometric comparison requires source review."},indent=2))
