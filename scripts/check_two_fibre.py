#!/usr/bin/env python3
"""Exact certificates for the two-fibre presentations and their pairings."""
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from functools import reduce
import json
import platform


def det(a):
    n = len(a)
    ans = 0
    for p in permutations(range(n)):
        sign = (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = sign
        for i in range(n):
            term *= a[i][p[i]]
        ans += term
    return ans


def smith_by_minors(a):
    previous = 1
    result = []
    for k in range(1, len(a) + 1):
        minors = [det([[a[i][j] for j in cols] for i in rows])
                  for rows in combinations(range(len(a)), k)
                  for cols in combinations(range(len(a)), k)]
        divisor = reduce(gcd, minors, 0)
        result.append(divisor // previous if previous else 0)
        previous = divisor
    return result


def bezout(x, y):
    old_r, r, old_s, s, old_t, t = x, y, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def mv(a, x):
    return [sum(u * v for u, v in zip(row, x)) for row in a]


def add(x, y):
    return [a + b for a, b in zip(x, y)]


def arithmetic(r, s, m, n, section):
    nu = n - s * section
    delta = r * nu + s * m
    d = gcd(gcd(r, s), gcd(m, n))
    g = gcd(r, s)
    R, S = r // g, s // g
    _, a, b = bezout(S, R)
    ell = g * R * S
    k, t = delta // g, b * m - a * n
    A = [[r, s], [-m, nu]]
    E = [[k, 0], [t, g]]
    expected = [d, abs(delta) // d] if delta else [d, 0]
    assert smith_by_minors(A) == expected
    assert smith_by_minors(E) == expected
    assert gcd(gcd(g, k), t) == d
    assert a * S + b * R == 1
    assert det([[a, R], [b, -S]]) == -1
    assert k == -ell * section + S * m + R * n
    for j in [-2, -1, 0, 1, 2]:
        changed_t = (b - S * j) * m - (a + R * j) * n
        assert (changed_t - t + j * k) % g == 0
    if gcd(r, m) == gcd(s, n) == 1:
        _, alpha, beta = bezout(m, r)
        q = s * beta - nu * alpha
        assert q * r + delta * alpha == s
        assert -q * m + delta * beta == nu
        assert gcd(q, delta) == 1
        assert d == 1
        if not delta:
            assert r == s and m + n == r * section
        else:
            for j in [-2, -1, 0, 1, 2]:
                new_q = s * (beta - m * j) - nu * (alpha + r * j)
                assert new_q == q - j * delta
                assert (Fraction(-q, delta) - Fraction(-new_q, delta)).denominator == 1
        if r == 3 and s == 4:
            assert gcd(delta, 12) == 1
    return A, E, delta, d, k, t


def quotient_representatives(a):
    D = det(a)
    assert D
    adj = [[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]]
    def key(x):
        return tuple(v % abs(D) for v in mv(adj, x))
    reps = {key([0, 0]): [0, 0]}
    queue = [[0, 0]]
    for x in queue:
        for step in ([1, 0], [0, 1]):
            y = add(x, step)
            if key(y) not in reps:
                reps[key(y)] = y
                queue.append(y)
    assert len(reps) == abs(D)
    return queue


def check_pairing(a):
    D = det(a)
    xreps = quotient_representatives(a)
    yreps = quotient_representatives(transpose(a))
    invt = [[Fraction(a[1][1], D), Fraction(-a[1][0], D)],
            [Fraction(-a[0][1], D), Fraction(a[0][0], D)]]
    def pair(x, y):
        return sum(u * v for u, v in zip(x, mv(invt, y))) % 1
    rows = {tuple(pair(x, y) for y in yreps) for x in xreps}
    cols = {tuple(pair(x, y) for x in xreps) for y in yreps}
    assert len(rows) == len(cols) == abs(D)
    for x in xreps:
        for y in yreps:
            for step in ([1, 0], [0, 1]):
                assert pair(add(x, mv(a, step)), y) == pair(x, y)
                assert pair(x, add(y, mv(transpose(a), step))) == pair(x, y)
    return len(xreps) * len(yreps)


count = rank_drops = effective = 0
for r, s, m, n, section in product(range(1, 9), range(1, 9), range(-5, 6), range(-5, 6), range(-2, 3)):
    A, E, delta, d, k, t = arithmetic(r, s, m, n, section)
    count += 1
    rank_drops += delta == 0
    effective += gcd(r, m) == gcd(s, n) == 1

examples = []
for args in [(2, 2, -1, -1, 0), (2, 2, -1, -1, -1),
             (2, 3, 1, 1, 0), (2, 4, 2, 2, 0), (2, 4, 2, -4, 0),
             (3, 4, 1, -1, 0), (3, 4, 3, -2, 0), (6, 10, 2, 4, 1),
             (1, 1, 0, 0, 0), (3, 3, 0, 0, 0)]:
    A, E, delta, d, k, t = arithmetic(*args)
    gram = [[0, 0, *A[0]], [0, 0, *A[1]],
            [-A[0][0], -A[1][0], 0, 0], [-A[0][1], -A[1][1], 0, 0]]
    snf = smith_by_minors(gram)
    assert snf == ([d, d, abs(delta) // d, abs(delta) // d] if delta else [d, d, 0, 0])
    row = dict(parameters=args, A=A, extension_matrix=E, delta=delta, d=d,
               k=k, t=t, gram_smith=snf)
    if delta:
        row['pairing_entries_verified'] = check_pairing(A)
    r, s, m, n, section = args
    if delta and gcd(r, m) == gcd(s, n) == 1:
        _, alpha, beta = bezout(m, r)
        q = s * beta - (n - s * section) * alpha
        row.update(alpha=alpha, beta=beta, q=q, linking=str(Fraction(-q, delta) % 1))
    examples.append(row)

T0 = [[0, -1, -1, 0], [1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
T1 = [[0, 1, 0, 0], [-1, 0, -1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
C = [[1, 1, 0, 1], [0, 1, 0, 0], [0, -1, 1, 0], [0, 0, 0, 1]]
M = [[0, 3, 1, 0], [-3, 0, -2, 0], [-1, 2, 0, -2], [0, 0, 2, 0]]
P = [[1, 0, 2, -2], [0, 0, 1, 0], [0, 1, -3, 0], [0, 0, 0, 1]]
delta0, delta1 = [-2, -1, 3, 0], [-1, -1, 2, 0]
assert mv(C, delta1) == delta0
assert matmul([delta0], M) == [[0, 0, 0, -6]]
assert matmul(matmul(transpose(P), M), P) == [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 6], [0, 0, -6, 0]]
assert smith_by_minors(M) == [1, 1, 6, 6]
x0 = [Fraction(-1, 3), Fraction(-1, 3), 0, 0]
x1 = [Fraction(-1, 4), Fraction(-1, 4), 0, 0]
assert [v + Fraction(a, 3) - w for v, a, w in zip(mv(T0, x0), delta0, x0)] == [0, 0, 1, 0]
assert [v + Fraction(a, 2) - w for v, a, w in zip(mv(matmul(T1, T1), x1), delta1, x1)] == [0, 0, 1, 0]

print(json.dumps(dict(python=platform.python_version(), arithmetic_cases=count,
                     zero_determinant_cases=rank_drops, effective_cases=effective,
                     parameter_box={'r_s': [1, 8], 'm_n': [-5, 5], 'b0': [-2, 2]},
                     examples=examples, fibre_smith=[1, 1, 6, 6],
                     fixed_point_counterexamples='both exact rational identities verified',
                     scope='Exact finite checks; general claims depend on the manuscript proofs.'), indent=2))
