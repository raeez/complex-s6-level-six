from pathlib import Path
import hashlib
import json

root = Path(__file__).parent
catalogue = Path('/Users/raeez/mathematics/worktrees/frontier-catalogue-20260913/reports/research/COVERAGE-2026-09-13/semantic/documents')
recovery = Path('/Users/raeez/mathematics/worktrees/frontier-recovery-astra-ultra-20260913/reports/research/RECOVERY-2026-09-13/returns')


def source(path, anchors):
    p = Path(path)
    data = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'anchors': anchors}


def document(prefix, anchors):
    matches = list((catalogue / prefix[:2]).glob(prefix + '*.txt'))
    assert len(matches) == 1
    return source(matches[0], anchors)


def returned(name, anchors):
    return source(recovery / name, anchors)


sw = 'sw002_g08--p01-final-01.md'
syn = 'critique_groups_02_08--g05--s001-final-01.md'
rows = []


def claim(id, statement, sources, disposition, destination, proof, residual):
    rows.append(dict(id=id, mathematical_statement=statement, sources=sources,
                     disposition=disposition, destination=destination,
                     proof_or_counterexample=proof, residual_obligation=residual,
                     confidence='Proof supplied in the named manuscript scope; independent acceptance pending.'))


claim('S6-M01', 'The marked rank-four lattice has invariant form coefficients (3,1,0,-2,0,-2), contraction i_delta xi=-6 psi, and Smith factors (1,1,6,6).',
      [returned(sw, ['1-25']), returned(syn, ['116-140']), document('ca34f4b3', ['paper Sections 1-2']), document('c07ad511', ['complete public computation input'])],
      'PREEXISTING_SOURCE_RETAINED_AND_EXACTLY_RECOMPUTED', 'paper.tex, Theorem 1.1; scripts/check_two_fibre.py',
      'Integer basis matrix has determinant -1 and congruence J plus 6J; contraction and all determinantal divisors checked.',
      'No new proof of the full complex-threefold construction is claimed.')
claim('S6-M02', 'ker(psi)/Z delta is a unimodular alternating plane.',
      [returned(syn, ['116-140'])], 'INTEGRATED_UNCONSUMED_RESULT', 'paper.tex, prop:reduction',
      'The displayed unimodular basis restricts to J plus zero on ker(psi); quotient removes exactly the primitive radical.', 'None within the stated lattice.')
claim('S6-M03', 'The discriminant pairing gives a six-dimensional irreducible finite Heisenberg representation; it does not specify vertex operations or a physical theory.',
      [returned('critique_groups_02_08--g05--p002-final-02.md', ['33-97']), returned(syn, ['116-140', 'H23'])],
      'PREEXISTING_SOURCE_RETAINED_WITH_GENERALIZATION', 'paper.tex, Section 2 and thm:double',
      'Pairing is induced by inverse alternating form; character projectors and translations prove irreducibility. The doubled presentation gives a separate general finite carrier.',
      'A VOA/QFT application still requires fields, products, state spaces, anomaly and sewing comparisons.')
claim('S6-M04', 'The two-fibre presentation has first Smith divisor d=gcd(r,s,m,n), determinant Delta=rn+sm-rsb0, and a free summand when Delta=0.',
      [returned(sw, ['26-38']), returned(syn, ['142-159']), document('0150f260', ['PR-AFFINE-TRANS'])],
      'PREEXISTING_SOURCE_CONSUMED_IN_NEW_PAIRING_THEOREM', 'paper.tex, Theorem 3.1, thm:extension, thm:double',
      'New quotient and doubled forms use this actual matrix. All 38720 chosen integer cases satisfy the determinantal-divisor calculations.',
      'Formal non-effective data do not define primitive meridional fillings.')
claim('S6-M05', 'For effective rank-one data, the primitive coarse carrier is lcm(r,s), with coefficient Delta/gcd(r,s).',
      [returned(sw, ['39-64']), document('ca34f4b3', ['Section 4'])],
      'PREEXISTING_SOURCE_CONSUMED_IN_INTEGRAL_EXTENSION', 'paper.tex, Theorem 4.1 and prop:leray-extension',
      'Kollar Propositions 43,47 and Corollary 44 supply the sheaf and differential. The new filtration sequence has cyclic middle H2 of order |Delta|.',
      'Transport to an arbitrary affine torus fibration still requires an actual map of constructible sheaves.')
claim('S6-M06', 'The global class has torsion invisible to its rational degree.',
      [returned(sw, ['39-64']), document('ca34f4b3', ['Section 4, equations 4.9-4.14'])],
      'INTEGRATED_EXPLICIT_GENERALIZATION', 'paper.tex, eq:class-coordinates and thm:extension',
      'Bezout coordinates give epsilon=kU+tT with gT=0, k=Delta/g, t=bm-an. The quotient gives all Smith factors and a split extension exactly when gcd(g,k) divides t.',
      'No canonical identification of algebraic and Leray filtrations is asserted; their cyclic factors occur in opposite orders.')
claim('S6-M07', 'Effective two-fibre linking needs oriented meridional slopes in addition to the group order.',
      [document('0150f260', ['PR-AFFINE-TRANS; orientation and section data']), returned(syn, ['142-159'])],
      'CONSTRUCTED_UNCONSUMED_EXTENSION', 'paper.tex, thm:linking',
      'With m alpha+r beta=1, q=s beta-(n-sb0) alpha, the meridian relation is mu1=q mu0+Delta lambda0. Disk chain D1-qD0-B gives linking -q/Delta.',
      'This symmetric torsion form is attached to the explicit oriented three-manifold, not to an arbitrary presentation or to Engel H1 of the smooth torus fibre.')
