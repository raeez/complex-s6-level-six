# Actual cusp boundary and the first common cone groups

Status: constructed and checked; independent exact review remains pending.

This extension preserves every byte of the accepted local026 module and its manifest. It reads the accepted common-chain path repair. The input hashes are in `input-freeze.json`. Only the newly assigned `global-map002/` source and report directories were changed. No staging, commit, push, cleanup, native integration, or application-reader operation occurred.

## Result and exact boundary

The new mathematical module constructs the actual smooth boundary identification `j_infinity` from the period matrix. Its induced map `kappa_infinity` is composition of actual cubical chains with that diffeomorphism. The endpoint identity uses the same positive mapping-torus shear and right-to-left path convention as the common-chain source.

The explicit radial and boundary homotopies compare this map with `K(a,b)=p(a)+H(b)` on one common chain carrier. Degree-two and degree-three fibre matrices are retained. Their meridian terms are determined by geometric mapping-torus cycles, not omitted.

The actual boundary homology has ranks `(1,3,6,6,3,1)`, without torsion. In suitable integral bases, its map to the cusp core is `[I 0]` in degrees zero through four and zero in degree five. The complementary basis consists of actual meridian mapping tori.

The local attachment cone has homology ranks `(0,0,1,2,4,2,1)` in degrees zero through six, with no torsion. The calculation explicitly expresses incoming boundaries in an integral basis of outgoing cycles. Its bridge to the actual map is a proved contraction of finite free complexes with free homology, applied after the meridian map is identified.

For the specified common topological attachment, the degree-one map is

```text
          beta1 beta2 gammaInfinity
g           0    12       -1
coreBeta1  -1     0        0
coreBeta2   0    -1        0
```

Its determinant is `-1`. The actual global cone therefore has `H0=Z` and `H1=0`. This is the first global cone homology calculation. The complete global cone homology is not claimed.

## Mathematical anchors

All anchors refer to `research-candidates/s6_cusp026/global-map002/cusp-attachment.tex`.

- Lines 1–85: smooth marked boundary identification, actual cubical `kappa_infinity`, cone-compatible radial comparison, and the degree-two and degree-three matrices.
- Lines 87–177: primitive integral invariant lattices and actual meridian mapping-torus representatives. The degree-two kernel is represented by the squares `(v,s) -> [s alpha_j,v]`. Their cusp images are independent of `v`.
- Lines 179–254: the contraction formula `U=h_A f+i_A p_A f h_B`, the reduced differential matrices, and the integral local cone homology proof.
- Lines 256–367: the explicit real finite fillings, common chain cone, marking, and first global Smith calculation.
- Lines 369 onward: the next exact global map and the external geometric obligations.

The local reduced complex has ranks `(1,3,7,8,7,3,1)`. Its differential ranks are `(1,2,4,2,1,0)`. Every nonzero Smith factor is one. The proof identifies the quotient of each integral cycle group by its incoming boundary subgroup; rank subtraction is not the only evidence.

## Deciding geometric cycles

For an invariant subtorus `V`, its mapping torus `M(V)` maps under the Wang projection to `[V]`. The invariant bases in degrees zero through four are

```text
1
alpha1, alpha2
alpha1 alpha2, alpha1 beta1, alpha2 beta2,
    (alpha1+alpha2)(beta1+beta2)
alpha1 alpha2 beta1, alpha1 alpha2 beta2
alpha1 alpha2 beta1 beta2
```

The corresponding meridian mapping tori lie in the kernel of the actual cusp map. Purely angular cycles lose the meridian parameter. The diagonal subtori use polygon lines in directions `(1,0)`, `(0,1)`, and `(1,1)`, whose seam translations have those same directions. Their angular shifts stay in the stated subtorus. Their cusp images therefore factor through spaces of strictly smaller dimension. The top boundary class maps into the four-dimensional toric core.

These factorizations establish the integral kernel splitting before any homology reduction of chains. They also prevent the complete angular-collapse model from entering the calculation.

## Exact calculations and build

Run from the worktree root:

```text
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/global-map002/check_attachment.py > reports/research/s6_cusp026/global-map002/exact-checks.json
python3 research-candidates/s6_cusp026/global-map002/verify_certificates.py > reports/research/s6_cusp026/global-map002/certificate-verification.json
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/global-map002/build.py
```

The calculation uses Python 3.14.6 and SymPy 1.14.0. It verifies primitive invariant bases, exterior monodromy compatibility, the actual marked homology maps, and every reduced differential. For each degree it computes a kernel basis and writes the incoming differential in that basis. The retained Smith certificates include unimodular left and right changes of basis.

The second verifier uses only standard-library integer arithmetic and rational determinant elimination. All 35 Smith certificates pass that verification.

The standalone dependency closure includes the unchanged accepted local026 module followed by the new attachment module. Its build has 16 pages and no overflow, missing-character, duplicate-reference, or unresolved-reference diagnostic. `build.json` records the exact command and all 294 input hashes. The final PDF and raster hashes are bound by the candidate manifest.

All final pages are rasterized and visually inspected before the freeze. The source, extracted text, and metadata are checked for manuscript-firewall violations. Operational records remain in this report tree.

## First remaining maps

The next global calculation is now a concrete quotient:

```text
H2(Y_top) = H2(W) / < bInfinity_* z1, bInfinity_* z2 >,
zj(v,s) = [s alpha_j,v].
```

It requires the images of these two actual meridian tori in the finite common complex and an integral presentation of `H2(W)`. This extension does not compute that matrix or higher global groups.

The first external family comparison must identify the original punctured torus bundle with the specified flat bundle relative to all three boundary markings and the section. At the finite punctures, the lifted translation on each reduced divisor torsor must extend smoothly, commute with the cyclic deck action, and have a proper quotient with the prescribed periods. The section must retain the conormal comparisons `e=s^-2 e'` at order three and `e=s^-1 e'` at order four. These are map-level existence and compatibility obligations. The monodromy matrices do not establish them.

No global complex structure or six-sphere conclusion is asserted. The computed real topological attachment is not identified with an unconstructed global complex family.

## Review and controls

This extension is synthesis from the accepted local geometry and accepted common-chain conventions. It is not an independent review of either source. The local PASS does not accept this extension.

The mathematical contract requires `gpt-6-astra` and `ultra`. Independently observed runtime metadata remain unavailable and unverified. No child work was delegated.
