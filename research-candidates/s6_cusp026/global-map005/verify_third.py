"""Recompute the degree-three data using standard-library exact arithmetic."""
from fractions import Fraction as Q
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
    n=len(a)
    b=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next(i for i in range(j,n) if b[i][j])
        b[j],b[p]=b[p],b[j]
        z=b[j][j]
        b[j]=[x/z for x in b[j]]
        for i in range(n):
            if i!=j:
                z=b[i][j]
                b[i]=[x-z*y for x,y in zip(b[i],b[j])]
    return [r[n:] for r in b]


def exterior(a,k):
    rows=list(combinations(range(len(a)),k))
    cols=list(combinations(range(len(a[0])),k))
    return [[det([[a[i][j] for j in cc] for i in rr]) for cc in cols] for rr in rows]


def add(a,b):
    return [[x+y for x,y in zip(r,t)] for r,t in zip(a,b)]


def scale(a,q):
    return [[q*x for x in r] for r in a]


def rational(a):
    return [[Q(x) for x in r] for r in a]


report=Path(__file__).resolve().parents[3]/"reports/research/s6_cusp026/global-map005"
data=json.loads((report/"exact-checks.json").read_text())
for name,v in data["smith_certificates"].items():
    a,l,r,d=[v[k] for k in ["matrix","left","right","diagonal"]]
    assert mul(mul(l,a),r)==d,name
    assert abs(det(l))==abs(det(r))==1,name
    assert all(not x or i==j for i,row in enumerate(d) for j,x in enumerate(row))
    f=[abs(d[i][i]) for i in range(min(len(d),len(d[0]))) if d[i][i]]
    assert f==v["factors"]
    assert all(y%x==0 for x,y in zip(f,f[1:]))

T0=[[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]]
T1=[[-1,1,-1,2],[-1,0,-1,1],[1,1,2,-1],[0,0,0,1]]
B0=[[0,-1,-1,4],[0,0,-1,2],[1,1,1,-6],[0,0,0,1]]
B1=[[1,1,0,-1],[0,1,0,-1],[0,-1,1,3],[0,0,0,1]]
f0=mul([[1,0,0,0],[0,1,-1,1]],exterior(inverse(B0),3))
f1=mul([[1,0,0,0],[0,4,2,-2]],exterior(inverse(B1),3))
assert f0==[[1,6,2,-4],[0,3,1,-2]]
assert f1==[[1,-3,-1,1],[0,6,2,-4]]
j3=f0+scale(f1,-1)
assert j3==data["smith_certificates"]["J3"]["matrix"]
u=data["J3_relation_basis"]
assert det(u)==1
assert mul(inverse(u),j3)==[[1,0,0,0],[0,3,1,0],[0,0,0,1],[0,0,0,0]]

v=[[-1,0,0,0],[1,1,0,1],[0,0,0,1],[-1,0,0,-1],[0,0,-1,-1],[0,0,1,0]]
ident=[[int(i==j) for j in range(6)] for i in range(6)]
dd=mul(add(ident,scale(exterior(inverse(T0),2),-1)),v)
assert dd==data["connecting_matrix"]
assert mul(dd,[[-2],[0],[-3],[2]])==[[0] for _ in range(6)]
assert det(data["domain_basis"])==-1
assert mul(dd,data["domain_basis"])==[row+[0] for row in data["integral_kernel_basis"]]
assert mul(data["smith_certificates"]["J2"]["matrix"],data["integral_kernel_basis"])==[[0]*3 for _ in range(4)]

r0=inverse(B0)[:3]
r1=inverse(B1)[:3]
evaluation=add(scale(mul([[1,-1,1]],exterior(r0,2)),-Q(2,3)),
               scale(mul([[2,1,-1]],exterior(mul(r1,inverse(T0)),2)),Q(1,2)))
assert evaluation==rational(data["evaluation_row"])
values=mul(evaluation,v)
assert values==[[0,-Q(1,6),-1,-2]]
assert mul(values,[[-2],[0],[-3],[2]])==[[-1]]
eta0=mul([[0,2,-2,2]],exterior(inverse(B0),3))
eta1=mul([[0,4,2,-2]],exterior(inverse(B1),3))
assert eta0==eta1==[[0,6,2,-4]]
L=[[1,0,0,0],[0,-1,0,0],[-1,1,1,0],[0,0,0,1]]
assert mul(eta0,exterior(L,3))==[[0,0,2,4]]

# Verify literal chain closure before identifying the surface chains in homology.
b=data["literal_chain_boundaries"]
assert add(b["Q0"],b["shifted"])==[[0,0,0]]
assert add(add(b["Q1"],scale(b["seam_correction"],-1)),scale(b["shifted"],-1))==[[0,0,0]]
full=data["full_matrix"]
assert det(full)==1
assert inverse(full)==data["full_inverse"]
assert mul(data["meridian_matrix"],[[-2],[0],[-3],[2]])==[[0],[0],[0],[-1]]
print(json.dumps(dict(python=platform.python_version(),arithmetic="Standard-library integers and fractions",
    smith_certificates_verified=len(data["smith_certificates"]),
    covering_maps_reconstructed=True,integral_global_relations_verified=True,
    connecting_map_recomputed=True,literal_seam_boundary_verified=True,
    matching_three_forms_recomputed=True,primitive_relation_evaluation=-1,
    full_degree_three_determinant=1,scope="Finite exact calculations; source proof supplies geometric comparisons and map identifications."),indent=2))