claim('S6-M08', 'An alternating pairing for the general two-fibre arithmetic exists on the doubled cokernel, with full invariant factors.',
      [document('0150f260', ['PR-AFFINE-TRANS']), returned('critique_groups_02_08--g05--p002-final-02.md', ['33-80'])],
      'CONSTRUCTED_UNCONSUMED_EXTENSION', 'paper.tex, thm:double and eq:arithmetic-pairing',
      'The block matrix (0,A;-A^T,0) has elementary divisors (d,|Delta|/d); its inverse gives x^T A^-T y-prime minus x-prime^T A^-T y. At rank drop, quotient by the primitive radical gives dJ.',
      'The doubled lattice is an explicit arithmetic construction; a geometric comparison is not supplied.')
claim('S6-M09', 'Primitive torsion does not guarantee a free local affine action.',
      [returned(sw, ['89-102'])], 'CONTRADICTED_BY_EXACT_FIXED_POINTS_AND_REPAIRED', 'paper.tex, prop:affine-free and following examples',
      'T0 with delta0/3 fixes -(e1+e2)/3; the square of T1 with delta1/4 fixes -(f1+f2)/4. The new proof gives the exact free boundary gcd(m,3)=gcd(n,4)=1 in these markings.',
      'Nonfree quotient stabilizers and their global topology remain outside the free-filling theorem.')
claim('S6-M10', 'The (3,4) topological presentation or transgression cannot identify its arithmetic discriminant with the fibre discriminant.',
      [returned(sw, ['65-107']), returned(syn, ['142-159'])], 'REFUTED_PUTATIVE_IDENTIFICATION_WITH_EXACT_SEPARATION', 'paper.tex, prop:separation',
      'Effective (3,4) data imply gcd(p,12)=1, so the arithmetic double type (1,|p|) cannot equal (1,6). At |p|=1 the arithmetic discriminant is zero.',
      'An abstract isometry at non-effective (3,4;3,-2) supplies no geometric map.')
claim('S6-M11', 'The current Engel PDF uses different theorem locators from the older paper citations.',
      [returned(sw, ['89']), source(root/'primary-sources.json', ['Engel exact PDF identity'])],
      'SOURCE_LOCATORS_CORRECTED_AND_PINNED', 'paper.tex, Engel bibliography and citations throughout Sections 1 and 5',
      'Verified current 25-page PDF hash 81ad7344...: Theorem 5.1, Proposition 6.1, Lemmas 7.2,7.5,7.6; total-space Theorem 4.1.',
      'This source-locator repair does not certify the complete analytic or S6 theorem.')
claim('S6-M12', 'A stopped public calculation of the level-six Smith form left no completed output in that event.',
      [document('1cd6c09d', ['complete stopped notification']), document('4264b6cd', ['complete stopped notification']), document('c07ad511', ['complete separate public calculation input'])],
      'STOPPED_CALCULATION_RECOVERED_WITH_NEW_EXACT_INPUTS', 'scripts/check_two_fibre.py and exact-results.json',
      'A standard-library script recomputes the lattice normal form, Smith divisors and rational fixed-point identities; no missing private reasoning is reconstructed.',
      'The stopped command also concerned unrelated identities, which are outside this source assignment.')
claim('S6-M13', 'Historical papers may retain different exact source and PDF versions.',
      [returned('status_papers_exact_custody-final-01.md', ['11-13','25']), document('1ca626197084', ['complete historical nine-page source']), document('ca34f4b3', ['complete principal source'])],
      'DISTINCT_IDENTITIES_PRESERVED', 'candidate-manifest.json; primary-sources.json; source-baseline.json',
      'Principal baseline remains 5d9f632... with paper SHA ca34f4b3... . New candidate and rendered PDF receive separate hashes and no acceptance claim.',
      'Root owns integration and central working/accepted PDF placement.')

records=[]
for row in json.load(open(root/'topic-index.json')):
    p=Path(row['path'])
    records.append({'path':str(p),'sha256':p.stem,'bytes':row['bytes'],
                    'topic_anchors':[x[0] for x in row['matches']],
                    'disposition':'DISCOVERY_INDEX_ONLY_UNCONSUMED_OUTSIDE_EXPLICIT_CLAIM_ROWS',
                    'read_scope':'Keyword search and bounded source selection. No whole-record semantic acceptance.',
                    'remaining_obligation':'Resolve any additional mathematical argument not covered by an explicit claim row before counting this record as consumed.'})
result={'scope':'Lattice, Smith, rank-one Seifert, affine freeness and finite Heisenberg source candidate.',
        'claim_dispositions':rows,
        'broad_catalogue_search':{'documents_scanned':480202,'hits':1332,'method':'all-topic-paths.txt and topic-index.json',
                                  'claim':'Discovery completeness for the recorded query, not complete semantic reading or programme completion.'},
        'record_dispositions':records,
        'returns_manifest':'returns-manifest-049.json',
        'public_record_policy':'Use surfaced mathematics and public computation inputs. No reconstruction of unavailable private or stopped reasoning.',
        'independent_acceptance':'pending root-assigned review of frozen bytes'}
(root/'mining-dispositions.json').write_text(json.dumps(result,indent=2)+'\n')
print('claim rows',len(rows),'preserved discovery records',len(records))
