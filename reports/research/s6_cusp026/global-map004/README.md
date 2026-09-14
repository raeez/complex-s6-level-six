# Meridian tori in the common real attachment

Status: constructed, exactly checked, and rendered. Independent mathematical acceptance remains pending.

The bounded result computes the actual two-torus inclusion into `H2(W)`. It does not certify a complex six-sphere family. The inherited `global-map002` manuscript and all earlier candidate bytes remain unchanged.

## Result

For the two specified finite fillings, the actual manifold `W` is homotopy equivalent to the double mapping cylinder `G0 <- F -> G1`. The equivalence retains the finite meridian homotopies. The fibre maps are the actual degree-three and degree-four coverings in the matrices `B0` and `B1`.

The resulting integral sequence is

```text
0 -> Z c -> H2(W) -> Z e1 -> 0,
c = -S0 + S1.
```

Here `Si` is the positive core mapping torus of the primitive invariant vector `Ui`. The actual cusp tori `zj=M(alpha_j)` have connecting images `e1` and `2e1`. The common invariant vector is `delta=alpha2-2 alpha1`, and its global cusp torus is exactly `-S0+S1`.

Consequently `H2(W)=Z t + Z c`, with `t=b_infinity(z1)`, and

```text
           z1  z2
t           1   2
c           0   1
```

The map has image all of `H2(W)` and kernel zero. Its determinant is one. Under the actual marked cusp specialization hypotheses from `global-map002`, this supplies `H2(Y_top)=0`. The standalone manuscript states those local hypotheses explicitly, so the independent global theorem does not depend on acceptance of the still-unreviewed local attachment comparison.

## Deciding chains and relations

For `a4=0` and `T_infinity a=a`, set `a'=T0^-1 a`. Let `Ri` be the first three rows of `Bi^-1`. The actual core squares are

```text
Q0(a)(v,s) = [s R0 a, -v],
Q1(a')(v,s) = [s R1 a', v].
```

Their boundaries are `f0(ell(a')-ell(a))` and `f1(ell(a)-ell(a'))`. Thus

```text
(Q0(a), Q1(a'), ell(a)-ell(a'))
```

is an actual cycle in the cone of `(f0,-f1)`. Its connecting image is `(I-T0^-1)a`. These formulas retain literal singular loop differences before passing to lattice classes.

In the core surface basis `(A0,S0,A1,S1)`, the fibre relation matrix is

```text
 3  1  0 -2  0  0
 0  0  0  0  0 -1
-3 -1  0  2 -3 -1
 0  0  0  0  2  2
```

Columns 2, 5, and 6, followed by `c=(0,-1,0,1)`, form a determinant-one matrix. Therefore the entire incoming relation subgroup is saturated and the quotient is `Z c`. This is an integral basis proof, not rank subtraction.

The covering-map matrices include their fibre coefficients. The Wang projection supplies the norm component. Invariant constant two-forms evaluate the remaining fibre component and prove it is zero for covered mixed tori. This closes the possible correction term before the Smith calculation.

## Dependency and claim boundaries

The standalone source defines the marked real filling directly in core product coordinates. Substituting `a=Bi(y,t)` into the unchanged finite boundary maps from `common-chain.tex` gives the same maps. In particular, the conormal shifts remain in the fourth columns of `Bi`; they are not omitted.

The new core calculation reconstructs `H1(W)=Z`, `e4=12g`, and the cusp meridian `-g`. Together with the stated local cusp data, the degree-one attachment is the same determinant-minus-one matrix as in `global-map002`.

The dependency chain is:

1. Explicit finite quotient markings and actual boundary maps.
2. A spine retraction with the two meridian homotopies.
3. The double mapping cylinder and its integral chain cone.
4. Integral bases of the core surface groups and actual fibre matrices.
5. Global relations, explicit cusp squares, and the primitive class `c`.
6. The unconditional real-attachment theorem `H2(W)=Z^2` and its two-torus isomorphism.
7. The conditional consequence `H2(Y_top)=0` using the actual marked cusp map.

The broad question remains the complex family for every sufficiently small nonzero parameter and every permitted primitive increment. The present theorem addresses the specified pair only. The punctured-family comparison relative to all three boundaries and the section remains required. So do the smooth equivariant finite translations, proper quotients, conormal comparisons, and the remaining global homology.

## Checks and reproduction

Run from the assigned worktree root:

```text
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/global-map004/check_global.py > reports/research/s6_cusp026/global-map004/exact-checks.json
python3 research-candidates/s6_cusp026/global-map004/verify_global.py > reports/research/s6_cusp026/global-map004/certificate-verification.json
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/global-map004/build.py
pdftoppm -scale-to 1500 -png reports/research/s6_cusp026/global-map004/build/paper.pdf reports/research/s6_cusp026/global-map004/render/page
pdftotext -layout reports/research/s6_cusp026/global-map004/build/paper.pdf reports/research/s6_cusp026/global-map004/render/paper.txt
```

The first exact calculation uses Python 3.14.6 and SymPy 1.14.0. The second uses Python 3.9.6 with standard-library integers and fractions. It checks eight complete unimodular Smith certificates, independently reconstructs both covering matrices from the coordinate bases, and recomputes the cusp connecting vectors. These are separate arithmetic implementations, not independent mathematical acceptance lanes.

The finite computation verifies its stated relation lattice and actual square endpoint data. The proof of the topological comparison and the integral core bases remains in the TeX source. No full higher-dimensional simplicial incidence array is claimed.

The PDF has seven pages. The final build converges in two passes, with 289 recorded input hashes. No overflow, unresolved reference, duplicate identifier, or missing-character diagnostic remains. Every final page was inspected as a raster. The final source and extracted text contain no manuscript-firewall violation. Legitimate mathematical uses of “CW model” and “chain model” were manually distinguished from prohibited production narration.

An initial build stopped at a missing `end{equation}`. It was repaired before the converged build. Visual inspection found two malformed spacing commands. Both were repaired, and the affected pages were rendered and inspected again. The final hashes bind only the corrected source and render.

The primary PDF at `https://philip-engel.github.io/S6.pdf` was fetched and hashed. It matches the stored source byte-for-byte. Its role here is motivation and the original geometric question. The global map is derived from the explicit finite maps, not imported from the primary manuscript's homology conclusion.

## Scope and remaining acceptance

Only `research-candidates/s6_cusp026/global-map004/` and `reports/research/s6_cusp026/global-map004/` were written. No staging, commit, push, central PDF copy, reader opening, or child dispatch occurred.

The supplied `global003` partials could not be located in the assigned worktree or programme worktrees. The available `global002-fresh-review/independent_checks.py` was read as evidence to inspect, without importing a verdict. Its source is frozen in `input-freeze.json`.

Operational controls require `gpt-6-astra` and `ultra`. Independently observed runtime metadata were unavailable and remain unverified. This is an operational limitation, not proof evidence.

Fresh acceptance should inspect the cylinder equivalence with its marked cusp path, the core basis and fibre-component calculation, the signed square boundaries, and the exact frozen artifact. The local `global-map002` comparison still requires its separate acceptance. Higher global homology is outside this bounded calculation.
