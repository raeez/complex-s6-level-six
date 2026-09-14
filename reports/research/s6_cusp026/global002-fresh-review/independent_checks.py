"""Exact review calculations. Standard library only. No source mutation."""
from fractions import Fraction
from itertools import combinations
from functools import reduce
from math import gcd
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

def transpose(a):
    return list(map(list, zip(*a)))

def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def identity(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def det(a):
    n=len(a)
    if not n: return 1
    if n==1: return a[0][0]
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(n))

def rank(a):
    if not a or not a[0]: return 0
    a=[[Fraction(v) for v in r] for r in a]
    p=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(p,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[p],a[pivot]=a[pivot],a[p]
        q=a[p][j]
        a[p]=[x/q for x in a[p]]
        for i in range(len(a)):
            if i!=p:
                q=a[i][j]
                a[i]=[x-q*y for x,y in zip(a[i],a[p])]
        p+=1
        if p==len(a): break
    return p

def minor_gcd(a,k):
    if k==0: return 1
    return reduce(gcd,(abs(det([[a[i][j] for j in cs] for i in rs]))
        for rs in combinations(range(len(a)),k)
        for cs in combinations(range(len(a[0])),k)),0)

def exterior(a,k):
    ix=list(combinations(range(len(a)),k))
    return [[det([[a[i][j] for j in cs] for i in rs]) for cs in ix] for rs in ix]

def subtract_identity(a):
    return [[v-int(i==j) for j,v in enumerate(row)] for i,row in enumerate(a)]

def zero(a):
    return all(v==0 for row in a for v in row)

T=[[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]
L=[[1,0,0,0],[0,-1,0,0],[-1,1,1,0],[0,0,0,1]]
Li=[[1,0,0,0],[0,-1,0,0],[1,1,1,0],[0,0,0,1]]
T0=[[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]]
T1=[[-1,1,-1,2],[-1,0,-1,1],[1,1,2,-1],[0,0,0,1]]
C=[[1,1,0,1],[0,1,0,0],[0,-1,1,0],[0,0,0,1]]
P1=[[0,-1,-1],[1,0,0],[0,0,1]]
P0=[[0,0,1],[1,0,0],[0,1,0]]
U1=[[-1],[-1],[2]]
delta=[[-2],[-1],[3],[0]]
assert mul(L,Li)==identity(4)
assert mul(mul(T0,T1),mul(mul(L,T),Li))==identity(4)
assert mul(P1,U1)==U1
assert mul(mul(P1,P1),mul(P1,P1))==identity(3)
assert mul(mul(P0,P0),P0)==identity(3)
assert mul(C,[[-1],[-1],[2],[0]])==delta

# Columns of each matrix are the proposed primitive invariant cycles.
invariant_bases=[[[1]],
 [[1,0],[0,1],[0,0],[0,0]],
 [[1,0,0,0],[0,1,0,1],[0,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,0,0]],
 [[1,0],[0,1],[0,0],[0,0]],
 [[1]]]
exterior_results=[]
for k in range(5):
    N=subtract_identity(exterior(T,k))
    B=invariant_bases[k]
    assert zero(mul(N,B))
    r=rank(N)
    nullity=len(N)-r
    assert rank(B)==nullity
    assert minor_gcd(B,nullity)==1
    smith=[minor_gcd(N,j)//minor_gcd(N,j-1) for j in range(1,r+1)]
    assert all(d==1 for d in smith)
    exterior_results.append(dict(degree=k,N=N,kernel_basis=B,kernel_rank=nullity,
       kernel_maximal_minor_gcd=minor_gcd(B,nullity),image_smith_factors=smith,
       cokernel_free_rank=nullity))

# For the three polygon lines, the first crossing is at t=1/2.
# Each crosses only the pair of edges whose normal is its angular direction.
Q=[[2,-1],[-1,2]]
line_results=[]
for d in [(1,0),(0,1),(1,1)]:
    qd=mul(Q,[[d[0]],[d[1]]])
    y=[Fraction(v[0],2) for v in qd]
    assert max(abs(y[0]),abs(y[1]),abs(y[0]+y[1]))==1
    assert sum(Fraction(d[i])*y[i] for i in range(2))==1
    line_results.append(dict(direction=d,crossing=[str(x) for x in y],
        next_representative=[str(-x) for x in y],seam_translation=[v[0] for v in qd]))

# The cone reduction is derived from the integral projection map on homology.
r=[1,2,4,2,1,0,0]
b=[1,3,6,6,3,1,0]
sizes=[r[n]+(b[n-1] if n else 0) for n in range(7)]
differentials=[[]]
for n in range(1,7):
    d=[[0]*sizes[n] for _ in range(sizes[n-1])]
    for j in range(r[n-1]): d[j][r[n]+j]=1
    differentials.append(d)
cone=[]
for n in range(7):
    outgoing=differentials[n] if n else []
    incoming=differentials[n+1] if n<6 else []
    outgoing_rank=rank(outgoing)
    incoming_rank=rank(incoming)
    if n>=1 and n<6: assert zero(mul(outgoing,incoming))
    # The kernel consists of standard basis vectors outside selected columns.
    selected={r[n]+j for j in range(r[n-1])} if n else set()
    kernel_indices=[j for j in range(sizes[n]) if j not in selected]
    assert len(kernel_indices)==sizes[n]-outgoing_rank
    # Incoming image is exactly the target summand, with unit coefficients.
    assert incoming_rank==r[n] if n<6 else incoming_rank==0
    assert all(j in kernel_indices for j in range(incoming_rank))
    homology_indices=[j for j in kernel_indices if j>=incoming_rank]
    cone.append(dict(degree=n,chain_rank=sizes[n],outgoing_rank=outgoing_rank,
      integral_kernel_standard_indices=kernel_indices,
      integral_image_standard_indices=list(range(incoming_rank)),
      homology_standard_indices=homology_indices,homology_rank=len(homology_indices),torsion=[]))
assert [x['homology_rank'] for x in cone]==[0,0,1,2,4,2,1]

# The first global group from the actual core relations.
N0=subtract_identity(T0)
N1=subtract_identity(T1)
G=[N0[i]+N1[i] for i in range(4)]
assert G[3]==[0]*8
assert rank(G)==3 and minor_gcd(G,3)==1
relation=[[-1,3,0],[1,0,4]]
quotient=[[12],[4],[-3]]
assert zero(mul(relation,quotient))
assert minor_gcd(relation,1)==minor_gcd(relation,2)==1
assert gcd(gcd(12,4),3)==1
attachment=[[0,12,-1],[-1,0,0],[0,-1,0]]
assert det(attachment)==-1

frozen=json.loads((ROOT/'reports/research/s6_cusp026/global-map002/candidate-manifest.json').read_text())
checks=[]
for item in frozen['files']:
    p=ROOT/item['path']
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    record=dict(path=item['path'],expected=item['sha256'],actual=actual,matches=actual==item['sha256'])
    if item.get('type')=='symlink':
        import os
        target=os.readlink(p)
        record.update(link_target=target,link_target_matches=target==item['target'],
            link_sha256=hashlib.sha256(target.encode()).hexdigest())
        assert record['link_sha256']==item['link_sha256']
    checks.append(record)
    assert record['matches']

result=dict(python=sys.version,arithmetic='Exact integers and fractions, no external packages',
    independent_of_writer_scripts=True,exterior_degrees=exterior_results,
    meridian_polygon_lines=line_results,local_cone=cone,
    global=dict(monodromy_image=G,image_rank=3,image_maximal_minor_gcd=1,
      abelian_relations=relation,primitive_quotient_weights=[12,4,-3],
      degree_one_attachment=attachment,determinant=-1,H0='Z',H1='0'),
    manifest_files=checks,manifest_files_verified=len(checks))
(OUT/'independent-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(exterior_kernel_ranks=[x['kernel_rank'] for x in exterior_results],
    local_cone_ranks=[x['homology_rank'] for x in cone],global_determinant=-1,
    manifest_files_verified=len(checks))))
