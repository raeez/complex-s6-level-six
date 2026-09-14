# Toric cusp construction

Status: a complete local candidate is ready for independent review. No independent acceptance is asserted.

The question is the marked toric cusp with periods `(q c1,c2)` and `(c3,q c4)`. The four functions are specified holomorphic units. The section has a holomorphic unit lift after an integral period translation. These local data are hypotheses. Their identification with another geometric family remains an external obligation.

All writes remain in the two assigned directories of this worktree. No staging, commit, push, native integration, publication, or worktree cleanup occurred.

## Mathematical result

The source constructs the smooth toric quotient from the periodic unimodular fan. It gives the actual central fibre as a quotient of a hexagon times an angular two-torus. It constructs the whole marked boundary map, including its positive meridian homotopy. It proves a mapping-cylinder comparison with the smooth local neighborhood.

The resulting integral homology ranks are `(1,2,4,2,1)`, without torsion. The specialization is surjective in every degree. Its kernel equals the image of exterior monodromy minus the identity. The dual image is the full integral invariant lattice.

The smooth family of units is retained. Its transport preserves the section, the map to the disk, the complex orientation, and the full period marking.

## First stage and source policy

`source-freeze.json` records the live cusp024 bytes before editing. `first-stage.md` records the geometric derivation before the historical review reports were read. This was a source-informed derivation, not a fresh-context certification. The earlier common-chain verdict was read only afterward and was not imported as proof of this cusp.

Primary PDFs were retrieved again from their author sites. Their URLs and SHA-256 values are in `sources/manifest.json`.

- Engel, *Complex structures on S6*, Propositions 2.7–2.9, printed pages 5–7: the punctured periods, fan, and section used as local input. No global conclusion is imported.
- Nakayama–Ogus, *Relative rounding in toric and logarithmic geometry*, Theorem 5.1: physical author-preprint page 40, printed page 1040. The theorem requires a proper, separated, exact, relatively smooth morphism, fine target, and relatively coherent source. The manuscript checks these conditions using the diagonal monoid charts and the proved quotient properness.

The research contract requests `gpt-6-astra` and `ultra`. Independently observed runtime controls are unavailable and remain unverified. This records an operational constraint and a verification limit, not authorship.

## Decisive constructions

1. **Moment sign and edge gluing**, `toric-cusp.tex:142`. The polygon uses negative moment coordinates. On a divisor, its two surviving homogeneous coordinates give an explicit weighted endpoint formula. The adjacent component has endpoints shifted by `-Qn`. Its residual character agrees because its exponent annihilates `n`. This proves the actual edge gluing and fixes the seam sign.
2. **Full marked specialization**, `toric-cusp.tex:273`. The polar seam changes local angle by `-vn` and moment coordinate by `-Qn`. Hence `theta=phi-v Q^{-1}y` is invariant. The endpoint relation is the positive shear. The forgetful map is `[y,theta+v Q^{-1}y]`.
3. **Radial marking**, `toric-cusp.tex:343`. Character phases detect both angular periods. The unquotiented polar covering detects both period translations. These invariants persist through radial transport. A fibre translation corrects the radial bundle isomorphism to fix the entire section.
4. **Unit transport**, `toric-cusp.tex:381`. The local horizontal fields preserve the disk coordinate. Their derivatives of branch coordinates are smoothly divisible by those coordinates. This property survives the partition of unity and proves liftability to polar spaces. Mere tangency would not suffice.
5. **Actual finite cells**, `toric-cusp.tex:440`. The quotient has chain ranks `(2,3,4,2,1)`. The degree-one incidence matrix has three columns `(-1,1)`. Opposite polygon edges cancel in the higher incidences. Characteristic maps define these cells on the actual quotient.
6. **Integral result**, `toric-cusp.tex:529`. The source and target contractible pairs are integral. The resulting specialization matrices have only unit Smith factors. The kernel formulas and dual invariant lattice follow over the integers.
7. **Boundary homotopy and marking**, `toric-cusp.tex:593`. The interval-first cubical homotopy satisfies `dH+Hd=pT-p`. The cone map is `K(a,b)=p(a)+H(b)`. The separate common-chain path-convention repair was not changed.

## Exact evidence

Run from the worktree root:

```text
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/check_cusp.py > reports/research/s6_cusp026/exact-checks.json
python3 research-candidates/s6_cusp026/verify_certificates.py > reports/research/s6_cusp026/certificate-verification.json
/opt/homebrew/bin/python3 research-candidates/s6_cusp026/build.py
```

The first calculation derives vertex and edge identifications from the polygon coordinates. It constructs the product and quotient chain complexes, then checks all chain identities. It uses symbolic seam parameters, rather than a sample of angles. It verifies the cone determinants, homology, exterior monodromy, and all marked specialization matrices.

Each Smith result retains left and right unimodular matrices. The second calculation checks all 28 certificates with standard-library integer and rational arithmetic. It does not use SymPy.

The main calculation used Python 3.14.6 and SymPy 1.14.0. The second verification used the system Python. Exact executable versions and build inputs are retained in the evidence files.

The final PDF has 10 pages. The build converged in four passes. All 289 external and local build inputs have recorded hashes. The log has no overflow, missing-character, duplicate-anchor, or unresolved-reference diagnostic.

All 10 final pages were rasterized and visually inspected. Their final images are in `render/`. No clipping, missing formulas, empty pages, or manuscript-firewall violation appeared. Text extraction has more than 2,400 characters on each page. The PDF metadata contains only mathematical publication metadata.

The images directly in `build/` preserve an earlier exploratory render. They are not the final render. The `render/` directory binds the final PDF.

## Failed route preserved

The complete angular collapse has target `H/Gamma`, a two-torus. It has zero fourth homology and Euler characteristic. The actual central fibre retains the toric four-cell, has fourth homology `Z`, and has Euler characteristic two. Thus the complete collapse cannot supply the actual local attachment. This failure does not refute the toric filling.

Ordinary positive moment coordinates would reverse the seam displacement used with the selected period action. The present proof uses the explicitly defined negative moment coordinate. It does not infer the boundary map from monodromy ranks alone.

Tangency of a smooth field to a complex divisor does not by itself imply smooth divisibility by a branch coordinate. The transport proof derives divisibility from holomorphic coordinate changes before applying the smooth partition of unity.

## Residual obligations

The independent exact review and integration are owned by the coordinator. The candidate does not self-certify.

Identification of the supplied periods and section with a specified global family remains outside this local theorem. Smooth lifted translations at the finite punctures are not constructed here. The full global integral cone is not evaluated. No conclusion about a complex structure on the six-sphere follows from this local candidate alone.

The source module is `research-candidates/s6_cusp026/toric-cusp.tex`. Its wrapper is `paper.tex`. Its only nonstandard typesetting dependency is the canonical shared template, linked without a local fork. The module uses the `c26:` label prefix and the bibliography keys `CuspEngel` and `CuspNO`.
