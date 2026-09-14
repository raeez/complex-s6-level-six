#!/usr/bin/env python3
"""Exact signed integral maps for the marked positive filling."""
import itertools
import json
from fractions import Fraction
from pathlib import Path

namespace={}
exec(compile(Path(__file__).with_name('check_filling.py').read_text(),
             'check_filling.py','exec'),namespace)
old=namespace['run']()
det=namespace['det'];mul=namespace['mul'];smith=namespace['smith']
slots=namespace['slots'];vector=namespace['vector'];add=namespace['add']
pmat=namespace['pmat'];ident=namespace['ident'];norm=namespace['norm']
minus=namespace['minus_identity'];bd=namespace['bd'];f=namespace['f']
hp=namespace['hp'];mm=namespace['mm'];columns=namespace['columns_of']


def inverse(a):
    n=len(a)
    b=[[Fraction(v) for v in row]+[Fraction(i==j) for j in range(n)]
       for i,row in enumerate(a)]
    for j in range(n):
        k=next(k for k in range(j,n) if b[k][j]);b[k],b[j]=b[j],b[k]
        z=b[j][j];b[j]=[v/z for v in b[j]]
        for k in range(n):
            if k!=j:
                z=b[k][j];b[k]=[v-z*w for v,w in zip(b[k],b[j])]
    out=[row[n:] for row in b]
    assert all(v.denominator==1 for row in out for v in row)
    return [[int(v) for v in row] for row in out]


def qd(n,z):
    out=vector('Q',n-1);add(out,'x',z,'y',minus(pmat(n-1)));return out


def kmap(n,z):
    out=f(n,z);add(out,'y',z,'z',ident(n-1));return out


def section(n,z):
    out=vector('B',n);add(out,'x',z,'x',ident(n));add(out,'z',z,'y',ident(n-1));return out


def kernel(n,z):
    out=vector('B',n);add(out,'y',z,'x',ident(n-1),-1)
    add(out,'z',z,'x',norm(n-1));add(out,'w',z,'y',ident(n-2));return out


def exterior(a,n):
    subsets=list(itertools.combinations(range(4),n))
    return [[det([[a[i][j] for j in col] for i in row]) for col in subsets] for row in subsets]


def polyadd(a,b,scale=1):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,0)+scale*v
    return {k:v for k,v in out.items() if v}


def polymul(a,b):
    out={}
    for i,v in a.items():
        for j,w in b.items():out[i+j]=out.get(i+j,0)+v*w
    return {k:v for k,v in out.items() if v}


def run():
    T=old['native_matrix'];A=mul(T,T)
    V=[[0,-1,-1,4],[0,0,-1,2],[1,1,1,-6],[0,0,0,1]]
    assert det(V)==1 and mul(T,V)==mul(V,old['permutation'])
    delta=[-2,-1,3,0];e4=[0,0,0,1]
    assert [V[i][3] for i in range(4)]==[e4[i]-2*delta[i] for i in range(4)]
    affine=[Fraction(delta[i]+e4[i],3) for i in range(4)]
    transformed=[sum(inverse(V)[i][j]*affine[j] for j in range(4)) for i in range(4)]
    assert transformed==[1,1,1,Fraction(1,3)]
    # The exact discriminant after the actual Weierstrass substitution.
    aa={1:3,4:-3};bb={0:2,3:-4,6:2}
    disc=polyadd({k:-64*v for k,v in polymul(polymul(aa,aa),aa).items()},
                 {k:-432*v for k,v in polymul(bb,bb).items()})
    assert disc=={0:-1728,3:5184,6:-5184,9:1728}
    assert (-4)%3==2 and (-6)%3==0 and (-2)%3==1
    counts=dict(F=0,H=0,K=0,section=0,kernel=0,native_H=0)
    rows=[]
    dsubsets={0:[()],1:[(0,),(1,),(2,)],2:[(1,2),(2,0),(0,1)],3:[(0,1,2)]}
    for n in range(6):
        for key in slots('C',n):
            z={key:1};assert not any(qd(n,f(n,z)).values());counts['F']+=1
            assert qd(n+1,hp(n,z))==f(n,mm(n,z));counts['H']+=1
        for key in slots('B',n):
            z={key:1};assert qd(n,kmap(n,z))==kmap(n-1,bd(n,z));counts['K']+=1
        for key in slots('Q',n):
            z=vector('Q',n);z[key]=1
            assert kmap(n,section(n,z))==z
            assert bd(n,section(n,z))==section(n-1,qd(n,z));counts['section']+=1
            assert not any(qd(n-1,qd(n,z)).values())
        for key in slots('Q',n-1):
            z={key:1};assert not any(kmap(n,kernel(n,z)).values())
            assert bd(n,kernel(n,z))==kernel(n-1,{k:-v for k,v in qd(n-1,z).items()})
            counts['kernel']+=1
        cols=[section(n,{key:1}) for key in slots('Q',n)]
        cols += [kernel(n,{key:1}) for key in slots('Q',n-1)]
        split=[[col.get(key,0) for col in cols] for key in slots('B',n)]
        assert abs(det(split))==1
        row={'degree':n,'Q_boundary':columns('Q',n,qd,'Q',n-1),
             'F':columns('C',n,f,'Q',n),'H':columns('C',n,hp,'Q',n+1),
             'K':columns('B',n,kmap,'Q',n),'section':columns('Q',n,section,'B',n),
             'kernel_shift':columns('Q',n-1,lambda _,z:kernel(n,z),'B',n),
             'split_basis_determinant':det(split)}
        if n<=4:
            lex=list(itertools.combinations(range(4),n))
            cell_words=dsubsets.get(n,[])+[(3,)+v for v in dsubsets.get(n-1,[])]
            change=[[det([[V[i][j] for j in col] for i in rs]) for col in cell_words] for rs in lex]
            assert abs(det(change))==1
            back=inverse(change);Mn=exterior(T,n)
            nativeF=mul(row['F'],back);nativeH=mul(row['H'],back)
            left=mul(columns('Q',n+1,qd,'Q',n),nativeH) if n<4 else [[0]*len(lex) for _ in slots('Q',n)]
            right=mul(nativeF,minus(Mn))
            assert left==right;counts['native_H']+=len(lex)
            FH=mul(old['homology_and_fibre_maps'][n]['F_on_homology'],back)
            assert smith(FH)==[[1],[1,3],[1,1],[1,1],[3]][n]
            if n==1:assert FH==[[0,0,1,6],[0,0,0,3]]
            row.update(cell_words=cell_words,cell_to_original=change,original_to_cell=back,
                       native_exterior_monodromy=Mn,F_original=nativeF,H_original=nativeH,
                       F_homology_original=FH,smith_factors=smith(FH))
        rows.append(row)
    return {'old_local_calculation':old,'positive_native_matrix':T,'actual_linear_deck':A,
            'marked_cell_basis_V':V,'det_V':det(V),'V_inverse':inverse(V),
            'native_affine_increment':[str(x) for x in affine],
            'combined_affine_in_marked_cells':[str(x) for x in transformed],
            'weierstrass_discriminant_coefficients':disc,
            'conormal_order':-2,'central_character_exponent_mod3':1,
            'native_meridian_cubed_vector':[4,2,-6,1],
            'chain_identity_column_counts':counts,'positive_matrices':rows,
            'mathematical_scope':'Exact integer verification of printed maps; smooth reduction existence and commuting linearization are explicit geometric hypotheses.'}


if __name__=='__main__':print(json.dumps(run(),indent=2))
