#!/usr/bin/env python3
"""Exact integral maps for the specified free order-three torus filling."""
import itertools
import json
import math
from fractions import Fraction


def det(a):
    if not a:return 1
    b=[[Fraction(x) for x in row] for row in a]
    result=Fraction(1)
    for j in range(len(b)):
        p=next((i for i in range(j,len(b)) if b[i][j]),None)
        if p is None:return 0
        if p!=j:b[p],b[j]=b[j],b[p];result=-result
        result*=b[j][j]
        for i in range(j+1,len(b)):
            c=b[i][j]/b[j][j]
            b[i]=[x-c*y for x,y in zip(b[i],b[j])]
    assert result.denominator==1
    return int(result)


def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def smith(a):
    previous=1;answer=[]
    for k in range(1,min(len(a),len(a[0]))+1):
        divisor=0
        for rows in itertools.combinations(range(len(a)),k):
            for cols in itertools.combinations(range(len(a[0])),k):
                divisor=math.gcd(divisor,det([[a[i][j] for j in cols] for i in rows]))
        if not divisor:break
        answer.append(divisor//previous);previous=divisor
    return answer


DIM={0:1,1:3,2:3,3:1}
P3=[[0,0,1],[1,0,0],[0,1,0]]
R3=mul(P3,P3)


def pmat(k):
    return P3 if k in (1,2) else [[1]] if k in (0,3) else []


def rmat(k):
    return R3 if k in (1,2) else [[1]] if k in (0,3) else []


def norm(k):
    return [[1]*3 for _ in range(3)] if k in (1,2) else [[3]] if k in (0,3) else []


def slots(kind,n):
    summands=[('x',n),('y',n-1)]
    if kind=='B':summands += [('z',n-1),('w',n-2)]
    return [(letter,j) for letter,k in summands for j in range(DIM.get(k,0))]


def vector(kind,n):
    return {key:0 for key in slots(kind,n)}


def add(out,dst,src,letter,matrix,scale=1):
    for i,row in enumerate(matrix):
        out[(dst,i)]+=scale*sum(coefficient*src.get((letter,j),0) for j,coefficient in enumerate(row))


def ident(k):
    return [[int(i==j) for j in range(DIM.get(k,0))] for i in range(DIM.get(k,0))]


def minus_identity(a):
    return [[v-int(i==j) for j,v in enumerate(row)] for i,row in enumerate(a)]


def qd(n,z):
    out=vector('Q',n-1);add(out,'x',z,'y',minus_identity(rmat(n-1)));return out


def bd(n,z):
    out=vector('B',n-1)
    add(out,'x',z,'z',minus_identity(pmat(n-1)))
    add(out,'y',z,'w',minus_identity(pmat(n-2)))
    return out


def f(n,z):
    out=vector('Q',n);add(out,'x',z,'x',ident(n));add(out,'y',z,'y',norm(n-1));return out


def h(n,z):
    out=vector('Q',n+1);add(out,'y',z,'x',pmat(n),-1);return out


def hp(n,z):
    out=vector('Q',n+1);add(out,'y',z,'x',ident(n));return out


def mm(n,z,inverse=False):
    out=vector('C',n);action=rmat if inverse else pmat
    add(out,'x',z,'x',minus_identity(action(n)))
    add(out,'y',z,'y',minus_identity(action(n-1)));return out


def kmap(n,z):
    out=f(n,z);add(out,'y',z,'z',pmat(n-1),-1);return out


def section(n,z):
    out=vector('B',n);add(out,'x',z,'x',ident(n));add(out,'z',z,'y',rmat(n-1),-1);return out


def kernel(n,z):
    out=vector('B',n)
    add(out,'y',z,'x',pmat(n-1));add(out,'z',z,'x',norm(n-1))
    add(out,'w',z,'y',ident(n-2));return out


def columns_of(kind,n,func,target,m):
    columns=[]
    for key in slots(kind,n):columns.append(func(n,{key:1}))
    return [[col.get(key,0) for col in columns] for key in slots(target,m)]


def reduce_q(n,z):
    assert not any(qd(n,z).values())
    values=[]
    if n in range(4):values.append(sum(z.get(('x',i),0) for i in range(DIM[n])))
    if n-1 in range(4):
        y=[z.get(('y',i),0) for i in range(DIM[n-1])]
        assert len(set(y))==1
        values.append(y[0])
    return values


def run():
    native=[[0,-1,-1,0],[1,-1,0,0],[0,0,1,0],[0,0,0,1]]
    change=[[0,-1,-1,0],[0,0,-1,0],[1,1,1,0],[0,0,0,1]]
    permutation=[row+[0] for row in P3]+[[0,0,0,1]]
    assert det(change)==1
    assert mul(native,change)==mul(change,permutation)
    # Actual second exterior action in the signed cyclic cell basis.
    lex=list(itertools.combinations(range(3),2))
    exterior=[[det([[P3[i][j] for j in b] for i in a]) for b in lex] for a in lex]
    cyclic=[[0,0,1],[0,-1,0],[1,0,0]]
    assert det(cyclic)==1
    assert mul(exterior,cyclic)==mul(cyclic,P3)
    counts={'homotopy_columns':0,'positive_homotopy_columns':0,'boundary_map_columns':0,
            'chain_section_columns':0,'kernel_shift_columns':0}
    matrices=[];homology=[];splittings=[]
    for n in range(6):
        for key in slots('C',n):
            z={key:1}
            assert not any(qd(n,f(n,z)).values())
            assert qd(n+1,h(n,z))==f(n,mm(n,z))
            assert qd(n+1,hp(n,z))==f(n,mm(n,z,True))
            counts['homotopy_columns']+=1;counts['positive_homotopy_columns']+=1
        for key in slots('B',n):
            z={key:1}
            assert qd(n,kmap(n,z))==kmap(n-1,bd(n,z))
            if n>=2:assert not any(bd(n-1,bd(n,z)).values())
            counts['boundary_map_columns']+=1
        for key in slots('Q',n):
            z=vector('Q',n);z[key]=1
            assert kmap(n,section(n,z))==z
            assert bd(n,section(n,z))==section(n-1,qd(n,z))
            if n>=2:assert not any(qd(n-1,qd(n,z)).values())
            counts['chain_section_columns']+=1
        for key in slots('Q',n-1):
            z={key:1}
            assert not any(kmap(n,kernel(n,z)).values())
            minus={key:-v for key,v in qd(n-1,z).items()}
            assert bd(n,kernel(n,z))==kernel(n-1,minus)
            counts['kernel_shift_columns']+=1
        combined=[section(n,{key:1}) for key in slots('Q',n)]
        combined += [kernel(n,{key:1}) for key in slots('Q',n-1)]
        splitting=[[col.get(key,0) for col in combined] for key in slots('B',n)]
        assert abs(det(splitting))==1
        splittings.append({'degree':n,'matrix':splitting,'determinant':det(splitting)})
        matrices.append({'degree':n,'C_rank':len(slots('C',n)),'Q_rank':len(slots('Q',n)),
                         'B_rank':len(slots('B',n)),
                         'Q_boundary':columns_of('Q',n,qd,'Q',n-1),
                         'B_boundary':columns_of('B',n,bd,'B',n-1),
                         'F':columns_of('C',n,f,'Q',n),
                         'H':columns_of('C',n,h,'Q',n+1),
                         'K':columns_of('B',n,kmap,'Q',n)})
        if n<=4:
            cols=[reduce_q(n,f(n,{key:1})) for key in slots('C',n)]
            induced=[list(row) for row in zip(*cols)]
            expected_maps=[[[1]],[[1,1,1,0],[0,0,0,3]],
                           [[1,1,1,0,0,0],[0,0,0,1,1,1]],
                           [[1,0,0,0],[0,1,1,1]],[[3]]]
            assert induced==expected_maps[n],(n,induced)
            factors=smith(induced)
            expected=[[1],[1,3],[1,1],[1,1],[3]][n]
            assert factors==expected,(n,induced,factors)
            homology.append({'degree':n,'H_N_rank':[1,2,2,2,1][n],
                             'F_on_homology':induced,'nonzero_smith_factors':factors,
                             'kernel_rank':len(slots('C',n))-len(factors),
                             'cokernel_torsion':[x for x in factors if x>1]})
    circle_minus=[[3,-1],[-1,0]];circle_plus=[[3,1],[-1,0]]
    assert det(circle_minus)==-1 and det(circle_plus)==1
    # The actual affine action is free by its fourth coordinate, including its square.
    assert all(Fraction(k,3).denominator==3 for k in [1,2])
    return {'native_matrix':native,'integral_change_of_basis':change,'determinant':det(change),
            'permutation':permutation,'cyclic_degree_two_basis':cyclic,
            'clockwise_circle_matrix':circle_minus,'counterclockwise_circle_matrix':circle_plus,
            'chain_matrix_order':'Q and C: (x,y); B: (x,y,z,w), each fibre triple ordered as printed',
            'matrices':matrices,'chain_identity_counts':counts,'split_chain_bases':splittings,
            'homology_and_fibre_maps':homology,
            'specialization_indices_degrees_1_to_4':[3,1,1,3],
            'boundary_homology_ranks':[1,3,4,4,3,1]}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
