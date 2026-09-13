# The Level-Six Fibre Lattice and Two-Fibre Linking Forms

The note identifies Engel's smooth-fibre lattice `H_1(F,Z)`, reconstructs its
integral monodromy and distinguished classes, and proves
`iota_delta xi = -6 psi`. It derives the `(1,6)` discriminant pairing and finite
Heisenberg module, computes the full Smith form and Seifert Euler numerator of
a two-fibre presentation, and proves the integral Leray transgression for a
fully specified effective rank-one Seifert `C*`-bundle. Its primitive carrier
has index `lcm(r,s)` and coefficient `Delta/gcd(r,s)`; the full global Seifert
class has additional `Z/gcd(r,s)` torsion invisible to that coarse
transgression. Engel's rank-four torus transgression remains a separate
geometric `(3,4)` calculation, and no general affine-torus transgression is
asserted.

The integral Seifert class has explicit coordinates `epsilon = k U + t T`,
with `g T = 0`. Its quotient presentation determines the complete invariant
factors and the splitting criterion. The effective two-solid-torus filling
has a symmetric torsion linking coefficient `-q/Delta`, calculated from
a Bezout longitude with a fixed boundary orientation.

For arbitrary local integers, the doubled relation matrix defines a separate
alternating lattice with elementary divisors `(d, |Delta|/d)`. Its
discriminant pairing and Heisenberg representation include non-effective
data and the zero-determinant reduction. Effective `(3,4)` data have
`gcd(Delta,12)=1`, so this arithmetic double never has the level-six fibre
type. A free-action criterion and two exact fixed-point examples specify
the affine quotient hypotheses.

Run `make check` to build the paper and execute the exact integer and rational
calculations. The calculation script uses only the Python standard library.
