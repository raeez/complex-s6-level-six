# Two-fibre arithmetic and pairing candidate

The candidate adds explicit integral extension data and pairings to the existing
level-six fibre paper. It also repairs the affine free-action hypothesis.
Independent acceptance of these exact bytes is pending.

## Mathematical construction

The global two-fibre class has a basis `U,T`, with `g T = 0`, in which
`epsilon = k U + t T`. Here `g = gcd(r,s)`, `k = Delta/g`, and `t` is an
explicit Bezout expression in `m,n`. The quotient has relation matrix
`[[k,0],[t,g]]`. Its Smith factors agree with those of the actual filling
presentation, and its finite extension splits exactly when `gcd(g,k)` divides
`t`. For effective local data the coarse Leray sequence has cyclic middle
cohomology of order `|Delta|`; it splits exactly when `gcd(g,k)=1`.
The algebraic and Leray sequences have their cyclic factors in opposite order.
The paper does not identify their filtrations.

The effective filling is defined by two primitive meridians on an oriented
torus. A Bezout longitude gives `mu1 = q mu0 + Delta lambda0`.
The integral disk chain `D1-qD0-B` computes the symmetric linking value
`-q/Delta`. This proof includes the sign, the chosen generator, independence
of the Bezout choice, orientation reversal, and the zero-determinant case.

For every integral two-fibre relation matrix `A`, the alternating double
`[[0,A],[-A^T,0]]` has elementary divisors `(d,|Delta|/d)` when nonsingular.
Its discriminant is `coker(A) + coker(A^T)`, paired by the inverse transpose.
The resulting Heisenberg representation has dimension `|Delta|` and central
order `|Delta|/d`. At determinant zero, quotienting by the primitive radical
gives the form `d J`. All these carriers are explicit.

The geometric `(3,4)` affine actions are free exactly when
`gcd(m,3)=gcd(n,4)=1`. The proof includes necessity and sufficiency, and the
primitive-torsion counterexamples remain displayed. For effective `(3,4)`
data, `gcd(Delta,12)=1`, so the arithmetic double cannot have fibre type
`(1,6)`. At `|Delta|=1` its discriminant vanishes. The original fibre
still has discriminant `(Z/6)^2`.

The previously unconsumed reduction `ker(psi)/Z delta` is now a proved
unimodular symplectic plane in the reader source.

## Source and computation evidence

The source baseline is the clean principal HEAD
`5d9f632b5d9795e51075a9c15e2ee58d4cfb40af`. Its `paper.tex` hash is
`ca34f4b3ebc27ba86d632480aa047d795978c7861610cb5926b3f3424d9c7099`.
The dedicated branch is `repair/frontier-mine-s6-20260913`.
No shared source files were changed. No staging, commit, push, or central
PDF publication occurred.

The bibliography now uses the 25-page Engel source with corrected locators.
Exact primary PDF identities and URLs are in `primary-sources.json`.
The decisive external inputs are the explicit Engel monodromy markings,
Kollar's multiplicity/sheaf/transgression statements, and the ordinary
oriented solid-torus and torsion-linking constructions of Hatcher and Hillman.
The entire complex-threefold construction is not certified by this candidate.

Run from the worktree:

```
make check
python3 -B scripts/check_two_fibre.py
pdftoppm -scale-to 1200 -png out/paper.pdf reports/research/MINING-2026-09-13/render/page
```

The script uses Python 3.9.6 and only its standard library. It independently
computes determinantal divisors by minors for 38,720 integer parameter choices,
including 762 determinant-zero cases and 17,405 effective cases. Ten worked
examples include direct finite-cokernel enumeration, pairing tables,
non-effective local fractions, and radical reduction. Exact rational
arithmetic checks both affine fixed-point identities and the original
level-six contraction and congruence. These finite calculations do not replace
the general proofs in the paper.

The latest `make check` passed. The final PDF has 17 pages. All 17 page renders
were visually inspected, and no clipping, absent glyphs, overlap, or process
language was found. The LaTeX log has no warning, unresolved reference,
overfull box, or underfull box. The source firewall scan has no hits.

## Mining scope and preserved failures

`mining-dispositions.json` contains thirteen mathematical disposition rows
with exact source identities, anchors, proofs, destinations, and residuals.
These include completed returns, rejected inferences, and a stopped public
Smith-calculation event whose corresponding mathematics was recomputed.
`relevant-returns.json` preserves all ten topical returns found in the assigned
`returns-manifest-049.json`.

The broader retained catalogue was searched with the recorded topic query.
All 1,332 matching records are preserved in the disposition ledger, including
metadata, false-positive uses of "two fibres", and distinct archival copies.
This is a discovery index, not a claim to have semantically read all 923 MB of
matching records. The unconsumed status is explicit for every record outside
the named mathematical rows. No private or missing interrupted reasoning was
reconstructed. Additional unique arguments in that broader search remain a
mining obligation before whole-corpus closure.

The following failed implications are preserved with their mathematical
remedies: primitive torsion implies freeness; scalar transgression determines
the integral extension; a presentation determines its geometric pairing;
nonprimitive filling slopes are ordinary meridians; a cyclic torsion group has
a perfect alternating form; equal numerical levels identify geometric
carriers; and an inverse-matrix pairing survives determinant zero unchanged.

Remaining mathematical obligations are the topology of the nonfree affine
quotients, a general higher-rank affine transgression comparison, and the
geometric/physical constructions needed for any VOA or QFT interpretation.
The candidate proves no priority claim and no complete complex-S6 theorem.

Root owns independent exact-candidate review, integration, and any placement
in the central working or accepted PDF directories. Any changed manuscript
byte requires a new freeze and renewed whole-candidate review.
